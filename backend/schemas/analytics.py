"""
Analytics-related Pydantic schemas
"""
from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class PlatformStats(BaseModel):
    """Platform statistics"""
    count: int
    revenue: float


class DashboardAnalyticsResponse(BaseModel):
    """Dashboard analytics response"""
    total_products: int
    pending_review: int
    approved: int
    posted: int
    rejected: int
    platform_stats: Dict[str, PlatformStats]


class InsightModel(BaseModel):
    """Single insight"""
    type: str  # warning, success, info
    title: str
    message: str
    action: str


class RejectionOverallStats(BaseModel):
    """Overall rejection statistics"""
    total_products: int
    total_rejected: int
    total_approved: int
    rejection_rate: float
    approval_rate: float


class ScoreRangeStats(BaseModel):
    """Statistics for a score range"""
    total: int
    rejected: int
    rejection_rate: float


class SourceStats(BaseModel):
    """Statistics for a trend source"""
    total: int
    rejected: int
    approved: int
    rejection_rate: float
    approval_rate: float


class RecentTrendsStats(BaseModel):
    """Recent trends statistics"""
    last_30_products: int
    recent_rejection_rate: float


class RejectionAnalyticsResponse(BaseModel):
    """Rejection analytics response"""
    overall: RejectionOverallStats
    rejection_by_reason: Dict[str, int]
    rejection_by_score_range: Dict[str, ScoreRangeStats]
    rejection_by_source: Dict[str, SourceStats]
    rejection_by_category: Dict[str, Dict[str, Any]]
    recent_trends: RecentTrendsStats
    insights: List[InsightModel]
