"""
Dr. Marcus Chen, PhD - Root Cause Analyst Agent
Deep dive investigation into why errors occurred
"""
import os
import subprocess
from typing import Dict, List
from datetime import datetime


class RootCauseAnalystAgent:
    """
    Dr. Marcus Chen, PhD - Root Cause Analyst
    Credentials: PhD Computer Science Stanford, 12+ years Site Reliability at Google
    Role: Deep root cause analysis and diagnosis
    """

    def __init__(self):
        self.name = "Dr. Marcus Chen"
        self.role = "Root Cause Analyst"

    def analyze_root_cause(self, error_analysis: Dict) -> Dict:
        """Perform deep root cause analysis"""
        print(f"\n{'='*70}")
        print(f"🔬 [{self.role}] {self.name}, PhD")
        print(f"   Performing root cause analysis...")
        print(f"{'='*70}\n")

        priority_issues = error_analysis.get("priority_issues", [])

        if not priority_issues:
            return {
                "status": "no_issues",
                "root_causes": []
            }

        root_causes = []

        for issue in priority_issues:
            root_cause = self._diagnose_issue(issue)
            root_causes.append(root_cause)

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "root_causes": root_causes,
            "confidence": self._calculate_overall_confidence(root_causes)
        }

        self._print_analysis(result)

        return result

    def _diagnose_issue(self, issue: Dict) -> Dict:
        """Diagnose specific issue"""
        issue_type = issue.get("type")

        if issue_type == "database_column_length":
            return self._diagnose_database_column_length(issue)
        elif issue_type == "model_deprecation":
            return self._diagnose_model_deprecation(issue)
        elif issue_type == "rate_limiting":
            return self._diagnose_rate_limiting(issue)
        elif issue_type == "database_errors":
            return self._diagnose_database_errors(issue)
        elif issue_type == "connection_errors":
            return self._diagnose_connection_errors(issue)
        elif issue_type == "recurring_pattern":
            return self._diagnose_recurring_pattern(issue)
        elif issue_type == "data_corruption":
            return self._diagnose_data_corruption(issue)
        else:
            return self._diagnose_generic(issue)

    def _diagnose_database_column_length(self, issue: Dict) -> Dict:
        """Diagnose PostgreSQL column length issues"""
        return {
            "issue_type": "database_column_length",
            "root_cause": "Database VARCHAR column size insufficient for AI-generated content",
            "evidence": [
                f"{issue.get('count')} products failing with StringDataRightTruncation",
                "PostgreSQL error: value too long for type character varying(50)",
                "AI agents generating content exceeding 50 characters"
            ],
            "confidence": 98,
            "fix_category": "database_schema",
            "affected_component": "PostgreSQL products table",
            "fix_priority": "critical",
            "estimated_fix_time_minutes": 2
        }

    def _diagnose_model_deprecation(self, issue: Dict) -> Dict:
        """Diagnose AI model deprecation issues"""
        return {
            "issue_type": "model_deprecation",
            "root_cause": "AI model has been decommissioned by provider",
            "evidence": [
                f"{issue.get('count')} API calls failing with 404/400 errors",
                "Model marked as 'decommissioned' or 'deprecated'",
                "Provider removed model from available endpoints"
            ],
            "confidence": 95,
            "fix_category": "model_upgrade",
            "affected_component": "agentic_system.py model configuration",
            "fix_priority": "critical",
            "estimated_fix_time_minutes": 5
        }

    def _diagnose_rate_limiting(self, issue: Dict) -> Dict:
        """Diagnose rate limiting issues"""
        # Check if sequential processing is enabled
        sequential_enabled = self._check_sequential_processing()

        if not sequential_enabled:
            return {
                "issue_type": "rate_limiting",
                "root_cause": "Parallel API calls overwhelming rate limits",
                "evidence": [
                    "High volume of 429 errors",
                    "Parallel processing using asyncio.gather()",
                    f"{issue.get('count')} rate limit errors detected"
                ],
                "confidence": 95,
                "fix_category": "configuration",
                "affected_component": "agentic_system.py",
                "fix_priority": "high",
                "estimated_fix_time_minutes": 10
            }
        else:
            return {
                "issue_type": "rate_limiting",
                "root_cause": "Delays too short or batch size too large",
                "evidence": [
                    "Sequential processing enabled but still hitting limits",
                    f"{issue.get('count')} rate limit errors",
                    "May need longer delays or smaller batches"
                ],
                "confidence": 85,
                "fix_category": "configuration_tuning",
                "affected_component": "agentic_system.py or analysis_tasks.py",
                "fix_priority": "medium",
                "estimated_fix_time_minutes": 5
            }

    def _diagnose_database_errors(self, issue: Dict) -> Dict:
        """Diagnose database connection issues"""
        return {
            "issue_type": "database_errors",
            "root_cause": "Database connection timeout or connection pool exhaustion",
            "evidence": [
                f"{issue.get('count')} database errors detected",
                "Likely timeout or connection limit issues",
                "May need connection pooling or timeout increases"
            ],
            "confidence": 90,
            "fix_category": "configuration",
            "affected_component": "database.py",
            "fix_priority": "high",
            "estimated_fix_time_minutes": 15
        }

    def _diagnose_connection_errors(self, issue: Dict) -> Dict:
        """Diagnose connection errors"""
        return {
            "issue_type": "connection_errors",
            "root_cause": "Network instability or missing retry logic",
            "evidence": [
                f"{issue.get('count')} connection errors",
                "May need retry logic with exponential backoff",
                "Connection timeout may be too short"
            ],
            "confidence": 85,
            "fix_category": "code_enhancement",
            "affected_component": "API client code",
            "fix_priority": "medium",
            "estimated_fix_time_minutes": 12
        }

    def _diagnose_recurring_pattern(self, issue: Dict) -> Dict:
        """Diagnose recurring error pattern"""
        pattern = issue.get("pattern", "Unknown pattern")

        return {
            "issue_type": "recurring_pattern",
            "root_cause": "Systematic error in code logic",
            "evidence": [
                f"Pattern repeating {issue.get('count')} times",
                f"Pattern: {pattern[:100]}",
                "Indicates code-level issue"
            ],
            "confidence": 75,
            "fix_category": "code_fix",
            "affected_component": "Unknown - requires code inspection",
            "fix_priority": "medium",
            "estimated_fix_time_minutes": 20
        }

    def _diagnose_data_corruption(self, issue: Dict) -> Dict:
        """Diagnose data corruption issues (e.g., string 'null' in JSON fields)"""
        return {
            "issue_type": "data_corruption",
            "root_cause": "JSON fields storing string 'null' instead of actual NULL values",
            "evidence": [
                f"{issue.get('count')} frontend errors from corrupted JSON fields",
                "Frontend trying to call .map() on string instead of array",
                "Backend storing string 'null' instead of NULL in database"
            ],
            "confidence": 85,
            "fix_category": "data_cleanup",
            "affected_component": "Database products table (ai_keywords, ai_description, ai_category)",
            "fix_priority": "high",
            "estimated_fix_time_minutes": 10
        }

    def _diagnose_generic(self, issue: Dict) -> Dict:
        """Generic diagnosis for unknown issues"""
        return {
            "issue_type": issue.get("type", "unknown"),
            "root_cause": "Issue requires further investigation",
            "evidence": [
                f"Issue count: {issue.get('count', 0)}",
                "Pattern not yet recognized"
            ],
            "confidence": 60,
            "fix_category": "investigation_needed",
            "affected_component": "Unknown",
            "fix_priority": "low",
            "estimated_fix_time_minutes": 30
        }

    def _check_sequential_processing(self) -> bool:
        """Check if sequential processing is enabled"""
        try:
            file_path = "/app/services/ai_analysis/agentic_system.py"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()
                    return "await asyncio.sleep" in content and "asyncio.gather" not in content
            return False
        except:
            return False

    def _calculate_overall_confidence(self, root_causes: List[Dict]) -> int:
        """Calculate overall confidence in diagnosis"""
        if not root_causes:
            return 0

        avg_confidence = sum(rc.get("confidence", 0) for rc in root_causes) / len(root_causes)
        return int(avg_confidence)

    def _print_analysis(self, result: Dict):
        """Print root cause analysis"""
        print(f"🔍 Root Cause Analysis:")
        print(f"   Total Issues Analyzed: {len(result['root_causes'])}")
        print(f"   Overall Confidence: {result['confidence']}%")

        if result['root_causes']:
            print(f"\n📋 Root Causes Identified:")
            for rc in result['root_causes']:
                print(f"\n   Issue: {rc['issue_type']}")
                print(f"   Root Cause: {rc['root_cause']}")
                print(f"   Confidence: {rc['confidence']}%")
                print(f"   Priority: {rc['fix_priority'].upper()}")
                print(f"   Est. Fix Time: {rc['estimated_fix_time_minutes']} minutes")

        print(f"\n{'='*70}\n")
