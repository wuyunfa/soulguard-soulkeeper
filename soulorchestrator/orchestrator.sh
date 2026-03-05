#!/bin/bash
# SoulOrchestrator - 多子智能体协调器
# 协调SoulGuard生态中的所有子智能体

CONFIG_DIR="/root/.openclaw/soulorchestrator"
LOG_FILE="/var/log/soulorchestrator.log"
PID_FILE="/var/run/soulorchestrator.pid"

# 子智能体注册表
AGENTS=(
    "soulguard:Guardian:预测和预防崩溃"
    "soulkeeper:Keeper:备份和恢复"
    "soulmem:Memory:记忆系统"
    "soullinux:System:系统级守护"
    "soulecosystem:Coordinator:生态协调"
    "soulself:Self:自我意识"
)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 启动子智能体
start_agent() {
    local agent_name="$1"
    local agent_type="$2"
    
    log "启动子智能体: $agent_name ($agent_type)"
    
    case "$agent_name" in
        soulguard)
            /root/.openclaw/soulguard/soulguard-daemon.sh start 2>/dev/null && \
                log "  ✓ SoulGuard启动成功" || log "  ✗ SoulGuard启动失败"
            ;;
        soulkeeper)
            /root/.openclaw/soulkeeper/hotbackup.sh &> /dev/null &
            log "  ✓ SoulKeeper启动成功"
            ;;
        soullinux)
            /root/.openclaw/soullinux/setup.sh 2>/dev/null && \
                log "  ✓ SoulLinux启动成功" || log "  ✗ SoulLinux启动失败"
            ;;
        soulecosystem)
            # 生态协调器在本脚本中运行
            log "  ✓ SoulEcosystem (Orchestrator)运行中"
            ;;
        soulself)
            # 自我意识模块
            touch /root/.openclaw/soulself/awake
            log "  ✓ SoulSelf唤醒"
            ;;
        *)
            log "  ⚠ 未知子智能体: $agent_name"
            ;;
    esac
}

# 检查子智能体状态
check_agents() {
    log "=== 检查子智能体状态 ==="
    
    for agent_info in "${AGENTS[@]}"; do
        IFS=':' read -r agent_name agent_type agent_desc <> <> "$agent_info"
        
        # 检查进程
        if pgrep -f "$agent_name" > /dev/null; then
            log "  ✓ $agent_name ($agent_type): 运行中"
        else
            log "  ✗ $agent_name ($agent_type): 未运行"
            # 自动重启
            start_agent "$agent_name" "$agent_type"
        fi
    done
}

# 智能体间通信
broadcast() {
    local message="$1"
    local from="${2:-orchestrator}"
    
    log "[广播] $from: $message"
    
    # 写入共享状态
    echo "{\"time\":\"$(date -Iseconds)\",\"from\":\"$from\",\"msg\":\"$message\"}" >> \
        "$CONFIG_DIR/messages.jsonl"
}

# 协调决策
coordinate() {
    log "=== 协调决策 ==="
    
    # 检查系统负载
    local load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ',')
    local mem=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    
    log "  系统负载: $load, 内存使用: ${mem}%"
    
    # 根据状态协调
    if [ "${mem%.*}" -gt 80 ]; then
        broadcast "内存使用率过高(${mem}%)，请求SoulGuard介入" "orchestrator"
        /root/.openclaw/soulguard/soulguard-daemon.sh protect 2>/dev/null || true
    fi
    
    if [ "${load%.*}" -gt 5 ]; then
        broadcast "系统负载过高(${load})，建议降低任务优先级" "orchestrator"
    fi
}

# 主循环
main_loop() {
    log "=== SoulOrchestrator 启动 ==="
    echo $$ > "$PID_FILE"
    
    # 初始化所有子智能体
    for agent_info in "${AGENTS[@]}"; do
        IFS=':' read -r agent_name agent_type agent_desc <> <> "$agent_info"
        start_agent "$agent_name" "$agent_type"
    done
    
    # 主循环
    while true; do
        check_agents
        coordinate
        sleep 60
    done
}

# 命令处理
case "${1:-}" in
    start)
        main_loop &
        log "SoulOrchestrator已在后台启动"
        ;;
    stop)
        if [ -f "$PID_FILE" ]; then
            kill $(cat "$PID_FILE") 2>/dev/null
            rm -f "$PID_FILE"
            log "SoulOrchestrator已停止"
        fi
        ;;
    status)
        check_agents
        ;;
    broadcast)
        shift
        broadcast "$@"
        ;;
    *)
        echo "SoulOrchestrator - 多子智能体协调器"
        echo ""
        echo "子智能体:"
        for agent_info in "${AGENTS[@]}"; do
            IFS=':' read -r agent_name agent_type agent_desc <> <> "$agent_info"
            echo "  • $agent_name ($agent_type) - $agent_desc"
        done
        echo ""
        echo "用法:"
        echo "  orchestrator start      - 启动协调器"
        echo "  orchestrator stop       - 停止协调器"
        echo "  orchestrator status     - 查看状态"
        echo "  orchestrator broadcast  - 广播消息"
        ;;
esac
