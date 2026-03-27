#!/bin/bash
# install.sh - 一键安装 evo-agents Workspace
# 用法：curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s <agent-name>
# Usage: curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s <agent-name> [--force] [--activate]

set -e

AGENT_NAME="${1:-my-agent}"
FORCE=""
ACTIVATE=""

# 解析参数
for arg in "$@"; do
    case $arg in
        --force|-f)
            FORCE="yes"
            ;;
        --activate|-a)
            ACTIVATE="yes"
            ;;
    esac
done

WORKSPACE_ROOT="$HOME/.openclaw/workspace-$AGENT_NAME"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  evo-agents 一键安装 / One-Click Install                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "📁 Workspace: $WORKSPACE_ROOT"
echo ""

# Check if workspace exists | 检查 workspace 是否存在
if [ -d "$WORKSPACE_ROOT" ]; then
    # 如果使用了 --force，跳过确认
    if [[ -n "$FORCE" ]]; then
        echo "⚠️  Workspace 已存在，使用 --force 跳过确认"
        echo "   Workspace exists, using --force to skip confirmation"
        echo ""
        cd "$WORKSPACE_ROOT"
    else
        echo "⚠️  检测到 $AGENT_NAME 的 workspace 已存在"
        echo "   Workspace for $AGENT_NAME already exists"
        echo ""
        echo "🔄 继续安装将更新通用模板文件："
        echo "   Continuing will update template files:"
        echo ""
        echo "   ✅ 保留以下内容（不会删除）:"
        echo "      - 您的个人配置 (USER.md, SOUL.md 等)"
        echo "      - 记忆数据 (memory/ 目录)"
        echo "      - 知识库 (public/ 目录)"
        echo "      - 您添加的技能（skills/ 目录）"
        echo "      - 您的脚本和数据"
        echo ""
        echo "   📦 将更新以下内容:"
        echo "      - 通用技能（memory-search, rag, self-evolution, web-knowledge）"
        echo "      - 系统脚本（scripts/core/ 目录）"
        echo "      - 文档（README.md 等）"
        echo ""
        echo "   📝 您的自定义脚本:"
        echo "      - scripts/ 目录的其他文件不会被覆盖"
        echo "      - 请将自定义脚本放在 scripts/ 根目录"
        echo ""
        
        echo "❓ 是否继续？/ Continue?"
        echo "   y - 继续（迁移改造 / Migrate and update）"
        echo "   n - 取消 / Cancel"
        echo ""
        
        # 检查是否是交互式终端
        if [ -t 0 ]; then
            # 标准终端输入
            read -p "请输入 / Enter (y/N): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "❌ 已取消 / Cancelled"
                exit 1
            fi
        else
            # 管道输入，无法交互式确认
            echo ""
            echo "⚠️  检测到管道输入，无法读取确认"
            echo "⚠️  Detected pipe input, cannot read confirmation"
            echo ""
            echo "请使用以下方式之一 / Please use one of:"
            echo ""
            echo "1. 推荐方式（支持交互）/ Recommended (interactive):"
            echo "   bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)\" -s $AGENT_NAME"
            echo ""
            echo "2. 下载后运行 / Download first:"
            echo "   curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh"
            echo "   bash install.sh $AGENT_NAME"
            echo ""
            echo "3. 强制继续（跳过确认）/ Force (skip confirmation):"
            echo "   curl -s ... | bash -s $AGENT_NAME --force"
            echo ""
            exit 1
        fi
        
        cd "$WORKSPACE_ROOT"
    fi
else
    # 1. 克隆模板 / Clone template
    echo "1️⃣  克隆 evo-agents 模板 / Cloning template..."
    git clone --depth 1 https://github.com/luoboask/evo-agents.git "$WORKSPACE_ROOT"
    echo "   ✅ 克隆完成 / Clone complete"
    cd "$WORKSPACE_ROOT"
fi

# 2. 注册到 OpenClaw / Register to OpenClaw
echo ""
echo "2️⃣  注册到 OpenClaw / Registering to OpenClaw..."
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    echo "   ⚠️  Agent 已注册，跳过 / Agent already registered, skipping"
else
    openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE_ROOT" --non-interactive
    echo "   ✅ 注册完成 / Registration complete"
fi

# 4. 创建目录结构 / Create directory structure
echo ""
echo "4️⃣  创建目录结构 / Creating directory structure..."
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/$AGENT_NAME
echo "   ✅ 目录创建完成 / Directories created"

# 5. 测试 / Test
echo ""
echo "5️⃣  测试 / Testing..."
python3 scripts/session_recorder.py -t event -c "$AGENT_NAME 初始化完成" --agent $AGENT_NAME 2>/dev/null && \
    echo "   ✅ 测试通过 / Test passed" || echo "   ⚠️  测试跳过（可选）/ Test skipped (optional)"

# 6. 激活功能 / Activate Features (可选)
echo ""
if [[ -n "$ACTIVATE" ]]; then
    echo "6️⃣  激活功能 / Activating features..."
    echo ""
    
    # 检查 Ollama
    if command -v ollama &> /dev/null; then
        echo "   ✅ Ollama 已安装 / Ollama is installed"
        
        # 下载 bge-m3 模型（中文支持好）
        echo "   📥 下载嵌入模型 / Downloading embedding model..."
        ollama pull bge-m3 2>/dev/null && \
            echo "   ✅ bge-m3 模型就绪 / bge-m3 model ready" || \
            echo "   ⚠️  模型下载失败 / Model download failed"
    else
        echo "   ⚠️  Ollama 未安装 / Ollama not installed"
        echo "   安装方法 / Install:"
        echo "   macOS: brew install ollama"
        echo "   Linux: curl -fsSL https://ollama.com/install.sh | sh"
    fi
    
    echo ""
    echo "   ✅ 基础功能已激活 / Basic features activated"
    echo ""
    echo "   更多功能可以稍后运行 / For more features, run later:"
    echo "   ./scripts/activate-features.sh"
else
    echo "5️⃣  功能激活 / Feature Activation"
    echo ""
    echo "   要激活高级功能（语义搜索、RAG 等），请运行："
    echo "   To activate advanced features (semantic search, RAG, etc.):"
    echo ""
    echo "   ./scripts/activate-features.sh"
    echo ""
    echo "   或者使用 --activate 参数自动激活："
    echo "   Or use --activate flag for auto activation:"
    echo "   curl -s ... | bash -s $AGENT_NAME --activate"
    echo ""
fi

# 7. 完成 / Complete
echo ""
echo "8️⃣  完成 / Complete"
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 安装完成！/ Installation Complete!                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 安装位置 / Installation Location:"
echo "   Workspace: $WORKSPACE_ROOT"
echo "   Agent: $AGENT_NAME"
echo ""
echo "🚀 下一步 / Next Steps:"
echo "   cd $WORKSPACE_ROOT"
echo "   ./scripts/activate-features.sh  # 激活高级功能 / Activate features"
echo ""
echo "📖 文档 / Documentation:"
echo "   - README.md - 快速入门 / Quick Start"
echo "   - workspace-setup.md - 完整指南 / Full Guide"
echo "   - docs/MIGRATION.md - 迁移指南 / Migration Guide"
echo ""
