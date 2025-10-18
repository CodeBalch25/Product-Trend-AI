"""
Celery configuration for background tasks
"""
from celery import Celery
from celery.schedules import crontab
from backend.config.settings import settings

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
        'task': 'backend.tasks.trend_tasks.scan_trends_task',
        'schedule': crontab(minute=0),  # Every hour
    },
    'analyze-pending-products': {
        'task': 'backend.tasks.analysis_tasks.analyze_pending_products_task',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'sync-platform-listings': {
        'task': 'backend.tasks.platform_tasks.sync_listings_task',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}

# Auto-discover tasks
celery_app.autodiscover_tasks([
    'backend.tasks'
])
