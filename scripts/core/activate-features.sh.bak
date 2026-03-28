#!/bin/bash
# activate-features.sh - 交互式功能激活脚本
# 用法：./activate-features.sh

set -e

# 使用 path_utils 统一路径解析（与其他脚本保持一致）
WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
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
echo "   2) 📚 知识库系统"
echo "   3) 🧬 自进化系统 (self-evolution)"
echo "   4) 📊 RAG 评估系统"
echo "   5) ⏰ 定时任务 (cron)"
echo "   6) ✅ 全部激活"
echo "   7) ❌ 跳过"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 主菜单
select_feature() {
    echo "请选择要激活的功能 (可多选，用空格分隔，如：1 2 3):"
    read -p "> " FEATURES
    
    if [[ "$FEATURES" == "7" ]]; then
        echo ""
        echo "⏭️  跳过激活"
        exit 0
    fi
    
    if [[ "$FEATURES" == "6" ]]; then
        FEATURES="1 2 3 4 5"
    fi
    
    echo ""
    echo "已选择功能：$FEATURES"
    echo ""
}

# 检查 Ollama 和下载模型
setup_ollama() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔮 激活：语义搜索模型"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if ! command -v ollama &> /dev/null; then
        echo "   ❌ Ollama 未安装"
        echo ""
        echo "   安装方法:"
        echo "   macOS: brew install ollama"
        echo "   Linux: curl -fsSL https://ollama.com/install.sh | sh"
        echo "   Windows: https://ollama.com/download/windows"
        echo ""
        read -p "是否继续激活其他功能？[Y/n] " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
        return 0
    fi
    
    echo "   ✅ Ollama 已安装"
    echo ""
    
    # 检查已有模型
    EXISTING_MODELS=$(ollama list 2>/dev/null | grep -E "bge-m3|nomic-embed|mxbai-embed|all-minilm" || true)
    
    if [ -n "$EXISTING_MODELS" ]; then
        echo "   ✅ 已有嵌入模型:"
        echo "$EXISTING_MODELS" | while read line; do
            echo "      $line"
        done
        echo ""
        read -p "是否下载更多模型？[y/N] " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "   ✅ 语义搜索已就绪"
            return 0
        fi
    fi
    
    echo ""
    echo "   请选择嵌入模型（根据主要使用语言）:"
    echo ""
    echo "   1) bge-m3            (1.2GB,  🇨🇳 中文最佳)"
    echo "   2) nomic-embed-text  (274MB,  🇺🇸 英文最佳)"
    echo "   3) mxbai-embed-large (670MB,  🌍 多语言支持)"
    echo "   4) all-minilm        (46MB,   🇺🇸 英文，快速测试)"
    echo "   5) 全部下载          (所有常用模型)"
    echo "   6) 跳过"
    echo ""
    read -p "   选择 [1-6]: " MODEL_CHOICE
    
    echo ""
    case $MODEL_CHOICE in
        1)
            echo "   📥 下载 bge-m3 (中文最佳)..."
            ollama pull bge-m3
            echo "   ✅ bge-m3 下载完成"
            ;;
        2)
            echo "   📥 下载 nomic-embed-text (英文最佳)..."
            ollama pull nomic-embed-text
            echo "   ✅ nomic-embed-text 下载完成"
            ;;
        3)
            echo "   📥 下载 mxbai-embed-large (多语言)..."
            ollama pull mxbai-embed-large
            echo "   ✅ mxbai-embed-large 下载完成"
            ;;
        4)
            echo "   📥 下载 all-minilm (最小最快)..."
            ollama pull all-minilm
            echo "   ✅ all-minilm 下载完成"
            ;;
        5)
            echo "   📥 下载所有模型..."
            ollama pull bge-m3
            ollama pull nomic-embed-text
            ollama pull mxbai-embed-large
            echo "   ✅ 所有模型下载完成"
            ;;
        *)
            echo "   ⏭️  跳过模型下载"
            ;;
    esac
    
    echo ""
    echo "   ✅ 语义搜索模型已激活"
    return 0
}

# 激活知识库
setup_knowledge_base() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📚 激活：知识库系统"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    python3 << EOF
import sys
from pathlib import Path

# 使用 path_utils 统一路径解析（与其他脚本保持一致）
sys.path.insert(0, '$WORKSPACE')
from path_utils import resolve_workspace

workspace = resolve_workspace()
sys.path.insert(0, str(workspace / 'libs'))

from memory_hub import MemoryHub

hub = MemoryHub('$AGENT_NAME')

try:
    # 添加基础知识
    print("   📝 添加基础知识...")
    
    hub.knowledge.add(
        title='项目介绍',
        content='这是我的个人项目，专注于知识管理和内容创作。',
        category='projects',
        tags=['项目', '介绍']
    )
    print("      ✅ 项目介绍")
    
    hub.knowledge.add(
        title='工作流程',
        content='标准工作流程：规划 → 创作 → 发布 → 分析',
        category='workflow',
        tags=['流程', '工作']
    )
    print("      ✅ 工作流程")
    
    hub.knowledge.add(
        title='内容策略',
        content='专注于高质量内容，重视真实分享和实用价值。',
        category='strategy',
        tags=['内容', '策略']
    )
    print("      ✅ 内容策略")
    
    print("")
    print(f'   ✅ 知识库已激活')
    print(f'   📊 分类：{len(hub.knowledge.list_categories())} 个')
    print(f'   📚 知识条目：3 条基础')
