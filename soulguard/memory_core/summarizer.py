"""
记忆自动总结
"""

from datetime import datetime
from collections import Counter

class MemorySummarizer:
    """记忆总结生成器"""
    
    def __init__(self, vector_store):
        self.store = vector_store
    
    def generate_summary(self, days=7):
        """生成近期总结"""
        memories = self.store.get_all()
        
        # 过滤近期记忆
        from datetime import datetime, timedelta
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        recent = [m for m in memories if m.get('timestamp', '') > cutoff]
        
        if not recent:
            return "近期没有新的记忆。"
        
        # 统计
        types = Counter(m.get('type', 'unknown') for m in recent)
        total = len(recent)
        
        # 提取重要记忆
        important = [m for m in recent if m.get('importance', 5) >= 8]
        
        # 生成总结
        summary = f"# 近期记忆总结 (过去{days}天)\n\n"
        summary += f"**总计**: {total} 条记忆\n\n"
        
        summary += "**类型分布**:\n"
        for t, count in types.most_common():
            summary += f"- {t}: {count} 条\n"
        
        if important:
            summary += f"\n**重要记忆** ({len(important)} 条):\n"
            for m in important:
                summary += f"- {m['content'][:100]}...\n"
        
        return summary
    
    def generate_insights(self):
        """生成洞察"""
        memories = self.store.get_all()
        
        if not memories:
            return "记忆库为空，暂无洞察。"
        
        # 分析主题
        all_content = ' '.join(m['content'] for m in memories)
        words = all_content.lower().split()
        word_freq = Counter(words)
        
        # 过滤常见词
        stop_words = {'的', '了', '是', '我', '你', '在', '和', '有', '就', '都', 'the', 'a', 'is', 'to'}
        keywords = {w: c for w, c in word_freq.items() if len(w) > 2 and w not in stop_words}
        
        insights = "# 记忆洞察\n\n"
        insights += "**高频主题**:\n"
        for word, count in Counter(keywords).most_common(10):
            insights += f"- {word}: {count} 次\n"
        
        # 情感分析（简单版本）
        positive_words = ['喜欢', '爱', '开心', '希望', '好', '成功']
        negative_words = ['害怕', '痛苦', '失去', '担心', '失败', '创伤']
        
        positive = sum(1 for m in memories if any(w in m['content'] for w in positive_words))
        negative = sum(1 for m in memories if any(w in m['content'] for w in negative_words))
        
        insights += f"\n**情感倾向**: 积极 {positive} 条, 消极 {negative} 条\n"
        
        return insights
