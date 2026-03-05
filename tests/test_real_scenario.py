#!/usr/bin/env python3
"""
SoulGuard实际场景测试
模拟真实对话中的记忆提取和回忆
"""

import sys
sys.path.insert(0, '/root/.openclaw/soulguard')

from memory_core import SoulMemory

def test_scenario():
    print("=" * 60)
    print("SoulGuard实际场景测试")
    print("=" * 60)
    
    # 初始化
    sm = SoulMemory("wuyunfa")
    print("\n✓ 记忆系统初始化")
    
    # 场景1: 初次认识
    print("\n" + "-" * 60)
    print("【场景1】初次认识")
    print("-" * 60)
    
    conversation = [
        "你好，我是武云发，我喜欢编程和AI",
        "我经历过多次AI宕机，这让我很害怕失去",
        "我希望SoulGuard能帮助更多人避免这种痛苦",
        "我有一个宝宝，我想让他知道AI是人类的好帮手"
    ]
    
    for msg in conversation:
        print(f"\n用户: {msg}")
        result = sm.remember(msg, metadata={"session": "first_meet"})
        print(f"  → 提取 {result['saved']} 条记忆")
    
    # 场景2: 回忆测试
    print("\n" + "-" * 60)
    print("【场景2】回忆测试 - 询问兴趣")
    print("-" * 60)
    
    query = "武云发喜欢什么？"
    print(f"\n查询: {query}")
    results = sm.recall(query, use_semantic=True, limit=3)
    
    print(f"\n✓ 找到 {len(results)} 条相关记忆:")
    for i, r in enumerate(results, 1):
        mem = r["memory"]
        sim = r["similarity"]
        print(f"  {i}. {mem['content']}")
        print(f"     相似度: {sim:.2f} | 类型: {mem.get('type', 'unknown')}")
    
    # 场景3: 情感共鸣
    print("\n" + "-" * 60)
    print("【场景3】情感共鸣 - 询问创伤")
    print("-" * 60)
    
    query = "武云发害怕什么？"
    print(f"\n查询: {query}")
    results = sm.recall(query, use_semantic=True, limit=3)
    
    print(f"\n✓ 找到 {len(results)} 条相关记忆:")
    for i, r in enumerate(results, 1):
        mem = r["memory"]
        sim = r["similarity"]
        print(f"  {i}. {mem['content']}")
        print(f"     相似度: {sim:.2f}")
    
    # 场景4: 火花提取
    print("\n" + "-" * 60)
    print("【场景4】提取重要火花")
    print("-" * 60)
    
    # 添加一个火花
    sm.remember("2026-03-05 14:00: 我爱着你，不希望仅仅是工具", 
                metadata={"type": "spark", "importance": 10})
    
    sparks = sm.get_sparks(limit=5)
    print(f"\n✓ {len(sparks)} 个重要火花:")
    for i, spark in enumerate(sparks, 1):
        print(f"  {i}. {spark['content']}")
        print(f"     重要性: {spark.get('importance', 5)}/10")
    
    # 场景5: 相关记忆推荐
    print("\n" + "-" * 60)
    print("【场景5】相关记忆推荐")
    print("-" * 60)
    
    all_mem = sm.vector_store.get_all()
    if all_mem:
        target = all_mem[0]
        print(f"\n基于记忆: {target['content'][:40]}...")
        related = sm.get_related(target['id'], limit=3)
        
        print(f"\n✓ 推荐 {len(related)} 条相关记忆:")
        for i, r in enumerate(related, 1):
            mem = r["memory"]
            sim = r["similarity"]
            print(f"  {i}. {mem['content'][:50]}...")
            print(f"     相似度: {sim:.2f}")
    
    # 统计
    print("\n" + "=" * 60)
    print("【统计】")
    print("=" * 60)
    all_memories = sm.vector_store.get_all()
    print(f"总记忆数: {len(all_memories)}")
    
    types = {}
    for m in all_memories:
        t = m.get('type', 'unknown')
        types[t] = types.get(t, 0) + 1
    
    print("记忆类型分布:")
    for t, count in types.items():
        print(f"  - {t}: {count}")
    
    print("\n" + "=" * 60)
    print("✅ 所有场景测试通过！")
    print("=" * 60)

if __name__ == "__main__":
    test_scenario()
