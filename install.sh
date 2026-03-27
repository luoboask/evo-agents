#!/bin/bash
# install.sh - 一键安装 evo-agents Workspace
# 用法：curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s <agent-name>
# Usage: curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s <agent-name>

set -e

AGENT_NAME="${1:-my-agent}"
FORCE="${2:-}"
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
    if [[ "$FORCE" == "--force" ]] || [[ "$FORCE" == "-f" ]]; then
        echo "⚠️  Workspace 已存在 / Workspace already exists"
        echo "   使用 --force 参数，跳过确认 / Using --force, skipping confirmation"
        echo ""
        cd "$WORKSPACE_ROOT"
    else
        echo "⚠️  Workspace 已存在 / Workspace already exists"
    echo ""
    echo "这可能是因为:"
    echo "This could be because:"
    echo "  1. 您之前安装过 / You installed before"
    echo "  2. 这是改造现有 Agent / This is migrating an existing agent"
    echo ""
    
    # Check if it looks like an evo-agents workspace | 检查是否像 evo-agents workspace
    if [ -f "$WORKSPACE_ROOT/skills/memory-search/search.py" ] || \
       [ -f "$WORKSPACE_ROOT/README.md" ]; then
        echo "📊 检测到现有 evo-agents workspace"
        echo "   Detected existing evo-agents workspace"
        echo ""
        echo "🔄 迁移改造 / Migration:"
        echo "   - ✅ 保留个人配置 (USER.md, SOUL.md 等)"
        echo "   - ✅ 保留记忆数据 (memory/, public/)"
        echo "   - 🗑️ 清理特定技能"
        echo "   - 📦 更新为通用模板"
        echo ""
    fi
    
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
        echo "请使用以下方式运行 / Please run:"
        echo "  bash install.sh $AGENT_NAME"
        echo ""
        echo "或者添加 --force 参数强制继续 / Or use --force to continue:"
        echo "  curl -s ... | bash -s $AGENT_NAME --force"
        echo ""
        exit 1
    fi
    
    cd "$WORKSPACE_ROOT"
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

# 3. 创建目录结构 / Create directory structure
echo ""
echo "3️⃣  创建目录结构 / Creating directory structure..."
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/$AGENT_NAME
echo "   ✅ 目录创建完成 / Directories created"

# 4. 如果是迁移，清理特定技能 / If migration, clean up specific skills
if [ -d "skills" ] && [ "$(ls -A skills 2>/dev/null)" ]; then
    SKILL_COUNT=$(ls -d skills/*/ 2>/dev/null | wc -l)
    if [ "$SKILL_COUNT" -gt 4 ]; then
        echo ""
        echo "🗑️  清理特定技能 / Cleaning up specific skills..."
        
        # 保留通用技能 / Keep universal skills
        KEEP_SKILLS="memory-search rag self-evolution web-knowledge"
        
        cd skills
        for dir in */; do
            skill=$(basename "$dir")
            if [[ ! " $KEEP_SKILLS " =~ " $skill " ]]; then
                echo "   🗑️  删除 / Removing: $skill"
                rm -rf "$dir"
            fi
        done
        cd ..
        echo "   ✅ 清理完成 / Cleanup complete"
    fi
fi

# 5. 测试 / Test
echo ""
echo "4️⃣  测试 / Testing..."
python3 scripts/session_recorder.py -t event -c "$AGENT_NAME 初始化完成" --agent $AGENT_NAME 2>/dev/null && \
    echo "   ✅ 测试通过 / Test passed" || echo "   ⚠️  测试跳过（可选）/ Test skipped (optional)"

# 6. 完成 / Complete
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
