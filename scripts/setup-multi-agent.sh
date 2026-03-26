#!/bin/bash
# setup-multi-agent.sh - 一键创建多 Agent 体系
# 用法：./setup-multi-agent.sh <role1> [role2] [role3] ...
# 说明：每个角色会自动生成 role-agent，如果已带 -agent 则不再添加

set -e

# 自动获取 workspace 目录（脚本的父目录）
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

# 必须传参数
if [ $# -eq 0 ]; then
    echo "用法：./setup-multi-agent.sh <role1> [role2] [role3] ..."
    echo ""
    echo "说明：每个角色会自动生成 role-agent，如果已带 -agent 则不再添加"
    echo ""
    echo "示例:"
    echo "   ./setup-multi-agent.sh designer writer ops"
    echo "   ./setup-multi-agent.sh designer-agent writer-agent"
    echo "   ./setup-multi-agent.sh \"designer:UI/UX 设计师:🎨\" \"writer:内容创作者:✍️\""
    exit 1
fi

AGENTS=("$@")

echo "╔════════════════════════════════════════════════════════╗"
echo "║     创建多 Agent 体系                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo "📋 角色列表：${AGENTS[*]}"
echo ""

# 创建子 Agent
for agent_spec in "${AGENTS[@]}"; do
    # 解析 agent_spec (格式：name:desc:emoji 或 name)
    IFS=':' read -ra PARTS <<< "$agent_spec"
    NAME="${PARTS[0]}"
    
    # 添加 -agent 后缀（如果没有）
    if [[ "$NAME" == *"-agent" ]]; then
        AGENT_NAME="$NAME"
    else
        AGENT_NAME="${NAME}-agent"
    fi
    
    # 默认描述和 emoji
    DESC="${PARTS[1]:-${PARTS[0]}}"
    EMOJI="${PARTS[2]:-🤖}"
    
    # 提取角色名（去掉 -agent 后缀）
    ROLE="${AGENT_NAME%-agent}"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📁 创建 $AGENT_NAME ($DESC $EMOJI)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 1. 创建目录
    mkdir -p "agents/$AGENT_NAME/{memory,data}"
    echo "   ✅ 目录结构"
    
    # 2. 创建配置文件
    cat > "agents/$AGENT_NAME/AGENTS.md" << EOF
# AGENTS.md - $AGENT_NAME

**角色：** $DESC
**职责：** 专业任务处理

## 工作流程
1. 接收任务
2. 处理任务
3. 输出结果
EOF
    
    cat > "agents/$AGENT_NAME/SOUL.md" << EOF
# SOUL.md - $AGENT_NAME

**你是谁：** $DESC
**emoji：** $EMOJI

## 个性
- 专业、认真、负责
- 善于思考和解决问题
EOF
    
    cat > "agents/$AGENT_NAME/MEMORY.md" << EOF
# MEMORY.md - $AGENT_NAME

## 长期记忆
_重要的人、事、偏好、决定_

## 用户
- 名称：待填写
- 时区：Asia/Shanghai
EOF
    
    cat > "agents/$AGENT_NAME/config.yaml" << EOF
agent:
  name: $AGENT_NAME
  role: $ROLE
  description: "$DESC"
  data_path: agents/$AGENT_NAME/data
  memory_path: agents/$AGENT_NAME/memory
EOF
    
    echo "   ✅ 配置文件"
    
    # 3. 注册到 OpenClaw
    if openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE/agents/$AGENT_NAME" --non-interactive 2>/dev/null; then
        echo "   ✅ 已注册到 OpenClaw"
    else
        echo "   ⚠️  可能已存在"
    fi
    
    echo ""
done

# 4. 更新 config/agents.yaml
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 更新 config/agents.yaml..."

MAIN_AGENT=$(basename "$WORKSPACE" | sed 's/workspace-//')

cat > config/agents.yaml << EOF
# Multi-Agent Configuration
# Main agent
$MAIN_AGENT:
  name: $MAIN_AGENT
  role: coordinator
  data_path: data/$MAIN_AGENT
  memory_path: memory

# Sub-agents
EOF

for agent_spec in "${AGENTS[@]}"; do
    IFS=':' read -ra PARTS <<< "$agent_spec"
    NAME="${PARTS[0]}"
    if [[ "$NAME" == *"-agent" ]]; then
        AGENT_NAME="$NAME"
    else
        AGENT_NAME="${NAME}-agent"
    fi
    ROLE="${AGENT_NAME%-agent}"
    DESC="${PARTS[1]:-$ROLE}"
    
    cat >> config/agents.yaml << EOF
$AGENT_NAME:
  name: $AGENT_NAME
  role: $ROLE
  data_path: agents/$AGENT_NAME/data
  memory_path: agents/$AGENT_NAME/memory

EOF
done

echo "   ✅ 已更新"

# 5. 输出结果
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     ✅ 多 Agent 体系创建完成！                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 创建结果:"
echo "   • $MAIN_AGENT (主协调)"
for agent_spec in "${AGENTS[@]}"; do
    IFS=':' read -ra PARTS <<< "$agent_spec"
    NAME="${PARTS[0]}"
    if [[ "$NAME" == *"-agent" ]]; then
        AGENT_NAME="$NAME"
    else
        AGENT_NAME="${NAME}-agent"
    fi
    DESC="${PARTS[1]:-$NAME}"
    EMOJI="${PARTS[2]:-🤖}"
    echo "   • $AGENT_NAME ($DESC $EMOJI)"
done
echo ""
echo "🎯 使用:"
echo "   python3 scripts/session_recorder.py -t event -c '内容' --agent <agent-name>"
echo "   openclaw agent --agent <agent-name> --message '任务'"
echo ""
