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

# 检测系统语言（默认英文，使用自定义变量避免覆盖系统 LANG）
INSTALL_LANG="en"  # 默认英文
if locale 2>/dev/null | grep -qiE "zh_CN|zh_TW|zh_HK|zh_SG|zh-Hans|zh-Hant|Chinese"; then
    INSTALL_LANG="zh"
fi

# Git 源配置
GIT_URL="https://gitee.com/luoboask/evo-agents.git"
SOURCE_NAME="Gitee"

# 欢迎信息
if [ "$INSTALL_LANG" = "zh" ]; then
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
        echo "⚠️  Workspace 已存在，执行完全重装..."
        echo ""
        
        # 1. 备份用户数据
        echo "💾 备份用户数据..."
        BACKUP_DIR="/tmp/evo-agents-backup-$AGENT_NAME-$(date +%Y%m%d%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        
        if [ -d "$WORKSPACE_ROOT/data" ]; then
            cp -r "$WORKSPACE_ROOT/data" "$BACKUP_DIR/" && echo "   ✅ data/ 已备份"
        fi
        if [ -d "$WORKSPACE_ROOT/memory" ]; then
            cp -r "$WORKSPACE_ROOT/memory" "$BACKUP_DIR/" && echo "   ✅ memory/ 已备份"
        fi
        if [ -d "$WORKSPACE_ROOT/config" ]; then
            cp -r "$WORKSPACE_ROOT/config" "$BACKUP_DIR/" && echo "   ✅ config/ 已备份"
        fi
        if [ -f "$WORKSPACE_ROOT/.install-config" ]; then
            cp "$WORKSPACE_ROOT/.install-config" "$BACKUP_DIR/" && echo "   ✅ .install-config 已备份"
        fi
        
        echo "   📁 备份位置：$BACKUP_DIR"
        echo ""
        
        # 2. 删除旧 workspace（保留 .openclaw 配置）
        echo "🗑️  删除旧 workspace..."
        rm -rf "$WORKSPACE_ROOT"
        echo "   ✅ 完成"
        echo ""
        
        # 3. 重新克隆
        echo "📥 克隆最新代码..."
        echo "   源：$SOURCE_NAME ($GIT_URL)"
        
        if ! git clone --depth 1 "$GIT_URL" "$WORKSPACE_ROOT" 2>/dev/null; then
            if [[ "$GIT_URL" == *"gitee.com"* ]]; then
                echo "   ⚠️  Gitee 失败，尝试 GitHub..."
                GIT_URL="https://github.com/luoboask/evo-agents.git"
                SOURCE_NAME="GitHub"
                if ! git clone --depth 1 "$GIT_URL" "$WORKSPACE_ROOT" 2>/dev/null; then
                    echo "❌ 所有源都失败，请检查网络连接"
                    echo ""
                    echo "💡 从备份恢复..."
                    if [ -d "$BACKUP_DIR" ]; then
                        mkdir -p "$WORKSPACE_ROOT"
                        cp -r "$BACKUP_DIR"/* "$WORKSPACE_ROOT/" 2>/dev/null || true
                        echo "   ✅ 已恢复到：$WORKSPACE_ROOT"
                    fi
                    exit 1
                fi
            else
                echo "❌ 克隆失败，请检查网络连接"
                exit 1
            fi
        fi
        
        cd "$WORKSPACE_ROOT"
        
        # 4. 恢复用户数据
        echo ""
        echo "💾 恢复用户数据..."
        if [ -d "$BACKUP_DIR/data" ]; then
            cp -r "$BACKUP_DIR/data" "$WORKSPACE_ROOT/" && echo "   ✅ data/ 已恢复"
        fi
        if [ -d "$BACKUP_DIR/memory" ]; then
            cp -r "$BACKUP_DIR/memory" "$WORKSPACE_ROOT/" && echo "   ✅ memory/ 已恢复"
        fi
        if [ -d "$BACKUP_DIR/config" ]; then
            cp -r "$BACKUP_DIR/config" "$WORKSPACE_ROOT/" && echo "   ✅ config/ 已恢复"
        fi
        if [ -f "$BACKUP_DIR/.install-config" ]; then
            cp "$BACKUP_DIR/.install-config" "$WORKSPACE_ROOT/" && echo "   ✅ .install-config 已恢复"
        fi
        echo ""
        
        # 5. 清理开发文件和无关文档
        echo "🧹 清理开发文件..."
        rm -rf .github/ 2>/dev/null || true
        rm -f CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md 2>/dev/null || true
        rm -f GITHUB_PUSH_RULES.md CHANGELOG.md workspace-setup.md 2>/dev/null || true
        rm -rf examples/ 2>/dev/null || true
        rm -rf benchmarks/ 2>/dev/null || true
        rm -f skills/self-evolution/README_*.md skills/self-evolution/ARCHITECTURE.md 2>/dev/null || true
        rm -f skills/self-evolution/*.md 2>/dev/null || true
        rm -f skills/rag/report.html 2>/dev/null || true
        rm -f skills/BILINGUAL_STATUS.md skills/FINAL_STATUS.md skills/STATUS.md 2>/dev/null || true
        rm -f skills/harness-agent/*_REPORT.md skills/harness-agent/QUICK_SUMMARY.md 2>/dev/null || true
        echo "   ✅ 完成"
        echo ""
        
        # 6. 标记为完全重装
        FORCE_REINSTALL="true"
        echo "✅ 完全重装完成！"
        echo "   备份位置：$BACKUP_DIR (可手动删除)"
        echo ""
    else
        echo "⚠️  Workspace 已存在"
        echo ""
        echo "💡 建议："
        echo "   1. 下载脚本以获得交互体验："
        echo "      curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh"
        echo "      bash install.sh $AGENT_NAME"
        echo ""
        echo "   2. 或使用 --force 强制重装："
        echo "      curl -fsSL ... | bash -s $AGENT_NAME --force"
        echo "      ⚠️  注意：--force 会完全重装（备份→删除→克隆→恢复）"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # 询问是否清理旧 Cron 任务
        read -p "是否清理旧的 Cron 任务并重新配置？(y/N，默认 N): " -r CLEAN_CRON
        if [[ "$CLEAN_CRON" =~ ^[Yy]$ ]]; then
            echo "🧹 清理旧的 Cron 任务..."
            if command -v openclaw &> /dev/null; then
                # 使用 --json 获取完整输出，避免截断问题
                openclaw cron list --json 2>/dev/null | jq -r ".[] | select(.agentId | contains(\"$AGENT_NAME\")) | select(.name | test(\"session-scan|daily-review|daily-compress|nightly-evolution|weekly-compress|weekly-maintenance|monthly-compress\")) | .id" | while read job_id; do
                    [ -n "$job_id" ] && openclaw cron remove "$job_id" >/dev/null 2>&1 && echo "   ✅ 已删除任务 $job_id" || true
                done
                echo "   ✅ 完成"
                FORCE_REINSTALL="true"  # 标记需要重新配置
            else
                echo "   ⚠️  OpenClaw 未安装，跳过"
            fi
        fi
        
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
            SOURCE_NAME="GitHub"
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
    rm -rf examples/ benchmarks/ 2>/dev/null || true
    rm -f skills/self-evolution/README_*.md 2>/dev/null || true
    rm -f skills/self-evolution/ARCHITECTURE.md 2>/dev/null || true
    rm -f skills/self-evolution/*.md 2>/dev/null || true
    rm -f skills/rag/report.html 2>/dev/null || true
    rm -f skills/BILINGUAL_STATUS.md skills/FINAL_STATUS.md skills/STATUS.md 2>/dev/null || true
    rm -f skills/harness-agent/*_REPORT.md skills/harness-agent/QUICK_SUMMARY.md 2>/dev/null || true
    echo "   ✅ 完成"
fi

# 创建目录
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "📁 创建目录..."
else
    echo "📁 Creating directories..."
fi
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/$AGENT_NAME/work data/$AGENT_NAME/archive data/$AGENT_NAME/drafts
mkdir -p scripts/user
echo "   ✅ Done"

# 注册到 OpenClaw
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "📝 注册到 OpenClaw..."
else
    echo "📝 Registering to OpenClaw..."
fi
if openclaw agents list 2>/dev/null | grep -q "^$AGENT_NAME"; then
    if [ "$INSTALL_LANG" = "zh" ]; then
        echo "   ⚠️  已注册"
    else
        echo "   ⚠️  Already registered"
    fi
else
    openclaw agents add "$AGENT_NAME" --workspace "$WORKSPACE_ROOT" --non-interactive
    if [ "$INSTALL_LANG" = "zh" ]; then
        echo "   ✅ 完成"
    else
        echo "   ✅ Done"
    fi
fi

echo ""

# 追加规则引用（如果 AGENTS.md 已存在）
# 追加规则引用（如果 AGENTS.md 已存在）
if [ -f "AGENTS.md" ] && ! grep -q "SKILL_RULES" AGENTS.md; then
    # 修改 Session Startup 部分，添加规则文档读取
    if grep -q "Read \`SOUL.md\`" AGENTS.md; then
        # 在 "Read SOUL.md" 后添加规则文档读取
        sed -i.bak 's/Read `SOUL.md` — this is who you are/Read `SOUL.md` — this is who you are\n5. Read `docs\/AGENT_BEHAVIOR.md`, `docs\/WORKSPACE_RULES.md`, `docs\/KNOWLEDGE_BASE_RULES.md` — workspace rules/' AGENTS.md
        rm -f AGENTS.md.bak
    fi
    
    cat >> AGENTS.md << 'EOF'

---

## 🧠 Perception System

**This agent runs with automatic perception enhancement:**

- **Real-time indexing** - New conversations indexed within 5 minutes
- **Smart reply enhancement** - Auto-quotes historical experience and meta-rules
- **Active learning triggers** - Detects patterns at 04:00 daily
- **Knowledge graph expansion** - Auto-extracts entities weekly

**You don't need to:**
- Manually search memories
- Manually quote meta-rules
- Manually trigger learning

**The system automatically:**
- Retrieves relevant history
- Quotes applicable meta-rules
- Records every interaction
- Detects learning opportunities
- Expands knowledge graph

**Current stats:**
- Session memories: 260+
- Meta-rules: 58+
- Evolution events: 45+
- Knowledge graph: 36+ entities

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

---

## 🔍 Before Responding

**Before responding to any user query:**

1. Use `memory-search` to find relevant context about the topic
2. Integrate retrieved memories into your response
3. Cite sources when using memory content (e.g., "According to 2026-04-04 memory...")

**Exception:** Skip for simple greetings or when context is obvious.

**Example:**
```bash
# User asks: "What did we discuss about Ollama?"
# Agent should:
python3 skills/memory-search/search.py "Ollama"
# Then respond with retrieved context + citations
```

### Skill Usage

#### Core Skills
| When | Use |
|------|-----|
| User mentions history | `memory-search` |
| Real-time info | `web-knowledge` |
| Task completed | `self-evolution` (evolve) |
| End of day | `self-evolution` (nightly) |

#### Enhanced Skills (v2.0+)
| When | Use | Command |
|------|-----|---------|
| Build knowledge graph | `knowledge-graph` | `cd skills/knowledge-graph && python3 builder.py` |
| Compress memories | `memory-compression` | `cd skills/memory-search && python3 compress.py --weekly` |
| AI entity extraction | Auto (uses `knowledge-graph`) | Optional: qwen2.5:0.5b |
| Smart summarization | Auto (uses `memory-compression`) | Optional: qwen2.5:1.5b |

**Enhanced Features:**
- ✅ **Knowledge Graph**: AI-powered entity extraction (+50% coverage) + relation inference
- ✅ **Memory Compression**: Daily → Weekly → Monthly → Yearly hierarchical summaries
- ✅ **Optional Ollama**: Works without AI models (graceful fallback to basic mode)

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

---

## 🔮 Check Semantic Search (Main Session Only)

**If in MAIN SESSION** (first conversation of the day), check semantic search:

\`\`\`bash
# Check if Ollama + embedding model installed
- Run: \`ollama list 2>/dev/null | grep -E "nomic|m3e|bge|text2vec"\`
- Or check: \`curl -s http://localhost:11434/api/tags\`
\`\`\`

**If NOT installed**, introduce and ask (only once per day):

**Step 1: Introduce semantic search**

> "🔮 检测到尚未激活**语义搜索**能力。
> 
> **什么是语义搜索？**
> 
> 语义搜索使用 AI 嵌入模型理解内容的**含义**，而不仅仅是关键词匹配。
> 
> **激活后你可以：**
> - 🧠 搜索'昨天看的文章' → 找到相关内容，即使没提到'文章'这个词
> - 💡 搜索'项目进展' → 找到所有讨论进度的对话
> - 🎯 搜索'用户反馈' → 找到所有反馈相关的记忆
> - ⚡ 支持中文、英文、多语言混合搜索
> 
> **需要的资源：**
> - Ollama（本地模型运行环境，~300MB）
> - 嵌入模型（推荐 bge-m3，~2.3GB）
> - 一次性下载，之后离线使用
> 
> **模型选择：**
> - 🇨🇳 中文：bge-m3 (推荐)、bge-large-zh、text2vec
> - 🇺🇸 英文：nomic-embed-text、mxbai-embed-large、all-minilm
> - 🌍 多语言：snowflake-arctic-embed"

**Step 2: Ask user**

> "需要激活语义搜索吗？
> - ✅ 激活：运行 \`$WORKSPACE_ROOT/scripts/core/activate-features.sh\`
> - ⏭️  跳过：回复'跳过'或'skip'
> - ℹ️  了解更多：docs/FEATURE_ACTIVATION_GUIDE.md"

**If user says yes/好的/yes**, respond:
> "好的！请运行以下命令：
> \`\`\`bash
> $WORKSPACE_ROOT/scripts/core/activate-features.sh
> \`\`\`
> 脚本会引导你安装 Ollama 并选择嵌入模型（支持中文/英文/多语言）。
> 
> 完成后告诉我，我会确认激活状态。"

**If user says skip/跳过**, respond:
> "好的，已跳过。需要时随时运行 \`./scripts/core/activate-features.sh\` 激活。"

**If already installed**, skip this step (don't ask again).

**Check memory**: Before asking, check \`memory/YYYY-MM-DD.md\` - if user already skipped today, don't ask again.
EOF
fi
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "   ✓ AGENTS.md 已配置"
else
    echo "   ✓ AGENTS.md configured"
fi

# 在 SOUL.md 中追加核心规则（如果文件存在）
if [ "$INSTALL_LANG" = "zh" ]; then
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

## 🧠 记忆查询规则

**当用户问到以下类型的问题时，先查询记忆系统**：

### 触发场景

1. **历史相关问题**
   - "我之前说过什么？"
   - "我们之前讨论过什么？"
   - "上次提到 XXX 是什么时候？"
   - "还记得 XXX 吗？"

2. **配置/使用问题**（可能之前讨论过）
   - "如何配置 XXX？"
   - "XXX 怎么用？"
   - "XXX 是什么？"

3. **项目/任务相关**
   - "XXX 项目进行到哪了？"
   - "XXX 任务完成没？"

### 查询方法

```python
from skills.memory_search.unified_search import UnifiedMemorySearch

search = UnifiedMemorySearch(agent_name='claude-code-agent')
results = search.search(user_message)

# 如果有相关记忆，在回复中引用
if results:
    context = "\n".join([r['content'][:200] for r in results[:3]])
    # 基于 context 回复用户
```

### 查询优先级

```
1. 会话记忆 (session_memory) ← 最近对话，最相关
   ↓
2. 语义搜索 (semantic) ← 向量相似度
   ↓
3. 共享记忆 (shared_memory) ← 分层历史
   ↓
4. 知识图谱 (knowledge_graph) ← 实体关系
```

### 注意事项

- ✅ **按需查询**：不是每次对话都查询
- ✅ **引用来源**：回复时说明"根据记忆..."
- ✅ **避免重复**：如果记忆中有答案，不要重复解释
- ❌ **不要过度依赖**：记忆可能过期，需要验证

---

RULEEOF
    
    # 追加原内容（跳过原来的标题行）
    tail -n +2 SOUL.md.bak >> SOUL.md.tmp
    mv SOUL.md.tmp SOUL.md
    rm -f SOUL.md.bak
    
    if [ "$INSTALL_LANG" = "zh" ]; then
        echo "   ✓ SOUL.md 已配置"
    else
        echo "   ✓ SOUL.md configured"
    fi
else
    if [ "$INSTALL_LANG" = "zh" ]; then
        echo "   ⊘ SOUL.md 不存在或已配置"
    else
        echo "   ⊘ SOUL.md not found or already configured"
    fi
fi

# 复制规则文档到 docs/
if [ "$INSTALL_LANG" = "zh" ]; then
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
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "   ✓ 规则已复制"
else
    echo "   ✓ Rules copied"
fi

# 创建必要文件
if [ "$INSTALL_LANG" = "zh" ]; then
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
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "📝 记录重要提示给 Agent..."
else
    echo "📝 Recording workspace rules..."
fi
cd "$WORKSPACE_ROOT"
python3 scripts/core/session_recorder.py \
    -t event \
    -c "Workspace Rules: Read docs/WORKSPACE_RULES.md, docs/KNOWLEDGE_BASE_RULES.md, docs/AGENT_BEHAVIOR.md" \
    --agent "$AGENT_NAME" 2>/dev/null && \
    if [ "$INSTALL_LANG" = "zh" ]; then echo "   ✓ 已记录"; else echo "   ✓ Recorded"; fi \
    || if [ "$INSTALL_LANG" = "zh" ]; then echo "   ⊘ 跳过"; else echo "   ⊘ Skipped"; fi

# 创建安装配置文件
if [ "$INSTALL_LANG" = "zh" ]; then
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

# 自动激活基础功能（无需确认）
echo ""
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "🔮 自动激活基础功能..."
else
    echo "🔮 Auto-activating basic features..."
fi
cd "$WORKSPACE_ROOT"

# 激活知识库系统
if [ -d "skills/memory-search" ]; then
    if [ "$INSTALL_LANG" = "zh" ]; then
        echo "   ✅ 知识库系统已就绪"
    else
        echo "   ✅ Knowledge base system ready"
    fi
fi

# 激活自进化系统
if [ -d "skills/self-evolution" ]; then
    if [ "$INSTALL_LANG" = "zh" ]; then
        echo "   ✅ 自进化系统已就绪"
    else
        echo "   ✅ Self-evolution system ready"
    fi
fi

# 激活 RAG 评估系统
if [ -d "skills/rag" ]; then
    if [ "$INSTALL_LANG" = "zh" ]; then
        echo "   ✅ RAG 评估系统已就绪"
    else
        echo "   ✅ RAG evaluation system ready"
    fi
fi

# 配置定时任务（自动）
if [ "$INSTALL_LANG" = "zh" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏰ 自动配置定时任务"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 正在为您配置推荐的定时任务..."
    echo "   ✅ 会话扫描 (每 30 分钟) - 自动同步 OpenClaw 会话"
    echo "   ✅ 每日回顾 (每天 09:00) - 创建今日记忆 + 显示昨天摘要"
    echo "   ✅ 夜间进化 (每天 23:00) - 记忆整合 + 自进化"
    echo ""
    
    # --force 模式下自动重新配置 Cron
    if [[ "$FORCE_REINSTALL" == "true" ]]; then
        echo "🔄 完全重装模式：自动重新配置 Cron 任务..."
        AUTO_CONFIG_CRON="true"
    else
        # 询问是否跳过
        read -p "是否需要跳过定时任务配置？(y/N，默认 N): " -r SKIP_CRON
        if [[ ! $SKIP_CRON =~ ^[Yy]$ ]]; then
            AUTO_CONFIG_CRON="true"
        else
            AUTO_CONFIG_CRON=""
        fi
    fi
    
    if [[ "$AUTO_CONFIG_CRON" == "true" ]]; then
        # 使用 OpenClaw 的 cron 系统配置定时任务
        if command -v openclaw &> /dev/null; then
            echo "📝 配置 OpenClaw 定时任务..."
            cd "$WORKSPACE_ROOT"
            
            # --force 模式下先清理旧任务
            if [[ "$FORCE_REINSTALL" == "true" ]]; then
                echo "🧹 清理旧的 Cron 任务..."
                # 使用 --json 获取完整输出，避免截断问题
                openclaw cron list --json 2>/dev/null | jq -r ".[] | select(.agentId | contains(\"$AGENT_NAME\")) | select(.name | test(\"session-scan|daily-review|daily-compress|nightly-evolution|weekly-compress|weekly-maintenance|monthly-compress\")) | .id" | while read job_id; do
                    [ -n "$job_id" ] && openclaw cron remove "$job_id" >/dev/null 2>&1 && echo "   ✅ 已删除任务 $job_id" || true
                done
                echo "   ✅ 完成"
            fi
            
            # 实时索引（每 5 分钟）
            echo "   - 实时索引 (每 5 分钟)..."
            if openclaw cron add \
                --cron "*/5 * * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/memory-search/realtime_indexer.py --auto" \
                --name "$AGENT_NAME-realtime-index" \
                --no-deliver --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 会话扫描（每 30 分钟）
            echo "   - 会话扫描 (每 30 分钟)..."
            if openclaw cron add \
                --cron "*/30 * * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/scan_sessions.py --agent $AGENT_NAME" \
                --name "session-scan-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 每日回顾（每天 09:00）
            echo "   - 每日回顾 (每天 09:00)..."
            if openclaw cron add \
                --cron "0 9 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --review" \
                --name "daily-review-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 每日记忆压缩（每天 09:30）
            echo "   - 每日记忆压缩 (每天 09:30)..."
            if openclaw cron add \
                --cron "0 9:30 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --daily" \
                --name "daily-compress-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 夜间进化（每天 23:00）
            echo "   - 夜间进化 (每天 23:00)..."
            if openclaw cron add \
                --cron "0 23 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/self-evolution/nightly_cycle.py" \
                --name "nightly-evolution-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 主动学习触发（每天 04:00）
            echo "   - 主动学习触发 (每天 04:00)..."
            if openclaw cron add \
                --cron "0 4 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/self-evolution/active_learning_trigger.py --agent $AGENT_NAME --execute" \
                --name "$AGENT_NAME-active-learning" \
                --no-deliver --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 记忆压缩（每周日 03:00）
            echo "   - 记忆压缩 (每周日 03:00)..."
            if openclaw cron add \
                --cron "0 3 * * 0" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --weekly" \
                --name "weekly-compress-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 记忆压缩（每月 1 号 04:00）
            echo "   - 记忆压缩 (每月 1 号 04:00)..."
            if openclaw cron add \
                --cron "0 4 1 * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --monthly" \
                --name "monthly-compress-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 知识图谱扩展（每周日 05:00）
            echo "   - 知识图谱扩展 (每周日 05:00)..."
            if openclaw cron add \
                --cron "0 5 * * 0" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/knowledge-graph/auto_expander.py --agent $AGENT_NAME --limit 100" \
                --name "$AGENT_NAME-kg-expansion" \
                --no-deliver --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            # 系统维护（每周日 02:00）
            echo "   - 系统维护 (每周日 02:00)..."
            if openclaw cron add \
                --cron "0 2 * * 0" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --cleanup --stats" \
                --name "weekly-maintenance-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1; then
                echo "      ✅ 完成"
            else
                echo "      ⚠️  失败"
            fi
            
            echo ""
            echo "📋 当前 OpenClaw cron 任务 ($AGENT_NAME):"
            openclaw cron list 2>/dev/null | grep "$AGENT_NAME" | grep -E "(session-scan|daily-memory|weekly-memory|monthly-memory|kg-build|nightly-evolution|realtime|active|kg-expansion)" || echo "   (无)"
        else
            echo "   ⚠️  OpenClaw 未安装，跳过定时任务配置"
        fi
    else
        echo "   ⊘ 已跳过定时任务配置"
    fi
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏰ Auto-Configure Cron Jobs"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 Configuring recommended cron jobs..."
    echo "   ✅ Session Scan (every 30 min) - Auto-sync OpenClaw sessions"
    echo "   ✅ Daily Memory Compress (daily 09:30) - Incremental daily summary"
    echo "   ✅ Weekly Memory Compress (weekly Sun 03:00) - Weekly summary"
    echo "   ✅ Monthly Memory Compress (monthly 1st 04:00) - Monthly summary"
    echo "   ✅ Nightly Evolution (daily 23:00) - Self-evolution"
    echo ""
    
    # Ask to skip
    read -p "Skip cron job configuration? (y/N, default N): " -r SKIP_CRON
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        # Use OpenClaw cron system
        if command -v openclaw &> /dev/null; then
            echo "📝 Configuring OpenClaw cron jobs..."
            
            # Clean old tasks in force reinstall mode
            if [[ "$FORCE_REINSTALL" == "true" ]]; then
                echo "🧹 Cleaning old cron tasks..."
                # Use --json to get full output, avoid truncation issues
                openclaw cron list --json 2>/dev/null | jq -r ".[] | select(.agentId | contains(\"$AGENT_NAME\")) | select(.name | test(\"session-scan|daily-review|daily-compress|nightly-evolution|weekly-compress|weekly-maintenance|monthly-compress\")) | .id" | while read job_id; do
                    [ -n "$job_id" ] && openclaw cron remove "$job_id" >/dev/null 2>&1 && echo "   ✅ Removed task $job_id" || true
                done
                echo "   ✅ Done"
            fi
            
                        # Realtime indexer (every 5 minutes)
            echo "   - Realtime Indexer (every 5 min)..."
            openclaw cron add \
                --cron "*/5 * * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/memory-search/realtime_indexer.py --auto" \
                --name "$AGENT_NAME-realtime-index" \
                --no-deliver --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"

