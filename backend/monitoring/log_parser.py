"""
Log parser for error detection
Parses Docker logs, application logs, and Celery logs
"""
import re
import subprocess
from typing import List, Dict
from datetime import datetime, timedelta
from collections import Counter


class LogParser:
    """Parse logs from various sources"""

    # Error patterns to detect - EXPANDED FOR FULL APPLICATION COVERAGE
    ERROR_PATTERNS = {
        # Infrastructure & API Errors
        "api_error": r"(429|500|502|503|504) (Client|Server) Error",
        "database_column_length": r"(value too long for type character varying|StringDataRightTruncation|StringDataTruncation)",
        "model_deprecation": r"(model.*decommissioned|model.*deprecated|no longer supported)",
        "rate_limit": r"429.*Too Many Requests",
        "groq_error": r"Groq API error",
        "hf_error": r"HuggingFace API error",

        # Database Errors
        "database_error": r"(psycopg2\..*Error|DatabaseError|OperationalError|IntegrityError)",
        "database_null_violation": r"(NOT NULL constraint|null value in column)",
        "database_foreign_key": r"(ForeignKeyViolation|foreign key constraint)",
        "database_unique_violation": r"(UniqueViolation|duplicate key value)",

        # Python Code Errors
        "python_exception": r"(Traceback \(most recent call last\)|raise \w+Error|^\w+Error: )",
        "attribute_error": r"AttributeError.*has no attribute",
        "key_error": r"KeyError:",
        "index_error": r"IndexError:",
        "value_error": r"ValueError:",
        "type_error": r"TypeError:",
        "name_error": r"NameError:",
        "zero_division_error": r"ZeroDivisionError:",
        "import_error": r"(ImportError|ModuleNotFoundError)",
        "syntax_error": r"(SyntaxError|IndentationError)",

        # Connection & Network Errors
        "connection_error": r"(ConnectionError|TimeoutError|ConnectionRefusedError)",
        "ssl_error": r"SSLError",
        "dns_error": r"(DNSError|Name or service not known)",

        # Resource Errors
        "memory_error": r"(MemoryError|OutOfMemory)",
        "disk_space_error": r"(No space left on device|Disk quota exceeded)",
        "file_not_found": r"FileNotFoundError",

        # Business Logic Errors
        "validation_error": r"(ValidationError|Invalid.*format|Failed validation)",
        "authentication_error": r"(AuthenticationError|Unauthorized|401|Invalid credentials)",
        "permission_error": r"(PermissionError|Forbidden|403|Access denied)",
        "not_found_error": r"(NotFound|404|does not exist)",

        # Performance Issues
        "slow_query": r"(slow query|query.*exceeded|timeout.*query)",
        "high_cpu": r"(CPU.*high|CPU usage.*%)",
        "high_memory": r"(Memory.*high|Memory usage.*%)",

        # Frontend Errors (from logs/API)
        "frontend_error": r"(React.*Error|Uncaught.*error|Frontend error)",
        "cors_error": r"(CORS|Cross-Origin|blocked by CORS)",

        # Platform API Errors
        "amazon_api_error": r"(Amazon.*error|SP-API.*error)",
        "ebay_api_error": r"(eBay.*error|eBay API)",
        "tiktok_api_error": r"(TikTok.*error|TikTok API)",

        # Data Quality Issues
        "data_corruption": r"(corrupted data|invalid data|malformed)",
        "missing_required_field": r"(missing required|field.*required)",
        "invalid_json_field": r"(is not a function|\.map is not a function|JSON field.*string)",
        "null_string_in_json": r"(ai_keywords.*null|string 'null'|\"null\" instead of null)",
    }

    def __init__(self):
        self.errors_detected = []

    def parse_docker_logs(self, container_name: str, since_minutes: int = 5) -> List[Dict]:
        """Parse Docker container logs for errors"""
        try:
            # Get logs from last N minutes
            result = subprocess.run(
                [
                    "docker", "logs",
                    "--since", f"{since_minutes}m",
                    container_name
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            logs = result.stdout + result.stderr
            return self._extract_errors(logs, source=container_name)

        except Exception as e:
            return [{
                "error": f"Failed to parse logs: {str(e)}",
                "source": container_name,
                "severity": "warning"
            }]

    def _extract_errors(self, log_text: str, source: str) -> List[Dict]:
        """Extract errors from log text"""
        errors = []
        lines = log_text.split("\n")

        for i, line in enumerate(lines):
            for error_type, pattern in self.ERROR_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    error = {
                        "type": error_type,
                        "message": line.strip(),
                        "source": source,
                        "timestamp": datetime.utcnow().isoformat(),
                        "severity": self._determine_severity(error_type),
                        "context": self._get_context(lines, i)
                    }
                    errors.append(error)

        return errors

    def _determine_severity(self, error_type: str) -> str:
        """Determine error severity"""
        critical_errors = ["database_error", "database_column_length", "model_deprecation", "memory_error", "500"]
        warning_errors = ["rate_limit", "429", "connection_error"]

        if error_type in critical_errors:
            return "critical"
        elif error_type in warning_errors:
            return "warning"
        else:
            return "error"

    def _get_context(self, lines: List[str], index: int, context_lines: int = 3) -> List[str]:
        """Get surrounding lines for context"""
        start = max(0, index - context_lines)
        end = min(len(lines), index + context_lines + 1)
        return lines[start:end]

    def analyze_error_patterns(self, errors: List[Dict]) -> Dict:
        """Analyze error patterns to identify recurring issues"""
        if not errors:
            return {"pattern": "no_errors", "count": 0}

        # Count error types (handle missing 'type' key gracefully)
        error_counts = Counter(e.get("type", "unknown") for e in errors)

        # Find most common
        most_common = error_counts.most_common(1)[0]

        # Detect patterns
        pattern_analysis = {
            "total_errors": len(errors),
            "unique_types": len(error_counts),
            "most_common_type": most_common[0],
            "most_common_count": most_common[1],
            "error_distribution": dict(error_counts),
            "severity_breakdown": self._get_severity_breakdown(errors),
            "requires_immediate_action": self._requires_immediate_action(errors)
        }

        return pattern_analysis

    def _get_severity_breakdown(self, errors: List[Dict]) -> Dict:
        """Break down errors by severity"""
        severity_counts = Counter(e.get("severity", "unknown") for e in errors)
        return dict(severity_counts)

    def _requires_immediate_action(self, errors: List[Dict]) -> bool:
        """Determine if errors require immediate action"""
        # Check for critical errors
        critical_count = sum(1 for e in errors if e.get("severity") == "critical")
        if critical_count > 0:
            return True

        # Check for high error rate
        if len(errors) > 50:  # More than 50 errors in 5 minutes
            return True

        # Check for error rate increase
        recent_errors = [e for e in errors if self._is_recent(e, minutes=1)]
        if len(recent_errors) > 20:  # Spike in last minute
            return True

        return False

    def _is_recent(self, error: Dict, minutes: int = 1) -> bool:
        """Check if error is recent"""
        try:
            error_time = datetime.fromisoformat(error["timestamp"])
            cutoff = datetime.utcnow() - timedelta(minutes=minutes)
            return error_time > cutoff
        except:
            return False

    def get_celery_errors(self, since_minutes: int = 5) -> List[Dict]:
        """Get errors from Celery worker logs"""
        return self.parse_docker_logs("product-trend-celery", since_minutes)

    def get_backend_errors(self, since_minutes: int = 5) -> List[Dict]:
        """Get errors from backend API logs"""
        return self.parse_docker_logs("product-trend-backend", since_minutes)

    def get_all_errors(self, since_minutes: int = 5) -> Dict:
        """Get errors from all sources"""
        all_errors = []

        # Get errors from each container
        all_errors.extend(self.get_celery_errors(since_minutes))
        all_errors.extend(self.get_backend_errors(since_minutes))

        # Analyze patterns
        analysis = self.analyze_error_patterns(all_errors)

        return {
            "errors": all_errors,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
