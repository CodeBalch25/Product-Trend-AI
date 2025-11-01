"""
Database Management Script
View, clear, and manage products in the database
"""
import sys
from models.database import SessionLocal, Product, ProductStatus
from sqlalchemy import func


def show_stats():
    """Show database statistics"""
    db = SessionLocal()
    try:
        print("\n" + "="*80)
        print("📊 DATABASE STATISTICS")
        print("="*80)

        total = db.query(Product).count()
        print(f"Total Products: {total}")

        if total > 0:
            # Count by status
            print("\nBy Status:")
            for status in ProductStatus:
                count = db.query(Product).filter(Product.status == status).count()
                if count > 0:
                    print(f"  {status.value}: {count}")

            # Count by source
            print("\nBy Source:")
            sources = db.query(Product.trend_source, func.count(Product.id)).group_by(Product.trend_source).all()
            for source, count in sources:
                print(f"  {source or 'Unknown'}: {count}")

        print("="*80 + "\n")

    finally:
        db.close()


def list_products(limit=20):
    """List recent products"""
    db = SessionLocal()
    try:
        print("\n" + "="*80)
        print(f"📦 RECENT PRODUCTS (showing {limit})")
        print("="*80)

        products = db.query(Product).order_by(Product.discovered_at.desc()).limit(limit).all()

        if not products:
            print("No products in database.")
        else:
            for i, p in enumerate(products, 1):
                print(f"\n{i}. {p.title[:60]}")
                print(f"   ID: {p.id} | Status: {p.status.value} | Score: {p.trend_score}")
                print(f"   Source: {p.trend_source}")
                print(f"   Discovered: {p.discovered_at}")

        print("\n" + "="*80 + "\n")

    finally:
        db.close()


def clear_all_products():
    """Clear all products from database"""
    db = SessionLocal()
    try:
        count = db.query(Product).count()

        if count == 0:
            print("\n✓ Database is already empty.\n")
            return

        print(f"\n⚠️  WARNING: About to delete {count} products from database!")
        confirm = input("Type 'DELETE' to confirm: ")

        if confirm == "DELETE":
            db.query(Product).delete()
            db.commit()
            print(f"\n✅ Deleted {count} products successfully!\n")
        else:
            print("\n❌ Cancelled - no products deleted.\n")

    finally:
        db.close()


def clear_rejected_products():
    """Clear only rejected products"""
    db = SessionLocal()
    try:
        count = db.query(Product).filter(Product.status == ProductStatus.REJECTED).count()

        if count == 0:
            print("\n✓ No rejected products to delete.\n")
            return

        print(f"\n⚠️  About to delete {count} rejected products")
        confirm = input("Type 'YES' to confirm: ")

        if confirm == "YES":
            db.query(Product).filter(Product.status == ProductStatus.REJECTED).delete()
            db.commit()
            print(f"\n✅ Deleted {count} rejected products!\n")
        else:
            print("\n❌ Cancelled.\n")

    finally:
        db.close()


def main():
    """Main menu"""
    while True:
        print("\n" + "="*80)
        print("🛠️  PRODUCT DATABASE MANAGER")
        print("="*80)
        print("1. Show statistics")
        print("2. List recent products (20)")
        print("3. List all products")
        print("4. Clear ALL products (DANGER!)")
        print("5. Clear rejected products only")
        print("6. Exit")
        print("="*80)

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            show_stats()
        elif choice == "2":
            list_products(20)
        elif choice == "3":
            db = SessionLocal()
            try:
                total = db.query(Product).count()
                list_products(total)
            finally:
                db.close()
        elif choice == "4":
            clear_all_products()
        elif choice == "5":
            clear_rejected_products()
        elif choice == "6":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...\n")
        sys.exit(0)
