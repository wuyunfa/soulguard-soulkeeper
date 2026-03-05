"""
记忆检索模块
支持关键词搜索和重要性排序
"""

class MemoryRetriever:
    """检索记忆"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def search(self, query, context=None, limit=5):
        """搜索记忆"""
        memories = self.storage.get_all()
        results = []
        
        query_lower = query.lower()
        
        for mem in memories:
            score = 0
            content = mem.get("content", "").lower()
            
            # 关键词匹配
            if query_lower in content:
                score += 10
            
            # 重要性加成
            score += mem.get("importance", 5)
            
            # 频率加成
            score += mem.get("count", 1) * 2
            
            if score > 0:
                results.append((score, mem))
        
        # 排序并返回
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]
