# ⚡ QUICK FIX - Run These Commands Now

## 🎯 Your Situation
- Docker won't start - Port 5432 conflict
- Want to clear database for fresh scan

## ✅ SOLUTION - Copy & Paste These Commands

### **Step 1: Open Command Prompt as Administrator**

**Windows Key → Type "cmd" → Right-click → "Run as administrator"**

---

### **Step 2: Find What's Using Port 5432**

```cmd
netstat -ano | findstr :5432
```

**Look for output like:**
```
TCP    0.0.0.0:5432    0.0.0.0:0    LISTENING    1234
```

The last number (1234) is the Process ID.

**If you see output**, there's something using port 5432. Most likely PostgreSQL.

**If you see nothing**, port is free - skip to Step 4.

---

### **Step 3A: Stop PostgreSQL Service**

```cmd
net stop postgresql-x64-14
```

**Or try:**
```cmd
net stop postgresql-x64-15
```

**Or try:**
```cmd
net stop postgresql-x64-16
```

**Expected:** `The PostgreSQL service was stopped successfully.`

**If that doesn't work, try Step 3B:**

---

### **Step 3B: Kill the Process (Replace 1234 with your PID from Step 2)**

```cmd
taskkill /PID 1234 /F
```

**Expected:** `SUCCESS: The process with PID 1234 has been terminated.`

---

### **Step 4: Verify Port is Free**

```cmd
netstat -ano | findstr :5432
```

**Expected:** No output (port is free!) ✅

---

### **Step 5: Navigate to Project**

```cmd
cd C:\Users\timud\Documents\product-trend-automation
```

---

### **Step 6: Clean Docker**

```cmd
docker-compose down -v
```

**Expected:**
```
Stopping containers...
Removing containers...
Removing volumes...
```

---

### **Step 7: Start Docker Services**

```cmd
docker-compose up -d
```

**Wait 30 seconds...**

**Expected:**
```
Creating network...
Creating product-trend-db ... done
Creating product-trend-redis ... done
Creating product-trend-backend ... done
Creating product-trend-celery ... done
Creating product-trend-frontend ... done
```

---

### **Step 8: Check All Containers Are Running**

```cmd
docker-compose ps
```

**ALL should show "Up":**
```
NAME                        STATUS
product-trend-backend       Up
product-trend-celery        Up
product-trend-db            Up
product-trend-frontend      Up
product-trend-redis         Up
```

**If any show "Exit" or "Restarting":**
```cmd
docker-compose logs [container-name]
```

---

### **Step 9: Initialize Empty Database**

```cmd
docker-compose exec backend python -c "from models.database import init_db; init_db()"
```

**Expected:**
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

---

### **Step 10: OPTIONAL - Clear Any Existing Products**

**Only if database had products from before:**

```cmd
docker-compose exec backend python clear_database.py
```

**Expected:**
```
============================================================
🗑️  DATABASE RESET
============================================================
Current products: 28
✅ Deleted 28 products successfully!
Remaining products: 0
============================================================
✓ Database is now empty and ready for fresh scan!
============================================================
```

**If database was already empty:**
```
Current products: 0
✓ Database is already empty!
```

---

### **Step 11: Verify Services Are Working**

**Test backend:**
```cmd
curl http://localhost:8000/
```

**Expected:** JSON response with `"status": "running"`

**Open frontend:**
```cmd
start http://localhost:3000
```

**Expected:** Dashboard opens in browser

---

## 🎉 NOW TEST A FRESH SCAN!

### **Option A: Watch Logs While Scanning**

**Open a second Command Prompt:**

```cmd
cd C:\Users\timud\Documents\product-trend-automation
docker-compose logs -f backend
```

**Keep this open, then go to browser and click "Scan Trends Now"**

You'll see products being created in real-time!

---

### **Option B: Just Scan**

1. Go to: `http://localhost:3000`
2. Click **"Scan Trends Now"**
3. Wait for green toast: "Found X new trending products!"
4. Refresh page - products appear!

---

## 🔍 What You'll See (Fresh Database)

**In the logs:**
```
================================================================================
🔍 TREND SCANNER - Starting Multi-Source Scan
================================================================================

📡 Scanning source: _scan_amazon_best_sellers
   Found 5 products from this source
   → Product 1/5: Apple AirPods Pro (2nd Generation)...
      ✓ Creating new product  ← CREATING!
   → Product 2/5: Instant Pot Duo 7-in-1...
      ✓ Creating new product
   ...

📊 SCAN SUMMARY:
   Sources Scanned: 3
   Products Found: 13
   Products Created: 13  ← ALL NEW!
   Products Updated: 0
   Products Skipped: 0
================================================================================

✅ SCAN COMPLETED SUCCESSFULLY!
   Message: Found 13 new trending products!
```

**In the browser:**
- Green toast: "Found 13 new trending products!"
- Products appear in dashboard
- Status shows "discovered" or "pending_review"

---

## ❌ If Something Goes Wrong

### **Port still in use?**
```cmd
# Reboot computer
shutdown /r /t 0
```

### **Docker container errors?**
```cmd
# Check specific container logs
docker-compose logs backend
docker-compose logs postgres

# Restart problem container
docker-compose restart backend
```

### **Can't connect to database?**
```cmd
# Restart postgres
docker-compose restart postgres

# Wait 10 seconds, then try init again
docker-compose exec backend python -c "from models.database import init_db; init_db()"
```

### **Frontend won't load?**
```cmd
# Restart frontend
docker-compose restart frontend

# Check logs
docker-compose logs frontend
```

---

## ✅ SUCCESS CHECKLIST

After these steps, you should have:

- [x] Port 5432 free (no PostgreSQL conflict)
- [x] All Docker containers running ("Up" status)
- [x] Database initialized with empty tables
- [x] Products cleared (0 products)
- [x] Backend API responding
- [x] Frontend dashboard loading
- [x] Ready for fresh scan!

---

## 🚀 After Fresh Scan

Products will be:
1. **Created** (13 products from Amazon, Google Trends, Reddit)
2. **Analyzed by AI** (multi-agent system)
3. **Ready for review** (status: "pending_review")
4. **Visible in dashboard** (refresh to see them)

Then you can:
- Approve good products
- Reject bad products
- Post to platforms (after configuring platform APIs)

---

## 💡 Summary - All Commands in Order

```cmd
# 1. Stop PostgreSQL (as Administrator)
net stop postgresql-x64-14

# 2. Navigate to project
cd C:\Users\timud\Documents\product-trend-automation

# 3. Clean Docker
docker-compose down -v

# 4. Start fresh
docker-compose up -d

# 5. Wait 30 seconds, then init database
timeout /t 30
docker-compose exec backend python -c "from models.database import init_db; init_db()"

# 6. Clear products (if any)
docker-compose exec backend python clear_database.py

# 7. Watch logs (optional)
docker-compose logs -f backend

# 8. Open dashboard and scan!
start http://localhost:3000
```

---

**Ready?** Start with Step 1 and work through the commands! 🎯