except Exception as e:
    print(f'   ⚠️  知识库激活失败：{e}')
EOF
    
    echo ""
    return 0
}

# 激活自进化系统
setup_self_evolution() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧬 激活：自进化系统"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ ! -d "skills/self-evolution" ]; then
        echo "   ⚠️  自进化系统不存在"
        return 1
    fi
    
    cd skills/self-evolution
    
    # 检查状态
    if python3 main.py status 2>&1 | grep -q "✅"; then
        echo "   ✅ 自进化系统已激活"
        cd ../..
        return 0
    fi
    
    echo "   📝 初始化自进化系统..."
    python3 << EOF
from storage import MemoryStream

ms = MemoryStream()
ms.add_memory(
    content='自进化系统初始化完成',
    memory_type='observation',
    importance=5.0,
    tags=['初始化', '系统']
)
print("   ✅ 自进化系统已初始化")
EOF
    
    cd ../..
    echo ""
    return 0
}

# 激活 RAG 评估
setup_rag() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 激活：RAG 评估系统"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ ! -d "skills/rag" ]; then
        echo "   ⚠️  RAG 系统不存在"
        return 1
    fi
    
    echo "   📝 记录测试数据..."
    python3 skills/rag/evaluate.py \
        --record \
        --query "测试 RAG 系统" \
        --retrieved 5 \
        --latency 100 \
        --feedback positive \
        --agent "$AGENT_NAME" 2>&1 | head -3
    
    echo "   ✅ RAG 评估系统已激活"
    echo ""
    return 0
}

# 配置定时任务
setup_cron() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏰ 配置：定时任务"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    read -p "   是否配置定时任务？[y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "   ⏭️  跳过定时任务配置"
        return 0
    fi
    
    echo "   📝 添加定时任务..."
    echo ""
    
    # 夜间循环
    if openclaw cron add --name "nightly-cycle" --cron "0 2 * * *" \
        --system-event "cd $WORKSPACE/skills/self-evolution && python3 main.py nightly" 2>/dev/null; then
        echo "   ✅ 夜间循环（每天 2:00）"
    else
        echo "   ⚠️  夜间循环（可能已存在）"
    fi
    
    # 分形思考
    if openclaw cron add --name "fractal-thinking" --cron "0 3 * * 0" \
        --system-event "cd $WORKSPACE/skills/self-evolution && python3 main.py fractal --limit 50" 2>/dev/null; then
        echo "   ✅ 分形思考（每周日 3:00）"
    else
        echo "   ⚠️  分形思考（可能已存在）"
    fi
    
    # 索引更新
    if openclaw cron add --name "daily-index" --cron "0 3 * * *" \
        --system-event "cd $WORKSPACE && python3 scripts/memory_indexer.py --incremental --embed" 2>/dev/null; then
        echo "   ✅ 索引更新（每天 3:00）"
    else
        echo "   ⚠️  索引更新（可能已存在）"
    fi
    
    echo ""
    echo "   查看 cron 任务：openclaw cron list"
    echo ""
    return 0
}

# 主流程
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

select_feature

# 执行选择的功能
for feature in $FEATURES; do
    case $feature in
        1)
            setup_ollama
            ;;
        2)
            setup_knowledge_base
            ;;
        3)
            setup_self_evolution
            ;;
        4)
            setup_rag
            ;;
        5)
            setup_cron
            ;;
    esac
done

# 输出总结
echo "╔════════════════════════════════════════════════════════╗"
echo "║     ✅ 功能激活完成！                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 激活总结:"
echo ""
echo "   已激活的功能:"
[[ " $FEATURES " =~ " 1 " ]] && echo "   ✅ 语义搜索模型"
[[ " $FEATURES " =~ " 2 " ]] && echo "   ✅ 知识库系统"
[[ " $FEATURES " =~ " 3 " ]] && echo "   ✅ 自进化系统"
[[ " $FEATURES " =~ " 4 " ]] && echo "   ✅ RAG 评估系统"
[[ " $FEATURES " =~ " 5 " ]] && echo "   ✅ 定时任务"
echo ""
echo "🎯 使用示例:"
echo ""
if [[ " $FEATURES " =~ " 1 " ]]; then
    echo "   # 语义搜索"
    echo "   python3 scripts/unified_search.py '关键词' --agent $AGENT_NAME --semantic"
    echo ""
fi

if [[ " $FEATURES " =~ " 2 " ]]; then
    echo "   # 查看知识库"
    echo "   python3 -c \"import sys; sys.path.insert(0, 'libs'); from memory_hub import MemoryHub; print(MemoryHub('$AGENT_NAME').knowledge.list_categories())\""
    echo ""
fi

if [[ " $FEATURES " =~ " 3 " ]]; then
    echo "   # 自进化状态"
    echo "   cd skills/self-evolution && python3 main.py status"
    echo ""
fi

if [[ " $FEATURES " =~ " 5 " ]]; then
    echo "   # 查看 cron"
    echo "   openclaw cron list"
    echo ""
fi

echo "📖 详细文档：docs/FEATURE_ACTIVATION_GUIDE.md"
echo ""
