#!/bin/bash
# reinstall.sh - 重装/修复 evo-agents workspace
# 用法：./reinstall.sh

set -e

WORKSPACE="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')

echo "╔════════════════════════════════════════════════════════╗"
echo "║     evo-agents 重装/修复向导                            ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo "🤖 Agent: $AGENT_NAME"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "请选择操作："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   1) 🔧 仅修复 skills（推荐）"
echo "   2) 🔄 完全重装（保留数据）"
echo "   3) 🗑️ 完全重置（删除所有数据）"
echo "   4) ❌ 取消"
echo ""

read -p "> " CHOICE

case $CHOICE in
    1)
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🔧 修复 skills"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # 从 GitHub 拉取最新 skills
        echo "📥 从 GitHub 拉取最新 skills..."
        if [ -d ".git" ]; then
            git fetch origin master
            git checkout origin/master -- skills/
            echo "   ✅ skills 已更新"
        else
            echo "   ⚠️  不是 git 仓库，跳过"
        fi
        
        # 修复硬编码
        echo ""
        echo "🔧 修复硬编码..."
        find skills/ -name "*.py" -exec sed -i.bak 's|Path("/Users/dhr/.openclaw/workspace")|Path(__file__).parent.parent.parent|g' {} \;
        find skills/ -name "*.py" -exec sed -i.bak "s/'ai-baby'/'$AGENT_NAME'/g" {} \;
        find skills/ -name "*.json" -exec sed -i.bak "s/\"author\": \"ai-baby\"/\"author\": \"$AGENT_NAME\"/g" {} \;
        find skills/ -name "*.bak" -delete
        echo "   ✅ 硬编码已修复"
        
        # 清理缓存
        echo ""
        echo "🧹 清理缓存..."
        find skills/ -type d -name "__pycache__" -exec rm -rf {} \; 2>/dev/null || true
        find skills/ -name "*.pyc" -delete 2>/dev/null || true
        echo "   ✅ 缓存已清理"
        
        echo ""
        echo "╔════════════════════════════════════════════════════════╗"
        echo "║  ✅ skills 修复完成！                                   ║"
        echo "╚════════════════════════════════════════════════════════╝"
        ;;
        
    2)
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🔄 完全重装（保留数据）"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # 备份重要数据
        echo "📦 备份重要数据..."
        BACKUP_DIR="/tmp/workspace-backup-$AGENT_NAME-$(date +%Y%m%d-%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        cp -r memory/ "$BACKUP_DIR/" 2>/dev/null || true
        cp -r data/ "$BACKUP_DIR/" 2>/dev/null || true
        cp -r public/ "$BACKUP_DIR/" 2>/dev/null || true
        cp -f *.md "$BACKUP_DIR/" 2>/dev/null || true
        echo "   ✅ 备份到：$BACKUP_DIR"
        
        # 删除旧文件（保留数据）
        echo ""
        echo "🗑️  删除旧文件..."
        rm -rf scripts/ libs/ skills/ docs/
        rm -f *.md 2>/dev/null || true
        echo "   ✅ 已删除"
        
        # 从 GitHub 拉取最新代码
        echo ""
        echo "📥 从 GitHub 拉取最新代码..."
        if [ -d ".git" ]; then
            git fetch origin master
            git reset --hard origin/master
            git clean -fd
            echo "   ✅ 已更新"
        else
            echo "   ⚠️  不是 git 仓库，请手动克隆"
            exit 1
        fi
        
        # 恢复数据
        echo ""
        echo "📦 恢复数据..."
        cp -r "$BACKUP_DIR/memory/" memory/ 2>/dev/null || true
        cp -r "$BACKUP_DIR/data/" data/ 2>/dev/null || true
        cp -r "$BACKUP_DIR/public/" public/ 2>/dev/null || true
        cp -f "$BACKUP_DIR/"*.md . 2>/dev/null || true
        echo "   ✅ 数据已恢复"
        
        # 修复硬编码
        echo ""
        echo "🔧 修复硬编码..."
        find skills/ -name "*.py" -exec sed -i.bak "s/'ai-baby'/'$AGENT_NAME'/g" {} \;
        find skills/ -name "*.json" -exec sed -i.bak "s/\"author\": \"ai-baby\"/\"author\": \"$AGENT_NAME\"/g" {} \;
        find skills/ -name "*.bak" -delete
        echo "   ✅ 硬编码已修复"
        
        echo ""
        echo "╔════════════════════════════════════════════════════════╗"
        echo "║  ✅ 重装完成！                                          ║"
        echo "╚════════════════════════════════════════════════════════╝"
        echo ""
        echo "💡 提示：可以运行 ./scripts/core/activate-features.sh 重新激活功能"
        ;;
        
    3)
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🗑️  完全重置（删除所有数据）"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        echo "⚠️  警告：这将删除所有数据，包括："
        echo "   - memory/ 目录"
        echo "   - data/ 目录"
        echo "   - public/ 目录"
        echo ""
        read -p "确认要重置吗？(输入 YES 确认): " CONFIRM
        
        if [[ "$CONFIRM" == "YES" ]]; then
            # 备份
            echo ""
            echo "📦 创建紧急备份..."
            BACKUP_DIR="/tmp/workspace-backup-$AGENT_NAME-$(date +%Y%m%d-%H%M%S)"
            mkdir -p "$BACKUP_DIR"
            cp -r memory/ "$BACKUP_DIR/" 2>/dev/null || true
            cp -r data/ "$BACKUP_DIR/" 2>/dev/null || true
            cp -r public/ "$BACKUP_DIR/" 2>/dev/null || true
            echo "   备份到：$BACKUP_DIR"
            
            # 删除数据
            echo ""
            echo "🗑️  删除数据..."
            rm -rf memory/* data/* public/*
            mkdir -p memory/weekly memory/monthly memory/archive
            mkdir -p data/index data/$AGENT_NAME
            mkdir -p public
            touch memory/.gitkeep data/.gitkeep public/.gitkeep
            echo "   ✅ 已重置"
            
            echo ""
            echo "╔════════════════════════════════════════════════════════╗"
            echo "║  ✅ 重置完成！                                          ║"
            echo "╚════════════════════════════════════════════════════════╝"
        else
            echo ""
            echo "❌ 已取消"
        fi
        ;;
        
    4)
        echo ""
        echo "❌ 已取消"
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
