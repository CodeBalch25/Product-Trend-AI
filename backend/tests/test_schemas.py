"""
Schema validation tests
"""
import pytest
from pydantic import ValidationError
from schemas.product import ProductRejectRequest, ProductPostRequest
from schemas.common import PaginationParams


class TestProductRejectRequest:
    """Test ProductRejectRequest schema"""

    def test_valid_rejection(self):
        """Test valid rejection request"""
        data = {"reason": "Not suitable for our market"}
        request = ProductRejectRequest(**data)
        assert request.reason == "Not suitable for our market"

    def test_empty_reason_fails(self):
        """Test that empty reason fails validation"""
        with pytest.raises(ValidationError):
            ProductRejectRequest(reason="")

    def test_whitespace_only_reason_fails(self):
        """Test that whitespace-only reason fails validation"""
        with pytest.raises(ValidationError):
            ProductRejectRequest(reason="   ")

    def test_reason_too_long_fails(self):
        """Test that overly long reason fails validation"""
        with pytest.raises(ValidationError):
            ProductRejectRequest(reason="x" * 1001)


class TestProductPostRequest:
    """Test ProductPostRequest schema"""

    def test_valid_platforms(self):
        """Test valid platform list"""
        data = {"platforms": ["amazon", "ebay"]}
        request = ProductPostRequest(**data)
        assert request.platforms == ["amazon", "ebay"]

    def test_invalid_platform_fails(self):
        """Test that invalid platform fails validation"""
        with pytest.raises(ValidationError):
            ProductPostRequest(platforms=["invalid_platform"])

    def test_empty_platforms_fails(self):
        """Test that empty platform list fails validation"""
        with pytest.raises(ValidationError):
            ProductPostRequest(platforms=[])

    def test_platform_case_insensitive(self):
        """Test that platform names are case-insensitive"""
        data = {"platforms": ["AMAZON", "eBay"]}
        request = ProductPostRequest(**data)
        assert request.platforms == ["amazon", "ebay"]


class TestPaginationParams:
    """Test PaginationParams schema"""

    def test_default_values(self):
        """Test default pagination values"""
        params = PaginationParams()
        assert params.limit == 50
        assert params.offset == 0

    def test_custom_values(self):
        """Test custom pagination values"""
        params = PaginationParams(limit=25, offset=10)
        assert params.limit == 25
        assert params.offset == 10

    def test_limit_max_constraint(self):
        """Test that limit is capped at max value"""
        params = PaginationParams(limit=200)
        assert params.limit == 100  # Should be capped at MAX_PAGE_LIMIT

    def test_negative_offset_fails(self):
        """Test that negative offset fails validation"""
        with pytest.raises(ValidationError):
            PaginationParams(offset=-1)
