#!/bin/bash
# SoulGuard OpenClaw Skill安装脚本

echo "=== 安装SoulGuard OpenClaw Skill ==="

# 检查依赖
if [ ! -d "/root/.openclaw/soulguard" ]; then
    echo "✗ SoulGuard未安装"
    exit 1
fi

echo "✓ 依赖检查通过"

# 创建skill链接
mkdir -p /root/.openclaw/skills/soulguard-openclay
ln -sf /root/.openclaw/skills/soulguard-openclaw/soulguard_skill.py \
       /root/.openclaw/skills/soulguard-openclay/

echo "✓ Skill链接创建"

# 添加到OpenClaw启动
echo ""
echo "安装完成！"
echo "使用方法:"
echo "  from skills.soulguard-openclaw.soulguard_skill import SoulGuardSkill"
echo "  skill = SoulGuardSkill()"
