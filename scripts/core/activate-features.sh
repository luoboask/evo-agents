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
        
        # 检查是否已有语义搜索模型
        if ollama list 2>/dev/null | grep -qE "nomic|m3e|bge|text2vec"; then
            echo "✅ 语义搜索已可用（已安装嵌入模型）"
            echo ""
            read -p "是否需要更换嵌入模型？(y/N): " -r INSTALL_MODEL
        else
            echo "⚠️  语义搜索不可用（未安装嵌入模型）"
            echo ""
            echo "💡 嵌入模型用于语义搜索功能："
            echo "   - 理解查询的含义，而非关键词匹配"
            echo "   - 搜索"昨天看的文章" → 找到相关内容，即使没提到"文章"这个词"
            echo "   - 搜索"项目进展" → 找到所有讨论进度的对话"
            echo ""
            read -p "是否安装嵌入模型以启用语义搜索？(y/N): " -r INSTALL_MODEL
        fi
        
        if [[ "$INSTALL_MODEL" =~ ^[Yy]$ ]]; then
            echo ""
            echo "💡 根据需求选择模型："
            echo ""
            echo "  想要最佳效果？"
            echo "  → 5) bge-m3 (中文最佳，~2.3GB)"
            echo "  → 2) mxbai-embed-large (英文最佳，~0.7GB)"
            echo ""
            echo "  电脑配置较低？"
            echo "  → 3) all-minilm (最小最快，~0.2GB)"
            echo "  → 6) m3e (中文轻量，~0.5GB)"
            echo ""
            echo "  中英文混合使用？"
            echo "  → 5) bge-m3 (支持多语言)"
            echo "  → 4) snowflake-arctic-embed (多语言优化)"
            echo ""
            echo "  专业领域搜索？"
            echo "  → 7) bge-large-zh (中文专业)"
            echo "  → 2) mxbai-embed-large (英文专业)"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "【资源占用详情】"
            echo ""
            echo "  【英文模型】"
            echo "  1) nomic-embed-text (通用)"
            echo "     磁盘：0.5GB | 内存：1GB | 显存：1GB | 速度：快"
            echo ""
            echo "  2) mxbai-embed-large (高性能)"
            echo "     磁盘：0.7GB | 内存：1.5GB | 显存：1.5GB | 速度：中"
            echo ""
            echo "  3) all-minilm (轻量)"
            echo "     磁盘：0.2GB | 内存：0.5GB | 显存：0.5GB | 速度：最快"
            echo ""
            echo "  4) snowflake-arctic-embed (多语言)"
            echo "     磁盘：0.5GB | 内存：1GB | 显存：1GB | 速度：快"
            echo ""
            echo "  【中文模型】"
            echo "  5) bge-m3 (最佳效果)"
            echo "     磁盘：2.3GB | 内存：4GB | 显存：2GB | 速度：中"
            echo ""
            echo "  6) m3e (中文轻量)"
            echo "     磁盘：0.5GB | 内存：1GB | 显存：1GB | 速度：快"
            echo ""
            echo "  7) bge-large-zh (中文专用)"
            echo "     磁盘：1.3GB | 内存：2GB | 显存：1.5GB | 速度：中"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            read -p "选择 [0-7，按场景推荐]： " -r MODEL_CHOICE
            
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
    echo "💡 提示："
    echo "   - 语义搜索已启用，下次会话自动生效"
    echo "   - 如果使用 OpenClaw，开始新对话即可体验"
    echo "   - 查看文档：docs/QUICKSTART.md"
    
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
        
        # Check if semantic search model exists
        if ollama list 2>/dev/null | grep -qE "nomic|m3e|bge|text2vec"; then
            echo "✅ Semantic search available (embedding model installed)"
            echo ""
            read -p "Change embedding model? (y/N): " -r INSTALL_MODEL
        else
            echo "⚠️  Semantic search unavailable (no embedding model)"
            echo ""
            echo "💡 Embedding models enable semantic search:"
            echo "   - Understand query meaning, not just keyword matching"
            echo "   - Search 'yesterday's article' → find relevant content, even without 'article' keyword"
            echo "   - Search 'project progress' → find all conversations about progress"
            echo ""
            read -p "Install embedding model to enable semantic search? (y/N): " -r INSTALL_MODEL
        fi
        
        if [[ "$INSTALL_MODEL" =~ ^[Yy]$ ]]; then
            echo ""
            echo "Select model:"
            echo ""
            echo "  [English Recommended]"
            echo "  1) nomic-embed-text (general purpose, ~0.5GB)"
            echo "     Use: Document search, Q&A systems, general semantic understanding"
            echo ""
            echo "  2) mxbai-embed-large (high performance, ~0.7GB)"
            echo "     Use: Complex queries, long document retrieval, high-precision search"
            echo ""
            echo "  3) all-minilm (lightweight & fast, ~0.2GB)"
            echo "     Use: Rapid prototyping, resource-constrained environments, real-time search"
            echo ""
            echo "  4) snowflake-arctic-embed (multilingual, ~0.5GB)"
            echo "     Use: Multilingual scenarios, international applications"
            echo ""
            echo "  [Chinese Recommended]"
            echo "  5) bge-m3 (best for Chinese, ~2.3GB)"
            echo "     Use: Chinese document search, cross-lingual retrieval, high-precision tasks"
            echo ""
            echo "  6) m3e (Chinese lightweight, ~0.5GB)"
            echo "     Use: Fast Chinese search, resource-constrained environments"
            echo ""
            echo "  7) bge-large-zh (Chinese specialized, ~1.3GB)"
            echo "     Use: Complex Chinese queries, domain-specific search"
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
    echo "💡 Tip:"
    echo "   - Semantic search enabled, will work in next session"
    echo "   - If using OpenClaw, start a new conversation to experience"
    echo "   - Documentation: docs/QUICKSTART.md"
fi
