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

# 选择并下载嵌入模型
download_embedding_model() {
    echo ""
    
    # 检查 Ollama
    if command -v ollama &> /dev/null; then
        echo "   ✅ Ollama 已安装"
        
        # 显示已有模型
        echo ""
        echo "   📋 已有模型:"
        ollama list 2>/dev/null | grep -E "^[a-z]" | while read line; do
            echo "      $line"
        done
        echo ""
        
        # 询问是否拉取新模型
        echo "   需要拉取新的嵌入模型吗？"
        echo ""
        echo "   🇨🇳 中文模型推荐："
        echo "   • bge-m3              - 中文最佳 (推荐，~2.3GB)"
        echo "   • bge-large-zh        - 中文专用 (~1.2GB)"
        echo "   • text2vec            - 轻量中文 (~800MB)"
        echo ""
        echo "   🇺🇸 英文模型推荐："
        echo "   • mxbai-embed-large   - 性能王者 (MTEB 第一，~1.2GB)"
        echo "   • nomic-embed-text    - 轻量首选 (~500MB)"
        echo "   • all-minilm          - 超轻量 (~100MB)"
        echo "   • snowflake-arctic    - 多语言均衡 (~1.5GB)"
        echo ""
        read -p "   输入模型名称（直接回车使用 bge-m3）: " MODEL_NAME
        
        # 默认使用 bge-m3
        if [ -z "$MODEL_NAME" ]; then
            MODEL_NAME="bge-m3"
            echo "   ✅ 已选择：bge-m3 (中文最佳)"
        fi
        
        if [ -n "$MODEL_NAME" ]; then
            echo "   📥 正在下载：$MODEL_NAME"
            echo "   ℹ️  提示：大模型可能需要几分钟，请耐心等待..."
            echo ""
            
            # 显示下载进度（不过滤，让用户看到实时输出）
            if ollama pull "$MODEL_NAME" 2>&1; then
                echo ""
                echo "   ✅ 模型下载并安装成功！"
            else
                echo ""
                echo "   ⚠️  模型下载失败，请检查网络连接"
            fi
        fi
    else
        echo "   ⚠️  Ollama 未安装"
        echo "   访问：https://ollama.com"
        echo ""
        read -p "   是否现在安装？(y/N): " INSTALL_OLLAMA
        if [[ "$INSTALL_OLLAMA" =~ ^[Yy]$ ]]; then
            echo "   请访问 https://ollama.com 下载安装"
        fi
    fi
    echo ""
    
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
