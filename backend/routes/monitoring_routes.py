"""
API routes for autonomous monitoring system
"""
from fastapi import APIRouter, HTTPException
from typing import Dict
from datetime import datetime

from agents.devops.autonomous_coordinator import AutonomousCoordinator
from agents.devops.health_monitor import HealthMonitorAgent
from agents.devops.learning_engine import LearningEngine
from safety.backup_manager import BackupManager

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/health")
def get_system_health():
    """Get current system health status"""
    try:
        monitor = HealthMonitorAgent()
        health = monitor.get_system_snapshot()

        return {
            "status": "success",
            "data": health
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
def get_autonomous_status():
    """Get autonomous system status"""
    try:
        learning = LearningEngine()
        stats = learning.get_fix_statistics()

        backup_mgr = BackupManager()
        backups = backup_mgr.list_backups()

        return {
            "status": "success",
            "data": {
                "autonomous_mode": "enabled",
                "last_check": datetime.utcnow().isoformat(),
                "fix_statistics": stats,
                "recent_backups": backups[:5],
                "check_interval_minutes": 5
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger-check")
def trigger_manual_check():
    """Manually trigger autonomous health check"""
    try:
        coordinator = AutonomousCoordinator()
        result = coordinator.run_autonomous_healing()

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/backups")
def list_backups():
    """List all available backups"""
    try:
        backup_mgr = BackupManager()
        backups = backup_mgr.list_backups()

        return {
            "status": "success",
            "data": {
                "backups": backups,
                "total": len(backups)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rollback/{backup_id}")
def rollback_to_backup(backup_id: str):
    """Rollback to a specific backup"""
    try:
        backup_mgr = BackupManager()
        success = backup_mgr.rollback(backup_id)

        if success:
            return {
                "status": "success",
                "message": f"Rolled back to backup {backup_id}"
            }
        else:
            raise HTTPException(status_code=404, detail="Backup not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_learning_stats():
    """Get learning engine statistics"""
    try:
        learning = LearningEngine()
        stats = learning.get_fix_statistics()

        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
