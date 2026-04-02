#!/bin/bash
# uninstall-agent.sh - Uninstall Agent
# Usage: ./uninstall-agent.sh <agent-name>

set -e

# Detect system language (default: English)
if locale | grep -q "zh_CN\|zh_CN\|Chinese"; then
    LANG="zh"
else
    LANG="en"
fi

# 优先从 .install-config 读取配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$WORKSPACE"

AGENT_NAME="$1"

if [ -z "$AGENT_NAME" ]; then
    if [ "$LANG" = "zh" ]; then
        echo "用法：./uninstall-agent.sh <agent-name>"
        echo ""
        echo "示例:"
        echo "   ./uninstall-agent.sh assistant-agent"
    else
        echo "Usage: ./uninstall-agent.sh <agent-name>"
        echo ""
        echo "Examples:"
        echo "   ./uninstall-agent.sh assistant-agent"
    fi
    exit 1
fi

AGENT_DIR="agents/$AGENT_NAME"

if [ ! -d "$AGENT_DIR" ]; then
    if [ "$LANG" = "zh" ]; then
        echo "❌ Agent 不存在：$AGENT_NAME"
        echo ""
        echo "可用的 Agent:"
        ls -1 agents/ 2>/dev/null || echo "   (无)"
    else
        echo "❌ Agent does not exist: $AGENT_NAME"
        echo ""
        echo "Available Agents:"
        ls -1 agents/ 2>/dev/null || echo "   (none)"
    fi
    exit 1
fi

# 标题
echo "╔════════════════════════════════════════════════════════╗"
if [ "$LANG" = "zh" ]; then
    echo "║  卸载 Agent                                                ║"
else
    echo "║  Uninstall Agent                                           ║"
fi
echo "╚════════════════════════════════════════════════════════╝"
echo ""
if [ "$LANG" = "zh" ]; then
    echo "📁 Agent: $AGENT_NAME"
    echo "📂 目录：$AGENT_DIR"
else
    echo "📁 Agent: $AGENT_NAME"
    echo "📂 Directory: $AGENT_DIR"
fi
echo ""

# 显示将要删除的内容
if [ "$LANG" = "zh" ]; then
    echo "🔍 将要删除的内容:"
    echo "   - $AGENT_DIR/agent/      (OpenClaw 配置)"
    echo "   - $AGENT_DIR/memory/     (记忆数据)"
    echo "   - $AGENT_DIR/sessions/   (聊天会话)"
    echo "   - $AGENT_DIR/data/       (Agent 数据)"
    echo "   - $AGENT_DIR/scripts/    (Agent 脚本)"
    echo "   - $AGENT_DIR/libs/       (Agent 库)"
    echo ""
    echo "⚠️  警告：此操作将删除 Agent 的所有数据"
    echo "   备份建议：cp -r $AGENT_DIR /tmp/backup-$AGENT_NAME"
    echo ""
    read -p "是否继续？(y/N): " -n 1 -r
else
    echo "🔍 Will delete:"
    echo "   - $AGENT_DIR/agent/      (OpenClaw config)"
    echo "   - $AGENT_DIR/memory/     (Memory data)"
    echo "   - $AGENT_DIR/sessions/   (Chat sessions)"
    echo "   - $AGENT_DIR/data/       (Agent data)"
    echo "   - $AGENT_DIR/scripts/    (Agent scripts)"
    echo "   - $AGENT_DIR/libs/       (Agent libraries)"
    echo ""
    echo "⚠️  Warning: This will delete all Agent data"
    echo "   Backup suggestion: cp -r $AGENT_DIR /tmp/backup-$AGENT_NAME"
    echo ""
    read -p "Continue? (y/N): " -n 1 -r
fi
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    if [ "$LANG" = "zh" ]; then
        echo "❌ 已取消"
    else
        echo "❌ Cancelled"
    fi
    exit 0
fi

