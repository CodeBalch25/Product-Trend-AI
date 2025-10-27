"""
Database models and schema with optimized connection pooling and indexes
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, JSON, Text, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from datetime import datetime
import enum
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.DEBUG,  # Log SQL statements in debug mode
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class ProductStatus(enum.Enum):
    """Product workflow status"""
    DISCOVERED = "discovered"
    ANALYZING = "analyzing"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    POSTED = "posted"
    FAILED = "failed"


class Platform(enum.Enum):
    """Supported platforms"""
    AMAZON = "amazon"
    EBAY = "ebay"
    TIKTOK_SHOP = "tiktok_shop"
    FACEBOOK_MARKETPLACE = "facebook_marketplace"
    INSTAGRAM_SHOP = "instagram_shop"
    ETSY = "etsy"
    MERCARI = "mercari"


class Product(Base):
    """Product model for discovered trending products"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Product Information
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(200), index=True)
    image_url = Column(String(1000))
    source_url = Column(String(1000))

    # Trend Analysis
    trend_score = Column(Float, default=0.0, index=True)
    trend_source = Column(String(200), index=True)  # Where we found it trending
    search_volume = Column(Integer)
    social_mentions = Column(Integer)

    # AI Analysis
    ai_category = Column(String(200))
    ai_keywords = Column(JSON)  # List of keywords
    ai_description = Column(Text)
    profit_potential_score = Column(Float)
    competition_level = Column(String(50))  # low, medium, high

    # Pricing
    estimated_cost = Column(Float)
    suggested_price = Column(Float)
    potential_margin = Column(Float)

    # Status & Workflow
    status = Column(
        Enum(ProductStatus, values_callable=lambda x: [e.value for e in x]),
        default=ProductStatus.DISCOVERED,
        nullable=False,
        index=True
    )
    approved_by_user = Column(Boolean, default=False, index=True)
    rejection_reason = Column(Text)

    # Platform Posting Status
    posted_platforms = Column(JSON)  # List of platforms where posted
    platform_ids = Column(JSON)  # Dict of platform: listing_id

    # Metadata
    discovered_at = Column(DateTime, default=datetime.utcnow, index=True)
    analyzed_at = Column(DateTime)
    approved_at = Column(DateTime)
    rejected_at = Column(DateTime)  # Track when product was rejected (for learning)
    posted_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scan_id = Column(String(50), index=True)  # Track which scan found this product
    is_new = Column(Boolean, default=True)  # Mark as new for current scan

    # Composite indexes for common query patterns
    __table_args__ = (
        Index('idx_status_discovered_at', 'status', 'discovered_at'),
        Index('idx_status_trend_score', 'status', 'trend_score'),
        Index('idx_trend_source_status', 'trend_source', 'status'),
    )


class TrendSource(Base):
    """Tracking trend sources and their performance"""
    __tablename__ = "trend_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    source_type = Column(String(100), index=True)  # google_trends, social_media, marketplace
    url = Column(String(1000))
    enabled = Column(Boolean, default=True, index=True)

    # Performance Metrics
    products_found = Column(Integer, default=0)
    successful_posts = Column(Integer, default=0)
    last_scan = Column(DateTime, index=True)

    # Configuration
    scan_interval_minutes = Column(Integer, default=60)
    config = Column(JSON)  # Source-specific configuration

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PlatformListing(Base):
    """Track posted listings across platforms"""
    __tablename__ = "platform_listings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    platform = Column(
        Enum(Platform, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        index=True
    )

    # Platform-specific data
    platform_listing_id = Column(String(200))
    listing_url = Column(String(1000))
    listing_status = Column(String(100), index=True)  # active, sold, removed, error

    # Performance
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)

    # Metadata
    posted_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_synced = Column(DateTime)
    error_message = Column(Text)

    __table_args__ = (
        Index('idx_product_platform', 'product_id', 'platform'),
    )


class AuditLog(Base):
    """Audit log for compliance and debugging"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(200), nullable=False, index=True)
    entity_type = Column(String(100), index=True)  # product, listing, trend_source
    entity_id = Column(Integer)

    details = Column(JSON)
    user_id = Column(String(200))  # For future multi-user support

    created_at = Column(DateTime, default=datetime.utcnow, index=True)


def get_db():
    """Database session dependency with automatic cleanup"""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables with proper logging"""
    logger.info("="*60)
    logger.info("Initializing database")
    logger.info("="*60)

    try:
        # Mask sensitive parts of database URL for logging
        db_url_safe = settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'
        logger.info(f"Database URL: {db_url_safe}")
        logger.info("Creating tables...")

        # Test connection first
        with engine.connect() as conn:
            logger.info("Database connection successful")

        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        logger.info(f"Tables created: {', '.join(tables)}")
        logger.info("="*60)

        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}", exc_info=True)
        raise
