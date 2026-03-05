"""
AI模式识别器
自动识别用户行为模式和偏好
"""

import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta

class PatternRecognizer:
    """用户行为模式识别"""
    
    def __init__(self, vector_store):
        self.store = vector_store
        self.patterns = defaultdict(list)
    
    def analyze_user_patterns(self, user_id, days=30):
        """分析用户行为模式"""
        memories = self.store.get_all()
        recent = [
            m for m in memories 
            if (datetime.now() - datetime.fromisoformat(m.get('timestamp', '2000-01-01'))).days <= days
        ]
        
        patterns = {
            'active_hours': self._analyze_active_hours(recent),
            'topic_preferences': self._analyze_topics(recent),
            'emotional_trends': self._analyze_emotions(recent),
            'interaction_frequency': self._analyze_frequency(recent)
        }
        
        return patterns
    
    def _analyze_active_hours(self, memories):
        """分析活跃时间"""
        hours = [datetime.fromisoformat(m['timestamp']).hour for m in memories if 'timestamp' in m]
        if not hours:
            return {}
        return dict(Counter(hours).most_common(5))
    
    def _analyze_topics(self, memories):
        """分析话题偏好"""
        topics = []
        for m in memories:
            content = m.get('content', '')
            # 提取关键词
            words = [w for w in content.split() if len(w) >= 2]
            topics.extend(words[:3])
        return dict(Counter(topics).most_common(10))
    
    def _analyze_emotions(self, memories):
        """分析情感趋势"""
        emotions = []
        for m in memories:
            emotion = m.get('metadata', {}).get('emotion')
            if emotion:
                emotions.append(emotion)
        return dict(Counter(emotions))
    
    def _analyze_frequency(self, memories):
        """分析互动频率"""
        if not memories:
            return {'daily_average': 0}
        
        dates = set()
        for m in memories:
            if 'timestamp' in m:
                dates.add(m['timestamp'][:10])
        
        total_days = (datetime.now() - datetime.fromisoformat(memories[0]['timestamp'])).days + 1
        daily_avg = len(memories) / max(total_days, 1)
        
        return {
            'daily_average': round(daily_avg, 2),
            'active_days': len(dates),
            'total_memories': len(memories)
        }
    
    def predict_needs(self, user_id):
        """预测用户需求"""
        patterns = self.analyze_user_patterns(user_id)
        
        predictions = []
        
        # 基于活跃时间预测
        if patterns.get('active_hours'):
            peak_hour = max(patterns['active_hours'], key=patterns['active_hours'].get)
            predictions.append(f"用户通常在 {peak_hour}:00 左右活跃")
        
        # 基于话题偏好预测
        if patterns.get('topic_preferences'):
            top_topic = list(patterns['topic_preferences'].keys())[0]
            predictions.append(f"用户对 '{top_topic}' 话题最感兴趣")
        
        # 基于情感趋势预测
        emotions = patterns.get('emotional_trends', {})
        if emotions:
            dominant = max(emotions, key=emotions.get)
            predictions.append(f"近期情感倾向: {dominant}")
        
        return predictions