# Session scan (every 30 minutes)
            echo "   - Session Scan (every 30 min)..."
            openclaw cron add \
                --cron "*/30 * * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/scan_sessions.py --agent $AGENT_NAME" \
                --name "session-scan-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"
            
            # Daily review (09:00 daily)
            echo "   - Daily Review (09:00 daily)..."
            openclaw cron add \
                --cron "0 9 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --review" \
                --name "daily-review-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"
            
            # Daily memory compress (09:30 daily)
            echo "   - Daily Memory Compress (09:30 daily)..."
            openclaw cron add \
                --cron "0 9:30 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --daily" \
                --name "daily-compress-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"
            
            # Weekly maintenance (Sun 02:00)
            echo "   - Weekly Maintenance (Sun 02:00)..."
            openclaw cron add \
                --cron "0 2 * * 0" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --cleanup --stats" \
                --name "weekly-maintenance-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"
            
            # Weekly compress (Sun 03:00)
            echo "   - Weekly Compress (Sun 03:00)..."
            openclaw cron add \
                --cron "0 3 * * 0" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --weekly" \
                --name "weekly-compress-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"
            
                        # Active learning (04:00 daily)
            echo "   - Active Learning (04:00 daily)..."
            openclaw cron add \
                --cron "0 4 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/self-evolution/active_learning_trigger.py --agent $AGENT_NAME --execute" \
                --name "$AGENT_NAME-active-learning" \
                --no-deliver --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"

