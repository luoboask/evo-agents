#!/bin/bash
# uninstall-agent.sh - 卸载子 Agent
# 用法：./uninstall-agent.sh <agent-name>

set -e

# 优先从 .install-config 读取配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$WORKSPACE"

AGENT_NAME="$1"

if [ -z "$AGENT_NAME" ]; then
    echo "用法：./uninstall-agent.sh <agent-name>"
    echo ""
    echo "示例:"
    echo "   ./uninstall-agent.sh assistant-agent"
    echo "   ./uninstall-agent.sh researcher-agent"
    exit 1
fi

AGENT_DIR="agents/$AGENT_NAME"

if [ ! -d "$AGENT_DIR" ]; then
    echo "❌ Agent 不存在：$AGENT_NAME"
    echo ""
    echo "可用的 Agent:"
    ls -1 agents/ 2>/dev/null || echo "   (无)"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  卸载 Agent / Uninstall Agent                            ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Agent: $AGENT_NAME"
echo "📂 目录：$AGENT_DIR"
echo ""

# 显示将要删除的内容
echo "🔍 将要删除的内容:"
echo "   - $AGENT_DIR/agent/      (OpenClaw 配置)"
echo "   - $AGENT_DIR/memory/     (记忆数据)"
echo "   - $AGENT_DIR/sessions/   (聊天会话)"
echo "   - $AGENT_DIR/data/       (Agent 数据)"
echo "   - $AGENT_DIR/scripts/    (Agent 脚本)"
echo "   - $AGENT_DIR/libs/       (Agent 库)"
echo ""

# 询问确认
echo "⚠️  警告：此操作将删除 Agent 的所有数据"
echo "   备份建议：cp -r $AGENT_DIR /tmp/backup-$AGENT_NAME"
echo ""
read -p "是否继续？/ Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消 / Cancelled"
    exit 0
fi

# 备份（可选）
echo ""
read -p "是否在删除前备份？/ Backup before delete? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    BACKUP_DIR="/tmp/backup-$AGENT_NAME-$(date +%Y%m%d-%H%M%S)"
    echo "📦 备份到 / Backing up to: $BACKUP_DIR"
    cp -r "$AGENT_DIR" "$BACKUP_DIR"
    echo "   ✅ 备份完成 / Backup complete"
    echo ""
fi

# 从 OpenClaw 注销
echo "📝 从 OpenClaw 注销 / Unregister from OpenClaw..."
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    echo "   运行 / Running: openclaw agents delete $AGENT_NAME --force"
    openclaw agents delete "$AGENT_NAME" --force 2>/dev/null && \
        echo "   ✅ 已注销 / Unregistered" || \
        echo "   ⚠️  注销失败 / Unregister failed"
else
    echo "   ⚠️  Agent 未注册 / Agent not registered"
fi
echo ""

# 删除目录
echo "🗑️  删除 Agent 目录 / Deleting agent directory..."
rm -rf "$AGENT_DIR"
echo "   ✅ 已删除 / Deleted"
echo ""

# 清理 config/agents.yaml（如果存在）
if [ -f "config/agents.yaml" ]; then
    echo "📝 更新 config/agents.yaml..."
    # 移除该 Agent 的配置
    grep -v "^$AGENT_NAME:" config/agents.yaml > config/agents.yaml.tmp || true
    mv config/agents.yaml.tmp config/agents.yaml
    echo "   ✅ 已更新 / Updated"
    echo ""
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ Agent 已卸载 / Agent Uninstalled!                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 摘要 / Summary:"
echo "   Agent: $AGENT_NAME"
echo "   状态 / Status: 已删除 / Deleted"
if [ -n "$BACKUP_DIR" ]; then
    echo "   备份 / Backup: $BACKUP_DIR"
fi
echo ""
echo "💡 提示 / Tips:"
echo "   - 如需恢复，从备份复制回 agents/ 目录"
echo "   - 运行 'openclaw agents list' 查看剩余 Agent"
echo ""
