#!/bin/bash
# activate-features.sh - 激活语义搜索模型
# 用法：./activate-features.sh
# 说明：基础功能（知识库、自进化、RAG、定时任务）已在安装时自动激活

set -e

# 获取 workspace 根目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$WORKSPACE"

# 获取 Agent 名称
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')

echo "╔════════════════════════════════════════════════════════╗"
echo "║     激活语义搜索模型                                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo "🤖 Agent: $AGENT_NAME"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔮 语义搜索模型需要以下组件："
echo ""
echo "   1) Ollama - 本地模型运行环境"
echo "   2) 嵌入模型 - nomic-embed-text (用于语义搜索)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

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

# 下载嵌入模型
download_embedding_model() {
    echo ""
    echo "📥 下载嵌入模型：nomic-embed-text..."
    echo ""
    
    ollama pull nomic-embed-text
    
    if [ $? -eq 0 ]; then
        echo "   ✅ 模型下载完成"
        return 0
    else
        echo "   ❌ 模型下载失败"
        return 1
    fi
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
    
    # 检查模型
    if ollama list | grep -q "nomic-embed-text"; then
        echo "   ✅ 嵌入模型已下载"
    else
        echo "   ❌ 嵌入模型未找到"
        return 1
    fi
    
    return 0
}

# 主流程
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
        exit 1
    fi
    
    if ! install_ollama; then
        echo "❌ Ollama 安装失败"
        exit 1
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 2/4: 启动 Ollama 服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! start_ollama; then
    echo "⚠️  请手动启动 Ollama 服务：ollama serve"
    echo "   启动后重新运行此脚本"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 3/4: 下载嵌入模型"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

read -p "是否下载 nomic-embed-text 模型？(y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
fi

if ! download_embedding_model; then
    echo "❌ 模型下载失败"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 4/4: 验证安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if verify_installation; then
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║     ✅ 语义搜索模型激活完成！                           ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 已激活组件:"
    echo "   ✅ Ollama 服务"
    echo "   ✅ nomic-embed-text 嵌入模型"
    echo ""
    echo "💡 使用方法:"
    echo "   - memory-search 技能现在支持语义搜索"
    echo "   - 使用 search.sh 进行语义检索"
    echo ""
else
    echo ""
    echo "⚠️  验证失败，请检查："
    echo "   1. Ollama 是否正确安装"
    echo "   2. Ollama 服务是否运行（ollama serve）"
    echo "   3. 模型是否下载完成（ollama list）"
    echo ""
    exit 1
fi

# 记录到 memory，让 Agent 感知
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 记录功能激活状态..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
MEMORY_FILE="memory/$(date +%Y-%m-%d).md"
mkdir -p memory/
if [ -n "$MODEL_NAME" ]; then
    cat >> "$MEMORY_FILE" << MEMORYEOF

## 功能激活
- 时间：$(date +%Y-%m-%d\ %H:%M)
- 激活的功能：语义搜索模型 (Ollama + $MODEL_NAME)
- 状态：已完成

MEMORYEOF
else
    cat >> "$MEMORY_FILE" << MEMORYEOF

## 功能激活
- 时间：$(date +%Y-%m-%d\ %H:%M)
- 激活的功能：Ollama 服务（模型稍后手动下载）
- 状态：部分完成

MEMORYEOF
fi
echo "   ✅ 已记录到 $MEMORY_FILE"
echo ""
echo "💡 提示：Agent 会在下次会话时读取此记录"
echo "   或运行 '/new' 开始新会话立即生效"
echo ""
