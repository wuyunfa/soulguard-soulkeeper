# SoulGuard Core - 预测算法模块
# 实时监控趋势，预测崩溃，提前干预

import os
import sys
import time
import json
import psutil
import logging
from datetime import datetime, timedelta
from collections import deque

# 配置
CONFIG = {
    'memory_threshold': 500,  # MB
    'cpu_threshold': 80,      # %
    'prediction_window': 30,  # 秒
    'trend_samples': 10,      # 采样数
    'intervention_threshold': 0.7,  # 干预阈值
}

class MemoryPredictor:
    """内存使用趋势预测器"""
    
    def __init__(self, window_size=10):
        self.samples = deque(maxlen=window_size)
        self.timestamps = deque(maxlen=window_size)
    
    def add_sample(self, mem_used_mb):
        """添加内存使用样本"""
        self.samples.append(mem_used_mb)
        self.timestamps.append(time.time())
    
    def predict(self, seconds_ahead=30):
        """预测未来内存使用"""
        if len(self.samples) < 3:
            return None, 0
        
        # 计算趋势
        recent = list(self.samples)[-5:]
        trend = (recent[-1] - recent[0]) / len(recent) if len(recent) > 1 else 0
        
        # 预测
        current = self.samples[-1]
        predicted = current + trend * seconds_ahead
        
        # 计算置信度
        confidence = min(len(self.samples) / 10, 1.0)
        
        return predicted, confidence
    
    def get_trend(self):
        """获取当前趋势"""
        if len(self.samples) < 2:
            return 0
        
        recent = list(self.samples)[-5:]
        return (recent[-1] - recent[0]) / len(recent)


class CPUPredictor:
    """CPU使用趋势预测器"""
    
    def __init__(self, window_size=10):
        self.samples = deque(maxlen=window_size)
    
    def add_sample(self, cpu_percent):
        """添加CPU使用样本"""
        self.samples.append(cpu_percent)
    
    def predict(self, seconds_ahead=30):
        """预测未来CPU使用"""
        if len(self.samples) < 3:
            return None, 0
        
        # 计算平均趋势
        avg = sum(self.samples) / len(self.samples)
        max_val = max(self.samples)
        
        # 预测（保守估计）
        predicted = max_val + (max_val - avg) * 0.5
        
        confidence = min(len(self.samples) / 10, 1.0)
        
        return predicted, confidence


class CrashPredictor:
    """崩溃预测器 - 整合多种指标"""
    
    def __init__(self):
        self.mem_predictor = MemoryPredictor()
        self.cpu_predictor = CPUPredictor()
        self.risk_score = 0.0
        self.last_intervention = 0
        
    def collect_metrics(self):
        """收集系统指标"""
        # 内存
        mem = psutil.virtual_memory()
        mem_used_mb = (mem.total - mem.available) / 1024 / 1024
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 添加样本
        self.mem_predictor.add_sample(mem_used_mb)
        self.cpu_predictor.add_sample(cpu_percent)
        
        return {
            'mem_used_mb': mem_used_mb,
            'mem_percent': mem.percent,
            'cpu_percent': cpu_percent,
            'timestamp': time.time()
        }
    
    def calculate_risk(self, metrics):
        """计算崩溃风险分数 (0-1)"""
        risks = []
        
        # 内存风险
        mem_free_mb = (psutil.virtual_memory().available / 1024 / 1024)
        if mem_free_mb < CONFIG['memory_threshold']:
            mem_risk = 1.0 - (mem_free_mb / CONFIG['memory_threshold'])
            risks.append(mem_risk)
        
        # 内存趋势风险
        mem_predicted, mem_conf = self.mem_predictor.predict(CONFIG['prediction_window'])
        if mem_predicted and mem_conf > 0.5:
            mem_total_mb = psutil.virtual_memory().total / 1024 / 1024
            if mem_predicted > mem_total_mb * 0.9:
                trend_risk = (mem_predicted - mem_total_mb * 0.9) / (mem_total_mb * 0.1)
                risks.append(min(trend_risk, 1.0) * mem_conf)
        
        # CPU风险
        if metrics['cpu_percent'] > CONFIG['cpu_threshold']:
            cpu_risk = (metrics['cpu_percent'] - CONFIG['cpu_threshold']) / (100 - CONFIG['cpu_threshold'])
            risks.append(cpu_risk)
        
        # 综合风险分数
        if risks:
            self.risk_score = max(risks)  # 取最大风险
        else:
            self.risk_score = 0.0
        
        return self.risk_score
    
    def should_intervene(self):
        """判断是否需要干预"""
        # 避免频繁干预
        if time.time() - self.last_intervention < 60:
            return False
        
        return self.risk_score > CONFIG['intervention_threshold']
    
    def get_recommendation(self):
        """获取干预建议"""
        recommendations = []
        
        # 内存相关建议
        mem_trend = self.mem_predictor.get_trend()
        if mem_trend > 10:  # 每秒增加10MB
            recommendations.append({
                'type': 'memory',
                'action': 'clean_chrome',
                'priority': 'high',
                'reason': f'内存快速增长: {mem_trend:.1f}MB/s'
            })
        
        # CPU相关建议
        if self.cpu_predictor.samples and max(self.cpu_predictor.samples) > 90:
            recommendations.append({
                'type': 'cpu',
                'action': 'reduce_load',
                'priority': 'medium',
                'reason': 'CPU使用率过高'
            })
        
        return recommendations


