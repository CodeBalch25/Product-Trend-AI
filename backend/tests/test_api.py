"""
API endpoint tests
"""
import pytest
from fastapi import status
from models.database import Product, ProductStatus


class TestHealthEndpoint:
    """Test health check endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns app info"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "app" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"


class TestProductEndpoints:
    """Test product-related endpoints"""

    def test_get_products_empty(self, client):
        """Test getting products when none exist"""
        response = client.get("/api/products")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_products_with_data(self, client, db_session, sample_product_data):
        """Test getting products when data exists"""
        # Create test product
        product = Product(**sample_product_data)
        db_session.add(product)
        db_session.commit()

        response = client.get("/api/products")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == sample_product_data["title"]

    def test_get_single_product(self, client, db_session, sample_product_data):
        """Test getting a single product by ID"""
        product = Product(**sample_product_data)
        db_session.add(product)
        db_session.commit()

        response = client.get(f"/api/products/{product.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == product.id
        assert data["title"] == product.title

    def test_get_nonexistent_product(self, client):
        """Test getting a product that doesn't exist"""
        response = client.get("/api/products/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_approve_product(self, client, db_session, sample_product_data):
        """Test approving a product"""
        product = Product(
            **sample_product_data,
            status=ProductStatus.PENDING_REVIEW
        )
        db_session.add(product)
        db_session.commit()

        response = client.post(f"/api/products/{product.id}/approve")
        assert response.status_code == status.HTTP_200_OK

        # Verify product was approved
        db_session.refresh(product)
        assert product.status == ProductStatus.APPROVED
        assert product.approved_by_user is True

    def test_reject_product(self, client, db_session, sample_product_data):
        """Test rejecting a product"""
        product = Product(
            **sample_product_data,
            status=ProductStatus.PENDING_REVIEW
        )
        db_session.add(product)
        db_session.commit()

        rejection_data = {"reason": "Not suitable for market"}
        response = client.post(
            f"/api/products/{product.id}/reject",
            json=rejection_data
        )
        assert response.status_code == status.HTTP_200_OK

        # Verify product was rejected
        db_session.refresh(product)
        assert product.status == ProductStatus.REJECTED
        assert product.rejection_reason == rejection_data["reason"]

    def test_reject_product_without_reason(self, client, db_session, sample_product_data):
        """Test rejecting a product without a reason fails validation"""
        product = Product(**sample_product_data)
        db_session.add(product)
        db_session.commit()

        response = client.post(
            f"/api/products/{product.id}/reject",
            json={"reason": ""}  # Empty reason should fail
        )
        # Should fail validation
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_400_BAD_REQUEST
        ]


class TestAnalyticsEndpoints:
    """Test analytics endpoints"""

    def test_dashboard_analytics(self, client, db_session):
        """Test dashboard analytics endpoint"""
        # Create some test products
        for i in range(5):
            product = Product(
                title=f"Product {i}",
                status=ProductStatus.PENDING_REVIEW if i < 3 else ProductStatus.APPROVED
            )
            db_session.add(product)
        db_session.commit()

        response = client.get("/api/analytics/dashboard")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "total_products" in data
        assert "pending_review" in data
        assert "approved" in data
        assert data["total_products"] == 5
        assert data["pending_review"] == 3
        assert data["approved"] == 2
