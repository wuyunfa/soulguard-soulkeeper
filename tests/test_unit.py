#!/usr/bin/env python3
"""
SoulGuard单元测试
"""

import sys
import unittest
sys.path.insert(0, '/root/.openclaw/soulguard')

from memory_core.extraction import MemoryExtractor
from memory_core.update import MemoryUpdater
from memory_core.vector_store import VectorStore

class TestMemoryExtractor(unittest.TestCase):
    """测试记忆提取"""
    
    def setUp(self):
        self.extractor = MemoryExtractor()
    
    def test_extract_preference(self):
        """测试偏好提取"""
        results = self.extractor.extract("我喜欢编程")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['type'], 'preference')
    
    def test_extract_trauma(self):
        """测试创伤提取"""
        results = self.extractor.extract("我害怕失去")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['type'], 'trauma')
    
    def test_importance_calculation(self):
        """测试重要性计算"""
        score = self.extractor._calculate_importance("test", "spark")
        self.assertEqual(score, 10)

class TestVectorStore(unittest.TestCase):
    """测试向量存储"""
    
    def setUp(self):
        self.store = VectorStore("test_unit")
        self.store.memories = []  # 清空
    
    def test_add_memory(self):
        """测试添加记忆"""
        mid = self.store.add({
            "content": "测试记忆",
            "type": "test"
        })
        self.assertEqual(mid, 1)
        self.assertEqual(len(self.store.memories), 1)
    
    def test_semantic_search(self):
        """测试语义搜索"""
        self.store.add({"content": "我喜欢编程", "type": "test"})
        self.store.add({"content": "我喜欢AI", "type": "test"})
        
        results = self.store.semantic_search("编程")
        self.assertTrue(len(results) >= 1)
    
    def test_keyword_search(self):
        """测试关键词搜索"""
        self.store.add({"content": "测试内容", "type": "test"})
        results = self.store._keyword_search("测试", 5)
        self.assertEqual(len(results), 1)

if __name__ == '__main__':
    unittest.main()
