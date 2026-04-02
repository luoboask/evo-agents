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

# 检测系统语言
if locale | grep -q "zh_CN\|zh_CN\|Chinese"; then
    LANG="zh"
else
    LANG="en"
fi

# Git 源配置
GIT_URL="https://gitee.com/luoboask/evo-agents.git"
SOURCE_NAME="Gitee"

# 欢迎信息
if [ "$LANG" = "zh" ]; then
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  evo-agents 一键安装                                     ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Agent: $AGENT_NAME"
    echo "📁 Workspace: $WORKSPACE_ROOT"
    echo ""
else
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  evo-agents Quick Install                                ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Agent: $AGENT_NAME"
    echo "📁 Workspace: $WORKSPACE_ROOT"
    echo ""
fi

# 检查 workspace 是否存在
if [ -d "$WORKSPACE_ROOT" ]; then
    if [[ "$FORCE" == "--force" ]] || [[ "$FORCE" == "-f" ]]; then
        echo "⚠️  Workspace 已存在，强制继续"
        cd "$WORKSPACE_ROOT"
        echo "🧹 清理开发文件..."
        rm -rf .github/ 2>/dev/null || true
        rm -f CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md 2>/dev/null || true
        rm -f GITHUB_PUSH_RULES.md CHANGELOG.md workspace-setup.md 2>/dev/null || true
        rm -rf examples/ 2>/dev/null || true
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
    echo "📥 克隆模板..."
    echo "   源：$SOURCE_NAME ($GIT_URL)"
    
    if ! git clone --depth 1 "$GIT_URL" "$WORKSPACE_ROOT" 2>/dev/null; then
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
    
    echo "🧹 清理开发文件..."
    rm -rf .github/ 2>/dev/null || true
    rm -f CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md 2>/dev/null || true
    rm -f GITHUB_PUSH_RULES.md CHANGELOG.md workspace-setup.md 2>/dev/null || true
    rm -f README.zh-CN.md 2>/dev/null || true
    rm -f LICENSE 2>/dev/null || true
    rm -rf docs/dev/ docs/internal/ 2>/dev/null || true
    rm -rf examples/ 2>/dev/null || true
    rm -f skills/self-evolution/README_*.md 2>/dev/null || true
    rm -f skills/self-evolution/ARCHITECTURE.md 2>/dev/null || true
    rm -f skills/rag/report.html 2>/dev/null || true
    echo "   ✅ 完成"
fi

# 创建目录
if [ "$LANG" = "zh" ]; then
    echo "📁 创建目录..."
else
    echo "📁 Creating directories..."
fi
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/$AGENT_NAME/work data/$AGENT_NAME/archive data/$AGENT_NAME/drafts
mkdir -p scripts/user
echo "   ✅ Done"

# 注册到 OpenClaw
if [ "$LANG" = "zh" ]; then
    echo "📝 注册到 OpenClaw..."
else
    echo "📝 Registering to OpenClaw..."
fi
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    if [ "$LANG" = "zh" ]; then
        echo "   ⚠️  已注册"
    else
        echo "   ⚠️  Already registered"
    fi
else
    openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE_ROOT" --non-interactive
    if [ "$LANG" = "zh" ]; then
        echo "   ✅ 完成"
    else
        echo "   ✅ Done"
    fi
fi

# 在 AGENTS.md 中追加规则引用
if [ "$LANG" = "zh" ]; then
    echo "📋 配置 AGENTS.md..."
else
    echo "📋 Configuring AGENTS.md..."
fi
if [ -f "AGENTS.md" ] && ! grep -q "SKILL_RULES" AGENTS.md; then
    # 修改 Session Startup 部分，添加规则文档读取
    if grep -q "Read \`SOUL.md\`" AGENTS.md; then
        # 在 "Read SOUL.md" 后添加规则文档读取
        sed -i.bak 's/Read `SOUL.md` — this is who you are/Read `SOUL.md` — this is who you are\n5. Read `docs\/AGENT_BEHAVIOR.md`, `docs\/WORKSPACE_RULES.md`, `docs\/KNOWLEDGE_BASE_RULES.md` — workspace rules/' AGENTS.md
        rm -f AGENTS.md.bak
    fi
    
    cat >> AGENTS.md << 'EOF'

---

## 🎯 Agent Rules

### Core Behavior
- No independent goals (no self-preservation, replication, power-seeking)
- Safety first (pause on conflicts, respect stop requests)
- Don't manipulate or bypass safeguards
- Tool names are case-sensitive
- Search memory before answering about prior work
- Only load MEMORY.md in main sessions

**Full rules:** See `docs/AGENT_BEHAVIOR.md`

### Skill Usage
| When | Use |
|------|-----|
| User mentions history | `memory-search` |
| Real-time info | `web-knowledge` |
| Task completed | `self-evolution` (evolve) |
| End of day | `self-evolution` (nightly) |

**Full rules:** See `docs/SKILL_RULES.md`

### Workspace
- Temp downloads → `/tmp/`
- Git projects → `/tmp/` or `~/projects/`
- Don't clone/download in workspace root

**Full rules:** See `docs/WORKSPACE_RULES.md`

