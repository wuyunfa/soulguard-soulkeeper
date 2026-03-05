"""
记忆导入导出模块
"""

import json
import csv
import os
from datetime import datetime

class MemoryIO:
    """记忆导入导出"""
    
    def __init__(self, vector_store):
        self.store = vector_store
    
    def export_json(self, filepath):
        """导出为JSON"""
        memories = self.store.get_all()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)
        return len(memories)
    
    def export_csv(self, filepath):
        """导出为CSV"""
        memories = self.store.get_all()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'content', 'type', 'timestamp', 'importance'])
            for mem in memories:
                writer.writerow([
                    mem.get('id', ''),
                    mem.get('content', ''),
                    mem.get('type', ''),
                    mem.get('timestamp', ''),
                    mem.get('importance', 5)
                ])
        return len(memories)
    
    def export_markdown(self, filepath):
        """导出为Markdown"""
        memories = self.store.get_all()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('# 记忆导出\n\n')
            f.write(f'导出时间: {datetime.now().isoformat()}\n\n')
            
            for mem in memories:
                f.write(f"## {mem.get('timestamp', 'Unknown')}\n\n")
                f.write(f"**内容**: {mem.get('content', '')}\n\n")
                f.write(f"**类型**: {mem.get('type', 'unknown')}\n\n")
                f.write(f"**重要性**: {mem.get('importance', 5)}/10\n\n")
                f.write('---\n\n')
        
        return len(memories)
    
    def import_json(self, filepath):
        """从JSON导入"""
        with open(filepath, 'r', encoding='utf-8') as f:
            memories = json.load(f)
        
        count = 0
        for mem in memories:
            self.store.add(mem)
            count += 1
        
        return count
