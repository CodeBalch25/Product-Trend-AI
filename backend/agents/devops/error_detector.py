"""
Sarah Mitchell, MS - Error Detection Specialist Agent
Analyzes error patterns and categorizes issues
"""
import re
from typing import Dict, List
from datetime import datetime


class ErrorDetectorAgent:
    """
    Sarah Mitchell, MS - Error Detection Specialist
    Credentials: MS Data Science NYU, 10+ years error analysis at Netflix
    Role: Error pattern detection and categorization
    """

    def __init__(self):
        self.name = "Sarah Mitchell"
        self.role = "Error Detection Specialist"

    def analyze_errors(self, errors: List[Dict]) -> Dict:
        """Analyze and categorize errors"""
        if not errors:
            return {
                "status": "no_errors",
                "categories": {},
                "priority_issues": []
            }

        print(f"\n{'='*70}")
        print(f"🔍 [{self.role}] {self.name}, MS")
        print(f"   Analyzing {len(errors)} errors...")
        print(f"{'='*70}\n")

        # Categorize errors
        categorized = self._categorize_errors(errors)

        # Find patterns
        patterns = self._find_patterns(errors)

        # Prioritize issues
        priority_issues = self._prioritize_issues(categorized, patterns)

        # Suggest fixes
        suggested_fixes = self._suggest_fixes(priority_issues)

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "total_errors": len(errors),
            "categories": categorized,
            "patterns": patterns,
            "priority_issues": priority_issues,
            "suggested_fixes": suggested_fixes,
            "requires_immediate_fix": len(priority_issues) > 0
        }

        self._print_analysis(result)

        return result

    def _categorize_errors(self, errors: List[Dict]) -> Dict:
        """Categorize errors by type"""
        categories = {
            "api_errors": [],
            "rate_limiting": [],
            "database_errors": [],
            "code_errors": [],
            "connection_errors": [],
            "unknown": []
        }

        for error in errors:
            error_type = error.get("type", "unknown")

            if "rate_limit" in error_type or "429" in error_type:
                categories["rate_limiting"].append(error)
            elif "api_error" in error_type:
                categories["api_errors"].append(error)
            elif "database" in error_type:
                categories["database_errors"].append(error)
            elif "connection" in error_type:
                categories["connection_errors"].append(error)
            elif any(x in error_type for x in ["exception", "syntax", "import"]):
                categories["code_errors"].append(error)
            else:
                categories["unknown"].append(error)

        return {k: len(v) for k, v in categories.items() if v}

    def _find_patterns(self, errors: List[Dict]) -> List[Dict]:
        """Find recurring error patterns"""
        patterns = []

        # Group by error message similarity
        message_groups = {}
        for error in errors:
            # Extract key parts of error message
            msg = error.get("message", "")

            # Find base pattern
            base_pattern = self._extract_base_pattern(msg)

            if base_pattern not in message_groups:
                message_groups[base_pattern] = []

            message_groups[base_pattern].append(error)

        # Find patterns that occur multiple times
        for pattern, occurrences in message_groups.items():
            if len(occurrences) >= 3:  # Pattern appears 3+ times
                patterns.append({
                    "pattern": pattern,
                    "occurrences": len(occurrences),
                    "severity": occurrences[0].get("severity", "error"),
                    "first_seen": occurrences[0].get("timestamp"),
                    "last_seen": occurrences[-1].get("timestamp")
                })

        return sorted(patterns, key=lambda x: x["occurrences"], reverse=True)

    def _extract_base_pattern(self, message: str) -> str:
        """Extract base error pattern from message"""
        # Remove specific values (numbers, URLs, etc.)
        pattern = re.sub(r'\d+', 'N', message)
        pattern = re.sub(r'http[s]?://\S+', 'URL', pattern)
        pattern = re.sub(r'/[/\w\-\.]+', 'PATH', pattern)

        # Keep first 100 chars
        return pattern[:100]

    def _prioritize_issues(self, categories: Dict, patterns: List[Dict]) -> List[Dict]:
        """Prioritize issues that need fixing"""
        priority_issues = []

        # High priority: Rate limiting
        if categories.get("rate_limiting", 0) > 10:
            priority_issues.append({
                "type": "rate_limiting",
                "severity": "high",
                "count": categories["rate_limiting"],
                "confidence": 95,
                "fix_type": "configuration",
                "description": f"Rate limiting detected: {categories['rate_limiting']} occurrences"
            })

        # High priority: Database errors
        if categories.get("database_errors", 0) > 5:
            priority_issues.append({
                "type": "database_errors",
                "severity": "critical",
                "count": categories["database_errors"],
                "confidence": 90,
                "fix_type": "connection",
                "description": f"Database errors: {categories['database_errors']} occurrences"
            })

        # Medium priority: Connection errors
        if categories.get("connection_errors", 0) > 10:
            priority_issues.append({
                "type": "connection_errors",
                "severity": "medium",
                "count": categories["connection_errors"],
                "confidence": 85,
                "fix_type": "retry_logic",
                "description": f"Connection errors: {categories['connection_errors']} occurrences"
            })

        # Recurring patterns
        for pattern in patterns:
            if pattern["occurrences"] > 10:
                priority_issues.append({
                    "type": "recurring_pattern",
                    "severity": "medium",
                    "pattern": pattern["pattern"],
                    "count": pattern["occurrences"],
                    "confidence": 80,
                    "fix_type": "code_fix",
                    "description": f"Recurring error pattern: {pattern['occurrences']} times"
                })

        return sorted(priority_issues, key=lambda x: x["count"], reverse=True)

    def _suggest_fixes(self, priority_issues: List[Dict]) -> List[Dict]:
        """Suggest potential fixes"""
        fixes = []

        for issue in priority_issues:
            if issue["type"] == "rate_limiting":
                fixes.append({
                    "issue_type": "rate_limiting",
                    "confidence": 95,
                    "fix_description": "Add delays between API calls",
                    "fix_actions": [
                        "Change parallel processing to sequential",
                        "Add 0.8-1.0 second delays between agent calls",
                        "Implement exponential backoff",
                        "Add retry logic with delays"
                    ],
                    "estimated_time_minutes": 10,
                    "risk_level": "low"
                })

            elif issue["type"] == "database_errors":
                fixes.append({
                    "issue_type": "database_errors",
                    "confidence": 90,
                    "fix_description": "Improve database connection handling",
                    "fix_actions": [
                        "Increase connection timeout",
                        "Add connection retry logic",
                        "Implement connection pooling",
                        "Add error handling"
                    ],
                    "estimated_time_minutes": 15,
                    "risk_level": "medium"
                })

            elif issue["type"] == "connection_errors":
                fixes.append({
                    "issue_type": "connection_errors",
                    "confidence": 85,
                    "fix_description": "Add retry logic for failed connections",
                    "fix_actions": [
                        "Implement exponential backoff",
                        "Add connection timeout handling",
                        "Add circuit breaker pattern",
                        "Log connection failures"
                    ],
                    "estimated_time_minutes": 12,
                    "risk_level": "low"
                })

        return fixes

    def _print_analysis(self, result: Dict):
        """Print analysis summary"""
        print(f"📊 Error Analysis:")
        print(f"   Total Errors: {result['total_errors']}")
        print(f"   Categories: {len(result['categories'])}")
        print(f"   Patterns Found: {len(result['patterns'])}")
        print(f"   Priority Issues: {len(result['priority_issues'])}")

        if result['priority_issues']:
            print(f"\n🎯 Top Priority Issues:")
            for issue in result['priority_issues'][:3]:
                print(f"   • [{issue['severity'].upper()}] {issue['description']}")
                print(f"     Confidence: {issue['confidence']}%, Count: {issue['count']}")

        if result['suggested_fixes']:
            print(f"\n💡 Suggested Fixes:")
            for fix in result['suggested_fixes'][:2]:
                print(f"   • {fix['fix_description']}")
                print(f"     Confidence: {fix['confidence']}%, Risk: {fix['risk_level']}")

        print(f"\n{'='*70}\n")
