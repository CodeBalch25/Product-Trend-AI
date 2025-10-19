"""
Celery configuration for background tasks
"""
from celery import Celery
from celery.schedules import crontab
from config.settings import settings

# Initialize Celery
celery_app = Celery(
    "product_trend_automation",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Periodic task schedule
celery_app.conf.beat_schedule = {
    'scan-trends-hourly': {
        'task': 'tasks.trend_tasks.scan_trends_task',
        'schedule': crontab(minute=0),  # Every hour
    },
    'analyze-pending-products': {
        'task': 'tasks.analysis_tasks.analyze_pending_products_task',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'sync-platform-listings': {
        'task': 'tasks.platform_tasks.sync_listings_task',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'autonomous-health-check': {
        'task': 'tasks.monitoring_tasks.autonomous_health_check',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes - Autonomous monitoring
    },
}

# Auto-discover tasks
celery_app.autodiscover_tasks([
    'tasks'
])

# Explicitly import tasks to ensure they're registered
from tasks import trend_tasks, analysis_tasks, platform_tasks, monitoring_tasks
