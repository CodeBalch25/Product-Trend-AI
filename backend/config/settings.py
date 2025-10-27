"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationError
from typing import Optional, List
import secrets
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Product Trend Automation"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/product_trends"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS - Environment-based configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    # API Keys - Platform Integrations
    AMAZON_SP_API_KEY: Optional[str] = None
    AMAZON_SP_API_SECRET: Optional[str] = None
    AMAZON_SP_REFRESH_TOKEN: Optional[str] = None

    EBAY_APP_ID: Optional[str] = None
    EBAY_CERT_ID: Optional[str] = None
    EBAY_DEV_ID: Optional[str] = None

    TIKTOK_SHOP_API_KEY: Optional[str] = None
    TIKTOK_SHOP_SECRET: Optional[str] = None

    FACEBOOK_APP_ID: Optional[str] = None
    FACEBOOK_APP_SECRET: Optional[str] = None
    FACEBOOK_ACCESS_TOKEN: Optional[str] = None

    # AI Services
    GROQ_API_KEY: Optional[str] = None  # FREE & FAST - Recommended
    HUGGINGFACE_API_KEY: Optional[str] = None  # FREE - Alternative
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Trend Discovery Sources
    GOOGLE_TRENDS_ENABLED: bool = True
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None

    # Security - CRITICAL: Must be set via environment variable in production
    SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_SCAN_PER_HOUR: int = 10
    TREND_SCAN_INTERVAL_MINUTES: int = 60
    MAX_PRODUCTS_PER_SCAN: int = 50

    # Compliance
    REQUIRE_MANUAL_APPROVAL: bool = True
    AUTO_POST_ENABLED: bool = False  # Must remain False for ToS compliance

    # Database Connection Pool
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: Optional[str], info) -> str:
        """Ensure SECRET_KEY is set and secure"""
        environment = info.data.get('ENVIRONMENT', 'development')

        # In production, SECRET_KEY must be set and secure
        if environment == 'production':
            if not v:
                raise ValueError(
                    "SECRET_KEY must be set in production environment. "
                    "Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
                )
            if len(v) < 32:
                raise ValueError(
                    "SECRET_KEY must be at least 32 characters in production"
                )

        # In development, generate a random key if not set
        if not v:
            generated_key = secrets.token_urlsafe(32)
            logger.warning(
                f"SECRET_KEY not set. Generated random key for {environment} environment. "
                "Set SECRET_KEY in .env for persistence."
            )
            return generated_key

        return v

    @field_validator('CORS_ORIGINS')
    @classmethod
    def validate_cors_origins(cls, v: str) -> List[str]:
        """Parse and validate CORS origins"""
        origins = [origin.strip() for origin in v.split(',')]
        return origins

    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"

    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == "development"


settings = Settings()
