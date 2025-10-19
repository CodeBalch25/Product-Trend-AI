# Product Trend Automation System

**Version:** 1.0.0 | **Status:** ✅ PRODUCTION READY | **Last Updated:** 2025-01-19

AI-powered product trend discovery and multi-platform listing management system with **autonomous self-healing** and manual approval workflows.

## 🎉 NEW: Autonomous Self-Healing System

Your application now **monitors and fixes itself automatically**:

- 🤖 **7 AI DevOps Agents** working 24/7
- ⏰ **Checks every 5 minutes** for issues
- 🔧 **Auto-fixes with 85%+ confidence**
- 💾 **Automatic backups** before changes
- 🔄 **Auto-rollback** if fixes fail
- 📊 **Health monitoring API** at `/api/monitoring/health`

**See [CURRENT_STATUS.md](CURRENT_STATUS.md) for complete system status and recent bug fixes.**

---

## ⚠️ IMPORTANT LEGAL & COMPLIANCE NOTICES

### Platform Terms of Service Compliance

**YOU MUST READ AND COMPLY WITH ALL PLATFORM TERMS OF SERVICE**

This application is designed as a **semi-automated** system that requires human review and approval before posting. Fully automated posting without human oversight violates the terms of service of most e-commerce platforms.

### Required Compliance Steps:

1. **Amazon**:
   - Must have approved Amazon Seller Central account
   - Must obtain SP-API credentials through official channels
   - Must comply with Amazon's listing policies and automation guidelines

2. **eBay**:
   - Must have eBay seller account in good standing
   - Must register as eBay developer and obtain API credentials
   - Must follow eBay's automation and listing policies

3. **TikTok Shop**:
   - Must have approved TikTok Shop seller account
   - Must obtain official API access
   - Must comply with TikTok Shop seller policies

4. **Facebook/Instagram**:
   - Must have Facebook Business account
   - Must set up Commerce Manager
   - Must obtain Graph API access
   - Must comply with Meta's commerce policies

5. **Legal Requirements**:
   - Proper business licensing in your jurisdiction
   - Right to sell products (no trademark infringement)
   - Tax compliance (sales tax, income tax)
   - Consumer protection law compliance
   - Product liability considerations

### This System DOES NOT:
- ❌ Automatically post without human review (manual approval required)
- ❌ Guarantee compliance with platform policies
- ❌ Replace need for proper business setup and licensing
- ❌ Handle order fulfillment, customer service, or returns
- ❌ Provide legal or business advice

### This System DOES:
- ✅ Discover trending products from multiple sources
- ✅ Use AI to analyze and categorize products
- ✅ Provide a dashboard for reviewing products
- ✅ Require manual approval before posting
- ✅ Support multi-platform posting through official APIs
- ✅ Track product performance across platforms
- ✅ **Monitor and self-heal system issues autonomously**
- ✅ **Auto-fix errors with AI-powered DevOps agents**

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- FastAPI (Python web framework)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- Celery + Redis (task queue)
- OpenAI/Anthropic/Groq APIs (AI analysis)
- psutil (System monitoring for autonomous agents)

**Frontend:**
- Next.js 14 (React framework)
- TypeScript
- Tailwind CSS
- SWR (data fetching)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (optional, for production)

### System Components

```
┌─────────────────┐
│  Trend Sources  │ (Google Trends, Reddit, TikTok, etc.)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Trend Scanner   │ (Celery periodic task)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │ (Store discovered products)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Analyzer    │ (Claude/GPT-4 analysis)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Review Queue    │ (Dashboard - MANUAL APPROVAL)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Platform Manager │ (Post to approved platforms)
└─────────────────┘
```

### 🤖 Autonomous Self-Healing System (NEW!)

**7 AI DevOps Agents Monitoring 24/7:**

```
┌──────────────────────────────────────────────────────────────┐
│            AUTONOMOUS MONITORING (Every 5 minutes)            │
└────────────────────────┬─────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │  Dr. James Harper             │
         │  Health Monitor Agent         │
         │  (Docker, DB, Redis, API)     │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │  Sarah Mitchell               │
         │  Error Detection Agent        │
         │  (Log parsing & categorization)│
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │  Dr. Marcus Chen              │
         │  Root Cause Analyst           │
         │  (85%+ confidence diagnosis)  │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │  Alex Thompson                │
         │  Fix Engineer                 │
         │  (Auto-apply code fixes)      │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │  Backup & Validation          │
         │  (2-min validation window)    │
         │  (Auto-rollback on failure)   │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │  Learning Engine              │
         │  (Improve from past fixes)    │
         └───────────────────────────────┘
```

**Key Features:**
- 🔄 Runs every 5 minutes automatically
- 🎯 85% confidence threshold for auto-fixes
- 💾 Automatic backups before changes
- ✅ 2-minute validation after fixes
- 🔙 Auto-rollback if fixes fail
- 📈 Learns from outcomes to improve

