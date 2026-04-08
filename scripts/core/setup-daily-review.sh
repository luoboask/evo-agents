#!/bin/bash
# setup-daily-review.sh - 设置每日回顾定时任务
#
# 用法:
#   ./scripts/core/setup-daily-review.sh my-agent
#   ./scripts/core/setup-daily-review.sh my-agent "09:00"  # 自定义时间

set -e

AGENT_NAME="${1:-}"
REVIEW_TIME="${2:-09:00}"  # 默认上午 9 点
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [ -z "$AGENT_NAME" ]; then
    # 尝试从 .install-config 读取
    if [ -f "$WORKSPACE_ROOT/.install-config" ]; then
        AGENT_NAME=$(grep "^agent_name=" "$WORKSPACE_ROOT/.install-config" | cut -d'=' -f2)
    fi
fi

if [ -z "$AGENT_NAME" ]; then
    echo "❌ 错误：请指定 Agent 名称或确保 .install-config 存在"
    echo "用法：$0 <agent-name> [review-time]"
    exit 1
fi

REVIEW_SCRIPT="$WORKSPACE_ROOT/skills/memory-search/daily_review.py"
PYTHON_CMD="python3"

# 检查 Python 和脚本
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ 错误：找不到 python3"
    exit 1
fi

if [ ! -f "$REVIEW_SCRIPT" ]; then
    echo "❌ 错误：找不到每日回顾脚本 $REVIEW_SCRIPT"
    echo "   请确保已安装 memory-search 技能"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  设置每日回顾定时任务                                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "⏰ 执行时间：每天 $REVIEW_TIME"
echo "📁 Workspace: $WORKSPACE_ROOT"
echo ""

# 解析时间为 cron 格式
HOUR=$(echo "$REVIEW_TIME" | cut -d':' -f1)
MINUTE=$(echo "$REVIEW_TIME" | cut -d':' -f2)
CRON_EXPR="$MINUTE $HOUR * * *"

# 创建 cron 命令
CRON_CMD="$CRON_EXPR cd $WORKSPACE_ROOT && $PYTHON_CMD $REVIEW_SCRIPT >> $WORKSPACE_ROOT/logs/daily_review.log 2>&1"

# 检查 crontab 是否已存在
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -c "daily_review.py" || true)
EXISTING_CRON=${EXISTING_CRON:-0}

if [ "$EXISTING_CRON" != "0" ] && [ "$EXISTING_CRON" -gt 0 ] 2>/dev/null; then
    echo "⚠️  每日回顾定时任务已存在"
    echo ""
    read -p "是否更新？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 0
    fi
    # 删除旧的 cron 任务
    crontab -l 2>/dev/null | grep -v "daily_review.py" | crontab -
    echo "   ✅ 已删除旧任务"
fi

# 创建日志目录
mkdir -p "$WORKSPACE_ROOT/logs"
touch "$WORKSPACE_ROOT/logs/daily_review.log"

# 添加新的 cron 任务
echo "📝 添加定时任务..."
(crontab -l 2>/dev/null | grep -v "daily_review.py"; echo "$CRON_CMD") | crontab -
echo "   ✅ 完成"

# 验证
echo ""
echo "📋 当前 cron 任务列表:"
crontab -l 2>/dev/null | grep "daily_review" || echo "   (无)"

# 测试运行
echo ""
echo "🧪 测试运行每日回顾..."
cd "$WORKSPACE_ROOT"
$PYTHON_CMD $REVIEW_SCRIPT
echo "   ✅ 测试完成"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 每日回顾定时任务设置完成！                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 日志文件：$WORKSPACE_ROOT/logs/daily_review.log"
echo ""
echo "🔧 管理命令:"
echo "   # 查看日志"
echo "   tail -f $WORKSPACE_ROOT/logs/daily_review.log"
echo ""
echo "   # 手动运行"
echo "   cd $WORKSPACE_ROOT && $PYTHON_CMD $REVIEW_SCRIPT"
echo ""
echo "   # 禁用定时任务"
echo "   crontab -l | grep -v 'daily_review.py' | crontab -"
echo ""
echo "   # 查看 cron 状态"
echo "   crontab -l"
echo ""
