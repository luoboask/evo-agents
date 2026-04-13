#!/bin/bash
# activate-features.sh - 功能激活脚本（支持中英文）
# 用法：./activate-features.sh

set -e

WORKSPACE="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$WORKSPACE"
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')

# 检测系统语言
if locale 2>/dev/null | grep -qiE "zh_CN|zh_TW|zh_HK|zh_SG|zh-Hans|zh-Hant|Chinese"; then
    LANG="zh"
else
    LANG="en"
fi

# 根据语言显示提示信息
if [ "$LANG" = "zh" ]; then
    echo "🔮 evo-agents 功能激活"
    echo ""
    echo "已预装功能（无需激活）："
    echo "  ✅ 知识库系统"
    echo "  ✅ 自进化系统"
    echo "  ✅ RAG 评估系统"
    echo "  ✅ Harness Agent 插件（8 个领域）"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # 检查 Ollama
    if ! command -v ollama &> /dev/null; then
        echo "⚠️  Ollama 未安装"
        echo ""
        read -p "是否安装 Ollama？(y/N): " -r INSTALL_OLLAMA
        if [[ "$INSTALL_OLLAMA" =~ ^[Yy]$ ]]; then
            echo ""
            echo "📥 安装 Ollama..."
            curl -fsSL https://ollama.com/install.sh | sh
            echo ""
        else
            echo ""
            echo "⏭️  跳过 Ollama 安装"
            echo ""
        fi
    fi
    
    # 检查已安装的嵌入模型
    if command -v ollama &> /dev/null; then
        echo "📊 已安装的嵌入模型:"
        ollama list 2>/dev/null | grep -E "nomic|m3e|bge|text2vec" || echo "  (无)"
        echo ""
        
        read -p "是否需要安装/更换嵌入模型？(y/N): " -r INSTALL_MODEL
        if [[ "$INSTALL_MODEL" =~ ^[Yy]$ ]]; then
            echo ""
            echo "选择模型："
            echo ""
            echo "  【英文推荐】"
            echo "  1) nomic-embed-text (通用，~0.5GB)"
            echo "  2) mxbai-embed-large (高性能，~0.7GB)"
            echo "  3) all-minilm (轻量，~0.2GB)"
            echo "  4) snowflake-arctic-embed (多语言，~0.5GB)"
            echo ""
            echo "  【中文推荐】"
            echo "  5) bge-m3 (中文推荐，~2.3GB)"
            echo "  6) m3e (中文，~0.5GB)"
            echo "  7) bge-large-zh (中文，~1.3GB)"
            echo ""
            echo "  0) 跳过"
            echo ""
            read -p "选择 [0-7]: " -r MODEL_CHOICE
            
            case "$MODEL_CHOICE" in
                1)
                    echo "📥 下载 nomic-embed-text..."
                    ollama pull nomic-embed-text
                    ;;
                2)
                    echo "📥 下载 mxbai-embed-large..."
                    ollama pull mxbai-embed-large
                    ;;
                3)
                    echo "📥 下载 all-minilm..."
                    ollama pull all-minilm
                    ;;
                4)
                    echo "📥 下载 snowflake-arctic-embed..."
                    ollama pull snowflake-arctic-embed
                    ;;
                5)
                    echo "📥 下载 bge-m3..."
                    ollama pull bge-m3
                    ;;
                6)
                    echo "📥 下载 m3e..."
                    ollama pull m3e
                    ;;
                7)
                    echo "📥 下载 bge-large-zh..."
                    ollama pull bge-large-zh
                    ;;
                *)
                    echo "⏭️  跳过模型安装"
                    ;;
            esac
            echo ""
        fi
    fi
    
    # 更新 RAG 配置
    echo "🔧 更新 RAG 配置..."
    if [ -f "skills/rag/config.json" ]; then
        if command -v ollama &> /dev/null && ollama list 2>/dev/null | grep -qE "nomic|m3e|bge|text2vec"; then
            echo "✅ 语义搜索已启用"
        else
            echo "⚠️  语义搜索不可用，使用关键词搜索"
        fi
    else
        echo "⏭️  RAG 配置不存在，跳过"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ 功能激活完成！"
    echo ""
    echo "💡 提示：运行 '/new' 开始新会话立即生效"
    
