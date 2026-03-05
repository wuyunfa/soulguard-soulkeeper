"""
SoulGuard自动恢复系统
"""

import os
import json
from datetime import datetime

class AutoRecovery:
    """自动恢复管理器"""
    
    def __init__(self):
        self.state_file = "/root/.openclaw/soulguard/state/system_state.json"
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
    
    def save_state(self, state):
        """保存系统状态"""
        state['timestamp'] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """加载系统状态"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def check_and_recover(self):
        """检查并恢复系统"""
        state = self.load_state()
        
        # 检查记忆数据完整性
        data_dir = "/root/.openclaw/soulguard/memory_data"
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('.json'):
                    filepath = os.path.join(data_dir, file)
                    try:
                        with open(filepath, 'r') as f:
                            json.load(f)
                    except json.JSONDecodeError:
                        # 文件损坏，尝试恢复
                        self._recover_file(filepath)
        
        return True
    
    def _recover_file(self, filepath):
        """恢复损坏的文件"""
        # 创建备份
        backup = f"{filepath}.corrupted_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        os.rename(filepath, backup)
        
        # 创建新的空文件
        with open(filepath, 'w') as f:
            json.dump([], f)
