# QUICK RESTART GUIDE

## How to Start Your Application

### 1. Start All Services:
```bash
cd C:\Users\timud\Documents\product-trend-automation
docker-compose up -d
```

### 2. Verify Everything Started:
```bash
docker ps
```

Should see 6 containers running:
- [RUNNING] product-trend-frontend
- [RUNNING] product-trend-backend
- [RUNNING] product-trend-celery
- [RUNNING] product-trend-celery-beat
- [RUNNING] product-trend-db
- [RUNNING] product-trend-redis

### 3. Access Your Application:
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Admin:** http://localhost:8000/admin

### 4. Monitor Self-Healing:
```bash
# Watch live
docker logs product-trend-celery --follow | grep "AUTONOMOUS"

# View recent fixes
docker exec product-trend-backend tail -50 /app/logs/autonomous_fixes.log
```

---

## If Something Goes Wrong

### Restart a specific service:
```bash
docker restart product-trend-backend
docker restart product-trend-celery
docker restart product-trend-frontend
```

### View logs:
```bash
docker logs product-trend-backend
docker logs product-trend-celery
docker logs product-trend-frontend
```

### Full restart:
```bash
docker-compose down
docker-compose up -d
```

---

## Before You Post Products

### Add Platform Tokens to .env:
```bash
# Amazon
AMAZON_SP_API_CLIENT_ID=your_client_id
AMAZON_SP_API_CLIENT_SECRET=your_secret
AMAZON_SP_API_REFRESH_TOKEN=your_token

# eBay
EBAY_APP_ID=your_app_id
EBAY_CERT_ID=your_cert
EBAY_DEV_ID=your_dev_id
EBAY_TOKEN=your_token

# TikTok
TIKTOK_SHOP_APP_KEY=your_key
TIKTOK_SHOP_APP_SECRET=your_secret
TIKTOK_SHOP_ACCESS_TOKEN=your_token
```

Then restart:
```bash
docker-compose restart backend celery
```

---

**That's it! Your self-healing system will monitor and fix issues automatically every 15 minutes.**
