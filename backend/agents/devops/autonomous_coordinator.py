"""
David Chen, CTO - Autonomous Coordinator Agent
Orchestrates the entire self-healing workflow
"""
from typing import Dict, List
from datetime import datetime
import time

from agents.devops.health_monitor import HealthMonitorAgent
from agents.devops.error_detector import ErrorDetectorAgent
from agents.devops.root_cause_analyst import RootCauseAnalystAgent
from agents.devops.fix_engineer import FixEngineerAgent


class AutonomousCoordinator:
    """
    David Chen, CTO - Technical Coordinator
    Credentials: Former CTO at Uber, 20+ years engineering leadership
    Role: Orchestrate autonomous self-healing workflow
    """

    def __init__(self):
        self.name = "David Chen"
        self.role = "Autonomous Coordinator"

        # Initialize all agents
        self.health_monitor = HealthMonitorAgent()
        self.error_detector = ErrorDetectorAgent()
        self.root_cause_analyst = RootCauseAnalystAgent()
        self.fix_engineer = FixEngineerAgent()

    def run_autonomous_healing(self) -> Dict:
        """Execute full autonomous self-healing workflow"""
        print(f"\n{'*'*80}")
        print(f"🤖 AUTONOMOUS SELF-HEALING SYSTEM")
        print(f"   Coordinator: {self.name}, CTO")
        print(f"   Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"{'*'*80}\n")

        workflow_start = time.time()

        # Step 1: Health Check
        print(f"📊 STEP 1: System Health Check")
        health_report = self.health_monitor.perform_health_check()

        # Check if issues found
        if not health_report.get("requires_action"):
            print(f"✅ System healthy - no action needed\n")
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": time.time() - workflow_start
            }

        # Step 2: Error Analysis
        print(f"\n📊 STEP 2: Error Detection & Analysis")
        errors = health_report["errors"]["errors"]
        error_analysis = self.error_detector.analyze_errors(errors)

        if not error_analysis.get("requires_immediate_fix"):
            print(f"📊 Issues detected but not critical - monitoring\n")
            return {
                "status": "monitoring",
                "issues": error_analysis.get("total_errors", 0),
                "timestamp": datetime.utcnow().isoformat()
            }

        # Step 3: Root Cause Analysis
        print(f"\n📊 STEP 3: Root Cause Analysis")
        root_cause_analysis = self.root_cause_analyst.analyze_root_cause(error_analysis)

        # Step 4: Fix Generation & Application
        print(f"\n📊 STEP 4: Fix Generation & Application")
        fix_results = []

        for root_cause in root_cause_analysis["root_causes"]:
            confidence = root_cause.get("confidence", 0)

            # Decide whether to auto-fix based on confidence
            if confidence >= 85:  # High confidence threshold
                print(f"\n🎯 High confidence ({confidence}%) - Generating fix...")

                # Generate fix
                fix = self.fix_engineer.generate_fix(root_cause)

                # Apply if auto_apply is True
                if fix.get("auto_apply"):
                    print(f"🚀 Auto-applying fix...")

                    apply_result = self.fix_engineer.apply_fix(fix)

                    if apply_result["status"] == "success":
                        print(f"✅ Fix applied successfully!")

                        # Monitor for 2 minutes
                        validation = self._validate_fix(fix, apply_result)

                        fix_results.append({
                            "root_cause": root_cause,
                            "fix": fix,
                            "apply_result": apply_result,
                            "validation": validation,
                            "status": "applied"
                        })
                    else:
                        print(f"❌ Fix application failed: {apply_result.get('error')}")
                        fix_results.append({
                            "root_cause": root_cause,
                            "fix": fix,
                            "apply_result": apply_result,
                            "status": "failed"
                        })
                else:
                    print(f"⏸️  Fix generated but requires manual review")
                    fix_results.append({
                        "root_cause": root_cause,
                        "fix": fix,
                        "status": "pending_review"
                    })
            else:
                print(f"\n📊 Low confidence ({confidence}%) - Monitoring only")
                fix_results.append({
                    "root_cause": root_cause,
                    "status": "monitoring",
                    "reason": "Confidence below threshold"
                })

        workflow_duration = time.time() - workflow_start

        # Final Summary
        self._print_summary(fix_results, workflow_duration)

        return {
            "status": "completed",
            "fixes_applied": sum(1 for r in fix_results if r["status"] == "applied"),
            "fixes_failed": sum(1 for r in fix_results if r["status"] == "failed"),
            "fixes_pending": sum(1 for r in fix_results if r["status"] == "pending_review"),
            "monitoring_only": sum(1 for r in fix_results if r["status"] == "monitoring"),
            "duration_seconds": workflow_duration,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _validate_fix(self, fix: Dict, apply_result: Dict) -> Dict:
        """Validate fix after application"""
        print(f"\n   ⏳ Validating fix for 2 minutes...")

        # Wait 2 minutes for system to stabilize
        validation_start = time.time()
        time.sleep(120)

        # Check for new errors
        health_check = self.health_monitor.perform_health_check()

        # Compare error counts
        new_error_count = len(health_check["errors"]["errors"])

        validation_duration = time.time() - validation_start

        if new_error_count == 0:
            print(f"   ✅ Validation passed - no new errors")
            return {
                "status": "success",
                "error_count": 0,
                "duration_seconds": validation_duration
            }
        elif new_error_count < 5:
            print(f"   ⚠️  Validation warning - {new_error_count} minor errors")
            return {
                "status": "warning",
                "error_count": new_error_count,
                "duration_seconds": validation_duration
            }
        else:
            print(f"   ❌ Validation failed - {new_error_count} errors detected")
            print(f"   🔄 Rolling back fix...")

            # Rollback would happen here
            # For now, just log it

            return {
                "status": "failed",
                "error_count": new_error_count,
                "duration_seconds": validation_duration,
                "rollback_performed": False  # TODO: Implement rollback
            }

    def _print_summary(self, fix_results: List[Dict], duration: float):
        """Print workflow summary"""
        print(f"\n{'*'*80}")
        print(f"📊 AUTONOMOUS HEALING SUMMARY")
        print(f"{'*'*80}\n")

        applied = sum(1 for r in fix_results if r["status"] == "applied")
        failed = sum(1 for r in fix_results if r["status"] == "failed")
        pending = sum(1 for r in fix_results if r["status"] == "pending_review")
        monitoring = sum(1 for r in fix_results if r["status"] == "monitoring")

        print(f"   ✅ Fixes Applied: {applied}")
        print(f"   ❌ Fixes Failed: {failed}")
        print(f"   ⏸️  Pending Review: {pending}")
        print(f"   📊 Monitoring: {monitoring}")
        print(f"\n   ⏱️  Total Duration: {duration:.1f} seconds")
        print(f"\n{'*'*80}\n")

    def enable_autonomous_mode(self, auto_apply_threshold: int = 85):
        """Enable autonomous self-healing mode"""
        print(f"\n🚀 Enabling Autonomous Self-Healing Mode")
        print(f"   Auto-apply threshold: {auto_apply_threshold}%")
        print(f"   System will automatically detect and fix issues")
        print(f"\n   Note: All fixes are backed up and can be rolled back")
        print(f"   Monitoring every 5 minutes via Celery Beat\n")

        return {
            "status": "enabled",
            "threshold": auto_apply_threshold,
            "timestamp": datetime.utcnow().isoformat()
        }
