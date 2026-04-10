#!/bin/bash
# 记忆系统安装脚本
# 
# 自动检测依赖并配置记忆系统

set -e

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENT_NAME=""

echo "╔════════════════════════════════════════════════════════╗"
echo "║  记忆系统安装配置                                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 获取 Agent 名称
if [ -f "$WORKSPACE_ROOT/.install-config" ]; then
    AGENT_NAME=$(grep "^agent_name=" "$WORKSPACE_ROOT/.install-config" | cut -d'=' -f2)
fi

if [ -z "$AGENT_NAME" ]; then
    read -p "请输入 Agent 名称: " AGENT_NAME
fi

echo "📦 Agent: $AGENT_NAME"
echo ""

# 检测 Ollama
echo "🔍 检测 Ollama..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama 已安装"
    
    # 检查 nomic-embed-text 模型
    if ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
        echo "   ✅ nomic-embed-text 模型已安装"
        OLLAMA_READY=true
    else
        echo "   ⚠️  nomic-embed-text 模型未安装"
        OLLAMA_READY=false
    fi
else
    echo "   ❌ Ollama 未安装"
    OLLAMA_READY=false
fi

echo ""

# 自动配置语义搜索
USE_SEMANTIC=false

if [ "$OLLAMA_READY" = true ]; then
    USE_SEMANTIC=true
    echo "   ✅ 语义搜索已启用（自动检测 Ollama 可用）"
else
    echo "   ⚠️  语义搜索不可用（Ollama 未安装或模型缺失）"
    echo "   💡 将自动降级到关键词搜索"
    echo "   如需启用语义搜索，请安装 Ollama: https://ollama.ai"
fi

echo ""

# 更新 RAG 配置
CONFIG_FILE="$WORKSPACE_ROOT/libs/rag_eval/config.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "🔧 更新 RAG 配置..."
    
    if [ "$USE_SEMANTIC" = true ]; then
        # 启用语义搜索
        cat > "$CONFIG_FILE" << 'EOF'
{
  "top_k_options": [3, 5, 7, 10],
  "similarity_thresholds": [0.6, 0.7, 0.8],
  "chunk_sizes": [256, 512, 1024],
  "weights": {
    "accuracy": 0.6,
    "latency": 0.3,
    "cost": 0.1
  },
  "current_config": {
    "top_k": 5,
    "similarity_threshold": 0.6,
    "chunk_size": 512
  },
  "semantic_search": {
    "enabled": true,
    "model": "nomic-embed-text",
    "ollama_host": "http://127.0.0.1:11434"
  },
  "experiment_mode": false,
  "auto_tune_enabled": true,
  "min_samples_for_comparison": 10
}
EOF
    else
        # 禁用语义搜索
        cat > "$CONFIG_FILE" << 'EOF'
{
  "top_k_options": [3, 5, 7, 10],
  "similarity_thresholds": [0.6, 0.7, 0.8],
  "chunk_sizes": [256, 512, 1024],
  "weights": {
    "accuracy": 0.6,
    "latency": 0.3,
    "cost": 0.1
  },
  "current_config": {
    "top_k": 5,
    "similarity_threshold": 0.6,
    "chunk_size": 512
  },
  "semantic_search": {
    "enabled": false,
    "model": "nomic-embed-text",
    "ollama_host": "http://127.0.0.1:11434"
  },
  "experiment_mode": false,
  "auto_tune_enabled": true,
  "min_samples_for_comparison": 10
}
EOF
    fi
    
    echo "   ✅ 配置已更新"
else
    echo "   ⚠️  配置文件不存在"
fi

echo ""

# 初始化知识图谱
echo "🧠 初始化知识图谱..."
if [ -f "$WORKSPACE_ROOT/libs/knowledge_graph/builder.py" ]; then
    python3 "$WORKSPACE_ROOT/libs/knowledge_graph/builder.py" --no-ai 2>&1 | sed 's/^/   /' || true
else
    echo "   ⚠️  知识图谱构建器不存在"
fi

echo ""

# 安装 Hook
echo "🪝 安装 Memory Fallback Hook..."
if [ -f "$WORKSPACE_ROOT/hooks/memory-fallback/install.sh" ]; then
    bash "$WORKSPACE_ROOT/hooks/memory-fallback/install.sh" 2>&1 | sed 's/^/   /' || true
else
    echo "   ⚠️  Hook 安装脚本不存在"
fi

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 安装完成！                                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 配置摘要:"
echo "   Agent: $AGENT_NAME"
echo "   语义搜索：$([ "$USE_SEMANTIC" = true ] && echo '✅ 已启用' || echo '❌ 未启用')"
echo ""
echo "🔧 使用命令:"
echo "   # 搜索记忆"
echo "   python3 skills/memory-search/unified_search.py \"关键词\""
echo ""
echo "   # 查看统计"
echo "   python3 skills/memory-search/session_memory_search.py --stats"
echo ""
echo "   # RAG 调优（积累 10+ 数据后）"
echo "   python3 libs/rag_eval/auto_tune.py --report"
echo ""
cho "   python3 skills/memory-search/session_memory_search.py --stats"
echo ""
echo "   # RAG 调优（积累 10+ 数据后）"
echo "   python3 libs/rag_eval/auto_tune.py --report"
echo ""
