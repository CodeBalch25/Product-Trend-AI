"""
Perplexity-Powered Trend Discovery Service

This service uses Perplexity's real-time web search to:
1. Discover NEW trending products and keywords from the web
2. Feed intelligence back to the trend scanner
3. Create a self-improving trend detection system
"""
import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Any


class PerplexityTrendDiscovery:
    """
    Proactive trend discovery using Perplexity's real-time web search
    """

    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar"  # Updated to valid Perplexity model

    async def discover_trending_products(self, category: str = None) -> Dict[str, Any]:
        """
        Use Perplexity to discover what's actually trending RIGHT NOW on the web

        Args:
            category: Optional category to focus on (e.g., "beauty", "electronics")

        Returns:
            Dict with discovered trends, keywords, and products
        """

        # Build search query based on category
        if category:
            search_focus = f"trending {category} products"
        else:
            search_focus = "viral products trending"

        prompt = f"""You are a Trend Discovery AI with real-time web access. Your job is to find what's ACTUALLY trending RIGHT NOW (not predictions).

**YOUR TASK: Discover Real-Time Trending Products**

Use your web search capability to find:

**STEP 1: Search Social Media Trends**
- Search: "viral products TikTok 2025"
- Search: "trending on Amazon right now"
- Search: "what's selling on eBay today"
- Search: "Instagram viral products"
- Find products with HIGH recent engagement (last 7-30 days)

**STEP 2: Search E-commerce Trends**
- Search: "{search_focus} 2025"
- Search: "best selling products this month"
- Search: "hottest products right now"
- Identify products with increasing search volume

**STEP 3: Search News & Media**
- Search: "new product launches 2025"
- Search: "products going viral"
- Find products getting media coverage

**STEP 4: Extract Intelligence**
For each trending product found:
- Product name/description
- Why it's trending (data points: views, searches, sales)
- Category
- Estimated price range
- Trend velocity (explosive/steady/emerging)
- Keywords people use to search for it

**REQUIRED OUTPUT (Valid JSON only)**:
{{
    "discovered_products": [
        {{
            "product_name": "Exact product name",
            "description": "What it is and what it does",
            "category": "Product category",
            "price_range": {{"min": 0, "max": 0}},
            "trend_strength": "explosive|strong|emerging",
            "evidence": "Why it's trending (specific data: views, searches, sales)",
            "keywords": ["keyword1", "keyword2", "keyword3"],
            "platforms": ["TikTok|Instagram|Amazon|etc"],
            "source_urls": ["url1", "url2"]
        }}
    ],
    "trending_keywords": [
        {{
            "keyword": "search term people are using",
            "search_volume_trend": "rising|stable",
            "category": "category",
            "related_products": ["product1", "product2"]
        }}
    ],
    "market_insights": {{
        "hot_categories": ["category1", "category2"],
        "emerging_niches": ["niche1", "niche2"],
        "fading_trends": ["trend1", "trend2"],
        "key_observations": "What patterns are you seeing across platforms?"
    }}
}}

**QUALITY REQUIREMENTS**:
- ✅ Only include products with RECENT trend data (last 30 days)
- ✅ Provide specific evidence (views, searches, sales numbers)
- ✅ Include source URLs for verification
- ✅ Focus on products that can be sourced and sold (not unicorns)
- ✅ Extract actual search keywords people are using

Find 5-10 high-quality trending products with strong evidence. Be specific with data, not vague."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a trend discovery AI with real-time web search. Find what's actually trending NOW with data to prove it."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 3000
            }

            print(f"\n🌐 [PERPLEXITY DISCOVERY] Searching web for trending products...")
            print(f"   Focus: {search_focus}")

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                # Parse JSON response
                discovered = self._parse_json_response(content)

                print(f"   ✅ Discovery complete!")
                print(f"   📦 Found {len(discovered.get('discovered_products', []))} trending products")
                print(f"   🔑 Found {len(discovered.get('trending_keywords', []))} trending keywords")

                return discovered

            else:
                print(f"   ❌ Perplexity API error: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error details: {error_detail}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return self._fallback_discovery()

        except Exception as e:
            print(f"   ❌ Perplexity discovery failed: {str(e)[:100]}")
            return self._fallback_discovery()

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON from Perplexity response"""
        try:
            # Try to find JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)
            return {}
        except:
            return {}

    def _fallback_discovery(self) -> Dict[str, Any]:
        """Fallback when Perplexity is unavailable"""
        return {
            "discovered_products": [],
            "trending_keywords": [],
            "market_insights": {
                "hot_categories": [],
                "emerging_niches": [],
                "fading_trends": [],
                "key_observations": "Web search unavailable - using fallback"
            },
            "status": "fallback"
        }

    def update_trend_scanner_intel(self, db, discovered_data: Dict[str, Any]) -> None:
        """
        Feed discovered trends back to the trend scanner
        Updates the system's knowledge of what to look for
        """
        try:
            print("\n🔄 [FEEDBACK LOOP] Updating system intelligence...")

            # Extract keywords to search for
            keywords = []
            for product in discovered_data.get('discovered_products', []):
                keywords.extend(product.get('keywords', []))

            for kw_data in discovered_data.get('trending_keywords', []):
                keywords.append(kw_data.get('keyword'))

            # Remove duplicates
            keywords = list(set(keywords))

            if keywords:
                print(f"   📝 Extracted {len(keywords)} trending keywords:")
                for kw in keywords[:10]:  # Show first 10
                    print(f"      - {kw}")

                # Store in database for future use
                self._store_trending_keywords(db, keywords, discovered_data)

                print(f"   ✅ System intelligence updated!")
                return keywords

            return []

        except Exception as e:
            print(f"   ❌ Failed to update intelligence: {str(e)[:100]}")
            return []

    def _store_trending_keywords(self, db, keywords: List[str], discovered_data: Dict[str, Any]) -> None:
        """
        Store trending keywords in database for trend scanner to use

        This creates a feedback loop:
        1. Perplexity discovers trending keywords
        2. Keywords stored in DB
        3. Trend scanner reads keywords and searches for related products
        4. System learns what's hot
        """
        try:
            from models.database import TrendingKeyword
            from datetime import datetime, timedelta

            # Store each keyword with metadata
            for keyword in keywords:
                # Find related products for this keyword
                related_products = []
                for product in discovered_data.get('discovered_products', []):
                    if keyword.lower() in ' '.join(product.get('keywords', [])).lower():
                        related_products.append(product.get('product_name'))

                # Check if keyword already exists
                existing = db.query(TrendingKeyword).filter(
                    TrendingKeyword.keyword == keyword
                ).first()

                if existing:
                    # Update existing
                    existing.search_count += 1
                    existing.last_seen = datetime.utcnow()
                    existing.related_products = related_products[:5]  # Top 5
                else:
                    # Create new
                    new_keyword = TrendingKeyword(
                        keyword=keyword,
                        category=self._infer_category(keyword, discovered_data),
                        search_count=1,
                        trend_strength="emerging",
                        last_seen=datetime.utcnow(),
                        expires_at=datetime.utcnow() + timedelta(days=30),
                        related_products=related_products[:5]
                    )
                    db.add(new_keyword)

            db.commit()
            print(f"   💾 Stored {len(keywords)} keywords in database")

        except Exception as e:
            print(f"   ⚠️ Could not store keywords (table may not exist): {str(e)[:100]}")
            db.rollback()

    def _infer_category(self, keyword: str, discovered_data: Dict[str, Any]) -> str:
        """Infer category from keyword and discovered data"""
        # Check if keyword is in any product's category
        for product in discovered_data.get('discovered_products', []):
            if keyword.lower() in ' '.join(product.get('keywords', [])).lower():
                return product.get('category', 'General')

        # Default
        return 'General'

    async def enrich_product_search(self, db, search_query: str) -> List[str]:
        """
        Use discovered keywords to enrich product searches

        Example: User searches "beauty" → Returns ["heated eyelash curler", "viral mascara", etc.]
        """
        try:
            from models.database import TrendingKeyword
            from datetime import datetime

            # Get related trending keywords from DB
            keywords = db.query(TrendingKeyword).filter(
                TrendingKeyword.keyword.ilike(f"%{search_query}%"),
                TrendingKeyword.expires_at > datetime.utcnow()
            ).order_by(
                TrendingKeyword.search_count.desc()
            ).limit(10).all()

            # Return keyword strings
            return [kw.keyword for kw in keywords]

        except Exception as e:
            print(f"   ⚠️ Could not enrich search: {str(e)[:100]}")
            return []
