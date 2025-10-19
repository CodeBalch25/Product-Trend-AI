"""
Alex Thompson - Principal Software Engineer Agent
Generates and implements fixes autonomously
"""
import os
import shutil
from typing import Dict, List
from datetime import datetime


class FixEngineerAgent:
    """
    Alex Thompson - Principal Software Engineer
    Credentials: 15+ years senior engineering at Amazon/Netflix
    Role: Generate and implement code fixes
    """

    def __init__(self):
        self.name = "Alex Thompson"
        self.role = "Fix Engineer"

    def generate_fix(self, root_cause: Dict) -> Dict:
        """Generate fix for identified root cause"""
        print(f"\n{'='*70}")
        print(f"🔧 [{self.role}] {self.name}")
        print(f"   Generating fix for: {root_cause['issue_type']}")
        print(f"{'='*70}\n")

        issue_type = root_cause.get("issue_type")

        if issue_type == "rate_limiting":
            fix = self._generate_rate_limit_fix(root_cause)
        elif issue_type == "database_errors":
            fix = self._generate_database_fix(root_cause)
        elif issue_type == "connection_errors":
            fix = self._generate_connection_fix(root_cause)
        else:
            fix = self._generate_generic_fix(root_cause)

        fix["timestamp"] = datetime.utcnow().isoformat()
        fix["agent"] = self.name

        self._print_fix(fix)

        return fix

    def _generate_rate_limit_fix(self, root_cause: Dict) -> Dict:
        """Generate fix for rate limiting"""
        # Check current delay configuration
        current_delay = self._get_current_delay()

        if current_delay < 1.0:
            # Increase delay
            new_delay = min(current_delay + 0.3, 2.0)

            return {
                "issue_type": "rate_limiting",
                "fix_type": "increase_delay",
                "confidence": 92,
                "actions": [
                    {
                        "action": "increase_api_delay",
                        "file": "services/ai_analysis/agentic_system.py",
                        "change": f"Increase asyncio.sleep from {current_delay}s to {new_delay}s",
                        "current_value": current_delay,
                        "new_value": new_delay
                    }
                ],
                "risk_level": "low",
                "rollback_available": True,
                "auto_apply": True,  # Safe to auto-apply
                "estimated_downtime_seconds": 0
            }
        else:
            # Delay already high, reduce batch size
            return {
                "issue_type": "rate_limiting",
                "fix_type": "reduce_batch_size",
                "confidence": 88,
                "actions": [
                    {
                        "action": "reduce_batch_size",
                        "file": "tasks/analysis_tasks.py",
                        "change": "Reduce batch size from 5 to 3 products",
                        "current_value": 5,
                        "new_value": 3
                    }
                ],
                "risk_level": "low",
                "rollback_available": True,
                "auto_apply": True,
                "estimated_downtime_seconds": 0
            }

    def _generate_database_fix(self, root_cause: Dict) -> Dict:
        """Generate fix for database errors"""
        return {
            "issue_type": "database_errors",
            "fix_type": "increase_timeout_and_retry",
            "confidence": 90,
            "actions": [
                {
                    "action": "increase_connection_timeout",
                    "file": "models/database.py",
                    "change": "Increase connection timeout from 5s to 30s",
                    "current_value": 5,
                    "new_value": 30
                },
                {
                    "action": "add_retry_logic",
                    "file": "models/database.py",
                    "change": "Add retry decorator with 3 attempts",
                    "implementation": "Use tenacity library for retries"
                }
            ],
            "risk_level": "medium",
            "rollback_available": True,
            "auto_apply": True,
            "estimated_downtime_seconds": 10
        }

    def _generate_connection_fix(self, root_cause: Dict) -> Dict:
        """Generate fix for connection errors"""
        return {
            "issue_type": "connection_errors",
            "fix_type": "add_exponential_backoff",
            "confidence": 85,
            "actions": [
                {
                    "action": "add_retry_with_backoff",
                    "file": "services/ai_analysis/agentic_system.py",
                    "change": "Add exponential backoff to API calls",
                    "implementation": "Retry with 1s, 2s, 4s delays"
                }
            ],
            "risk_level": "low",
            "rollback_available": True,
            "auto_apply": True,
            "estimated_downtime_seconds": 0
        }

    def _generate_generic_fix(self, root_cause: Dict) -> Dict:
        """Generate generic fix"""
        return {
            "issue_type": root_cause.get("issue_type"),
            "fix_type": "manual_review_required",
            "confidence": 60,
            "actions": [
                {
                    "action": "log_for_review",
                    "message": "Issue requires manual investigation"
                }
            ],
            "risk_level": "unknown",
            "rollback_available": False,
            "auto_apply": False,  # Don't auto-apply low confidence fixes
            "estimated_downtime_seconds": 0
        }

    def _get_current_delay(self) -> float:
        """Get current asyncio.sleep delay from code"""
        try:
            file_path = "/app/services/ai_analysis/agentic_system.py"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()
                    # Look for asyncio.sleep(X.X)
                    import re
                    match = re.search(r'asyncio\.sleep\((\d+\.?\d*)\)', content)
                    if match:
                        return float(match.group(1))
            return 0.8  # Default
        except:
            return 0.8

    def apply_fix(self, fix: Dict) -> Dict:
        """Apply the fix (with backup)"""
        if not fix.get("auto_apply", False):
            return {
                "status": "skipped",
                "reason": "Fix requires manual approval or low confidence"
            }

        print(f"\n🔧 Applying fix: {fix['fix_type']}")

        try:
            # Create backup first
            backups = self._create_backup(fix)

            # Apply each action
            results = []
            for action in fix["actions"]:
                result = self._apply_action(action)
                results.append(result)

            # Restart affected services if needed
            if any(r.get("restart_required") for r in results):
                self._restart_services(fix)

            return {
                "status": "success",
                "backups": backups,
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            print(f"❌ Fix application failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def _create_backup(self, fix: Dict) -> List[str]:
        """Create backup of files before modification"""
        backups = []
        backup_dir = f"/app/backups/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        try:
            os.makedirs(backup_dir, exist_ok=True)

            for action in fix["actions"]:
                if "file" in action:
                    source_file = f"/app/{action['file']}"
                    if os.path.exists(source_file):
                        backup_file = f"{backup_dir}/{os.path.basename(source_file)}"
                        shutil.copy2(source_file, backup_file)
                        backups.append(backup_file)
                        print(f"   ✓ Backed up: {action['file']}")

        except Exception as e:
            print(f"   ⚠️  Backup warning: {str(e)}")

        return backups

    def _apply_action(self, action: Dict) -> Dict:
        """Apply a single fix action"""
        action_type = action.get("action")

        if action_type == "increase_api_delay":
            return self._apply_delay_increase(action)
        elif action_type == "reduce_batch_size":
            return self._apply_batch_size_reduction(action)
        elif action_type == "increase_connection_timeout":
            return self._apply_timeout_increase(action)
        else:
            return {"status": "skipped", "reason": f"Action type {action_type} not implemented"}

    def _apply_delay_increase(self, action: Dict) -> Dict:
        """Increase asyncio.sleep delay"""
        try:
            file_path = f"/app/{action['file']}"
            old_delay = action['current_value']
            new_delay = action['new_value']

            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()

                # Replace old delay with new delay
                import re
                pattern = f'asyncio\\.sleep\\({old_delay}\\)'
                replacement = f'asyncio.sleep({new_delay})'
                new_content = re.sub(pattern, replacement, content)

                with open(file_path, "w") as f:
                    f.write(new_content)

                print(f"   ✓ Increased delay: {old_delay}s → {new_delay}s")

                return {
                    "status": "success",
                    "action": "increase_api_delay",
                    "restart_required": True
                }
            else:
                return {"status": "error", "reason": "File not found"}

        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def _apply_batch_size_reduction(self, action: Dict) -> Dict:
        """Reduce batch size"""
        try:
            file_path = f"/app/{action['file']}"
            old_size = action['current_value']
            new_size = action['new_value']

            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()

                # Replace .limit(5) with .limit(3)
                import re
                pattern = f'\\.limit\\({old_size}\\)'
                replacement = f'.limit({new_size})'
                new_content = re.sub(pattern, replacement, content)

                with open(file_path, "w") as f:
                    f.write(new_content)

                print(f"   ✓ Reduced batch size: {old_size} → {new_size}")

                return {
                    "status": "success",
                    "action": "reduce_batch_size",
                    "restart_required": True
                }
            else:
                return {"status": "error", "reason": "File not found"}

        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def _apply_timeout_increase(self, action: Dict) -> Dict:
        """Placeholder for timeout increase"""
        print(f"   ⚠️  Action not yet implemented: {action['action']}")
        return {"status": "skipped", "reason": "Not implemented"}

    def _restart_services(self, fix: Dict):
        """Restart affected services"""
        print(f"\n   🔄 Restarting services...")

        try:
            # Restart celery worker
            import subprocess
            subprocess.run(["docker", "restart", "product-trend-celery"], timeout=30)
            print(f"   ✓ Restarted celery worker")

        except Exception as e:
            print(f"   ⚠️  Service restart warning: {str(e)}")

    def _print_fix(self, fix: Dict):
        """Print fix details"""
        print(f"💡 Fix Generated:")
        print(f"   Type: {fix['fix_type']}")
        print(f"   Confidence: {fix['confidence']}%")
        print(f"   Risk Level: {fix['risk_level']}")
        print(f"   Auto-Apply: {'YES' if fix.get('auto_apply') else 'NO'}")
        print(f"   Actions: {len(fix['actions'])}")

        for action in fix['actions']:
            print(f"\n   Action: {action['action']}")
            if 'change' in action:
                print(f"   Change: {action['change']}")

        print(f"\n{'='*70}\n")
