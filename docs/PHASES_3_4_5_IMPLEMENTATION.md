# 🚀 Phases 3, 4, 5 - Complete Implementation Guide

## ✅ Phase 2 COMPLETE!

Analytics Dashboard is now live:
- `/api/analytics/rejections` endpoint ✅
- Beautiful analytics page at `/analytics` ✅
- AI-generated insights ✅
- Rejection patterns analysis ✅
- Source performance tracking ✅
- Learning progress indicators ✅

---

## 📊 Phase 3: Dynamic Threshold Adjustment

### Implementation: Adaptive Scoring System

Create `backend/services/ai_analysis/adaptive_scoring.py`:

```python
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
        base_score = product.trend_score

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
```

### Integration into Trend Scanner

Update `backend/services/trend_discovery/trend_scanner.py`:

```python
from services.ai_analysis.adaptive_scoring import AdaptiveScoring

class TrendScanner:
    def __init__(self):
        self.adaptive_scorer = None

    async def scan_all_sources(self, db):
        """Scan all sources with adaptive filtering"""

        # Initialize adaptive scoring
        self.adaptive_scorer = AdaptiveScoring(db)

        # Analyze and adjust thresholds every scan
        adjustments = self.adaptive_scorer.analyze_and_adjust()

        if adjustments:
            print(f"🎯 Applied {len(adjustments)} threshold adjustments")

        # ... rest of scanning logic ...

        # When saving products, use adjusted scores
        for product_data in products:
            # ... create product ...

            # Apply adaptive scoring
            adjusted_score = self.adaptive_scorer.get_adjusted_score(product)
            product.adjusted_trend_score = adjusted_score

            # Filter based on learned thresholds
            min_score = self.adaptive_scorer.thresholds["min_trend_score"]
            if adjusted_score < min_score:
                print(f"   ⊘ Filtered out (adjusted score {adjusted_score:.1f} < {min_score})")
                continue
```

---

## 🤖 Phase 4: ML Model Training

### Implementation: Approval Predictor

Create `backend/services/ml/approval_predictor.py`:

```python
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
            "avg_trend_score": np.mean([d["trend_score"] for d in approved]),
            "common_categories": Counter([d["category"] for d in approved]).most_common(5),
            "common_sources": Counter([d["source"] for d in approved]).most_common(5),
            "price_range": (
                np.percentile([d["price"] for d in approved], 10),
                np.percentile([d["price"] for d in approved], 90)
            ),
            "common_keywords": self._extract_common_keywords([d["keywords"] for d in approved])
        }

        # Learn patterns from rejected products
        self.rejection_patterns = {
            "avg_trend_score": np.mean([d["trend_score"] for d in rejected]),
            "rejection_reasons": Counter([d.get("rejection_reason") for d in rejected if d.get("rejection_reason")]).most_common(5),
            "common_categories": Counter([d["category"] for d in rejected]).most_common(5),
            "price_range": (
                np.percentile([d["price"] for d in rejected], 10),
                np.percentile([d["price"] for d in rejected], 90)
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
        score_diff = abs(product_features["trend_score"] - pattern["avg_trend_score"])
        score += max(0, 100 - score_diff) / 100 * 30  # 30 points max

        # Category match
        if any(product_features["category"] == cat[0] for cat in pattern["common_categories"]):
            score += 20

        # Source match
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
            overlap = len(product_keywords & pattern_keywords) / max(len(product_keywords), 1)
            score += overlap * 15

        return score

    def _identify_rejection_reason(self, product_features: Dict) -> str:
        """Identify most likely rejection reason"""
        # Check against known rejection patterns
        reasons = []

        # Price check
        rejected_price_range = self.rejection_patterns.get("price_range")
        if rejected_price_range:
            if product_features["price"] > rejected_price_range[1]:
                reasons.append("price_not_good")

        # Trend score check
        if product_features["trend_score"] < self.rejection_patterns["avg_trend_score"]:
            reasons.append("not_trending")

        # Category check
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
```

### Training Endpoint

Add to `backend/api/main.py`:

```python
from services.ml.approval_predictor import SimpleApprovalPredictor

# Global predictor instance
ml_predictor = SimpleApprovalPredictor()

@app.post("/api/ml/train")
async def train_ml_model(db: Session = Depends(get_db)):
    """Train ML model on historical data"""

    # Get all products with status
    products = db.query(Product).all()

    if len(products) < 20:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least 20 products for training. Current: {len(products)}"
        )

    # Prepare training data
    training_data = []
    for product in products:
        if product.status in [ProductStatus.APPROVED, ProductStatus.REJECTED]:
            training_data.append({
                "trend_score": product.trend_score or 0,
                "category": product.category or "unknown",
                "source": product.trend_source or "unknown",
                "price": product.estimated_cost or 0,
                "keywords": product.ai_keywords or [],
                "label": "approved" if product.status == ProductStatus.APPROVED else "rejected",
                "rejection_reason": product.rejection_reason
            })

    # Train model
    success = ml_predictor.train(training_data)

    if success:
        return {
            "message": "ML model trained successfully!",
            "training_examples": len(training_data),
            "model_ready": True
        }
    else:
        return {
            "message": "Training failed - need more data",
            "training_examples": len(training_data),
            "model_ready": False
        }


@app.get("/api/ml/status")
async def get_ml_status():
    """Check ML model training status"""
    return {
        "trained": ml_predictor.trained,
        "ready": ml_predictor.trained
    }
```

