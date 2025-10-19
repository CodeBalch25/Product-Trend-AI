# 🔧 Fix Port Conflict & Fresh Start Guide

## ❌ The Problem

**Port 5432 is already in use** - you likely have PostgreSQL running outside of Docker.

**Error:**
```
ports are not available: exposing port TCP 0.0.0.0:5432 -> 127.0.0.1:0:
bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
```

---

## ✅ SOLUTION - Step by Step

### **Step 1: Find What's Using Port 5432**

Open **Command Prompt as Administrator** and run:

```cmd
netstat -ano | findstr :5432
```

**Expected output:**
```
TCP    0.0.0.0:5432    0.0.0.0:0    LISTENING    1234
```

The last number (e.g., `1234`) is the Process ID (PID).

---

### **Step 2: Find Which Program is Using That Port**

```cmd
tasklist | findstr [PID]
```

Replace `[PID]` with the actual number from Step 1.

**Example:**
```cmd
tasklist | findstr 1234
```

**Common culprits:**
- `postgres.exe` - Local PostgreSQL installation
- `pg_ctl.exe` - PostgreSQL service
- Other database programs

---

### **Step 3: Stop the Conflicting Service**

**Option A: Stop PostgreSQL Service (Recommended)**

```cmd
# List PostgreSQL services
sc query | findstr postgres

# Stop the service (run as Administrator)
net stop postgresql-x64-[version]
```

**Example:**
```cmd
net stop postgresql-x64-14
```

