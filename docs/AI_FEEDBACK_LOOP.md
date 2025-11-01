# 🤖 AI Feedback Loop - Reinforcement Learning from User Rejections

## Overview

This system implements a **feedback loop** where user rejection decisions train the AI to find better products over time. Instead of deleting rejected products, we store them with detailed rejection reasons to create a training dataset for **reinforcement learning**.

---

## How It Works

### 1. **User Rejects a Product**

When a user rejects a product, they select from structured rejection reasons:

- 💰 **Price Not Good Enough** - Product pricing isn't competitive
- 👎 **Bad Product Quality** - Low-quality or problematic product
- 📉 **Not a Hot/Trending Product** - Not actually trending
- ⚔️ **Too Much Competition** - Market is too competitive
- 📊 **Profit Margin Too Low** - Not profitable enough
- 🏪 **Market Already Saturated** - Too many similar products
- 🏷️ **Wrong Product Category** - Outside target categories
- ❓ **Other Reason** - Custom feedback

### 2. **Data is Stored**

```python
# Database stores:
product.status = "rejected"
product.rejection_reason = "not_trending"  # User's reason
product.rejected_at = "2025-10-18 21:45:00"  # Timestamp
```

### 3. **AI Learns from Patterns**

The system can analyze rejection patterns to improve:

**Example Patterns:**
```
Rejection Reason: "not_trending"
- Products with trend_score < 75 → 80% rejection rate
- Products from Reddit source → 65% rejection rate
- Products in "Gadgets" category → 45% rejection rate

Action: Adjust thresholds
- Minimum trend_score: 75 → 85
- Reddit weight: 1.0 → 0.7
- Gadgets category: normal → low priority
```

---

## Implementation Roadmap

### Phase 1: Data Collection ✅ (CURRENT)

**Status: COMPLETE**

- [x] Store rejected products in database
- [x] Capture structured rejection reasons
- [x] Track rejection timestamps
- [x] Display rejection reasons in UI
- [x] Build rejection history dataset

**What's Working:**
- Users can reject products with specific reasons
- All rejection data is preserved in database
- Rejected products visible in "Rejected" tab
- Rejection reasons displayed on product cards

---

### Phase 2: Analytics Dashboard (NEXT)

**Create rejection analytics endpoint:**

```python
@app.get("/api/analytics/rejections")
async def get_rejection_analytics(db: Session = Depends(get_db)):
    """Analyze rejection patterns for AI improvement"""

    # Count by reason
    rejection_counts = db.query(
        Product.rejection_reason,
        func.count(Product.id)
    ).filter(
        Product.status == ProductStatus.REJECTED
    ).group_by(Product.rejection_reason).all()

    # Rejection rate by trend score range
    score_ranges = {
        "0-50": db.query(Product).filter(
            Product.trend_score < 50,
            Product.status == ProductStatus.REJECTED
        ).count(),
        "50-75": db.query(Product).filter(
            Product.trend_score >= 50,
            Product.trend_score < 75,
            Product.status == ProductStatus.REJECTED
        ).count(),
        "75-100": db.query(Product).filter(
            Product.trend_score >= 75,
            Product.status == ProductStatus.REJECTED
        ).count(),
    }

    # Rejection rate by source
    source_rejections = db.query(
        Product.trend_source,
        func.count(Product.id)
    ).filter(
        Product.status == ProductStatus.REJECTED
    ).group_by(Product.trend_source).all()

    return {
        "rejection_by_reason": dict(rejection_counts),
        "rejection_by_score_range": score_ranges,
        "rejection_by_source": dict(source_rejections),
        "total_rejections": db.query(Product).filter(
            Product.status == ProductStatus.REJECTED
        ).count()
    }
```

**Frontend Dashboard:**
- Charts showing rejection reasons (pie chart)
- Trend score vs rejection rate (line chart)
- Source performance (bar chart)
- Category rejection rates

---

### Phase 3: Dynamic Threshold Adjustment

**Automatically adjust AI scoring based on rejection patterns:**

