#!/bin/bash
# 启动SoulGuard守护进程

echo "启动SoulGuard系统守护进程..."

# 检查Python路径
export PYTHONPATH=/root/.openclaw/soulguard:$PYTHONPATH

# 启动守护进程
nohup python3 -c "
import sys
sys.path.insert(0, '/root/.openclaw/soulguard')
from core.daemon import SoulGuardDaemon
daemon = SoulGuardDaemon()
daemon.start()
" > /root/.openclaw/soulguard/logs/daemon_output.log 2>&1 &

echo $! > /root/.openclaw/soulguard/daemon.pid
echo "✓ 守护进程已启动 (PID: $(cat /root/.openclaw/soulguard/daemon.pid))"
