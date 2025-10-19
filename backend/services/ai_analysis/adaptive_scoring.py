"""
Dynamic Threshold Adjustment System
Automatically adjusts scoring based on rejection patterns
"""

from sqlalchemy.orm import Session
from models.database import Product, ProductStatus
from typing import Dict, Any

class AdaptiveScoring:
    """
    Learns from rejection patterns and adjusts thresholds
    """

    def __init__(self, db: Session):
        self.db = db
        self.thresholds = self._load_current_thresholds()

    def _load_current_thresholds(self) -> Dict[str, Any]:
        """Load current threshold configuration"""
        return {
            "min_trend_score": 70,
            "min_search_volume": 100,
            "source_weights": {
                "amazon": 1.0,
                "google_trends": 1.0,
                "reddit": 0.8,
            },
            "category_priorities": {}
        }

    def analyze_and_adjust(self) -> Dict[str, Any]:
        """
        Analyze rejection patterns and suggest threshold adjustments
        """
        adjustments = {}

        # 1. Adjust minimum trend score
        score_adjustment = self._analyze_score_patterns()
        if score_adjustment:
            adjustments["min_trend_score"] = score_adjustment

        # 2. Adjust source weights
        source_adjustments = self._analyze_source_performance()
        if source_adjustments:
            adjustments["source_weights"] = source_adjustments

        # 3. Adjust category priorities
        category_adjustments = self._analyze_category_performance()
        if category_adjustments:
            adjustments["category_priorities"] = category_adjustments

        # Apply adjustments
        if adjustments:
            self._apply_adjustments(adjustments)

        return adjustments

    def _analyze_score_patterns(self) -> int:
        """
        Analyze if we need to raise/lower minimum trend score
        """
        # Get products in each score range
        score_ranges = {
            "0-50": (0, 50),
            "50-70": (50, 70),
            "70-85": (70, 85),
            "85-100": (85, 100)
        }

        for range_name, (min_score, max_score) in score_ranges.items():
            products = self.db.query(Product).filter(
                Product.trend_score >= min_score,
                Product.trend_score < max_score
            ).all()

            if len(products) < 5:
                continue

            rejected = sum(1 for p in products if p.status == ProductStatus.REJECTED)
            rejection_rate = rejected / len(products)

            # If rejection rate > 70% in a range, raise minimum
            if rejection_rate > 0.7 and min_score < 85:
                return max_score  # New minimum

        return None

    def _analyze_source_performance(self) -> Dict[str, float]:
        """
        Adjust weights for each trend source
        """
        source_weights = {}

        sources = self.db.query(Product.trend_source).distinct().all()
        for (source,) in sources:
            if not source:
                continue

            products = self.db.query(Product).filter(
                Product.trend_source == source
            ).all()

            if len(products) < 3:
                continue

            rejected = sum(1 for p in products if p.status == ProductStatus.REJECTED)
            approved = sum(1 for p in products if p.status == ProductStatus.APPROVED)

            rejection_rate = rejected / len(products) if products else 0
            approval_rate = approved / len(products) if products else 0

            # Calculate weight based on performance
            if rejection_rate > 0.6:
                # Poor performance - reduce weight
                source_weights[source] = 0.5
            elif approval_rate > 0.6:
                # Excellent performance - increase weight
                source_weights[source] = 1.2
            else:
                # Normal performance
                source_weights[source] = 1.0

        return source_weights

    def _analyze_category_performance(self) -> Dict[str, str]:
        """
        Identify categories to prioritize or avoid
        """
        category_priorities = {}

        categories = self.db.query(Product.category).distinct().all()
        for (category,) in categories:
            if not category:
                continue

            products = self.db.query(Product).filter(
                Product.category == category
            ).all()

            if len(products) < 3:
                continue

            rejected = sum(1 for p in products if p.status == ProductStatus.REJECTED)
            approved = sum(1 for p in products if p.status == ProductStatus.APPROVED)

            rejection_rate = rejected / len(products) if products else 0
            approval_rate = approved / len(products) if products else 0

            if rejection_rate > 0.7:
                category_priorities[category] = "avoid"
            elif approval_rate > 0.7:
                category_priorities[category] = "prioritize"
            else:
                category_priorities[category] = "normal"

        return category_priorities

    def _apply_adjustments(self, adjustments: Dict[str, Any]):
        """
        Save adjustments to configuration
        (In production, save to database or config file)
        """
        print("\n" + "="*60)
        print("🔧 ADAPTIVE SCORING - Applying Adjustments")
        print("="*60)

        for key, value in adjustments.items():
            print(f"  • {key}: {value}")
            self.thresholds[key] = value

        print("="*60 + "\n")

    def get_adjusted_score(self, product) -> float:
        """
        Calculate adjusted score for a product based on learned patterns
        """
        base_score = product.trend_score or 0

        # Apply source weight
        source = product.trend_source or "unknown"
        source_weight = self.thresholds["source_weights"].get(source, 1.0)

        # Apply category adjustment
        category = product.category or "unknown"
        category_priority = self.thresholds["category_priorities"].get(category, "normal")

        category_multiplier = {
            "prioritize": 1.15,
            "normal": 1.0,
            "avoid": 0.85
        }[category_priority]

        adjusted_score = base_score * source_weight * category_multiplier

        return adjusted_score
