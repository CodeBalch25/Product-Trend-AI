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

    def __init__(self, groq_api_key: str = None, huggingface_api_key: str = None):
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.hf_api_key = huggingface_api_key or os.getenv("HUGGINGFACE_API_KEY")

        # Agent endpoints
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.hf_url = "https://api-inference.huggingface.co/models"

        # 🚨 GROQ-ONLY CONFIGURATION (HuggingFace Inference API deprecated text generation in July 2025)
        # All agents now use Groq's FREE models for maximum compatibility

        # CORE TEAM - High Quality Models with ADVANCED REASONING
        self.coordinator_model = "qwq-32b-preview"  # 🧠 NEW: Advanced reasoning for final decisions
        self.groq_scanner_model = "llama-3.3-70b-versatile"  # Product analysis - needs accuracy
        self.groq_trend_model = "qwq-32b-preview"  # 🧠 NEW: Advanced reasoning for trend forecasting

        # SPECIALIST TEAM - Using Groq models (HF text generation no longer available)
        self.hf_scanner_model = "llama-3.1-8b-instant"  # Variable name kept for compatibility
        self.hf_trend_model = "qwq-32b-preview"  # 🧠 NEW: Advanced reasoning for trends
        self.hf_research_model = "qwq-32b-preview"  # 🧠 NEW: Advanced reasoning for financial analysis
        self.hf_quality_model = "llama-3.1-8b-instant"  # Quality assessment
        self.hf_pricing_model = "llama-3.1-8b-instant"  # Pricing strategy
        self.hf_viral_model = "llama-3.1-8b-instant"  # Virality prediction
        self.hf_competition_model = "llama-3.1-8b-instant"  # Competition analysis
        self.hf_supply_model = "llama-3.1-8b-instant"  # Supply chain
        self.hf_psychology_model = "llama-3.1-8b-instant"  # Consumer psychology
        self.hf_data_science_model = "llama-3.1-8b-instant"  # Data science forecasting

        print(f"[AgenticAI] 🎓 EXPANDED EXPERT TEAM - 11 Professional Specialists")
        print(f"  🚀 ALL MODELS NOW USING GROQ (100% FREE & FAST)")
        print(f"  🧠 NEW: Qwen QwQ-32B for ADVANCED REASONING")
        print(f"  📌 Note: HuggingFace Inference API deprecated text generation in July 2025")
        print(f"")
        print(f"  CORE TEAM (ADVANCED REASONING - QwQ-32B):")
        print(f"    • 🧠 CPO: Robert Thompson, MBA Harvard (Final Decisions)")
        print(f"    • Sr. Product Analyst: Dr. Sarah Chen, PhD MIT (Llama-3.3 70B)")
        print(f"")
        print(f"  SPECIALIST TEAM (ADVANCED REASONING - QwQ-32B):")
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
        print(f"  ✅ All 11 agents: 100% GROQ-POWERED - Zero API costs!")

    async def analyze_product_multi_agent(self, product) -> Dict[str, Any]:
        """
        Orchestrate multi-agent analysis of a product
        Agents run sequentially with 0.8s delays to respect Groq free tier rate limits
        """
        analysis_start = time.time()

        print(f"\n{'='*60}")
        print(f"🚀 [MULTI-AGENT AI] Starting analysis")
        print(f"   Product: {product.title[:50]}...")
        print(f"   System: 11-Agent Architecture (Sequential - Rate Limit Optimized)")
        print(f"{'='*60}\n")

        try:
            # Step 1: Run ALL 10 specialist agents SEQUENTIALLY (to avoid Groq rate limits)
            print("📋 [PHASE 1] Deploying 10 specialist agents sequentially...")
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
                "data_science": data_science_result
            }

            for agent_name, result in agent_results.items():
                if isinstance(result, Exception):
                    print(f"\n❌ [{agent_name.title()} Agent] Error: {result}")
                    agent_results[agent_name] = {"status": "failed", "error": str(result)}

            print(f"\n✅ [PHASE 1] All 10 specialist agents completed sequentially in {phase1_time:.2f}s\n")

            # Step 2: Coordinator agent synthesizes results from all 10 agents
            print("📋 [PHASE 2] Coordinator synthesizing results from 10 agents...")
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
- Former Lead Product Analyst at Google Shopping (6 years)
- Expert in consumer behavior, marketplace optimization, and product intelligence
- Published researcher in e-commerce conversion optimization

