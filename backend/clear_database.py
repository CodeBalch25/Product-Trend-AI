"""
Quick Database Reset Script
Clears all products for fresh start
"""
from models.database import SessionLocal, Product
from sqlalchemy import text

def clear_all_products():
    """Clear all products from database"""
    db = SessionLocal()
    try:
        # Count before
        count_before = db.query(Product).count()
        print(f"\n{'='*60}")
        print(f"🗑️  DATABASE RESET")
        print(f"{'='*60}")
        print(f"Current products: {count_before}")

        if count_before == 0:
            print("✓ Database is already empty!")
            print(f"{'='*60}\n")
            return

        # Delete all products
        db.query(Product).delete()
        db.commit()

        # Reset auto-increment
        try:
            db.execute(text("ALTER SEQUENCE products_id_seq RESTART WITH 1"))
            db.commit()
        except:
            pass  # Sequence might not exist or different database

        # Count after
        count_after = db.query(Product).count()

        print(f"✅ Deleted {count_before} products successfully!")
        print(f"Remaining products: {count_after}")
        print(f"{'='*60}\n")
        print("✓ Database is now empty and ready for fresh scan!")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_products()
