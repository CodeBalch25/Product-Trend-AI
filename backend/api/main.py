"""
Main FastAPI application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from config.settings import settings
from models.database import get_db, init_db, Product, ProductStatus, PlatformListing, TrendSource
from services.trend_discovery.trend_scanner import TrendScanner
from services.ai_analysis.product_analyzer import ProductAnalyzer
from services.platform_integrations.platform_manager import PlatformManager
from services.ml.approval_predictor import ml_predictor
from routes.monitoring_routes import router as monitoring_router

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

# Include routers
app.include_router(monitoring_router)


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
            "rejection_reason": p.rejection_reason,  # Include rejection reason for AI learning
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
async def reject_product(
    product_id: int,
    request: dict,
    db: Session = Depends(get_db)
):
    """Reject a product and move to rejected section (for AI learning)"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Extract reason from request body
    reason = request.get("reason", "")

    # Soft delete: Change status to REJECTED and store reason
    product.status = ProductStatus.REJECTED
    product.rejection_reason = reason
    product.approved_by_user = False
    product.rejected_at = datetime.utcnow()

    db.commit()

    print(f"❌ Product REJECTED: {product.title} (ID: {product_id})")
    if reason:
        print(f"   Reason: {reason}")
    else:
        print(f"   ⚠️ WARNING: No rejection reason provided!")
    print(f"   → Moved to Rejected section (kept for AI learning)")

    return {
        "message": "Product rejected and moved to rejected section",
        "product_id": product_id,
        "reason": reason,
        "rejected": True
    }


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
    import uuid
    import traceback

    print("\n" + "="*80)
    print("🔍 SCAN TRENDS ENDPOINT CALLED - DEBUG MODE")
    print("="*80)

    try:
        # TEST: Database connection
        print("✓ Step 1: Testing database connection...")
        try:
            product_count = db.query(Product).count()
            print(f"  ✓ Database connected! Current products: {product_count}")
        except Exception as db_err:
            print(f"  ✗ Database error: {str(db_err)}")
            raise HTTPException(
                status_code=500,
                detail=f"Database connection failed: {str(db_err)}"
            )

        # Generate unique scan ID
        scan_id = str(uuid.uuid4())[:8]
        print(f"✓ Step 2: Generated scan ID: {scan_id}")

        # Mark all existing products as not new
        print("✓ Step 3: Marking existing products as not new...")
        db.query(Product).update({"is_new": False})
        db.commit()
        print("  ✓ Products marked")

        # Count products before scan
        products_before = db.query(Product).count()
        print(f"✓ Step 4: Products before scan: {products_before}")

        # Run scan
        print("✓ Step 5: Initializing TrendScanner...")
        try:
            scanner = TrendScanner()
            print("  ✓ TrendScanner initialized")
        except Exception as scanner_err:
            print(f"  ✗ Scanner initialization failed: {str(scanner_err)}")
            print(f"  Traceback: {traceback.format_exc()}")
            raise

        print("✓ Step 6: Running scan_all_sources...")
        try:
            results = await scanner.scan_all_sources(db)
            print(f"  ✓ Scan complete! Results: {results}")
        except Exception as scan_err:
            print(f"  ✗ Scan failed: {str(scan_err)}")
            print(f"  Traceback: {traceback.format_exc()}")
            raise

        # Mark newly discovered products with scan_id and is_new=True
        print("✓ Step 7: Marking new products...")
        new_products = db.query(Product).filter(
            Product.scan_id.is_(None)
        ).all()

        for product in new_products:
            product.scan_id = scan_id
            product.is_new = True

        db.commit()
        print(f"  ✓ Marked {len(new_products)} new products")

        # Count new products
        products_after = db.query(Product).count()
        new_count = products_after - products_before
        print(f"✓ Step 8: Products after scan: {products_after} (new: {new_count})")

        # Trigger AI analysis for discovered products (async) - Make optional if Celery not running
        print("✓ Step 9: Attempting to trigger Celery AI analysis...")
        try:
            from tasks.analysis_tasks import analyze_pending_products_task
            analyze_pending_products_task.delay()
            print("  ✓ AI analysis task triggered successfully")
        except Exception as celery_error:
            print(f"  ⚠ Celery task failed (non-critical): {str(celery_error)}")
            print("  → Products discovered successfully. AI analysis will run when Celery is available.")

        message = f"Found {new_count} new trending products!" if new_count > 0 else "No new products found. Market trends unchanged."

        print(f"\n✅ SCAN COMPLETED SUCCESSFULLY!")
        print(f"   Message: {message}")
        print("="*80 + "\n")

        return {
            "message": message,
            "products_found": results["products_found"],
            "new_products_count": new_count,
            "total_products": products_after,
            "sources_scanned": results["sources_scanned"],
            "scan_id": scan_id
        }

    except Exception as e:
        print(f"\n❌ SCAN FAILED!")
        print(f"   Error: {str(e)}")
        print(f"   Type: {type(e).__name__}")
        print(f"   Traceback:\n{traceback.format_exc()}")
        print("="*80 + "\n")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to scan trends: {str(e)}"
        )


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
    rejected = db.query(Product).filter(
        Product.status == ProductStatus.REJECTED
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
        "rejected": rejected,
        "platform_stats": platform_stats
    }


