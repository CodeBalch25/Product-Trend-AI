"""
Celery tasks for AI product analysis
"""
from backend.tasks.celery_app import celery_app
from backend.models.database import SessionLocal, Product, ProductStatus
from backend.services.ai_analysis.product_analyzer import ProductAnalyzer
from datetime import datetime


@celery_app.task(name='backend.tasks.analysis_tasks.analyze_pending_products_task')
def analyze_pending_products_task():
    """
    Analyze all products in DISCOVERED status
    Runs every 15 minutes
    """
    db = SessionLocal()
    try:
        # Get products that need analysis
        products = db.query(Product).filter(
            Product.status == ProductStatus.DISCOVERED
        ).limit(10).all()  # Process 10 at a time

        analyzer = ProductAnalyzer()
        analyzed_count = 0

        import asyncio

        for product in products:
            try:
                # Update status to analyzing
                product.status = ProductStatus.ANALYZING
                db.commit()

                # Run analysis
                analysis = asyncio.run(analyzer.analyze_product(product))

                # Update product with analysis results
                product.ai_category = analysis.get("ai_category")
                product.ai_keywords = analysis.get("ai_keywords")
                product.ai_description = analysis.get("ai_description")
                product.profit_potential_score = analysis.get("profit_potential_score")
                product.competition_level = analysis.get("competition_level")

                # Extract price if available
                if analysis.get("suggested_price"):
                    # Parse price range like "$20-$50"
                    price_str = analysis.get("suggested_price")
                    try:
                        if "-" in price_str:
                            # Get average of range
                            low = float(price_str.split("$")[1].split("-")[0])
                            high = float(price_str.split("-")[1].replace("$", ""))
                            product.suggested_price = (low + high) / 2
                    except:
                        pass

                # Move to pending review
                product.status = ProductStatus.PENDING_REVIEW
                product.analyzed_at = datetime.utcnow()

                analyzed_count += 1
                db.commit()

            except Exception as e:
                print(f"Error analyzing product {product.id}: {str(e)}")
                product.status = ProductStatus.DISCOVERED  # Reset status
                db.commit()

        return {
            "status": "completed",
            "analyzed_count": analyzed_count
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
    finally:
        db.close()


@celery_app.task(name='backend.tasks.analysis_tasks.analyze_single_product')
def analyze_single_product_task(product_id: int):
    """Analyze a specific product"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"status": "failed", "error": "Product not found"}

        analyzer = ProductAnalyzer()
        import asyncio
        analysis = asyncio.run(analyzer.analyze_product(product))

        # Update product
        product.ai_category = analysis.get("ai_category")
        product.ai_keywords = analysis.get("ai_keywords")
        product.ai_description = analysis.get("ai_description")
        product.profit_potential_score = analysis.get("profit_potential_score")
        product.competition_level = analysis.get("competition_level")
        product.status = ProductStatus.PENDING_REVIEW
        product.analyzed_at = datetime.utcnow()

        db.commit()

        return {"status": "completed", "product_id": product_id}

    except Exception as e:
        return {"status": "failed", "error": str(e)}
    finally:
        db.close()
