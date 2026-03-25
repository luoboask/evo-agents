#!/bin/bash
# init-agent.sh - 一键初始化 OpenClaw Agent
# 用法: curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s <agent-name>

set -e

AGENT_NAME="${1:-my-agent}"
WORKSPACE_ROOT="${HOME}/.openclaw/workspace-${AGENT_NAME}"
REPO_URL="https://github.com/luoboask/evo-agents.git"

echo "🚀 初始化 Agent: ${AGENT_NAME}"
echo "📁 Workspace: ${WORKSPACE_ROOT}"
echo ""

# 1. Clone 模板（如果 workspace 不存在）
if [ ! -d "${WORKSPACE_ROOT}" ]; then
    echo "⬇️  Clone 模板..."
    git clone --depth 1 --branch master "${REPO_URL}" "${WORKSPACE_ROOT}"
else
    echo "📂 Workspace 已存在，跳过 clone"
fi

cd "${WORKSPACE_ROOT}"

# 2. 创建目录结构
echo "📂 创建目录结构..."
mkdir -p memory/weekly memory/monthly memory/archive data/index "data/${AGENT_NAME}/memory" scripts/bridge

# 3. 修改默认 agent 名称
echo "⚙️  配置 agent 名称..."
for f in scripts/bridge/bridge_sync.py scripts/bridge/bridge_to_markdown.py scripts/bridge/bridge_to_knowledge.py scripts/unified_search.py scripts/memory_stats.py scripts/health_check.py scripts/session_recorder.py; do
    if [ -f "$f" ]; then
        sed -i.bak "s/default=\"demo-agent\"/default=\"${AGENT_NAME}\"/g; s/--agent\", \"demo-agent\"/--agent\", \"${AGENT_NAME}\"/g; s/--agent\", \"ai-baby\"/--agent\", \"${AGENT_NAME}\"/g" "$f" 2>/dev/null || true
        rm -f "${f}.bak"
    fi
done

# 4. 注册 OpenClaw agent
echo "📝 注册 OpenClaw agent..."
openclaw agents add "${AGENT_NAME}" --workspace "${WORKSPACE_ROOT}" --non-interactive 2>/dev/null || echo "(agent 可能已存在)"

# 5. 测试
echo ""
echo "🧪 测试..."
python3 scripts/session_recorder.py -t event -c "${AGENT_NAME} 初始化完成" 2>/dev/null || echo "⚠️  session_recorder 测试失败"

# 6. 输出结果
echo ""
echo "✅ Agent ${AGENT_NAME} 初始化完成！"
echo ""
echo "📋 下一步:"
echo "   cd ${WORKSPACE_ROOT}"
echo "   python3 scripts/session_recorder.py -t event -c '你的第一条记录'"
echo "   python3 scripts/unified_search.py '关键词' --agent ${AGENT_NAME}"
echo ""
echo "📚 文档: ${WORKSPACE_ROOT}/README.md"
echo "🧠 记忆流程: ${WORKSPACE_ROOT}/AGENTS.md"