# 备份（可选）
echo ""
if [ "$LANG" = "zh" ]; then
    read -p "是否在删除前备份？(y/N): " -n 1 -r
else
    read -p "Backup before delete? (y/N): " -n 1 -r
fi
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    BACKUP_DIR="/tmp/backup-$AGENT_NAME-$(date +%Y%m%d-%H%M%S)"
    if [ "$LANG" = "zh" ]; then
        echo "📦 备份到：$BACKUP_DIR"
    else
        echo "📦 Backing up to: $BACKUP_DIR"
    fi
    cp -r "$AGENT_DIR" "$BACKUP_DIR"
    if [ "$LANG" = "zh" ]; then
        echo "   ✅ 备份完成"
    else
        echo "   ✅ Backup complete"
    fi
    echo ""
fi

# 从 OpenClaw 注销
if [ "$LANG" = "zh" ]; then
    echo "📝 从 OpenClaw 注销..."
else
    echo "📝 Unregistering from OpenClaw..."
fi
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    if [ "$LANG" = "zh" ]; then
        echo "   运行：openclaw agents delete $AGENT_NAME --force"
    else
        echo "   Running: openclaw agents delete $AGENT_NAME --force"
    fi
    openclaw agents delete "$AGENT_NAME" --force 2>/dev/null && \
        if [ "$LANG" = "zh" ]; then echo "   ✅ 已注销"; else echo "   ✅ Unregistered"; fi || \
        if [ "$LANG" = "zh" ]; then echo "   ⚠️  注销失败"; else echo "   ⚠️  Unregister failed"; fi
else
    if [ "$LANG" = "zh" ]; then
        echo "   ⚠️  Agent 未注册"
    else
        echo "   ⚠️  Agent not registered"
    fi
fi
echo ""

# 删除目录
if [ "$LANG" = "zh" ]; then
    echo "🗑️  删除 Agent 目录..."
else
    echo "🗑️  Deleting agent directory..."
fi
rm -rf "$AGENT_DIR"
if [ "$LANG" = "zh" ]; then
    echo "   ✅ 已删除"
else
    echo "   ✅ Deleted"
fi
echo ""

# 清理 config/agents.yaml（如果存在）
if [ -f "config/agents.yaml" ]; then
    if [ "$LANG" = "zh" ]; then
        echo "📝 更新 config/agents.yaml..."
    else
        echo "📝 Updating config/agents.yaml..."
    fi
    grep -v "^$AGENT_NAME:" config/agents.yaml > config/agents.yaml.tmp || true
    mv config/agents.yaml.tmp config/agents.yaml
    if [ "$LANG" = "zh" ]; then
        echo "   ✅ 已更新"
    else
        echo "   ✅ Updated"
    fi
    echo ""
fi

# 完成
echo "╔════════════════════════════════════════════════════════╗"
if [ "$LANG" = "zh" ]; then
    echo "║  ✅ Agent 已卸载！                                          ║"
else
    echo "║  ✅ Agent Uninstalled!                                     ║"
fi
echo "╚════════════════════════════════════════════════════════╝"
echo ""
if [ "$LANG" = "zh" ]; then
    echo "📊 摘要:"
    echo "   Agent: $AGENT_NAME"
    echo "   状态：已删除"
    if [ -n "$BACKUP_DIR" ]; then
        echo "   备份：$BACKUP_DIR"
    fi
    echo ""
    echo "💡 恢复数据:"
    echo "   cp -r $BACKUP_DIR agents/$AGENT_NAME"
else
    echo "📊 Summary:"
    echo "   Agent: $AGENT_NAME"
    echo "   Status: Deleted"
    if [ -n "$BACKUP_DIR" ]; then
        echo "   Backup: $BACKUP_DIR"
    fi
    echo ""
    echo "💡 Restore data:"
    echo "   cp -r $BACKUP_DIR agents/$AGENT_NAME"
fi
echo ""
