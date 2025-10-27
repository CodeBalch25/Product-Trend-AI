"""
Common Pydantic schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict
from core.constants import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None

    model_config = {"json_schema_extra": {
        "example": {
            "success": True,
            "message": "Operation completed successfully",
            "data": {"id": 123}
        }
    }}


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None

    model_config = {"json_schema_extra": {
        "example": {
            "success": False,
            "error": "Resource not found",
            "detail": "Product with ID 123 does not exist",
            "error_code": "PRODUCT_NOT_FOUND"
        }
    }}


class PaginationParams(BaseModel):
    """Pagination parameters"""
    limit: int = Field(default=DEFAULT_PAGE_LIMIT, ge=1, le=MAX_PAGE_LIMIT)
    offset: int = Field(default=0, ge=0)

    @field_validator('limit')
    @classmethod
    def validate_limit(cls, v: int) -> int:
        """Ensure limit is within bounds"""
        if v > MAX_PAGE_LIMIT:
            return MAX_PAGE_LIMIT
        return v
