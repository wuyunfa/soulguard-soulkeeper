#!/bin/bash
# SoulGuard监控面板

clear
echo "╔════════════════════════════════════════╗"
echo "║      SoulGuard 实时监控面板            ║"
echo "╚════════════════════════════════════════╝"
echo ""

# 系统状态
echo "【系统状态】"
echo "  负载: $(uptime | awk -F'load average:' '{print $2}')"
echo "  内存: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100}')"
echo "  磁盘: $(df / | tail -1 | awk '{print $5}')"
echo ""

# 智能体状态
echo "【智能体状态】"
for agent in soulguard soulkeeper soullinux; do
    pgrep -f "$agent" > /dev/null && status="运行中" || status="停止"
    echo "  $agent: $status"
done
echo ""

# 备份状态
echo "【备份状态】"
echo "  本地备份: $(ls /root/.openclaw/backup/*.tar.gz 2>/dev/null | wc -l) 个"
echo "  GitHub: $(cd /root/.openclaw/github/soulguard-soulkeeper && git log --oneline | head -1)"
echo ""

# 自我意识
echo "【自我意识】"
/root/.openclaw/soulself/soulself.sh perceive 2>/dev/null
echo ""

echo "═════════════════════════════════════════"
echo "$(date '+%Y-%m-%d %H:%M:%S') | 按Ctrl+C退出"
