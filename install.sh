#!/bin/bash
# install.sh - 一键安装 evo-agents Workspace
# 用法：curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s <agent-name>

set -e

AGENT_NAME="${1:-my-agent}"
WORKSPACE_ROOT="$HOME/.openclaw/workspace-$AGENT_NAME"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  evo-agents 一键安装                                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 安装 Agent: $AGENT_NAME"
echo "📁 Workspace: $WORKSPACE_ROOT"
echo ""

# 1. 克隆模板
echo "1️⃣  克隆 evo-agents 模板..."
if [ -d "$WORKSPACE_ROOT" ]; then
    echo "   ⚠️  Workspace 已存在，跳过克隆"
else
    git clone --depth 1 https://github.com/luoboask/evo-agents.git "$WORKSPACE_ROOT"
    echo "   ✅ 克隆完成"
fi

cd "$WORKSPACE_ROOT"

# 2. 注册到 OpenClaw
echo ""
echo "2️⃣  注册到 OpenClaw..."
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    echo "   ⚠️  Agent 已注册，跳过"
else
    openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE_ROOT" --non-interactive
    echo "   ✅ 注册完成"
fi

# 3. 创建目录结构
echo ""
echo "3️⃣  创建目录结构..."
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/$AGENT_NAME
echo "   ✅ 目录创建完成"

# 4. 测试
echo ""
echo "4️⃣  测试..."
python3 scripts/session_recorder.py -t event -c "$AGENT_NAME 初始化完成" --agent $AGENT_NAME 2>/dev/null && \
    echo "   ✅ 测试通过" || echo "   ⚠️  测试跳过（可选）"

# 5. 完成
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ 安装完成！                                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 安装位置："
echo "   Workspace: $WORKSPACE_ROOT"
echo "   Agent: $AGENT_NAME"
echo ""
echo "🚀 下一步："
echo "   cd $WORKSPACE_ROOT"
echo "   ./scripts/activate-features.sh  # 激活高级功能"
echo ""
echo "📖 文档："
echo "   - README.md - 快速入门"
echo "   - workspace-setup.md - 完整指南"
echo ""