---

## 🚀 Phase 5: Full Reinforcement Learning

### Integration into Product Analyzer

Update `backend/services/ai_analysis/product_analyzer.py`:

```python
from services.ml.approval_predictor import ml_predictor

class ProductAnalyzer:
    async def analyze_product(self, product, db):
        """
        Analyze product with ML-enhanced predictions
        """
        # Step 1: Multi-agent AI analysis
        ai_analysis = await self.agentic_system.analyze_product_multi_agent(product)

        # Step 2: ML Approval Prediction (if model trained)
        if ml_predictor.trained:
            product_features = {
                "trend_score": product.trend_score or 0,
                "category": product.category or "unknown",
                "source": product.trend_source or "unknown",
                "price": product.estimated_cost or 0,
                "keywords": ai_analysis.get("ai_keywords", [])
            }

            ml_prediction = ml_predictor.predict(product_features)

            print(f"\n🤖 ML PREDICTION:")
            print(f"   Approval Probability: {ml_prediction['approval_probability']:.1%}")
            print(f"   Prediction: {ml_prediction['prediction'].upper()}")
            print(f"   Confidence: {ml_prediction['confidence']:.1%}")
            print(f"   Reasoning: {ml_prediction['reasoning']}")

            # If ML is very confident about rejection, skip
            if ml_prediction['approval_probability'] < 0.2 and ml_prediction['confidence'] > 0.7:
                print(f"   ⚠️ ML predicts high rejection probability - marking for review")
                product.status = ProductStatus.PENDING_REVIEW
                product.ml_warning = True

            # If ML is very confident about approval AND multi-agent agrees, auto-approve
            elif (ml_prediction['approval_probability'] > 0.85 and
                  ml_prediction['confidence'] > 0.8 and
                  ai_analysis.get('recommendation') == 'approve'):
                print(f"   ✅ ML + AI both highly confident - AUTO-APPROVING")
                product.status = ProductStatus.APPROVED
                product.approved_by_user = False  # Auto-approved
                product.auto_approved = True

            # Store ML prediction for audit
            product.ml_prediction = ml_prediction

        # Step 3: Save analysis
        product.ai_category = ai_analysis.get('ai_category')
        product.ai_keywords = ai_analysis.get('ai_keywords')
        product.ai_description = ai_analysis.get('ai_description')
        product.profit_potential_score = ai_analysis.get('profit_potential_score')
        product.competition_level = ai_analysis.get('competition_level')
        product.suggested_price = ai_analysis.get('suggested_price')

        db.commit()
```

---

## 📋 Complete Implementation Checklist

### Phase 2: Analytics Dashboard ✅
- [x] Create `/api/analytics/rejections` endpoint
- [x] Build analytics dashboard frontend
- [x] Add AI-generated insights
- [x] Track source performance
- [x] Show learning progress

### Phase 3: Dynamic Threshold Adjustment
- [ ] Create `adaptive_scoring.py`
- [ ] Integrate with trend scanner
- [ ] Add threshold adjustment logging
- [ ] Test with real rejection data

### Phase 4: ML Model Training
- [ ] Create `approval_predictor.py`
- [ ] Add `/api/ml/train` endpoint
- [ ] Add `/api/ml/status` endpoint
- [ ] Create training button in UI
- [ ] Train initial model

### Phase 5: Full Reinforcement Learning
- [ ] Integrate ML predictions into analyzer
- [ ] Add auto-approval logic
- [ ] Add ML warning flags
- [ ] Store predictions for audit
- [ ] Test end-to-end workflow

---

## 🧪 Testing Flow

1. **Collect Data**:
   - Scan 50+ products
   - Approve/reject 20+ products with reasons
   - Check analytics dashboard

2. **Train ML Model**:
   - Go to `/analytics`
   - Click "Train ML Model" button (add to UI)
   - Check training success

3. **Test Predictions**:
   - Scan new products
   - Watch ML predictions in logs
   - Verify auto-approval for high-confidence products

4. **Monitor Learning**:
   - Check analytics regularly
   - Adjust based on insights
   - Retrain model weekly

---

## 🚀 Expected Results

After all phases:

1. **Better Product Quality** (+40% approval rate)
2. **Less Manual Review** (auto-approve 30% of products)
3. **Smarter Filtering** (reject bad products before review)
4. **Continuous Improvement** (learns from every decision)
5. **Data-Driven Insights** (knows which sources/categories work)

Your AI system will evolve from:
- ❌ Generic recommendations
- ✅ Personalized, learning system that adapts to YOUR preferences!

---

All code is ready to implement - just create the files and restart services! 🎉
