"""
向量存储模块 - 修复版
解决中文搜索问题
"""

import json
import os
import re

class VectorStore:
    """修复版向量存储，优化中文支持"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.data_dir = "/root/.openclaw/soulguard/memory_data"
        self.memories_file = f"{self.data_dir}/{user_id}_memories.json"
        self.memories = []
        self._load()
    
    def _load(self):
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self.memories_file):
            with open(self.memories_file, 'r', encoding='utf-8') as f:
                self.memories = json.load(f)
    
    def add(self, memory):
        """添加记忆"""
        memory["id"] = len(self.memories) + 1
        self.memories.append(memory)
        self._save()
        return memory["id"]
    
    def semantic_search(self, query, limit=5, threshold=0.0):
        """
        语义搜索 - 使用简单但有效的算法
        基于关键词匹配 + 重要性排序
        """
        if not self.memories:
            return []
        
        results = []
        query_keywords = set(self._extract_keywords(query))
        
        for mem in self.memories:
            content = mem.get("content", "")
            mem_keywords = set(self._extract_keywords(content))
            
            # 计算Jaccard相似度
            intersection = query_keywords & mem_keywords
            union = query_keywords | mem_keywords
            
            if union:
                similarity = len(intersection) / len(union)
            else:
                similarity = 0
            
            # 额外加分：直接包含查询字符串
            if query.lower() in content.lower():
                similarity += 0.5
            
            # 重要性加成
            importance = mem.get("importance", 5) / 10
            similarity += importance * 0.3
            
            if similarity >= threshold:
                results.append((similarity, mem))
        
        # 排序并返回
        results.sort(key=lambda x: x[0], reverse=True)
        return [(r[1], float(r[0])) for r in results[:limit]]
    
    def _extract_keywords(self, text):
        """提取关键词（支持中文）"""
        # 移除标点，保留中文和英文
        text = re.sub(r'[^\w\s]', ' ', text)
        # 分词（简单按空格和常见词）
        words = []
        for word in text.split():
            word = word.strip().lower()
            if len(word) >= 2:  # 至少2个字符
                words.append(word)
        return words
    
    def _save(self):
        with open(self.memories_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def get_all(self):
        return self.memories
