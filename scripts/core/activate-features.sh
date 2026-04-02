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
echo "   1) 🔮 语义搜索模型 (Ollama + 嵌入模型)"
echo "   2) 📚 知识库系统 (已预装)"
echo "   3) 🧬 自进化系统 (已预装)"
echo "   4) 📊 RAG 评估系统 (已预装)"
echo "   5) ⏰ 定时任务 (已预装)"
echo "   6) ✅ 全部激活"
echo "   7) ❌ 跳过"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示：基础功能已在安装时自动激活"
echo "   语义搜索模型需要单独安装（需 Ollama）"
echo ""

# 选择功能
select_feature() {
    echo "请选择要激活的功能 (可多选，用空格分隔，如：1 2 3):"
    read -p "> " FEATURES
    
    # 特殊选项
    if [[ "$FEATURES" == "7" ]]; then
        echo "已跳过"
        exit 0
    fi
    
    if [[ "$FEATURES" == "6" ]]; then
        FEATURES="1"
    fi
    
    echo ""
    echo "已选择功能：$FEATURES"
    echo ""
    
    # 执行选择的功能
    for feature in $FEATURES; do
        case $feature in
            1) setup_ollama ;;
            2) 
                echo "📚 知识库系统已预装，跳过"
                ;;
            3) 
                echo "🧬 自进化系统已预装，跳过"
                ;;
            4) 
                echo "📊 RAG 评估系统已预装，跳过"
                ;;
            5) 
                echo "⏰ 定时任务已预装，跳过"
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
    echo "   已激活的功能:"
    for feature in $FEATURES; do
        case $feature in
            1) echo "   ✅ 语义搜索模型" ;;
            *) ;;
        esac
    done
    echo "   ✅ 知识库系统 (预装)"
    echo "   ✅ 自进化系统 (预装)"
    echo "   ✅ RAG 评估系统 (预装)"
    echo "   ✅ 定时任务 (预装)"
    echo ""
}

# 检查 Ollama
check_ollama() {
    if command -v ollama &> /dev/null; then
        echo "✅ Ollama 已安装"
        return 0
    else
        echo "⚠️  Ollama 未安装"
        return 1
    fi
}

# 安装 Ollama
install_ollama() {
    echo ""
    echo "📥 安装 Ollama..."
    echo ""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "   使用 Homebrew 安装..."
            brew install ollama
        else
            echo "   ⚠️  Homebrew 未安装，请先安装 Homebrew："
            echo "      /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            return 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "   使用官方脚本安装..."
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "   ⚠️  未知系统类型，请手动安装 Ollama"
        echo "      https://ollama.com/download"
        return 1
    fi
    
    echo "   ✅ Ollama 安装完成"
    return 0
}

# 启动 Ollama 服务
start_ollama() {
    echo ""
    echo "🚀 启动 Ollama 服务..."
    
    # 检查是否已在运行
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "   ✅ Ollama 已在运行"
        return 0
    fi
    
    # 后台启动
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - 使用后台进程
        ollama serve &
        sleep 3
    else
        # Linux - 使用 systemd 或后台
        if systemctl is-active --quiet ollama 2>/dev/null; then
            echo "   ✅ Ollama 服务已启动（systemd）"
            return 0
        else
            ollama serve &
            sleep 3
        fi
    fi
    
    # 验证启动
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "   ✅ Ollama 服务已启动"
        return 0
    else
        echo "   ⚠️  Ollama 服务启动失败，请手动运行：ollama serve"
        return 1
    fi
}

