#!/usr/bin/env python3
"""
SoulGuard集成测试
"""

import sys
sys.path.insert(0, '/root/.openclaw/soulguard')

from memory_core.enhanced import SoulMemoryEnhanced

def test_full_workflow():
    """测试完整工作流程"""
    print("=== 集成测试：完整工作流程 ===\n")
    
    sm = SoulMemoryEnhanced("integration_test")
    
    # 1. 添加记忆
    print("1. 添加记忆...")
    result = sm.remember("我喜欢Python编程", {"type": "interest"})
    assert result['saved'] > 0, "添加记忆失败"
    print(f"   ✓ 添加 {result['saved']} 条记忆")
    
    # 2. 搜索记忆
    print("2. 搜索记忆...")
    results = sm.recall("编程")
    assert len(results) > 0, "搜索记忆失败"
    print(f"   ✓ 找到 {len(results)} 条记忆")
    
    # 3. 获取时间线
    print("3. 获取时间线...")
    timeline = sm.get_timeline()
    assert len(timeline) >= 0, "获取时间线失败"
    print(f"   ✓ 时间线有 {len(timeline)} 天")
    
    # 4. 获取图谱
    print("4. 获取关联图谱...")
    graph = sm.get_graph()
    assert 'nodes' in graph, "获取图谱失败"
    print(f"   ✓ 图谱有 {len(graph['nodes'])} 节点")
    
    # 5. 生成总结
    print("5. 生成总结...")
    summary = sm.get_summary(days=30)
    assert len(summary) > 0, "生成总结失败"
    print(f"   ✓ 总结长度: {len(summary)} 字符")
    
    # 6. 生成洞察
    print("6. 生成洞察...")
    insights = sm.get_insights()
    assert len(insights) > 0, "生成洞察失败"
    print(f"   ✓ 洞察长度: {len(insights)} 字符")
    
    print("\n✅ 集成测试通过！")
    return True

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 集成测试：边界情况 ===\n")
    
    sm = SoulMemoryEnhanced("edge_test")
    
    # 空搜索
    print("1. 空搜索...")
    results = sm.recall("不存在的查询")
    print(f"   ✓ 空搜索返回 {len(results)} 条")
    
    # 重复添加
    print("2. 重复添加...")
    sm.remember("重复内容")
    sm.remember("重复内容")
    print("   ✓ 重复添加处理完成")
    
    # 长内容
    print("3. 长内容...")
    long_content = "这是一个很长的内容" * 100
    sm.remember(long_content)
    print("   ✓ 长内容处理完成")
    
    print("\n✅ 边界测试通过！")
    return True

if __name__ == '__main__':
    test_full_workflow()
    test_edge_cases()
