"""
Backup manager for safe fix application
Creates backups before any code changes
"""
import os
import shutil
import json
from datetime import datetime
from typing import Dict, List


class BackupManager:
    """Manage backups and rollbacks"""

    def __init__(self):
        self.backup_root = "/app/backups"
        os.makedirs(self.backup_root, exist_ok=True)

    def create_backup(self, files: List[str], metadata: Dict = None) -> str:
        """Create backup of files"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        backup_id = f"backup_{timestamp}"
        backup_dir = os.path.join(self.backup_root, backup_id)

        os.makedirs(backup_dir, exist_ok=True)

        backed_up_files = []

        for file_path in files:
            if os.path.exists(file_path):
                dest = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.copy2(file_path, dest)
                backed_up_files.append(file_path)

        # Save metadata
        metadata_file = os.path.join(backup_dir, "metadata.json")
        with open(metadata_file, "w") as f:
            json.dump({
                "backup_id": backup_id,
                "timestamp": timestamp,
                "files": backed_up_files,
                "metadata": metadata or {}
            }, f, indent=2)

        return backup_id

    def rollback(self, backup_id: str) -> bool:
        """Rollback to a specific backup"""
        backup_dir = os.path.join(self.backup_root, backup_id)

        if not os.path.exists(backup_dir):
            return False

        metadata_file = os.path.join(backup_dir, "metadata.json")

        if not os.path.exists(metadata_file):
            return False

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        # Restore files
        for file_path in metadata["files"]:
            backup_file = os.path.join(backup_dir, os.path.basename(file_path))
            if os.path.exists(backup_file):
                shutil.copy2(backup_file, file_path)

        return True

    def list_backups(self) -> List[Dict]:
        """List all backups"""
        backups = []

        if not os.path.exists(self.backup_root):
            return backups

        for backup_id in os.listdir(self.backup_root):
            backup_dir = os.path.join(self.backup_root, backup_id)
            metadata_file = os.path.join(backup_dir, "metadata.json")

            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    backups.append(metadata)

        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
