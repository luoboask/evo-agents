#!/bin/bash
# setup-cron.sh - 设置会话扫描定时任务
#
# 用法:
#   ./scripts/core/setup-cron.sh my-agent
#   ./scripts/core/setup-cron.sh my-agent --interval 30  # 30 分钟

set -e

AGENT_NAME="${1:-}"
INTERVAL_MINUTES="${2:-60}"  # 默认 60 分钟
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [ -z "$AGENT_NAME" ]; then
    # 尝试从 .install-config 读取
    if [ -f "$WORKSPACE_ROOT/.install-config" ]; then
        AGENT_NAME=$(grep "^agent_name=" "$WORKSPACE_ROOT/.install-config" | cut -d'=' -f2)
    fi
fi

if [ -z "$AGENT_NAME" ]; then
    echo "❌ 错误：请指定 Agent 名称或确保 .install-config 存在"
    echo "用法：$0 <agent-name> [interval-minutes]"
    exit 1
fi

SCAN_SCRIPT="$WORKSPACE_ROOT/scripts/core/scan_sessions.py"
PYTHON_CMD="python3"

# 检查 Python 和脚本
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ 错误：找不到 python3"
    exit 1
fi

if [ ! -f "$SCAN_SCRIPT" ]; then
    echo "❌ 错误：找不到扫描脚本 $SCAN_SCRIPT"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  设置会话扫描定时任务                                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "⏰ 间隔：$INTERVAL_MINUTES 分钟"
echo "📁 Workspace: $WORKSPACE_ROOT"
echo ""

# 创建 cron 表达式
CRON_EXPR="*/$INTERVAL_MINUTES * * * *"

# 创建 cron 命令
CRON_CMD="$CRON_CMD cd $WORKSPACE_ROOT && $PYTHON_CMD $SCAN_SCRIPT --agent $AGENT_NAME >> $WORKSPACE_ROOT/logs/session_scan.log 2>&1"

# 检查 crontab 是否已存在
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -c "scan_sessions.py.*$AGENT_NAME" || echo "0")

if [ "$EXISTING_CRON" -gt 0 ]; then
    echo "⚠️  定时任务已存在"
    echo ""
    read -p "是否更新？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 0
    fi
    # 删除旧的 cron 任务
    crontab -l 2>/dev/null | grep -v "scan_sessions.py.*$AGENT_NAME" | crontab -
    echo "   ✅ 已删除旧任务"
fi

# 创建日志目录
mkdir -p "$WORKSPACE_ROOT/logs"
touch "$WORKSPACE_ROOT/logs/session_scan.log"

# 添加新的 cron 任务
echo "📝 添加定时任务..."
(crontab -l 2>/dev/null | grep -v "scan_sessions.py.*$AGENT_NAME"; echo "$CRON_CMD") | crontab -
echo "   ✅ 完成"

# 验证
echo ""
echo "📋 当前 cron 任务列表:"
crontab -l 2>/dev/null | grep "scan_sessions.py" || echo "   (无)"

# 测试运行
echo ""
echo "🧪 测试运行扫描脚本..."
cd "$WORKSPACE_ROOT"
$PYTHON_CMD $SCAN_SCRIPT --agent "$AGENT_NAME" --cleanup-days 0
echo "   ✅ 测试完成"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 定时任务设置完成！                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 日志文件：$WORKSPACE_ROOT/logs/session_scan.log"
echo ""
echo "🔧 管理命令:"
echo "   # 查看日志"
echo "   tail -f $WORKSPACE_ROOT/logs/session_scan.log"
echo ""
echo "   # 手动运行"
echo "   cd $WORKSPACE_ROOT && $PYTHON_CMD $SCAN_SCRIPT --agent $AGENT_NAME"
echo ""
echo "   # 禁用定时任务"
echo "   crontab -l | grep -v 'scan_sessions.py.*$AGENT_NAME' | crontab -"
echo ""
echo "   # 查看 cron 状态"
echo "   crontab -l"
echo ""