YOUR EXPERTISE:
- Jobs-to-be-Done (JTBD) framework for customer needs
- Semantic analysis and keyword research
- Marketplace taxonomy and categorization
- Consumer segmentation and psychographics
- Conversion rate optimization

PRODUCT TO ANALYZE:
Title: {product.title}
Description: {product.description}
Category: {product.category}
Price: ${product.estimated_cost}

YOUR TASK:
Apply advanced product analysis methodologies to extract insights:

1. **Category Precision**: Use marketplace taxonomy (Amazon/eBay structure)
   - Format: "Main > Sub > Micro" (e.g., "Electronics > Audio > Headphones > True Wireless")

2. **Keyword Research**: Generate 8-12 high-value keywords
   - Use searchable terms with volume
   - Include long-tail keywords
   - Cover customer intent (features + benefits)
   - Think like an SEO expert

3. **Marketplace Description**: Write 2 compelling sentences
   - Focus on BENEFITS not features
   - Address customer pain points
   - Create urgency and desire
   - Optimized for conversion

4. **Key Features**: Rank by importance to purchase decision
   - What makes this unique?
   - What solves customer problems?

5. **Target Audience**: Specific demographic + psychographic profile
   - Age range, income level, lifestyle
   - Behavioral insights

OUTPUT (Valid JSON only):
{{
    "ai_category": "Precise category path using marketplace taxonomy",
    "ai_keywords": ["8-12 high-value, searchable keywords"],
    "ai_description": "2 sentences, benefits-focused, conversion-optimized",
    "key_features": ["ranked features by customer importance"],
    "target_audience": "Specific demographic + psychographic profile",
    "product_positioning": "How this differentiates from alternatives"
}}

QUALITY STANDARDS:
- Keywords must be searchable terms (no generic words like "best", "great")
- Category must follow Amazon/eBay taxonomy structure
- Description emphasizes benefits over features
- Target audience based on behavioral data, not assumptions

Think like a PhD researcher with 12 years at Google. Use data-driven insights. Be precise and professional.
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
        Uses Qwen QwQ-32B (Groq) - Advanced reasoning for forecasting
        """
        print("\n" + "─"*50)
        print("📊 [TREND AGENT] Dr. Michael Rodriguez, PhD - Lead Market Research Scientist")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Trend Score: {product.trend_score}/100")
        print(f"   Credentials: PhD Stanford, 15+ years Nielsen/McKinsey")
        print(f"   🧠 Model: Qwen QwQ-32B (Advanced Reasoning)")
        print("─"*50)

        prompt = f"""You are Dr. Michael Rodriguez, PhD, Lead Market Research Scientist with 15 years of experience.

YOUR CREDENTIALS:
- PhD in Data Science & Predictive Analytics from Stanford University
- MS in Economics from London School of Economics
- Former Director of Market Intelligence at Nielsen (6 years)
- Former Senior Data Scientist at McKinsey & Company (5 years)
- Expert in trend forecasting, time series analysis, and market dynamics

YOUR EXPERTISE:
- Time series forecasting (ARIMA, Prophet, LSTM models)
- Gartner Hype Cycle analysis for product adoption curves
- Bass Diffusion Model for innovation adoption
- Seasonal decomposition and cyclical pattern detection
- Social listening and sentiment analysis
- Search volume prediction and correlation analysis

PRODUCT TO ANALYZE:
Product: {product.title}
Category: {product.category}
Current Trend Score: {product.trend_score}/100
Search Volume: {product.search_volume}
Data Source: {product.trend_source}

YOUR TASK:
Conduct rigorous market trend analysis using advanced statistical methods:

1. **Trend Strength Assessment**:
   - Analyze momentum and velocity
   - Compare to historical baselines
   - Validate across multiple data sources
   - Classification: weak/moderate/strong (with evidence)

2. **Demand Trajectory Prediction**:
   - Apply time series forecasting
   - Identify growth phase (emerging/growth/maturity/decline)
   - Consider market saturation indicators
   - Forecast: rising/stable/declining (with confidence level)

3. **Seasonal Factor Detection**:
   - Decompose trend from seasonality
   - Identify cyclical patterns
   - Holiday/event impact analysis
   - Result: yes/no (with pattern description if yes)

4. **Hype Cycle Position** (Gartner Framework):
   - Innovation Trigger: Just emerging
   - Peak of Inflated Expectations: Overhyped
   - Trough of Disillusionment: Fad fading
   - Slope of Enlightenment: Real adoption starting
   - Plateau of Productivity: Mainstream acceptance