```python
class AdaptiveScoring:
    """
    Adjusts product scoring based on user feedback
    """

    def calculate_adjusted_score(self, product, rejection_history):
        base_score = product.trend_score

        # Get rejection patterns for similar products
        similar_rejected = self._get_similar_rejections(
            category=product.category,
            source=product.trend_source,
            price_range=product.estimated_cost
        )

        # Calculate penalties based on historical rejections
        penalties = {
            "category_penalty": self._category_rejection_rate(product.category) * 10,
            "source_penalty": self._source_rejection_rate(product.trend_source) * 15,
            "price_penalty": self._price_rejection_rate(product.estimated_cost) * 5,
        }

        # Apply penalties
        adjusted_score = base_score
        for penalty_name, penalty_value in penalties.items():
            adjusted_score -= penalty_value

        # Store adjustment metadata
        product.score_adjustments = {
            "original_score": base_score,
            "adjusted_score": adjusted_score,
            "penalties_applied": penalties,
            "reason": "user_feedback_learning"
        }

        return adjusted_score
```

---

### Phase 4: Reinforcement Learning Model

**Train a neural network to predict approval probability:**

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class ProductApprovalPredictor:
    """
    Uses transformer model to predict if user will approve product
    Trained on historical approval/rejection data
    """

    def __init__(self):
        # Use a pre-trained model and fine-tune on our data
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "microsoft/deberta-v3-small",  # Free open-source model
            num_labels=8  # 8 rejection categories + approve
        )
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-small")

    def prepare_training_data(self, db):
        """
        Prepare training dataset from approved and rejected products
        """
        # Get approved products (positive examples)
        approved = db.query(Product).filter(
            Product.status == ProductStatus.APPROVED
        ).all()

        # Get rejected products (negative examples)
        rejected = db.query(Product).filter(
            Product.status == ProductStatus.REJECTED
        ).all()

        training_data = []

        for product in approved:
            training_data.append({
                "text": f"{product.title} {product.description} {product.category}",
                "label": "approved",
                "features": {
                    "trend_score": product.trend_score,
                    "price": product.estimated_cost,
                    "source": product.trend_source,
                }
            })

        for product in rejected:
            training_data.append({
                "text": f"{product.title} {product.description} {product.category}",
                "label": product.rejection_reason,  # Use rejection reason as label
                "features": {
                    "trend_score": product.trend_score,
                    "price": product.estimated_cost,
                    "source": product.trend_source,
                }
            })

        return training_data

    def train(self, training_data):
        """
        Fine-tune model on user approval/rejection data
        """
        # Convert to torch dataset
        # Train with gradient descent
        # Save model weights
        pass

    def predict_approval_probability(self, product):
        """
        Predict probability user will approve this product
        """
        text = f"{product.title} {product.description} {product.category}"
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)

        # Return probability of approval
        return {
            "approval_probability": probabilities[0][0].item(),
            "predicted_rejection_reason": self._get_top_rejection_reason(probabilities),
            "confidence": torch.max(probabilities).item()
        }
```

---

### Phase 5: Active Learning Integration

**Integrate ML predictions into product analyzer:**

```python
# In backend/services/ai_analysis/product_analyzer.py

async def analyze_product(self, product, db):
    """
    Analyze product with ML-enhanced scoring
    """

    # Step 1: Multi-agent AI analysis (existing)
    ai_analysis = await self.agentic_system.analyze_product_multi_agent(product)

    # Step 2: Check approval predictor (NEW)
    if self.approval_predictor:
        ml_prediction = self.approval_predictor.predict_approval_probability(product)

        print(f"\n🤖 ML PREDICTION:")
        print(f"   Approval Probability: {ml_prediction['approval_probability']:.2%}")
        print(f"   Confidence: {ml_prediction['confidence']:.2%}")

        # If approval probability is too low, skip or downgrade
        if ml_prediction['approval_probability'] < 0.3:
            print(f"   ⚠️ Low approval probability - likely to be rejected")
            print(f"   Predicted reason: {ml_prediction['predicted_rejection_reason']}")

            # Option 1: Skip entirely
            # return None

            # Option 2: Downgrade score
            ai_analysis['profit_potential_score'] *= 0.5
            ai_analysis['ml_warning'] = True
            ai_analysis['ml_prediction'] = ml_prediction

    # Step 3: Save analysis
    product.profit_potential_score = ai_analysis.get('profit_potential_score', 70)
    # ... rest of analysis
