# FAQ | 常见问题

[English](#english) | [中文](#中文)

---

## English {#english}

### 📦 Installation

#### Q: How do I install evo-agents?

**A:** Run this command:
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

See [QUICKSTART.md](QUICKSTART.md) for details.

---

#### Q: Can I reinstall without losing data?

**A:** Yes! The install script will:
- ✅ Ask for confirmation
- ✅ Backup your workspace automatically
- ✅ Preserve personal files (USER.md, memory/, public/, etc.)
- ✅ Only update template files

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s my-agent
```

---

#### Q: Where is my workspace located?

**A:** `~/.openclaw/workspace-<agent-name>/`

For example: `~/.openclaw/workspace-my-agent/`

---

### 🤖 Agents

#### Q: How do I add a sub-agent?

**A:** Use the add-agent script:
```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/add-agent.sh assistant "My Assistant" 🤖
```

See [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) for details.

---

#### Q: Where are sub-agents stored?

**A:** In `agents/<agent-name>/` directory.

Each sub-agent has:
- `agent/` - OpenClaw config
- `memory/` - Agent memory
- `sessions/` - Chat sessions
- `skills/` - Symlink to parent skills

---

#### Q: Do sub-agents share skills?

**A:** Yes! Sub-agents have a symlink:
```bash
agents/<agent-name>/skills → ../../skills
```

This means:
- ✅ All agents share the same skills
- ✅ Update parent skills, all agents benefit
- ✅ No duplicate storage

---

### 📁 Workspace Rules

#### Q: Where should I create scripts?

**A:** In `scripts/` directory:
```bash
cd scripts/
cat > my-tool.sh
```

**Don't** create scripts in root directory.

---

#### Q: Where should I clone git projects?

**A:** Use one of these:
```bash
# Temporary work
cd /tmp/
git clone https://github.com/xxx/project.git

# Long-term projects
cd ~/projects/
git clone https://github.com/xxx/project.git

# Agent-specific work
cd data/my-agent/work/
git clone https://github.com/xxx/project.git
```

**Don't** clone in workspace root!

---

#### Q: Where should I store permanent data?

**A:** In `data/<agent>/` root directory:
```bash
cd data/my-agent/
mkdir config/  # Permanent config
```

**Don't** store permanent data in `work/` directory (it may be cleaned).

---

#### Q: What does cleanup.sh do?

**A:** It cleans build artifacts:
- ✅ `node_modules/`
- ✅ `__pycache__/`
- ✅ `*.log`, `*.tmp`, `*.pyc`
- ❌ Does NOT clean `work/` directories (you decide)

Run it with:
```bash
./scripts/core/cleanup.sh
```

---

### 🧠 Memory System

#### Q: How do I record sessions?

**A:** Use session_recorder.py:
```bash
python3 scripts/core/session_recorder.py -t event -c "Content" --agent my-agent
```

---

#### Q: How do I sync memory?

**A:** Use bridge_sync.py:
```bash
python3 scripts/core/bridge/bridge_sync.py --agent my-agent
```

This syncs between:
- Markdown files (`memory/`)
- SQLite database (`data/<agent>/`)

---

#### Q: Where is memory stored?

**A:** Two places:
1. **Markdown files:** `memory/YYYY-MM-DD.md`
2. **SQLite database:** `data/<agent>/knowledge_base.db`

They are synced automatically.

---

### 🔧 Scripts

#### Q: What scripts are available?

**A:** See [SCRIPTS_INVENTORY.md](SCRIPTS_INVENTORY.md) for full list.

Core scripts:
- `activate-features.sh` - Activate features
- `add-agent.sh` - Add agent
- `setup-multi-agent.sh` - Add multiple agents
- `cleanup.sh` - Clean workspace
- `session_recorder.py` - Record sessions

---

#### Q: Can I create my own scripts?

**A:** Yes! Put them in `scripts/` root:
```bash
scripts/
├── core/              # System scripts (updated)
├── my-tool.sh         # Your script (preserved) ✅
└── custom-tool.py     # Your script (preserved) ✅
```

---

### 🆘 Troubleshooting

#### Q: Script not found?

**A:** Check the path:
```bash
# ✅ Correct
./scripts/core/add-agent.sh

# ❌ Wrong
./add-agent.sh  # Not in root!
```

---

#### Q: Agent not working?

**A:** Check:
1. Agent is registered: `openclaw agents list`
2. Config exists: `ls agents/<agent>/agent/`
3. Workspace path is correct

---

#### Q: Workspace is messy?

**A:** Run cleanup:
```bash
./scripts/core/cleanup.sh
```

And manually check:
```bash
ls data/*/work/
ls agents/*/data/*/work/
```

---

## 中文 {#中文}

### 📦 安装

#### Q: 如何安装 evo-agents？

**A:** 运行此命令：
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

详见 [QUICKSTART.md](QUICKSTART.md)。

---

#### Q: 重新安装会丢失数据吗？

**A:** 不会！安装脚本会：
- ✅ 询问确认
- ✅ 自动备份 workspace
- ✅ 保留个人文件（USER.md, memory/, public/ 等）
- ✅ 只更新模板文件

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s my-agent
```

---

#### Q: workspace 在哪里？

**A:** `~/.openclaw/workspace-<agent-name>/`

例如：`~/.openclaw/workspace-my-agent/`

---

### 🤖 Agent

#### Q: 如何添加子 Agent？

**A:** 使用 add-agent 脚本：
```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/add-agent.sh assistant "我的助手" 🤖
```

详见 [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md)。

---

#### Q: 子 Agent 存储在哪里？

**A:** 在 `agents/<agent-name>/` 目录。

每个子 Agent 有：
- `agent/` - OpenClaw 配置
- `memory/` - Agent 记忆
- `sessions/` - 聊天会话
- `skills/` - 符号链接到父 skills

---

#### Q: 子 Agent 共享技能吗？

**A:** 是的！子 Agent 有符号链接：
```bash
agents/<agent-name>/skills → ../../skills
```

这意味着：
- ✅ 所有 Agent 共享同一套技能
- ✅ 更新父 workspace 技能，所有 Agent 受益
- ✅ 不占用额外空间

---

### 📁 Workspace 规则

#### Q: 应该在哪里创建脚本？

**A:** 在 `scripts/` 目录：
```bash
cd scripts/
cat > my-tool.sh
```

**不要**在根目录创建脚本。

---

#### Q: 应该在哪里克隆 git 项目？

**A:** 使用以下之一：
```bash
# 临时工作
cd /tmp/
git clone https://github.com/xxx/project.git

# 长期项目
cd ~/projects/
git clone https://github.com/xxx/project.git

# Agent 特定工作
cd data/my-agent/work/
git clone https://github.com/xxx/project.git
```

**不要**在 workspace 根目录克隆！

---

#### Q: 应该在哪里存储永久数据？

**A:** 在 `data/<agent>/` 根目录：
```bash
cd data/my-agent/
mkdir config/  # 永久配置
```

**不要**在 `work/` 目录存储永久数据（可能会被清理）。

---

#### Q: cleanup.sh 做什么？

**A:** 清理构建产物：
- ✅ `node_modules/`
- ✅ `__pycache__/`
- ✅ `*.log`, `*.tmp`, `*.pyc`
- ❌ 不清理 `work/` 目录（你自己决定）

运行：
```bash
./scripts/core/cleanup.sh
```

---

### 🧠 记忆系统

#### Q: 如何记录会话？

**A:** 使用 session_recorder.py：
```bash
python3 scripts/core/session_recorder.py -t event -c "内容" --agent my-agent
```

---

#### Q: 如何同步记忆？

**A:** 使用 bridge_sync.py：
```bash
python3 scripts/core/bridge/bridge_sync.py --agent my-agent
```

这会在以下之间同步：
- Markdown 文件（`memory/`）
- SQLite 数据库（`data/<agent>/`）

---

#### Q: 记忆存储在哪里？

**A:** 两个地方：
1. **Markdown 文件：** `memory/YYYY-MM-DD.md`
2. **SQLite 数据库：** `data/<agent>/knowledge_base.db`

它们自动同步。

---

### 🔧 脚本

#### Q: 有哪些脚本可用？

**A:** 详见 [SCRIPTS_INVENTORY.md](SCRIPTS_INVENTORY.md)。

核心脚本：
- `activate-features.sh` - 激活功能
- `add-agent.sh` - 添加 Agent
- `setup-multi-agent.sh` - 批量添加 Agent
- `cleanup.sh` - 清理 workspace
- `session_recorder.py` - 记录会话

---

#### Q: 可以创建自己的脚本吗？

**A:** 可以！放在 `scripts/` 根目录：
```bash
scripts/
├── core/              # 系统脚本（更新）
├── my-tool.sh         # 你的脚本（保留）✅
└── custom-tool.py     # 你的脚本（保留）✅
```

---

### 🆘 故障排除

#### Q: 找不到脚本？

**A:** 检查路径：
```bash
# ✅ 正确
./scripts/core/add-agent.sh

# ❌ 错误
./add-agent.sh  # 不在根目录！
```

---

#### Q: Agent 不工作？

**A:** 检查：
1. Agent 已注册：`openclaw agents list`
2. 配置存在：`ls agents/<agent>/agent/`
3. workspace 路径正确

---

#### Q: workspace 太乱？

**A:** 运行清理：
```bash
./scripts/core/cleanup.sh
```

并手动检查：
```bash
ls data/*/work/
ls agents/*/data/*/work/
```

---

## 📞 Still need help? | 还需要帮助？

- **Documentation:** [docs/README.md](README.md)
- **Installation:** [workspace-setup.md](../workspace-setup.md)
- **Migration:** [MIGRATION.md](MIGRATION.md)
- **GitHub Issues:** https://github.com/luoboask/evo-agents/issues

---

**Last updated:** 2026-03-27  
**最后更新：** 2026-03-27
