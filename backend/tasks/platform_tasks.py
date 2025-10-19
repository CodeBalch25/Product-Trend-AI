"""
Celery tasks for platform integration and syncing
"""
from tasks.celery_app import celery_app
from models.database import SessionLocal, PlatformListing
from datetime import datetime


@celery_app.task(name='tasks.platform_tasks.sync_listings_task')
def sync_listings_task():
    """
    Sync listing status and metrics from all platforms
    Runs every 30 minutes
    """
    db = SessionLocal()
    try:
        # Get all active listings
        listings = db.query(PlatformListing).filter(
            PlatformListing.listing_status == "active"
        ).all()

        synced_count = 0

        for listing in listings:
            try:
                # Sync status from platform
                # In production, call platform APIs to get latest stats
                # For now, just update sync timestamp
                listing.last_synced = datetime.utcnow()
                synced_count += 1

            except Exception as e:
                print(f"Error syncing listing {listing.id}: {str(e)}")

        db.commit()

        return {
            "status": "completed",
            "synced_count": synced_count
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
    finally:
        db.close()


@celery_app.task(name='tasks.platform_tasks.post_product_to_platform')
def post_product_to_platform_task(product_id: int, platform_name: str):
    """
    Background task to post a product to a specific platform
    """
    db = SessionLocal()
    try:
        from models.database import Product
        from services.platform_integrations.platform_manager import PlatformManager

        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"status": "failed", "error": "Product not found"}

        manager = PlatformManager()
        import asyncio
        results = asyncio.run(manager.post_to_platforms(product, [platform_name], db))

        return {
            "status": "completed",
            "product_id": product_id,
            "platform": platform_name,
            "result": results.get(platform_name)
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
    finally:
        db.close()
