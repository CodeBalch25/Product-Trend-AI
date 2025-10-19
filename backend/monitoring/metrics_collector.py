"""
Metrics collector for system performance
Tracks CPU, memory, response times, error rates
"""
import subprocess
import psutil
from typing import Dict
from datetime import datetime
from sqlalchemy import text
from models.database import SessionLocal, Product, ProductStatus


class MetricsCollector:
    """Collect system metrics"""

    def collect_all_metrics(self) -> Dict:
        """Collect all system metrics"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": self.get_system_metrics(),
            "docker": self.get_docker_metrics(),
            "application": self.get_application_metrics(),
            "database": self.get_database_metrics()
        }

    def get_system_metrics(self) -> Dict:
        """Get system resource usage"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_available_mb": psutil.virtual_memory().available / (1024 * 1024),
                "disk_percent": psutil.disk_usage('/').percent,
                "status": "healthy"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def get_docker_metrics(self) -> Dict:
        """Get Docker container metrics"""
        try:
            # Get container stats
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format",
                 "{{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.MemUsage}}"],
                capture_output=True,
                text=True,
                timeout=5
            )

            containers = {}
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("\t")
                    if len(parts) >= 4:
                        name = parts[0]
                        containers[name] = {
                            "cpu_percent": parts[1].replace("%", ""),
                            "memory_percent": parts[2].replace("%", ""),
                            "memory_usage": parts[3]
                        }

            return {
                "status": "healthy",
                "containers": containers
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def get_application_metrics(self) -> Dict:
        """Get application-specific metrics"""
        db = SessionLocal()
        try:
            # Count products by status
            total_products = db.query(Product).count()
            discovered = db.query(Product).filter(Product.status == ProductStatus.DISCOVERED).count()
            analyzing = db.query(Product).filter(Product.status == ProductStatus.ANALYZING).count()
            pending_review = db.query(Product).filter(Product.status == ProductStatus.PENDING_REVIEW).count()
            approved = db.query(Product).filter(Product.status == ProductStatus.APPROVED).count()
            rejected = db.query(Product).filter(Product.status == ProductStatus.REJECTED).count()

            return {
                "status": "healthy",
                "products": {
                    "total": total_products,
                    "discovered": discovered,
                    "analyzing": analyzing,
                    "pending_review": pending_review,
                    "approved": approved,
                    "rejected": rejected
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
        finally:
            db.close()

    def get_database_metrics(self) -> Dict:
        """Get database performance metrics"""
        db = SessionLocal()
        try:
            # Simple query performance test
            start = datetime.utcnow()
            db.execute(text("SELECT 1"))
            end = datetime.utcnow()

            query_time_ms = (end - start).total_seconds() * 1000

            return {
                "status": "healthy",
                "query_response_time_ms": round(query_time_ms, 2),
                "connection_status": "connected"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
        finally:
            db.close()

    def check_thresholds(self, metrics: Dict) -> Dict:
        """Check if metrics exceed thresholds"""
        alerts = []

        # Check system resources
        system = metrics.get("system", {})
        if system.get("cpu_percent", 0) > 90:
            alerts.append({
                "severity": "critical",
                "type": "high_cpu",
                "message": f"CPU usage at {system['cpu_percent']}%",
                "threshold": 90
            })
        elif system.get("cpu_percent", 0) > 70:
            alerts.append({
                "severity": "warning",
                "type": "high_cpu",
                "message": f"CPU usage at {system['cpu_percent']}%",
                "threshold": 70
            })

        if system.get("memory_percent", 0) > 90:
            alerts.append({
                "severity": "critical",
                "type": "high_memory",
                "message": f"Memory usage at {system['memory_percent']}%",
                "threshold": 90
            })
        elif system.get("memory_percent", 0) > 70:
            alerts.append({
                "severity": "warning",
                "type": "high_memory",
                "message": f"Memory usage at {system['memory_percent']}%",
                "threshold": 70
            })

        return {
            "has_alerts": len(alerts) > 0,
            "alert_count": len(alerts),
            "alerts": alerts
        }