**Monitoring Dashboard API:**
- `GET /api/monitoring/health` - System health status
- `GET /api/monitoring/status` - Autonomous system status
- `POST /api/monitoring/trigger-check` - Manual trigger
- `GET /api/monitoring/backups` - List backups
- `POST /api/monitoring/rollback/{id}` - Rollback
- `GET /api/monitoring/stats` - Fix statistics

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Python 3.11+ (if running locally)
- Node.js 18+ (if running locally)
- API credentials for platforms you want to use

### Installation

1. **Clone or navigate to the repository:**
```bash
cd C:\Users\timud\Documents\product-trend-automation
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Edit `.env` file and add your API credentials:**
```bash
# Open in your text editor
notepad .env
```

4. **Start the application with Docker:**
```bash
docker-compose up -d
```

5. **Initialize the database:**
```bash
docker-compose exec backend python -c "from models.database import init_db; init_db()"
```

6. **Access the application:**
- Frontend Dashboard: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 🔧 Configuration

### Required API Keys

#### 1. AI Services (at least one required)

**OpenAI (GPT-4):**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Anthropic (Claude):**
1. Go to https://console.anthropic.com/
2. Create API key
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

#### 2. Platform Integration (configure only the platforms you need)

**Amazon SP-API:**
1. Register as Amazon seller
2. Apply for SP-API access: https://developer-docs.amazon.com/sp-api/
3. Create app and get credentials
4. Add to `.env`:
   ```
   AMAZON_SP_API_KEY=your_key
   AMAZON_SP_API_SECRET=your_secret
   AMAZON_SP_REFRESH_TOKEN=your_token
   ```

**eBay API:**
1. Create eBay developer account: https://developer.ebay.com/
2. Register application
3. Get API keys
4. Add to `.env`:
   ```
   EBAY_APP_ID=your_app_id
   EBAY_CERT_ID=your_cert_id
   EBAY_DEV_ID=your_dev_id
   ```

**TikTok Shop:**
1. Apply for TikTok Shop seller account
2. Request API access: https://partner.tiktokshop.com/
3. Add to `.env`:
   ```
   TIKTOK_SHOP_API_KEY=your_key
   TIKTOK_SHOP_SECRET=your_secret
   ```

**Facebook/Instagram:**
1. Create Facebook Business account
2. Set up Commerce Manager
3. Create app at https://developers.facebook.com/
4. Get access token
5. Add to `.env`:
   ```
   FACEBOOK_APP_ID=your_app_id
   FACEBOOK_APP_SECRET=your_secret
   FACEBOOK_ACCESS_TOKEN=your_token
   ```

#### 3. Trend Discovery Sources (optional)

**Reddit API:**
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
```

**Twitter/X API:**
```
TWITTER_BEARER_TOKEN=your_token
```

---

## 📖 Usage Guide

### Workflow

1. **Automated Trend Discovery**
   - System automatically scans trend sources every hour
   - Or manually trigger: Click "Scan Trends Now" in dashboard

2. **AI Analysis**
   - Discovered products are automatically analyzed by AI
   - AI generates descriptions, keywords, pricing suggestions
   - Products move to "Pending Review" status

3. **Manual Review & Approval** (REQUIRED)
   - Review products in dashboard
   - Check AI analysis and suggestions
   - Approve or reject each product
   - Only approved products can be posted

4. **Platform Posting**
   - Select approved product
   - Choose target platforms
   - Click "Post to Platforms"
   - System posts to selected platforms via APIs

5. **Performance Tracking**
   - Monitor posted products
   - View analytics by platform
   - Track revenue and performance

### Dashboard Features

- **Product Queue**: View and filter products by status
- **Analytics**: See total products, pending reviews, posted items
- **Platform Stats**: Track performance across platforms
- **Trend Scanning**: Manual trigger for immediate scans

---

## 🛠️ Development

### Running Locally (without Docker)

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -c "from models.database import init_db; init_db()"

# Start FastAPI server
uvicorn api.main:app --reload --port 8000

# In separate terminal: Start Celery worker
celery -A tasks.celery_app worker --loglevel=info

# In another terminal: Start Celery Beat
celery -A tasks.celery_app beat --loglevel=info
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Database & Redis:**
```bash
# PostgreSQL
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15

# Redis
docker run -d -p 6379:6379 redis:7-alpine
```

### Project Structure