**Option B: Kill the Process (If service stop doesn't work)**

```cmd
taskkill /PID [PID] /F
```

**Example:**
```cmd
taskkill /PID 1234 /F
```

---

### **Step 4: Verify Port is Free**

```cmd
netstat -ano | findstr :5432
```

**Expected:** No output (port is free)

---

### **Step 5: Clean Docker Setup**

```cmd
# Navigate to project
cd C:\Users\timud\Documents\product-trend-automation

# Stop all containers
docker-compose down -v

# Remove any orphaned containers
docker-compose down --remove-orphans

# Verify nothing is running
docker-compose ps
```

**Expected:** No containers listed

---

### **Step 6: Start Fresh**

```cmd
# Start all services
docker-compose up -d

# Wait 30 seconds
timeout /t 30

# Check status - ALL should show "Up"
docker-compose ps
```

**Expected output:**
```
NAME                        STATUS
product-trend-backend       Up
product-trend-celery        Up
product-trend-db            Up (healthy)
product-trend-frontend      Up
product-trend-redis         Up
```

---

### **Step 7: Initialize Database**

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

### **Step 8: Verify Services**

```cmd
# Check backend API
curl http://localhost:8000/

# Check frontend
start http://localhost:3000
```

**Expected:**
- Backend: JSON response with `"status": "running"`
- Frontend: Dashboard opens in browser

---

## 🗑️ CLEAR ALL PRODUCTS (Fresh Database)

Since database is empty after the fresh start, you don't need to clear anything!

**But if you want to clear products later:**

```cmd
docker-compose exec backend python manage_products.py
# Select option 4: Clear ALL products
# Type: DELETE
```

---

## 🧪 TEST FRESH SCAN

Now test a fresh scan:

### **1. Open Two Terminals**

**Terminal 1 - Watch Backend Logs:**
```cmd
cd C:\Users\timud\Documents\product-trend-automation
docker-compose logs -f backend
```

**Terminal 2 - Optional: Watch All Logs:**
```cmd
cd C:\Users\timud\Documents\product-trend-automation
docker-compose logs -f
```

### **2. Open Browser**

```
http://localhost:3000
```

### **3. Click "Scan Trends Now"**

### **4. Watch the Logs!**

You should see:

```
================================================================================
🔍 SCAN TRENDS ENDPOINT CALLED - DEBUG MODE
================================================================================
✓ Step 1: Testing database connection...
  ✓ Database connected! Current products: 0  ← Empty database!

...

================================================================================
🔍 TREND SCANNER - Starting Multi-Source Scan
================================================================================

📡 Scanning source: _scan_amazon_best_sellers
   Found 5 products from this source
   → Product 1/5: Apple AirPods Pro (2nd Generation)...
      ✓ Creating new product  ← CREATING, not skipping!
   → Product 2/5: Instant Pot Duo 7-in-1 Electric Pressure...
      ✓ Creating new product
   ... (continues)

📡 Scanning source: _scan_google_trends
   ✓ Google Trends API successful - found 3 trending searches
   Found 3 products from this source
   → Product 1/3: Smart Home Security Camera System...
      ✓ Creating new product

📡 Scanning source: _scan_reddit_trends
   Found 5 products from this source
   → Product 1/5: cool new lockpick set...
      ✓ Creating new product

================================================================================
📊 SCAN SUMMARY:
   Sources Scanned: 3
   Products Found: 13
   Products Created: 13  ← ALL NEW!
   Products Updated: 0
   Products Skipped (duplicates): 0
================================================================================

✅ SCAN COMPLETED SUCCESSFULLY!
   Message: Found 13 new trending products!
================================================================================
```

### **5. Check Dashboard**

Refresh `http://localhost:3000`

**You should see:**
- 13 new products appear!
- Status: "discovered" or "pending_review" (after AI analysis)

---

## 🤖 AI ANALYSIS WILL START AUTOMATICALLY

After products are created, watch for:

```
[Celery logs]
🤖 MULTI-AGENT AI SYSTEM ACTIVATED 🤖
  ✓ Coordinator: Qwen (via Groq)
  ✓ Scanner Agent: Mixtral-8x7B (Hugging Face)
  ✓ Trend Agent: Mistral-7B (Hugging Face)
  ✓ Research Agent: Llama-3-8B (Hugging Face)

🚀 Using Multi-Agent AI System for analysis...

============================================================
[AgenticAI] Starting multi-agent analysis for: Apple AirPods Pro
============================================================

[Phase 1] Deploying specialist agents...
[Scanner Agent] Analyzing product details...
[Trend Agent] Analyzing market trends...
[Research Agent] Evaluating market opportunity...

[Scanner Agent] ✓ Analysis complete (Llama-3.3 70B via Groq)
[Trend Agent] ✓ Trend analysis complete (DeepSeek R1 via Groq)
[Research Agent] ✓ Market research complete (Llama-3.2 11B)

[Phase 1] ✓ All specialist agents completed

[Phase 2] Coordinator agent synthesizing results...
[Coordinator Agent] ✓ Final decision: APPROVE
[Coordinator Agent]   Confidence: 87%

✅ Multi-Agent analysis complete!
============================================================
```

**Products will move to "Pending Review" status!**

---

## 📋 Quick Troubleshooting

### **Port still in use after stopping service?**

```cmd
# Reboot your computer
shutdown /r /t 0
```

### **Docker won't start?**

```cmd
# Make sure Docker Desktop is running
# Check system tray for Docker icon

# Restart Docker Desktop
```

### **Containers keep restarting?**

```cmd
# Check individual logs
docker-compose logs backend
docker-compose logs postgres

# Look for error messages
```

### **Database connection failed?**

```cmd
# Verify postgres is healthy
docker-compose ps

# Check postgres logs
docker-compose logs postgres

# Try restarting postgres
docker-compose restart postgres
```

---

## 🎯 SUCCESS CHECKLIST

After following these steps, verify:

- [ ] Port 5432 is free (`netstat -ano | findstr :5432` shows nothing)
- [ ] All Docker containers are "Up" (`docker-compose ps`)
- [ ] Database initialized successfully
- [ ] Backend API responds (`curl http://localhost:8000/`)
- [ ] Frontend loads (`http://localhost:3000`)
- [ ] Scan creates 13 new products
- [ ] Products appear in dashboard
- [ ] AI analysis starts automatically (watch celery logs)
- [ ] Products move to "Pending Review"

---

## 🚀 Alternative: Change Docker Port (If you need local PostgreSQL)

If you need to keep your local PostgreSQL running, change Docker's port:

**Edit `docker-compose.yml`:**

Find this:
```yaml
postgres:
  ports:
    - "5432:5432"
```

Change to:
```yaml
postgres:
  ports:
    - "5433:5432"  # Use 5433 on host, 5432 in container
```

**Then update `.env`:**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/product_trends
```

**Then restart:**
```cmd
docker-compose down
docker-compose up -d
```

---

## 💡 Summary Commands

```cmd
# 1. Find what's using port 5432
netstat -ano | findstr :5432

# 2. Stop PostgreSQL service (as Administrator)
net stop postgresql-x64-[version]

# 3. Clean Docker
cd C:\Users\timud\Documents\product-trend-automation
docker-compose down -v

# 4. Start fresh
docker-compose up -d

# 5. Initialize database
docker-compose exec backend python -c "from models.database import init_db; init_db()"

# 6. Watch logs
docker-compose logs -f backend

# 7. Scan and watch products being created!
http://localhost:3000
```

---

You'll have a completely fresh database and can watch products being created in real-time! 🎉
