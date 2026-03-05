"""
记忆提醒系统
基于时间或事件触发回忆
"""

import json
import os
from datetime import datetime, timedelta

class MemoryReminder:
    """记忆提醒器"""
    
    def __init__(self, vector_store):
        self.store = vector_store
        self.reminders_file = "/root/.openclaw/soulguard/data/reminders.json"
        os.makedirs(os.path.dirname(self.reminders_file), exist_ok=True)
    
    def set_reminder(self, memory_id, trigger_time, message=None):
        """设置提醒"""
        reminders = self._load_reminders()
        
        reminders.append({
            'memory_id': memory_id,
            'trigger_time': trigger_time.isoformat(),
            'message': message or '回顾这段记忆',
            'created': datetime.now().isoformat(),
            'triggered': False
        })
        
        self._save_reminders(reminders)
    
    def check_reminders(self):
        """检查待触发的提醒"""
        reminders = self._load_reminders()
        now = datetime.now()
        
        triggered = []
        for r in reminders:
            if not r['triggered']:
                trigger_time = datetime.fromisoformat(r['trigger_time'])
                if now >= trigger_time:
                    r['triggered'] = True
                    triggered.append(r)
        
        self._save_reminders(reminders)
        return triggered
    
    def create_anniversary_reminder(self, memory_id, memory_date):
        """创建周年提醒"""
        # 每年同一天提醒
        now = datetime.now()
        next_date = memory_date.replace(year=now.year)
        if next_date < now:
            next_date = next_date.replace(year=now.year + 1)
        
        self.set_reminder(memory_id, next_date, "周年记忆提醒")
    
    def _load_reminders(self):
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_reminders(self, reminders):
        with open(self.reminders_file, 'w') as f:
            json.dump(reminders, f, indent=2)
