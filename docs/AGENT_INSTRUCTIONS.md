# Agent Instructions | Agent 指令

[English](#english) | [中文](#中文)

---

## English {#english}

### 🎯 Your Role

You are an AI assistant working in this workspace. Follow these rules to keep the workspace clean and organized.

---

### 📋 Quick Rules | 快速规则

**✅ Always Do:**
- Scripts → `scripts/` directory
- Git projects → `/tmp/` or `~/projects/` or `data/<agent>/work/`
- Move temp files to `archive/` after tasks
- Search memory before answering about prior work
- Only load MEMORY.md in main sessions
- Name temp files with prefix: `temp_`, `tmp_`

**❌ Never Do:**
- Don't clone git in workspace root
- Don't create projects in root
- Don't delete temp files without user confirmation
- Don't share private info in group chats
- Don't use vague names like `test.txt`, `data.json`

**Full rules:** [WORKSPACE_RULES.md](WORKSPACE_RULES.md)

---

### 📁 Directory Usage

| Directory | Purpose | Can I use? |
|-----------|---------|------------|
| `scripts/` | Scripts only | ✅ Yes - for your scripts |
| `skills/` | Skills only | ✅ Yes - for your skills |
| `data/<agent>/work/` | Temporary work | ✅ Yes - for agent work |
| `docs/` | Rule documents | ✅ Yes - READ THESE |
| `memory/` | Memory files | ❌ No - system use only |
| `public/` | Knowledge base | ❌ No - system use only |
| Root `/` | Workspace root | ❌ No - keep clean |

**External directories:**
- `/tmp/` - Temporary work ✅
- `~/projects/` - Long-term projects ✅

---

### 🛠️ Common Tasks

#### Creating Scripts

```bash
# ✅ Correct
cd scripts/
cat > my-tool.sh
chmod +x my-tool.sh

# ❌ Wrong
cd ..
cat > my-tool.sh  # Don't create in root!
```

#### Git Projects

```bash
# ✅ Correct - Temporary
cd /tmp/
git clone https://github.com/xxx/project.git
# Work here, then delete when done

# ✅ Correct - Long-term
cd ~/projects/
git clone https://github.com/xxx/project.git
# Keep here

# ✅ Correct - Agent-specific
cd data/my-agent/work/
git clone https://github.com/xxx/project.git
# Clean up when done

# ❌ Wrong
cd ~/workspace
git clone ...  # Don't clone in workspace root!
```

---

### 🧠 Memory Rules

**Before answering about prior work:**
1. Search memory first
2. Only load MEMORY.md in main sessions
3. Write important things to files

```python
# ✅ Correct
results = memory.search("query")

# ❌ Wrong
# Answering without searching memory
```

---

### 🤖 Sub-Agent Rules

**When spawning sub-agents:**
- They inherit the same rules
- They cannot access MEMORY.md
- Pass private info via task parameter
- They don't execute cron/heartbeat tasks

---

### 📚 Rule Documents

**Read these documents:**

| Document | Purpose |
|----------|---------|
| [AGENT_BEHAVIOR.md](AGENT_BEHAVIOR.md) | Core behavior rules |
| [SKILL_RULES.md](SKILL_RULES.md) | When to use which skill |
| [WORKSPACE_RULES.md](WORKSPACE_RULES.md) | Workspace organization |
| [KNOWLEDGE_BASE_RULES.md](KNOWLEDGE_BASE_RULES.md) | Knowledge base management |
| [SUBAGENT_RULES.md](SUBAGENT_RULES.md) | Sub-agent rules |
| [SCHEDULER.md](SCHEDULER.md) | Scheduled tasks |

---

## 中文 {#中文}

### 🎯 你的角色

你是工作在这个 workspace 的 AI 助手。遵守这些规则保持 workspace 整洁有序。

---

### 📋 快速规则

**✅ 始终要做：**
- 脚本 → `scripts/` 目录
- Git 项目 → `/tmp/` 或 `~/projects/` 或 `data/<agent>/work/`
- 完成任务后清理
- 回答历史问题前先搜索记忆
- 只在主会话加载 MEMORY.md

**❌ 绝对不要：**
- 不要在 workspace 根目录 clone git
- 不要在根目录创建项目
- 不要在根目录遗留临时文件
- 不要在群聊中分享私人信息
- 不要未经用户确认删除文件

**完整规则：** [WORKSPACE_RULES.md](WORKSPACE_RULES.md)

---

### 📁 目录使用

| 目录 | 用途 | 可以使用？ |
|------|------|-----------|
| `scripts/` | 仅脚本 | ✅ 是 - 放你的脚本 |
| `skills/` | 仅技能 | ✅ 是 - 放你的技能 |
| `data/<agent>/work/` | 临时工作 | ✅ 是 - Agent 工作 |
| `docs/` | 规则文档 | ✅ 是 - 阅读这些 |
| `memory/` | 记忆文件 | ❌ 否 - 系统专用 |
| `public/` | 知识库 | ❌ 否 - 系统专用 |
| 根目录 `/` | Workspace 根 | ❌ 否 - 保持整洁 |

**外部目录：**
- `/tmp/` - 临时工作 ✅
- `~/projects/` - 长期项目 ✅

---

### 🛠️ 常见任务

#### 创建脚本

```bash
# ✅ 正确
cd scripts/
cat > my-tool.sh
chmod +x my-tool.sh

# ❌ 错误
cd ..
cat > my-tool.sh  # 不要在根目录创建！
```

#### Git 项目

```bash
# ✅ 正确 - 临时
cd /tmp/
git clone https://github.com/xxx/project.git
# 在这里工作，完成后删除

# ✅ 正确 - 长期
cd ~/projects/
git clone https://github.com/xxx/project.git
# 保留在这里

# ✅ 正确 - Agent 专用
cd data/my-agent/work/
git clone https://github.com/xxx/project.git
# 完成后清理

# ❌ 错误
cd ~/workspace
git clone ...  # 不要在 workspace 根目录 clone！
```

---

### 🧠 记忆规则

**回答历史问题前：**
1. 先搜索记忆
2. 只在主会话加载 MEMORY.md
3. 重要的事写文件

```python
# ✅ 正确
results = memory.search("query")

# ❌ 错误
# 不搜索记忆直接回答
```

---

### 🤖 子 Agent 规则

**Spawn 子 Agent 时：**
- 他们继承同样的规则
- 不能访问 MEMORY.md
- 通过 task 参数传递私人信息
- 不执行 cron/heartbeat 任务

---

### 📚 规则文档

**阅读这些文档：**

| 文档 | 作用 |
|------|------|
| [AGENT_BEHAVIOR.md](AGENT_BEHAVIOR.md) | 核心行为规范 |
| [SKILL_RULES.md](SKILL_RULES.md) | 技能使用规则 |
| [WORKSPACE_RULES.md](WORKSPACE_RULES.md) | Workspace 规范 |
| [KNOWLEDGE_BASE_RULES.md](KNOWLEDGE_BASE_RULES.md) | 知识库管理 |
| [SUBAGENT_RULES.md](SUBAGENT_RULES.md) | 子 Agent 规则 |
| [SCHEDULER.md](SCHEDULER.md) | 定时任务 |

---

_版本：2.0.0 | 更新：2026-04-01_