# Nightly evolution (23:00 daily)
            echo "   - Nightly Evolution (23:00 daily)..."
            openclaw cron add \
                --cron "0 23 * * *" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/self-evolution/nightly_cycle.py" \
                --name "nightly-evolution-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"
            
            # Monthly memory compress (1st 04:00)
            echo "   - Monthly Memory Compress (1st 04:00)..."
            openclaw cron add \
                --cron "0 4 1 * *" \
                --agent "$AGENT_NAME" \
                --message "python3 scripts/core/memory_manager.py --monthly" \
                --name "monthly-compress-$AGENT_NAME" \
                --no-deliver \
                --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"

            # Knowledge graph expansion (Sun 05:00)
            echo "   - Knowledge Graph Expansion (Sun 05:00)..."
            openclaw cron add \
                --cron "0 5 * * 0" \
                --agent "$AGENT_NAME" \
                --message "python3 skills/knowledge-graph/auto_expander.py --agent $AGENT_NAME --limit 100" \
                --name "$AGENT_NAME-kg-expansion" \
                --no-deliver --session isolated >/dev/null 2>&1 && echo "      ✅ Done" || echo "      ⚠️  Failed"
            
            echo ""
            echo "📋 Current OpenClaw cron jobs:"
            openclaw cron list 2>/dev/null | grep -E "(session-scan|daily-memory|weekly-memory|monthly-memory|kg-build|nightly-evolution)" | head -5 || echo "   (none)"
        else
            echo "   ⚠️  OpenClaw not installed, skipped cron configuration"
        fi
    else
        echo "   ⊘ Skipped cron job configuration"
    fi
