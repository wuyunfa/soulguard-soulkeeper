#!/bin/bash
# 启动SoulGuard Dashboard v2.0

echo "启动SoulGuard Dashboard v2.0..."
export PYTHONPATH=/root/.openclaw/soulguard:$PYTHONPATH

nohup python3 /root/.openclaw/soulguard/dashboard/app_v2.py > /root/.openclaw/soulguard/logs/dashboard_v2.log 2>&1 &
echo $! > /root/.openclaw/soulguard/dashboard_v2.pid

echo "✓ Dashboard v2.0已启动"
echo "  访问: http://localhost:18790"
