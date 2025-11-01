# System Architecture - Product Trend Automation

**Visual Reference Guide**
**Last Updated:** October 21, 2025

---

## 🏗️ Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                                │
│                                                                         │
│  Frontend (React)                                                       │
│  - Product dashboard                                                    │
│  - Review workflow                                                      │
│  - Analytics                                                            │
│  Port: 3000                                                             │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ HTTP/REST
                             ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          BACKEND API (FastAPI)                          │
│                                                                         │
│  - REST API endpoints                                                   │
│  - Database operations                                                  │
│  - Task queue management                                                │
│  Port: 8000                                                             │
└────────┬────────────────┬────────────────────┬─────────────────────────┘
         │                │                    │
         │                │                    │
         ↓                ↓                    ↓
┌────────────────┐  ┌─────────────────┐  ┌──────────────────────┐
│   PostgreSQL   │  │  Redis (Cache)  │  │  Celery Workers      │
│                │  │                 │  │                      │
│  - products    │  │  - Task queue   │  │  - Trend scanning    │
│  - keywords ⭐ │  │  - Results      │  │  - AI analysis       │
│  - sources     │  │  - Sessions     │  │  - Platform posting  │
│  - listings    │  │                 │  │  - Health checks     │
│  Port: 5432    │  │  Port: 6379     │  │  Workers: 32         │
└────────────────┘  └─────────────────┘  └──────────────────────┘
                                                    ↑
                                                    │ Triggers tasks
                                                    ↓
                                         ┌──────────────────────┐
                                         │  Celery Beat         │
                                         │  (Scheduler)         │
                                         │                      │
                                         │  - Every 1hr: Scan   │
                                         │  - Every 6hr: Perpl. │
                                         │  - Every 15min: AI   │
                                         │  - Every 5min: Health│
                                         └──────────────────────┘
```

---

## 🤖 12-Agent AI System Architecture

```
                         ┌─────────────────────────┐
                         │   Product to Analyze    │
                         │  (from TrendScanner)    │
                         └───────────┬─────────────┘
                                     │
                                     ↓
        ┌────────────────────────────────────────────────────┐
        │            PHASE 1: SPECIALIST AGENTS              │
        │         (11 agents run sequentially)               │
        │         0.8s delay between calls (rate-limit)      │
        └────────────────────────────────────────────────────┘
                                     │
        ┌────────────────────────────┼───────────────────────────┐
        │                            │                           │
        ↓                            ↓                           ↓

┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  GROQ AGENTS  │    │  GROQ AGENTS  │    │  PERPLEXITY   │
│   (Core 3)    │    │(Specialists 8)│    │   (Web 1) ⭐  │
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                     │
        ↓                    ↓                     ↓

┌─────────────────────────────────────────────────────────────┐
│  1. Scanner Agent                                           │
│     Dr. Sarah Chen, PhD MIT                                 │
│     Model: Llama-3.3 70B                                    │
│     Task: Category mapping, keywords, competitive advantage │
│     Instructions: 200 lines "ultrathink"                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. Trend Agent                                             │
│     Dr. Michael Rodriguez, PhD Stanford                     │
│     Model: Qwen3 32B (Advanced Reasoning)                   │
│     Task: Trend analysis, market cycles, forecasting        │
│     Instructions: 230 lines "ultrathink"                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  3. Research Agent                                          │
│     Jennifer Park, MBA/CFA Columbia                         │
│     Model: Qwen3 32B (Advanced Reasoning)                   │
│     Task: Financial analysis, Porter's 5 Forces, profit     │
│     Instructions: 260 lines "ultrathink"                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  4-11. Specialist Agents (8 agents)                         │
│     - Quality Officer (Dr. Elizabeth Martinez)              │
│     - Pricing Director (David Kim)                          │
│     - Viral Specialist (Alex Chen)                          │
│     - Competition Analyst (Maria Gonzalez)                  │
│     - Supply Chain (James Wilson)                           │
│     - Psychology (Dr. Sophia Patel)                         │
│     - Data Science (Ryan Lee)                               │
│     Model: Llama-3.1 8B Instant                             │
│     Instructions: 40-80 lines each "ultrathink"             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  12. Perplexity Web Search Agent ⭐ NEW                     │
│      Dr. Emma Watson, PhD Oxford                            │
│      Model: Sonar (Perplexity)                              │
│      Task: Real-time web search, citations, market data     │
│      Instructions: 260 lines "ultrathink"                   │
│      Special: Searches live web for product trends          │
└─────────────────────────────────────────────────────────────┘

        │                    │                     │
        └────────────────────┼─────────────────────┘
                             ↓
        ┌────────────────────────────────────────────────────┐
        │            PHASE 2: COORDINATOR                    │
        │         (Synthesizes all agent reports)            │
        └────────────────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│  Coordinator Agent                                          │
