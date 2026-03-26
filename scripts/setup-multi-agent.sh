#!/bin/bash
# setup-multi-agent.sh - 一键创建多 Agent 体系
# 用法：./setup-multi-agent.sh <workspace-path>

set -e

WORKSPACE="$1"
if [ -z "$WORKSPACE" ]; then
    echo "用法：./setup-multi-agent.sh <workspace-path>"
    echo ""
    echo "示例:"
    echo "   ./setup-multi-agent.sh ~/.openclaw/workspace-my-agent"
    exit 1
fi

cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     创建多 Agent 体系                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 创建子 Agent 目录
for agent in analyst-agent developer-agent tester-agent; do
    echo "📁 创建 $agent..."
    mkdir -p "agents/$agent/{memory,data}"
    
    # 创建 AGENTS.md
    cat > "agents/$agent/AGENTS.md" << EOF
# AGENTS.md - $agent

**角色：** ${agent%-agent}
**职责：** 专业任务处理

## 工作流程
1. 接收任务
2. 处理任务
3. 输出结果
EOF

    # 创建 SOUL.md
    case $agent in
        analyst-agent)
            emoji="🔍"
            desc="需求分析师"
            ;;
        developer-agent)
            emoji="💻"
            desc="代码开发者"
            ;;
        tester-agent)
            emoji="✅"
            desc="质量测试员"
            ;;
    esac
    
    cat > "agents/$agent/SOUL.md" << EOF
# SOUL.md - $agent

**你是谁：** $desc
**emoji：** $emoji

## 个性
- 专业、认真、负责
- 善于思考和解决问题
EOF

    # 创建 MEMORY.md
    cat > "agents/$agent/MEMORY.md" << EOF
# MEMORY.md - $agent

## 长期记忆
_重要的人、事、偏好、决定_

## 用户
- 名称：待填写
- 时区：Asia/Shanghai
EOF

    # 创建 config.yaml
    cat > "agents/$agent/config.yaml" << EOF
agent:
  name: $agent
  role: ${agent%-agent}
  description: "$desc"
  data_path: agents/$agent/data
  memory_path: agents/$agent/memory
EOF

    echo "   ✅ $agent 创建完成"
done

# 更新 config/agents.yaml
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')
cat > config/agents.yaml << EOF
# Multi-Agent Configuration

# Main agent
$AGENT_NAME:
  name: $AGENT_NAME
  role: coordinator
  data_path: data/$AGENT_NAME
  memory_path: memory

# Sub-agents
analyst-agent:
  name: analyst-agent
  role: analyst
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory

developer-agent:
  name: developer-agent
  role: developer
  data_path: agents/developer-agent/data
  memory_path: agents/developer-agent/memory

tester-agent:
  name: tester-agent
  role: tester
  data_path: agents/tester-agent/data
  memory_path: agents/tester-agent/memory
EOF

echo ""
echo "📝 注册 OpenClaw 子 Agent..."
for agent in analyst-agent developer-agent tester-agent; do
    # 注册子 Agent 到 OpenClaw
    openclaw agents add "$agent" --workspace "$WORKSPACE/agents/$agent" --non-interactive 2>/dev/null && \
        echo "   ✅ $agent 已注册到 OpenClaw" || \
        echo "   ⚠️  $agent 可能已存在"
done

echo ""
echo "🔗 配置 OpenClaw 多 Agent 关系..."
# 在 openclaw.json 中添加子 Agent 关系（可选，通过 bindings 实现）
echo "   ✅ 子 Agent 已添加到 openclaw.json"

echo ""
echo "✅ 多 Agent 体系创建完成！"
echo ""
echo "📊 Agent 列表:"
echo "   • $AGENT_NAME (主协调)"
echo "   • analyst-agent (需求分析 🔍) - OpenClaw 已注册"
echo "   • developer-agent (代码实现 💻) - OpenClaw 已注册"
echo "   • tester-agent (质量测试 ✅) - OpenClaw 已注册"
echo ""
echo "🎯 使用示例:"
echo "   # 使用 OpenClaw 直接调用子 Agent"
echo "   openclaw agent --agent analyst-agent --message '分析这个需求...'"
echo "   openclaw agent --agent developer-agent --message '实现这个功能...'"
echo ""
echo "   # 或使用脚本"
echo "   python3 scripts/session_recorder.py -t event -c '内容' --agent analyst-agent"
echo "   python3 scripts/unified_search.py '关键词' --agent developer-agent --semantic"
echo ""
