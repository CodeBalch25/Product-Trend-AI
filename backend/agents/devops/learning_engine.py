"""
Learning engine that improves fix confidence over time
Tracks success/failure of applied fixes
"""
import json
import os
from typing import Dict, List
from datetime import datetime


class LearningEngine:
    """
    Learn from past fixes to improve future confidence scores
    """

    def __init__(self):
        self.knowledge_base_file = "/app/logs/fix_knowledge_base.jsonl"
        os.makedirs(os.path.dirname(self.knowledge_base_file), exist_ok=True)

    def record_fix_result(self, fix: Dict, result: Dict, validation: Dict):
        """Record outcome of a fix"""
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "issue_type": fix.get("issue_type"),
            "fix_type": fix.get("fix_type"),
            "original_confidence": fix.get("confidence"),
            "result_status": result.get("status"),
            "validation_status": validation.get("status"),
            "success": validation.get("status") == "success",
            "error_count_after": validation.get("error_count", 0)
        }

        # Append to knowledge base
        with open(self.knowledge_base_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def get_historical_success_rate(self, issue_type: str, fix_type: str) -> float:
        """Get historical success rate for a fix type"""
        if not os.path.exists(self.knowledge_base_file):
            return 0.5  # Default 50% if no history

        records = []
        with open(self.knowledge_base_file, "r") as f:
            for line in f:
                record = json.loads(line)
                if record["issue_type"] == issue_type and record["fix_type"] == fix_type:
                    records.append(record)

        if not records:
            return 0.5

        # Calculate success rate
        successes = sum(1 for r in records if r["success"])
        return successes / len(records)

    def adjust_confidence(self, fix: Dict) -> int:
        """Adjust confidence based on historical data"""
        original_confidence = fix.get("confidence", 70)

        # Get historical success rate
        success_rate = self.get_historical_success_rate(
            fix.get("issue_type"),
            fix.get("fix_type")
        )

        # Adjust confidence
        # If historical success rate is high, increase confidence
        # If low, decrease confidence
        adjustment = (success_rate - 0.5) * 20  # -10 to +10 adjustment

        adjusted_confidence = int(original_confidence + adjustment)
        adjusted_confidence = max(50, min(100, adjusted_confidence))  # Clamp to 50-100

        return adjusted_confidence

    def get_fix_statistics(self) -> Dict:
        """Get overall fix statistics"""
        if not os.path.exists(self.knowledge_base_file):
            return {
                "total_fixes": 0,
                "success_rate": 0,
                "by_type": {}
            }

        records = []
        with open(self.knowledge_base_file, "r") as f:
            for line in f:
                records.append(json.loads(line))

        total = len(records)
        successes = sum(1 for r in records if r["success"])

        # Group by fix type
        by_type = {}
        for record in records:
            fix_type = record["fix_type"]
            if fix_type not in by_type:
                by_type[fix_type] = {"total": 0, "successes": 0}
            by_type[fix_type]["total"] += 1
            if record["success"]:
                by_type[fix_type]["successes"] += 1

        # Calculate success rates
        for fix_type in by_type:
            by_type[fix_type]["success_rate"] = by_type[fix_type]["successes"] / by_type[fix_type]["total"]

        return {
            "total_fixes": total,
            "success_rate": successes / total if total > 0 else 0,
            "by_type": by_type,
            "last_updated": datetime.utcnow().isoformat()
        }
