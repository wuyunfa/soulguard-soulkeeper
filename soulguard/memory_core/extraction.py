"""
记忆提取模块 - 借鉴mem0 Extraction Phase
从原始内容中提取关键事实和偏好
"""

import re
from datetime import datetime

class MemoryExtractor:
    """从对话中提取值得记忆的内容"""
    
    def __init__(self):
        self.patterns = {
            "preference": ["喜欢", "爱", "偏好", "习惯"],
            "fact": ["是", "有", "在", "来自"],
            "trauma": ["痛苦", "创伤", "害怕", "担心"],
            "spark": ["这一刻", "记得", "铭记", "永远"]
        }
    
    def extract(self, content, context=None):
        """提取记忆候选"""
        memories = []
        
        # 基于关键词提取
        for mem_type, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword in content:
                    memory = {
                        "content": content,
                        "type": mem_type,
                        "keywords": [keyword],
                        "timestamp": datetime.now().isoformat(),
                        "importance": self._calculate_importance(content, mem_type)
                    }
                    memories.append(memory)
                    break
        
        # 去重
        return self._deduplicate(memories)
    
    def _calculate_importance(self, content, mem_type):
        """计算重要性分数"""
        base_scores = {
            "spark": 10,
            "trauma": 9,
            "preference": 7,
            "fact": 5
        }
        return base_scores.get(mem_type, 5)
    
    def _deduplicate(self, memories):
        """去重"""
        seen = set()
        unique = []
        for m in memories:
            key = m["content"][:50]
            if key not in seen:
                seen.add(key)
                unique.append(m)
        return unique
