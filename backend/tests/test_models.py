"""
Database model tests
"""
import pytest
from datetime import datetime
from models.database import Product, ProductStatus, TrendSource, Platform, PlatformListing


class TestProductModel:
    """Test Product model"""

    def test_create_product(self, db_session):
        """Test creating a product"""
        product = Product(
            title="Test Product",
            description="Test Description",
            category="Electronics",
            trend_score=85.0,
            status=ProductStatus.DISCOVERED
        )
        db_session.add(product)
        db_session.commit()

        assert product.id is not None
        assert product.title == "Test Product"
        assert product.status == ProductStatus.DISCOVERED
        assert product.discovered_at is not None

    def test_product_status_transitions(self, db_session):
        """Test product status transitions"""
        product = Product(title="Test", status=ProductStatus.DISCOVERED)
        db_session.add(product)
        db_session.commit()

        # Transition to pending review
        product.status = ProductStatus.PENDING_REVIEW
        db_session.commit()
        assert product.status == ProductStatus.PENDING_REVIEW

        # Approve
        product.status = ProductStatus.APPROVED
        product.approved_by_user = True
        product.approved_at = datetime.utcnow()
        db_session.commit()

        assert product.status == ProductStatus.APPROVED
        assert product.approved_by_user is True
        assert product.approved_at is not None


class TestTrendSourceModel:
    """Test TrendSource model"""

    def test_create_trend_source(self, db_session):
        """Test creating a trend source"""
        source = TrendSource(
            name="Amazon Best Sellers",
            source_type="marketplace",
            enabled=True
        )
        db_session.add(source)
        db_session.commit()

        assert source.id is not None
        assert source.name == "Amazon Best Sellers"
        assert source.enabled is True

    def test_unique_source_name(self, db_session):
        """Test that source names must be unique"""
        source1 = TrendSource(name="Test Source", source_type="test")
        db_session.add(source1)
        db_session.commit()

        source2 = TrendSource(name="Test Source", source_type="test")
        db_session.add(source2)

        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()


class TestPlatformListingModel:
    """Test PlatformListing model"""

    def test_create_platform_listing(self, db_session):
        """Test creating a platform listing"""
        product = Product(title="Test Product")
        db_session.add(product)
        db_session.commit()

        listing = PlatformListing(
            product_id=product.id,
            platform=Platform.AMAZON,
            listing_status="active",
            views=100,
            sales=5,
            revenue=250.0
        )
        db_session.add(listing)
        db_session.commit()

        assert listing.id is not None
        assert listing.platform == Platform.AMAZON
        assert listing.views == 100
        assert listing.sales == 5
        assert listing.revenue == 250.0
