# SoulGuard Memory Architecture

## 借鉴mem0的核心设计

### 两阶段记忆管道
1. **提取阶段 (Extraction)**
   - 从对话中提取关键事实
   - 识别4种记忆类型：preference/fact/trauma/spark
   - 自动计算重要性分数

2. **更新阶段 (Update)**
   - 语义去重（相似度>0.8合并）
   - 更新计数和时间戳
   - 动态重要性调整

### 向量语义检索
- **TF-IDF向量表示**
- **余弦相似度计算**
- **语义搜索 + 关键词降级**

### 核心功能
| 功能 | 说明 |
|-----|------|
| `remember()` | 记住内容，自动提取和去重 |
| `recall()` | 语义检索相关记忆 |
| `get_sparks()` | 获取重要火花记忆 |
| `get_related()` | 获取相关记忆推荐 |

### 使用示例
```python
from soulguard.memory_core import SoulMemory

sm = SoulMemory("wuyunfa")

# 记住
sm.remember("我喜欢编程", metadata={"type": "preference"})

# 回忆
results = sm.recall("兴趣爱好", use_semantic=True)

# 获取火花
sparks = sm.get_sparks()
```
