"""
记忆时间线视图
"""

from datetime import datetime
from collections import defaultdict

class MemoryTimeline:
    """记忆时间线管理"""
    
    def __init__(self, vector_store):
        self.store = vector_store
    
    def get_timeline(self, start_date=None, end_date=None):
        """获取时间线视图"""
        memories = self.store.get_all()
        
        # 按日期分组
        timeline = defaultdict(list)
        
        for mem in memories:
            timestamp = mem.get('timestamp', '')
            if timestamp:
                date = timestamp[:10]  # YYYY-MM-DD
                timeline[date].append(mem)
        
        # 排序
        sorted_timeline = dict(sorted(timeline.items(), reverse=True))
        
        return sorted_timeline
    
    def get_daily_summary(self, date):
        """获取每日摘要"""
        timeline = self.get_timeline()
        memories = timeline.get(date, [])
        
        if not memories:
            return None
        
        # 分类统计
        types = defaultdict(int)
        for m in memories:
            types[m.get('type', 'unknown')] += 1
        
        return {
            "date": date,
            "total": len(memories),
            "types": dict(types),
            "highlights": [m for m in memories if m.get('importance', 5) >= 8][:3]
        }
    
    def export_timeline(self, format='json'):
        """导出时间线"""
        timeline = self.get_timeline()
        
        if format == 'json':
            import json
            return json.dumps(timeline, indent=2, ensure_ascii=False)
        elif format == 'markdown':
            md = "# 记忆时间线\n\n"
            for date, memories in timeline.items():
                md += f"## {date}\n\n"
                for m in memories:
                    md += f"- {m['content'][:100]}...\n"
                md += "\n"
            return md
        
        return timeline
