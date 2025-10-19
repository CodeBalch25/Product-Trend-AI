"""
Celery tasks for trend discovery
"""
from tasks.celery_app import celery_app
from models.database import SessionLocal, Product, ProductStatus
from services.trend_discovery.trend_scanner import TrendScanner


@celery_app.task(name='tasks.trend_tasks.scan_trends_task')
def scan_trends_task():
    """
    Periodic task to scan all trend sources
    Runs every hour by default
    """
    db = SessionLocal()
    try:
        scanner = TrendScanner()
        # Run async function in sync context
        import asyncio
        results = asyncio.run(scanner.scan_all_sources(db))

        return {
            "status": "completed",
            "products_found": results["products_found"],
            "sources_scanned": results["sources_scanned"]
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
    finally:
        db.close()


@celery_app.task(name='tasks.trend_tasks.scan_specific_source')
def scan_specific_source_task(source_name: str):
    """Scan a specific trend source"""
    db = SessionLocal()
    try:
        scanner = TrendScanner()
        # Implement source-specific scanning
        return {"status": "completed", "source": source_name}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
    finally:
        db.close()
