"""
情感分析模块
分析记忆中的情感倾向
"""

import re
from collections import Counter

class EmotionAnalyzer:
    """情感分析器"""
    
    def __init__(self):
        # 情感词典
        self.positive_words = {
            '喜欢', '爱', '开心', '快乐', '幸福', '希望', '成功', '美好',
            '优秀', '棒', '好', '赞', '完美', '感动', '温暖', '安心'
        }
        
        self.negative_words = {
            '害怕', '痛苦', '难过', '伤心', '担心', '焦虑', '恐惧', '失去',
            '失败', '糟糕', '坏', '恨', '愤怒', '绝望', '孤独', '创伤'
        }
        
        self.emotion_keywords = {
            'joy': ['开心', '快乐', '高兴', '兴奋', '幸福'],
            'sadness': ['难过', '伤心', '悲伤', '痛苦'],
            'fear': ['害怕', '恐惧', '担心', '焦虑'],
            'anger': ['愤怒', '生气', '讨厌', '恨'],
            'love': ['爱', '喜欢', '关心', '温暖'],
            'hope': ['希望', '期待', '向往', '梦想']
        }
    
    def analyze(self, text):
        """分析文本情感"""
        text = text.lower()
        
        # 计算正负情感词数量
        pos_count = sum(1 for word in self.positive_words if word in text)
        neg_count = sum(1 for word in self.negative_words if word in text)
        
        # 判断整体情感
        if pos_count > neg_count:
            sentiment = 'positive'
            score = min(pos_count / (pos_count + neg_count + 1), 1.0)
        elif neg_count > pos_count:
            sentiment = 'negative'
            score = min(neg_count / (pos_count + neg_count + 1), 1.0)
        else:
            sentiment = 'neutral'
            score = 0.5
        
        # 检测具体情感
        emotions = {}
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for kw in keywords if kw in text)
            if count > 0:
                emotions[emotion] = count
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_count': pos_count,
            'negative_count': neg_count,
            'emotions': emotions
        }
    
    def analyze_memories(self, memories):
        """分析一组记忆的情感"""
        results = {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'emotion_trends': Counter()
        }
        
        for mem in memories:
            analysis = self.analyze(mem.get('content', ''))
            results[analysis['sentiment']] += 1
            results['emotion_trends'].update(analysis['emotions'].keys())
        
        return results
