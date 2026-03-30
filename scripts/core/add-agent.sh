#!/bin/bash
# add-agent.sh - 新增单个 Agent
# 用法：./add-agent.sh <role> [description] [emoji]
# 说明：会自动生成 role-agent，如果已带 -agent 则不再添加

set -e

# 自动获取 workspace 目录（scripts/core/的父目录的父目录）
WORKSPACE="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$WORKSPACE"

# 必须传参数
AGENT_NAME="$1"
DESC="${2:-助手}"
EMOJI="${3:-🤖}"

if [ -z "$AGENT_NAME" ]; then
    echo "用法：./add-agent.sh <role> [description] [emoji]"
    echo ""
    echo "说明：会自动生成 role-agent，如果已带 -agent 则不再添加"
    echo ""
    echo "示例:"
    echo "   ./add-agent.sh designer"
    echo "   ./add-agent.sh designer-agent"
    echo "   ./add-agent.sh designer UI/UX 设计师 🎨"
    exit 1
fi

# 添加 -agent 后缀（如果没有）
if [[ "$AGENT_NAME" == *"-agent" ]]; then
    # 已有 -agent，不再添加
    :
else
    # 没有 -agent，添加后缀
    AGENT_NAME="${AGENT_NAME}-agent"
fi

# 提取角色名
ROLE="${AGENT_NAME%-agent}"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     新增子 Agent: $AGENT_NAME ($DESC $EMOJI)"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Workspace: $WORKSPACE"
echo ""

# 1. 创建目录
echo "📁 创建目录..."
mkdir -p "agents/$AGENT_NAME/memory"
echo "   ✅ agents/$AGENT_NAME/memory"

# 2. 创建配置文件
echo ""
echo "📝 创建配置文件..."

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

echo "   ✅ AGENTS.md, SOUL.md, MEMORY.md, config.yaml"

# 3. 注册到 OpenClaw
echo ""
echo "📝 注册到 OpenClaw..."
if openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE/agents/$AGENT_NAME" --non-interactive 2>/dev/null; then
    echo "   ✅ 已注册"
else
    echo "   ⚠️  可能已存在"
fi

# 4. 更新 config/agents.yaml
echo ""
echo "📝 更新 config/agents.yaml..."
if grep -q "^$AGENT_NAME:" config/agents.yaml 2>/dev/null; then
    echo "   ⏭️  配置已存在"
else
    cat >> config/agents.yaml << EOF

# Sub-agent: $AGENT_NAME
$AGENT_NAME:
  name: $AGENT_NAME
  role: $ROLE
  data_path: agents/$AGENT_NAME/data
  memory_path: agents/$AGENT_NAME/memory
EOF
    echo "   ✅ 已添加"
fi

# 5. 输出结果
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     ✅ $AGENT_NAME 创建完成！"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 信息:"
echo "   • 名称：$AGENT_NAME"
echo "   • 角色：$DESC"
echo "   • Emoji: $EMOJI"
echo ""
echo "🎯 使用:"
echo "   python3 scripts/session_recorder.py -t event -c '内容' --agent $AGENT_NAME"
echo "   openclaw agent --agent $AGENT_NAME --message '任务'"
echo ""

# 创建子 Agent 的 scripts/, skills/, libs/ 目录
echo ""
echo "📁 创建子 Agent 资源目录..."
WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "agents/$AGENT_NAME"

# 创建 scripts/ 和 libs/ 空目录（可选，Agent 特定）
mkdir -p scripts libs 2>/dev/null || true
echo "   ✅ 已创建 scripts/, libs/ 目录（可放置 Agent 特定资源）"

# 创建 skills/ 符号链接到父 workspace（共享技能）
mkdir -p skills
echo "   ✅ skills/（专属技能）"
ln -sf ../../skills-parent skills-parent
echo "   ✅ skills-parent/（共享父 Agent 技能）" 2>/dev/null || true
echo "   ✅ 已创建 skills/ → ../../skills（共享父 workspace 技能）"

echo "   💡 提示：scripts/ 和 libs/ 可以放置 Agent 特定资源"
cd "$WORKSPACE_ROOT"

