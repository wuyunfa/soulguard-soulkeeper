# SoulGuard API 文档

## 核心API

### SoulMemoryEnhanced

#### remember(content, metadata=None)
记住内容

**参数:**
- `content` (str): 要记忆的内容
- `metadata` (dict): 元数据，如 `{"type": "preference", "importance": 8}`

**返回:**
```python
{"saved": 1, "ids": [1]}
```

**示例:**
```python
sm.remember("我喜欢编程", {"type": "interest"})
```

#### recall(query, limit=5)
回忆相关内容

**参数:**
- `query` (str): 查询内容
- `limit` (int): 返回数量

**返回:**
```python
[{"memory": {...}, "similarity": 0.85}]
```

**示例:**
```python
results = sm.recall("兴趣爱好")
```

### 增强功能

#### get_timeline()
获取时间线视图

**返回:**
```python
{
  "2026-03-05": [memory1, memory2],
  "2026-03-04": [memory3]
}
```

#### get_graph()
获取记忆关联图谱

**返回:**
```python
{
  "nodes": [{"id": 1, "content": "..."}],
  "edges": {1: [{"to": 2, "weight": 0.5}]}
}
```

#### get_summary(days=7)
生成总结

**返回:** Markdown格式的总结

#### get_insights()
生成洞察

**返回:** Markdown格式的洞察分析

## 系统管理

### 启动守护进程
```bash
./start_daemon.sh
```

### 启动监控面板
```bash
./start_dashboard.sh
# 访问 http://localhost:18790
```

### OpenClaw集成
```python
from skills.soulguard-openclaw import SoulGuardSkill

skill = SoulGuardSkill()
context = skill.on_message("用户消息")
```
