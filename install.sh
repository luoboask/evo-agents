#!/bin/bash
# install.sh - evo-agents 一键安装
# 
# 用法:
#   推荐（国内）：curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s my-agent
#   海外：curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent

set -e

AGENT_NAME="${1:-my-agent}"
FORCE="${2:-}"
WORKSPACE_ROOT="$HOME/.openclaw/workspace-$AGENT_NAME"

# 检测脚本来源，自动选择对应 Git 源
if [[ "${BASH_SOURCE[0]}" == *"gitee.com"* ]] || [[ "$0" == *"gitee.com"* ]]; then
    # 从 Gitee 下载，使用 Gitee Git 源
    GIT_URL="https://gitee.com/luoboask/evo-agents.git"
    SOURCE_NAME="Gitee"
else
    # 从 GitHub 下载，优先尝试 Gitee（国内更快）
    GIT_URL="https://gitee.com/luoboask/evo-agents.git"
    SOURCE_NAME="Gitee (优先)"
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  evo-agents 一键安装                                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "📁 Workspace: $WORKSPACE_ROOT"
echo ""

# 检查 workspace 是否存在
if [ -d "$WORKSPACE_ROOT" ]; then
    if [[ "$FORCE" == "--force" ]] || [[ "$FORCE" == "-f" ]]; then
        echo "⚠️  Workspace 已存在，强制继续"
        cd "$WORKSPACE_ROOT"
        # 清理开发文件（即使已存在）
        echo "🧹 清理开发文件..."
        rm -rf .github/ 2>/dev/null || true
        rm -f CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md 2>/dev/null || true
        rm -f GITHUB_PUSH_RULES.md CHANGELOG.md workspace-setup.md 2>/dev/null || true
        rm -rf examples/ libs/ 2>/dev/null || true
        rm -f skills/self-evolution/README_*.md skills/self-evolution/ARCHITECTURE.md 2>/dev/null || true
        rm -f skills/rag/report.html 2>/dev/null || true
        echo "   ✅ 完成"
    else
        echo "⚠️  Workspace 已存在"
        echo ""
        echo "💡 建议："
        echo "   1. 下载脚本以获得交互体验："
        echo "      curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh"
        echo "      bash install.sh $AGENT_NAME"
        echo ""
        echo "   2. 或使用 --force 强制继续："
        echo "      curl -fsSL ... | bash -s $AGENT_NAME --force"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "继续安装（10 秒后自动继续，按 Ctrl+C 取消）..."
        sleep 10
        cd "$WORKSPACE_ROOT"
    fi
else
    # 克隆模板
    echo "📥 克隆模板..."
    echo "   源：$SOURCE_NAME ($GIT_URL)"
    
    if ! git clone --depth 1 "$GIT_URL" "$WORKSPACE_ROOT" 2>/dev/null; then
        # Gitee 失败时尝试 GitHub
        if [[ "$GIT_URL" == *"gitee.com"* ]]; then
            echo "   ⚠️  Gitee 失败，尝试 GitHub..."
            GIT_URL="https://github.com/luoboask/evo-agents.git"
            if ! git clone --depth 1 "$GIT_URL" "$WORKSPACE_ROOT" 2>/dev/null; then
                echo "❌ 所有源都失败，请检查网络连接"
                exit 1
            fi
        else
            echo "❌ 克隆失败，请检查网络连接"
            exit 1
        fi
    fi
    
    cd "$WORKSPACE_ROOT"
    
    # 清理用户不需要感知的开发文件
    echo "🧹 清理开发文件..."
    rm -rf .github/  # GitHub 开发配置
    rm -f CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md  # 贡献者文档
    rm -f GITHUB_PUSH_RULES.md CHANGELOG.md workspace-setup.md  # 维护文档
    rm -f README.zh-CN.md  # 冗余（README.md 已包含中文）
    rm -f LICENSE  # 许可证（GitHub 显示需要，用户不需要）
    rm -f FEATURE_ACTIVATION_GUIDE.md  # 功能激活指南（移到 docs/）
    mv -f FEATURE_ACTIVATION_GUIDE.md docs/ 2>/dev/null || true  # 移到 docs/
    rm -rf examples/  # 示例（用户不需要）
    # rm -rf libs/  # 保留 libs/memory_hub（知识库系统需要）
    rm -f skills/self-evolution/README_*.md  # 技能内部文档
    rm -f skills/self-evolution/ARCHITECTURE.md
    rm -f skills/rag/report.html  # 运行时生成
    echo "   ✅ 完成"
fi

# 注册到 OpenClaw
echo "📝 注册到 OpenClaw..."
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    echo "   ⚠️  已注册"
else
    openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE_ROOT" --non-interactive
    echo "   ✅ 完成"
fi

# 创建目录
echo "📁 创建目录..."
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/$AGENT_NAME
mkdir -p scripts/user
echo "   ✅ 完成"

# 创建安装配置文件（用于路径解析）
echo "📝 创建安装配置..."
cat > "$WORKSPACE_ROOT/.install-config" <<EOF
agent_name=$AGENT_NAME
workspace_path=$WORKSPACE_ROOT
install_time=$(date -Iseconds)
openclaw_registered=true
EOF
echo "   ✅ 完成"

# 记录重要提示给 Agent
echo ""
echo "📝 记录重要提示给 Agent..."
cd "$WORKSPACE_ROOT"  # 确保在正确的 workspace
python3 scripts/core/session_recorder.py \
    -t event \
    -c "📋 重要：Workspace 使用规则

请阅读以下文档：
1. docs/AGENT_INSTRUCTIONS.md - Agent 指令（必读）
2. docs/WORKSPACE_RULES.md - 使用规范

重要规则：
- 脚本放在 scripts/ 目录
- Git 项目放在 /tmp/ 或 ~/projects/ 或 data/<agent>/work/
- 不要在根目录创建文件或克隆项目
- 记忆数据自动保存在 memory/ 和 data/ 目录" \
    --agent "$AGENT_NAME" 2>/dev/null && \
    echo "   ✅ 已记录给 Agent" || echo "   ⚠️  跳过"

# 完成
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 安装完成！                                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 位置：$WORKSPACE_ROOT"
echo ""

# 提示激活高级特性
echo "🔮 激活高级特性..."
echo ""
echo "💡 提示：安装完成后，建议激活高级特性："
echo ""
echo "   cd $WORKSPACE_ROOT"
echo "   ./scripts/core/activate-features.sh"
echo ""
echo "   或者在 OpenClaw 中直接使用，需要时再激活"
echo ""
