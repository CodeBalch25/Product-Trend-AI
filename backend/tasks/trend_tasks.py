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


@celery_app.task(name='tasks.trend_tasks.perplexity_discovery_task')
def perplexity_discovery_task(category: str = None):
    """
    Perplexity-powered trend discovery task

    This task:
    1. Uses Perplexity to discover what's trending RIGHT NOW on the web
    2. Extracts trending keywords and products
    3. Feeds intelligence back to the trend scanner (feedback loop)
    4. Stores discovered keywords in database for future use

    Runs every 6 hours to keep system intelligence fresh
    """
    db = SessionLocal()
    try:
        from services.trend_discovery.perplexity_discovery import PerplexityTrendDiscovery
        import asyncio

        print("\n" + "="*80)
        print("🌐 [PERPLEXITY DISCOVERY] Starting real-time trend discovery")
        print("="*80)

        discovery = PerplexityTrendDiscovery()

        # Run async discovery
        discovered = asyncio.run(discovery.discover_trending_products(category))

        # Feed intelligence back to system (feedback loop)
        keywords = discovery.update_trend_scanner_intel(db, discovered)

        print("\n" + "="*80)
        print(f"✅ [PERPLEXITY DISCOVERY] Complete!")
        print(f"   📦 Discovered {len(discovered.get('discovered_products', []))} trending products")
        print(f"   🔑 Extracted {len(keywords)} trending keywords")
        print(f"   🔄 System intelligence updated")
        print("="*80 + "\n")

        return {
            "status": "completed",
            "products_discovered": len(discovered.get('discovered_products', [])),
            "keywords_extracted": len(keywords),
            "hot_categories": discovered.get('market_insights', {}).get('hot_categories', [])
        }

    except Exception as e:
        print(f"❌ [PERPLEXITY DISCOVERY] Failed: {str(e)[:100]}")
        return {
            "status": "failed",
            "error": str(e)
        }
    finally:
        db.close()