# 下载嵌入模型（带智能推荐）
download_embedding_model() {
    echo ""
    echo "📚 选择嵌入模型："
    echo ""
    
    # 检测系统语言，智能推荐
    if locale | grep -q "zh_CN\|zh_CN\|Chinese"; then
        echo "   💡 检测到中文系统，推荐："
        echo "      1) m3e-base (中文优化，推荐)"
        echo "      2) bge-m3 (多语言，支持中文)"
        echo "      3) nomic-embed-text (英文优化)"
        echo "      4) 跳过（稍后手动下载）"
        DEFAULT_CHOICE="1"
    else
        echo "   💡 Detected English system, recommended:"
        echo "      1) nomic-embed-text (English optimized, recommended)"
        echo "      2) bge-m3 (Multilingual)"
        echo "      3) m3e-base (Chinese optimized)"
        echo "      4) Skip (download later)"
        DEFAULT_CHOICE="1"
    fi
    echo ""
    
    read -p "请选择 (1/2/3/4，直接回车选推荐): " MODEL_CHOICE
    
    # 默认选择推荐
    if [ -z "$MODEL_CHOICE" ]; then
        MODEL_CHOICE="$DEFAULT_CHOICE"
    fi
    
    case $MODEL_CHOICE in
        1)
            if locale | grep -q "zh_CN\|zh_CN\|Chinese"; then
                MODEL_NAME="m3e-base"
                echo "   已选择：m3e-base (中文优化)"
            else
                MODEL_NAME="nomic-embed-text"
                echo "   Selected: nomic-embed-text (English optimized)"
            fi
            ;;
        2)
            MODEL_NAME="bge-m3"
            echo "   已选择：bge-m3 (多语言)"
            ;;
        3)
            if locale | grep -q "zh_CN\|zh_CN\|Chinese"; then
                MODEL_NAME="nomic-embed-text"
                echo "   已选择：nomic-embed-text (英文优化)"
            else
                MODEL_NAME="m3e-base"
                echo "   Selected: m3e-base (Chinese optimized)"
            fi
            ;;
        4)
            echo "   已跳过，稍后可手动下载："
            echo "      ollama pull nomic-embed-text"
            echo "      ollama pull m3e-base"
            echo "      ollama pull bge-m3"
            MODEL_NAME=""
            ;;
        *)
            echo "   ⚠️  无效选项，使用推荐模型"
            if locale | grep -q "zh_CN\|zh_CN\|Chinese"; then
                MODEL_NAME="m3e-base"
            else
                MODEL_NAME="nomic-embed-text"
            fi
            ;;
    esac
    
    echo ""
    
    if [ -n "$MODEL_NAME" ]; then
        echo "📥 下载模型：$MODEL_NAME ..."
        echo ""
        
        ollama pull $MODEL_NAME
        
        if [ $? -eq 0 ]; then
            echo "   ✅ 模型下载完成"
            return 0
        else
            echo "   ❌ 模型下载失败"
            return 1
        fi
    fi
    
    return 0
}

# 验证安装
verify_installation() {
    echo ""
    echo "🔍 验证安装..."
    echo ""
    
    # 检查 Ollama
    if ! command -v ollama &> /dev/null; then
        echo "   ❌ Ollama 未找到"
        return 1
    fi
    echo "   ✅ Ollama 已安装"
    
    # 检查服务
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "   ❌ Ollama 服务未运行"
        return 1
    fi
    echo "   ✅ Ollama 服务运行中"
    
    # 检查模型（任意一个即可）
    if ollama list | grep -qE "nomic-embed-text|m3e-base|bge-m3"; then
        echo "   ✅ 嵌入模型已下载"
    else
        echo "   ⚠️  嵌入模型未下载，可手动下载："
        echo "      ollama pull nomic-embed-text"
        return 1
    fi
    
    return 0
}

# 激活语义搜索模型
setup_ollama() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔮 激活：语义搜索模型"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "步骤 1/4: 检查 Ollama"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if check_ollama; then
        echo ""
        echo "✅ Ollama 已安装，跳过安装步骤"
    else
        read -p "是否安装 Ollama? (y/n): " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ 已取消"
            return 1
        fi
        
        if ! install_ollama; then
            echo "❌ Ollama 安装失败"
            return 1
        fi
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "步骤 2/4: 启动 Ollama 服务"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ! start_ollama; then
        echo "⚠️  请手动启动 Ollama 服务：ollama serve"
        echo "   启动后重新运行此脚本"
        return 1
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "步骤 3/4: 选择嵌入模型"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ! download_embedding_model; then
        echo "❌ 模型下载失败"
        return 1
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "步骤 4/4: 验证安装"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if verify_installation; then
        echo ""
        echo "✅ 语义搜索模型激活成功"
    else
        echo ""
        echo "⚠️  验证失败，请检查："
        echo "   1. Ollama 是否正确安装"
        echo "   2. Ollama 服务是否运行（ollama serve）"
        echo "   3. 模型是否下载完成（ollama list）"
        return 1
    fi
}

# 主流程
select_feature

# 记录到 memory，让 Agent 感知
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
- 状态：已完成

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
��━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if verify_installation; then
        echo ""
        echo "✅ 语义搜索模型激活成功"
    else
        echo ""
        echo "⚠️  验证失败，请检查："
        echo "   1. Ollama 是否正确安装"
        echo "   2. Ollama 服务是否运行（ollama serve）"
        echo "   3. 模型是否下载完成（ollama list）"
        return 1
    fi
}

# 主流程
select_feature

# 记录到 memory，让 Agent 感知
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
- 状态：已完成

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
