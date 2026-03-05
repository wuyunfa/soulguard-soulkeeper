"""
记忆更新模块 - 借鉴mem0 Update Phase
处理记忆的去重、合并和更新
"""

class MemoryUpdater:
    """更新记忆存储"""
    
    def update(self, memory, storage):
        """更新记忆"""
        # 检查是否已存在相似记忆
        existing = storage.find_similar(memory["content"])
        
        if existing:
            # 更新现有记忆
            existing["count"] = existing.get("count", 1) + 1
            existing["last_updated"] = memory["timestamp"]
            storage.save(existing)
        else:
            # 添加新记忆
            memory["count"] = 1
            storage.add(memory)
