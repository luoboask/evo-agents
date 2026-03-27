#!/bin/bash
# cleanup.sh - 清理 Workspace 临时文件
# 用法：./cleanup.sh [workspace-directory]

set -e

WORKSPACE="${1:-.}"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Workspace 清理 / Cleanup                                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo ""

# 询问确认
echo "⚠️  以下目录将被清理："
echo "   - data/*/work/ (Agent 临时工作目录)"
echo "   - agents/*/data/*/work/ (子 Agent 临时工作目录)"
echo "   - node_modules/, __pycache__/, *.log (构建产物)"
echo ""
echo "💡 这些是临时文件，不包含重要配置或数据"
echo ""

read -p "是否继续？/ Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消 / Cancelled"
    exit 0
fi

echo ""
echo "🧹 开始清理 / Starting cleanup..."
echo ""

# 统计清理前的空间
BEFORE_SIZE=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)

# 清理 Agent 临时工作目录
echo "📦 清理临时工作目录..."
COUNT=0
for dir in "$WORKSPACE/data"/*/work "$WORKSPACE/agents"/*/data/*/work; do
    if [ -d "$dir" ]; then
        ITEM_COUNT=$(find "$dir" -type f 2>/dev/null | wc -l)
        if [ "$ITEM_COUNT" -gt 0 ]; then
            echo "   - $dir ($ITEM_COUNT 个文件)"
            rm -rf "$dir"
            COUNT=$((COUNT + 1))
        fi
    fi
done
echo "   ✅ 已清理 $COUNT 个工作目录"
echo ""

# 清理构建产物
echo "📦 清理构建产物..."
find "$WORKSPACE" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "*.log" -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.tmp" -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ 已清理构建产物"
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
echo "💡 提示 / Tips:"
echo "   - work/ 目录用于临时工作，完成后请清理"
echo "   - 重要数据请放在 data/<agent>/ 根目录"
echo "   - 定期运行此脚本保持 workspace 整洁"
echo ""
