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

# 列出可能的临时文件
echo "🔍 扫描临时文件..."
echo ""

# 统计 work/ 目录
WORK_DIRS=()
for dir in "$WORKSPACE/data"/*/work "$WORKSPACE/agents"/*/data/*/work; do
    if [ -d "$dir" ]; then
        ITEM_COUNT=$(find "$dir" -type f 2>/dev/null | wc -l)
        if [ "$ITEM_COUNT" -gt 0 ]; then
            WORK_DIRS+=("$dir ($ITEM_COUNT 个文件)")
        fi
    fi
done

if [ ${#WORK_DIRS[@]} -eq 0 ]; then
    echo "✅ 没有发现临时工作目录"
else
    echo "📂 发现以下 work/ 目录："
    for dir in "${WORK_DIRS[@]}"; do
        echo "   - $dir"
    done
    echo ""
    echo "⚠️  注意：脚本无法判断这些是临时还是长期项目"
    echo "   请手动确认后再清理"
    echo ""
fi

# 列出构建产物
BUILD_ARTIFACTS=()
for pattern in "node_modules" "__pycache__" "*.log" "*.tmp" "*.pyc"; do
    COUNT=$(find "$WORKSPACE" -name "$pattern" 2>/dev/null | wc -l)
    if [ "$COUNT" -gt 0 ]; then
        BUILD_ARTIFACTS+=("$pattern ($COUNT 个)")
    fi
done

if [ ${#BUILD_ARTIFACTS[@]} -gt 0 ]; then
    echo "📦 发现构建产物："
    for artifact in "${BUILD_ARTIFACTS[@]}"; do
        echo "   - $artifact"
    done
    echo ""
fi

# 询问确认
echo "❓ 要清理哪些内容？/ What to clean?"
echo "   1) 只清理构建产物 (node_modules, __pycache__, *.log 等)"
echo "   2) 清理构建产物 + work/ 目录（请确认 work/ 是临时的）"
echo "   3) 取消"
echo ""
read -p "请选择 / Select (1/2/3): " -n 1 -r
echo ""

CLEAN_CHOICE="$REPLY"

if [[ "$CLEAN_CHOICE" == "3" ]]; then
    echo "❌ 已取消 / Cancelled"
    exit 0
fi

if [[ "$CLEAN_CHOICE" != "1" ]] && [[ "$CLEAN_CHOICE" != "2" ]]; then
    echo "❌ 无效选择 / Invalid selection"
    exit 1
fi

echo ""
echo "🧹 开始清理 / Starting cleanup..."
echo ""

# 统计清理前的空间
BEFORE_SIZE=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)

# 清理构建产物（总是清理）
echo "📦 清理构建产物..."
find "$WORKSPACE" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "*.log" -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.tmp" -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ 已清理构建产物"
echo ""

# 如果选择清理 work/ 目录
if [[ "$CLEAN_CHOICE" == "2" ]]; then
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
fi

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
echo "   - work/ 目录用于临时工作，完成后请手动清理"
echo "   - 重要数据请放在 data/<agent>/ 根目录（不会被清理）"
echo "   - 长期项目请放在 ~/projects/（外部目录）"
echo ""