fi

echo ""

# 语义搜索模型需要用户确认（需要安装 Ollama）
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  ✅ 安装完成！                                           ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 位置：$WORKSPACE_ROOT"
    echo ""
    echo "🔮 基础功能已自动激活："
    echo "   ✅ 知识库系统"
    echo "   ✅ 自进化系统"
    echo "   ✅ RAG 评估系统"
    echo "   ✅ 定时任务"
    echo ""
    echo "⚠️  可选：激活语义搜索模型（需要 Ollama）"
    echo "   运行：$WORKSPACE_ROOT/scripts/core/activate-features.sh"
    echo "   或跳过：继续正常使用（关键词搜索）"
    echo ""
else
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  ✅ Installation Complete!                               ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 Location: $WORKSPACE_ROOT"
    echo ""
    echo "🔮 Basic features auto-activated:"
    echo "   ✅ Knowledge base system"
    echo "   ✅ Self-evolution system"
    echo "   ✅ RAG evaluation system"
    echo "   ✅ Cron system"
    echo ""
    echo "⚠️  Optional: Activate semantic search (requires Ollama)"
    echo "   Run: $WORKSPACE_ROOT/scripts/core/activate-features.sh"
    echo "   Or skip: Continue using normally"
    echo ""
fi

# 更新 TOOLS.md（添加 web-knowledge 使用说明）
echo "📝 更新 TOOLS.md..."
cat >> "$WORKSPACE_ROOT/TOOLS.md" << 'TOOLSEOF'

