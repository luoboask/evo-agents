#!/bin/bash
# restore-backup.sh - 恢复 workspace 备份
# Usage: ./scripts/core/restore-backup.sh [backup-directory]

set -e

WORKSPACE="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')

echo "╔════════════════════════════════════════════════════════╗"
echo "║  evo-agents 恢复备份 / Restore Backup                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo "🤖 Agent: $AGENT_NAME"
echo ""

# 查找备份
if [ -n "$1" ]; then
    BACKUP_DIR="$1"
else
    # 自动查找最新的备份
    BACKUP_DIR=$(ls -td /tmp/workspace-backup-$AGENT_NAME-* 2>/dev/null | head -1)
fi

if [ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ 未找到备份 / Backup not found"
    echo ""
    echo "可用的备份 / Available backups:"
    ls -lt /tmp/workspace-backup-$AGENT_NAME-* 2>/dev/null | head -5 || echo "   (none)"
    echo ""
    echo "用法 / Usage:"
    echo "  ./scripts/core/restore-backup.sh /path/to/backup"
    exit 1
fi

echo "📦 找到备份 / Backup found:"
echo "   $BACKUP_DIR"
echo "   大小 / Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo "   创建时间 / Created: $(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$BACKUP_DIR" 2>/dev/null || stat -c "%y" "$BACKUP_DIR" 2>/dev/null | cut -d'.' -f1)"
echo ""

# 确认恢复
echo "⚠️  警告：恢复备份将覆盖当前 workspace 的所有修改"
echo "   Warning: Restoring backup will overwrite all current modifications"
echo ""
echo "❓ 是否继续？/ Continue?"
echo "   y - 恢复 / Restore"
echo "   n - 取消 / Cancel"
echo ""

read -p "请输入 / Enter (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消 / Cancelled"
    exit 1
fi

# 创建当前状态的备份
CURRENT_BACKUP="/tmp/workspace-pre-restore-$AGENT_NAME-$(date +%Y%m%d-%H%M%S)"
echo ""
echo "📦 备份当前状态 / Backing up current state:"
echo "   $CURRENT_BACKUP"
cp -r "$WORKSPACE" "$CURRENT_BACKUP"
echo "✅ 当前状态已备份 / Current state backed up"
echo ""

# 恢复备份
echo "🔄 正在恢复备份 / Restoring backup..."
echo "   从 / From: $BACKUP_DIR"
echo "   到 / To: $WORKSPACE"
echo ""

# 复制文件（保留个人配置）
cd "$WORKSPACE"

# 恢复所有文件，但保留个人配置
rsync -av --delete \
    --exclude='USER.md' \
    --exclude='SOUL.md' \
    --exclude='IDENTITY.md' \
    --exclude='MEMORY.md' \
    --exclude='HEARTBEAT.md' \
    --exclude='TOOLS.md' \
    --exclude='memory/' \
    --exclude='public/' \
    --exclude='data/' \
    "$BACKUP_DIR/" "$WORKSPACE/"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 恢复完成！/ Restore Complete!                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 恢复详情 / Restore Details:"
echo "   备份来源 / Backup source: $BACKUP_DIR"
echo "   当前备份 / Current backup: $CURRENT_BACKUP"
echo ""
echo "💡 下一步 / Next Steps:"
echo "   1. 检查 workspace 状态 / Check workspace status"
echo "   2. 运行测试 / Run tests"
echo "   3. 如有问题，可恢复当前备份 / Restore current backup if needed"
echo ""
echo "   恢复当前备份的命令 / Command to restore current backup:"
echo "   ./scripts/core/restore-backup.sh $CURRENT_BACKUP"
echo ""
