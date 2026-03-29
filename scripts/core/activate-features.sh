#!/bin/bash
# activate-features.sh - 交互式功能激活脚本
# 用法：./activate-features.sh

set -e

# 获取 workspace 根目录（正确的方式）
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
echo "   2) 📚 知识库系统"
echo "   3) 🧬 自进化系统 (self-evolution)"
echo "   4) 📊 RAG 评估系统"
echo "   5) ⏰ 定时任务 (cron)"
echo "   6) ✅ 全部激活"
echo "   7) ❌ 跳过"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
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
        FEATURES="1 2 3 4 5"
    fi
    
    echo ""
    echo "已选择功能：$FEATURES"
    echo ""
    
    # 执行选择的功能
    for feature in $FEATURES; do
        case $feature in
            1) setup_ollama ;;
            2) setup_knowledge ;;
            3) setup_self_evolution ;;
            4) setup_rag ;;
            5) setup_cron ;;
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
            2) echo "   ✅ 知识库系统" ;;
            3) echo "   ✅ 自进化系统" ;;
            4) echo "   ✅ RAG 评估系统" ;;
            5) echo "   ✅ 定时任务" ;;
        esac
    done
    echo ""
    echo "🎯 使用示例:"
    echo ""
    if [[ " $FEATURES " =~ " 1 " ]]; then
        echo "   # 查看嵌入模型"
        echo "   ollama list"
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
        echo "   # 查看定时任务"
        echo "   openclaw cron list"
        echo ""
    fi
    echo "📖 详细文档：docs/FEATURE_ACTIVATION_GUIDE.md"
    echo ""
}

# 激活语义搜索模型
setup_ollama() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔮 激活：语义搜索模型"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
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
        
        # 初始化向量数据库
        echo ""
        echo "   📊 初始化向量数据库..."
        python3 << 'PYINIT'
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'scripts' / 'core'))
from memory_indexer import get_db_path, init_db
import sqlite3

try:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    init_db(conn)
    conn.close()
    print("   ✅ 向量数据库初始化成功")
except Exception as e:
    print(f"   ⚠️  向量数据库初始化失败：{e}")
PYINIT
        echo ""
        
        # 询问是否拉取新模型
        echo "   需要拉取新的嵌入模型模型吗？"
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
}

# 激活知识库系统
setup_knowledge() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📚 激活：知识库系统"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ ! -d "libs/memory_hub" ]; then
        echo "   ⚠️  libs/memory_hub 不存在"
        return 1
    fi
    
    python3 << EOF
import sys
from pathlib import Path

sys.path.insert(0, str(Path('$WORKSPACE') / 'libs'))
sys.path.insert(0, str(Path('$WORKSPACE') / 'scripts' / 'core'))
from path_utils import resolve_workspace
from memory_hub import MemoryHub

workspace = resolve_workspace()
hub = MemoryHub('$AGENT_NAME')

try:
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
    
    print("")
    print("   ✅ 知识库已激活")
    print(f"   📊 分类：{len(hub.knowledge.list_categories())} 个")
except Exception as e:
    print(f"   ⚠️  知识库激活失败：{e}")
EOF
    
    echo ""
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
    
    # 保存 WORKSPACE_ROOT（避免 cd 后路径错误）
    WORKSPACE_ROOT="$(pwd)"
    AGENT_NAME=$(basename "$WORKSPACE_ROOT" | sed 's/workspace-//')
    
    # 检查状态（使用绝对路径）
    if python3 "$WORKSPACE_ROOT/skills/self-evolution/main.py" status 2>&1 | grep -q "✅"; then
        echo "   ✅ 自进化系统已激活"
        return 0
    fi
    
    echo "   📝 初始化自进化系统..."
    # 设置正确的 agent 名称
    export OPENCLAW_AGENT="$AGENT_NAME"
    python3 << EOF
import sys
sys.path.insert(0, '$WORKSPACE_ROOT/scripts/core')
sys.path.insert(0, '$WORKSPACE_ROOT/skills/self-evolution')
from memory_stream import MemoryStream

ms = MemoryStream()
ms.add_memory(
    content='自进化系统初始化完成',
    memory_type='observation',
    importance=5
)
print("   ✅ 初始化完成")
EOF
    
    echo "   ✅ 自进化系统已激活"
    echo ""
}

# 激活 RAG 评估系统
setup_rag() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 激活：RAG 评估系统"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ ! -d "skills/rag" ]; then
        echo "   ⚠️  skills/rag 不存在"
        return 1
    fi
    
    echo "   ✅ RAG 评估系统已就绪"
    echo "   📝 使用方法：cd skills/rag && python3 evaluate.py"
    echo ""
}

# 激活定时任务
setup_cron() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏰ 激活：定时任务"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    echo "   ✅ 定时任务已就绪"
    echo "   📝 使用方法：openclaw cron add/list/run"
    echo ""
}

# 主流程
select_feature
