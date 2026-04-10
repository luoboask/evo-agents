#!/bin/bash
# Memory Fallback Hook 卸载脚本

set -e

HOOK_NAME="memory-fallback"

echo "🗑️  卸载 Memory Fallback Hook..."
echo ""

# 禁用 Hook
echo "🚫 禁用 Hook..."
openclaw hooks disable "$HOOK_NAME" 2>&1 | sed 's/^/   /' || true

echo ""
echo "✅ Hook 已禁用"
echo ""
echo "📝 如需完全删除，请手动删除目录:"
echo "   rm -rf ~/.openclaw/hooks/$HOOK_NAME"
echo ""
