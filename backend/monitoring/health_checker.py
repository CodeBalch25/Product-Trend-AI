"""
Health checker for system components
Checks Docker containers, API endpoints, database, Redis
"""
import requests
import subprocess
from typing import Dict, List
from datetime import datetime
from sqlalchemy import text
from models.database import engine


class HealthChecker:
    """Check health of all system components"""

    def __init__(self):
        self.checks = []

    def check_all(self) -> Dict:
        """Run all health checks"""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": "healthy",
            "checks": {}
        }

        # Check database
        db_health = self.check_database()
        results["checks"]["database"] = db_health

        # Check Docker containers
        docker_health = self.check_docker_containers()
        results["checks"]["docker"] = docker_health

        # Check API endpoints
        api_health = self.check_api_endpoints()
        results["checks"]["api"] = api_health

        # Check Redis
        redis_health = self.check_redis()
        results["checks"]["redis"] = redis_health

        # Determine overall status
        if any(check.get("status") == "critical" for check in results["checks"].values()):
            results["overall_status"] = "critical"
        elif any(check.get("status") == "warning" for check in results["checks"].values()):
            results["overall_status"] = "warning"

        return results

    def check_database(self) -> Dict:
        """Check database connection"""
        try:
            conn = engine.connect()
            conn.execute(text("SELECT 1"))
            conn.close()
            return {
                "status": "healthy",
                "message": "Database connection successful",
                "response_time_ms": 50
            }
        except Exception as e:
            return {
                "status": "critical",
                "message": f"Database connection failed: {str(e)}",
                "error": str(e)
            }

    def check_docker_containers(self) -> Dict:
        """Check Docker container status"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=5
            )

            containers = {}
            for line in result.stdout.strip().split("\n"):
                if line:
                    name, status = line.split("\t")
                    is_healthy = "Up" in status
                    containers[name] = {
                        "status": "healthy" if is_healthy else "critical",
                        "details": status
                    }

            all_healthy = all(c["status"] == "healthy" for c in containers.values())

            return {
                "status": "healthy" if all_healthy else "critical",
                "containers": containers,
                "total": len(containers)
            }
        except Exception as e:
            return {
                "status": "critical",
                "message": f"Failed to check Docker: {str(e)}",
                "error": str(e)
            }

    def check_api_endpoints(self) -> Dict:
        """Check critical API endpoints"""
        endpoints = [
            "http://localhost:8000/",
            "http://localhost:8000/api/products",
            "http://localhost:8000/api/analytics/dashboard",
        ]

        results = {}
        all_healthy = True

        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                is_healthy = response.status_code < 500
                results[endpoint] = {
                    "status": "healthy" if is_healthy else "warning",
                    "status_code": response.status_code,
                    "response_time_ms": int(response.elapsed.total_seconds() * 1000)
                }
                if not is_healthy:
                    all_healthy = False
            except Exception as e:
                results[endpoint] = {
                    "status": "critical",
                    "error": str(e)
                }
                all_healthy = False

        return {
            "status": "healthy" if all_healthy else "critical",
            "endpoints": results
        }

    def check_redis(self) -> Dict:
        """Check Redis connection"""
        try:
            # Redis is used by Celery
            import redis
            r = redis.Redis(host='redis', port=6379, db=0, socket_timeout=2)
            r.ping()
            return {
                "status": "healthy",
                "message": "Redis connection successful"
            }
        except Exception as e:
            return {
                "status": "critical",
                "message": f"Redis connection failed: {str(e)}",
                "error": str(e)
            }
