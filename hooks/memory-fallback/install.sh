#!/bin/bash
# Memory Fallback Hook 安装脚本
# 
# 自动安装并启用 memory-fallback Hook
# 在 OpenClaw 原始记忆未找到时，自动从 memory-search 查询

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_NAME="memory-fallback"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Memory Fallback Hook 安装                              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 检查 OpenClaw 是否安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装，请先安装 OpenClaw"
    exit 1
fi

echo "✅ OpenClaw 已安装：$(openclaw --version)"
echo ""

# 检查 Hook 目录
if [ ! -f "$SCRIPT_DIR/HOOK.md" ]; then
    echo "❌ Hook 文件不存在：$SCRIPT_DIR/HOOK.md"
    exit 1
fi

echo "📦 Hook 文件:"
echo "   HOOK.md: ✓"
echo "   handler.ts: ✓"
echo "   package.json: ✓"
echo ""

# 安装 Hook
echo "🔧 安装 Hook..."
openclaw hooks install "$SCRIPT_DIR" 2>&1 | sed 's/^/   /'

if [ $? -ne 0 ]; then
    echo "❌ Hook 安装失败"
    exit 1
fi

echo "✅ Hook 安装成功"
echo ""

# 启用 Hook
echo "🚀 启用 Hook..."
openclaw hooks enable "$HOOK_NAME" 2>&1 | sed 's/^/   /'

if [ $? -ne 0 ]; then
    echo "⚠️  Hook 启用失败（可能已启用）"
else
    echo "✅ Hook 已启用"
fi

echo ""

# 验证安装
echo "📋 验证安装..."
openclaw hooks info "$HOOK_NAME" 2>&1 | sed 's/^/   /'

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 安装完成！                                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📝 使用说明:"
echo "   - Hook 会在 LLM 调用前自动执行"
echo "   - 自动检测关键词并查询记忆"
echo "   - 查询结果会添加到系统提示中"
echo ""
echo "🔧 管理命令:"
echo "   # 查看 Hook 状态"
echo "   openclaw hooks info $HOOK_NAME"
echo ""
echo "   # 禁用 Hook"
echo "   openclaw hooks disable $HOOK_NAME"
echo ""
echo "   # 重新启用"
echo "   openclaw hooks enable $HOOK_NAME"
echo ""
