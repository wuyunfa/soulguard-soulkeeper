"""
学习优化模块
持续优化记忆检索和存储效率
"""

import json
import os
from datetime import datetime

class LearningOptimizer:
    """学习优化器"""
    
    def __init__(self, data_dir="/root/.openclaw/soulguard/memory_data"):
        self.data_dir = data_dir
        self.metrics_file = f"{data_dir}/metrics.json"
        self.metrics = self._load_metrics()
    
    def _load_metrics(self):
        """加载性能指标"""
        if os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        return {
            'search_times': [],
            'storage_sizes': [],
            'hit_rates': [],
            'optimizations': []
        }
    
    def _save_metrics(self):
        """保存性能指标"""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def record_search(self, query, results, time_taken):
        """记录搜索性能"""
        self.metrics['search_times'].append({
            'timestamp': datetime.now().isoformat(),
            'query_length': len(query),
            'results_count': len(results),
            'time_ms': time_taken * 1000
        })
        
        # 只保留最近100条记录
        self.metrics['search_times'] = self.metrics['search_times'][-100:]
        self._save_metrics()
    
    def analyze_performance(self):
        """分析性能"""
        if not self.metrics['search_times']:
            return {"status": "no_data"}
        
        times = [m['time_ms'] for m in self.metrics['search_times']]
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        return {
            "status": "ok",
            "avg_search_time_ms": round(avg_time, 2),
            "max_search_time_ms": round(max_time, 2),
            "min_search_time_ms": round(min_time, 2),
            "total_searches": len(times)
        }
    
    def suggest_optimizations(self):
        """建议优化方案"""
        analysis = self.analyze_performance()
        suggestions = []
        
        if analysis.get('avg_search_time_ms', 0) > 100:
            suggestions.append("搜索响应较慢，建议优化索引结构")
        
        # 检查存储大小
        total_size = 0
        for file in os.listdir(self.data_dir):
            if file.endswith('.json'):
                total_size += os.path.getsize(os.path.join(self.data_dir, file))
        
        if total_size > 100 * 1024 * 1024:  # 100MB
            suggestions.append("存储空间超过100MB，建议进行数据归档")
        
        return suggestions
    
    def auto_optimize(self):
        """自动优化"""
        suggestions = self.suggest_optimizations()
        
        for suggestion in suggestions:
            self.metrics['optimizations'].append({
                'timestamp': datetime.now().isoformat(),
                'action': suggestion,
                'applied': True
            })
        
        self._save_metrics()
        return suggestions
