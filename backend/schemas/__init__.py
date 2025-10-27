"""
Pydantic schemas for request/response validation
"""
from schemas.product import (
    ProductResponse,
    ProductListResponse,
    ProductApproveRequest,
    ProductRejectRequest,
    ProductPostRequest,
)
from schemas.analytics import (
    DashboardAnalyticsResponse,
    RejectionAnalyticsResponse,
)
from schemas.common import (
    SuccessResponse,
    ErrorResponse,
    PaginationParams,
)

__all__ = [
    "ProductResponse",
    "ProductListResponse",
    "ProductApproveRequest",
    "ProductRejectRequest",
    "ProductPostRequest",
    "DashboardAnalyticsResponse",
    "RejectionAnalyticsResponse",
    "SuccessResponse",
    "ErrorResponse",
    "PaginationParams",
]
