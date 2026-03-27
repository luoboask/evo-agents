#!/bin/bash
# cleanup.sh - 清理 Workspace 构建产物
# 用法：./cleanup.sh [workspace-directory]

set -e

WORKSPACE="${1:-.}"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Workspace 清理 / Cleanup                                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo ""

# 统计清理前的空间
BEFORE_SIZE=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)

echo "🔍 扫描构建产物..."
echo ""

# 列出构建产物
ARTIFACTS=()
for pattern in "node_modules" "__pycache__" "*.log" "*.tmp" "*.pyc" "*.pyo" "dist" "build" "*.egg-info"; do
    COUNT=$(find "$WORKSPACE" -name "$pattern" 2>/dev/null | wc -l)
    if [ "$COUNT" -gt 0 ]; then
        ARTIFACTS+=("$pattern ($COUNT 个)")
    fi
done

if [ ${#ARTIFACTS[@]} -eq 0 ]; then
    echo "✅ 没有发现需要清理的构建产物"
    echo ""
    echo "💡 workspace 很干净！"
    exit 0
fi

echo "📦 发现以下构建产物："
for artifact in "${ARTIFACTS[@]}"; do
    echo "   - $artifact"
done
echo ""

# 询问确认
echo "❓ 是否清理这些构建产物？"
echo "   这些是明确的临时文件，可以安全清理"
echo ""
read -p "是否继续？/ Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消 / Cancelled"
    exit 0
fi

echo ""
echo "🧹 开始清理..."
echo ""

# 清理构建产物
echo "📦 清理 node_modules/..."
find "$WORKSPACE" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ 完成"

echo "📦 清理 __pycache__/..."
find "$WORKSPACE" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ 完成"

echo "📦 清理 *.log, *.tmp, *.pyc..."
find "$WORKSPACE" -name "*.log" -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.tmp" -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.pyc" -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.pyo" -delete 2>/dev/null || true
echo "   ✅ 完成"

echo "📦 清理 dist/, build/, *.egg-info/..."
find "$WORKSPACE" -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "build" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ 完成"

echo ""

# 统计清理后的空间
AFTER_SIZE=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)

echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 清理完成！/ Cleanup Complete!                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 清理结果 / Results:"
echo "   清理前 / Before: $BEFORE_SIZE"
echo "   清理后 / After:  $AFTER_SIZE"
echo ""
echo "✅ 已清理：构建产物（node_modules, __pycache__, *.log 等）"
echo ""
echo "⚠️  注意：work/ 目录未清理"
echo "   脚本无法判断是临时还是长期项目"
echo "   请手动检查后决定是否删除："
echo "   - data/*/work/"
echo "   - agents/*/data/*/work/"
echo ""
echo "💡 提示 / Tips:"
echo "   - 临时工作请使用 /tmp/ 或 ~/projects/"
echo "   - 重要数据请放在 data/<agent>/ 根目录"
echo "   - work/ 目录需要手动管理"
echo ""
