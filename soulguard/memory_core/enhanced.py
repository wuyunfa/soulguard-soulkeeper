"""
增强版记忆核心 - 集成所有高级功能
"""

from .vector_store import VectorStore
from .timeline import MemoryTimeline
from .graph import MemoryGraph
from .summarizer import MemorySummarizer

class SoulMemoryEnhanced:
    """SoulGuard增强版记忆系统"""
    
    def __init__(self, user_id="wuyunfa"):
        self.store = VectorStore(user_id)
        self.timeline = MemoryTimeline(self.store)
        self.graph = MemoryGraph(self.store)
        self.summarizer = MemorySummarizer(self.store)
    
    # 基础功能
    def remember(self, content, metadata=None):
        from .extraction import MemoryExtractor
        from .update import MemoryUpdater
        
        extractor = MemoryExtractor()
        updater = MemoryUpdater()
        
        extracted = extractor.extract(content, {})
        saved_ids = []
        
        for memory in extracted:
            if metadata:
                memory["metadata"] = {**(memory.get("metadata", {})), **metadata}
            
            similar = self.store.semantic_search(content, limit=1, threshold=0.8)
            if similar:
                existing = similar[0][0]
                existing["count"] = existing.get("count", 1) + 1
                self.store._save()
                saved_ids.append(existing["id"])
            else:
                mid = self.store.add(memory)
                saved_ids.append(mid)
        
        return {"saved": len(saved_ids), "ids": saved_ids}
    
    def recall(self, query, limit=5):
        results = self.store.semantic_search(query, limit=limit)
        return [{"memory": r[0], "similarity": r[1]} for r in results]
    
    # 增强功能
    def get_timeline(self):
        return self.timeline.get_timeline()
    
    def get_graph(self):
        return self.graph.build_graph()
    
    def get_summary(self, days=7):
        return self.summarizer.generate_summary(days)
    
    def get_insights(self):
        return self.summarizer.generate_insights()