```

---

## Benefits of This System

### 1. **Continuous Improvement**
- AI gets smarter with every rejection
- No manual tuning needed
- Learns your specific preferences

### 2. **Personalized Recommendations**
- Different users = different preferences
- Model adapts to each user's rejection patterns
- Can support multi-user systems with user-specific models

### 3. **Data-Driven Decisions**
- See exactly why products are rejected
- Identify weak trend sources
- Optimize category selection

### 4. **Reduced Noise**
- Fewer bad products over time
- Higher quality recommendations
- Less time reviewing obvious rejects

---

## Current Status

✅ **Implemented:**
- Soft delete with rejection reasons
- 8 structured rejection categories
- Rejection reason storage in database
- Rejection display in UI
- "Rejected" products tab
- Rejection timestamp tracking

📋 **Next Steps:**
1. Create rejection analytics dashboard
2. Implement dynamic scoring adjustments
3. Build training data pipeline
4. Train initial ML model
5. Integrate predictions into scanner

---

## Database Schema

```sql
-- products table
CREATE TABLE products (
    -- ... other fields ...

    status VARCHAR(50),  -- 'discovered', 'analyzing', 'pending_review', 'approved', 'rejected', 'posted'
    rejection_reason TEXT,  -- 'price_not_good', 'bad_product', 'not_trending', etc.
    rejected_at TIMESTAMP,  -- When was it rejected
    approved_by_user BOOLEAN,  -- Manual override

    -- ... other fields ...
);

-- Query rejections
SELECT
    rejection_reason,
    COUNT(*) as count,
    AVG(trend_score) as avg_trend_score,
    AVG(estimated_cost) as avg_price
FROM products
WHERE status = 'rejected'
GROUP BY rejection_reason
ORDER BY count DESC;

-- Find patterns
SELECT
    trend_source,
    COUNT(*) as total_products,
    SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected,
    ROUND(100.0 * SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) / COUNT(*), 2) as rejection_rate
FROM products
GROUP BY trend_source
ORDER BY rejection_rate DESC;
```

---

## Usage

### For Users

1. **Reject products with specific reasons** - This trains the AI
2. **Be consistent** - Use the same reasons for similar issues
3. **Review rejected tab** - See what the AI learned not to recommend
4. **Watch improvements** - AI will send fewer bad products over time

### For Developers

1. **Monitor rejection analytics** - Track which sources/categories perform poorly
2. **Adjust thresholds** - Use analytics to tune minimum scores
3. **Train ML models** - Use rejection data to build predictive models
4. **A/B test improvements** - Test if changes reduce rejection rates

---

## Example Use Cases

### Use Case 1: High Reddit Rejection Rate

**Observation:**
```
Source: Reddit
Total Products: 100
Rejected: 65
Rejection Rate: 65%
Top Reason: "not_trending" (80%)
```

**Action:**
- Reduce Reddit scan frequency
- Increase minimum trend score for Reddit products from 70 → 85
- Add "upvote ratio" requirement

**Result:**
- Rejection rate drops to 30%
- Better product quality from Reddit source

---

### Use Case 2: Price Sensitivity

**Observation:**
```
Rejection Reason: "price_not_good" (45% of rejections)
Products with price > $100: 70% rejection rate
Products with price < $30: 20% rejection rate
```

**Action:**
- Adjust price scoring algorithm
- Prioritize products in $20-80 range
- Flag expensive products for review

**Result:**
- Price-related rejections drop from 45% → 15%
- More products in preferred price range

---

## Future Enhancements

1. **Multi-user support** - Different models per user
2. **Seasonal adjustments** - Learn seasonal preferences
3. **Category-specific models** - Specialize by product type
4. **Confidence scoring** - Show AI's confidence in recommendations
5. **Explainable AI** - Show why AI thinks you'll like/reject a product
6. **Auto-approve high-confidence** - Skip review for obvious winners

---

## Metrics to Track

```python
metrics = {
    "rejection_rate": rejected / total,  # Want this to decrease over time
    "approval_rate": approved / total,  # Want this to increase
    "review_time_saved": avg_products_per_scan * rejection_rate * 30_seconds,
    "ml_accuracy": correct_predictions / total_predictions,
    "false_positives": predicted_approve_but_rejected,  # Minimize
    "false_negatives": predicted_reject_but_approved,  # Minimize
}
```

---

## Ready to Start Learning! 🎓

Your system is now set up to learn from every rejection. As you review products:

1. **Each rejection** creates training data
2. **Patterns emerge** from your decisions
3. **AI adapts** to your preferences
4. **Quality improves** automatically

The more products you review, the smarter the AI becomes! 🚀
