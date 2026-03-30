#!/bin/bash
# uninstall-workspace.sh - 卸载整个 Workspace
# 用法：./uninstall-workspace.sh [agent-name]

set -e

# 优先从 .install-config 读取配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG_FILE="$WORKSPACE/.install-config"

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
    WORKSPACE="$workspace_path"
    AGENT_NAME="$agent_name"
else
    # 回退到推导
    AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')
fi

if [ -n "$1" ]; then
    AGENT_NAME="$1"
    # 如果指定了 agent 名称，重新计算 workspace
    if [ -z "$WORKSPACE_ROOT" ]; then
        WORKSPACE="$HOME/.openclaw/workspace-$AGENT_NAME"
    fi
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  卸载 Workspace / Uninstall Workspace                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Agent: $AGENT_NAME"
echo "📂 Workspace: $WORKSPACE"
echo ""

# 确认 workspace 路径
if [[ "$WORKSPACE" != *"/workspace-$AGENT_NAME"* ]]; then
    echo "❌ 错误：Workspace 路径不匹配"
    echo "   预期包含 /workspace-$AGENT_NAME"
    echo "   实际：$WORKSPACE"
    exit 1
fi

# 显示将要删除的内容
echo "🔍 将要删除的内容:"
echo "   - $WORKSPACE/ (整个 workspace)"
echo ""
echo "📊 Workspace 大小:"
du -sh "$WORKSPACE" 2>/dev/null || echo "   (无法计算)"
echo ""

# 列出子 Agent（过滤 .gitkeep）
SUB_AGENTS=$(ls -1d "$WORKSPACE/agents/"*/ 2>/dev/null | wc -l || echo "0")
echo "📦 子 Agent 数量：$SUB_AGENTS"
if [ "$SUB_AGENTS" -gt 0 ]; then
    echo "   子 Agent:"
    ls -1d "$WORKSPACE/agents/"*/ 2>/dev/null | xargs -n1 basename | sed 's/^/      - /'
fi
echo ""

# 警告
echo "⚠️  严重警告 / CRITICAL WARNING:"
echo "   此操作将删除整个 workspace，包括:"
echo "   - 所有子 Agent 数据"
echo "   - 所有记忆数据 (memory/)"
echo "   - 所有知识库 (public/)"
echo "   - 所有运行时数据 (data/)"
echo "   - 所有自定义脚本和技能"
echo ""
echo "   以下文件会保留（在 .gitignore 中）:"
echo "   - USER.md, SOUL.md, IDENTITY.md"
echo "   - MEMORY.md, HEARTBEAT.md, TOOLS.md"
echo "   (但这些文件可能也包含重要数据)"
echo ""

# 备份建议
echo "💡 强烈建议先备份 / Strongly recommend backup:"
echo "   cp -r $WORKSPACE /tmp/backup-workspace-$AGENT_NAME-$(date +%Y%m%d)"
echo ""

# 询问确认
echo "❓ 是否继续？/ Continue?"
echo "   输入 agent 名称确认 / Type agent name to confirm:"
read -p "   输入 '$AGENT_NAME' 确认 / Enter '$AGENT_NAME' to confirm: " CONFIRM_NAME

if [ "$CONFIRM_NAME" != "$AGENT_NAME" ]; then
    echo ""
    echo "❌ 确认失败 / Confirmation failed"
    echo "   输入的是 / You entered: $CONFIRM_NAME"
    echo "   预期的是 / Expected: $AGENT_NAME"
    echo "   已取消 / Cancelled"
    exit 1
fi

echo ""

# 先从 OpenClaw 注销主 Agent（在删除 workspace 之前）
echo "📝 从 OpenClaw 注销主 Agent / Unregister main agent from OpenClaw..."
if openclaw agents list 2>/dev/null | grep -E "^- $AGENT_NAME$" >/dev/null; then
    echo "   运行 / Running: openclaw agents delete $AGENT_NAME --force"
    openclaw agents delete "$AGENT_NAME" --force 2>/dev/null && \
        echo "   ✅ 已注销 / Unregistered" || \
        echo "   ⚠️  注销失败 / Unregister failed (可能需要手动清理)"
else
    echo "   ⚠️  Agent 未注册 / Agent not registered"
fi
echo ""

# 注销所有子 Agent
if [ "$SUB_AGENTS" -gt 0 ]; then
    echo "📝 注销子 Agent / Unregister sub-agents..."
    for agent_dir in "$WORKSPACE/agents/"*/; do
        if [ -d "$agent_dir" ]; then
            sub_agent=$(basename "$agent_dir")
            # 跳过 .gitkeep
            if [ "$sub_agent" = ".gitkeep" ]; then
                continue
            fi
            echo "   - $sub_agent"
            openclaw agents delete "$sub_agent" --force 2>/dev/null || true
        fi
    done
    echo "   ✅ 子 Agent 已注销 / Sub-agents unregistered"
    echo ""
fi


# 最终确认
echo "⚠️  最后确认 / Final confirmation:"
read -p "   确定要删除整个 workspace 吗？/ Sure to delete entire workspace? (YES/NO): " FINAL_CONFIRM

if [ "$FINAL_CONFIRM" != "YES" ]; then
    echo ""
    echo "❌ 已取消 / Cancelled"
    exit 0
fi

echo ""

# 备份（可选）
read -p "是否在删除前完整备份？/ Full backup before delete? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    BACKUP_DIR="/tmp/backup-workspace-$AGENT_NAME-$(date +%Y%m%d-%H%M%S)"
    echo "📦 完整备份 / Full backup to: $BACKUP_DIR"
    cp -r "$WORKSPACE" "$BACKUP_DIR"
    echo "   ✅ 备份完成 / Backup complete"
    echo "   大小 / Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
    echo ""
fi

# 删除 workspace
echo "🗑️  删除 workspace / Deleting workspace..."
cd /tmp  # 切换到临时目录再删除
rm -rf "$WORKSPACE"
echo "   ✅ 已删除 / Deleted"
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ Workspace 已卸载 / Workspace Uninstalled!             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 摘要 / Summary:"
echo "   Agent: $AGENT_NAME"
echo "   Workspace: $WORKSPACE"
echo "   状态 / Status: 已删除 / Deleted"
if [ -n "$BACKUP_DIR" ]; then
    echo "   备份 / Backup: $BACKUP_DIR"
    echo "   大小 / Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
fi
echo ""
echo "💡 提示 / Tips:"
echo "   - 如需恢复，从备份复制回 ~/.openclaw/workspace-$AGENT_NAME"
echo "   - 运行 'openclaw agents list' 确认已注销"
echo "   - 重新安装：curl -s ... | bash -s $AGENT_NAME"
echo ""
