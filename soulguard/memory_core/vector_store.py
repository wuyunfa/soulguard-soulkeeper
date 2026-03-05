"""
向量存储模块 - 实现语义检索
使用简单的TF-IDF + 余弦相似度
"""

import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    """简单向量存储，支持语义检索"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.data_dir = "/root/.openclaw/soulguard/memory_data"
        self.vector_file = f"{self.data_dir}/{user_id}_vectors.json"
        self.memories_file = f"{self.data_dir}/{user_id}_memories.json"
        
        self.memories = []
        self.vectors = None
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        self._load()
    
    def _load(self):
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self.memories_file):
            with open(self.memories_file, 'r', encoding='utf-8') as f:
                self.memories = json.load(f)
            self._build_vectors()
    
    def _build_vectors(self):
        """构建向量表示"""
        if not self.memories:
            return
        
        texts = [m["content"] for m in self.memories]
        try:
            self.vectors = self.vectorizer.fit_transform(texts)
        except:
            # 如果失败，使用简单方式
            self.vectors = None
    
    def add(self, memory):
        """添加记忆并更新向量"""
        memory["id"] = len(self.memories) + 1
        self.memories.append(memory)
        self._save()
        self._build_vectors()
        return memory["id"]
    
    def semantic_search(self, query, limit=5, threshold=0.3):
        """语义搜索 - 使用余弦相似度"""
        if not self.memories or self.vectors is None:
            return []
        
        # 将查询转换为向量
        try:
            query_vec = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vec, self.vectors).flatten()
            
            # 获取最相似的结果
            results = []
            for idx, sim in enumerate(similarities):
                if sim >= threshold:
                    results.append((sim, self.memories[idx]))
            
            # 按相似度排序
            results.sort(key=lambda x: x[0], reverse=True)
            return [(r[1], float(r[0])) for r in results[:limit]]
        except:
            # 降级到关键词搜索
            return self._keyword_search(query, limit)
    
    def _keyword_search(self, query, limit):
        """关键词搜索（降级方案）"""
        results = []
        query_lower = query.lower()
        for m in self.memories:
            if query_lower in m["content"].lower():
                results.append((m, 1.0))
        return results[:limit]
    
    def _save(self):
        with open(self.memories_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def get_all(self):
        return self.memories
