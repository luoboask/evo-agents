# Quick Start | 快速入门

[English](#english) | [中文](#中文)

---

## English {#english}

### ⏱️ 5-Minute Quick Start

**Get evo-agents running in 5 minutes!**

---

### Step 1: Install (2 min)

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**That's it!** The script will:
- ✅ Clone evo-agents template
- ✅ Register agent to OpenClaw
- ✅ Create directory structure
- ✅ Run tests

---

### Step 2: Add Your First Sub-Agent (1 min)

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/add-agent.sh assistant "My Assistant" 🤖
```

**Created:** `agents/assistant-agent/`

---

### Step 3: Run Your First Task (2 min)

```bash
# Record a session
python3 scripts/core/session_recorder.py -t event -c "Hello from my first task!" --agent my-agent

# Or use OpenClaw CLI
openclaw agent --agent my-agent --message "What can you do?"
```

---

### ✅ You're Ready!

**Next steps:**
- Read [AGENT_INSTRUCTIONS.md](docs/AGENT_INSTRUCTIONS.md) for agent rules
- Read [WORKSPACE_RULES.md](docs/WORKSPACE_RULES.md) for workspace usage
- Read [workspace-setup.md](workspace-setup.md) for complete guide

---

## 中文 {#中文}

### ⏱️ 5 分钟快速入门

**5 分钟让 evo-agents 运行起来！**

---

### 第 1 步：安装（2 分钟）

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**就这么简单！** 脚本会自动：
- ✅ 克隆 evo-agents 模板
- ✅ 注册 agent 到 OpenClaw
- ✅ 创建目录结构
- ✅ 运行测试

---

### 第 2 步：添加第一个子 Agent（1 分钟）

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/add-agent.sh assistant "我的助手" 🤖
```

**创建：** `agents/assistant-agent/`

---

### 第 3 步：运行第一个任务（2 分钟）

```bash
# 记录会话
python3 scripts/core/session_recorder.py -t event -c "我的第一个任务！" --agent my-agent

# 或使用 OpenClaw CLI
openclaw agent --agent my-agent --message "你能做什么？"
```

---

### ✅ 完成！

**下一步：**
- 阅读 [AGENT_INSTRUCTIONS.md](docs/AGENT_INSTRUCTIONS.md) 了解 Agent 规则
- 阅读 [WORKSPACE_RULES.md](docs/WORKSPACE_RULES.md) 了解 workspace 使用
- 阅读 [workspace-setup.md](workspace-setup.md) 完整指南

---

## 📋 Command Reference | 命令参考

| Command | Description |
|---------|-------------|
| `./scripts/core/add-agent.sh <name>` | Add sub-agent |
| `./scripts/core/setup-multi-agent.sh <name1> <name2>` | Add multiple agents |
| `./scripts/core/cleanup.sh` | Clean workspace |
| `./scripts/core/activate-features.sh` | Activate features |

---

## 🆘 Need Help?

- **Full documentation:** [docs/README.md](docs/README.md)
- **Installation guide:** [workspace-setup.md](workspace-setup.md)
- **Migration guide:** [docs/MIGRATION.md](docs/MIGRATION.md)

---

**Happy coding! 🚀**
