"""
ML Model for Predicting Product Approval
Uses lightweight models compatible with CPU-only servers
"""

import json
import numpy as np
from typing import Dict, List, Any
from collections import Counter

class SimpleApprovalPredictor:
    """
    Lightweight ML predictor using pattern matching
    (Can be upgraded to transformers when you have more data)
    """

    def __init__(self):
        self.model = None
        self.trained = False
        self.rejection_patterns = {}
        self.approval_patterns = {}

    def train(self, training_data: List[Dict[str, Any]]):
        """
        Train on historical approval/rejection data
        training_data format:
        [
            {
                "trend_score": 85,
                "category": "Electronics",
                "source": "amazon",
                "price": 49.99,
                "keywords": ["wireless", "bluetooth"],
                "label": "approved|rejected",
                "rejection_reason": "price_not_good" (if rejected)
            }
        ]
        """
        print("\n" + "="*60)
        print("🎓 TRAINING ML MODEL - Approval Predictor")
        print("="*60)

        if len(training_data) < 20:
            print("  ⚠️ Need at least 20 examples for training")
            print(f"  Current data: {len(training_data)} examples")
            return False

        # Separate by label
        approved = [d for d in training_data if d["label"] == "approved"]
        rejected = [d for d in training_data if d["label"] == "rejected"]

        print(f"  Training data: {len(approved)} approved, {len(rejected)} rejected")

        # Learn patterns from approved products
        self.approval_patterns = {
            "avg_trend_score": np.mean([d["trend_score"] for d in approved]) if approved else 0,
            "common_categories": Counter([d["category"] for d in approved]).most_common(5),
            "common_sources": Counter([d["source"] for d in approved]).most_common(5),
            "price_range": (
                np.percentile([d["price"] for d in approved], 10) if approved else 0,
                np.percentile([d["price"] for d in approved], 90) if approved else 0
            ),
            "common_keywords": self._extract_common_keywords([d["keywords"] for d in approved])
        }

        # Learn patterns from rejected products
        self.rejection_patterns = {
            "avg_trend_score": np.mean([d["trend_score"] for d in rejected]) if rejected else 0,
            "rejection_reasons": Counter([d.get("rejection_reason") for d in rejected if d.get("rejection_reason")]).most_common(5),
            "common_categories": Counter([d["category"] for d in rejected]).most_common(5),
            "price_range": (
                np.percentile([d["price"] for d in rejected], 10) if rejected else 0,
                np.percentile([d["price"] for d in rejected], 90) if rejected else 0
            )
        }

        self.trained = True

        print("  ✅ Model trained successfully!")
        print(f"  Approved products avg score: {self.approval_patterns['avg_trend_score']:.1f}")
        print(f"  Rejected products avg score: {self.rejection_patterns['avg_trend_score']:.1f}")
        print("="*60 + "\n")

        return True

    def predict(self, product_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict approval probability for a product
        """
        if not self.trained:
            return {
                "approval_probability": 0.5,
                "confidence": 0,
                "prediction": "unknown",
                "reasoning": "Model not trained yet"
            }

        # Calculate similarity to approved pattern
        approval_score = self._calculate_similarity(product_features, self.approval_patterns)

        # Calculate similarity to rejected pattern
        rejection_score = self._calculate_similarity(product_features, self.rejection_patterns)

        # Normalize to probability
        total = approval_score + rejection_score
        approval_probability = approval_score / total if total > 0 else 0.5

        # Determine prediction
        if approval_probability > 0.7:
            prediction = "approve"
            reasoning = "High similarity to approved products"
        elif approval_probability < 0.3:
            prediction = "reject"
            reasoning = self._identify_rejection_reason(product_features)
        else:
            prediction = "review"
            reasoning = "Unclear - needs manual review"

        return {
            "approval_probability": round(approval_probability, 3),
            "confidence": abs(approval_probability - 0.5) * 2,  # 0-1 scale
            "prediction": prediction,
            "reasoning": reasoning,
            "approval_score": round(approval_score, 2),
            "rejection_score": round(rejection_score, 2)
        }

    def _calculate_similarity(self, product_features: Dict, pattern: Dict) -> float:
        """Calculate similarity score to a pattern"""
        score = 0

        # Trend score similarity
        if pattern.get("avg_trend_score"):
            score_diff = abs(product_features["trend_score"] - pattern["avg_trend_score"])
            score += max(0, 100 - score_diff) / 100 * 30  # 30 points max

        # Category match
        if pattern.get("common_categories"):
            if any(product_features["category"] == cat[0] for cat in pattern["common_categories"]):
                score += 20

        # Source match
        if pattern.get("common_sources"):
            if any(product_features["source"] == src[0] for src in pattern.get("common_sources", [])):
                score += 15

        # Price range match
        if pattern.get("price_range"):
            min_price, max_price = pattern["price_range"]
            if min_price <= product_features["price"] <= max_price:
                score += 20

        # Keyword overlap
        if pattern.get("common_keywords"):
            product_keywords = set(product_features.get("keywords", []))
            pattern_keywords = set(pattern["common_keywords"])
            if product_keywords:
                overlap = len(product_keywords & pattern_keywords) / max(len(product_keywords), 1)
                score += overlap * 15

        return score

    def _identify_rejection_reason(self, product_features: Dict) -> str:
        """Identify most likely rejection reason"""
        # Check against known rejection patterns
        reasons = []

        # Price check
        rejected_price_range = self.rejection_patterns.get("price_range")
        if rejected_price_range and rejected_price_range[0] > 0:
            if product_features["price"] > rejected_price_range[1]:
                reasons.append("price_not_good")

        # Trend score check
        if self.rejection_patterns.get("avg_trend_score"):
            if product_features["trend_score"] < self.rejection_patterns["avg_trend_score"]:
                reasons.append("not_trending")

        # Category check
        if self.rejection_patterns.get("common_categories"):
            if any(product_features["category"] == cat[0] for cat in self.rejection_patterns["common_categories"][:2]):
                reasons.append("wrong_category")

        if reasons:
            return f"Likely rejection reasons: {', '.join(reasons)}"
        else:
            return "Similar to rejected products pattern"

    def _extract_common_keywords(self, keyword_lists: List[List[str]]) -> List[str]:
        """Extract most common keywords across all products"""
        all_keywords = [kw for keywords in keyword_lists for kw in keywords]
        return [kw for kw, count in Counter(all_keywords).most_common(20)]


# Global predictor instance
ml_predictor = SimpleApprovalPredictor()
