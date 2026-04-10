#!/bin/bash
# activate-features.sh - 交互式功能激活脚本
# 用法：./activate-features.sh

set -e

# 获取 workspace 根目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$WORKSPACE"

# 获取 Agent 名称
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')

echo "╔════════════════════════════════════════════════════════╗"
echo "║     evo-agents 功能激活向导                             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo "🤖 Agent: $AGENT_NAME"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 可激活功能列表"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   【核心功能】"
echo "   1) 🔮 语义搜索模型 (Ollama + 嵌入模型)"
echo "   2) 📚 知识库系统 (已预装 ✅)"
echo "   3) 🧬 自进化系统 (已预装 ✅)"
echo "   4) 📊 RAG 评估系统 (已预装 ✅)"
echo "   5) ⏰ 定时任务 (已预装 ✅)"
echo ""
echo "   【Harness Agent 插件】(v2.0+ 已预装 ✅)"
echo "   💻 Programming - E-commerce - Data Analysis"
echo "   🔧 DevOps - Marketing - Content Creation - Self-Media"
echo ""
echo "   【快捷选项】"
echo "   100) ✅ 全部激活（语义搜索 + 所有插件）"
echo "   101) ⏭️ 仅激活语义搜索"
echo "   102) ❌ 跳过（基础功能已可用）"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示："
echo "   - Harness Agent 插件已预装并激活，可直接使用！"
echo "   - 语义搜索模型需要单独安装（需 Ollama）"
echo "   - 基础功能无需激活，开箱即用"
echo ""
echo "🚀 快速开始:"
echo ""

# 选择功能
select_feature() {
    echo "请选择要激活的功能:"
    read -p "> " FEATURES
    
    # 特殊选项
    if [[ "$FEATURES" == "102" ]]; then
        echo "已跳过（基础功能已预装）"
        exit 0
    fi
    
    if [[ "$FEATURES" == "100" ]]; then
        FEATURES="1"
        echo "将激活：语义搜索模型 + Harness Agent 插件（已预装）"
    elif [[ "$FEATURES" == "101" ]]; then
        FEATURES="1"
        echo "将激活：语义搜索模型"
    fi
    
    echo ""
    
    # 执行选择的功能
    for feature in $FEATURES; do
        case $feature in
            1) setup_ollama ;;
            *) echo "✅ 该功能已预装，跳过" ;;
        esac
        echo ""
    done
    
    # 完成
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║     ✅ 功能激活完成！                                   ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 激活总结:"
    echo ""
    
    if [[ "$FEATURES" == *"1"* ]]; then
        echo "   ✅ 语义搜索模型 (Ollama + nomic-embed-text)"
    else
        echo "   ⏭️ 语义搜索模型（未激活，可选）"
    fi
    
    echo ""
    echo "   ✅ 预装功能（已激活）:"
    echo "   • Harness Agent 插件 (8 个领域)"
    echo "     💻 Programming | 🛒 E-commerce | 📊 Data Analysis"
    echo "     🔧 DevOps | 📢 Marketing | ✍️ Content Creation"
    echo "     📱 Self-Media"
    echo "   • 记忆搜索系统"
    echo "   • Web 知识搜索"
    echo "   • 自进化系统"
    echo "   • RAG 评估系统"
    echo "   • 定时任务"
    echo ""
    echo "💡 提示：运行 '/new' 开始新会话立即生效"
    echo ""
}

