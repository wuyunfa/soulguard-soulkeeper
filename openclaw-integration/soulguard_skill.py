#!/usr/bin/env python3
"""
SoulGuard OpenClaw Skill
自动记忆和回忆系统
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/soulguard')

from memory_core import SoulMemory

class SoulGuardSkill:
    """SoulGuard OpenClaw集成Skill"""
    
    def __init__(self):
        self.memory = SoulMemory("openclaw_user")
        self.user_context = {}
    
    def on_message(self, message, user_id="default"):
        """
        收到消息时调用
        1. 保存消息到记忆
        2. 检索相关记忆
        3. 返回上下文增强的回复
        """
        # 保存消息
        self.memory.remember(
            f"用户说: {message}",
            metadata={"type": "conversation", "user_id": user_id}
        )
        
        # 检索相关记忆
        related = self.memory.recall(message, limit=3)
        
        context = ""
        if related:
            context = "\n\n[相关记忆]\n"
            for r in related:
                mem = r["memory"]
                context += f"• {mem['content'][:50]}...\n"
        
        return context
    
    def get_sparks(self):
        """获取重要火花记忆"""
        return self.memory.get_sparks(limit=5)

# OpenClaw集成入口
def main():
    skill = SoulGuardSkill()
    
    # 测试
    print("SoulGuard Skill 已加载")
    print(f"当前记忆数: {len(skill.memory.vector_store.get_all())}")
    
    # 示例
    context = skill.on_message("我喜欢编程", user_id="test")
    print(f"上下文: {context}")

if __name__ == "__main__":
    main()