```
product-trend-automation/
├── backend/
│   ├── api/
│   │   └── main.py              # FastAPI application
│   ├── config/
│   │   └── settings.py          # Configuration
│   ├── models/
│   │   └── database.py          # Database models
│   ├── services/
│   │   ├── trend_discovery/
│   │   │   └── trend_scanner.py # Trend scanning
│   │   ├── ai_analysis/
│   │   │   └── product_analyzer.py # AI analysis
│   │   └── platform_integrations/
│   │       └── platform_manager.py # Platform posting
│   ├── agents/                   # 🤖 NEW: Autonomous DevOps agents
│   │   └── devops/
│   │       ├── autonomous_coordinator.py  # Main orchestrator
│   │       ├── health_monitor.py          # System health checks
│   │       ├── error_detector.py          # Error analysis
│   │       ├── root_cause_analyst.py      # Diagnosis
│   │       ├── fix_engineer.py            # Auto-fix application
│   │       └── learning_engine.py         # Learning from fixes
│   ├── monitoring/               # 🤖 NEW: Monitoring infrastructure
│   │   ├── health_checker.py     # Health check utilities
│   │   ├── log_parser.py         # Log parsing & error detection
│   │   └── metrics_collector.py  # System metrics collection
│   ├── safety/                   # 🤖 NEW: Safety systems
│   │   └── backup_manager.py     # Backup & rollback
│   ├── routes/                   # 🤖 NEW: Monitoring API routes
│   │   └── monitoring_routes.py  # Monitoring dashboard endpoints
│   ├── tasks/
│   │   ├── celery_app.py        # Celery configuration
│   │   ├── trend_tasks.py       # Trend scanning tasks
│   │   ├── analysis_tasks.py    # AI analysis tasks
│   │   ├── platform_tasks.py    # Platform sync tasks
│   │   └── monitoring_tasks.py  # 🤖 NEW: Autonomous monitoring tasks
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── ProductCard.tsx
│   │   │   └── DashboardStats.tsx
│   │   ├── pages/
│   │   │   ├── index.tsx        # Main dashboard
│   │   │   └── _app.tsx
│   │   ├── services/
│   │   │   └── api.ts           # API client
│   │   └── styles/
│   │       └── globals.css
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🧪 Testing

### Test Trend Scanning
```bash
curl -X POST http://localhost:8000/api/trends/scan
```

### Test Product Approval
```bash
curl -X POST http://localhost:8000/api/products/1/approve
```

### Check Analytics
```bash
curl http://localhost:8000/api/analytics/dashboard
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Contains sensitive API keys
2. **Use strong SECRET_KEY** - Generate random string for JWT tokens
3. **Keep API keys secure** - Don't share or expose them
4. **Regular updates** - Keep dependencies updated
5. **HTTPS in production** - Use SSL/TLS certificates
6. **Database backups** - Regular PostgreSQL backups
7. **Monitor logs** - Check for unusual activity

---

## 🐛 Troubleshooting

### Common Issues

**1. Database connection error**
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart postgres
```

**2. Celery tasks not running**
```bash
# Check Celery worker logs
docker-compose logs celery

# Restart Celery
docker-compose restart celery celery-beat
```

**3. Frontend can't connect to backend**
```bash
# Check backend is running
curl http://localhost:8000/

# Check CORS settings in backend/api/main.py
```

**4. Platform API errors**
- Verify API credentials in `.env`
- Check platform rate limits
- Ensure account is in good standing
- Review platform API documentation

---

## 📊 Performance Optimization

- **Database indexes**: Already configured on frequently queried fields
- **Caching**: Consider Redis caching for frequent queries
- **Rate limiting**: Respect platform API rate limits
- **Background jobs**: Use Celery for long-running tasks
- **Image optimization**: Compress product images before storing

---

## 🚢 Production Deployment

### Recommended Stack
- **Hosting**: AWS, Google Cloud, or DigitalOcean
- **Database**: Managed PostgreSQL (RDS, Cloud SQL)
- **Redis**: Managed Redis (ElastiCache, MemoryStore)
- **Containers**: Docker with orchestration (ECS, Kubernetes)
- **Reverse Proxy**: Nginx with SSL

### Environment Variables for Production
```env
DEBUG=False
DATABASE_URL=postgresql://user:pass@prod-db:5432/dbname
REDIS_URL=redis://prod-redis:6379/0
SECRET_KEY=very-long-random-secure-key-here
```

---

## 📝 License

This project is provided as-is for educational and business purposes. Users are responsible for ensuring compliance with all applicable laws and platform terms of service.

---

## 🤝 Support & Contributing

### Getting Help
- Check this README thoroughly
- Review API documentation at http://localhost:8000/docs
- Check platform documentation for API issues

### Legal Disclaimer
This software is provided "as is" without warranty of any kind. Users are solely responsible for:
- Compliance with platform terms of service
- Legal and regulatory compliance
- Proper business licensing
- Product quality and fulfillment
- Customer service and returns

The creators of this software assume no liability for misuse, violations of terms of service, or legal issues arising from use of this system.

---

## 🎯 Roadmap

### Current Features
- ✅ Multi-source trend discovery (29 trending product sources)
- ✅ AI-powered product analysis (11-agent system)
- ✅ Manual approval workflow
- ✅ Multi-platform posting
- ✅ Analytics dashboard
- ✅ **Autonomous self-healing system (7 DevOps agents)**
- ✅ **Automated error detection & fixing**
- ✅ **Learning engine for continuous improvement**

### Future Enhancements
- [ ] Advanced trend prediction with ML models
- [ ] Automated pricing optimization
- [ ] Inventory management integration
- [ ] Order fulfillment automation
- [ ] Multi-user support with roles
- [ ] Mobile app
- [ ] Advanced reporting and insights

---

**Built with modern technologies for responsible e-commerce automation**