# Ollama 设置
setup_ollama() {
    echo "🔮 正在设置语义搜索模型..."
    echo ""
    
    # 检查 Ollama
    if command -v ollama &> /dev/null; then
        echo "✅ Ollama 已安装"
        OLLAMA_INSTALLED=true
    else
        echo "❌ Ollama 未安装"
        OLLAMA_INSTALLED=false
    fi
    
    # 如果已安装，检查模型
    if [ "$OLLAMA_INSTALLED" = true ]; then
        if ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
            echo "✅ nomic-embed-text 模型已安装"
            OLLAMA_READY=true
        else
            echo "⚠️  nomic-embed-text 模型未安装"
            echo ""
            read -p "是否下载模型？(y/N): " -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "📥 下载嵌入模型..."
                ollama pull nomic-embed-text && OLLAMA_READY=true || OLLAMA_READY=false
            else
                OLLAMA_READY=false
            fi
        fi
    else
        OLLAMA_READY=false
    fi
    
    echo ""
    
    # 自动配置 RAG
    CONFIG_FILE="$WORKSPACE/libs/rag_eval/config.json"
    if [ -f "$CONFIG_FILE" ]; then
        echo "🔧 更新 RAG 配置..."
        if [ "$OLLAMA_READY" = true ]; then
            # 启用语义搜索
            python3 << PYTHON
import json
with open("$CONFIG_FILE") as f:
    config = json.load(f)
config['semantic_search'] = {
    'enabled': True,
    'model': 'nomic-embed-text',
    'ollama_host': 'http://127.0.0.1:11434'
}
with open("$CONFIG_FILE", 'w') as f:
    json.dump(config, f, indent=2)
print("✅ 语义搜索已启用")
PYTHON
        else
            # 禁用语义搜索
            python3 << PYTHON
import json
with open("$CONFIG_FILE") as f:
    config = json.load(f)
config['semantic_search'] = {
    'enabled': False,
    'model': 'nomic-embed-text',
    'ollama_host': 'http://127.0.0.1:11434'
}
with open("$CONFIG_FILE", 'w') as f:
    json.dump(config, f, indent=2)
print("✅ 配置已更新（关键词搜索模式）")
PYTHON
        fi
    fi
    
    echo ""
    echo "💡 提示："
    if [ "$OLLAMA_READY" = true ]; then
        echo "   ✅ 语义搜索已启用，支持向量相似度查询"
        echo "   查询时自动使用语义搜索"
    else
        echo "   ⚠️  语义搜索不可用，自动降级到关键词搜索"
        echo "   如需启用，请安装 Ollama: https://ollama.ai"
    fi
}

# 安装 Memory Fallback Hook
install_memory_hook() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🪝 安装 Memory Fallback Hook"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    HOOK_DIR="$WORKSPACE/hooks/memory-fallback"
    if [ -f "$HOOK_DIR/install.sh" ]; then
        echo "📦 安装 Hook..."
        bash "$HOOK_DIR/install.sh" 2>&1 | sed 's/^/   /' || true
    else
        echo "   ⚠️  Hook 安装脚本不存在"
    fi
}

# 主流程
select_feature

# 记录到 memory
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 记录功能激活状态..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
MEMORY_FILE="memory/$(date +%Y-%m-%d).md"
mkdir -p memory/

if [[ "$FEATURES" == *"1"* ]]; then
    cat >> "$MEMORY_FILE" << MEMORYEOF

## 功能激活
- 时间：$(date +%Y-%m-%d\ %H:%M)
- 激活的功能：
  - ✅ 语义搜索模型 (Ollama + ${MODEL_NAME:-未下载})
  - ✅ Harness Agent 插件 (8 个领域，预装)
  - ✅ 基础功能 (记忆/Web/RAG/自进化/定时任务)
- 状态：已完成

MEMORYEOF
else
    cat >> "$MEMORY_FILE" << MEMORYEOF

## 功能激活
- 时间：$(date +%Y-%m-%d\ %H:%M)
- 激活的功能：
  - ⏭️ 语义搜索模型（未激活，可选）
  - ✅ Harness Agent 插件 (8 个领域，预装)
  - ✅ 基础功能 (记忆/Web/RAG/自进化/定时任务)
- 状态：基础功能已可用

MEMORYEOF
fi

echo "   ✅ 已记录到 $MEMORY_FILE"
echo ""
echo "💡 提示：Agent 会在下次会话时读取此记录"
echo "   或运行 '/new' 开始新会话立即生效"
echo ""
