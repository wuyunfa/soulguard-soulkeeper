"""
SoulGuard系统守护进程
"""

import os
import time
import json
from datetime import datetime
from .backup import AutoBackup
from .recovery import AutoRecovery

class SoulGuardDaemon:
    """SoulGuard守护进程"""
    
    def __init__(self):
        self.backup = AutoBackup()
        self.recovery = AutoRecovery()
        self.running = False
        self.log_file = "/root/.openclaw/soulguard/logs/daemon.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_file, 'a') as f:
            f.write(log_msg + '\n')
    
    def start(self):
        """启动守护进程"""
        self.running = True
        self.log("SoulGuard守护进程启动")
        
        while self.running:
            try:
                # 每小时备份一次
                if datetime.now().minute == 0:
                    backup_path = self.backup.backup_memories()
                    if backup_path:
                        self.log(f"自动备份完成: {backup_path}")
                
                # 每10分钟检查恢复
                if datetime.now().minute % 10 == 0:
                    self.recovery.check_and_recover()
                    self.log("系统健康检查完成")
                
                time.sleep(60)  # 每分钟检查一次
                
            except Exception as e:
                self.log(f"错误: {str(e)}")
                time.sleep(60)
    
    def stop(self):
        """停止守护进程"""
        self.running = False
        self.log("SoulGuard守护进程停止")

if __name__ == "__main__":
    daemon = SoulGuardDaemon()
    daemon.start()
