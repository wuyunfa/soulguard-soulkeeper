"""
SoulGuard自动备份系统
"""

import os
import json
import shutil
from datetime import datetime

class AutoBackup:
    """自动备份管理器"""
    
    def __init__(self, backup_dir="/root/.openclaw/soulguard/backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def backup_memories(self, data_dir="/root/.openclaw/soulguard/memory_data"):
        """备份记忆数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/memories_{timestamp}"
        
        if os.path.exists(data_dir):
            shutil.copytree(data_dir, backup_path)
            
            # 保留最近10个备份
            self._cleanup_old_backups()
            
            return backup_path
        return None
    
    def _cleanup_old_backups(self, keep=10):
        """清理旧备份"""
        backups = sorted([
            f for f in os.listdir(self.backup_dir)
            if f.startswith("memories_")
        ])
        
        for old in backups[:-keep]:
            shutil.rmtree(f"{self.backup_dir}/{old}")
    
    def restore(self, backup_name):
        """从备份恢复"""
        backup_path = f"{self.backup_dir}/{backup_name}"
        data_dir = "/root/.openclaw/soulguard/memory_data"
        
        if os.path.exists(backup_path):
            if os.path.exists(data_dir):
                shutil.rmtree(data_dir)
            shutil.copytree(backup_path, data_dir)
            return True
        return False
