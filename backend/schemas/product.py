"""
Product-related Pydantic schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class ProductStatusEnum(str, Enum):
    """Product status enumeration"""
    DISCOVERED = "discovered"
    ANALYZING = "analyzing"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    POSTED = "posted"
    FAILED = "failed"


class ProductResponse(BaseModel):
    """Single product response"""
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    trend_score: Optional[float] = None
    trend_source: Optional[str] = None
    search_volume: Optional[int] = None
    social_mentions: Optional[int] = None
    ai_category: Optional[str] = None
    ai_keywords: Optional[List[str]] = None
    ai_description: Optional[str] = None
    profit_potential_score: Optional[float] = None
    competition_level: Optional[str] = None
    estimated_cost: Optional[float] = None
    suggested_price: Optional[float] = None
    potential_margin: Optional[float] = None
    status: ProductStatusEnum
    approved_by_user: bool = False
    rejection_reason: Optional[str] = None
    posted_platforms: Optional[List[str]] = None
    platform_ids: Optional[Dict[str, str]] = None
    discovered_at: Optional[datetime] = None
    analyzed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    """Product list response"""
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    trend_score: Optional[float] = None
    trend_source: Optional[str] = None
    status: str
    suggested_price: Optional[float] = None
    potential_margin: Optional[float] = None
    ai_keywords: Optional[List[str]] = None
    rejection_reason: Optional[str] = None
    discovered_at: Optional[str] = None
    posted_platforms: Optional[List[str]] = None

    model_config = {"from_attributes": True}


class ProductApproveRequest(BaseModel):
    """Request to approve a product"""
    pass  # No additional fields needed, product_id from path


class ProductRejectRequest(BaseModel):
    """Request to reject a product"""
    reason: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Reason for rejection (required for ML learning)"
    )

    @field_validator('reason')
    @classmethod
    def sanitize_reason(cls, v: str) -> str:
        """Sanitize rejection reason"""
        # Remove any potentially harmful characters
        sanitized = v.strip()
        if not sanitized:
            raise ValueError("Rejection reason cannot be empty")
        return sanitized

    model_config = {"json_schema_extra": {
        "example": {
            "reason": "Product does not fit target market"
        }
    }}


class ProductPostRequest(BaseModel):
    """Request to post product to platforms"""
    platforms: List[str] = Field(
        ...,
        min_length=1,
        description="List of platform names to post to"
    )

    @field_validator('platforms')
    @classmethod
    def validate_platforms(cls, v: List[str]) -> List[str]:
        """Validate platform names"""
        valid_platforms = {
            "amazon", "ebay", "tiktok_shop",
            "facebook_marketplace", "instagram_shop",
            "etsy", "mercari"
        }
        invalid = [p for p in v if p.lower() not in valid_platforms]
        if invalid:
            raise ValueError(f"Invalid platforms: {', '.join(invalid)}")
        return [p.lower() for p in v]

    model_config = {"json_schema_extra": {
        "example": {
            "platforms": ["amazon", "ebay"]
        }
    }}
