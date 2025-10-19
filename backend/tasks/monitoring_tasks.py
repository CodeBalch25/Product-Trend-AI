"""
Celery tasks for autonomous system monitoring and self-healing
Runs every 5 minutes to detect and fix issues automatically
"""
from tasks.celery_app import celery_app
from agents.devops.autonomous_coordinator import AutonomousCoordinator
from datetime import datetime
import json


@celery_app.task(name='tasks.monitoring_tasks.autonomous_health_check')
def autonomous_health_check():
    """
    Autonomous health check and self-healing
    Runs every 5 minutes - detects and fixes issues automatically
    """
    try:
        # Run full autonomous healing workflow
        coordinator = AutonomousCoordinator()
        result = coordinator.run_autonomous_healing()

        # Log result
        log_monitoring_report(result)

        return result

    except Exception as e:
        print(f"❌ Autonomous healing failed: {str(e)}\n")
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


def log_monitoring_report(report: dict):
    """Log monitoring report to file for review"""
    try:
        log_file = "/app/logs/monitoring_reports.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(report) + "\n")
    except:
        pass  # Fail silently if logging fails
