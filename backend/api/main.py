"""
Main FastAPI application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.config.settings import settings
from backend.models.database import get_db, init_db, Product, ProductStatus, PlatformListing, TrendSource
from backend.services.trend_discovery.trend_scanner import TrendScanner
from backend.services.ai_analysis.product_analyzer import ProductAnalyzer
from backend.services.platform_integrations.platform_manager import PlatformManager

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered product trend discovery and multi-platform listing automation"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


# ==================== PRODUCT ENDPOINTS ====================

@app.get("/api/products", response_model=List[dict])
async def get_products(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get products with optional status filter"""
    query = db.query(Product)

    if status:
        query = query.filter(Product.status == status)

    products = query.order_by(Product.discovered_at.desc()).offset(offset).limit(limit).all()

    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "category": p.category,
            "image_url": p.image_url,
            "trend_score": p.trend_score,
            "trend_source": p.trend_source,
            "status": p.status.value,
            "suggested_price": p.suggested_price,
            "potential_margin": p.potential_margin,
            "ai_keywords": p.ai_keywords,
            "discovered_at": p.discovered_at.isoformat() if p.discovered_at else None,
            "posted_platforms": p.posted_platforms or []
        }
        for p in products
    ]


@app.get("/api/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product details"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "category": product.category,
        "image_url": product.image_url,
        "source_url": product.source_url,
        "trend_score": product.trend_score,
        "trend_source": product.trend_source,
        "search_volume": product.search_volume,
        "social_mentions": product.social_mentions,
        "ai_category": product.ai_category,
        "ai_keywords": product.ai_keywords,
        "ai_description": product.ai_description,
        "profit_potential_score": product.profit_potential_score,
        "competition_level": product.competition_level,
        "estimated_cost": product.estimated_cost,
        "suggested_price": product.suggested_price,
        "potential_margin": product.potential_margin,
        "status": product.status.value,
        "approved_by_user": product.approved_by_user,
        "rejection_reason": product.rejection_reason,
        "posted_platforms": product.posted_platforms or [],
        "platform_ids": product.platform_ids or {},
        "discovered_at": product.discovered_at.isoformat() if product.discovered_at else None,
        "analyzed_at": product.analyzed_at.isoformat() if product.analyzed_at else None
    }


@app.post("/api/products/{product_id}/approve")
async def approve_product(product_id: int, db: Session = Depends(get_db)):
    """Approve a product for posting"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.status = ProductStatus.APPROVED
    product.approved_by_user = True
    product.approved_at = datetime.utcnow()

    db.commit()

    return {"message": "Product approved", "product_id": product_id}


@app.post("/api/products/{product_id}/reject")
async def reject_product(product_id: int, reason: str = "", db: Session = Depends(get_db)):
    """Reject a product"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.status = ProductStatus.REJECTED
    product.approved_by_user = False
    product.rejection_reason = reason

    db.commit()

    return {"message": "Product rejected", "product_id": product_id}


@app.post("/api/products/{product_id}/post")
async def post_product(
    product_id: int,
    platforms: List[str],
    db: Session = Depends(get_db)
):
    """Post approved product to selected platforms"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product.approved_by_user:
        raise HTTPException(
            status_code=400,
            detail="Product must be approved before posting"
        )

    # Use platform manager to post
    platform_manager = PlatformManager()
    results = await platform_manager.post_to_platforms(product, platforms, db)

    return {
        "message": "Product posting initiated",
        "product_id": product_id,
        "results": results
    }


# ==================== TREND DISCOVERY ENDPOINTS ====================

@app.post("/api/trends/scan")
async def scan_trends(db: Session = Depends(get_db)):
    """Manually trigger trend scan"""
    scanner = TrendScanner()
    results = await scanner.scan_all_sources(db)

    return {
        "message": "Trend scan completed",
        "products_found": results["products_found"],
        "sources_scanned": results["sources_scanned"]
    }


@app.get("/api/trends/sources")
async def get_trend_sources(db: Session = Depends(get_db)):
    """Get all trend sources and their status"""
    sources = db.query(TrendSource).all()

    return [
        {
            "id": s.id,
            "name": s.name,
            "source_type": s.source_type,
            "enabled": s.enabled,
            "products_found": s.products_found,
            "last_scan": s.last_scan.isoformat() if s.last_scan else None
        }
        for s in sources
    ]


# ==================== ANALYTICS ENDPOINTS ====================

@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics(db: Session = Depends(get_db)):
    """Get dashboard analytics data"""
    total_products = db.query(Product).count()
    pending_review = db.query(Product).filter(
        Product.status == ProductStatus.PENDING_REVIEW
    ).count()
    approved = db.query(Product).filter(
        Product.status == ProductStatus.APPROVED
    ).count()
    posted = db.query(Product).filter(
        Product.status == ProductStatus.POSTED
    ).count()

    # Platform breakdown
    listings = db.query(PlatformListing).all()
    platform_stats = {}
    for listing in listings:
        platform_name = listing.platform.value
        if platform_name not in platform_stats:
            platform_stats[platform_name] = {"count": 0, "revenue": 0}
        platform_stats[platform_name]["count"] += 1
        platform_stats[platform_name]["revenue"] += listing.revenue or 0

    return {
        "total_products": total_products,
        "pending_review": pending_review,
        "approved": approved,
        "posted": posted,
        "platform_stats": platform_stats
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
