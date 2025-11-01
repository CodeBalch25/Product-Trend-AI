# 🐛 DEBUG GUIDE: "Failed to Scan" Issue

## 🎯 What We're Fixing

You're seeing "Failed to start trend scan" when clicking the "Scan Trends Now" button. This guide will help you:
1. Stop and restart all services cleanly
2. View detailed debug logs
3. Identify the exact error
4. Fix the specific issue

---

## 📋 Prerequisites

Make sure you have:
- ✅ Docker Desktop running (you mentioned you see PostgreSQL in it)
- ✅ Terminal/Command Prompt access
- ✅ `.env` file with API keys (already created for you)

---

## 🚀 STEP-BY-STEP DEBUGGING

### **Step 1: Stop Everything Cleanly**

Open a terminal and navigate to your project:

```bash
cd C:\Users\timud\Documents\product-trend-automation
```

Stop and remove all containers:

```bash
docker-compose down -v
```

**What this does**:
- Stops all running containers
- Removes containers
- Removes volumes (including database data - we'll recreate it fresh)

**Expected output:**
```
Stopping product-trend-frontend ... done
Stopping product-trend-backend  ... done
Stopping product-trend-celery   ... done
Stopping product-trend-db       ... done
Stopping product-trend-redis    ... done
Removing containers...
Removing volumes...
```

---

### **Step 2: Rebuild and Start Services**

Rebuild everything with fresh configuration:

```bash
docker-compose up --build -d
```

**What this does**:
- `--build`: Rebuilds the Docker images (includes latest code changes)
- `-d`: Runs in detached mode (background)

**Expected output:**
```
Building backend...
Building frontend...
Building celery...
Creating network "product-trend-automation_app-network" ...
Creating product-trend-db ... done
Creating product-trend-redis ... done
Creating product-trend-backend ... done
Creating product-trend-celery ... done
Creating product-trend-frontend ... done
```

**⏱️ Wait 30 seconds** for services to fully start.

---

### **Step 3: Check Service Status**

Verify all containers are running:

```bash
docker-compose ps
```

**Expected output - ALL should show "Up":**
```
NAME                        STATUS
product-trend-backend       Up
product-trend-celery        Up
product-trend-celery-beat   Up
product-trend-db            Up
product-trend-frontend      Up
product-trend-redis         Up
```

**⚠️ If any show "Exit" or "Restarting":**
```bash
# Check logs for that specific service
docker-compose logs [service-name]

# Example:
docker-compose logs backend
```

---

### **Step 4: Initialize Database**

The database tables should be auto-created, but let's verify:

```bash
docker-compose exec backend python -c "from models.database import init_db; init_db()"
```

**Expected output:**
```
============================================================
🔧 INITIALIZING DATABASE
============================================================
Database URL: postgresql://postgres:postgres@postgres:5432/product_trends
Creating tables...
✓ Database connection successful!
✓ Tables created: products, trend_sources, platform_listings, audit_logs
============================================================
```

**✅ If you see this**: Database is ready!

**❌ If you see an error**:
- Check if PostgreSQL container is running: `docker ps | findstr postgres`
- Check backend can reach database: `docker-compose logs backend`

---

### **Step 5: Watch Backend Logs in Real-Time**

Open a **NEW terminal window** and run:

```bash
cd C:\Users\timud\Documents\product-trend-automation
docker-compose logs -f backend
```

**What this does**: Shows live backend logs with all debug messages

**Keep this terminal open** - you'll see detailed output when you click "Scan Trends Now"

---

### **Step 6: Open the Application**

1. Open your browser
2. Go to: **http://localhost:3000**
3. You should see the dashboard

**⚠️ If the page doesn't load:**
- Check frontend is running: `docker ps | findstr frontend`
- Check frontend logs: `docker-compose logs frontend`
- Try: `http://127.0.0.1:3000`

---

### **Step 7: Click "Scan Trends Now" and Watch Logs**

1. In the browser, click **"Scan Trends Now"** button
2. **Immediately look at the terminal** with backend logs

**You should see detailed output like:**

```
================================================================================
🔍 SCAN TRENDS ENDPOINT CALLED - DEBUG MODE
================================================================================
✓ Step 1: Testing database connection...
  ✓ Database connected! Current products: 0
✓ Step 2: Generated scan ID: a1b2c3d4
✓ Step 3: Marking existing products as not new...
  ✓ Products marked
✓ Step 4: Products before scan: 0
✓ Step 5: Initializing TrendScanner...
  ✓ TrendScanner initialized
✓ Step 6: Running scan_all_sources...
Scanning _scan_amazon_best_sellers...
Scanning _scan_google_trends...
Scanning _scan_reddit_trends...
  ✓ Scan complete! Results: {'products_found': 8, 'sources_scanned': 3}
✓ Step 7: Marking new products...
  ✓ Marked 8 new products
✓ Step 8: Products after scan: 8 (new: 8)
✓ Step 9: Attempting to trigger Celery AI analysis...
  ✓ AI analysis task triggered successfully

✅ SCAN COMPLETED SUCCESSFULLY!
   Message: Found 8 new trending products!
================================================================================
```

**✅ If you see this**: Scan is working! Products should appear in the dashboard.

---

### **Step 8: What If It Fails?**

If you see:
```
❌ SCAN FAILED!
   Error: [some error message]
   Type: [error type]
   Traceback: [detailed error]
```

**Take a screenshot or copy the full error** and look for these common issues:

---

## 🔧 COMMON ERRORS & SOLUTIONS

### **Error 1: Database Connection Failed**
```
✗ Database error: could not connect to server
```

**Solution:**
```bash
# Check if PostgreSQL is running
docker ps | findstr postgres

# If not running, start it
docker-compose up -d postgres

# Check PostgreSQL logs
docker-compose logs postgres
```

---

### **Error 2: Import Error (pytrends, requests, etc.)**
```
✗ Scanner initialization failed: No module named 'pytrends'
```

**Solution - Missing Python packages:**
```bash
# Rebuild backend with dependencies
docker-compose build backend

# Restart backend
docker-compose up -d backend
```

---

### **Error 3: Celery Connection Error**
```
⚠ Celery task failed (non-critical): [Errno 111] Connection refused
```

**This is OK!** The scan will still work. Products just won't get AI analysis immediately.

**To fix (optional):**
```bash
# Check if Redis is running
docker ps | findstr redis

# Check Celery worker
docker-compose logs celery

# Restart Celery
docker-compose restart celery
```

---

### **Error 4: Groq/HuggingFace API Error**
```
✗ AI analysis error: 401 Unauthorized
```

**Solution - Check API keys in `.env`:**
```bash
# View current .env file
type .env

# Make sure these lines exist and have values:
# GROQ_API_KEY=your_groq_api_key_here
# HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# If changed, restart backend
docker-compose restart backend
```

---

### **Error 5: Empty Scan Results**
```
✅ SCAN COMPLETED SUCCESSFULLY!
   Message: No new products found. Market trends unchanged.
```

**This is normal if:**
- Amazon/Reddit blocked the scraper (they do this sometimes)
- All products from scan already exist in database

**Solution - Check fallback data:**
The scanner should automatically use fallback products if scraping fails. Check logs for:
```
Amazon best sellers error: [error]
# Fallback: If scraping failed, provide sample real products
```

Products should still be added even if scraping fails.

---

## 📊 Verifying It Works

### **1. Check Backend Logs**
Should show:
```
✅ SCAN COMPLETED SUCCESSFULLY!
```

### **2. Check Frontend**
- Refresh the page
- Products should appear in "Pending Review" section
- Click "All Products" to see all discovered items

### **3. Check Database**
```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d product_trends

# Count products
SELECT COUNT(*) FROM products;

# View recent products
SELECT id, title, status FROM products ORDER BY discovered_at DESC LIMIT 5;

# Exit
\q
```

---

## 🎯 Quick Troubleshooting Checklist

Run through this if something isn't working:

```bash
# 1. Are all containers running?
docker-compose ps

# 2. Can backend reach database?
docker-compose exec backend python -c "from models.database import engine; print(engine.connect())"

# 3. Is frontend connecting to backend?
curl http://localhost:8000/

# 4. Check all logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
docker-compose logs celery

# 5. Restart everything
docker-compose restart
```

---

## 🚑 Nuclear Option: Complete Reset

If nothing works, do a complete reset:

```bash
# Stop everything
docker-compose down -v

# Remove all product-trend images
docker images | findstr product-trend
# (Note the IMAGE IDs, then:)
docker rmi [IMAGE_ID] [IMAGE_ID] ...

# Rebuild from scratch
docker-compose build --no-cache

# Start fresh
docker-compose up -d

# Initialize database
docker-compose exec backend python -c "from models.database import init_db; init_db()"

# Check logs
docker-compose logs -f backend
```

---

## 📸 What to Share If Still Stuck

If you're still having issues, provide:

1. **Full error from backend logs**:
   ```bash
   docker-compose logs backend > backend_error.log
   ```

2. **Service status**:
   ```bash
   docker-compose ps > services_status.txt
   ```

3. **Environment check**:
   ```bash
   docker-compose exec backend env | findstr API > api_keys_check.txt
   ```

---

## ✅ Success Indicators

You know it's working when:

1. ✅ Backend logs show `✅ SCAN COMPLETED SUCCESSFULLY!`
2. ✅ Browser shows green toast: "Found X new trending products!"
3. ✅ Products appear in the dashboard
4. ✅ After a few minutes, products status changes to "Pending Review" (AI analysis complete)

---

## 🎉 Next Steps After Scan Works

Once scanning works:

1. **Review Products**: Click on products to see details
2. **Approve/Reject**: Use the buttons to approve good products
3. **Check AI Analysis**: Wait a few minutes and refresh - products should have AI descriptions
4. **Platform Integration**: Configure platform API keys if you want to post products

---

## 💡 Tips

- **First scan is slower**: HuggingFace models take 10-20 seconds to load initially
- **Celery is optional**: Scans work even without Celery, AI analysis just happens later
- **Groq is faster**: If Groq is working, you'll see "via Groq" in logs
- **Debug mode**: Keep `DEBUG=True` in `.env` until everything works perfectly

---

## 📞 Still Need Help?

The detailed logs from Step 7 will show EXACTLY where it's failing. Share:
- The full output from the backend terminal
- Any red error messages
- Which step number it failed at

This guide is designed to find the exact problem, not just guess! 🎯