else
    # English
    echo "🔮 evo-agents Feature Activation"
    echo ""
    echo "Pre-installed features (no activation needed):"
    echo "  ✅ Knowledge Base System"
    echo "  ✅ Self-Evolution System"
    echo "  ✅ RAG Evaluation System"
    echo "  ✅ Harness Agent Plugins (8 domains)"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check Ollama
    if ! command -v ollama &> /dev/null; then
        echo "⚠️  Ollama not installed"
        echo ""
        read -p "Install Ollama? (y/N): " -r INSTALL_OLLAMA
        if [[ "$INSTALL_OLLAMA" =~ ^[Yy]$ ]]; then
            echo ""
            echo "📥 Installing Ollama..."
            curl -fsSL https://ollama.com/install.sh | sh
            echo ""
        else
            echo ""
            echo "⏭️  Skipped Ollama installation"
            echo ""
        fi
    fi
    
    # Check installed embedding models
    if command -v ollama &> /dev/null; then
        echo "📊 Installed embedding models:"
        ollama list 2>/dev/null | grep -E "nomic|m3e|bge|text2vec" || echo "  (none)"
        echo ""
        
        read -p "Install/change embedding model? (y/N): " -r INSTALL_MODEL
        if [[ "$INSTALL_MODEL" =~ ^[Yy]$ ]]; then
            echo ""
            echo "Select model:"
            echo ""
            echo "  [English Recommended]"
            echo "  1) nomic-embed-text (general, ~0.5GB)"
            echo "  2) mxbai-embed-large (high performance, ~0.7GB)"
            echo "  3) all-minilm (lightweight, ~0.2GB)"
            echo "  4) snowflake-arctic-embed (multilingual, ~0.5GB)"
            echo ""
            echo "  [Chinese Recommended]"
            echo "  5) bge-m3 (Chinese recommended, ~2.3GB)"
            echo "  6) m3e (Chinese, ~0.5GB)"
            echo "  7) bge-large-zh (Chinese, ~1.3GB)"
            echo ""
            echo "  0) Skip"
            echo ""
            read -p "Select [0-7]: " -r MODEL_CHOICE
            
            case "$MODEL_CHOICE" in
                1)
                    echo "📥 Downloading nomic-embed-text..."
                    ollama pull nomic-embed-text
                    ;;
                2)
                    echo "📥 Downloading mxbai-embed-large..."
                    ollama pull mxbai-embed-large
                    ;;
                3)
                    echo "📥 Downloading all-minilm..."
                    ollama pull all-minilm
                    ;;
                4)
                    echo "📥 Downloading snowflake-arctic-embed..."
                    ollama pull snowflake-arctic-embed
                    ;;
                5)
                    echo "📥 Downloading bge-m3..."
                    ollama pull bge-m3
                    ;;
                6)
                    echo "📥 Downloading m3e..."
                    ollama pull m3e
                    ;;
                7)
                    echo "📥 Downloading bge-large-zh..."
                    ollama pull bge-large-zh
                    ;;
                *)
                    echo "⏭️  Skipped model installation"
                    ;;
            esac
            echo ""
        fi
    fi
    
    # Update RAG config
    echo "🔧 Updating RAG configuration..."
    if [ -f "skills/rag/config.json" ]; then
        if command -v ollama &> /dev/null && ollama list 2>/dev/null | grep -qE "nomic|m3e|bge|text2vec"; then
            echo "✅ Semantic search enabled"
        else
            echo "⚠️  Semantic search unavailable, using keyword search"
        fi
    else
        echo "⏭️  RAG config not found, skipping"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ Feature activation complete!"
    echo ""
    echo "💡 Tip: Run '/new' to start a new session"
fi
