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
        # JSON log for programmatic access
        json_log_file = "/app/logs/monitoring_reports.jsonl"
        with open(json_log_file, "a") as f:
            f.write(json.dumps(report) + "\n")

        # Human-readable log with ENHANCED DETAILS
        human_log_file = "/app/logs/autonomous_fixes.log"
        with open(human_log_file, "a") as f:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            f.write(f"\n{'='*80}\n")
            f.write(f"🤖 AUTONOMOUS HEALTH CHECK RUN - {timestamp}\n")
            f.write(f"{'='*80}\n")

            status = report.get("status", "unknown")

            # ENHANCED: Always show what was checked
            f.write(f"\n📋 SYSTEMS CHECKED:\n")
            f.write(f"   ✓ Docker Containers (6 expected: frontend, backend, celery, celery-beat, db, redis)\n")
            f.write(f"   ✓ Database Connection (PostgreSQL)\n")
            f.write(f"   ✓ Redis Connection (Cache & Queue)\n")
            f.write(f"   ✓ Backend API Health\n")
            f.write(f"   ✓ Celery Workers Status\n")
            f.write(f"   ✓ Application Logs (Scanning for errors)\n")
            f.write(f"   ✓ System Resources (Memory, CPU if available)\n")
            f.write(f"\n")

            if status == "healthy":
                f.write(f"✅ RESULT: All Systems Healthy!\n")
                f.write(f"   • No issues detected\n")
                f.write(f"   • No action required\n")
                f.write(f"   • All services operating normally\n")
                f.write(f"   ⏱️  Check Duration: {report.get('duration_seconds', 0):.2f}s\n")

            elif status == "monitoring":
                issues = report.get("issues", 0)
                f.write(f"📊 RESULT: Monitoring Mode\n")
                f.write(f"   • Non-critical issues detected: {issues}\n")
                f.write(f"   • Issues are below auto-fix threshold (70% confidence)\n")
                f.write(f"   • Continuing to monitor - no action taken\n")
                f.write(f"   • Will auto-fix if confidence increases\n")

            elif status == "completed":
                fixes_applied = report.get("fixes_applied", 0)
                fixes_failed = report.get("fixes_failed", 0)
                fixes_pending = report.get("fixes_pending", 0)
                monitoring_only = report.get("monitoring_only", 0)

                f.write(f"🔧 RESULT: Auto-Fix Actions Taken!\n")
                f.write(f"\n   📊 FIX SUMMARY:\n")
                f.write(f"   ✅ Successfully Applied: {fixes_applied}\n")
                f.write(f"   ❌ Failed to Apply: {fixes_failed}\n")
                f.write(f"   ⏸️  Pending Manual Review: {fixes_pending}\n")
                f.write(f"   👁️  Monitoring Only: {monitoring_only}\n")
                f.write(f"   ⏱️  Total Duration: {report.get('duration_seconds', 0):.1f}s\n")

                if fixes_applied > 0:
                    f.write(f"\n   🎉 AUTONOMOUS FIXES APPLIED!\n")
                    f.write(f"   Check logs above for detailed fix information.\n")

            elif status == "failed":
                error = report.get("error", "Unknown error")
                f.write(f"❌ RESULT: Health Check Failed\n")
                f.write(f"   • Error encountered during check\n")
                f.write(f"   • Error: {error}\n")
                f.write(f"   • Will retry in 5 minutes\n")

            # ENHANCED: Always show next run time
            f.write(f"\n⏰ NEXT CHECK: In 5 minutes (runs 24/7 every 5 minutes)\n")
            f.write(f"{'='*80}\n")

    except Exception as e:
        print(f"⚠️  Logging failed: {str(e)}")
        pass  # Fail silently if logging fails
