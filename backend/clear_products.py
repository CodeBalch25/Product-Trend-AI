"""
Clear all products from the database for fresh start
"""
from models.database import SessionLocal, Product

def clear_all_products():
    """Delete all products from database"""
    db = SessionLocal()
    try:
        # Count products before deletion
        count_before = db.query(Product).count()
        print(f"\n📊 Products in database: {count_before}")

        if count_before == 0:
            print("✓ Database is already empty!")
            return

        # Delete all products
        print(f"🗑️  Deleting all {count_before} products...")
        db.query(Product).delete()
        db.commit()

        # Verify deletion
        count_after = db.query(Product).count()
        print(f"✅ SUCCESS! Deleted {count_before} products")
        print(f"📊 Products remaining: {count_after}")
        print("\n🎉 Database is clean and ready for fresh testing!\n")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧹 CLEARING PRODUCT DATABASE")
    print("="*60)
    clear_all_products()
