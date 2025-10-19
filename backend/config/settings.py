"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Product Trend Automation"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/product_trends"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

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

    # Security
    SECRET_KEY: str = "CHANGE-THIS-IN-PRODUCTION-USE-SECURE-RANDOM-KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    TREND_SCAN_INTERVAL_MINUTES: int = 60
    MAX_PRODUCTS_PER_SCAN: int = 50

    # Compliance
    REQUIRE_MANUAL_APPROVAL: bool = True
    AUTO_POST_ENABLED: bool = False  # Must remain False for ToS compliance

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