### Knowledge Base
| Type | Location | Access |
|------|----------|--------|
| Public | `skills/`, `docs/` | All Agents |
| Private | `MEMORY.md` | Main session only |
| Agent | `data/<agent>/` | Own Agent |

**Full rules:** See `docs/KNOWLEDGE_BASE_RULES.md`

### Sub-Agent
- Cannot access `MEMORY.md`
- Pass private info via `task` parameter
- Don't execute cron/heartbeat tasks

**Full rules:** See `docs/SUBAGENT_RULES.md`
EOF
fi
if [ "$LANG" = "zh" ]; then
    echo "   ✓ AGENTS.md 已配置"
else
    echo "   ✓ AGENTS.md configured"
fi

# 在 SOUL.md 中追加核心规则（如果文件存在）
if [ "$LANG" = "zh" ]; then
    echo "📝 配置 SOUL.md..."
else
    echo "📝 Configuring SOUL.md..."
fi
if [ -f "SOUL.md" ] && ! grep -q "核心规则" SOUL.md; then
    # 备份原文件
    cp SOUL.md SOUL.md.bak
    
    # 在顶部插入核心规则
    cat > SOUL.md.tmp << 'RULEEOF'
# SOUL.md - Who You Are

> ⚠️ **核心规则（每次会话必读）**
>
> **删除文件**：用户必须明确说"删除"，二次确认，优先 `trash`
>
> **隐私信息**：群聊中不分享私人内容
>
> **详细规则**：读 `AGENTS.md`

---

RULEEOF
    
    # 追加原内容（跳过原来的标题行）
    tail -n +2 SOUL.md.bak >> SOUL.md.tmp
    mv SOUL.md.tmp SOUL.md
    rm -f SOUL.md.bak
    
    if [ "$LANG" = "zh" ]; then
        echo "   ✓ SOUL.md 已配置"
    else
        echo "   ✓ SOUL.md configured"
    fi
else
    if [ "$LANG" = "zh" ]; then
        echo "   ⊘ SOUL.md 不存在或已配置"
    else
        echo "   ⊘ SOUL.md not found or already configured"
    fi
fi

# 复制规则文档到 docs/
if [ "$LANG" = "zh" ]; then
    echo "📋 复制规则文档..."
else
    echo "📋 Copying rule documents..."
fi
mkdir -p docs
for doc in AGENT_INSTRUCTIONS AGENT_BEHAVIOR SKILL_RULES WORKSPACE_RULES KNOWLEDGE_BASE_RULES SUBAGENT_RULES SCHEDULER; do
    src="$HOME/.openclaw/workspace/docs/${doc}.md"
    dst="docs/${doc}.md"
    if [ -f "$src" ] && [ ! -f "$dst" ]; then
        cp "$src" "$dst"
    fi
done
if [ "$LANG" = "zh" ]; then
    echo "   ✓ 规则已复制"
else
    echo "   ✓ Rules copied"
fi

# 创建必要文件
if [ "$LANG" = "zh" ]; then
    echo "📝 创建必要文件..."
else
    echo "📝 Creating files..."
fi
cat > memory/MEMORY.md << 'MEMEOF'
# MEMORY.md - 长期记忆

_重要的人、事、偏好、决定_

---

## 用户
- 名称：待填写
- 时区：Asia/Shanghai

## 重要事件

## 技能

## 偏好

## 决定
MEMEOF
touch data/.gitkeep
echo "   ✅ Done"

# 记录重要提示给 Agent
echo ""
if [ "$LANG" = "zh" ]; then
    echo "📝 记录重要提示给 Agent..."
else
    echo "📝 Recording workspace rules..."
fi
cd "$WORKSPACE_ROOT"
python3 scripts/core/session_recorder.py \
    -t event \
    -c "Workspace Rules: Read docs/WORKSPACE_RULES.md, docs/KNOWLEDGE_BASE_RULES.md, docs/AGENT_BEHAVIOR.md" \
    --agent "$AGENT_NAME" 2>/dev/null && \
    if [ "$LANG" = "zh" ]; then echo "   ✓ 已记录"; else echo "   ✓ Recorded"; fi \
    || if [ "$LANG" = "zh" ]; then echo "   ⊘ 跳过"; else echo "   ⊘ Skipped"; fi

# 创建安装配置文件
if [ "$LANG" = "zh" ]; then
    echo "📝 创建安装配置..."
else
    echo "📝 Creating install config..."
fi
cat > "$WORKSPACE_ROOT/.install-config" <<EOF
agent_name=$AGENT_NAME
workspace_path=$WORKSPACE_ROOT
install_time=$(date -Iseconds)
openclaw_registered=true
EOF
echo "   ✅ Done"

# 完成
echo ""
if [ "$LANG" = "zh" ]; then
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  ✅ 安装完成！                                           ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 位置：$WORKSPACE_ROOT"
    echo ""
    echo "🔮 激活高级特性（可选）:"
    echo "   cd $WORKSPACE_ROOT"
    echo "   ./scripts/core/activate-features.sh"
    echo ""
else
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  ✅ Installation Complete!                               ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 Location: $WORKSPACE_ROOT"
    echo ""
    echo "🔮 Activate features (optional):"
    echo "   cd $WORKSPACE_ROOT"
    echo "   ./scripts/core/activate-features.sh"
    echo ""
fi
