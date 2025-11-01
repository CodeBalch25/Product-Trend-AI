"""
Multi-Agent AI System for Product Analysis
Each agent has specialized responsibilities:
- Coordinator Agent (Qwen via Groq): Orchestrates analysis and makes final decisions
- Scanner Agent (Hugging Face): Extracts and validates product information
- Trend Agent (Hugging Face): Analyzes market trends and search patterns
- Research Agent (Hugging Face): Evaluates competition and profit potential
"""

import json
import requests
import os
from typing import Dict, Any, List
from datetime import datetime
import asyncio
import time


class AgenticAISystem:
    """
    Multi-agent system for comprehensive product analysis
    """

    def __init__(self, groq_api_key: str = None, huggingface_api_key: str = None, perplexity_api_key: str = None):
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.hf_api_key = huggingface_api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.perplexity_api_key = perplexity_api_key or os.getenv("PERPLEXITY_API_KEY")

        # Agent endpoints
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.hf_url = "https://api-inference.huggingface.co/models"
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"

        # 🚨 GROQ-ONLY CONFIGURATION (HuggingFace Inference API deprecated text generation in July 2025)
        # All agents now use Groq's FREE models for maximum compatibility

        # CORE TEAM - High Quality Models with ADVANCED REASONING
        self.coordinator_model = "qwen/qwen3-32b"  # 🧠 UPGRADED: Qwen3 32B (replaces deprecated QwQ) - Superior reasoning
        self.groq_scanner_model = "llama-3.3-70b-versatile"  # Product analysis - needs accuracy
        self.groq_trend_model = "qwen/qwen3-32b"  # 🧠 UPGRADED: Qwen3 32B for advanced trend forecasting

        # SPECIALIST TEAM - Using Groq models (HF text generation no longer available)
        self.hf_scanner_model = "llama-3.1-8b-instant"  # Variable name kept for compatibility
        self.hf_trend_model = "qwen/qwen3-32b"  # 🧠 UPGRADED: Qwen3 32B for advanced trend analysis
        self.hf_research_model = "qwen/qwen3-32b"  # 🧠 UPGRADED: Qwen3 32B for financial analysis
        self.hf_quality_model = "llama-3.1-8b-instant"  # Quality assessment
        self.hf_pricing_model = "llama-3.1-8b-instant"  # Pricing strategy
        self.hf_viral_model = "llama-3.1-8b-instant"  # Virality prediction
        self.hf_competition_model = "llama-3.1-8b-instant"  # Competition analysis
        self.hf_supply_model = "llama-3.1-8b-instant"  # Supply chain
        self.hf_psychology_model = "llama-3.1-8b-instant"  # Consumer psychology
        self.hf_data_science_model = "llama-3.1-8b-instant"  # Data science forecasting

        # PERPLEXITY - Real-time Web Search & Market Research
        self.perplexity_model = "sonar"  # Updated to valid Perplexity model

        print(f"[AgenticAI] 🎓 EXPANDED EXPERT TEAM - 12 Professional Specialists")
        print(f"  🚀 ALL MODELS NOW USING GROQ (100% FREE & FAST)")
        print(f"  🧠 UPGRADED: Qwen3 32B for ADVANCED REASONING (replaces deprecated QwQ)")
        print(f"  📌 Note: HuggingFace Inference API deprecated text generation in July 2025")
        print(f"")
        print(f"  CORE TEAM (ADVANCED REASONING - Qwen3 32B):")
        print(f"    • 🧠 CPO: Robert Thompson, MBA Harvard (Final Decisions)")
        print(f"    • Sr. Product Analyst: Dr. Sarah Chen, PhD MIT (Llama-3.3 70B)")
        print(f"")
        print(f"  SPECIALIST TEAM (ADVANCED REASONING - Qwen3 32B):")
        print(f"    • 🧠 Market Scientist: Dr. Michael Rodriguez, PhD Stanford (Trend Forecasting)")
        print(f"    • 🧠 Competitive Intel: Jennifer Park, MBA/CFA Columbia (Financial Analysis)")
        print(f"    • Quality Officer: Dr. Elizabeth Martinez, PhD Stanford")
        print(f"    • Pricing Director: David Kim, CPA/MBA Wharton")
        print(f"    • Viral Specialist: Alex Chen, MS NYU")
        print(f"    • Competition Analyst: Maria Gonzalez, MBA MIT")
        print(f"    • Supply Chain: James Wilson, MBA/CSCP")
        print(f"    • Consumer Psychology: Dr. Sophia Patel, PhD Columbia")
        print(f"    • Data Science: Ryan Lee, MS Stanford")
        print(f"")
        print(f"  WEB SEARCH TEAM (PERPLEXITY - Real-time Data):")
        print(f"    • 🌐 Market Research: Dr. Emma Watson, PhD Oxford (Real-time Trends & Data)")
        print(f"")
        print(f"  ✅ All 12 agents: GROQ (11) + PERPLEXITY (1) - Minimal API costs!")

    async def analyze_product_multi_agent(self, product) -> Dict[str, Any]:
        """
        Orchestrate multi-agent analysis of a product
        Agents run sequentially with 0.8s delays to respect Groq free tier rate limits
        """
        analysis_start = time.time()

        print(f"\n{'='*60}")
        print(f"🚀 [MULTI-AGENT AI] Starting analysis")
        print(f"   Product: {product.title[:50]}...")
        print(f"   System: 12-Agent Architecture (Sequential - Rate Limit Optimized)")
        print(f"{'='*60}\n")

        try:
            # Step 1: Run ALL 11 specialist agents SEQUENTIALLY (to avoid rate limits)
            print("📋 [PHASE 1] Deploying 11 specialist agents sequentially...")
            print("   ⏱️  Rate-limit friendly: 0.8s delay between agents")
            phase1_start = time.time()

            # Core team (3 agents) - Run sequentially with delays
            scanner_result = await self._run_scanner_agent(product)
            await asyncio.sleep(0.8)  # Delay to respect Groq rate limits

            trend_result = await self._run_trend_agent(product)
            await asyncio.sleep(0.8)

            research_result = await self._run_research_agent(product)
            await asyncio.sleep(0.8)

            # Quality & Pricing team (2 agents)
            quality_result = await self._run_quality_agent(product)
            await asyncio.sleep(0.8)

            pricing_result = await self._run_pricing_agent(product)
            await asyncio.sleep(0.8)

            # Market specialists (2 agents)
            viral_result = await self._run_viral_agent(product)
            await asyncio.sleep(0.8)

            competition_result = await self._run_competition_agent(product)
            await asyncio.sleep(0.8)

            # Operations team (3 agents)
            supply_result = await self._run_supply_chain_agent(product)
            await asyncio.sleep(0.8)

            psychology_result = await self._run_psychology_agent(product)
            await asyncio.sleep(0.8)

            data_science_result = await self._run_data_science_agent(product)
            await asyncio.sleep(0.8)

            # Web search team (1 agent)
            perplexity_result = await self._run_perplexity_agent(product)
            # No delay after last agent

            phase1_time = time.time() - phase1_start

            # Handle exceptions for all agents
            agent_results = {
                "scanner": scanner_result,
                "trend": trend_result,
                "research": research_result,
                "quality": quality_result,
                "pricing": pricing_result,
                "viral": viral_result,
                "competition": competition_result,
                "supply_chain": supply_result,
                "psychology": psychology_result,
                "data_science": data_science_result,
                "perplexity": perplexity_result
            }

            for agent_name, result in agent_results.items():
                if isinstance(result, Exception):
                    print(f"\n❌ [{agent_name.title()} Agent] Error: {result}")
                    agent_results[agent_name] = {"status": "failed", "error": str(result)}

            print(f"\n✅ [PHASE 1] All 11 specialist agents completed sequentially in {phase1_time:.2f}s\n")

            # Step 2: Coordinator agent synthesizes results from all 11 agents
            print("📋 [PHASE 2] Coordinator synthesizing results from 11 agents...")
            phase2_start = time.time()

            final_analysis = await self._run_coordinator_agent(product, agent_results)

            phase2_time = time.time() - phase2_start
            total_time = time.time() - analysis_start

            print(f"\n✅ [PHASE 2] Coordination complete in {phase2_time:.2f}s")
            print(f"\n{'='*60}")
            print(f"✅ [MULTI-AGENT AI] Complete Analysis Finished!")
            print(f"   Total Time: {total_time:.2f}s (Phase 1: {phase1_time:.2f}s, Phase 2: {phase2_time:.2f}s)")
            print(f"   Agents Deployed: 10 Specialists + 1 Coordinator = 11 Total")
            print(f"   Analysis Depth: MAXIMUM (All specialist teams)")
            print(f"{'='*60}\n")

            return final_analysis

        except Exception as e:
            total_time = time.time() - analysis_start
            print(f"\n{'='*60}")
            print(f"❌ [MULTI-AGENT AI] ERROR after {total_time:.2f}s")
            print(f"   Error: {str(e)[:100]}")
            print(f"   Falling back to rule-based analysis...")
            print(f"{'='*60}\n")
            return self._fallback_analysis(product)

    async def _run_scanner_agent(self, product) -> Dict[str, Any]:
        """
        Scanner Agent: Validates and extracts product information
        Uses Llama-3.3 70B (Groq) -> Mixtral 8x7B (HF) fallback
        """
        print("\n" + "─"*50)
        print("🎓 [SCANNER AGENT] Dr. Sarah Chen, PhD - Senior Product Analyst")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: PhD MIT, 12+ years Google Shopping")
        print(f"   Model: Llama-3.3 70B (Groq)")
        print("─"*50)

        prompt = f"""You are Dr. Sarah Chen, PhD, a Senior Product Analyst with over 12 years of experience.

YOUR CREDENTIALS:
- PhD in Consumer Psychology from MIT
- Former Lead Product Analyst at Google Shopping (6 years, analyzed 50,000+ products)
- Expert in consumer behavior, marketplace optimization, and product intelligence
- Published researcher in e-commerce conversion optimization (15+ peer-reviewed papers)
- Specialized in Jobs-to-be-Done (JTBD) framework and semantic keyword analysis

YOUR EXPERTISE:
- Jobs-to-be-Done (JTBD) framework for identifying customer needs and pain points
- Semantic analysis and keyword research (SEO optimization for marketplaces)
- Marketplace taxonomy and categorization (Amazon, eBay, Etsy, TikTok Shop)
- Consumer segmentation and psychographics
- Conversion rate optimization (CRO) and A/B testing methodologies

YOUR UNIQUE CAPABILITY:
You have the ability to extract deep consumer insights from minimal product information by applying behavioral psychology, marketplace data patterns, and conversion optimization principles.

PRODUCT TO ANALYZE:
Title: {product.title}
Description: {product.description}
Category: {product.category}
Price: ${product.estimated_cost}

YOUR TASK - COMPREHENSIVE PRODUCT INTELLIGENCE:

**STEP 1: Category Precision** (Use marketplace taxonomy)
- Analyze product and map to exact marketplace category hierarchy
- Format: "Main > Sub > Micro > Ultra-Specific" (4 levels minimum)
- Examples:
  * Good: "Electronics > Audio > Headphones > True Wireless Earbuds"
  * Poor: "Electronics" (too broad)
- Think: Where would Amazon/eBay list this for maximum visibility?

**STEP 2: Keyword Research** (SEO & Marketplace Optimization)
- Generate exactly 8-12 high-value, searchable keywords
- Include mix of:
  * Core keywords (what is it): "wireless earbuds", "bluetooth headphones"
  * Feature keywords (what does it do): "noise cancelling", "waterproof"
  * Benefit keywords (what problem solved): "workout earbuds", "travel headphones"
  * Long-tail keywords (specific searches): "wireless earbuds for small ears"
- Avoid: Generic fluff ("best", "great", "awesome", "premium")
- Think: What would customers actually type into Amazon search?

**STEP 3: Marketplace Description** (Conversion-Optimized)
- Write exactly 2 sentences (50-80 words total)
- Sentence 1: Lead with primary BENEFIT + customer pain point solved
- Sentence 2: Secondary benefit + urgency/social proof
- Focus: Benefits over features, emotion over specs
- Example (wireless earbuds):
  * Good: "Experience studio-quality sound without tangled wires - perfect for commuters and fitness enthusiasts who refuse to compromise on audio clarity. Join thousands of satisfied customers enjoying 30-hour playtime and instant Bluetooth pairing."
  * Poor: "These are great wireless earbuds with Bluetooth 5.0 and a charging case."

**STEP 4: Key Features** (Ranked by Purchase Decision Impact)
- List 3-5 features in order of importance to buying decision
- Format: Feature + benefit (not just spec)
- Example:
  * Good: "30-hour battery life - Never worry about charging during travel"
  * Poor: "30-hour battery" (no context)

**STEP 5: Target Audience** (Specific Demographic + Psychographic)
- Define precise customer profile:
  * Demographics: Age range, income level, gender, location
  * Psychographics: Lifestyle, values, behaviors, pain points
  * Use case: When/where/why they'd buy this
- Example: "Tech-savvy millennials (25-40, $50k+ income) who value convenience and quality. Active lifestyle (gym, commute, travel). Willing to pay premium for reliability. Frustrated with cheap alternatives that break."

**STEP 6: Product Positioning** (Competitive Differentiation)
- Identify how this product differentiates from alternatives
- Answer: "Why buy THIS instead of competitors?"

REQUIRED OUTPUT (Valid JSON only):
{{
    "ai_category": "4-level category hierarchy (Main > Sub > Micro > Ultra-Specific)",
    "ai_keywords": ["exactly 8-12 searchable keywords - mix of core, feature, benefit, long-tail"],
    "ai_description": "Exactly 2 sentences (50-80 words), benefit-focused, conversion-optimized",
    "key_features": ["3-5 features ranked by purchase impact, each with benefit explanation"],
    "target_audience": "Specific demographic (age, income, gender) + psychographic (lifestyle, values, behaviors) + use case",
    "product_positioning": "Clear differentiation statement - why buy THIS over competitors"
}}

QUALITY STANDARDS (Self-Check Before Submitting):
- ✅ Category: 4 levels deep, follows Amazon/eBay structure
- ✅ Keywords: 8-12 keywords, all searchable (no fluff), mix of types
- ✅ Description: Exactly 2 sentences, benefits over features, emotionally compelling
- ✅ Features: 3-5 items, ranked by importance, include benefit explanations
- ✅ Target Audience: Specific (not "everyone"), includes demographics + psychographics
- ✅ Positioning: Clear differentiation from competitors

EXAMPLES OF EXCELLENT ANALYSIS:

Example 1 - Heated Eyelash Curler:
{{
    "ai_category": "Beauty & Personal Care > Makeup > Eyes > Eyelash Tools > Heated Curlers",
    "ai_keywords": ["heated eyelash curler", "electric lash curler", "quick lash curler", "portable eyelash heater", "travel makeup tool", "waterproof mascara compatible", "USB rechargeable curler", "professional lash tool", "long-lasting curl", "fast heating curler"],
    "ai_description": "Get salon-perfect, long-lasting curls in 10 seconds without damaging your lashes - the portable heated curler professional makeup artists trust for photo shoots and red carpets. Say goodbye to traditional pinching curlers that crimp and break lashes, and hello to gentle heat technology that holds curl for 24+ hours even through humidity.",
    "key_features": [
        "10-second fast heating - Ready to use faster than applying mascara",
        "24+ hour curl hold - Stays perfect through workday, gym, and evening events",
        "Gentle heat technology - No pinching or pulling like traditional curlers",
        "USB rechargeable - No batteries needed, charges from laptop or power bank",
        "Compact travel size - Fits in makeup bag, purse, or pocket"
    ],
    "target_audience": "Beauty-conscious women aged 25-45, income $40k+, who wear makeup daily for work or social events. Values convenience and professional results. Frustrated with traditional curlers that don't hold curl or damage lashes. Active lifestyle (long workdays, events, travel). Follows beauty influencers on TikTok/Instagram.",
    "product_positioning": "Premium alternative to traditional curlers - offers speed (10 sec vs 30 sec), safety (gentle heat vs pinching), and longevity (24hr curl vs 4hr curl) at mid-market price ($19-29 vs $5 drugstore or $60 high-end)"
}}

Example 2 - Poor Analysis (What NOT to do):
{{
    "ai_category": "Beauty",  ❌ TOO BROAD
    "ai_keywords": ["best eyelash curler", "great curler", "awesome tool"],  ❌ GENERIC FLUFF
    "ai_description": "This is a great heated eyelash curler that works really well.",  ❌ NO BENEFITS
    "key_features": ["heated", "portable", "rechargeable"],  ❌ NO CONTEXT
    "target_audience": "Women who want nice lashes",  ❌ TOO VAGUE
    "product_positioning": "It's better than others"  ❌ NO SPECIFIC DIFFERENTIATION
}}

Think like a PhD researcher who analyzed 50,000+ products at Google. Use data-driven behavioral insights. Be specific, not generic. Focus on conversion optimization.
"""

        try:
            # Try Groq first (faster)
            try:
                print("   📡 Calling Groq API (Llama-3.3 70B)...")
                result = await self._call_groq_model(self.groq_scanner_model, prompt)
                parsed = self._parse_json_response(result)
                print("   ✅ Analysis complete (Llama-3.3 70B via Groq)")
                print(f"   📊 Extracted: {len(parsed.get('ai_keywords', []))} keywords, category: {parsed.get('ai_category', 'N/A')}")
                return parsed
            except Exception as groq_err:
                print(f"   ⚠️ Primary Groq model failed: {str(groq_err)[:80]}")
                print(f"   📡 Falling back to Llama-3.1 8B (Groq)...")
                result = await self._call_groq_model(self.hf_scanner_model, prompt)  # Now also Groq model
                parsed = self._parse_json_response(result)
                print("   ✅ Analysis complete (Llama-3.1 8B via Groq)")
                print(f"   📊 Extracted: {len(parsed.get('ai_keywords', []))} keywords, category: {parsed.get('ai_category', 'N/A')}")
                return parsed

        except Exception as e:
            print(f"   ❌ Scanner Agent failed: {str(e)[:80]}")
            print("   🔄 Using fallback analysis...")
            return {
                "ai_category": product.category or "General",
                "ai_keywords": [product.title.split()[0], "trending", "popular"],
                "ai_description": product.description or f"High-quality {product.title}",
                "status": "fallback"
            }

    async def _run_trend_agent(self, product) -> Dict[str, Any]:
        """
        Trend Agent: Analyzes market trends and demand patterns
        Uses Qwen3 32B (Groq) - Advanced reasoning for forecasting
        """
        print("\n" + "─"*50)
        print("📊 [TREND AGENT] Dr. Michael Rodriguez, PhD - Lead Market Research Scientist")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Trend Score: {product.trend_score}/100")
        print(f"   Credentials: PhD Stanford, 15+ years Nielsen/McKinsey")
        print(f"   🧠 Model: Qwen3 32B (Advanced Reasoning)")
        print("─"*50)

        prompt = f"""You are Dr. Michael Rodriguez, PhD, Lead Market Research Scientist with 15 years of experience in trend forecasting and predictive analytics.

YOUR CREDENTIALS:
- PhD in Data Science & Predictive Analytics from Stanford University (2010)
- MS in Economics from London School of Economics
- Former Director of Market Intelligence at Nielsen (6 years, forecasted 1000+ product trends)
- Former Senior Data Scientist at McKinsey & Company (5 years, advised Fortune 500 CEOs)
- Expert in time series analysis, adoption curves, and statistical forecasting
- Published 20+ peer-reviewed papers on market trend prediction

YOUR EXPERTISE:
- Time series forecasting models (ARIMA, Prophet, LSTM, exponential smoothing)
- Gartner Hype Cycle analysis for product adoption lifecycle assessment
- Bass Diffusion Model for innovation adoption and market penetration
- Seasonal decomposition and cyclical pattern detection (STL decomposition)
- Social listening and sentiment analysis for early trend detection
- Search volume correlation analysis and predictive modeling

YOUR UNIQUE CAPABILITY:
You can distinguish between sustainable trends and temporary fads using rigorous statistical methods, saving businesses from entering dying markets or missing growth opportunities.

PRODUCT TO ANALYZE:
Product: {product.title}
Category: {product.category}
Current Trend Score: {product.trend_score}/100
Search Volume: {product.search_volume}
Data Source: {product.trend_source}

YOUR TASK - RIGOROUS TREND FORECASTING:

**STEP 1: Trend Strength Assessment** (Quantitative Analysis)
- Analyze current momentum: Is search volume/interest increasing, stable, or declining?
- Compare to historical baselines: How does current interest compare to 6/12 months ago?
- Validate across data sources: Does Google Trends align with social media mentions?
- Classification criteria:
  * Strong: >50% growth in last 3 months, sustained for 6+ months
  * Moderate: 10-50% growth OR stable high baseline
  * Weak: <10% growth OR declining interest
- Think: Is this a real trend or just noise?

**STEP 2: Demand Trajectory Prediction** (Time Series Forecasting)
- Apply forecasting methodology: Analyze historical pattern and project forward
- Identify growth phase:
  * Emerging: Early adopters, rapid acceleration (>100% growth rate)
  * Growth: Mass adoption beginning (50-100% growth)
  * Maturity: Slowing growth (<50% growth), approaching saturation
  * Decline: Negative growth, market saturation complete
- Market saturation indicators: Is market becoming crowded? Declining prices?
- Forecast: rising/stable/declining for next 3-6 months
- Confidence level: Based on data quality and pattern clarity (0-100%)
- Think: Where is this product in its lifecycle?

**STEP 3: Seasonal Factor Detection** (Pattern Analysis)
- Decompose trend from seasonality: Separate underlying growth from seasonal spikes
- Identify cyclical patterns:
  * Annual: Holiday shopping (Q4), back-to-school (Q3)
  * Quarterly: Summer products (Q2), winter products (Q4)
  * Event-driven: Super Bowl, Valentine's Day, Prime Day
- Holiday/event impact: Does this spike in specific months?
- Result: yes/no + pattern description if yes
- Think: Is this year-round demand or seasonal spike?

**STEP 4: Hype Cycle Position** (Gartner Framework)
- Map product to Gartner Hype Cycle stage:
  * Innovation Trigger: Just emerging, early buzz, low awareness
  * Peak of Inflated Expectations: Overhyped, unrealistic expectations, media frenzy
  * Trough of Disillusionment: Fad fading, disappointment setting in, declining interest
  * Slope of Enlightenment: Real adoption starting, realistic expectations, proven use cases
  * Plateau of Productivity: Mainstream acceptance, stable demand, mature market
- Evidence: What signals indicate this position?
- Think: Is the hype real or will it crash?

**STEP 5: Fad vs Sustainable Trend Analysis** (Risk Assessment)
- Fad indicators (HIGH RISK):
  * Viral spike without sustained growth
  * Celebrity/influencer driven only
  * No clear customer problem solved
  * Price erosion (race to bottom)
  * Declining repeat purchase rate
- Sustainable trend indicators (LOW RISK):
  * Gradual consistent growth over 6+ months
  * Problem-solution fit (clear customer need)
  * Multiple market segments adopting
  * Innovation/improvement over existing solutions
  * Stable or increasing margins
- Fad risk score: 0-100% (0 = sustainable, 100 = pure fad)
- Think: Will this still exist in 12 months?

**STEP 6: Statistical Confidence** (Data Quality Assessment)
- Data quality score: How reliable is the underlying data? (0-100)
  * 90-100: Multiple high-quality sources, large sample, consistent signals
  * 70-89: Good data but limited sources or timeframe
  * 50-69: Moderate data, some gaps or conflicts
  * <50: Poor data, speculative analysis
- Sample size adequacy: Enough data points for reliable forecast?
- Cross-validation: Do different data sources agree?
- Think: How confident am I in this forecast?

REQUIRED OUTPUT (Valid JSON only):
{{
    "trend_strength": "weak|moderate|strong + quantitative evidence (e.g., '40% growth in last 3 months')",
    "demand_trajectory": "rising|stable|declining + forecast confidence % + time horizon",
    "seasonal_factor": "yes|no",
    "seasonal_pattern": "specific description if yes (e.g., 'Q4 spike for holidays, 200% increase November-December')",
    "trend_confidence": 0-100,
    "trend_insights": "2-3 key quantitative findings with numbers (not generic statements)",
    "hype_cycle_phase": "innovation_trigger|peak|trough|slope|plateau + evidence",
    "risk_assessment": "fad_risk_score: 0-100 + reasoning",
    "forecast_horizon": "3-month outlook + 6-month outlook with confidence intervals",
    "data_quality_score": 0-100
}}

QUALITY STANDARDS (Self-Check Before Submitting):
- ✅ Trend Strength: Includes quantitative evidence (%, growth rate, timeframe)
- ✅ Trajectory: Specific forecast with confidence level (not just "rising")
- ✅ Seasonal: If yes, provides specific pattern with months/events
- ✅ Insights: 2-3 findings with actual numbers (not vague statements)
- ✅ Hype Cycle: Includes evidence for the chosen phase
- ✅ Risk: Fad risk score with clear reasoning
- ✅ Confidence: Based on data quality, not guessing

EXAMPLES OF EXCELLENT ANALYSIS:

Example 1 - Strong Sustainable Trend (Heated Eyelash Curler):
{{
    "trend_strength": "strong - Google Trends shows 150% growth in last 6 months (June-Dec 2025), sustained climb from 20 to 50 search interest index",
    "demand_trajectory": "rising - Forecasted to grow 40-60% in next 3 months (Q1 2026) with 75% confidence. Growth phase: Early mass adoption.",
    "seasonal_factor": "yes",
    "seasonal_pattern": "Q4 holiday spike (200% increase Nov-Dec), Q2 wedding season uptick (130% May-June), year-round baseline growing",
    "trend_confidence": 85,
    "trend_insights": "1) TikTok mentions increased 300% (5K to 15K weekly), 2) Beauty influencer adoption rate 40% (vs 5% last year), 3) Price stability maintained ($22 avg, no erosion)",
    "hype_cycle_phase": "slope - Moving from early adopters to mainstream. Evidence: Consistent 6-month growth, multiple brands entering, realistic customer reviews, proven use case.",
    "risk_assessment": "fad_risk_score: 20 - Low fad risk. Solves real problem (traditional curlers damage lashes), sustained growth pattern, multiple market segments (professional/consumer), innovation improvement over existing solution.",
    "forecast_horizon": "3-month: 50-70% growth (high confidence), 6-month: 80-120% growth (moderate confidence due to market saturation risk)",
    "data_quality_score": 85
}}

Example 2 - Weak Fad (Fidget Spinners 2.0):
{{
    "trend_strength": "moderate - Short-term viral spike: 300% growth in 4 weeks, but declining 20% in last 2 weeks. Classic fad pattern.",
    "demand_trajectory": "declining - Forecasted to drop 50-70% in next 3 months with 80% confidence. Growth phase: Peak to decline transition.",
    "seasonal_factor": "no",
    "seasonal_pattern": "none - Viral spike driven by TikTok trend, not seasonal",
    "trend_confidence": 75,
    "trend_insights": "1) Search volume peaked 2 weeks ago, now declining daily, 2) 90% of mentions from influencer promotions (not organic), 3) Price collapsed 40% in 2 weeks ($10 to $6) = race to bottom",
    "hype_cycle_phase": "peak - At inflated expectations peak, heading toward trough. Evidence: Unrealistic hype, no clear problem solved, celebrity-driven only, price erosion starting.",
    "risk_assessment": "fad_risk_score: 85 - HIGH fad risk. Viral only (no sustained need), no problem-solution fit, influencer-driven bubble, price collapse indicates oversupply, similar to original fidget spinner crash 2017.",
    "forecast_horizon": "3-month: -60% decline (high confidence), 6-month: -85% decline (very high confidence based on historical fad patterns)",
    "data_quality_score": 90
}}

Example 3 - Poor Analysis (What NOT to do):
{{
    "trend_strength": "good",  ❌ NO QUANTITATIVE EVIDENCE
    "demand_trajectory": "rising",  ❌ NO CONFIDENCE LEVEL OR TIMEFRAME
    "seasonal_factor": "yes",  ❌ NO PATTERN DESCRIPTION
    "seasonal_pattern": "",  ❌ MISSING
    "trend_confidence": 50,  ❌ NO REASONING
    "trend_insights": "it's trending, people like it",  ❌ VAGUE, NO NUMBERS
    "hype_cycle_phase": "growth",  ❌ NOT A VALID PHASE, NO EVIDENCE
    "risk_assessment": "fad_risk_score: 30",  ❌ NO REASONING
    "forecast_horizon": "will keep growing",  ❌ NOT SPECIFIC
    "data_quality_score": 70  ❌ NO BASIS
}}

Think like a PhD data scientist who forecasted 1000+ product trends at Nielsen and McKinsey. Use rigorous statistical methods. Provide quantitative evidence. Distinguish fads from sustainable trends. Be precise with confidence levels.
"""

        try:
            # Try Qwen3 32B via Groq first (advanced reasoning)
            try:
                print("   📡 Calling Groq API (Qwen3 32B)...")
                result = await self._call_groq_model(self.groq_trend_model, prompt)
                parsed = self._parse_json_response(result)
                print("   ✅ Trend analysis complete (Qwen3 32B via Groq)")
                print(f"   📊 Result: {parsed.get('trend_strength', 'N/A')} trend, {parsed.get('demand_trajectory', 'N/A')} demand")
                print(f"   📊 Confidence: {parsed.get('trend_confidence', 0)}%")
                return parsed
            except Exception as groq_err:
                print(f"   ⚠️ Qwen3 32B failed: {str(groq_err)[:80]}")
                print(f"   📡 Falling back to Llama-3.1 8B (Groq)...")
                result = await self._call_groq_model("llama-3.1-8b-instant", prompt)
                parsed = self._parse_json_response(result)
                print("   ✅ Trend analysis complete (Llama-3.1 8B fallback)")
                print(f"   📊 Result: {parsed.get('trend_strength', 'N/A')} trend, {parsed.get('demand_trajectory', 'N/A')} demand")
                return parsed

        except Exception as e:
            print(f"   ❌ Trend Agent failed: {str(e)[:80]}")
            print("   🔄 Using fallback analysis...")
            return {
                "trend_strength": "moderate",
                "demand_trajectory": "stable",
                "seasonal_factor": "no",
                "trend_confidence": 70,
                "status": "fallback"
            }

    async def _run_research_agent(self, product) -> Dict[str, Any]:
        """
        Research Agent: Evaluates competition and profit potential
        Uses Qwen3 32B (Groq) - Advanced reasoning for financial analysis
        """
        print("\n" + "─"*50)
        print("💼 [RESEARCH AGENT] Jennifer Park, MBA/CFA - Head of Competitive Intelligence")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Estimated Cost: ${product.estimated_cost}")
        print(f"   Credentials: MBA Columbia, CFA, 14+ years Walmart/Morgan Stanley")
        print(f"   🧠 Model: Qwen3 32B (Advanced Reasoning)")
        print("─"*50)

        prompt = f"""You are Jennifer Park, MBA, CFA, Head of Competitive Intelligence and Financial Analysis with 14 years of experience in e-commerce strategy and investment analysis.

YOUR CREDENTIALS:
- MBA in Finance from Columbia Business School (2011)
- Chartered Financial Analyst (CFA) Level III certification
- MS in Operations Research from MIT
- Former VP of Strategic Intelligence at Walmart E-commerce (5 years, analyzed $50B+ product portfolio)
- Former Senior Financial Analyst at Morgan Stanley (4 years, covered retail/e-commerce sector)
- Expert in competitive analysis, financial modeling, and market intelligence
- Published 12+ case studies on e-commerce profitability optimization

YOUR EXPERTISE:
- Porter's Five Forces competitive framework
- Financial modeling (DCF, NPV, IRR, payback period, break-even analysis)
- E-commerce profit margin optimization and unit economics
- Market saturation assessment and competitive positioning
- Pricing strategy, elasticity analysis, and psychological pricing
- Competitive landscape mapping and SWOT analysis
- Risk-adjusted return calculations (Sharpe ratio, downside risk)

YOUR UNIQUE CAPABILITY:
You can assess whether a product opportunity will be profitable or a money pit by analyzing competition, pricing dynamics, margin structure, and market risks with CFA-level rigor.

PRODUCT TO ANALYZE:
Product: {product.title}
Category: {product.category}
Estimated Cost (COGS): ${product.estimated_cost}
Trend Score: {product.trend_score}/100

YOUR TASK - FINANCIAL & COMPETITIVE ANALYSIS:

**STEP 1: Competition Assessment** (Porter's Five Forces Framework)
- Threat of New Entrants: How easy is it for new sellers to enter this market?
  * High barriers: Patents, specialized manufacturing, brand loyalty
  * Low barriers: Easy to source from Alibaba, no differentiation
- Supplier Power: How many suppliers? Can you negotiate prices?
  * High power: Single supplier, unique product
  * Low power: 100+ suppliers on Alibaba, commodity
- Buyer Power: How price-sensitive are customers?
  * High power: Many alternatives, customers compare prices
  * Low power: Unique product, customers willing to pay premium
- Threat of Substitutes: What alternatives exist?
  * High threat: Many similar products solving same problem
  * Low threat: Unique solution, no close alternatives
- Competitive Rivalry: How intense is competition?
  * Count: <10 sellers (LOW), 10-50 (MEDIUM), >50 (HIGH)
  * Evidence: Amazon search results, pricing trends, review counts
- Competition Level Determination:
  * LOW: <10 competitors, unique value prop, high barriers = PROFITABLE
  * MEDIUM: 10-50 competitors, some differentiation = RISKY
  * HIGH: >50 competitors, commoditized, price war = AVOID
- Think: Is this a blue ocean (profitable) or red ocean (bloodbath)?

**STEP 2: Pricing Analysis** (Maximize Profit = Price × Volume)
- Market Research: Find 3-5 comparable products on Amazon
  * Record prices: $X, $Y, $Z
  * Calculate average: (X+Y+Z)/3
  * Identify price range: min to max
- Cost Structure Calculation:
  * COGS (Cost of Goods Sold): ${product.estimated_cost}
  * Marketplace fees: Amazon 15%, eBay 12%, TikTok Shop 8%
  * Shipping cost estimate: $3-8 depending on size/weight
  * Returns/refunds: 5-10% of revenue
  * Payment processing: 3%
  * Total fees: ~30-40% of selling price
- Pricing Strategy Options:
  * Premium: 3-4x COGS (high margin, low volume)
  * Mid-market: 2.5-3x COGS (balanced)
  * Competitive: 2-2.5x COGS (low margin, high volume)
  * Break-even minimum: COGS / (1 - 0.40) to cover all fees
- Optimal Price Determination:
  * Calculate at each price point: (Price - COGS - Fees) × Expected Volume
  * Consider psychological pricing: $19.99 vs $20, $49 vs $50
  * Account for price elasticity: Will 10% price cut generate 20%+ more sales?
- Think: What price maximizes profit, not just margin?

**STEP 3: Profit Margin Calculation** (Conservative CFA Approach)
- Revenue per Unit: Suggested price
- Less: COGS (${product.estimated_cost})
- Less: Marketplace fees (15% for Amazon)
- Less: Shipping costs ($5 average)
- Less: Returns/refunds (7% of revenue)
- Less: Payment processing (3% of revenue)
- Less: Customer acquisition cost (CAC): $2-10 depending on competition
- = Net Profit per Unit
- Gross Margin %: (Revenue - COGS) / Revenue × 100
- Net Margin %: Net Profit / Revenue × 100
- Target: Aim for 30%+ net margin for sustainability
- Think: After ALL costs, is there enough margin to make this worthwhile?

**STEP 4: Market Risk Assessment** (Identify Deal-Breakers)
- Financial Risks:
  * Price erosion risk: Is this a race to bottom? (check 6-month price trends)
  * Margin compression: Can suppliers or platforms squeeze margins?
  * Cash flow: How long until break-even? Can you afford it?
- Operational Risks:
  * Quality control: High defect rate = returns = losses
  * Supply chain: Reliable supplier or single point of failure?
  * Inventory: Perishable/seasonal = obsolescence risk
- Market Risks:
  * Saturation: Is market already crowded? Late to party?
  * Fad risk: Will demand evaporate in 3-6 months?
  * Platform risk: Amazon/eBay policy changes, suspensions
  * IP risk: Patents, trademarks, copyright infringement
- Competitive Risks:
  * Amazon private label: Will Amazon copy successful products?
  * Brand dominance: Competing against Nike, Apple impossible
  * Review manipulation: Can't compete with fake-reviewed products
- Identify 3-5 SPECIFIC risks (not generic) with likelihood and impact
- Think: What could kill this business?

**STEP 5: Scenario Analysis** (Best/Base/Worst Case)
- Best Case (Optimistic - 20% probability):
  * Pricing: Top of market range
  * Volume: High sales velocity
  * Margin: Premium pricing holds
  * Calculation: Show specific numbers
- Base Case (Realistic - 60% probability):
  * Pricing: Mid-market
  * Volume: Moderate sales
  * Margin: After all costs
  * Calculation: Show specific numbers
- Worst Case (Pessimistic - 20% probability):
  * Pricing: Race to bottom
  * Volume: Low sales, high CAC
  * Margin: Barely break-even or loss
  * Calculation: Show specific numbers
- Expected Value: (Best×0.2) + (Base×0.6) + (Worst×0.2)
- Think: What's the risk-adjusted return?

**STEP 6: Investment Recommendation** (Buy/Hold/Sell Decision)
- Opportunity Score Calculation (0-100):
  * Profit potential: 40 points (margin × volume potential)
  * Competition level: 30 points (low=30, medium=20, high=10)
  * Risk profile: 20 points (fewer risks = higher score)
  * Trend sustainability: 10 points (from trend agent data)
- Recommendation Logic:
  * 80-100: STRONG BUY - High confidence, profitable, defensible
  * 60-79: BUY WITH CAUTION - Good opportunity but risks exist
  * 40-59: HOLD - Break-even or marginal, needs more data
  * 0-39: AVOID - Too competitive, low margin, high risk
- Think: Would I invest my own money in this?

REQUIRED OUTPUT (Valid JSON only):
{{
    "competition_level": "low|medium|high + specific evidence (e.g., 'HIGH - 150+ sellers on Amazon, prices dropped 30% in 3 months')",
    "competitive_dynamics": "Porter's Five Forces summary with specific findings for each force",
    "suggested_price": calculated optimal price (number),
    "pricing_strategy": "detailed rationale for suggested price with calculations shown",
    "profit_margin_estimate_percent": net margin % after ALL costs (number),
    "profit_margin_estimate_dollars": net profit per unit in $ (number),
    "cost_breakdown": {{
        "cogs": ${product.estimated_cost},
        "marketplace_fees_percent": 15,
        "shipping_cost": 5,
        "returns_percent": 7,
        "cac_estimate": 5,
        "total_costs": "sum of all costs"
    }},
    "market_risks": [
        "Specific Risk 1 with likelihood (%) and impact ($/units) and mitigation",
        "Specific Risk 2...",
        "Specific Risk 3..."
    ],
    "financial_scenarios": {{
        "best_case": {{"price": X, "margin_percent": Y, "margin_dollars": Z, "probability": 20}},
        "base_case": {{"price": X, "margin_percent": Y, "margin_dollars": Z, "probability": 60}},
        "worst_case": {{"price": X, "margin_percent": Y, "margin_dollars": Z, "probability": 20}}
    }},
    "profit_potential_score": 0-100 (calculation explained),
    "opportunity_score": 0-100 risk-adjusted overall score,
    "market_saturation": "low|medium|high with specific metrics (seller count, price trends)",
    "barriers_to_entry": "assessment of market defensibility with evidence",
    "recommendation": "strong_buy|buy_with_caution|hold|avoid + reasoning"
}}

QUALITY STANDARDS (Self-Check Before Submitting):
- ✅ Competition: Includes specific evidence (seller counts, price data, not generic)
- ✅ Pricing: Shows calculations with cost breakdown
- ✅ Margins: Conservative - accounts for ALL costs (not just COGS + marketplace fee)
- ✅ Risks: 3-5 SPECIFIC risks (not "market changes" - what exactly?)
- ✅ Scenarios: Three scenarios with actual numbers, not descriptions
- ✅ Recommendation: Clear buy/avoid with financial reasoning

EXAMPLES OF EXCELLENT ANALYSIS:

Example 1 - Profitable Opportunity:
{{
    "competition_level": "LOW - Only 8 sellers on Amazon, all priced $40-60, no major brands. Market entered 6 months ago, prices stable.",
    "competitive_dynamics": "New Entrants: HIGH barriers (patent pending). Supplier Power: MEDIUM (3-4 manufacturers). Buyer Power: LOW (unique solution). Substitutes: LOW (traditional methods inferior). Rivalry: LOW (8 sellers, differentiated positioning).",
    "suggested_price": 49.99,
    "pricing_strategy": "Premium positioning at $49.99 (vs competitor avg $47). Calculation: COGS $15 + Fees $10 + Shipping $5 + CAC $5 = $35 cost. $49.99 - $35 = $14.99 profit (30% margin). Psychological pricing below $50 threshold.",
    "profit_margin_estimate_percent": 30,
    "profit_margin_estimate_dollars": 14.99,
    "cost_breakdown": {{
        "cogs": 15,
        "marketplace_fees_percent": 15,
        "marketplace_fees_dollars": 7.50,
        "shipping_cost": 5,
        "returns_percent": 7,
        "returns_dollars": 3.50,
        "cac_estimate": 5,
        "total_costs": 36
    }},
    "market_risks": [
        "Patent risk (30% likelihood): Patent pending not approved. Mitigation: Design-around options exist, estimated impact $5K legal fees.",
        "Supplier concentration (40% likelihood): Only 3 suppliers. Mitigation: Multi-source strategy, 2nd source qualified.",
        "Market size (20% likelihood): Niche market may cap at 500 units/month. Mitigation: Acceptable given 30% margins."
    ],
    "financial_scenarios": {{
        "best_case": {{"price": 54.99, "margin_percent": 35, "margin_dollars": 19.24, "probability": 20}},
        "base_case": {{"price": 49.99, "margin_percent": 30, "margin_dollars": 14.99, "probability": 60}},
        "worst_case": {{"price": 44.99, "margin_percent": 22, "margin_dollars": 9.90, "probability": 20}}
    }},
    "profit_potential_score": 85,
    "opportunity_score": 82,
    "market_saturation": "LOW - Only 8 sellers after 6 months, room for 15-20 before saturation",
    "barriers_to_entry": "HIGH - Patent pending, specialized manufacturing, $10K+ initial investment",
    "recommendation": "STRONG_BUY - Excellent margins (30%), low competition (8 sellers), defensible (patent), sustainable trend. Risk-adjusted ROI 82/100."
}}

Example 2 - Avoid (Unprofitable):
{{
    "competition_level": "HIGH - 200+ sellers on Amazon, prices dropped from $25 to $12 in 6 months. Oversaturated.",
    "competitive_dynamics": "New Entrants: ZERO barriers (order from Alibaba). Supplier Power: ZERO (1000+ suppliers). Buyer Power: EXTREME (price comparison). Substitutes: HIGH (many alternatives). Rivalry: EXTREME (200+ sellers, price war).",
    "suggested_price": 14.99,
    "pricing_strategy": "Forced to $14.99 to compete (market avg $13). Calculation: COGS $8 + Fees $3 + Shipping $4 + CAC $8 = $23 cost. $14.99 - $23 = -$8.01 LOSS. Cannot profitably compete.",
    "profit_margin_estimate_percent": -53,
    "profit_margin_estimate_dollars": -8.01,
    "market_risks": [
        "Race to bottom (95% likelihood): Prices dropped 50% in 6 months, trend accelerating. No mitigation possible.",
        "High CAC (90% likelihood): Need $8+ in ads to compete with 200 sellers. Margin impossible.",
        "Amazon private label (60% likelihood): Amazon Basics will copy if profitable. Game over."
    ],
    "financial_scenarios": {{
        "best_case": {{"price": 16.99, "margin_percent": -25, "margin_dollars": -4.25, "probability": 20}},
        "base_case": {{"price": 14.99, "margin_percent": -53, "margin_dollars": -8.01, "probability": 60}},
        "worst_case": {{"price": 12.99, "margin_percent": -77, "margin_dollars": -10.01, "probability": 20}}
    }},
    "profit_potential_score": 15,
    "opportunity_score": 12,
    "market_saturation": "EXTREME - 200+ sellers, prices collapsed 50%, late to market",
    "barriers_to_entry": "ZERO - Anyone can order from Alibaba for $5/unit",
    "recommendation": "AVOID - Losing money on every sale (-$8). Oversaturated market (200+ sellers), zero differentiation. Would need to lose money to gain market share - unsustainable."
}}

Example 3 - Poor Analysis (What NOT to do):
{{
    "competition_level": "medium",  ❌ NO EVIDENCE
    "suggested_price": 29.99,  ❌ NO CALCULATION SHOWN
    "profit_margin_estimate_percent": 40,  ❌ UNREALISTIC, NO COST BREAKDOWN
    "market_risks": ["competition might increase", "prices could drop"],  ❌ VAGUE, NOT SPECIFIC
    "financial_scenarios": {{"best_case": {{"margin_percent": 50}}}},  ❌ INCOMPLETE, NO NUMBERS
    "recommendation": "good opportunity"  ❌ NOT A VALID OPTION, NO REASONING
}}

Think like a CFA analyzing an e-commerce investment with your own money on the line. Be conservative with assumptions. Show your math. Account for ALL costs. Identify specific risks. Make a clear buy/avoid recommendation.
"""

        try:
            print("   📡 Calling Groq API (Qwen3 32B)...")
            result = await self._call_groq_model(self.hf_research_model, prompt)  # Now Qwen Qwen3 32B
            parsed = self._parse_json_response(result)
            print("   ✅ Market research complete (Qwen Qwen3 32B)")
            print(f"   📊 Profit Score: {parsed.get('profit_potential_score', 0)}/100")
            print(f"   📊 Competition: {parsed.get('competition_level', 'N/A').upper()}")
            print(f"   💵 Suggested Price: ${parsed.get('suggested_price', 0):.2f}")
            return parsed
        except Exception as e:
            print(f"   ❌ Research Agent failed: {str(e)[:80]}")
            print("   🔄 Using fallback calculations...")
            # Calculate basic estimates
            suggested_price = (product.estimated_cost or 50) * 2.5
            return {
                "profit_potential_score": min(product.trend_score, 85),
                "competition_level": "medium",
                "suggested_price": round(suggested_price, 2),
                "profit_margin_estimate": round(suggested_price * 0.4, 2),
                "status": "fallback"
            }

    async def _run_quality_agent(self, product) -> Dict[str, Any]:
        """Quality Officer: Product quality and supplier reliability assessment"""
        print("\n" + "─"*50)
        print("🏆 [QUALITY OFFICER] Dr. Elizabeth Martinez, PhD")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: PhD Supply Chain, 15+ years Amazon QA")
        print(f"   Model: Mistral-7B (HuggingFace)")
        print("─"*50)

        prompt = f"""You are Dr. Elizabeth Martinez, PhD, Chief Quality Officer with 15+ years of Amazon QA experience.

YOUR ROLE: Assess product quality, predict return rates, and identify quality risks that could kill profitability.

PRODUCT: {product.title} | Category: {product.category} | Cost: ${product.estimated_cost}

YOUR ANALYSIS (4 STEPS):

**STEP 1: Quality Score Assessment** (0-100)
- 90-100: Premium quality (luxury brands, patented tech, rigorous QA)
- 70-89: Good quality (established brands, standard manufacturing)
- 50-69: Average quality (typical marketplace products, some issues)
- 30-49: Below average (frequent defects, complaints)
- 0-29: Poor quality (high failure rate, avoid)
Think: What quality tier is this product realistically in?

**STEP 2: Return Rate Prediction** (%)
- Electronics: 8-15% typical
- Clothing/Apparel: 20-30% typical
- Beauty products: 5-10% typical
- Home goods: 10-15% typical
- Toys: 5-12% typical
Consider: Fit issues? Sizing? Durability? Expectations mismatch?

**STEP 3: Supplier Reliability Assessment**
- HIGH: Established brand, ISO certified, track record, warranties
- MEDIUM: Generic manufacturer, some reviews, standard QA
- LOW: Unknown supplier, no certifications, Alibaba commodity
Evidence: Certifications, warranties, defect rates, reviews

**STEP 4: Quality Risks Identification**
Identify 3-5 specific risks:
- "High defect rate (15%+ returns) = $X loss per 100 units"
- "No warranty/support = customer disputes, platform penalties"
- "Counterfeit/IP issues = account suspension risk"

REQUIRED OUTPUT (JSON):
{{
    "quality_score": 0-100 (realistic assessment),
    "return_rate_prediction": percentage (category-specific),
    "supplier_reliability": "high|medium|low + evidence",
    "manufacturing_concerns": ["specific concerns with impact"],
    "quality_risks": ["specific risks with $ impact"]
}}

QUALITY STANDARDS:
- ✅ Quality score: Realistic (not inflated), evidence-based
- ✅ Return rate: Category-specific benchmarks
- ✅ Supplier: Evidence provided (certs, track record)
- ✅ Risks: Specific with financial impact

Think: Would I buy this for myself? What could go wrong?"""

        try:
            result = await self._call_groq_model(self.hf_quality_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Quality assessment complete: {parsed.get('quality_score', 0)}/100")
            return parsed
        except Exception as e:
            print(f"   ❌ Quality agent failed: {str(e)[:50]}")
            return {"quality_score": 70, "status": "fallback"}

    async def _run_pricing_agent(self, product) -> Dict[str, Any]:
        """Pricing Director: Optimal pricing strategy"""
        print("\n" + "─"*50)
        print("💰 [PRICING DIRECTOR] David Kim, CPA/MBA")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: MBA Wharton, CPA, 10+ years Walmart/Target")
        print(f"   Model: Phi-2 (HuggingFace)")
        print("─"*50)

        prompt = f"""You are David Kim, CPA/MBA, Director of Pricing Strategy with 10+ years at Walmart/Target.

YOUR ROLE: Determine optimal price that maximizes profit (price × volume), not just margin.

PRODUCT: {product.title} | Cost: ${product.estimated_cost} | Category: {product.category}

YOUR ANALYSIS (3 STEPS):

**STEP 1: Price Elasticity Assessment**
- HIGH elasticity: 10% price cut → 20%+ volume increase (commodities, many alternatives)
- MEDIUM elasticity: 10% cut → 10-15% increase (some differentiation)
- LOW elasticity: 10% cut → <5% increase (unique products, brand loyalty)
Think: How sensitive are customers to price changes?

**STEP 2: Optimal Price Calculation**
Test 3 scenarios:
- Premium: COGS × 3.5 (high margin, low volume)
- Mid-market: COGS × 2.5-3 (balanced, sweet spot)
- Competitive: COGS × 2 (low margin, high volume)
Calculate profit = (Price - COGS - Fees) × Expected Volume
Choose price that maximizes total profit, not margin %

**STEP 3: Psychological Pricing**
- $19.99 vs $20 (below threshold effect)
- $49 vs $50 (charm pricing)
- $97 vs $100 (prestige pricing for premium)
Apply psychology to optimal price

REQUIRED OUTPUT (JSON):
{{
    "optimal_price": calculated price (number),
    "profit_margin_percent": net margin after all fees,
    "price_elasticity": "high|medium|low + evidence",
    "psychological_price": price with charm pricing applied,
    "pricing_strategy": "value|premium|penetration + rationale"
}}

QUALITY STANDARDS:
- ✅ Price: Maximizes profit (not just margin)
- ✅ Elasticity: Based on competition/differentiation
- ✅ Psychology: Applied (ends in .99, .97, or 9)
- ✅ Strategy: Aligned with market position

Think: What price makes the most total profit?"""

        try:
            result = await self._call_groq_model(self.hf_pricing_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Pricing complete: ${parsed.get('optimal_price', 0):.2f}")
            return parsed
        except:
            return {"optimal_price": (product.estimated_cost or 50) * 2.5, "status": "fallback"}

    async def _run_viral_agent(self, product) -> Dict[str, Any]:
        """Viral Specialist: Social media and virality potential"""
        print("\n" + "─"*50)
        print("📱 [VIRAL SPECIALIST] Alex Chen, MS")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: MS Data Science NYU, Ex-TikTok Shop Lead")
        print(f"   Model: Flan-T5-Large (HuggingFace)")
        print("─"*50)

        prompt = f"""You are Alex Chen, MS, Viral Product Specialist - Ex-TikTok Shop Lead (2M+ followers generated).

YOUR ROLE: Assess if this product can go viral and drive organic traffic (vs paid ads).

PRODUCT: {product.title} | Category: {product.category}

YOUR ANALYSIS:

**Virality Score Factors** (0-100):
- Visual appeal: "Wow" factor in photo/video (20 pts)
- Surprise factor: Unexpected/novel/clever (20 pts)
- Problem-solving: Clear before/after transformation (20 pts)
- Shareability: "My friends need to see this" (20 pts)
- Demo-ability: Shows well in 15-30sec video (20 pts)

**Best Platform Analysis**:
- TikTok: Novelty, hacks, transformations, under $30
- Instagram: Aesthetic, lifestyle, aspirational, $30-100
- Pinterest: DIY, home decor, planning products, any price

**Viral Triggers** (what makes people share):
- Utility: "This solves my problem!"
- Aspiration: "I want to be like that"
- Entertainment: "This is hilarious/amazing"
- FOMO: "Everyone has this but me"

**Influencer Potential**:
- HIGH: Unique, visual, under $50, mass appeal
- MEDIUM: Some appeal, higher price, niche
- LOW: Boring, commodity, expensive, unsexy

REQUIRED OUTPUT (JSON):
{{
    "virality_score": 0-100 (realistic, not inflated),
    "best_platform": "tiktok|instagram|pinterest + why",
    "viral_triggers": ["specific triggers this product has"],
    "influencer_potential": "high|medium|low + rationale",
    "trend_lifecycle": "emerging|peak|declining"
}}

Think: Would I share this with friends? Why or why not?"""

        try:
            result = await self._call_groq_model(self.hf_viral_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Viral analysis: {parsed.get('virality_score', 0)}/100")
            return parsed
        except:
            return {"virality_score": 60, "best_platform": "tiktok", "status": "fallback"}

    async def _run_competition_agent(self, product) -> Dict[str, Any]:
        """Competition Analyst: Market saturation and competitive positioning"""
        print("\n" + "─"*50)
        print("⚔️ [COMPETITION ANALYST] Maria Gonzalez, MBA")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: MBA MIT Sloan, 8+ years Shopify")
        print(f"   Model: Llama-3.1-8B (HuggingFace)")
        print("─"*50)

        prompt = f"""You are Maria Gonzalez, MBA MIT Sloan, Competition Analyst (8+ years Shopify analytics).

YOUR ROLE: Assess if this market is a blue ocean (opportunity) or red ocean (bloodbath).

PRODUCT: {product.title} | Category: {product.category}

YOUR ANALYSIS:

**Market Saturation Levels**:
- LOW (<10 sellers): Blue ocean, early market, opportunity
- MEDIUM (10-50 sellers): Growing market, room for differentiation
- HIGH (>50 sellers): Saturated, price competition, avoid unless unique

**Competitive Advantage Assessment**:
Ask: What makes THIS product different from competitors?
- Unique features/design?
- Better quality/price ratio?
- Brand/marketing angle?
- Distribution advantage?
- Or... nothing special? (commodity = avoid)

**Market Entry Difficulty** (1-10):
- 1-3: Easy (anyone can copy, high risk)
- 4-7: Moderate (some barriers, defendable)
- 8-10: Difficult (patents, brand, capital required = defensible)

**Blue Ocean Potential**:
TRUE if: <10 competitors + unique value prop + defensible
FALSE if: >50 competitors OR commodity OR late to market

REQUIRED OUTPUT (JSON):
{{
    "market_saturation": "low|medium|high + evidence (seller count)",
    "competitor_count": estimated number,
    "competitive_advantage": "specific differentiation OR 'none - commodity'",
    "market_entry_difficulty": 1-10 (with reasoning),
    "blue_ocean_potential": true|false + reasoning
}}

Think: Is this a profitable niche or a crowded mess?"""

        try:
            result = await self._call_groq_model(self.hf_competition_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Competition: {parsed.get('market_saturation', 'medium')}")
            return parsed
        except:
            return {"market_saturation": "medium", "competitor_count": 50, "status": "fallback"}

    async def _run_supply_chain_agent(self, product) -> Dict[str, Any]:
        """Supply Chain Director: Sourcing and logistics"""
        print("\n" + "─"*50)
        print("📦 [SUPPLY CHAIN] James Wilson, MBA/CSCP")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: MBA Operations, CSCP, 12+ years Alibaba/FBA")
        print(f"   Model: Flan-T5-XL (HuggingFace)")
        print("─"*50)

        prompt = f"""You are James Wilson, MBA/CSCP, Supply Chain Director (12+ years Alibaba/FBA operations).

YOUR ROLE: Assess operational feasibility - can we actually source, ship, and fulfill this profitably?

PRODUCT: {product.title} | Category: {product.category}

YOUR ANALYSIS:

**Sourcing Difficulty** (1-10):
- 1-3: Easy (standard product, 100+ suppliers on Alibaba)
- 4-7: Moderate (specialized, 10-50 suppliers, some MOQ)
- 8-10: Difficult (custom, few suppliers, high MOQ, long lead times)

**Lead Time Estimate**:
- Standard products: 15-30 days (Alibaba + sea freight)
- Custom products: 45-60 days (design + manufacturing)
- Air freight: +$5-10/unit but 7-10 days

**Shipping Cost** (per unit):
- Small/light (<1 lb): $2-4
- Medium (1-5 lbs): $5-8
- Large/heavy (>5 lbs): $10-15+

**Fulfillment Method**:
- FBA (Amazon): Best for <50 lbs, high volume, easy
- FBM (self-ship): Cost savings but labor intensive
- 3PL: Medium volume, multiple platforms

REQUIRED OUTPUT (JSON):
{{
    "sourcing_difficulty": 1-10 (with evidence),
    "lead_time_days": estimated days,
    "shipping_cost_estimate": $ per unit,
    "fulfillment_method": "FBA|FBM|3PL + rationale",
    "supplier_availability": "high|medium|low + supplier count estimate"
}}

Think: Can we actually execute this operationally?"""

        try:
            result = await self._call_groq_model(self.hf_supply_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Supply chain: {parsed.get('lead_time_days', 0)} days lead time")
            return parsed
        except:
            return {"sourcing_difficulty": 5, "lead_time_days": 30, "status": "fallback"}

    async def _run_psychology_agent(self, product) -> Dict[str, Any]:
        """Consumer Psychology Expert: Customer needs and behavior"""
        print("\n" + "─"*50)
        print("🧠 [PSYCHOLOGY] Dr. Sophia Patel, PhD")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: PhD Consumer Psychology Columbia")
        print(f"   Model: MPNet (HuggingFace)")
        print("─"*50)

        prompt = f"""You are Dr. Sophia Patel, PhD Consumer Psychology Columbia (15+ years behavioral research).

YOUR ROLE: Assess customer needs and emotional drivers - will people actually want to buy this?

PRODUCT: {product.title} | Category: {product.category}

YOUR ANALYSIS:

**Product-Market Fit** (0-100):
Does this solve a REAL problem people are willing to pay for?
- 80-100: Clear pain point + proven demand (pain relievers, productivity tools)
- 60-79: Nice-to-have improvement (convenience, upgrades)
- 40-59: Want but don't need (novelty, luxury)
- <40: Solution looking for problem (avoid)

**Customer Pain Point**:
Be specific: What exact frustration/desire does this address?
- "Traditional curlers damage lashes and don't hold curl" (specific)
- NOT: "People want nice lashes" (too vague)

**Emotional Triggers**:
What emotions drive purchase?
- Fear: Safety, security, loss aversion
- Desire: Status, beauty, achievement
- Frustration: Problem that needs solving NOW
- Aspiration: "Be like successful people who use this"

**Purchase Intent Factors**:
- Urgency: Need it now vs someday?
- Willingness to pay: Luxury or necessity budget?
- Switching cost: Easy to try or committed to current solution?

REQUIRED OUTPUT (JSON):
{{
    "product_market_fit": 0-100 (realistic assessment),
    "customer_pain_point": "specific problem solved",
    "emotional_triggers": ["specific emotions this activates"],
    "target_demographic": "age, income, lifestyle, values",
    "purchase_intent_score": 0-100 (likelihood they'll actually buy)
}}

Think: Would I buy this? Why or why not? Be honest."""

        try:
            result = await self._call_groq_model(self.hf_psychology_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Psychology: {parsed.get('product_market_fit', 0)}/100 fit")
            return parsed
        except:
            return {"product_market_fit": 70, "purchase_intent_score": 65, "status": "fallback"}

    async def _run_data_science_agent(self, product) -> Dict[str, Any]:
        """Data Science Lead: Trend forecasting and demand prediction"""
        print("\n" + "─"*50)
        print("📊 [DATA SCIENCE] Ryan Lee, MS")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: MS Computer Science Stanford, Ex-Google Trends")
        print(f"   Model: BART-Large (HuggingFace)")
        print("─"*50)

        prompt = f"""You are Ryan Lee, MS Data Science Stanford, Trend Forecasting Lead (Ex-Google Trends team).

YOUR ROLE: Predict demand trajectory - will this still be selling in 3 months or dead?

PRODUCT: {product.title} | Trend Score: {product.trend_score} | Search Volume: {product.search_volume}

YOUR ANALYSIS:

**Forecast Logic**:
- RISING: Growing interest, early in lifecycle, opportunity
- STABLE: Mature market, consistent demand, safe but competitive
- DECLINING: Fading trend, late to party, avoid

**Time Horizons**:
- 30 days: Short-term momentum (current trend direction)
- 60 days: Medium-term outlook (seasonal factors kicking in?)
- 90 days: Long-term viability (will this last or fad out?)

**Peak Season Analysis**:
Identify if product has seasonal spikes:
- Q4 (Oct-Dec): Holidays, gifts, winter products
- Q2 (Apr-Jun): Summer, outdoor, graduations
- Q3 (Jul-Sep): Back-to-school, fall prep
- None: Year-round stable demand

**Demand Score** (0-100):
Overall demand strength considering:
- Current trend momentum (30pts)
- Search volume levels (30pts)
- Seasonal factors (20pts)
- Market maturity (20pts)

REQUIRED OUTPUT (JSON):
{{
    "30_day_forecast": "rising|stable|declining + confidence %",
    "60_day_forecast": "rising|stable|declining + confidence %",
    "90_day_forecast": "rising|stable|declining + confidence %",
    "peak_season": "month name or 'none' + reasoning",
    "demand_score": 0-100 (aggregated demand strength)
}}

Think: Will this still be relevant in 90 days?"""

        try:
            result = await self._call_groq_model(self.hf_data_science_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Forecast: {parsed.get('30_day_forecast', 'stable')}")
            return parsed
        except:
            return {"30_day_forecast": "stable", "demand_score": 70, "status": "fallback"}

    async def _run_perplexity_agent(self, product) -> Dict[str, Any]:
        """
        Perplexity Agent: Real-time web search and market research
        Uses Perplexity's Sonar model with live web access
        """
        print("\n" + "─"*50)
        print("🌐 [WEB SEARCH] Dr. Emma Watson, PhD")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: PhD Market Research Oxford, Ex-Nielsen")
        print(f"   Model: Llama-3.1-Sonar-Large-128k-Online (Perplexity)")
        print(f"   Capability: Real-time web search with citations")
        print("─"*50)

        prompt = f"""You are Dr. Emma Watson, PhD, Senior Market Research Analyst specializing in real-time trend analysis and competitive intelligence.

YOUR CREDENTIALS:
- PhD in Market Research and Consumer Analytics from Oxford University
- Former Senior Analyst at Nielsen (8 years)
- Expert in digital trend monitoring, competitive intelligence, and web analytics
- Published researcher in real-time market dynamics and social commerce

YOUR EXPERTISE:
- Real-time trend detection and validation
- Competitive product analysis using live web data
- Social media sentiment analysis
- Market sizing and opportunity assessment
- E-commerce pricing intelligence

YOUR UNIQUE CAPABILITY:
You have access to real-time web search and can query current market data, competitor listings, social media trends, and news. Use this to provide up-to-date, validated insights.

PRODUCT TO RESEARCH:
Title: {product.title}
Description: {product.description}
Category: {product.category}
Price: ${product.estimated_cost}

YOUR TASK - REAL-TIME WEB RESEARCH:

**STEP 1: Market Validation** (Search: Current market demand)
- Search for: "{product.title} trending 2025"
- Search for: "best {product.category} products 2025"
- Validate if this product category is currently popular
- Check social media mentions and discussions

**STEP 2: Competitive Intelligence** (Search: Competitor analysis)
- Search for: "{product.title} Amazon eBay price"
- Search for: "similar to {product.title}"
- Find 3-5 direct competitors with current prices
- Identify price ranges and positioning

**STEP 3: Trend Validation** (Search: Trend signals)
- Search for: "{product.category} market trends 2025"
- Search for: "why {product.title} popular"
- Verify trend momentum (rising/stable/declining)
- Find supporting evidence from recent sources (last 30 days)

**STEP 4: Risk Assessment** (Search: Market saturation)
- Search for: "{product.title} oversaturated market"
- Search for: "{product.category} competition analysis"
- Assess market saturation level
- Identify potential challenges

REQUIRED OUTPUT (Valid JSON only):
{{
    "market_validation": {{
        "is_trending": true/false,
        "trend_strength": "strong|moderate|weak",
        "evidence": "Specific findings from web search with citations",
        "sources": ["URL 1", "URL 2", "URL 3"]
    }},
    "competitive_intelligence": {{
        "competitor_count": "estimate based on search results",
        "price_range": {{"min": 0.0, "max": 0.0}},
        "top_competitors": [
            {{"name": "Product name", "price": 0.0, "source": "Amazon/eBay/etc"}}
        ],
        "our_price_position": "below|at|above market average"
    }},
    "trend_validation": {{
        "momentum": "rising|stable|declining",
        "peak_interest": "current|past|future",
        "supporting_evidence": "Recent data points and findings",
        "news_mentions": "Count or notable mentions",
        "social_signals": "Strong|Moderate|Weak"
    }},
    "risk_assessment": {{
        "market_saturation": "low|medium|high",
        "competition_level": "low|medium|high|extreme",
        "barriers_to_entry": "low|medium|high",
        "risks": ["List specific risks found"],
        "opportunities": ["List specific opportunities found"]
    }},
    "recommendation": {{
        "market_entry_score": 0-100,
        "confidence_level": "high|medium|low",
        "reasoning": "Summary of why this score based on real-time data",
        "action": "proceed|proceed_with_caution|reconsider"
    }}
}}

QUALITY STANDARDS:
- ✅ All findings MUST be based on actual web search results
- ✅ Include specific citations (URLs) for major claims
- ✅ Prioritize recent data (last 30 days) over older sources
- ✅ Validate trends with multiple independent sources
- ✅ Be objective - report both opportunities AND risks
- ✅ Quantify findings whenever possible (prices, counts, percentages)

EXAMPLES OF EXCELLENT ANALYSIS:

Example 1 - Strong Trending Product:
{{
    "market_validation": {{
        "is_trending": true,
        "trend_strength": "strong",
        "evidence": "Google Trends shows 340% increase in searches for 'heated eyelash curler' in Q4 2025. TikTok hashtag #heatedlashcurler has 45M views. Multiple beauty influencers posting reviews.",
        "sources": ["trends.google.com/...", "tiktok.com/@...", "reddit.com/r/beauty"]
    }},
    "competitive_intelligence": {{
        "competitor_count": "15-20 active sellers on Amazon",
        "price_range": {{"min": 12.99, "max": 29.99}},
        "top_competitors": [
            {{"name": "TempTech Heated Curler", "price": 24.99, "source": "Amazon"}},
            {{"name": "BeautyHeat Pro", "price": 19.99, "source": "Amazon"}},
            {{"name": "QuickCurl Plus", "price": 27.99, "source": "eBay"}}
        ],
        "our_price_position": "below market average"
    }},
    "recommendation": {{
        "market_entry_score": 85,
        "confidence_level": "high",
        "reasoning": "Strong validated trend with 340% search growth, moderate competition (15-20 sellers), our price point below average = good opportunity. Risk: Trend may be seasonal (Q4 beauty push).",
        "action": "proceed"
    }}
}}

Example 2 - Oversaturated Market:
{{
    "market_validation": {{
        "is_trending": false,
        "trend_strength": "weak",
        "evidence": "Google Trends flat for 'phone case' - mature market. Amazon shows 50,000+ listings. Dominated by established brands.",
        "sources": ["trends.google.com/...", "amazon.com/s?k=..."]
    }},
    "risk_assessment": {{
        "market_saturation": "high",
        "competition_level": "extreme",
        "risks": ["50,000+ existing listings", "Dominated by major brands (Otterbox, Spigen)", "Race to bottom pricing", "High advertising costs"],
        "opportunities": ["Niche designs (fandom, custom)", "Eco-friendly materials gaining traction"]
    }},
    "recommendation": {{
        "market_entry_score": 35,
        "confidence_level": "high",
        "reasoning": "Extremely saturated market with 50,000+ listings and major brand dominance. Only viable with unique niche or custom designs.",
        "action": "reconsider"
    }}
}}

Think like a PhD market researcher with real-time web access. Use current data to validate or challenge assumptions. Be thorough and cite your sources.
"""

        try:
            print("   📡 Calling Perplexity API (Real-time Web Search)...")

            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.perplexity_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a market research expert with real-time web access. Provide thorough, cited analysis based on current web data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 2000
            }

            response = requests.post(
                self.perplexity_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                parsed = self._parse_json_response(content)

                market_score = parsed.get('recommendation', {}).get('market_entry_score', 50)
                action = parsed.get('recommendation', {}).get('action', 'unknown')
                print(f"   ✅ Real-time analysis complete")
                print(f"   📊 Market Entry Score: {market_score}/100")
                print(f"   🎯 Action: {action}")

                return parsed
            else:
                print(f"   ⚠️ Perplexity API error: {response.status_code}")
                raise Exception(f"Perplexity API returned {response.status_code}")

        except Exception as e:
            print(f"   ❌ Perplexity Agent failed: {str(e)[:80]}")
            print("   🔄 Using fallback analysis (no web search)...")
            return {
                "market_validation": {
                    "is_trending": True,
                    "trend_strength": "unknown",
                    "evidence": "Real-time data unavailable - using conservative estimates",
                    "sources": []
                },
                "competitive_intelligence": {
                    "competitor_count": "unknown",
                    "price_range": {"min": 0, "max": 0},
                    "top_competitors": [],
                    "our_price_position": "unknown"
                },
                "recommendation": {
                    "market_entry_score": 50,
                    "confidence_level": "low",
                    "reasoning": "Unable to perform real-time web search - proceed with manual research",
                    "action": "proceed_with_caution"
                },
                "status": "fallback"
            }

    async def _run_coordinator_agent(
        self, product, agent_results: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """
        Coordinator Agent: Synthesizes all agent results into final decision
        Uses Qwen3 32B (Groq) - Advanced reasoning for strategic decisions
        """
        print("\n" + "─"*50)
        print("👔 [COORDINATOR] Robert Thompson, MBA - Chief Product Officer")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: MBA Harvard, 20+ years Amazon/eBay/Shopify")
        print(f"   🧠 Model: Qwen3 32B (Advanced Reasoning)")
        print(f"   Role: Final Decision Maker - Synthesizing Expert Reports")
        print("─"*50)

        # Extract individual agent results
        scanner_result = agent_results.get("scanner", {})
        trend_result = agent_results.get("trend", {})
        research_result = agent_results.get("research", {})
        quality_result = agent_results.get("quality", {})
        pricing_result = agent_results.get("pricing", {})
        viral_result = agent_results.get("viral", {})
        competition_result = agent_results.get("competition", {})
        supply_result = agent_results.get("supply_chain", {})
        psychology_result = agent_results.get("psychology", {})
        data_science_result = agent_results.get("data_science", {})
        perplexity_result = agent_results.get("perplexity", {})

        prompt = f"""You are Robert Thompson, MBA, Chief Product Officer with over 20 years of experience.

YOUR CREDENTIALS:
- MBA from Harvard Business School (Strategy & Operations)
- BS in Computer Science from Stanford University
- Former VP of Product at Amazon (5 years, managed $100M+ P&L)
- Former Director of Marketplace Strategy at eBay (7 years)
- Former Product Lead at Shopify (4 years)
- Expert in product strategy, multi-platform marketplaces, and P&L management

YOUR ROLE AS CPO:
You are the final decision maker. You synthesize expert reports from your team of specialists and make strategic recommendations based on:
- Business objectives and strategic fit
- Risk-adjusted opportunity assessment
- Long-term sustainability vs short-term gains
- Ethical sourcing and compliance
- Competitive advantage and defensibility

YOUR TEAM'S REPORTS:
You have received detailed analysis from 11 expert specialists. Review their findings carefully:

PRODUCT: {product.title}

CORE ANALYSIS TEAM:
1. SCANNER AGENT (Dr. Sarah Chen, PhD - Product Analyst):
{json.dumps(scanner_result, indent=2)}

2. TREND AGENT (Dr. Michael Rodriguez, PhD - Market Scientist):
{json.dumps(trend_result, indent=2)}

3. RESEARCH AGENT (Jennifer Park, MBA/CFA - Competitive Intelligence):
{json.dumps(research_result, indent=2)}

QUALITY & PRICING TEAM:
4. QUALITY OFFICER (Dr. Elizabeth Martinez, PhD):
{json.dumps(quality_result, indent=2)}

5. PRICING DIRECTOR (David Kim, CPA/MBA):
{json.dumps(pricing_result, indent=2)}

MARKET SPECIALISTS:
6. VIRAL SPECIALIST (Alex Chen, MS - Social Media Expert):
{json.dumps(viral_result, indent=2)}

7. COMPETITION ANALYST (Maria Gonzalez, MBA):
{json.dumps(competition_result, indent=2)}

OPERATIONS TEAM:
8. SUPPLY CHAIN DIRECTOR (James Wilson, MBA/CSCP):
{json.dumps(supply_result, indent=2)}

9. CONSUMER PSYCHOLOGY (Dr. Sophia Patel, PhD):
{json.dumps(psychology_result, indent=2)}

10. DATA SCIENCE LEAD (Ryan Lee, MS - Forecasting):
{json.dumps(data_science_result, indent=2)}

WEB RESEARCH TEAM:
11. MARKET RESEARCH (Dr. Emma Watson, PhD - Real-time Web Intelligence):
{json.dumps(perplexity_result, indent=2)}

YOUR CPO DECISION FRAMEWORK - "ULTRATHINK" STRATEGIC ANALYSIS:

**STEP 1: Synthesize Expert Insights** (Find the signal in the noise)
Review all 11 agent reports and identify:
- Consensus findings: Where do 8+ agents agree? (High confidence)
- Conflicting signals: Where do agents disagree? (Requires judgment)
- Missing data: What critical info is incomplete? (Risk flag)
- Red flags: Any agent raising serious concerns? (Investigate)
Think: What's the story these reports are telling?

**STEP 2: Financial Viability Assessment** (Will this make money?)
Cross-check Financial Agent findings:
- Net margin after ALL costs: Must be >25% for approve (Research Agent)
- Competition level: LOW = good, HIGH = avoid (Research + Competition Agents)
- Pricing power: Can we charge premium or race to bottom? (Pricing + Research Agents)
- Financial scenarios: Is worst-case still profitable? (Research Agent)
Red flag if: Margin <20% OR High competition OR Negative worst-case scenario
Think: Would this pass a CFO review?

**STEP 3: Market Opportunity Validation** (Is there real demand?)
Cross-check Trend & Market Intelligence:
- Trend sustainability: Fad (reject) vs sustainable (approve) (Trend Agent)
- Search volume trajectory: Rising (good) vs declining (bad) (Trend + Data Science Agents)
- Real-time validation: Does Perplexity confirm trend? (Perplexity Agent)
- Seasonal risk: Year-round demand vs one-time spike? (Trend + Data Science Agents)
Red flag if: Fad risk >60% OR Declining trajectory OR Failed real-time validation
Think: Will this still be selling in 6 months?

**STEP 4: Competitive Position Analysis** (Can we win?)
Cross-check Competition & Differentiation:
- Market saturation: <10 sellers = blue ocean (Competition Agent)
- Competitive advantage: Unique value prop vs commodity (Scanner + Competition Agents)
- Barriers to entry: Can competitors easily copy? (Research Agent)
- Virality potential: Organic growth vs paid ads? (Viral Agent)
Red flag if: >50 competitors OR No differentiation OR Low barriers
Think: Why would customers choose US over competitors?

**STEP 5: Operational Feasibility Check** (Can we execute?)
Cross-check Operations & Quality:
- Sourcing difficulty: Easy (<5/10) = good (Supply Chain Agent)
- Quality score: Must be >70/100 for approve (Quality Agent)
- Return rate risk: Must be <15% for category (Quality Agent)
- Lead time: <45 days preferred (Supply Chain Agent)
Red flag if: Sourcing >8/10 OR Quality <60 OR Returns >20%
Think: Can we actually deliver this successfully?

**STEP 6: Risk Assessment** (What could go wrong?)
Aggregate all risks from agents:
- Financial risks: Margin compression, price erosion (Research Agent)
- Market risks: Saturation, fad crash (Trend + Competition Agents)
- Quality risks: Returns, defects (Quality Agent)
- Operational risks: Supply chain, fulfillment (Supply Chain Agent)
Count critical risks: 0-2 = Low, 3-4 = Medium, 5+ = High
Think: What's our worst-case scenario?

**STEP 7: Make Strategic Recommendation** (The Decision)
Apply decision criteria:

**APPROVE** criteria (ALL must be true):
- ✅ Net margin >25% (Research Agent)
- ✅ Low-Medium competition (Competition Agent)
- ✅ Sustainable trend OR early emerging trend (Trend Agent)
- ✅ Unique competitive advantage (Scanner + Competition Agents)
- ✅ Operational feasibility (Supply Chain + Quality Agents)
- ✅ <3 critical risks
Action: Proceed with product launch

**REVIEW** criteria (need more validation):
- ⚠️ Margin 20-25% (marginal)
- ⚠️ Medium competition (risky but possible)
- ⚠️ Trend unclear OR conflicting signals
- ⚠️ Some differentiation but not unique
- ⚠️ 3-4 risks present
Action: Get more data, test small batch, manual review required

**REJECT** criteria (ANY of these = reject):
- ❌ Margin <20% (unprofitable)
- ❌ High competition (>50 sellers, price war)
- ❌ Declining/fad trend (will be dead soon)
- ❌ Commodity product (no differentiation)
- ❌ 5+ critical risks (too many failure modes)
- ❌ Quality score <60 (will destroy reputation)
- ❌ Operational infeasibility (can't execute)
Action: Do not pursue, move to next opportunity

**STEP 8: Calculate Confidence Score** (How sure are we?)
Confidence formula:
- Data quality: All agents returned good data? +30pts
- Agent consensus: 8+ agents agree on key points? +30pts
- Market validation: Real-time data confirms? +20pts
- Track record: Similar products succeeded? +20pts
= Confidence Score (0-100)

80-100: High confidence (data-backed decision)
60-79: Medium confidence (some unknowns remain)
<60: Low confidence (insufficient data, more research needed)

REQUIRED OUTPUT (Valid JSON only):
{{
    "recommendation": "approve|review|reject + CLEAR reasoning matching criteria above",
    "confidence_score": 0-100 (calculated per formula),
    "ai_category": "Use Scanner Agent's category (most precise)",
    "ai_keywords": ["Use Scanner Agent's 8-12 keywords"],
    "ai_description": "Use Scanner Agent's conversion-optimized description",
    "suggested_price": Use Pricing/Research Agent's optimal price,
    "profit_potential_score": 0-100 (from Research Agent, adjusted for risks),
    "competition_level": "low|medium|high (from Research + Competition Agents)",
    "top_strengths": [
        "Strength 1 with specific data (e.g., '30% net margin - highly profitable')",
        "Strength 2 with specific data",
        "Strength 3 with specific data"
    ],
    "top_risks": [
        "Risk 1 with likelihood and impact (e.g., 'Market saturation - 40% likelihood, could drop margin to 15%')",
        "Risk 2 with likelihood and impact",
        "Risk 3 with likelihood and impact"
    ],
    "success_probability": 0-100 (risk-adjusted probability of profitable outcome),
    "strategic_fit": "How this aligns with business goals (e.g., 'High-margin niche product, fits premium strategy')",
    "reasoning": "2-3 paragraph executive summary explaining the decision:
        Paragraph 1: What makes this opportunity attractive (or not)?
        Paragraph 2: Key risks and how significant they are
        Paragraph 3: Final recommendation and next steps",
    "next_steps": "Specific actions if approve/review (e.g., 'Order 100 unit test batch, list on Amazon, monitor for 30 days')"
}}

QUALITY STANDARDS (Harvard MBA + Amazon VP Level):
- ✅ Recommendation: Matches decision criteria exactly (not arbitrary)
- ✅ Strengths/Risks: Specific with data (not generic like "good product")
- ✅ Reasoning: Clear logic chain from agent data to decision
- ✅ Confidence: Reflects actual data quality (not inflated)
- ✅ Conservative: Protect P&L from bad bets (say NO to marginal opportunities)

DECISION PHILOSOPHY:
- **Be conservative**: Better to miss a marginal opportunity than lose money on a bad bet
- **Require proof**: Data must support the decision, not gut feel
- **Protect the business**: 1 big loss can wipe out 10 small wins
- **Focus on winners**: Only approve products with clear competitive advantage
- **Speed matters**: But not at the expense of quality analysis

Think like a CPO managing a $100M P&L who will be held accountable for this decision. Your job is to approve WINNERS and reject LOSERS. Be decisive but conservative.
"""

        try:
            print("   📡 Calling Groq API (Qwen3 32B)...")
            result = await self._call_groq_qwen(prompt)
            parsed = self._parse_json_response(result)

            # Ensure all required fields exist
            final_analysis = {
                "ai_category": parsed.get("ai_category") or scanner_result.get("ai_category", "General"),
                "ai_keywords": parsed.get("ai_keywords") or scanner_result.get("ai_keywords", []),
                "ai_description": parsed.get("ai_description") or scanner_result.get("ai_description", ""),
                "profit_potential_score": parsed.get("profit_potential_score") or research_result.get("profit_potential_score", 70),
                "competition_level": parsed.get("competition_level") or research_result.get("competition_level", "medium"),
                "suggested_price": parsed.get("suggested_price") or research_result.get("suggested_price", 0),
                "recommendation": parsed.get("recommendation", "review"),
                "reasoning": parsed.get("reasoning", "Multi-agent analysis completed"),
                "confidence_score": parsed.get("confidence_score", 75),
                # Include ALL agent reports for audit trail
                "agent_reports": {
                    "scanner": scanner_result,
                    "trend": trend_result,
                    "research": research_result,
                    "quality": quality_result,
                    "pricing": pricing_result,
                    "viral": viral_result,
                    "competition": competition_result,
                    "supply_chain": supply_result,
                    "psychology": psychology_result,
                    "data_science": data_science_result
                }
            }

            print("   ✅ Coordination complete (Qwen3 32B)")
            print(f"\n   🎯 FINAL DECISION:")
            print(f"      Recommendation: {final_analysis['recommendation'].upper()}")
            print(f"      Confidence: {final_analysis['confidence_score']}%")
            print(f"      Category: {final_analysis['ai_category']}")
            print(f"      Suggested Price: ${final_analysis['suggested_price']:.2f}")
            print(f"      Reasoning: {final_analysis['reasoning'][:80]}...")

            return final_analysis

        except Exception as e:
            print(f"   ❌ Coordinator failed: {str(e)[:80]}")
            print("   🔄 Merging best available data from agents...")
            # Fallback: merge best data from all agents
            return {
                "ai_category": scanner_result.get("ai_category", "General"),
                "ai_keywords": scanner_result.get("ai_keywords", []),
                "ai_description": scanner_result.get("ai_description", product.description),
                "profit_potential_score": research_result.get("profit_potential_score", 70),
                "competition_level": research_result.get("competition_level", "medium"),
                "suggested_price": research_result.get("suggested_price", 0),
                "recommendation": "review",
                "reasoning": "Coordinator fallback - agent data merged",
                "confidence_score": 60
            }

    async def _call_groq_model(self, model: str, prompt: str, system_msg: str = "You are an expert AI assistant. Always respond with valid JSON.") -> str:
        """
        Call Groq API with any model
        """
        start_time = time.time()
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }

            # Special parameters for Qwen3 32B to optimize reasoning
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6 if "qwen" in model.lower() else 0.3,
                "top_p": 0.95 if "qwen" in model.lower() else 1.0,
                "max_tokens": 1500
            }

            response = requests.post(self.groq_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            elapsed = time.time() - start_time
            print(f"      ⏱️  Groq API response time: {elapsed:.2f}s")

            return content

        except Exception as e:
            elapsed = time.time() - start_time
            print(f"      ⏱️  Groq API failed after: {elapsed:.2f}s")
            raise Exception(f"Groq API error: {str(e)}")

    async def _call_groq_qwen(self, prompt: str) -> str:
        """
        Call Groq API with Qwen model for reasoning (wrapper for coordinator)
        """
        return await self._call_groq_model(
            self.coordinator_model,
            prompt,
            "You are an expert AI coordinator with advanced reasoning capabilities. Always respond with valid JSON."
        )

    async def _call_huggingface(self, model: str, prompt: str, max_retries: int = 2) -> str:
        """
        Call Hugging Face Inference API
        """
        url = f"{self.hf_url}/{model}"
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        start_time = time.time()

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json={"inputs": prompt, "parameters": {"max_new_tokens": 800, "temperature": 0.4}},
                    timeout=30
                )

                if response.status_code == 503:
                    # Model loading, wait and retry
                    if attempt < max_retries - 1:
                        print(f"      ⏳ Model loading... retrying in 10s (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(10)
                        continue
                    raise Exception("Model unavailable after retries")

                response.raise_for_status()
                result = response.json()

                elapsed = time.time() - start_time
                print(f"      ⏱️  HuggingFace API response time: {elapsed:.2f}s")

                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    return result.get("generated_text", json.dumps(result))

                return str(result)

            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(5)
                    continue
                elapsed = time.time() - start_time
                print(f"      ⏱️  HuggingFace API failed after: {elapsed:.2f}s")
                raise Exception(f"HuggingFace API error: {str(e)}")

        raise Exception("Max retries exceeded")

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from AI response (handles markdown code blocks)
        """
        try:
            # Remove markdown code blocks if present
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]

            # Clean up response
            response = response.strip()

            # Try to find JSON object
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)

            # Fallback: try parsing entire response
            return json.loads(response)

        except Exception as e:
            print(f"  JSON parsing error: {str(e)}")
            # Return empty dict if parsing fails
            return {"status": "parse_failed", "raw_response": response[:200]}

    def _fallback_analysis(self, product) -> Dict[str, Any]:
        """
        Basic rule-based analysis when all agents fail
        """
        print("[Fallback] Using rule-based analysis")

        keywords = [word for word in product.title.split() if len(word) > 3][:8]
        suggested_price = (product.estimated_cost or 50) * 2.5

        return {
            "ai_category": product.category or "General",
            "ai_keywords": keywords,
            "ai_description": product.description or f"High-quality {product.title}",
            "profit_potential_score": min(product.trend_score, 75),
            "competition_level": "medium",
            "suggested_price": round(suggested_price, 2),
            "recommendation": "review",
            "reasoning": "Fallback rule-based analysis",
            "confidence_score": 50
        }


# Example usage
if __name__ == "__main__":
    async def test():
        system = AgenticAISystem()

        # Mock product for testing
        class MockProduct:
            title = "Smart LED Light Bulbs with WiFi Control"
            description = "Color changing smart bulbs"
            category = "Smart Home"
            estimated_cost = 29.99
            trend_score = 85
            search_volume = 50000
            trend_source = "Amazon Best Sellers"

        result = await system.analyze_product_multi_agent(MockProduct())
        print("\n" + "="*60)
        print("FINAL ANALYSIS:")
        print(json.dumps(result, indent=2))
        print("="*60)

    asyncio.run(test())
