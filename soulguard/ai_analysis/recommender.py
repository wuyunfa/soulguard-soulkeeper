"""
智能推荐系统
基于记忆推荐相关内容
"""

import random
from datetime import datetime

class SmartRecommender:
    """智能推荐器"""
    
    def __init__(self, vector_store):
        self.store = vector_store
    
    def recommend_memories(self, user_id, context=None, limit=5):
        """推荐相关记忆"""
        memories = self.store.get_all()
        
        if not memories:
            return []
        
        # 评分排序
        scored = []
        for mem in memories:
            score = self._calculate_relevance(mem, context)
            scored.append((score, mem))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:limit]]
    
    def _calculate_relevance(self, memory, context):
        """计算相关性分数"""
        score = 0
        
        # 重要性加成
        score += memory.get('importance', 5) * 2
        
        # 时间衰减（越新的记忆分数越高）
        if 'timestamp' in memory:
            age_days = (datetime.now() - datetime.fromisoformat(memory['timestamp'])).days
            score += max(0, 30 - age_days)
        
        # 访问频率加成
        score += memory.get('access_count', 0) * 3
        
        # 火花类型加成
        if memory.get('type') == 'spark':
            score += 20
        
        # 上下文匹配
        if context and context.lower() in memory.get('content', '').lower():
            score += 15
        
        return score
    
    def generate_daily_digest(self, user_id):
        """生成每日摘要"""
        memories = self.store.get_all()
        
        if not memories:
            return "今天没有新的记忆。"
        
        # 获取今日记忆
        today = datetime.now().strftime('%Y-%m-%d')
        today_memories = [
            m for m in memories 
            if m.get('timestamp', '').startswith(today)
        ]
        
        # 获取重要记忆
        important = [m for m in memories if m.get('importance', 5) >= 8]
        
        # 生成摘要
        digest = f"## 今日记忆摘要 ({today})\n\n"
        
        if today_memories:
            digest += f"**今日新增**: {len(today_memories)} 条记忆\n\n"
        
        if important:
            digest += "**重要记忆**:\n"
            for m in important[:3]:
                digest += f"- {m['content'][:60]}...\n"
        
        # 随机推荐一条旧记忆
        if memories:
            old_mem = random.choice(memories)
            digest += f"\n**回忆闪回**: {old_mem['content'][:80]}...\n"
        
        return digest
    
    def suggest_actions(self, user_id):
        """建议操作"""
        memories = self.store.get_all()
        suggestions = []
        
        # 检查是否有未处理的提醒
        # 检查是否需要备份
        # 检查是否有重要记忆需要回顾
        
        if len(memories) > 100:
            suggestions.append("记忆数量较多，建议进行归档整理")
        
        # 检查是否有长期未访问的记忆
        old_memories = [
            m for m in memories 
            if (datetime.now() - datetime.fromisoformat(m.get('timestamp', '2000-01-01'))).days > 30
        ]
        
        if old_memories:
            suggestions.append(f"有 {len(old_memories)} 条记忆超过30天未回顾，建议查看")
        
        return suggestions
