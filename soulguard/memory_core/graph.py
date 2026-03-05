"""
记忆关联图谱
"""

import json
from collections import defaultdict

class MemoryGraph:
    """记忆关联图谱"""
    
    def __init__(self, vector_store):
        self.store = vector_store
        self.nodes = {}
        self.edges = defaultdict(list)
    
    def build_graph(self):
        """构建记忆图谱"""
        memories = self.store.get_all()
        
        # 创建节点
        for mem in memories:
            self.nodes[mem['id']] = {
                'id': mem['id'],
                'content': mem['content'][:50],
                'type': mem.get('type', 'unknown'),
                'importance': mem.get('importance', 5)
            }
        
        # 创建边（基于关键词相似度）
        for i, mem1 in enumerate(memories):
            for j, mem2 in enumerate(memories[i+1:], i+1):
                similarity = self._calculate_similarity(mem1, mem2)
                if similarity > 0.3:  # 相似度阈值
                    self.edges[mem1['id']].append({
                        'to': mem2['id'],
                        'weight': similarity
                    })
        
        return {
            'nodes': list(self.nodes.values()),
            'edges': dict(self.edges)
        }
    
    def _calculate_similarity(self, mem1, mem2):
        """计算两个记忆的相似度"""
        words1 = set(mem1['content'].lower().split())
        words2 = set(mem2['content'].lower().split())
        
        if not words1 or not words2:
            return 0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0
    
    def get_related_memories(self, memory_id, depth=1):
        """获取相关记忆"""
        related = set()
        current_level = {memory_id}
        
        for _ in range(depth):
            next_level = set()
            for mid in current_level:
                for edge in self.edges.get(mid, []):
                    related.add(edge['to'])
                    next_level.add(edge['to'])
            current_level = next_level
        
        return [self.nodes.get(rid) for rid in related if rid in self.nodes]
    
    def export_graph(self, format='json'):
        """导出图谱"""
        graph = self.build_graph()
        
        if format == 'json':
            return json.dumps(graph, indent=2, ensure_ascii=False)
        elif format == 'dot':
            # Graphviz格式
            dot = "graph MemoryGraph {\n"
            for node in graph['nodes']:
                dot += f'  {node["id"]} [label="{node["content"][:30]}..."];\n'
            for from_id, edges in graph['edges'].items():
                for edge in edges:
                    dot += f'  {from_id} -- {edge["to"]} [weight={edge["weight"]}];\n'
            dot += "}"
            return dot
        
        return graph