│  Robert Thompson, MBA Harvard                               │
│  Model: Qwen3 32B (Advanced Reasoning)                      │
│  Role: Chief Product Officer - Final Decision Maker         │
│  Task: APPROVE / REVIEW / REJECT                            │
│  Instructions: 140 lines with 8-step decision framework     │
│                                                             │
│  Decision Criteria:                                         │
│  ✅ APPROVE: Margin >25%, Low competition, Sustainable      │
│  ⚠️ REVIEW: Margin 20-25%, Medium competition               │
│  ❌ REJECT: Margin <20%, High competition, Fatal risks      │
└─────────────────────────────────────────────────────────────┘
                             │
                             ↓
                   ┌─────────────────┐
                   │ Final Decision  │
                   │ + Analysis Data │
                   │ Stored in DB    │
                   └─────────────────┘
```

---

## 🔄 Perplexity Feedback Loop Architecture ⭐ NEW

```
┌────────────────────────────────────────────────────────────────┐
│                     PERPLEXITY DISCOVERY                       │
│                    (Runs every 6 hours)                        │
└────────────────────────────────────────────────────────────────┘
                              │
                              │ 1. Web Search
                              ↓
                    ┌─────────────────────┐
                    │  Perplexity API     │
                    │  Model: Sonar       │
                    │                     │
                    │  Searches:          │
                    │  - "viral products" │
                    │  - "trending now"   │
                    │  - "TikTok trends"  │
                    │  - "Amazon hot"     │
                    └─────────────────────┘
                              │
                              │ 2. Extracts Data
                              ↓
              ┌──────────────────────────────────┐
              │  Discovered Data                 │
              │                                  │
              │  Products (7):                   │
              │  - Product name                  │
              │  - Category                      │
              │  - Price range                   │
              │  - Trend strength                │
              │  - Evidence/Citations            │
              │                                  │
              │  Keywords (28):                  │
              │  - "skin repair patches"         │
              │  - "kojic acid serum"            │
              │  - "TikTok perfume"              │
              │  - "nail bloom effect"           │
              │  - ... 24 more                   │
              └──────────────────────────────────┘
                              │
                              │ 3. Store in Database
                              ↓
              ┌──────────────────────────────────┐
              │  trending_keywords table         │
              │                                  │
              │  - keyword (unique, indexed)     │
              │  - category                      │
              │  - trend_strength                │
              │  - search_count                  │
              │  - last_seen                     │
              │  - expires_at (30 days)          │
              │  - related_products              │
              │                                  │
              │  Current: 28 keywords stored     │
              └──────────────────────────────────┘
                              │
                              │ 4. TrendScanner Loads
                              ↓
┌────────────────────────────────────────────────────────────────┐
│                        TREND SCANNER                           │
│                      (Runs every 1 hour)                       │
│                                                                │
│  Step 1: Load keywords from database                          │
│  → SELECT keyword FROM trending_keywords                       │
│     WHERE expires_at > NOW()                                   │
│     ORDER BY search_count DESC                                 │
│     LIMIT 20                                                   │
│                                                                │
│  Step 2: Scan 7 sources                                       │
│  → Amazon Best Sellers, Amazon Deals, TikTok, Reddit          │
│    Google Trends, Instagram, Pinterest                        │
│                                                                │
│  Step 3: For each product found:                              │
│  → Check if product matches any keyword                       │
│  → if match: PRIORITIZE (higher trend score)                  │
│  → Save to database                                           │
│                                                                │
│  Result: Products matching Perplexity keywords get analyzed   │
│          first by the 12-agent system                         │
└────────────────────────────────────────────────────────────────┘
                              │
                              │ 5. Continuous Learning
                              ↓
              ┌──────────────────────────────────┐
              │  SELF-IMPROVING SYSTEM           │
              │                                  │
              │  - Perplexity discovers new      │
              │    trends from the web           │
              │  - Keywords stored in DB         │
              │  - Scanner uses keywords to      │
              │    find matching products        │
              │  - System learns what's hot      │
              │  - Process repeats every 6hrs    │
              │                                  │
              │  → SYSTEM GETS SMARTER OVER TIME │
              └──────────────────────────────────┘
