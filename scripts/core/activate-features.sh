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
echo "   2) 📚 知识库系统 (已预装)"
echo "   3) 🧬 自进化系统 (已预装)"
echo "   4) 📊 RAG 评估系统 (已预装)"
echo "   5) ⏰ 定时任务 (已预装)"
echo ""
echo "   【Harness Agent 插件】(v2.0+)"
echo "   6) 💻 Programming 插件 - 软件开发"
echo "   7) 🛒 E-commerce 插件 - 电商运营"
echo "   8) 📊 Data Analysis 插件 - 数据分析"
echo "   9) 🔧 DevOps 插件 - CI/CD 部署监控"
echo "   10) 📢 Marketing 插件 - 营销策划"
echo "   11) ✍️ Content Creation 插件 - 内容创作"
echo "   12) 📱 Self-Media 插件 - 自媒体运营"
echo ""
echo "   【快捷选项】"
echo "   100) ✅ 全部激活（核心 + 所有插件）"
echo "   101) ❌ 跳过"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示："
echo "   - 基础功能已在安装时自动激活"
echo "   - 语义搜索模型需要单独安装（需 Ollama）"
echo "   - Harness Agent 插件已预装，可直接使用"
echo "   - 使用 /harness-agent 命令调用插件功能"
echo ""

# 选择功能
select_feature() {
    echo "请选择要激活的功能 (可多选，用空格分隔，如：1 6 7):"
    read -p "> " FEATURES
    
    # 特殊选项
    if [[ "$FEATURES" == "101" ]]; then
        echo "已跳过"
        exit 0
    fi
    
    if [[ "$FEATURES" == "100" ]]; then
        FEATURES="1 6 7 8 9 10 11 12"
    fi
    
    echo ""
    echo "已选择功能：$FEATURES"
    echo ""
    
    # 执行选择的功能
    for feature in $FEATURES; do
        case $feature in
            1) setup_ollama ;;
            6) 
                echo "💻 Programming 插件已预装"
                echo "   使用示例：/harness-agent \"开发博客系统\" --domain programming"
                ;;
            7) 
                echo "🛒 E-commerce 插件已预装"
                echo "   使用示例：/harness-agent \"双十一活动\" --domain ecommerce"
                ;;
            8) 
                echo "📊 Data Analysis 插件已预装"
                echo "   使用示例：/harness-agent \"Q1 销售分析\" --domain data_analysis"
                ;;
            9) 
                echo "🔧 DevOps 插件已预装"
                echo "   使用示例：/harness-agent \"部署到 AWS\" --domain devops"
                ;;
            10) 
                echo "📢 Marketing 插件已预装"
                echo "   使用示例：/harness-agent \"新品发布会\" --domain marketing"
                ;;
            11) 
                echo "✍️ Content Creation 插件已预装"
                echo "   使用示例：/harness-agent \"写产品测评\" --domain content_creation"
                ;;
            12) 
                echo "📱 Self-Media 插件已预装"
                echo "   使用示例：/harness-agent \"运营小红书\" --domain self_media_content"
                ;;
            2|3|4|5) 
                echo "✅ 该功能已预装，跳过"
                ;;
            *) echo "⚠️  无效选项：$feature" ;;
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
    
    # 显示已选择的核心功能
    core_features=""
    plugin_features=""
    
    for feature in $FEATURES; do
        case $feature in
            1) core_features="$core_features\n   ✅ 语义搜索模型" ;;
            2) core_features="$core_features\n   ✅ 知识库系统" ;;
            3) core_features="$core_features\n   ✅ 自进化系统" ;;
            4) core_features="$core_features\n   ✅ RAG 评估系统" ;;
            5) core_features="$core_features\n   ✅ 定时任务" ;;
            6) plugin_features="$plugin_features\n   ✅ Programming 插件" ;;
            7) plugin_features="$plugin_features\n   ✅ E-commerce 插件" ;;
            8) plugin_features="$plugin_features\n   ✅ Data Analysis 插件" ;;
            9) plugin_features="$plugin_features\n   ✅ DevOps 插件" ;;
            10) plugin_features="$plugin_features\n   ✅ Marketing 插件" ;;
            11) plugin_features="$plugin_features\n   ✅ Content Creation 插件" ;;
            12) plugin_features="$plugin_features\n   ✅ Self-Media 插件" ;;
        esac
    done
    
    if [[ -n "$core_features" ]]; then
        echo "   核心功能:$core_features"
        echo ""
    fi
    
    if [[ -n "$plugin_features" ]]; then
        echo "   Harness Agent 插件:$plugin_features"
        echo ""
    fi
    
    echo "   预装功能（无需激活）:"
    echo "   ✅ 基础记忆系统"
    echo "   ✅ Web 知识搜索"
    echo "   ✅ Harness Agent 核心"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🚀 快速开始:"
    echo ""
    echo "   # 使用 Programming 插件"
    echo "   /harness-agent \"开发博客系统\" --domain programming"
    echo ""
    echo "   # 使用数据分析插件"
    echo "   /harness-agent \"Q1 销售分析\" --domain data_analysis"
    echo ""
    echo "   # 查看所有可用领域"
    echo "   ls skills/harness-agent/plugins/"
    echo ""
}

# Ollama 设置（保持不变）
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
- 激活的功能：语义搜索模型 (Ollama + ${MODEL_NAME:-未下载})
- Harness Agent 插件：已查看（预装无需激活）
- 状态：已完成

MEMORYEOF
elif [[ "$FEATURES" =~ ^(6|7|8|9|10|11|12)$ ]]; then
    cat >> "$MEMORY_FILE" << MEMORYEOF

## 功能激活
- 时间：$(date +%Y-%m-%d\ %H:%M)
- 激活的功能：Harness Agent 插件（已预装）
- 使用的插件：$FEATURES
- 状态：已了解使用方法

MEMORYEOF
else
    cat >> "$MEMORY_FILE" << MEMORYEOF

## 功能激活
- 时间：$(date +%Y-%m-%d\ %H:%M)
- 激活的功能：无（基础功能已预装）
- 状态：已跳过

MEMORYEOF
fi

echo "   ✅ 已记录到 $MEMORY_FILE"
echo ""
echo "💡 提示：Agent 会在下次会话时读取此记录"
echo "   或运行 '/new' 开始新会话立即生效"
echo ""
