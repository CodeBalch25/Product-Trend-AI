"""
AI-powered product analysis service
Now using Multi-Agent AI System for enhanced analysis
"""
from typing import Dict, Any, Optional
from datetime import datetime
import json

from config.settings import settings
from services.ml.approval_predictor import ml_predictor
from models.database import ProductStatus


class ProductAnalyzer:
    """Analyzes products using AI - now with Multi-Agent System"""

    def __init__(self):
        # Check if agentic system is available (priority)
        self.agentic_enabled = bool(settings.GROQ_API_KEY and settings.HUGGINGFACE_API_KEY)

        self.groq_enabled = bool(settings.GROQ_API_KEY)
        self.huggingface_enabled = bool(settings.HUGGINGFACE_API_KEY)
        self.openai_enabled = bool(settings.OPENAI_API_KEY)
        self.anthropic_enabled = bool(settings.ANTHROPIC_API_KEY)

        # Initialize Multi-Agent System (TOP PRIORITY)
        if self.agentic_enabled:
            try:
                from services.ai_analysis.agentic_system import AgenticAISystem
                self.agentic_system = AgenticAISystem(
                    groq_api_key=settings.GROQ_API_KEY,
                    huggingface_api_key=settings.HUGGINGFACE_API_KEY
                )
                print("="*60)
                print("🤖 MULTI-AGENT AI SYSTEM ACTIVATED 🤖")
                print("  ✓ Coordinator: Qwen (via Groq)")
                print("  ✓ Scanner Agent: Mixtral-8x7B (Hugging Face)")
                print("  ✓ Trend Agent: Mistral-7B (Hugging Face)")
                print("  ✓ Research Agent: Llama-3-8B (Hugging Face)")
                print("="*60)
            except Exception as e:
                print(f"Failed to initialize agentic system: {str(e)}")
                self.agentic_enabled = False

        # Groq setup (FREE & FAST - Fallback)
        if self.groq_enabled and not self.agentic_enabled:
            try:
                from openai import OpenAI
                self.groq_client = OpenAI(
                    api_key=settings.GROQ_API_KEY,
                    base_url="https://api.groq.com/openai/v1"
                )
                print("Groq API enabled (FREE & FAST)")
            except ImportError:
                print("OpenAI library not installed for Groq")
                self.groq_enabled = False

        # Hugging Face setup (FREE - Alternative)
        if self.huggingface_enabled and not self.agentic_enabled:
            self.hf_api_key = settings.HUGGINGFACE_API_KEY
            self.hf_api_url = "https://api-inference.huggingface.co/models/"
            self.hf_model = "mistralai/Mistral-7B-Instruct-v0.1"  # Free model
            print("Hugging Face API enabled (FREE)")

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

    async def analyze_product(self, product, db=None) -> Dict[str, Any]:
        """
        Comprehensive product analysis using AI with ML-enhanced predictions
        Priority: Multi-Agent System > Individual AI Services > Rule-based
        """
        analysis = {
            "ai_category": None,
            "ai_keywords": [],
            "ai_description": None,
            "profit_potential_score": 0.0,
            "competition_level": "unknown",
            "suggested_price": None,
            "target_audience": None,
            "selling_points": [],
            "recommendation": "review"  # Default recommendation
        }

        try:
            # STEP 1: Multi-Agent AI Analysis
            if self.agentic_enabled:
                print("\n🚀 Using Multi-Agent AI System for analysis...")
                analysis = await self.agentic_system.analyze_product_multi_agent(product)
                print("✓ Multi-Agent analysis complete\n")

            # FALLBACK: Single AI services
            elif self.groq_enabled:
                print("Using Groq (single agent)...")
                analysis = await self._analyze_with_groq(product)
            elif self.huggingface_enabled:
                print("Using Hugging Face (single agent)...")
                analysis = await self._analyze_with_huggingface(product)
            elif self.anthropic_enabled:
                print("Using Claude (single agent)...")
                analysis = await self._analyze_with_claude(product)
            elif self.openai_enabled:
                print("Using GPT-4 (single agent)...")
                analysis = await self._analyze_with_gpt(product)
            else:
                print("Using rule-based analysis (no AI available)...")
                analysis = self._basic_analysis(product)

            # STEP 2: ML Approval Prediction (if model trained)
            if ml_predictor.trained:
                product_features = {
                    "trend_score": product.trend_score or 0,
                    "category": analysis.get("ai_category") or product.category or "unknown",
                    "source": product.trend_source or "unknown",
                    "price": product.estimated_cost or 0,
                    "keywords": analysis.get("ai_keywords", [])
                }

                ml_prediction = ml_predictor.predict(product_features)

                print(f"\n🤖 ML PREDICTION:")
                print(f"   Approval Probability: {ml_prediction['approval_probability']:.1%}")
                print(f"   Prediction: {ml_prediction['prediction'].upper()}")
                print(f"   Confidence: {ml_prediction['confidence']:.1%}")
                print(f"   Reasoning: {ml_prediction['reasoning']}")

                # STEP 3: Combine AI + ML for final decision
                ai_recommendation = analysis.get('recommendation', 'review')

                # Auto-reject logic: ML is very confident about rejection
                if ml_prediction['approval_probability'] < 0.2 and ml_prediction['confidence'] > 0.7:
                    print(f"   ⚠️ ML predicts high rejection probability - flagging for review")
                    if db and product:
                        product.status = ProductStatus.PENDING_REVIEW
                        product.ml_warning = True

                # Auto-approval logic: ML + AI both highly confident
                elif (ml_prediction['approval_probability'] > 0.85 and
                      ml_prediction['confidence'] > 0.8 and
                      ai_recommendation == 'approve'):
                    print(f"   ✅ ML + AI both highly confident - AUTO-APPROVING")
                    if db and product:
                        product.status = ProductStatus.APPROVED
                        product.auto_approved = True

                # Store ML prediction for audit
                analysis['ml_prediction'] = ml_prediction

        except Exception as e:
            print(f"AI analysis error: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            analysis = self._basic_analysis(product)

        return analysis

    async def _analyze_with_groq(self, product) -> Dict[str, Any]:
        """Analyze product using Groq (FREE & FAST)"""
        try:
            prompt = f"""Analyze this product for e-commerce listing:

Title: {product.title}
Description: {product.description or 'N/A'}
Category: {product.category or 'Unknown'}
Trend Score: {product.trend_score}

Provide JSON response ONLY with:
{{
  "category": "optimized category",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "description": "compelling 2-3 sentence product description",
  "profit_potential": 75,
  "competition_level": "medium",
  "price_range": "$30-$50",
  "target_audience": "tech enthusiasts",
  "selling_points": ["point1", "point2", "point3"]
}}"""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Fast & accurate (updated model)
                messages=[
                    {"role": "system", "content": "You are an expert e-commerce product analyst. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            result_text = response.choices[0].message.content.strip()

            # Parse JSON response
            try:
                # Extract JSON if embedded in markdown code blocks
                if "```json" in result_text:
                    json_str = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    json_str = result_text.split("```")[1].split("```")[0].strip()
                elif "{" in result_text and "}" in result_text:
                    json_str = result_text[result_text.find("{"):result_text.rfind("}")+1]
                else:
                    json_str = result_text

                result = json.loads(json_str)
            except:
                # Fallback if JSON parsing fails
                return self._basic_analysis(product)

            return {
                "ai_category": result.get("category"),
                "ai_keywords": result.get("keywords", [])[:10],
                "ai_description": result.get("description"),
                "profit_potential_score": float(result.get("profit_potential", 50)),
                "competition_level": result.get("competition_level", "medium"),
                "suggested_price": result.get("price_range"),
                "target_audience": result.get("target_audience"),
                "selling_points": result.get("selling_points", [])
            }

        except Exception as e:
            print(f"Groq analysis error: {str(e)}")
            return self._basic_analysis(product)

    async def _analyze_with_huggingface(self, product) -> Dict[str, Any]:
        """Analyze product using Hugging Face (FREE)"""
        import requests

        try:
            prompt = f"""Analyze this product for e-commerce:
Title: {product.title}
Description: {product.description or 'N/A'}
Category: {product.category or 'Unknown'}

Provide JSON with: category, keywords (array), description, profit_potential (0-100), competition_level (low/medium/high), price_range, target_audience, selling_points (array)"""

            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }

            response = requests.post(
                f"{self.hf_api_url}{self.hf_model}",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result_text = response.json()[0]["generated_text"]

                # Try to parse JSON from response
                try:
                    # Extract JSON if embedded in text
                    if "{" in result_text and "}" in result_text:
                        json_str = result_text[result_text.find("{"):result_text.rfind("}")+1]
                        result = json.loads(json_str)
                    else:
                        # Fallback: create structured response from text
                        result = {
                            "category": product.category or "General",
                            "keywords": [w for w in product.title.lower().split() if len(w) > 3][:10],
                            "description": result_text[:500],
                            "profit_potential": 65,
                            "competition_level": "medium",
                            "price_range": "$20-$50",
                            "target_audience": "General consumers",
                            "selling_points": ["Quality product", "Trending item", "Great value"]
                        }
                except:
                    result = self._basic_analysis(product)
                    return result

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
            else:
                print(f"Hugging Face API error: {response.status_code}")
                return self._basic_analysis(product)

        except Exception as e:
            print(f"Hugging Face analysis error: {str(e)}")
            return self._basic_analysis(product)

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
