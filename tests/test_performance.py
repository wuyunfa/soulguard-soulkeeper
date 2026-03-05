#!/usr/bin/env python3
"""
SoulGuard性能测试
"""

import sys
import time
sys.path.insert(0, '/root/.openclaw/soulguard')

from memory_core import SoulMemory

def test_performance():
    print("=== SoulGuard性能测试 ===\n")
    
    sm = SoulMemory("test_user")
    
    # 批量添加
    print("1. 批量添加测试 (100条记忆)...")
    start = time.time()
    for i in range(100):
        sm.remember(f"测试记忆内容 {i}，包含一些关键词如编程、AI、学习", 
                   metadata={"batch": True})
    add_time = time.time() - start
    print(f"   ✓ 添加100条记忆耗时: {add_time:.2f}秒")
    print(f"   ✓ 平均每条: {add_time/100*1000:.2f}ms")
    
    # 搜索性能
    print("\n2. 搜索性能测试...")
    start = time.time()
    for i in range(10):
        results = sm.recall("编程学习", limit=5)
    search_time = (time.time() - start) / 10
    print(f"   ✓ 平均搜索耗时: {search_time*1000:.2f}ms")
    
    # 内存占用
    print("\n3. 数据规模...")
    import os
    data_file = f"/root/.openclaw/soulguard/memory_data/test_user_memories.json"
    if os.path.exists(data_file):
        size = os.path.getsize(data_file)
        print(f"   ✓ 数据文件大小: {size/1024:.2f}KB")
    
    print("\n✅ 性能测试完成！")

if __name__ == "__main__":
    test_performance()
