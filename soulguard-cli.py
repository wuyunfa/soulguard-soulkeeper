#!/usr/bin/env python3
"""
SoulGuard CLI工具
"""

import sys
import argparse
sys.path.insert(0, '/root/.openclaw/soulguard')

from memory_core.enhanced import SoulMemoryEnhanced
from core.optimizer import MemoryOptimizer

def main():
    parser = argparse.ArgumentParser(description='SoulGuard CLI')
    subparsers = parser.add_subparsers(dest='command')
    
    # remember
    p_remember = subparsers.add_parser('remember', help='记住内容')
    p_remember.add_argument('content', help='要记忆的内容')
    p_remember.add_argument('--user', default='default', help='用户ID')
    
    # recall
    p_recall = subparsers.add_parser('recall', help='回忆内容')
    p_recall.add_argument('query', help='查询内容')
    p_recall.add_argument('--user', default='default', help='用户ID')
    
    # summary
    p_summary = subparsers.add_parser('summary', help='生成总结')
    p_summary.add_argument('--days', type=int, default=7, help='天数')
    p_summary.add_argument('--user', default='default', help='用户ID')
    
    # optimize
    p_opt = subparsers.add_parser('optimize', help='优化存储')
    
    args = parser.parse_args()
    
    if args.command == 'remember':
        sm = SoulMemoryEnhanced(args.user)
        result = sm.remember(args.content)
        print(f"✓ 已记住 {result['saved']} 条")
    
    elif args.command == 'recall':
        sm = SoulMemoryEnhanced(args.user)
        results = sm.recall(args.query)
        print(f"找到 {len(results)} 条相关记忆:")
        for r in results:
            print(f"  - {r['memory']['content'][:50]}...")
    
    elif args.command == 'summary':
        sm = SoulMemoryEnhanced(args.user)
        print(sm.get_summary(args.days))
    
    elif args.command == 'optimize':
        opt = MemoryOptimizer()
        opt.compress_old_memories()
        opt.cleanup_duplicates()
        print("✓ 优化完成")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
