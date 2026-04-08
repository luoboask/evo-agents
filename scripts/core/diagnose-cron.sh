#!/bin/bash
# diagnose-cron.sh - 诊断定时任务配置问题

AGENT_NAME="${1:-}"
if [ -z "$AGENT_NAME" ]; then
    echo "用法：$0 <agent-name>"
    exit 1
fi

WORKSPACE="$HOME/.openclaw/workspace-$AGENT_NAME"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  定时任务配置诊断                                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "📁 Workspace: $WORKSPACE"
echo ""

# 1. 检查脚本文件
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. 检查脚本文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

scripts=(
    "scripts/core/scan_sessions.py"
    "skills/memory-search/daily_review.py"
    "skills/self-evolution/nightly_cycle.py"
    "scripts/core/memory_compressor.py"
    "skills/memory-search/maintenance.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$WORKSPACE/$script" ]; then
        echo "   ✅ $script"
    else
        echo "   ❌ $script (不存在)"
    fi
done

echo ""

# 2. 检查脚本权限
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. 检查脚本权限"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for script in "${scripts[@]}"; do
    if [ -x "$WORKSPACE/$script" ]; then
        echo "   ✅ $script (可执行)"
    else
        echo "   ⚠️  $script (无执行权限，但使用 python3/bash 调用不影响)"
    fi
done

echo ""

# 3. 检查 OpenClaw cron
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. 检查 OpenClaw cron"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v openclaw &> /dev/null; then
    echo "   ✅ OpenClaw 已安装"
    
    echo ""
    echo "📋 当前 cron 任务:"
    openclaw cron list 2>&1 | grep "$AGENT_NAME" | head -10 || echo "   (无任务)"
else
    echo "   ❌ OpenClaw 未安装"
fi

echo ""

# 4. 测试运行脚本
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. 测试运行脚本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$WORKSPACE"

echo "   测试夜间进化脚本..."
if python3 skills/self-evolution/nightly_cycle.py --help >/dev/null 2>&1; then
    echo "   ✅ 夜间进化脚本可运行"
else
    echo "   ❌ 夜间进化脚本运行失败"
fi

echo "   测试记忆压缩脚本..."
if python3 scripts/core/memory_compressor.py --help >/dev/null 2>&1; then
    echo "   ✅ 记忆压缩脚本可运行"
else
    echo "   ❌ 记忆压缩脚本运行失败"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "诊断完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
