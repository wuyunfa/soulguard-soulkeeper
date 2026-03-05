#!/bin/bash
# 启动SoulGuard监控面板

echo "启动SoulGuard Dashboard..."
export PYTHONPATH=/root/.openclaw/soulguard:$PYTHONPATH

nohup python3 /root/.openclaw/soulguard/dashboard/app.py > /root/.openclaw/soulguard/logs/dashboard.log 2>&1 &
echo $! > /root/.openclaw/soulguard/dashboard.pid

echo "✓ Dashboard已启动"
echo "  访问: http://localhost:18790"
