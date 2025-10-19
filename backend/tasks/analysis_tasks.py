"""
Celery tasks for AI product analysis
"""
from tasks.celery_app import celery_app
from models.database import SessionLocal, Product, ProductStatus
from services.ai_analysis.product_analyzer import ProductAnalyzer
from datetime import datetime


@celery_app.task(name='tasks.analysis_tasks.analyze_pending_products_task')
def analyze_pending_products_task():
    """
    Analyze all products in DISCOVERED status
    Runs every 15 minutes

    Rate-limit optimized: Processes 5 products per batch
    Each product takes ~15-20 seconds with sequential agent processing
    """
    db = SessionLocal()
    try:
        # Get products that need analysis (reduced batch size for rate limiting)
        products = db.query(Product).filter(
            Product.status == ProductStatus.DISCOVERED
        ).limit(5).all()  # Process 5 at a time to respect Groq rate limits

        if not products:
            print("📭 No products to analyze")
            return {"status": "completed", "analyzed_count": 0}

        analyzer = ProductAnalyzer()
        analyzed_count = 0
        total_products = len(products)

        # Calculate estimated time: ~18s per product + 5s cooldown between products
        estimated_seconds = (total_products * 18) + ((total_products - 1) * 5)
        estimated_minutes = estimated_seconds / 60

        print(f"\n{'='*70}")
        print(f"🤖 AI ANALYSIS BATCH STARTED")
        print(f"   Products to analyze: {total_products}")
        print(f"   Rate-limit friendly: Sequential agents + product delays")
        print(f"   Estimated time: ~{estimated_seconds} seconds ({estimated_minutes:.1f} minutes)")
        print(f"{'='*70}\n")

        import asyncio

        for idx, product in enumerate(products, 1):
            try:
                print(f"📦 [{idx}/{total_products}] Analyzing: {product.title[:60]}...")
                print(f"    Status: DISCOVERED → ANALYZING")

                # Update status to analyzing
                product.status = ProductStatus.ANALYZING
                db.commit()

                # Run analysis (with db for ML integration)
                print(f"    🤖 Deploying 11-agent AI system...")
                analysis = asyncio.run(analyzer.analyze_product(product, db))

                # Update product with analysis results
                product.ai_category = analysis.get("ai_category")
                product.ai_keywords = analysis.get("ai_keywords")
                product.ai_description = analysis.get("ai_description")
                product.profit_potential_score = analysis.get("profit_potential_score")
                product.competition_level = analysis.get("competition_level")

                # Store ML prediction if available
                if analysis.get("ml_prediction"):
                    product.ml_prediction_data = analysis.get("ml_prediction")

                # Calculate suggested_price from estimated_cost
                if product.estimated_cost and product.estimated_cost > 0:
                    # Apply 2.5x markup for suggested retail price
                    product.suggested_price = round(product.estimated_cost * 2.5, 2)
                    product.potential_margin = round(product.suggested_price - product.estimated_cost, 2)
                elif analysis.get("suggested_price"):
                    # Parse price range from AI like "$20-$50"
                    price_str = analysis.get("suggested_price")
                    try:
                        if "-" in price_str:
                            # Get average of range
                            low = float(price_str.split("$")[1].split("-")[0])
                            high = float(price_str.split("-")[1].replace("$", ""))
                            product.suggested_price = round((low + high) / 2, 2)
                            if product.estimated_cost:
                                product.potential_margin = round(product.suggested_price - product.estimated_cost, 2)
                    except:
                        pass

                # Move to pending review
                product.status = ProductStatus.PENDING_REVIEW
                product.analyzed_at = datetime.utcnow()

                analyzed_count += 1
                db.commit()

                print(f"    ✅ Analysis complete! Status: ANALYZING → PENDING_REVIEW")
                print(f"    📊 Profit Score: {product.profit_potential_score}/100")
                print(f"    💰 Suggested Price: ${product.suggested_price:.2f}")

                # Add delay between products to avoid rate limiting
                if idx < total_products:
                    print(f"    ⏸️  Cooling down for 5 seconds before next product...")
                    import time
                    time.sleep(5)
                print()

            except Exception as e:
                print(f"    ❌ Error analyzing product {product.id}: {str(e)}")
                product.status = ProductStatus.DISCOVERED  # Reset status
                db.commit()
                print()

        print(f"\n{'='*70}")
        print(f"✅ AI ANALYSIS BATCH COMPLETED")
        print(f"   Successfully analyzed: {analyzed_count}/{total_products} products")
        print(f"   Failed: {total_products - analyzed_count}/{total_products} products")
        print(f"{'='*70}\n")

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


@celery_app.task(name='tasks.analysis_tasks.analyze_single_product')
def analyze_single_product_task(product_id: int):
    """Analyze a specific product"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"status": "failed", "error": "Product not found"}

        analyzer = ProductAnalyzer()
        import asyncio
        analysis = asyncio.run(analyzer.analyze_product(product, db))

        # Update product
        product.ai_category = analysis.get("ai_category")
        product.ai_keywords = analysis.get("ai_keywords")
        product.ai_description = analysis.get("ai_description")
        product.profit_potential_score = analysis.get("profit_potential_score")
        product.competition_level = analysis.get("competition_level")

        # Store ML prediction if available
        if analysis.get("ml_prediction"):
            product.ml_prediction_data = analysis.get("ml_prediction")

        product.status = ProductStatus.PENDING_REVIEW
        product.analyzed_at = datetime.utcnow()

        db.commit()

        return {"status": "completed", "product_id": product_id}

    except Exception as e:
        return {"status": "failed", "error": str(e)}
    finally:
        db.close()
