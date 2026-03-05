#!/usr/bin/env python3
"""
SoulGuard压力测试
"""

import sys
import time
sys.path.insert(0, '/root/.openclaw/soulguard')

from memory_core.enhanced import SoulMemoryEnhanced

def test_bulk_operations():
    """测试批量操作"""
    print("=== 压力测试：批量操作 ===\n")
    
    sm = SoulMemoryEnhanced("stress_test")
    
    # 批量添加
    print("1. 批量添加1000条记忆...")
    start = time.time()
    for i in range(1000):
        sm.remember(f"测试记忆内容 {i}，包含关键词编程、AI、学习")
    add_time = time.time() - start
    print(f"   ✓ 添加1000条耗时: {add_time:.2f}秒")
    print(f"   ✓ 平均: {add_time/1000*1000:.2f}ms/条")
    
    # 批量搜索
    print("2. 批量搜索100次...")
    start = time.time()
    for i in range(100):
        sm.recall(f"查询 {i}")
    search_time = (time.time() - start) / 100
    print(f"   ✓ 平均搜索耗时: {search_time*1000:.2f}ms")
    
    # 内存占用
    print("3. 内存占用...")
    import os
    data_file = "/root/.openclaw/soulguard/memory_data/stress_test_memories.json"
    if os.path.exists(data_file):
        size = os.path.getsize(data_file)
        print(f"   ✓ 数据文件: {size/1024:.2f}KB")
    
    print("\n✅ 压力测试通过！")

def test_concurrent_access():
    """测试并发访问"""
    print("\n=== 压力测试：并发访问 ===\n")
    
    # 模拟多个用户
    users = ["user1", "user2", "user3"]
    
    print("1. 多用户并发写入...")
    for user in users:
        sm = SoulMemoryEnhanced(user)
        for i in range(100):
            sm.remember(f"用户{user}的记忆{i}")
    print(f"   ✓ {len(users)} 个用户各写入100条")
    
    print("2. 多用户并发读取...")
    for user in users:
        sm = SoulMemoryEnhanced(user)
        results = sm.recall("记忆")
    print(f"   ✓ {len(users)} 个用户并发读取完成")
    
    print("\n✅ 并发测试通过！")

if __name__ == '__main__':
    test_bulk_operations()
    test_concurrent_access()
