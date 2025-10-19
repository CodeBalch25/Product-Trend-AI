"""
Dr. James Harper, PhD - System Health Monitor Agent
Watches logs, metrics, and health endpoints 24/7
"""
from typing import Dict, List
from datetime import datetime
from monitoring.health_checker import HealthChecker
from monitoring.log_parser import LogParser
from monitoring.metrics_collector import MetricsCollector


class HealthMonitorAgent:
    """
    Dr. James Harper, PhD - System Health Monitor
    Credentials: PhD Computer Science MIT, 15+ years DevOps at Google/Amazon
    Role: 24/7 system monitoring and error detection
    """

    def __init__(self):
        self.name = "Dr. James Harper"
        self.role = "System Health Monitor"
        self.health_checker = HealthChecker()
        self.log_parser = LogParser()
        self.metrics_collector = MetricsCollector()

    def perform_health_check(self) -> Dict:
        """Perform comprehensive health check"""
        print(f"\n{'='*70}")
        print(f"🔍 [{self.role}] {self.name}, PhD")
        print(f"   Performing system health check...")
        print(f"{'='*70}\n")

        # Collect all data
        health_status = self.health_checker.check_all()
        metrics = self.metrics_collector.collect_all_metrics()
        errors = self.log_parser.get_all_errors(since_minutes=5)

        # Analyze
        analysis = self._analyze_system_state(health_status, metrics, errors)

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "health": health_status,
            "metrics": metrics,
            "errors": errors,
            "analysis": analysis,
            "requires_action": analysis["requires_action"]
        }

        # Print summary
        self._print_summary(report)

        return report

    def _analyze_system_state(self, health: Dict, metrics: Dict, errors: Dict) -> Dict:
        """Analyze overall system state"""
        issues = []
        severity = "healthy"

        # Check health status
        if health["overall_status"] == "critical":
            issues.append({
                "type": "health_check_failed",
                "severity": "critical",
                "message": "Critical health check failures detected"
            })
            severity = "critical"

        # Check for errors
        if errors["analysis"].get("requires_immediate_action"):
            issues.append({
                "type": "high_error_rate",
                "severity": "critical",
                "message": f"High error rate: {errors['analysis']['total_errors']} errors in 5 min"
            })
            severity = "critical"

        # Check metrics
        threshold_check = self.metrics_collector.check_thresholds(metrics)
        if threshold_check["has_alerts"]:
            for alert in threshold_check["alerts"]:
                issues.append(alert)
                if alert["severity"] == "critical" and severity != "critical":
                    severity = "critical"

        # Check for specific error patterns
        if errors["analysis"].get("most_common_type") == "rate_limit":
            if errors["analysis"]["most_common_count"] > 20:
                issues.append({
                    "type": "rate_limiting",
                    "severity": "warning",
                    "message": f"Rate limiting detected: {errors['analysis']['most_common_count']} occurrences",
                    "error_type": "rate_limit"
                })

        return {
            "overall_severity": severity,
            "issue_count": len(issues),
            "issues": issues,
            "requires_action": len(issues) > 0,
            "confidence": self._calculate_confidence(issues)
        }

    def _calculate_confidence(self, issues: List[Dict]) -> int:
        """Calculate confidence in diagnosis"""
        if not issues:
            return 100

        # High confidence for known patterns
        known_patterns = ["rate_limiting", "high_error_rate", "high_cpu", "high_memory"]
        known_count = sum(1 for issue in issues if issue["type"] in known_patterns)

        confidence = 70 + (known_count * 10)
        return min(confidence, 100)

    def _print_summary(self, report: Dict):
        """Print health check summary"""
        analysis = report["analysis"]

        print(f"📊 Health Check Summary:")
        print(f"   Overall Status: {analysis['overall_severity'].upper()}")
        print(f"   Issues Found: {analysis['issue_count']}")
        print(f"   Requires Action: {'YES' if analysis['requires_action'] else 'NO'}")
        print(f"   Confidence: {analysis['confidence']}%")

        if analysis["issues"]:
            print(f"\n🐛 Issues Detected:")
            for issue in analysis["issues"]:
                icon = "🔴" if issue["severity"] == "critical" else "🟡"
                print(f"   {icon} [{issue['severity'].upper()}] {issue['message']}")

        print(f"\n{'='*70}\n")

    def get_system_snapshot(self) -> Dict:
        """Get quick system snapshot"""
        return {
            "health": self.health_checker.check_all(),
            "metrics": self.metrics_collector.collect_all_metrics(),
            "timestamp": datetime.utcnow().isoformat()
        }