class InterventionExecutor:
    """干预执行器"""
    
    def __init__(self):
        self.actions_log = []
    
    def execute(self, recommendation):
        """执行干预措施"""
        action = recommendation['action']
        result = {'action': action, 'timestamp': time.time(), 'success': False}
        
        try:
            if action == 'clean_chrome':
                result['success'] = self._kill_chrome()
            elif action == 'reduce_load':
                result['success'] = self._reduce_load()
            elif action == 'clear_cache':
                result['success'] = self._clear_cache()
            
            result['details'] = f"执行成功: {action}"
        except Exception as e:
            result['details'] = f"执行失败: {str(e)}"
        
        self.actions_log.append(result)
        return result
    
    def _kill_chrome(self):
        """清理Chrome进程"""
        import subprocess
        try:
            subprocess.run(['pkill', '-9', 'chrome'], check=False)
            return True
        except:
            return False
    
    def _reduce_load(self):
        """降低系统负载"""
        # 降低进程优先级
        try:
            os.nice(10)
            return True
        except:
            return False
    
    def _clear_cache(self):
        """清理缓存"""
        try:
            import subprocess
            subprocess.run(['sync'], check=False)
            # 清理文件系统缓存需要root权限
            return True
        except:
            return False


# 主函数
def main():
    """SoulGuard核心守护循环"""
    predictor = CrashPredictor()
    executor = InterventionExecutor()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/log/soulguard-core.log'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("SoulGuard Core 启动")
    
    while True:
        try:
            # 收集指标
            metrics = predictor.collect_metrics()
            
            # 计算风险
            risk = predictor.calculate_risk(metrics)
            
            # 记录状态
            logging.info(f"内存: {metrics['mem_used_mb']:.0f}MB ({metrics['mem_percent']}%), "
                        f"CPU: {metrics['cpu_percent']}%, 风险: {risk:.2f}")
            
            # 判断是否需要干预
            if predictor.should_intervene():
                recommendations = predictor.get_recommendation()
                
                for rec in recommendations:
                    if rec['priority'] == 'high':
                        logging.warning(f"高风险! 执行干预: {rec['action']} - {rec['reason']}")
                        result = executor.execute(rec)
                        predictor.last_intervention = time.time()
                        
                        if result['success']:
                            logging.info(f"干预成功: {rec['action']}")
                        else:
                            logging.error(f"干预失败: {result['details']}")
            
            # 保存状态
            status = {
                'timestamp': time.time(),
                'metrics': metrics,
                'risk_score': risk,
                'recommendations': predictor.get_recommendation()
            }
            
            with open('/tmp/soulguard-status.json', 'w') as f:
                json.dump(status, f)
            
        except Exception as e:
            logging.error(f"错误: {str(e)}")
        
        time.sleep(5)  # 每5秒检查一次


if __name__ == '__main__':
    main()