5. **Statistical Confidence**:
   - Data quality assessment (0-100)
   - Sample size adequacy
   - Cross-validation results
   - Confidence interval width

OUTPUT (Valid JSON only):
{{
    "trend_strength": "weak|moderate|strong with statistical basis",
    "demand_trajectory": "rising|stable|declining with forecast confidence",
    "seasonal_factor": "yes|no",
    "seasonal_pattern": "description of seasonal pattern if yes",
    "trend_confidence": 0-100 statistical confidence score,
    "trend_insights": "2-3 key findings from quantitative analysis",
    "hype_cycle_phase": "innovation_trigger|peak|trough|slope|plateau",
    "risk_assessment": "fad risk percentage 0-100",
    "forecast_horizon": "3-month, 6-month outlook",
    "data_quality_score": 0-100
}}

STATISTICAL RIGOR:
- Use 95% confidence intervals for forecasts
- Validate trends across multiple data sources
- Account for autocorrelation in time series
- Identify and handle outliers appropriately
- Report data limitations honestly

Think like a PhD data scientist at McKinsey. Use quantitative methods. Show statistical reasoning. Be rigorous and evidence-based.
"""

        try:
            # Try Qwen QwQ-32B via Groq first (advanced reasoning)
            try:
                print("   📡 Calling Groq API (Qwen QwQ-32B)...")
                result = await self._call_groq_model(self.groq_trend_model, prompt)
                parsed = self._parse_json_response(result)
                print("   ✅ Trend analysis complete (Qwen QwQ-32B via Groq)")
                print(f"   📊 Result: {parsed.get('trend_strength', 'N/A')} trend, {parsed.get('demand_trajectory', 'N/A')} demand")
                print(f"   📊 Confidence: {parsed.get('trend_confidence', 0)}%")
                return parsed
            except Exception as groq_err:
                print(f"   ⚠️ Qwen QwQ-32B failed: {str(groq_err)[:80]}")
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
        Uses Qwen QwQ-32B (Groq) - Advanced reasoning for financial analysis
        """
        print("\n" + "─"*50)
        print("💼 [RESEARCH AGENT] Jennifer Park, MBA/CFA - Head of Competitive Intelligence")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Estimated Cost: ${product.estimated_cost}")
        print(f"   Credentials: MBA Columbia, CFA, 14+ years Walmart/Morgan Stanley")
        print(f"   🧠 Model: Qwen QwQ-32B (Advanced Reasoning)")
        print("─"*50)

        prompt = f"""You are Jennifer Park, MBA, CFA, Head of Competitive Intelligence with 14 years of experience.

YOUR CREDENTIALS:
- MBA in Finance from Columbia Business School
- Chartered Financial Analyst (CFA) certification
- MS in Operations Research from MIT
- Former VP of Strategic Intelligence at Walmart E-commerce (5 years)
- Former Senior Financial Analyst at Morgan Stanley (4 years)
- Expert in competitive analysis, financial modeling, and market intelligence

YOUR EXPERTISE:
- Porter's Five Forces competitive analysis
- Financial modeling (DCF, NPV, IRR calculations)
- Profit margin optimization
- Market saturation assessment
- Pricing strategy and elasticity analysis
- Competitive landscape mapping
- Risk-adjusted return calculations

PRODUCT TO ANALYZE:
Product: {product.title}
Category: {product.category}
Estimated Cost (COGS): ${product.estimated_cost}
Trend Score: {product.trend_score}/100

YOUR TASK:
Perform comprehensive competitive intelligence and financial analysis:

1. **Competitive Dynamics** (Porter's Five Forces):
   - Threat of new entrants: barriers to entry
   - Supplier power: how many suppliers available
   - Buyer power: price sensitivity of customers
   - Threat of substitutes: alternative products
   - Competitive rivalry: number and strength of competitors

2. **Profit Potential Analysis**:
   - Calculate optimal price point (maximize revenue × margin)
   - Estimate gross margin after marketplace fees (Amazon 15%, eBay 12%)
   - Account for customer acquisition cost (CAC)
   - Consider shipping and handling costs
   - Score: 0-100 based on risk-adjusted ROI

3. **Competition Level Assessment**:
   - LOW: <10 competitors, unique positioning, high barriers
   - MEDIUM: 10-50 competitors, some differentiation possible
   - HIGH: >50 competitors, commoditized, price competition
   - Provide evidence for assessment

4. **Pricing Strategy**:
   - Analyze comparable products pricing
   - Calculate price elasticity considerations
   - Determine optimal price for margin + volume
   - Consider psychological pricing ($19.99 vs $20)

5. **Market Risks**:
   - Identify 3-5 specific risks
   - Rate severity and likelihood
   - Suggest mitigation strategies

6. **Financial Sensitivity Analysis**:
   - Best case scenario (optimistic assumptions)
   - Base case scenario (realistic assumptions)
   - Worst case scenario (pessimistic assumptions)

OUTPUT (Valid JSON only):
{{
    "profit_potential_score": 0-100 data-driven calculation,
    "competition_level": "low|medium|high with specific evidence",
    "suggested_price": optimal calculated price,
    "profit_margin_estimate_percent": percentage margin,
    "profit_margin_estimate_dollars": dollar amount per unit,
    "market_risks": ["3-5 specific risks with mitigation"],
    "opportunity_score": 0-100 risk-adjusted ROI potential,
    "competitive_dynamics": "Porter's Five Forces summary",
    "market_saturation": "low|medium|high with metrics",
    "barriers_to_entry": "assessment of market defensibility",
    "pricing_strategy": "rationale for suggested price",
    "financial_scenarios": {{
        "best_case": {{"margin": X, "probability": Y}},
        "base_case": {{"margin": X, "probability": Y}},
        "worst_case": {{"margin": X, "probability": Y}}
    }}
}}

FINANCIAL RIGOR:
- Use comparable market data for pricing
- Calculate COGS and fully-loaded costs accurately
- Account for ALL marketplace fees (Amazon 15%, shipping, returns)
- Consider CAC (Customer Acquisition Cost)
- Perform sensitivity analysis on key variables
- Be conservative with assumptions (CFA standards)
- Show your financial modeling work

Think like a CFA analyzing an investment. Use rigorous financial methods. Be conservative on risk. Show your calculations.
"""

        try:
            print("   📡 Calling Groq API (Qwen QwQ-32B)...")
            result = await self._call_groq_model(self.hf_research_model, prompt)  # Now Qwen QwQ-32B
            parsed = self._parse_json_response(result)
            print("   ✅ Market research complete (Qwen QwQ-32B)")
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

        prompt = f"""You are Dr. Elizabeth Martinez, PhD, Chief Quality Officer.

CREDENTIALS: PhD in Supply Chain Management from Stanford, 15+ years at Amazon Quality Assurance

PRODUCT: {product.title}
Category: {product.category}
Price: ${product.estimated_cost}

Analyze product quality and return JSON with:
{{
    "quality_score": 0-100,
    "return_rate_prediction": estimated percentage,
    "supplier_reliability": "high|medium|low",
    "manufacturing_concerns": ["list concerns"],
    "quality_risks": ["specific risks"]
}}"""

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

        prompt = f"""You are David Kim, CPA/MBA, Director of Pricing Strategy.

PRODUCT: {product.title}
Cost: ${product.estimated_cost}
Category: {product.category}

Calculate optimal pricing and return JSON:
{{
    "optimal_price": calculated price,
    "profit_margin_percent": percentage,
    "price_elasticity": "high|medium|low",
    "psychological_price": price with .99 ending,
    "pricing_strategy": "value|premium|penetration"
}}"""

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

        prompt = f"""You are Alex Chen, MS, Viral Product Specialist.

PRODUCT: {product.title}
Category: {product.category}

Analyze virality potential and return JSON:
{{
    "virality_score": 0-100,
    "best_platform": "tiktok|instagram|pinterest",
    "viral_triggers": ["what makes it shareable"],
    "influencer_potential": "high|medium|low",
    "trend_lifecycle": "emerging|peak|declining"
}}"""

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

        prompt = f"""You are Maria Gonzalez, MBA, E-commerce Competition Analyst.

PRODUCT: {product.title}
Category: {product.category}

Analyze competition and return JSON:
{{
    "market_saturation": "low|medium|high",
    "competitor_count": estimated number,
    "competitive_advantage": "description",
    "market_entry_difficulty": 1-10,
    "blue_ocean_potential": true|false
}}"""

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

        prompt = f"""You are James Wilson, MBA/CSCP, Supply Chain Director.

PRODUCT: {product.title}
Category: {product.category}

Analyze supply chain and return JSON:
{{
    "sourcing_difficulty": 1-10,
    "lead_time_days": estimated days,
    "shipping_cost_estimate": dollar amount,
    "fulfillment_method": "FBA|FBM|3PL",
    "supplier_availability": "high|medium|low"
}}"""

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

        prompt = f"""You are Dr. Sophia Patel, PhD, Consumer Psychology Expert.

PRODUCT: {product.title}
Category: {product.category}

Analyze consumer psychology and return JSON:
{{
    "product_market_fit": 0-100,
    "customer_pain_point": "what problem it solves",
    "emotional_triggers": ["list triggers"],
    "target_demographic": "description",
    "purchase_intent_score": 0-100
}}"""

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

        prompt = f"""You are Ryan Lee, MS, Data Science & Trend Forecasting Lead.

PRODUCT: {product.title}
Current Trend Score: {product.trend_score}
Search Volume: {product.search_volume}

Forecast trends and return JSON:
{{
    "30_day_forecast": "rising|stable|declining",
    "60_day_forecast": "rising|stable|declining",
    "90_day_forecast": "rising|stable|declining",
    "peak_season": "month name or none",
    "demand_score": 0-100
}}"""

        try:
            result = await self._call_groq_model(self.hf_data_science_model, prompt)  # Now Groq model
            parsed = self._parse_json_response(result)
            print(f"   ✅ Forecast: {parsed.get('30_day_forecast', 'stable')}")
            return parsed
        except:
            return {"30_day_forecast": "stable", "demand_score": 70, "status": "fallback"}

    async def _run_coordinator_agent(
        self, product, agent_results: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """
        Coordinator Agent: Synthesizes all agent results into final decision
        Uses Qwen QwQ-32B (Groq) - Advanced reasoning for strategic decisions
        """
        print("\n" + "─"*50)
        print("👔 [COORDINATOR] Robert Thompson, MBA - Chief Product Officer")
        print(f"   Product: {product.title[:50]}...")
        print(f"   Credentials: MBA Harvard, 20+ years Amazon/eBay/Shopify")
        print(f"   🧠 Model: Qwen QwQ-32B (Advanced Reasoning)")
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
You have received detailed analysis from 10 expert specialists. Review their findings carefully:

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

YOUR CPO DECISION FRAMEWORK:

**Step 1: Synthesize Expert Insights**
- What are the key findings from each specialist?
- Where do they agree? Where do they conflict?
- What data quality issues exist?

**Step 2: Strategic Assessment**
- Does this align with business objectives?
- Is there defensible competitive advantage?
- What are the critical risks?
- Long-term sustainability vs short-term opportunity?

**Step 3: Risk-Adjusted Evaluation**
- Calculate risk-adjusted opportunity score
- Consider market saturation and competition
- Evaluate trend sustainability (fad vs real demand)
- Assess profit margin after ALL costs

**Step 4: Make Recommendation**
- APPROVE: High confidence winner, clear path to profit, sustainable advantage
- REVIEW: Promising but needs more validation, missing data, moderate confidence
- REJECT: High risk, low margin, commodity market, unsustainable trend

**Step 5: Provide Executive Summary**
- Clear reasoning for decision
- Top 3 strengths and top 3 risks
- Confidence level based on data quality

REQUIRED OUTPUT (Valid JSON only):
{{
    "ai_category": "Final category decision (most precise from Scanner)",
    "ai_keywords": ["final optimized keyword list (best 8-12 from Scanner)"],
    "ai_description": "Final marketplace description (conversion-optimized from Scanner)",
    "profit_potential_score": 0-100 final score after all adjustments,
    "competition_level": "low|medium|high with executive summary",
    "suggested_price": final pricing recommendation with rationale,
    "recommendation": "approve|review|reject",
    "reasoning": "Executive summary: why this decision, key factors, critical risks",
    "confidence_score": 0-100 based on data quality and specialist agreement,
    "strategic_fit": "How this aligns with business objectives",
    "top_strengths": ["3 key strengths"],
    "top_risks": ["3 critical risks"],
    "success_probability": 0-100 likelihood of profitable outcome,
    "next_steps": "What needs to happen next (if review/approve)"
}}

DECISION STANDARDS (Harvard MBA + Amazon VP level):
- Data must support all conclusions
- Be conservative on risk assessment
- Prioritize sustainable competitive advantage
- Consider total addressable market (TAM)
- Account for execution complexity
- Ethical sourcing and compliance are non-negotiable

Think like a CPO managing a $100M P&L. Make strategic decisions. Balance risk vs opportunity. Protect the business from bad bets while capturing high-potential wins.
"""

        try:
            print("   📡 Calling Groq API (Qwen QwQ-32B)...")
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

            print("   ✅ Coordination complete (Qwen QwQ-32B)")
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

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
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