```

---

## 📦 Data Flow: Product Discovery → Analysis → Posting

```
┌─────────────────────────────────────────────────────────────────┐
│                     STEP 1: DISCOVERY                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │   TrendScanner scans 7 sources:     │
        │                                     │
        │   1. Amazon Best Sellers            │
        │   2. Amazon Deals                   │
        │   3. TikTok Trends                  │
        │   4. Reddit (r/shutupandtakemymoney)│
        │   5. Google Trends                  │
        │   6. Instagram Trends               │
        │   7. Pinterest Trends               │
        │                                     │
        │   Loads 20 Perplexity keywords ⭐   │
        │   Prioritizes matching products     │
        └─────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │   Products saved to database        │
        │   Status: DISCOVERED                │
        │                                     │
        │   Example:                          │
        │   - Ergonomic Split Keyboard        │
        │   - Trend Score: 78/100             │
        │   - Source: Reddit                  │
        └─────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     STEP 2: AI ANALYSIS                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │   12-Agent AI System analyzes:      │
        │                                     │
        │   Phase 1: 11 Specialists (17s)    │
        │   - Scanner, Trend, Research        │
        │   - Quality, Pricing, Viral         │
        │   - Competition, Supply Chain       │
        │   - Psychology, Data Science        │
        │   - Perplexity Web Search ⭐        │
        │                                     │
        │   Phase 2: Coordinator (0.5s)      │
        │   - Synthesizes all reports         │
        │   - Makes final decision            │
        │                                     │
        │   Total: ~17-20 seconds             │
        └─────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │   Analysis complete                 │
        │   Status: PENDING_REVIEW            │
        │                                     │
        │   Example:                          │
        │   - Quality: 85/100                 │
        │   - Price: $149.99                  │
        │   - Margin: 32%                     │
        │   - Competition: Medium             │
        │   - Viral Potential: 72/100         │
        │   - Decision: APPROVE ✅            │
        └─────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     STEP 3: MANUAL REVIEW                       │
│                  (REQUIRE_MANUAL_APPROVAL=True)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │   User reviews in dashboard         │
        │                                     │
        │   - Views AI analysis               │
        │   - Checks all agent reports        │
        │   - Reviews pricing/margins         │
        │   - Validates decision              │
        │                                     │
        │   User clicks:                      │
        │   ✅ Approve → Status: APPROVED     │
        │   ❌ Reject  → Status: REJECTED     │
        └─────────────────────────────────────┘
                              │
                              ↓ (if approved)
┌─────────────────────────────────────────────────────────────────┐
│                     STEP 4: PLATFORM POSTING                    │
│                   (Only if AUTO_POST_ENABLED=True)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │   Platform Integration (Future)     │
        │                                     │
        │   - Amazon SP-API (not configured)  │
        │   - eBay API (not configured)       │
        │   - TikTok Shop (not configured)    │
        │   - Facebook Marketplace            │
        │                                     │
        │   Current: Manual posting only      │
        └─────────────────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │   Product posted                    │
        │   Status: POSTED                    │
        │                                     │
        │   Tracked in platform_listings:     │
        │   - Platform name                   │
        │   - Listing ID                      │
        │   - Views, clicks, sales            │
        └─────────────────────────────────────┘
