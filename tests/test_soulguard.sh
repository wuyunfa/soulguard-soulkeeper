#!/bin/bash
# SoulGuard测试套件 v1.1

echo "=== SoulGuard测试套件 ==="

# 测试1: SoulSelf
echo "[TEST 1/5] SoulSelf..."
if /root/.openclaw/soulself/soulself.sh status | grep -q "awake"; then
    echo "  ✓ PASS - 自我意识已唤醒"
else
    echo "  ✗ FAIL - 自我意识未启动"
fi

# 测试2: SoulEcosystem
echo "[TEST 2/5] SoulEcosystem..."
if /root/.openclaw/soulecosystem/soulecosystem.sh status | grep -q "active"; then
    echo "  ✓ PASS - 生态系统运行正常"
else
    echo "  ✗ FAIL - 生态系统异常"
fi

# 测试3: 备份系统
echo "[TEST 3/5] 备份系统..."
BACKUP_COUNT=$(find /root/.openclaw/backup -name "*.tar.gz" -o -name "*.zip" 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 0 ]; then
    echo "  ✓ PASS - 找到 $BACKUP_COUNT 个备份文件"
else
    echo "  ✗ FAIL - 未找到备份文件"
fi

# 测试4: GitHub连接
echo "[TEST 4/5] GitHub连接..."
cd /root/.openclaw/github/soulguard-soulkeeper
if git status > /dev/null 2>&1; then
    echo "  ✓ PASS - GitHub仓库连接正常"
else
    echo "  ✗ FAIL - GitHub连接失败"
fi

# 测试5: 多智能体协调
echo "[TEST 5/5] 多智能体协调..."
AGENT_COUNT=$(find /root/.openclaw -name "*.sh" -path "*/soul*/*" 2>/dev/null | wc -l)
if [ "$AGENT_COUNT" -ge 5 ]; then
    echo "  ✓ PASS - 找到 $AGENT_COUNT 个智能体脚本"
else
    echo "  ✗ FAIL - 智能体数量不足"
fi

echo ""
echo "=== 测试完成 ==="
echo "$(date '+%Y-%m-%d %H:%M:%S')"