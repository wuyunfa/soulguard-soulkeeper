# SoulGuard 使用教程

## 快速开始

### 1. 安装

```bash
git clone https://github.com/wuyunfa/soulguard-soulkeeper.git
cd soulguard-soulkeeper
```

### 2. 基础使用

```python
from soulguard.memory_core.enhanced import SoulMemoryEnhanced

# 创建记忆系统
sm = SoulMemoryEnhanced("my_user")

# 记住内容
sm.remember("我喜欢Python编程")

# 回忆
results = sm.recall("编程")
```

### 3. 查看时间线

```python
timeline = sm.get_timeline()
for date, memories in timeline.items():
    print(f"{date}: {len(memories)} 条记忆")
```

### 4. 生成总结

```python
summary = sm.get_summary(days=7)
print(summary)
```

## 高级用法

### 自定义重要性

```python
sm.remember(
    "这是重要记忆",
    metadata={"importance": 10, "type": "spark"}
)
```

### 导出图谱

```python
graph = sm.get_graph()
# 使用Graphviz可视化
```

## 系统监控

访问 `http://localhost:18790` 查看实时监控面板。