```

---

## 🗄️ Database Schema

```
┌─────────────────────────────────────────────────────────────────┐
│                          products                               │
├─────────────────────────────────────────────────────────────────┤
│  id (PK)                    INTEGER                             │
│  title                      VARCHAR(500)                        │
│  description                TEXT                                │
│  category                   VARCHAR(200)                        │
│  image_url                  VARCHAR(1000)                       │
│  source_url                 VARCHAR(1000)                       │
│                                                                 │
│  trend_score                FLOAT                               │
│  trend_source               VARCHAR(200)                        │
│  search_volume              INTEGER                             │
│  social_mentions            INTEGER                             │
│                                                                 │
│  ai_category                VARCHAR(200)                        │
│  ai_keywords                JSON                                │
│  ai_description             TEXT                                │
│  profit_potential_score     FLOAT                               │
│  competition_level          VARCHAR(50)                         │
│                                                                 │
│  estimated_cost             FLOAT                               │
│  suggested_price            FLOAT                               │
│  potential_margin           FLOAT                               │
│                                                                 │
│  status                     ENUM (ProductStatus)                │
│  approved_by_user           BOOLEAN                             │
│  posted_platforms           JSON                                │
│  platform_ids               JSON                                │
│                                                                 │
│  discovered_at              TIMESTAMP                           │
│  analyzed_at                TIMESTAMP                           │
│  approved_at                TIMESTAMP                           │
│  posted_at                  TIMESTAMP                           │
│  updated_at                 TIMESTAMP                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    trending_keywords ⭐ NEW                     │
├─────────────────────────────────────────────────────────────────┤
│  id (PK)                    INTEGER                             │
│  keyword                    VARCHAR(200) UNIQUE NOT NULL        │
│  category                   VARCHAR(200)                        │
│  trend_strength             VARCHAR(50)                         │
│                                                                 │
│  search_count               INTEGER DEFAULT 1                   │
│  last_seen                  TIMESTAMP                           │
│  first_discovered           TIMESTAMP                           │
│                                                                 │
│  related_products           JSON                                │
│  source_urls                JSON                                │
│                                                                 │
│  expires_at                 TIMESTAMP (30 days from discovery)  │
│  created_at                 TIMESTAMP                           │
│  updated_at                 TIMESTAMP                           │
│                                                                 │
│  Current Data: 28 keywords                                     │
│  Examples:                                                      │
│  - "skin repair patches" (Beauty & Skincare)                   │
│  - "kojic acid serum" (Beauty & Skincare)                      │
│  - "TikTok perfume" (General)                                  │
│  - "nail bloom effect" (Beauty & Nail Care)                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       trend_sources                             │
├─────────────────────────────────────────────────────────────────┤
│  id (PK)                    INTEGER                             │
│  name                       VARCHAR(200) UNIQUE                 │
│  source_type                VARCHAR(100)                        │
│  url                        VARCHAR(1000)                       │
│  enabled                    BOOLEAN                             │
│                                                                 │
│  products_found             INTEGER                             │
│  successful_posts           INTEGER                             │
│  last_scan                  TIMESTAMP                           │
│                                                                 │
│  scan_interval_minutes      INTEGER DEFAULT 60                  │
│  config                     JSON                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    platform_listings                            │
├─────────────────────────────────────────────────────────────────┤
│  id (PK)                    INTEGER                             │
│  product_id (FK)            INTEGER                             │
│  platform                   ENUM (Platform)                     │
│                                                                 │
│  platform_listing_id        VARCHAR(200)                        │
│  listing_url                VARCHAR(1000)                       │
│  listing_status             VARCHAR(100)                        │
│                                                                 │
│  views                      INTEGER                             │
│  clicks                     INTEGER                             │
│  sales                      INTEGER                             │
│  revenue                    FLOAT                               │
│                                                                 │
│  posted_at                  TIMESTAMP                           │
│  last_synced                TIMESTAMP                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        audit_logs                               │
├─────────────────────────────────────────────────────────────────┤
│  id (PK)                    INTEGER                             │
│  action                     VARCHAR(200)                        │
│  entity_type                VARCHAR(100)                        │
│  entity_id                  INTEGER                             │
│  details                    JSON                                │
│  user_id                    VARCHAR(200)                        │
│  created_at                 TIMESTAMP                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔌 External Integrations

