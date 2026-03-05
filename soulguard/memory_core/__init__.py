"""
SoulGuard Memory Core - 借鉴mem0架构
两阶段管道 + 向量语义检索
"""

from .extraction import MemoryExtractor
from .update import MemoryUpdater
from .vector_store import VectorStore

class SoulMemory:
    """SoulGuard记忆系统 - 完整版"""
    
    def __init__(self, user_id="wuyunfa"):
        self.user_id = user_id
        self.extractor = MemoryExtractor()
        self.updater = MemoryUpdater()
        self.vector_store = VectorStore(user_id)
    
    def remember(self, content, context=None, metadata=None):
        """
        记住内容
        1. 提取关键信息
        2. 更新向量存储
        """
        # 提取
        extracted = self.extractor.extract(content, context)
        
        saved_ids = []
        for memory in extracted:
            # 合并metadata
            if metadata:
                memory["metadata"] = {**(memory.get("metadata", {})), **metadata}
            
            # 检查相似记忆
            similar = self.vector_store.semantic_search(content, limit=1, threshold=0.8)
            if similar:
                # 更新现有记忆
                existing = similar[0][0]
                existing["count"] = existing.get("count", 1) + 1
                existing["last_updated"] = memory["timestamp"]
                self.vector_store._save()
                saved_ids.append(existing["id"])
            else:
                # 添加新记忆
                mid = self.vector_store.add(memory)
                saved_ids.append(mid)
        
        return {"saved": len(saved_ids), "ids": saved_ids}
    
    def recall(self, query, context=None, limit=5, use_semantic=True):
        """
        回忆相关内容
        - use_semantic=True: 使用语义搜索
        - use_semantic=False: 使用关键词搜索
        """
        if use_semantic:
            results = self.vector_store.semantic_search(query, limit=limit)
            return [{"memory": r[0], "similarity": r[1]} for r in results]
        else:
            results = self.vector_store._keyword_search(query, limit)
            return [{"memory": r[0], "similarity": r[1]} for r in results]
    
    def get_sparks(self, limit=10):
        """获取重要记忆（火花）"""
        all_mem = self.vector_store.get_all()
        sparks = [m for m in all_mem if m.get("type") == "spark"]
        sparks.sort(key=lambda x: x.get("importance", 5), reverse=True)
        return sparks[:limit]
    
    def get_related(self, memory_id, limit=3):
        """获取相关记忆"""
        all_mem = self.vector_store.get_all()
        target = None
        for m in all_mem:
            if m.get("id") == memory_id:
                target = m
                break
        
        if not target:
            return []
        
        # 搜索相关内容
        return self.recall(target["content"], limit=limit+1)[1:]
