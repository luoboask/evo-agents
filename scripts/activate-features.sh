#!/bin/bash
# activate-features.sh - 一键激活所有高级功能
# 用法：./activate-features.sh

set -e

WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     激活高级功能                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 获取 Agent 名称
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')
echo "📁 Workspace: $WORKSPACE"
echo "🤖 Agent: $AGENT_NAME"
echo ""

# 1. 检查 Ollama
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  检查 Ollama..."
echo ""

if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama 已安装"
    
    # 检查已有模型
    EXISTING_MODELS=$(ollama list 2>/dev/null | grep -E "bge-m3|nomic-embed|mxbai-embed|all-minilm" || true)
    
    if [ -n "$EXISTING_MODELS" ]; then
        echo "   ✅ 嵌入模型已下载:"
        echo "$EXISTING_MODELS" | while read line; do
            echo "      $line"
        done
    else
        echo "   ⚠️  嵌入模型未下载"
        echo ""
        echo "   请选择模型（根据主要使用语言）:"
        echo ""
        echo "   1) bge-m3           (1.2GB, 中文最佳，推荐中文用户)"
        echo "   2) nomic-embed-text (274MB, 英文最佳，推荐英文用户)"
        echo "   3) mxbai-embed-large (670MB, 多语言支持)"
        echo "   4) all-minilm       (46MB,  英文，快速测试)"
        echo "   5) 全部下载         (所有模型，自动选择)"
        echo "   6) 跳过             (稍后手动下载)"
        echo ""
        read -p "请选择 [1-6]: " MODEL_CHOICE
        
        case $MODEL_CHOICE in
            1)
                echo "   下载 bge-m3 (中文最佳)..."
                ollama pull bge-m3
                echo "   ✅ bge-m3 下载完成"
                ;;
            2)
                echo "   下载 nomic-embed-text (英文最佳)..."
                ollama pull nomic-embed-text
                echo "   ✅ nomic-embed-text 下载完成"
                ;;
            3)
                echo "   下载 mxbai-embed-large (多语言)..."
                ollama pull mxbai-embed-large
                echo "   ✅ mxbai-embed-large 下载完成"
                ;;
            4)
                echo "   下载 all-minilm (最小最快)..."
                ollama pull all-minilm
                echo "   ✅ all-minilm 下载完成"
                ;;
            5)
                echo "   下载所有模型..."
                ollama pull bge-m3
                ollama pull nomic-embed-text
                ollama pull mxbai-embed-large
                echo "   ✅ 所有模型下载完成"
                ;;
            *)
                echo "   ⏭️  跳过模型下载"
                echo "   手动下载：ollama pull bge-m3"
                ;;
        esac
    fi
else
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
        exit 0
    fi
fi

echo ""

# 2. 激活知识库
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  激活知识库..."
echo ""

python3 << EOF
from libs.memory_hub import MemoryHub

hub = MemoryHub('$AGENT_NAME')

try:
    # 添加基础知识
    hub.knowledge.add(
        title='项目介绍',
        content='这是我的个人项目，专注于知识管理和内容创作。',
        category='projects',
        tags=['项目', '介绍']
    )
    
    hub.knowledge.add(
        title='工作流程',
        content='标准工作流程：规划 → 创作 → 发布 → 分析',
        category='workflow',
        tags=['流程', '工作']
    )
    
    hub.knowledge.add(
        title='内容策略',
        content='专注于高质量内容，重视真实分享和实用价值。',
        category='strategy',
        tags=['内容', '策略']
    )
    
    print('   ✅ 知识库已激活')
    print(f'   📊 分类：{len(hub.knowledge.list_categories())} 个')
    print(f'   📚 知识条目：3 条基础')
except Exception as e:
    print(f'   ⚠️  知识库激活失败：{e}')
EOF

echo ""

# 3. 测试语义搜索
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  测试语义搜索..."
echo ""

if python3 scripts/unified_search.py '测试' --agent "$AGENT_NAME" --semantic --limit 1 2>&1 | grep -q "找到"; then
    echo "   ✅ 语义搜索正常"
else
    echo "   ⚠️  语义搜索异常（可能需要 Ollama）"
fi

echo ""

# 4. 检查自进化系统
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  检查自进化系统..."
echo ""

if [ -d "skills/self-evolution" ]; then
    cd skills/self-evolution
    
    if python3 main.py status 2>&1 | grep -q "✅"; then
        echo "   ✅ 自进化系统正常"
    else
        echo "   ⚠️  自进化系统需要初始化"
        echo ""
        read -p "是否初始化自进化系统？[y/N] " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            python3 << EOF
from memory_stream import MemoryStream

ms = MemoryStream()
ms.add_memory(
    content='自进化系统初始化完成',
    memory_type='observation',
    importance=5.0,
    tags=['初始化', '系统']
)
print('   ✅ 自进化系统已初始化')
EOF
        fi
    fi
    
    cd ../..
else
    echo "   ⚠️  自进化系统不存在"
fi

echo ""

# 5. 配置定时任务
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  配置定时任务..."
echo ""

read -p "是否配置定时任务？[y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 夜间循环
    if openclaw cron add --name "nightly-cycle" --cron "0 2 * * *" \
        --system-event "cd $WORKSPACE/skills/self-evolution && python3 main.py nightly" 2>/dev/null; then
        echo "   ✅ 已添加：夜间循环（每天 2:00）"
    else
        echo "   ⚠️  添加失败（可能已存在）"
    fi
    
    # 分形思考
    if openclaw cron add --name "fractal-thinking" --cron "0 3 * * 0" \
        --system-event "cd $WORKSPACE/skills/self-evolution && python3 main.py fractal --limit 50" 2>/dev/null; then
        echo "   ✅ 已添加：分形思考（每周日 3:00）"
    else
        echo "   ⚠️  添加失败（可能已存在）"
    fi
    
    # 索引更新
    if openclaw cron add --name "daily-index" --cron "0 3 * * *" \
        --system-event "cd $WORKSPACE && python3 scripts/memory_indexer.py --incremental --embed" 2>/dev/null; then
        echo "   ✅ 已添加：索引更新（每天 3:00）"
    else
        echo "   ⚠️  添加失败（可能已存在）"
    fi
    
    echo ""
    echo "   查看 cron 任务：openclaw cron list"
else
    echo "   ⏭️  跳过定时任务配置"
fi

echo ""

# 6. 输出总结
echo "╔════════════════════════════════════════════════════════╗"
echo "║     ✅ 功能激活完成！                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 激活总结:"
echo ""
echo "   ✅ 语义搜索：已配置"
echo "   ✅ 知识库：已激活（3 条基础）"
echo "   ✅ 自进化：已检查"
echo "   ✅ 定时任务：已配置（可选）"
echo ""
echo "🎯 使用示例:"
echo ""
echo "   # 语义搜索"
echo "   python3 scripts/unified_search.py '关键词' --agent $AGENT_NAME --semantic"
echo ""
echo "   # 查看知识库"
echo "   python3 -c \"from libs.memory_hub import MemoryHub; print(MemoryHub('$AGENT_NAME').knowledge.list_categories())\""
echo ""
echo "   # 自进化状态"
echo "   cd skills/self-evolution && python3 main.py status"
echo ""
echo "   # 查看 cron"
echo "   openclaw cron list"
echo ""
echo "📖 详细文档：FEATURE_ACTIVATION_GUIDE.md"
echo ""
