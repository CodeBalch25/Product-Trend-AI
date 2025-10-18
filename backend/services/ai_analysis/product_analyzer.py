"""
AI-powered product analysis service
"""
from typing import Dict, Any, Optional
from datetime import datetime
import json

from backend.config.settings import settings


class ProductAnalyzer:
    """Analyzes products using AI to generate descriptions, categorize, and score"""

    def __init__(self):
        self.openai_enabled = bool(settings.OPENAI_API_KEY)
        self.anthropic_enabled = bool(settings.ANTHROPIC_API_KEY)

        if self.openai_enabled:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except ImportError:
                print("OpenAI library not installed")
                self.openai_enabled = False

        if self.anthropic_enabled:
            try:
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            except ImportError:
                print("Anthropic library not installed")
                self.anthropic_enabled = False

    async def analyze_product(self, product) -> Dict[str, Any]:
        """
        Comprehensive product analysis using AI
        """
        analysis = {
            "ai_category": None,
            "ai_keywords": [],
            "ai_description": None,
            "profit_potential_score": 0.0,
            "competition_level": "unknown",
            "suggested_price": None,
            "target_audience": None,
            "selling_points": []
        }

        try:
            # Generate AI analysis
            if self.anthropic_enabled:
                analysis = await self._analyze_with_claude(product)
            elif self.openai_enabled:
                analysis = await self._analyze_with_gpt(product)
            else:
                # Fallback to rule-based analysis
                analysis = self._basic_analysis(product)

        except Exception as e:
            print(f"AI analysis error: {str(e)}")
            analysis = self._basic_analysis(product)

        return analysis

    async def _analyze_with_claude(self, product) -> Dict[str, Any]:
        """Analyze product using Claude AI"""
        try:
            prompt = f"""
Analyze this product for e-commerce listing:

Title: {product.title}
Description: {product.description or 'N/A'}
Category: {product.category or 'Unknown'}
Trend Score: {product.trend_score}
Source: {product.trend_source}

Please provide:
1. Optimized product category
2. 10-15 relevant keywords for SEO
3. Compelling product description (2-3 paragraphs)
4. Profit potential score (0-100)
5. Competition level (low/medium/high)
6. Suggested retail price range
7. Target audience
8. Key selling points (5-7 bullet points)

Return as JSON with keys: category, keywords, description, profit_potential, competition_level, price_range, target_audience, selling_points
"""

            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text

            # Extract JSON from response
            # Try to parse as JSON
            try:
                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0].strip()
                elif "{" in response_text:
                    json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
                else:
                    json_str = response_text

                result = json.loads(json_str)
            except:
                # If JSON parsing fails, create structured response
                result = {
                    "category": product.category or "General",
                    "keywords": ["trending", "popular", "viral"],
                    "description": response_text[:500],
                    "profit_potential": 65.0,
                    "competition_level": "medium",
                    "price_range": "$20-$50",
                    "target_audience": "General consumers",
                    "selling_points": ["High quality", "Trending item", "Great value"]
                }

            return {
                "ai_category": result.get("category"),
                "ai_keywords": result.get("keywords", []),
                "ai_description": result.get("description"),
                "profit_potential_score": float(result.get("profit_potential", 50)),
                "competition_level": result.get("competition_level", "medium"),
                "suggested_price": result.get("price_range"),
                "target_audience": result.get("target_audience"),
                "selling_points": result.get("selling_points", [])
            }

        except Exception as e:
            print(f"Claude analysis error: {str(e)}")
            return self._basic_analysis(product)

    async def _analyze_with_gpt(self, product) -> Dict[str, Any]:
        """Analyze product using GPT-4"""
        try:
            prompt = f"""
Analyze this product for e-commerce listing:

Title: {product.title}
Description: {product.description or 'N/A'}
Category: {product.category or 'Unknown'}
Trend Score: {product.trend_score}

Provide JSON response with:
{{
  "category": "optimized category",
  "keywords": ["keyword1", "keyword2", ...],
  "description": "compelling 2-3 paragraph description",
  "profit_potential": 0-100 score,
  "competition_level": "low|medium|high",
  "price_range": "$X-$Y",
  "target_audience": "description",
  "selling_points": ["point1", "point2", ...]
}}
"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert e-commerce product analyst."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            return {
                "ai_category": result.get("category"),
                "ai_keywords": result.get("keywords", []),
                "ai_description": result.get("description"),
                "profit_potential_score": float(result.get("profit_potential", 50)),
                "competition_level": result.get("competition_level", "medium"),
                "suggested_price": result.get("price_range"),
                "target_audience": result.get("target_audience"),
                "selling_points": result.get("selling_points", [])
            }

        except Exception as e:
            print(f"GPT analysis error: {str(e)}")
            return self._basic_analysis(product)

    def _basic_analysis(self, product) -> Dict[str, Any]:
        """Fallback rule-based analysis when AI is not available"""
        # Extract keywords from title
        keywords = [word.lower() for word in product.title.split() if len(word) > 3]

        # Basic profit calculation
        profit_score = min(100, product.trend_score or 50)

        # Competition based on trend score
        if product.trend_score and product.trend_score > 80:
            competition = "high"
        elif product.trend_score and product.trend_score > 50:
            competition = "medium"
        else:
            competition = "low"

        return {
            "ai_category": product.category or "General",
            "ai_keywords": keywords[:10],
            "ai_description": product.description or product.title,
            "profit_potential_score": profit_score,
            "competition_level": competition,
            "suggested_price": None,
            "target_audience": "General consumers",
            "selling_points": ["Trending product", "High quality", "Fast shipping"]
        }

    def generate_platform_specific_description(
        self,
        product,
        platform: str
    ) -> str:
        """Generate platform-optimized descriptions"""
        descriptions = {
            "amazon": self._amazon_description(product),
            "ebay": self._ebay_description(product),
            "tiktok_shop": self._tiktok_description(product),
            "facebook_marketplace": self._facebook_description(product)
        }

        return descriptions.get(platform, product.ai_description or product.description)

    def _amazon_description(self, product) -> str:
        """Amazon-optimized description with bullet points"""
        description = f"{product.ai_description}\n\n"
        description += "Key Features:\n"
        for point in (product.selling_points or [])[:5]:
            description += f"• {point}\n"
        return description

    def _ebay_description(self, product) -> str:
        """eBay-optimized HTML description"""
        # eBay allows HTML formatting
        return product.ai_description or product.description

    def _tiktok_description(self, product) -> str:
        """TikTok Shop - short, engaging description"""
        # Keep it short and punchy
        desc = product.ai_description or product.description
        return desc[:200] + "..." if len(desc) > 200 else desc

    def _facebook_description(self, product) -> str:
        """Facebook Marketplace - casual, friendly tone"""
        return product.ai_description or product.description
