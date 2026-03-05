"""
SoulGuard性能优化
"""

import os
import json
import gzip
from datetime import datetime, timedelta

class MemoryOptimizer:
    """记忆系统优化器"""
    
    def __init__(self, data_dir="/root/.openclaw/soulguard/memory_data"):
        self.data_dir = data_dir
    
    def compress_old_memories(self, days=30):
        """压缩旧记忆"""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        for file in os.listdir(self.data_dir):
            if file.endswith('.json') and not file.endswith('.gz'):
                filepath = os.path.join(self.data_dir, file)
                
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # 分离新旧记忆
                old = [m for m in data if m.get('timestamp', '') < cutoff]
                new = [m for m in data if m.get('timestamp', '') >= cutoff]
                
                if old:
                    # 压缩旧记忆
                    gz_path = filepath + '.archive.gz'
                    with gzip.open(gz_path, 'wt') as f:
                        json.dump(old, f)
                    
                    # 保留新记忆
                    with open(filepath, 'w') as f:
                        json.dump(new, f)
                    
                    print(f"压缩 {file}: {len(old)} 条旧记忆")
    
    def cleanup_duplicates(self, similarity_threshold=0.9):
        """清理重复记忆"""
        for file in os.listdir(self.data_dir):
            if file.endswith('.json'):
                filepath = os.path.join(self.data_dir, file)
                
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # 去重
                unique = []
                for mem in data:
                    is_dup = False
                    for u in unique:
                        if self._similarity(mem['content'], u['content']) > similarity_threshold:
                            is_dup = True
                            break
                    if not is_dup:
                        unique.append(mem)
                
                if len(unique) < len(data):
                    with open(filepath, 'w') as f:
                        json.dump(unique, f)
                    print(f"清理 {file}: 移除 {len(data) - len(unique)} 条重复")
    
    def _similarity(self, s1, s2):
        """计算相似度"""
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        if not words1 or not words2:
            return 0
        return len(words1 & words2) / len(words1 | words2)
