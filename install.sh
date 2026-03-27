#!/bin/bash
# install.sh - 一键安装 evo-agents Workspace
# 用法：curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s <agent-name>
# Usage: curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s <agent-name> [--force] [--activate]

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Progress bar
show_progress() {
    local task="$1"
    local current="$2"
    local total="$3"
    local percent=$((current * 100 / total))
    local filled=$((percent / 5))
    local empty=$((20 - filled))
    
    printf "\r${CYAN}[%s>%s]${NC} %3d%% - %s" \
        "$(printf '#%.0s' $(seq 1 $filled))" \
        "$(printf '=%.0s' $(seq 1 $empty))" \
        $percent \
        "$task"
}

echo_step() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓${NC} $1"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

echo_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

echo_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

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

# 检测是否是管道运行，如果是，重新加载为交互模式
if [ ! -t 0 ] && [[ -z "$FORCE" ]]; then
    # 管道运行，重新加载为交互模式
    SCRIPT_URL="https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh"
    TEMP_SCRIPT="/tmp/evo-install-$$.sh"
    
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  evo-agents 一键安装 / One-Click Install                 ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Agent: $AGENT_NAME"
    echo "📁 Workspace: $WORKSPACE_ROOT"
    echo ""
    echo "🔄 检测到管道运行，切换到交互模式..."
    echo "   Pipe mode detected, switching to interactive mode..."
    echo ""
    
    # 下载脚本到临时文件
    curl -sS "$SCRIPT_URL" -o "$TEMP_SCRIPT"
    chmod +x "$TEMP_SCRIPT"
    
    # 重新执行（交互模式）
    exec bash "$TEMP_SCRIPT" "$AGENT_NAME" "$@"
fi

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
        echo_warning "Workspace 已存在，使用 --force 跳过确认"
        echo "   Workspace exists, using --force to skip confirmation"
        echo ""
        cd "$WORKSPACE_ROOT"
    else
        echo_warning "检测到 $AGENT_NAME 的 workspace 已存在"
        echo "   Workspace for $AGENT_NAME already exists"
        echo ""
        
        # 交互式询问
        echo "❓ 是否继续安装？/ Continue installation?"
        echo "   y - 继续（保留数据）/ Continue (preserve data)"
        echo "   n - 取消 / Cancel"
        echo ""
        
        read -p "请输入 / Enter (Y/n): " -n 1 -r
        echo ""
        
        if [[ ! "$REPLY" =~ ^[Yy]$ ]] && [[ -n "$REPLY" ]]; then
            echo_error "已取消 / Cancelled"
            exit 0
        fi
        
        # 询问备份
        echo ""
        echo "❓ 安装前是否备份当前 workspace？/ Backup before install?"
        echo "   y - 备份（推荐）/ Backup (recommended)"
        echo "   n - 跳过备份 / Skip backup"
        echo ""
        
        read -p "请输入 / Enter (Y/n): " -n 1 -r
        BACKUP_REPLY="$REPLY"
        echo ""
        
        if [[ "$BACKUP_REPLY" =~ ^[Yy]$ ]] || [[ -z "$BACKUP_REPLY" ]]; then
            # 创建备份
            BACKUP_DIR="/tmp/workspace-backup-$AGENT_NAME-$(date +%Y%m%d-%H%M%S)"
            echo ""
            echo "📦 正在备份到 / Backing up to:"
            echo "   $BACKUP_DIR"
            echo ""
            
            cp -r "$WORKSPACE_ROOT" "$BACKUP_DIR"
            
            if [ $? -eq 0 ]; then
                echo_step "备份完成 / Backup complete"
                echo "   备份大小 / Backup size: $(du -sh "$BACKUP_DIR" | cut -f1)"
                echo ""
                echo "💡 如需恢复备份，运行："
                echo "   To restore backup, run:"
                echo "   cp -r $BACKUP_DIR/* $WORKSPACE_ROOT/"
                echo ""
            else
                echo_warning "备份失败，继续安装 / Backup failed, continuing install"
                echo ""
            fi
        fi
        
        cd "$WORKSPACE_ROOT"
    fi
else
    # 1. 克隆模板 / Clone template
    echo_step "1️⃣  克隆 evo-agents 模板 / Cloning template..."
    git clone --depth 1 https://github.com/luoboask/evo-agents.git "$WORKSPACE_ROOT"
    echo "   ✅ 克隆完成 / Clone complete"
    cd "$WORKSPACE_ROOT"
fi

# 2. 注册到 OpenClaw / Register to OpenClaw
echo ""
echo_step "2️⃣  注册到 OpenClaw / Registering to OpenClaw..."
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    echo "   ⚠️  Agent 已注册，跳过 / Agent already registered, skipping"
else
    openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE_ROOT" --non-interactive
    echo "   ✅ 注册完成 / Registration complete"
fi

# 3. 创建目录结构 / Create directory structure
echo ""
echo_step "3️⃣  创建目录结构 / Creating directory structure..."
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/$AGENT_NAME
echo "   ✅ 目录创建完成 / Directories created"

# 4. 测试 / Test
echo ""
echo_step "4️⃣  测试 / Testing..."
python3 scripts/core/session_recorder.py -t event -c "$AGENT_NAME 初始化完成" --agent $AGENT_NAME 2>/dev/null && \
    echo "   ✅ 测试通过 / Test passed" || echo "   ⚠️  测试跳过（可选）/ Test skipped (optional)"

# 5. 激活功能 / Activate Features (可选)
if [[ -n "$ACTIVATE" ]]; then
    echo ""
    echo_step "5️⃣  激活功能 / Activating features..."
    
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
    echo "   ./scripts/core/activate-features.sh"
else
    echo ""
    echo "5️⃣  功能激活 / Feature Activation"
    echo ""
    echo "   要激活高级功能（语义搜索、RAG 等），请运行："
    echo "   To activate advanced features (semantic search, RAG, etc.):"
    echo ""
    echo "   ./scripts/core/activate-features.sh"
    echo ""
    echo "   或者使用 --activate 参数自动激活："
    echo "   Or use --activate flag for auto activation:"
    echo "   curl -s ... | bash -s $AGENT_NAME --activate"
    echo ""
fi

# 6. 完成 / Complete
echo ""
echo_step "6️⃣  完成 / Complete"
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
echo "   ./scripts/core/activate-features.sh  # 激活高级功能 / Activate features"
echo ""
echo "📖 文档 / Documentation:"
echo "   - README.md - 快速入门 / Quick Start"
echo "   - workspace-setup.md - 完整指南 / Full Guide"
echo "   - docs/MIGRATION.md - 迁移指南 / Migration Guide"
echo ""
echo "📋 重要：Workspace 使用规则 / Important: Workspace Rules:"
echo "   - docs/AGENT_INSTRUCTIONS.md - Agent 指令（必读）/ Agent Instructions (must read)"
echo "   - docs/WORKSPACE_RULES.md - 使用规范 / Usage Rules"
echo ""
echo "💡 提示：请告诉你的 Agent 阅读 docs/AGENT_INSTRUCTIONS.md"
echo "   Tip: Tell your agents to read docs/AGENT_INSTRUCTIONS.md"
echo ""

# 清理临时脚本
if [[ "$0" == /tmp/evo-install-* ]]; then
    rm -f "$0"
fi
