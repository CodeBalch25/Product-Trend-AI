# 🤖 Autonomous Agents Monitoring Guide

**Last Updated:** October 23, 2025

---

## ✅ Quick Status - Are They Running?

**YES! They run every 5 minutes, 24/7!**

Current schedule:
- `:00` (on the hour)
- `:05` (5 minutes after)
- `:10` (10 minutes after)
- `:15`, `:20`, `:25`, `:30`, `:35`, `:40`, `:45`, `:50`, `:55`

---

## 📊 What They Check Every 5 Minutes

✓ **Docker Containers** - All 6 services running?
✓ **Database Connection** - PostgreSQL accessible?
✓ **Redis Connection** - Cache & queue working?
✓ **Backend API Health** - Responding to requests?
✓ **Celery Workers** - Processing tasks?
✓ **Application Logs** - Scanning for errors
✓ **System Resources** - Memory, CPU status

---

## 🔍 How to Monitor Them

### **Option 1: View Latest Health Checks (Recommended)**
```bash
docker exec product-trend-backend tail -60 /app/logs/autonomous_fixes.log
```

### **Option 2: View Last 5 Health Checks**
```bash
docker exec product-trend-backend tail -200 /app/logs/autonomous_fixes.log
```

### **Option 3: Watch Live (Real-time monitoring)**
```bash
docker logs product-trend-celery --follow | grep "AUTONOMOUS"
```

### **Option 4: View Full Log File**
```bash
docker exec product-trend-backend cat /app/logs/autonomous_fixes.log
```

### **Option 5: Check JSON Reports (For scripting)**
```bash
docker exec product-trend-backend tail -10 /app/logs/monitoring_reports.jsonl
```

---

## 📋 What Each Status Means

### ✅ **Healthy Status**
```
✅ RESULT: All Systems Healthy!
   • No issues detected
   • No action required
   • All services operating normally
```
**What this means:** Everything is perfect! Agents found no problems.

---

### 📊 **Monitoring Status**
```
📊 RESULT: Monitoring Mode
   • Non-critical issues detected: 2
   • Issues are below auto-fix threshold (70% confidence)
   • Continuing to monitor - no action taken
   • Will auto-fix if confidence increases
```
**What this means:** Minor issues detected, but not serious enough to auto-fix yet. Agents are watching and will fix if it gets worse.

---

### 🔧 **Auto-Fix Status**
```
🔧 RESULT: Auto-Fix Actions Taken!
   ✅ Successfully Applied: 2
   ❌ Failed to Apply: 0
   ⏸️  Pending Manual Review: 0
   👁️  Monitoring Only: 1
```
**What this means:** Agents detected a problem and **automatically fixed it!** Check logs for details.

---

### ❌ **Failed Status**
```
❌ RESULT: Health Check Failed
   • Error encountered during check
   • Will retry in 5 minutes
```
**What this means:** The health check itself had an error. Rare. Agents will retry.

---

## 🎯 Example: What You'll See

```
================================================================================
🤖 AUTONOMOUS HEALTH CHECK RUN - 2025-10-23 18:57:15 UTC
================================================================================

📋 SYSTEMS CHECKED:
   ✓ Docker Containers (6 expected: frontend, backend, celery, celery-beat, db, redis)
   ✓ Database Connection (PostgreSQL)
   ✓ Redis Connection (Cache & Queue)
   ✓ Backend API Health
   ✓ Celery Workers Status
   ✓ Application Logs (Scanning for errors)
   ✓ System Resources (Memory, CPU if available)

📊 RESULT: Monitoring Mode
   • Non-critical issues detected: 2
   • Issues are below auto-fix threshold (70% confidence)
   • Continuing to monitor - no action taken
   • Will auto-fix if confidence increases

⏰ NEXT CHECK: In 5 minutes (runs 24/7 every 5 minutes)
================================================================================
```

---

## 🚀 What Auto-Fixes Can They Do?

The autonomous agents can **automatically fix** these issues (when confidence > 70%):

1. **Database Issues:**
   - Column too small → Expand column
   - NULL violations → Add default values
   - Duplicate keys → Switch to upsert
   - Missing indexes → Add indexes

2. **Code Errors:**
   - KeyError → Change to dict.get()
   - AttributeError → Add getattr()
   - ImportError → pip install missing package

3. **API/Service Issues:**
   - CORS errors → Update middleware
   - Validation errors → Update schema
   - Rate limits → Add delays

4. **Infrastructure:**
   - Container stopped → Restart container
   - Missing files → Create files
   - Permission errors → Fix permissions

**Total: 20+ types of errors can be auto-fixed!**

---

## ⏰ Verify They're Running

Run this command to see the schedule:
```bash
docker exec product-trend-celery-beat celery -A tasks.celery_app inspect scheduled
```

You should see `autonomous-health-check` scheduled every 5 minutes.

---

## 📊 Quick Stats

To count how many checks have run:
```bash
docker exec product-trend-backend sh -c "grep 'AUTONOMOUS HEALTH CHECK RUN' /app/logs/autonomous_fixes.log | wc -l"
```

To count how many auto-fixes were applied:
```bash
docker exec product-trend-backend sh -c "grep 'Auto-Fix Actions Taken' /app/logs/autonomous_fixes.log | wc -l"
```

---

## 🎉 Current Status

**✅ ACTIVE AND RUNNING 24/7**

The autonomous agents are:
- ✅ Checking every 5 minutes
- ✅ Logging every run with full details
- ✅ Auto-fixing issues when confidence > 70%
- ✅ Monitoring non-critical issues
- ✅ Validating fixes after application

**You can now verify they're doing exactly what they're programmed to do!**

---

## 📞 Need to Trigger Manually?

If you want to run a health check right now (outside the 5-minute schedule):
```bash
docker exec product-trend-celery celery -A tasks.celery_app call tasks.monitoring_tasks.autonomous_health_check
```

Then check the logs:
```bash
docker exec product-trend-backend tail -40 /app/logs/autonomous_fixes.log
```

---

**Last Check:** The agents just ran and are monitoring 2 non-critical issues. Next check in 5 minutes!
