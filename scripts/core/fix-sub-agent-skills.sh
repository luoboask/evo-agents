#!/bin/bash
# 修复子 Agent 技能目录结构
# 用法：./fix-sub-agent-skills.sh agent-name

set -e

AGENT_NAME="${1:-}"

if [ -z "$AGENT_NAME" ]; then
    echo "用法：$0 <agent-name>"
    exit 1
fi

WORKSPACE_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_DIR="$WORKSPACE_ROOT/agents/$AGENT_NAME"

echo "╔══════════════════════════════════════════════════╗"
echo "║     修复子 Agent 技能目录结构                       ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "📦 Agent: $AGENT_NAME"
echo "📁 Agent 目录：$AGENT_DIR"
echo ""

# 检查是否是子 Agent
if [ ! -d "$AGENT_DIR" ]; then
    echo "❌ Agent 目录不存在"
    exit 1
fi

# 检查是否有旧的符号链接
if [ -L "$AGENT_DIR/skills" ]; then
    echo "📝 重命名符号链接..."
    cd "$AGENT_DIR"
    mv skills skills-parent
    echo "   ✅ skills -> skills-parent"
fi

# 创建专属技能目录
echo "📁 创建专属技能目录..."
mkdir -p "$AGENT_DIR/skills"
echo "   ✅ skills/"

# 创建 README
cat > "$AGENT_DIR/skills/README.md" << 'MD'
# 子 Agent 专属技能

在此目录下创建子 Agent 专属技能。

## 结构

```
skills/
└── my-custom-skill/
    ├── SKILL.md
    └── ...
```

## 访问父 Agent 技能

父 Agent 的共享技能在 `../skills-parent/` 目录。
MD

echo "   ✅ README.md"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     ✅ 修复完成！                                 ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "新的目录结构:"
echo "  agents/$AGENT_NAME/"
echo "  ├── skills/             # 专属技能"
echo "  └── skills-parent/      # 父 Agent 技能（共享）"
