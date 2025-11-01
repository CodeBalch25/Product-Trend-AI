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
        """Categorize errors by type - EXPANDED FOR FULL APPLICATION COVERAGE"""
        categories = {
            # Infrastructure & API
            "api_errors": [],
            "model_deprecation": [],
            "database_column_length": [],
            "rate_limiting": [],

            # Database
            "database_errors": [],
            "database_null_violation": [],
            "database_foreign_key": [],
            "database_unique_violation": [],

            # Code Errors
            "code_errors": [],
            "attribute_errors": [],
            "key_errors": [],
            "index_errors": [],
            "value_errors": [],
            "type_errors": [],
            "import_errors": [],

            # Connection & Network
            "connection_errors": [],
            "ssl_errors": [],
            "dns_errors": [],

            # Resource Issues
            "memory_errors": [],
            "disk_space_errors": [],
            "file_not_found": [],

            # Business Logic
            "validation_errors": [],
            "authentication_errors": [],
            "permission_errors": [],
            "not_found_errors": [],

            # Performance
            "slow_queries": [],
            "high_cpu": [],
            "high_memory": [],

            # Frontend
            "frontend_errors": [],
            "cors_errors": [],

            # Platform APIs
            "amazon_api_errors": [],
            "ebay_api_errors": [],
            "tiktok_api_errors": [],

            # Data Quality
            "data_corruption": [],
            "missing_required_fields": [],

            "unknown": []
        }

        for error in errors:
            error_type = error.get("type", "unknown")
            error_msg = error.get("message", "").lower()

            # Categorize based on error type with comprehensive mapping
            categorized = False

            # Database errors
            if "database_column_length" in error_type:
                categories["database_column_length"].append(error)
                categorized = True
            elif "database_null_violation" in error_type or "null value in column" in error_msg:
                categories["database_null_violation"].append(error)
                categorized = True
            elif "database_foreign_key" in error_type or "foreign key" in error_msg:
                categories["database_foreign_key"].append(error)
                categorized = True
            elif "database_unique_violation" in error_type or "duplicate key" in error_msg:
                categories["database_unique_violation"].append(error)
                categorized = True
            elif "database_error" in error_type or "database" in error_type:
                categories["database_errors"].append(error)
                categorized = True

            # Model/API errors
            elif "model_deprecation" in error_type:
                categories["model_deprecation"].append(error)
                categorized = True
            elif "rate_limit" in error_type or "429" in error_type:
                categories["rate_limiting"].append(error)
                categorized = True
            elif "api_error" in error_type:
                categories["api_errors"].append(error)
                categorized = True

            # Python code errors
            elif "attribute_error" in error_type:
                categories["attribute_errors"].append(error)
                categorized = True
            elif "key_error" in error_type:
                categories["key_errors"].append(error)
                categorized = True
            elif "index_error" in error_type:
                categories["index_errors"].append(error)
                categorized = True
            elif "value_error" in error_type:
                categories["value_errors"].append(error)
                categorized = True
            elif "type_error" in error_type:
                categories["type_errors"].append(error)
                categorized = True
            elif "import_error" in error_type:
                categories["import_errors"].append(error)
                categorized = True

            # Connection errors
            elif "ssl_error" in error_type:
                categories["ssl_errors"].append(error)
                categorized = True
            elif "dns_error" in error_type:
                categories["dns_errors"].append(error)
                categorized = True
            elif "connection_error" in error_type:
                categories["connection_errors"].append(error)
                categorized = True

            # Resource errors
            elif "memory_error" in error_type:
                categories["memory_errors"].append(error)
                categorized = True
            elif "disk_space_error" in error_type:
                categories["disk_space_errors"].append(error)
                categorized = True
            elif "file_not_found" in error_type:
                categories["file_not_found"].append(error)
                categorized = True

            # Business logic
            elif "validation_error" in error_type:
                categories["validation_errors"].append(error)
                categorized = True
            elif "authentication_error" in error_type or "401" in error_msg:
                categories["authentication_errors"].append(error)
                categorized = True
            elif "permission_error" in error_type or "403" in error_msg:
                categories["permission_errors"].append(error)
                categorized = True
            elif "not_found_error" in error_type:
                categories["not_found_errors"].append(error)
                categorized = True

            # Performance
            elif "slow_query" in error_type:
                categories["slow_queries"].append(error)
                categorized = True
            elif "high_cpu" in error_type:
                categories["high_cpu"].append(error)
                categorized = True
            elif "high_memory" in error_type:
                categories["high_memory"].append(error)
                categorized = True

            # Frontend
            elif "frontend_error" in error_type:
                categories["frontend_errors"].append(error)
                categorized = True
            elif "cors_error" in error_type:
                categories["cors_errors"].append(error)
                categorized = True

            # Platform APIs
            elif "amazon_api_error" in error_type:
                categories["amazon_api_errors"].append(error)
                categorized = True
            elif "ebay_api_error" in error_type:
                categories["ebay_api_errors"].append(error)
                categorized = True
            elif "tiktok_api_error" in error_type:
                categories["tiktok_api_errors"].append(error)
                categorized = True

            # Data quality
            elif "data_corruption" in error_type:
                categories["data_corruption"].append(error)
                categorized = True
            elif "missing_required_field" in error_type:
                categories["missing_required_fields"].append(error)
                categorized = True
            elif "invalid_json_field" in error_type or "map is not a function" in error_msg:
                categories["data_corruption"].append(error)
                categorized = True
            elif "null_string_in_json" in error_type:
                categories["data_corruption"].append(error)
                categorized = True

            # Fallback to code errors or unknown
            elif not categorized:
                if any(x in error_type for x in ["exception", "syntax", "error"]):
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

        # CRITICAL priority: Database column length (blocking product analysis)
        if categories.get("database_column_length", 0) > 0:
            priority_issues.append({
                "type": "database_column_length",
                "severity": "critical",
                "count": categories["database_column_length"],
                "confidence": 98,
                "fix_type": "increase_column_length",
                "description": f"Database column too short: {categories['database_column_length']} products failing to save"
            })

        # CRITICAL priority: Model deprecation (breaks core functionality)
        if categories.get("model_deprecation", 0) > 0:
            priority_issues.append({
                "type": "model_deprecation",
                "severity": "critical",
                "count": categories["model_deprecation"],
                "confidence": 95,
                "fix_type": "model_upgrade",
                "description": f"Model deprecation detected: {categories['model_deprecation']} AI agents failing"
            })

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

        # ========== EXPANDED ERROR HANDLING ==========

        # Database constraint violations
        if categories.get("database_null_violation", 0) > 0:
            priority_issues.append({
                "type": "database_null_violation",
                "severity": "high",
                "count": categories["database_null_violation"],
                "confidence": 90,
                "fix_type": "add_default_values",
                "description": f"NULL constraint violations: {categories['database_null_violation']} occurrences"
            })

        if categories.get("database_unique_violation", 0) > 3:
            priority_issues.append({
                "type": "database_unique_violation",
                "severity": "high",
                "count": categories["database_unique_violation"],
                "confidence": 85,
                "fix_type": "add_duplicate_check",
                "description": f"Duplicate key violations: {categories['database_unique_violation']} occurrences"
            })

        # Python code errors (common ones)
        if categories.get("attribute_errors", 0) > 5:
            priority_issues.append({
                "type": "attribute_errors",
                "severity": "high",
                "count": categories["attribute_errors"],
                "confidence": 80,
                "fix_type": "add_attribute_check",
                "description": f"AttributeError: {categories['attribute_errors']} occurrences"
            })

        if categories.get("key_errors", 0) > 5:
            priority_issues.append({
                "type": "key_errors",
                "severity": "high",
                "count": categories["key_errors"],
                "confidence": 80,
                "fix_type": "add_dict_get",
                "description": f"KeyError: {categories['key_errors']} occurrences"
            })

        if categories.get("import_errors", 0) > 0:
            priority_issues.append({
                "type": "import_errors",
                "severity": "critical",
                "count": categories["import_errors"],
                "confidence": 95,
                "fix_type": "install_dependency",
                "description": f"Import errors: {categories['import_errors']} missing modules"
            })

        # CORS errors (frontend)
        if categories.get("cors_errors", 0) > 5:
            priority_issues.append({
                "type": "cors_errors",
                "severity": "high",
                "count": categories["cors_errors"],
                "confidence": 90,
                "fix_type": "update_cors_config",
                "description": f"CORS errors: {categories['cors_errors']} blocked requests"
            })

        # Validation errors
        if categories.get("validation_errors", 0) > 10:
            priority_issues.append({
                "type": "validation_errors",
                "severity": "medium",
                "count": categories["validation_errors"],
                "confidence": 75,
                "fix_type": "improve_validation",
                "description": f"Validation failures: {categories['validation_errors']} occurrences"
            })

        # File not found errors
        if categories.get("file_not_found", 0) > 3:
            priority_issues.append({
                "type": "file_not_found",
                "severity": "high",
                "count": categories["file_not_found"],
                "confidence": 85,
                "fix_type": "create_missing_files",
                "description": f"File not found: {categories['file_not_found']} missing files"
            })

        # Performance issues
        if categories.get("slow_queries", 0) > 5:
            priority_issues.append({
                "type": "slow_queries",
                "severity": "medium",
                "count": categories["slow_queries"],
                "confidence": 75,
                "fix_type": "optimize_query",
                "description": f"Slow queries detected: {categories['slow_queries']} occurrences"
            })

        # Data quality issues
        if categories.get("missing_required_fields", 0) > 5:
            priority_issues.append({
                "type": "missing_required_fields",
                "severity": "high",
                "count": categories["missing_required_fields"],
                "confidence": 80,
                "fix_type": "add_field_defaults",
                "description": f"Missing required fields: {categories['missing_required_fields']} occurrences"
            })

        if categories.get("data_corruption", 0) > 3:
            priority_issues.append({
                "type": "data_corruption",
                "severity": "high",
                "count": categories["data_corruption"],
                "confidence": 85,
                "fix_type": "clean_corrupt_data",
                "description": f"Data corruption detected: {categories['data_corruption']} occurrences (e.g., string 'null' instead of NULL)"
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
            if issue["type"] == "database_column_length":
                fixes.append({
                    "issue_type": "database_column_length",
                    "confidence": 98,
                    "fix_description": "Increase database column size to accommodate data",
                    "fix_actions": [
                        "Parse error to find table and column name",
                        "Detect current column length",
                        "Calculate required length from failed data",
                        "ALTER TABLE to increase column size",
                        "Restart backend to clear cached schema",
                        "Retry failed product analysis"
                    ],
                    "estimated_time_minutes": 2,
                    "risk_level": "low"
                })

            elif issue["type"] == "model_deprecation":
                fixes.append({
                    "issue_type": "model_deprecation",
                    "confidence": 95,
                    "fix_description": "Research and upgrade to replacement model",
                    "fix_actions": [
                        "Detect deprecated model name from error logs",
                        "Search Groq documentation for replacement model",
                        "Update model ID in agentic_system.py",
                        "Update all documentation references",
                        "Restart backend and celery services",
                        "Test new model with sample product"
                    ],
                    "estimated_time_minutes": 5,
                    "risk_level": "medium"
                })

            elif issue["type"] == "rate_limiting":
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

            # ========== EXPANDED FIX SUGGESTIONS ==========

            elif issue["type"] == "database_null_violation":
                fixes.append({
                    "issue_type": "database_null_violation",
                    "confidence": 90,
                    "fix_description": "Add default values for NULL fields",
                    "fix_actions": [
                        "Detect which column has NULL constraint",
                        "Add DEFAULT value to column schema",
                        "Update application code to provide defaults",
                        "Backfill existing NULL values"
                    ],
                    "estimated_time_minutes": 5,
                    "risk_level": "low"
                })

            elif issue["type"] == "database_unique_violation":
                fixes.append({
                    "issue_type": "database_unique_violation",
                    "confidence": 85,
                    "fix_description": "Add duplicate checking before insert",
                    "fix_actions": [
                        "Add unique constraint validation in code",
                        "Implement upsert logic (INSERT ON CONFLICT)",
                        "Add duplicate detection before save",
                        "Log duplicate attempts for review"
                    ],
                    "estimated_time_minutes": 7,
                    "risk_level": "low"
                })

            elif issue["type"] == "attribute_errors":
                fixes.append({
                    "issue_type": "attribute_errors",
                    "confidence": 80,
                    "fix_description": "Add safe attribute access with hasattr/getattr",
                    "fix_actions": [
                        "Parse traceback to find failing attribute",
                        "Replace direct access with hasattr() check",
                        "Add getattr() with default value",
                        "Add defensive programming checks"
                    ],
                    "estimated_time_minutes": 5,
                    "risk_level": "low"
                })

            elif issue["type"] == "key_errors":
                fixes.append({
                    "issue_type": "key_errors",
                    "confidence": 80,
                    "fix_description": "Replace dict[key] with dict.get(key, default)",
                    "fix_actions": [
                        "Parse traceback to find failing key access",
                        "Replace dict[key] with dict.get(key, default)",
                        "Add validation for required keys",
                        "Log missing keys for investigation"
                    ],
                    "estimated_time_minutes": 5,
                    "risk_level": "low"
                })

            elif issue["type"] == "import_errors":
                fixes.append({
                    "issue_type": "import_errors",
                    "confidence": 95,
                    "fix_description": "Install missing Python packages",
                    "fix_actions": [
                        "Detect missing module name from error",
                        "Add module to requirements.txt",
                        "Run pip install in container",
                        "Restart affected services"
                    ],
                    "estimated_time_minutes": 3,
                    "risk_level": "low"
                })

            elif issue["type"] == "cors_errors":
                fixes.append({
                    "issue_type": "cors_errors",
                    "confidence": 90,
                    "fix_description": "Update CORS configuration to allow frontend",
                    "fix_actions": [
                        "Add frontend origin to CORS allowed origins",
                        "Update FastAPI CORS middleware",
                        "Allow credentials if needed",
                        "Restart backend service"
                    ],
                    "estimated_time_minutes": 3,
                    "risk_level": "low"
                })

            elif issue["type"] == "validation_errors":
                fixes.append({
                    "issue_type": "validation_errors",
                    "confidence": 75,
                    "fix_description": "Improve data validation rules",
                    "fix_actions": [
                        "Analyze validation failure patterns",
                        "Update validation schemas (Pydantic)",
                        "Add better error messages",
                        "Add data sanitization before validation"
                    ],
                    "estimated_time_minutes": 10,
                    "risk_level": "medium"
                })

            elif issue["type"] == "file_not_found":
                fixes.append({
                    "issue_type": "file_not_found",
                    "confidence": 85,
                    "fix_description": "Create missing files or fix paths",
                    "fix_actions": [
                        "Detect missing file path from error",
                        "Create missing directories if needed",
                        "Create placeholder files with defaults",
                        "Update file paths if incorrect"
                    ],
                    "estimated_time_minutes": 5,
                    "risk_level": "low"
                })

            elif issue["type"] == "slow_queries":
                fixes.append({
                    "issue_type": "slow_queries",
                    "confidence": 75,
                    "fix_description": "Optimize database queries",
                    "fix_actions": [
                        "Identify slow query from logs",
                        "Add database indexes on filtered columns",
                        "Optimize query with EXPLAIN ANALYZE",
                        "Consider query result caching"
                    ],
                    "estimated_time_minutes": 15,
                    "risk_level": "low"
                })

            elif issue["type"] == "missing_required_fields":
                fixes.append({
                    "issue_type": "missing_required_fields",
                    "confidence": 80,
                    "fix_description": "Add default values for required fields",
                    "fix_actions": [
                        "Detect which fields are missing",
                        "Add default value generation",
                        "Update data models with defaults",
                        "Add validation before save"
                    ],
                    "estimated_time_minutes": 7,
                    "risk_level": "low"
                })

            elif issue["type"] == "data_corruption":
                fixes.append({
                    "issue_type": "data_corruption",
                    "confidence": 85,
                    "fix_description": "Clean corrupted data (e.g., string 'null' → NULL)",
                    "fix_actions": [
                        "Scan database for string 'null' in JSON fields",
                        "Replace string 'null' with actual NULL",
                        "Update frontend to handle null values safely",
                        "Add validation to prevent future corruption"
                    ],
                    "estimated_time_minutes": 10,
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
