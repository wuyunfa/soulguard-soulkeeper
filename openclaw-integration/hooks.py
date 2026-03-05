#!/usr/bin/env python3
"""
OpenClaw消息钩子
自动记忆所有对话
"""

import sys
sys.path.insert(0, '/root/.openclaw/soulguard')
from memory_core import SoulMemory

_memory = None

def get_memory():
    global _memory
    if _memory is None:
        _memory = SoulMemory("openclaw_session")
    return _memory

def on_user_message(message, context=None):
    """用户发送消息时调用"""
    memory = get_memory()
    memory.remember(
        message,
        metadata={"type": "user_message", "context": context}
    )
    return True

def on_assistant_response(response, context=None):
    """助手回复时调用"""
    memory = get_memory()
    memory.remember(
        response,
        metadata={"type": "assistant_response", "context": context}
    )
    return True

def get_context_for_query(query, limit=3):
    """获取查询的相关上下文"""
    memory = get_memory()
    results = memory.recall(query, limit=limit)
    
    if not results:
        return ""
    
    context = "根据之前的对话:\n"
    for r in results:
        mem = r["memory"]
        context += f"- {mem['content'][:80]}...\n"
    
    return context
