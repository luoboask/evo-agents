#!/bin/bash
# setup-recommended-cron.sh - 设置推荐的定时任务组合
#
# 用法:
#   ./scripts/core/setup-recommended-cron.sh my-agent
#   ./scripts/core/setup-recommended-cron.sh my-agent --all  # 全部设置

set -e

AGENT_NAME="${1:-}"
MODE="${2:-interactive}"  # interactive / all / minimal
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [ -z "$AGENT_NAME" ]; then
    if [ -f "$WORKSPACE_ROOT/.install-config" ]; then
        AGENT_NAME=$(grep "^agent_name=" "$WORKSPACE_ROOT/.install-config" | cut -d'=' -f2)
    fi
fi

if [ -z "$AGENT_NAME" ]; then
    echo "❌ 错误：请指定 Agent 名称"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  设置推荐的定时任务组合                                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "📁 Workspace: $WORKSPACE_ROOT"
echo ""

# 定义任务
declare -A TASKS
TASKS=(
    ["scan"]="会话扫描定时任务 (每 60 分钟)"
    ["daily"]="每日回顾定时任务 (每天 09:00)"
    ["nightly"]="夜间进化循环 (每天 23:00)"
    ["weekly"]="每周记忆压缩 (每周日 03:00)"
    ["maintenance"]="每周系统维护 (每周日 02:00)"
)

# 显示任务列表
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 可选任务列表:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   1) 会话扫描定时任务 (每 60 分钟)"
echo "   2) 每日回顾定时任务 (每天 09:00)"
echo "   3) 夜间进化循环 (每天 23:00)"
echo "   4) 每周记忆压缩 (每周日 03:00)"
echo "   5) 每周系统维护 (每周日 02:00)"
echo "   6) ✅ 全部设置 (推荐)"
echo "   7) ❌ 跳过所有"
echo ""

# 选择模式
if [[ "$MODE" == "all" ]]; then
    SELECTED="1 2 3 4 5"
    echo "📌 模式：全部设置"
elif [[ "$MODE" == "minimal" ]]; then
    SELECTED="1 2"
    echo "📌 模式：最小设置 (仅会话扫描 + 每日回顾)"
else
    echo "请选择要设置的任务 (可多选，用空格分隔，如：1 2 3):"
    read -p "> " SELECTED
    
    if [[ "$SELECTED" == "7" ]]; then
        echo "已跳过所有定时任务"
        exit 0
    fi
    
    if [[ "$SELECTED" == "6" ]]; then
        SELECTED="1 2 3 4 5"
    fi
fi

echo ""
echo "已选择任务：$SELECTED"
echo ""

# 执行选择的任务
for task in $SELECTED; do
    case $task in
        1)
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "① 设置会话扫描定时任务"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            if [ -f "$WORKSPACE_ROOT/scripts/core/setup-cron.sh" ]; then
                bash "$WORKSPACE_ROOT/scripts/core/setup-cron.sh" "$AGENT_NAME" 60 || echo "   ⚠️  设置失败"
            fi
            ;;
        2)
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "② 设置每日回顾定时任务"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            if [ -f "$WORKSPACE_ROOT/scripts/core/setup-daily-review.sh" ]; then
                bash "$WORKSPACE_ROOT/scripts/core/setup-daily-review.sh" "$AGENT_NAME" "09:00" || echo "   ⚠️  设置失败"
            fi
            ;;
        3)
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "③ 设置夜间进化循环"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            # 添加 cron 任务
            CRON_CMD="0 23 * * * cd $WORKSPACE_ROOT && python3 skills/self-evolution/nightly_cycle.py >> logs/nightly_evolution.log 2>&1"
            (crontab -l 2>/dev/null | grep -v "nightly_cycle.py"; echo "$CRON_CMD") | crontab -
            echo "   ✅ 夜间进化循环已设置 (每天 23:00)"
            ;;
        4)
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "④ 设置每周记忆压缩"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            CRON_CMD="0 3 * * 0 cd $WORKSPACE_ROOT && python3 scripts/core/memory_compressor.py --weekly --monthly >> logs/memory_compress.log 2>&1"
            (crontab -l 2>/dev/null | grep -v "memory_compressor.py"; echo "$CRON_CMD") | crontab -
            echo "   ✅ 每周记忆压缩已设置 (每周日 03:00)"
            ;;
        5)
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "⑤ 设置每周系统维护"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            CRON_CMD="0 2 * * 0 cd $WORKSPACE_ROOT && bash skills/memory-search/maintenance.sh >> logs/system_maintenance.log 2>&1"
            (crontab -l 2>/dev/null | grep -v "maintenance.sh"; echo "$CRON_CMD") | crontab -
            echo "   ✅ 每周系统维护已设置 (每周日 02:00)"
            ;;
        *)
            echo "⚠️  未知选项：$task"
            ;;
    esac
    echo ""
done

# 验证
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 当前 cron 任务列表:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
crontab -l 2>/dev/null | grep -E "(scan_sessions|daily_review|nightly_cycle|memory_compressor|maintenance)" || echo "   (无)"
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 定时任务设置完成！                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 日志文件:"
echo "   - 会话扫描：$WORKSPACE_ROOT/logs/session_scan.log"
echo "   - 每日回顾：$WORKSPACE_ROOT/logs/daily_review.log"
echo "   - 夜间进化：$WORKSPACE_ROOT/logs/nightly_evolution.log"
echo "   - 记忆压缩：$WORKSPACE_ROOT/logs/memory_compress.log"
echo "   - 系统维护：$WORKSPACE_ROOT/logs/system_maintenance.log"
echo ""
echo "🔧 管理命令:"
echo "   # 查看所有 cron 任务"
echo "   crontab -l"
echo ""
echo "   # 查看日志"
echo "   tail -f $WORKSPACE_ROOT/logs/session_scan.log"
echo ""