@app.get("/api/analytics/rejections")
async def get_rejection_analytics(db: Session = Depends(get_db)):
    """Analyze rejection patterns for AI improvement"""
    from sqlalchemy import func

    # Total counts by status
    total_products = db.query(Product).count()
    total_rejected = db.query(Product).filter(
        Product.status == ProductStatus.REJECTED
    ).count()
    total_approved = db.query(Product).filter(
        Product.status == ProductStatus.APPROVED
    ).count()

    # Rejection rate
    rejection_rate = (total_rejected / total_products * 100) if total_products > 0 else 0
    approval_rate = (total_approved / total_products * 100) if total_products > 0 else 0

    # Count by rejection reason
    rejection_by_reason = {}
    reasons = db.query(
        Product.rejection_reason,
        func.count(Product.id).label('count')
    ).filter(
        Product.status == ProductStatus.REJECTED,
        Product.rejection_reason.isnot(None)
    ).group_by(Product.rejection_reason).all()

    for reason, count in reasons:
        rejection_by_reason[reason] = count

    # Rejection rate by trend score range
    score_ranges = {
        "0-50": {"total": 0, "rejected": 0},
        "50-70": {"total": 0, "rejected": 0},
        "70-85": {"total": 0, "rejected": 0},
        "85-100": {"total": 0, "rejected": 0},
    }

    all_products = db.query(Product).all()
    for product in all_products:
        score = product.trend_score or 0

        if score < 50:
            range_key = "0-50"
        elif score < 70:
            range_key = "50-70"
        elif score < 85:
            range_key = "70-85"
        else:
            range_key = "85-100"

        score_ranges[range_key]["total"] += 1
        if product.status == ProductStatus.REJECTED:
            score_ranges[range_key]["rejected"] += 1

    # Calculate rejection rates for each range
    for range_key in score_ranges:
        total = score_ranges[range_key]["total"]
        rejected = score_ranges[range_key]["rejected"]
        score_ranges[range_key]["rejection_rate"] = (rejected / total * 100) if total > 0 else 0

    # Rejection rate by source
    source_stats = {}
    for product in all_products:
        source = product.trend_source or "unknown"
        if source not in source_stats:
            source_stats[source] = {"total": 0, "rejected": 0, "approved": 0}

        source_stats[source]["total"] += 1
        if product.status == ProductStatus.REJECTED:
            source_stats[source]["rejected"] += 1
        elif product.status == ProductStatus.APPROVED:
            source_stats[source]["approved"] += 1

    # Calculate rates
    for source in source_stats:
        total = source_stats[source]["total"]
        source_stats[source]["rejection_rate"] = (source_stats[source]["rejected"] / total * 100) if total > 0 else 0
        source_stats[source]["approval_rate"] = (source_stats[source]["approved"] / total * 100) if total > 0 else 0

    # Rejection rate by category
    category_stats = {}
    for product in all_products:
        category = product.category or "uncategorized"
        if category not in category_stats:
            category_stats[category] = {"total": 0, "rejected": 0}

        category_stats[category]["total"] += 1
        if product.status == ProductStatus.REJECTED:
            category_stats[category]["rejected"] += 1

    for category in category_stats:
        total = category_stats[category]["total"]
        category_stats[category]["rejection_rate"] = (category_stats[category]["rejected"] / total * 100) if total > 0 else 0

    # Recent trends (last 30 products)
    recent_products = db.query(Product).order_by(
        Product.discovered_at.desc()
    ).limit(30).all()

    recent_rejected = sum(1 for p in recent_products if p.status == ProductStatus.REJECTED)
    recent_rejection_rate = (recent_rejected / len(recent_products) * 100) if recent_products else 0

    return {
        "overall": {
            "total_products": total_products,
            "total_rejected": total_rejected,
            "total_approved": total_approved,
            "rejection_rate": round(rejection_rate, 2),
            "approval_rate": round(approval_rate, 2)
        },
        "rejection_by_reason": rejection_by_reason,
        "rejection_by_score_range": score_ranges,
        "rejection_by_source": source_stats,
        "rejection_by_category": category_stats,
        "recent_trends": {
            "last_30_products": len(recent_products),
            "recent_rejection_rate": round(recent_rejection_rate, 2)
        },
        "insights": generate_insights(
            rejection_rate,
            score_ranges,
            source_stats,
            rejection_by_reason
        )
    }