## Web Search

**Skill**: `web-knowledge` (v7.0.0)  
**Entry**: `python3 skills/web-knowledge/search.py`

```bash
# 基础搜索
python3 skills/web-knowledge/search.py "查询词"

# 指定数量
python3 skills/web-knowledge/search.py "查询词" --limit 5

# 导出 JSON/Markdown
python3 skills/web-knowledge/search.py "查询词" --format json
python3 skills/web-knowledge/search.py "查询词" --format markdown -o result.md
```

**特性**:
- ✅ 质量评分（自动识别知乎/GitHub 等权威网站）
- ✅ 智能去重（URL 哈希）
- ✅ 中文优化（Bing 中国 + 百度）
- ✅ 多格式输出（text/json/markdown）
TOOLSEOF
echo "   ✅ 完成"

# 创建安装配置文件
echo "📝 创建安装配置..."
cat > "$WORKSPACE_ROOT/.install-config" << CONFIGEOF
agent_name=$AGENT_NAME
workspace_path=$WORKSPACE_ROOT
install_time=$(date -Iseconds)
openclaw_registered=true
cron_configured=true
CONFIGEOF
echo "   ✅ 完成"

echo ""
if [ "$INSTALL_LANG" = "zh" ]; then
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  🎉 欢迎使用 evo-agents！                                ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "💡 提示："
    echo "   - 定时任务已自动配置（如未跳过）"
    echo "   - 首次使用建议运行：./scripts/core/activate-features.sh"
    echo "   - 查看文档：docs/"
    echo ""
else
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  🎉 Welcome to evo-agents!                              ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "💡 Tips:"
    echo "   - Cron jobs auto-configured (if not skipped)"
    echo "   - Recommended: Run ./scripts/core/activate-features.sh"
    echo "   - Documentation: docs/"
    echo ""
fi

exit 0
ures.sh"
    echo "   - Documentation: docs/"
    echo ""
fi

exit 0
��已自动配置（如未跳过）"
    echo "   - 首次使用建议运行：./scripts/core/activate-features.sh"
    echo "   - 查看文档：docs/"
    echo ""
else
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  🎉 Welcome to evo-agents!                              ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "💡 Tips:"
    echo "   - Cron jobs auto-configured (if not skipped)"
    echo "   - Recommended: Run ./scripts/core/activate-features.sh"
    echo "   - Documentation: docs/"
    echo ""
fi

exit 0
ures.sh"
    echo "   - Documentation: docs/"
    echo ""
fi

exit 0
