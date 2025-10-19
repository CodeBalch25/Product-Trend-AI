"""
Database models and schema
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, JSON, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum

from config.settings import settings

Base = declarative_base()

# Create database engine
engine = create_engine(settings.DATABASE_URL)
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
    title = Column(String(500), nullable=False)
    description = Column(Text)
    category = Column(String(200))
    image_url = Column(String(1000))
    source_url = Column(String(1000))

    # Trend Analysis
    trend_score = Column(Float, default=0.0)
    trend_source = Column(String(200))  # Where we found it trending
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
    status = Column(Enum(ProductStatus, values_callable=lambda x: [e.value for e in x]), default=ProductStatus.DISCOVERED)
    approved_by_user = Column(Boolean, default=False)
    rejection_reason = Column(Text)

    # Platform Posting Status
    posted_platforms = Column(JSON)  # List of platforms where posted
    platform_ids = Column(JSON)  # Dict of platform: listing_id

    # Metadata
    discovered_at = Column(DateTime, default=datetime.utcnow)
    analyzed_at = Column(DateTime)
    approved_at = Column(DateTime)
    rejected_at = Column(DateTime)  # Track when product was rejected (for learning)
    posted_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scan_id = Column(String(50))  # Track which scan found this product
    is_new = Column(Boolean, default=True)  # Mark as new for current scan


class TrendSource(Base):
    """Tracking trend sources and their performance"""
    __tablename__ = "trend_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    source_type = Column(String(100))  # google_trends, social_media, marketplace
    url = Column(String(1000))
    enabled = Column(Boolean, default=True)

    # Performance Metrics
    products_found = Column(Integer, default=0)
    successful_posts = Column(Integer, default=0)
    last_scan = Column(DateTime)

    # Configuration
    scan_interval_minutes = Column(Integer, default=60)
    config = Column(JSON)  # Source-specific configuration

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PlatformListing(Base):
    """Track posted listings across platforms"""
    __tablename__ = "platform_listings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    platform = Column(Enum(Platform, values_callable=lambda x: [e.value for e in x]), nullable=False)

    # Platform-specific data
    platform_listing_id = Column(String(200))
    listing_url = Column(String(1000))
    listing_status = Column(String(100))  # active, sold, removed, error

    # Performance
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)

    # Metadata
    posted_at = Column(DateTime, default=datetime.utcnow)
    last_synced = Column(DateTime)
    error_message = Column(Text)


class AuditLog(Base):
    """Audit log for compliance and debugging"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(200), nullable=False)
    entity_type = Column(String(100))  # product, listing, trend_source
    entity_id = Column(Integer)

    details = Column(JSON)
    user_id = Column(String(200))  # For future multi-user support

    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    print("\n" + "="*60)
    print("🔧 INITIALIZING DATABASE")
    print("="*60)

    try:
        print(f"Database URL: {settings.DATABASE_URL}")
        print("Creating tables...")

        # Test connection first
        with engine.connect() as conn:
            print("✓ Database connection successful!")

        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"✓ Tables created: {', '.join(tables)}")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"✗ Database initialization failed!")
        print(f"  Error: {str(e)}")
        print("="*60 + "\n")
        raise