def generate_insights(rejection_rate, score_ranges, source_stats, rejection_by_reason):
    """Generate actionable insights from rejection data"""
    insights = []

    # Insight 1: Overall rejection rate
    if rejection_rate > 50:
        insights.append({
            "type": "warning",
            "title": "High Rejection Rate",
            "message": f"{rejection_rate:.1f}% of products are being rejected. Consider adjusting trend score thresholds.",
            "action": "Increase minimum trend score from 70 to 85"
        })
    elif rejection_rate < 20:
        insights.append({
            "type": "success",
            "title": "Low Rejection Rate",
            "message": f"Only {rejection_rate:.1f}% rejection rate - AI is finding good products!",
            "action": "System is performing well"
        })

    # Insight 2: Score range analysis
    for range_key, data in score_ranges.items():
        if data["total"] > 5 and data["rejection_rate"] > 70:
            insights.append({
                "type": "warning",
                "title": f"High Rejection in {range_key} Range",
                "message": f"{data['rejection_rate']:.1f}% rejection rate for trend scores {range_key}",
                "action": f"Consider filtering out products with trend score < {range_key.split('-')[1]}"
            })

    # Insight 3: Source performance
    worst_source = None
    worst_rate = 0
    for source, data in source_stats.items():
        if data["total"] > 3 and data["rejection_rate"] > worst_rate:
            worst_rate = data["rejection_rate"]
            worst_source = source

    if worst_source and worst_rate > 60:
        insights.append({
            "type": "warning",
            "title": f"Weak Source: {worst_source}",
            "message": f"{worst_rate:.1f}% rejection rate from {worst_source}",
            "action": f"Reduce priority of {worst_source} or increase quality threshold"
        })

    # Insight 4: Top rejection reason
    if rejection_by_reason:
        top_reason = max(rejection_by_reason.items(), key=lambda x: x[1])
        reason_name = top_reason[0].replace('_', ' ').title()
        insights.append({
            "type": "info",
            "title": f"Most Common Rejection: {reason_name}",
            "message": f"{top_reason[1]} products rejected for this reason",
            "action": f"AI should learn to avoid products with '{reason_name}' issues"
        })

    return insights


# ==================== ML MODEL ENDPOINTS ====================

@app.post("/api/ml/train")
async def train_ml_model(db: Session = Depends(get_db)):
    """Train ML model on historical data"""

    # Get all products with status
    products = db.query(Product).all()

    if len(products) < 20:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least 20 products for training. Current: {len(products)}"
        )

    # Prepare training data
    training_data = []
    for product in products:
        if product.status in [ProductStatus.APPROVED, ProductStatus.REJECTED]:
            training_data.append({
                "trend_score": product.trend_score or 0,
                "category": product.category or "unknown",
                "source": product.trend_source or "unknown",
                "price": product.estimated_cost or 0,
                "keywords": product.ai_keywords or [],
                "label": "approved" if product.status == ProductStatus.APPROVED else "rejected",
                "rejection_reason": product.rejection_reason
            })

    # Train model
    success = ml_predictor.train(training_data)

    if success:
        return {
            "message": "ML model trained successfully!",
            "training_examples": len(training_data),
            "model_ready": True
        }
    else:
        return {
            "message": "Training failed - need more data",
            "training_examples": len(training_data),
            "model_ready": False
        }


@app.get("/api/ml/status")
async def get_ml_status():
    """Check ML model training status"""
    return {
        "trained": ml_predictor.trained,
        "ready": ml_predictor.trained
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