```
┌─────────────────────────────────────────────────────────────────┐
│                        GROQ API                                 │
│                   (11 AI Agents - FREE)                         │
├─────────────────────────────────────────────────────────────────┤
│  Endpoint: https://api.groq.com/openai/v1/chat/completions     │
│  Auth: Bearer {GROQ_API_KEY}                                    │
│                                                                 │
│  Models Used:                                                   │
│  - Qwen3 32B (qwen/qwen3-32b)                                   │
│    → Coordinator, Trend Agent, Research Agent                   │
│  - Llama-3.3 70B (llama-3.3-70b-versatile)                      │
│    → Scanner Agent                                              │
│  - Llama-3.1 8B (llama-3.1-8b-instant)                          │
│    → 8 Specialist Agents                                        │
│                                                                 │
│  Rate Limit: 14,400 requests/day (free tier)                   │
│  Current Usage: ~100-200 req/day (97% headroom)                 │
│  Delay: 0.8s between calls (rate-limit friendly)               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     PERPLEXITY API ⭐                           │
│              (1 Web Search Agent - FREE TIER)                   │
├─────────────────────────────────────────────────────────────────┤
│  Endpoint: https://api.perplexity.ai/chat/completions          │
│  Auth: Bearer {PERPLEXITY_API_KEY}                              │
│                                                                 │
│  Model: sonar (online web search)                               │
│                                                                 │
│  Features:                                                      │
│  - Real-time web search                                         │
│  - Citations and sources                                        │
│  - Market trend discovery                                       │
│                                                                 │
│  Usage: Discovery task every 6 hours                            │
│  Response Time: ~40 seconds                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    PLATFORM APIs (Future)                       │
│                      (NOT CONFIGURED YET)                       │
├─────────────────────────────────────────────────────────────────┤
│  Amazon SP-API:                                                 │
│  - Get: https://developer-docs.amazon.com/sp-api/               │
│  - Env: AMAZON_SP_API_KEY, AMAZON_SP_API_SECRET                 │
│                                                                 │
│  eBay API:                                                      │
│  - Get: https://developer.ebay.com/                             │
│  - Env: EBAY_APP_ID, EBAY_CERT_ID, EBAY_DEV_ID                  │
│                                                                 │
│  TikTok Shop:                                                   │
│  - Get: https://partner.tiktokshop.com/                         │
│  - Env: TIKTOK_SHOP_API_KEY, TIKTOK_SHOP_SECRET                 │
│                                                                 │
│  Facebook/Instagram (Meta):                                     │
│  - Get: https://developers.facebook.com/                        │
│  - Env: FACEBOOK_APP_ID, FACEBOOK_APP_SECRET                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 Performance Characteristics

```
┌─────────────────────────────────────────────────────────────────┐
│                      OPERATION TIMES                            │
├─────────────────────────────────────────────────────────────────┤
│  Trend Scan (7 sources)              ~25 seconds                │
│  Perplexity Discovery                ~40 seconds                │
│  12-Agent Analysis                   ~17-20 seconds             │
│  Single Agent Call                   ~0.3-1.5 seconds           │
│  Database Query                      ~10-50ms                   │
│  API Request (Groq)                  ~0.3-1.0 seconds           │
│  API Request (Perplexity)            ~10-30 seconds             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       THROUGHPUT                                │
├─────────────────────────────────────────────────────────────────┤
│  Products scanned per hour           ~53 products               │
│  Products analyzed per hour          ~180 products (max)        │
│  Keywords discovered per 6hrs        ~20-30 keywords            │
│  API calls per hour                  ~15-25 calls               │
│  API calls per day                   ~100-200 calls             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     RESOURCE USAGE                              │
├─────────────────────────────────────────────────────────────────┤
│  Docker Containers                   6 containers               │
│  Memory (total)                      ~2-3 GB                    │
│  CPU (idle)                          ~5-10%                     │
│  CPU (analysis)                      ~20-40%                    │
│  Database Size                       ~50-100 MB                 │
│  Disk Space                          ~500 MB (total)            │
└─────────────────────────────────────────────────────────────────┘
```

---

**End of Architecture Documentation**

*For detailed implementation, see PROJECT_STATE.md*
*For commands and operations, see QUICK_REFERENCE.md*
*For session details, see SESSION_HANDOFF_2025-10-21.md*
