"""
记忆存储模块
本地JSON存储，支持向量检索
"""

import json
import os

class MemoryStorage:
    """本地记忆存储"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.data_dir = "/root/.openclaw/soulguard/memory_data"
        self.file_path = f"{self.data_dir}/{user_id}_memories.json"
        self.memories = []
        self._load()
    
    def _load(self):
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.memories = json.load(f)
    
    def save(self, memory):
        """保存记忆"""
        for i, m in enumerate(self.memories):
            if m.get("id") == memory.get("id"):
                self.memories[i] = memory
                break
        else:
            memory["id"] = len(self.memories) + 1
            self.memories.append(memory)
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def add(self, memory):
        """添加新记忆"""
        memory["id"] = len(self.memories) + 1
        self.memories.append(memory)
        self.save(memory)
    
    def find_similar(self, content, threshold=0.8):
        """查找相似记忆（简单实现）"""
        for m in self.memories:
            if content[:30] in m["content"] or m["content"][:30] in content:
                return m
        return None
    
    def get_all(self):
        return self.memories
