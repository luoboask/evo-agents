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
echo "   /harness-agent \"开发博客系统\" --domain programming"
echo "   /harness-agent \"Q1 销售分析\" --domain data_analysis"
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
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🚀 立即使用 Harness Agent:"
    echo ""
    echo "   # 软件开发"
    echo "   /harness-agent \"开发博客系统\" --domain programming"
    echo ""
    echo "   # 数据分析"
    echo "   /harness-agent \"Q1 销售分析\" --domain data_analysis"
    echo ""
    echo "   # 电商运营"
    echo "   /harness-agent \"双十一活动\" --domain ecommerce"
    echo ""
    echo "   # 运维部署"
    echo "   /harness-agent \"部署到 AWS\" --domain devops"
    echo ""
    echo "   # 营销策划"
    echo "   /harness-agent \"新品发布会\" --domain marketing"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 提示：运行 '/new' 开始新会话立即生效"
    echo ""
}

# Ollama 设置
setup_ollama() {
    echo "🔮 正在设置语义搜索模型..."
    echo ""
    
    # 检查 Ollama
    if ! command -v ollama &> /dev/null; then
        echo "❌ Ollama 未安装，请先安装："
        echo "   curl -fsSL https://ollama.com/install.sh | sh"
        return 1
    fi
    
    echo "✅ Ollama 已安装"
    
    # 启动服务
    echo "🔄 启动 Ollama 服务..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
    
    # 下载模型
    MODEL_NAME="nomic-embed-text"
    echo "📥 下载嵌入模型：$MODEL_NAME"
    ollama pull $MODEL_NAME
    
    echo ""
    echo "✅ 模型下载完成"
    
    # 验证
    echo "🔍 验证安装..."
    if ollama list | grep -q "$MODEL_NAME"; then
        echo "✅ 验证成功"
    else
        echo "❌ 验证失败"
        return 1
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
