#!/bin/bash
# SoulGuard测试套件

echo "=== SoulGuard测试套件 ==="

# 测试1: SoulSelf
echo "[TEST] SoulSelf..."
/root/.openclaw/soulself/soulself.sh status | grep -q "awake" && echo "  ✓ PASS" || echo "  ✗ FAIL"

# 测试2: SoulEcosystem
echo "[TEST] SoulEcosystem..."
/root/.openclaw/soulecosystem/soulecosystem.sh status | grep -q "active" && echo "  ✓ PASS" || echo "  ✗ FAIL"

# 测试3: 备份系统
echo "[TEST] 备份系统..."
[ -f /root/.openclaw/backup/sync-*.tar.gz ] && echo "  ✓ PASS" || echo "  ✗ FAIL"

# 测试4: GitHub连接
echo "[TEST] GitHub连接..."
cd /root/.openclaw/github/soulguard-soulkeeper
git status > /dev/null 2>&1 && echo "  ✓ PASS" || echo "  ✗ FAIL"

echo ""
echo "=== 测试完成 ==="
