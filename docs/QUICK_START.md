# Quick Start Guide

**Version:** 1.0.0 | **Status:** ✅ ALL SYSTEMS OPERATIONAL | **Last Updated:** 2025-01-19

## 🎉 System Status

✅ **All Docker services running**
✅ **Autonomous monitoring active** (checks every 5 minutes)
✅ **11 AI agents operational** (100% free Groq API)
✅ **Recent bugs fixed** (health monitoring, SQLAlchemy compatibility)

**See [CURRENT_STATUS.md](CURRENT_STATUS.md) for complete details.**

---

## Initial Setup (5 minutes)

### 1. Configure Environment
```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your API keys
notepad .env
```

**Minimum required:**
- At least ONE AI API key (OpenAI OR Anthropic)
- Platform API keys for platforms you want to use

### 2. Start the Application
```bash
# Using the start script (Windows)
start.bat

# OR manually with Docker
docker-compose up -d
```

### 3. Initialize Database
```bash
docker-compose exec backend python -c "from models.database import init_db; init_db()"
```

### 4. Access the Dashboard
Open browser to: http://localhost:3000

---

## Common Commands

### Docker Management
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Rebuild containers
docker-compose up -d --build
```

### Database Management
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d product_trends

# Backup database
docker-compose exec postgres pg_dump -U postgres product_trends > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U postgres product_trends
```

### Celery Management
```bash
# View Celery worker status
docker-compose exec celery celery -A tasks.celery_app status

# Purge all tasks
docker-compose exec celery celery -A tasks.celery_app purge

# View scheduled tasks
docker-compose exec celery celery -A tasks.celery_app inspect scheduled
```

---

## Testing the System

### 🤖 Test Autonomous Monitoring (NEW!)

**Verify the system monitors itself every 5 minutes:**

```bash
# Watch Celery Beat scheduler logs
docker-compose logs -f celery-beat

# You should see every 5 minutes:
# "Sending due task tasks.monitoring_tasks.autonomous_health_check"

# Watch autonomous healing in action
docker-compose logs -f celery

# Look for health check reports
```

**Test the monitoring API:**

```bash
# Check system health
curl http://localhost:8000/api/monitoring/health

# Get monitoring status
curl http://localhost:8000/api/monitoring/status

# Manually trigger a health check
curl -X POST http://localhost:8000/api/monitoring/trigger-check
```

**Expected Output:**
```json
{
  "timestamp": "2025-01-19T...",
  "overall_status": "healthy",
  "checks": {
    "database": {"status": "healthy"},
    "docker": {"status": "healthy"},
    "api": {"status": "healthy"},
    "redis": {"status": "healthy"}
  }
}
```

---

### 1. Manual Trend Scan
```bash
curl -X POST http://localhost:8000/api/trends/scan
```

### 2. Check Products
```bash
curl http://localhost:8000/api/products
```

### 3. View Analytics
```bash
curl http://localhost:8000/api/analytics/dashboard
```

---

## Troubleshooting

### Services won't start
```bash
# Check what's running
docker-compose ps

# Check logs for errors
docker-compose logs backend
docker-compose logs postgres
```

### Can't connect to database
```bash
# Restart PostgreSQL
docker-compose restart postgres

# Check if port 5432 is available
netstat -an | findstr 5432
```

### Frontend errors
```bash
# Rebuild frontend
docker-compose up -d --build frontend

# Check frontend logs
docker-compose logs frontend
```

### API returns errors
```bash
# Check backend logs
docker-compose logs backend

# Verify .env configuration
type .env

# Restart backend
docker-compose restart backend
```

---

## Daily Usage Workflow

1. **Check Dashboard**: http://localhost:3000
2. **Review Pending Products**: Check "Pending Review" tab
3. **Approve/Reject**: Make decisions on each product
4. **Post to Platforms**: Select platforms and post approved items
5. **Monitor Analytics**: Track performance

---

## Stopping the System

```bash
# Stop all services (data persists)
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## Getting Help

1. Check README.md for detailed documentation
2. Check API docs: http://localhost:8000/docs
3. View logs: `docker-compose logs -f`
4. Check platform API documentation for integration issues
