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

#### Q: Can I reinstall without losing data?

**A:** Yes! The install script will:
- ✅ Ask for confirmation
- ✅ Backup your workspace automatically
- ✅ Preserve personal files
- ✅ Only update template files

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s my-agent
```

#### Q: What if installation fails?

**A:** Try these steps:
1. Check your internet connection
2. Verify OpenClaw is installed: `openclaw --version`
3. Check Python version: `python3 --version` (need 3.10+)
4. Run with verbose output: `bash -x install.sh my-agent`

---

### 🤖 Agents

#### Q: How do I add a sub-agent?

**A:** Use the add-agent script:
```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/add-agent.sh assistant "My Assistant" 🤖
```

#### Q: How many sub-agents can I create?

**A:** There's no limit! You can create as many as you need.

#### Q: Do sub-agents share skills?

**A:** Yes! Sub-agents have a symlink to parent skills:
```
agents/<agent>/skills → ../../skills
```

---

### 🧠 Memory System

#### Q: Where is memory stored?

**A:** Two places:
1. **Markdown files:** `memory/YYYY-MM-DD.md`
2. **SQLite database:** `data/<agent>/memory/memory_stream.db`

They are synced automatically by bridge_sync.py.

#### Q: How do I search my memory?

**A:** Use the search script:
```bash
python3 skills/memory-search/search.py "your query"
```

#### Q: Can I export my memory?

**A:** Yes! Memory is stored in Markdown format:
```bash
cat memory/$(date +%Y-%m-%d).md
```

---

### 🔧 Troubleshooting

#### Q: Script not found?

**A:** Check the path:
```bash
# ✅ Correct
./scripts/core/add-agent.sh

# ❌ Wrong
./add-agent.sh
```

#### Q: ModuleNotFoundError?

**A:** Make sure you're in the workspace directory:
```bash
cd ~/.openclaw/workspace-my-agent
python3 scripts/core/session_recorder.py ...
```

#### Q: Permission denied?

**A:** Make scripts executable:
```bash
chmod +x scripts/core/*.sh
```

---

## 中文 {#中文}

### 📦 安装

#### Q: 如何安装 evo-agents？

**A:** 运行此命令：
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

#### Q: 重新安装会丢失数据吗？

**A:** 不会！安装脚本会：
- ✅ 询问确认
- ✅ 自动备份 workspace
- ✅ 保留个人文件
- ✅ 只更新模板文件

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s my-agent
```

#### Q: 安装失败怎么办？

**A:** 尝试以下步骤：
1. 检查网络连接
2. 验证 OpenClaw 已安装：`openclaw --version`
3. 检查 Python 版本：`python3 --version` (需要 3.10+)
4. 使用详细输出运行：`bash -x install.sh my-agent`

---

### 🤖 Agent

#### Q: 如何添加子 Agent？

**A:** 使用 add-agent 脚本：
```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/add-agent.sh assistant "我的助手" 🤖
```

#### Q: 可以创建多少个子 Agent？

**A:** 无限制！可以根据需要创建任意数量。

#### Q: 子 Agent 共享技能吗？

**A:** 是的！子 Agent 有符号链接到父 workspace 技能：
```
agents/<agent>/skills → ../../skills
```

---

### 🧠 记忆系统

#### Q: 记忆存储在哪里？

**A:** 两个地方：
1. **Markdown 文件：** `memory/YYYY-MM-DD.md`
2. **SQLite 数据库：** `data/<agent>/memory/memory_stream.db`

它们通过 bridge_sync.py 自动同步。

#### Q: 如何搜索记忆？

**A:** 使用搜索脚本：
```bash
python3 skills/memory-search/search.py "你的查询"
```

#### Q: 可以导出记忆吗？

**A:** 可以！记忆以 Markdown 格式存储：
```bash
cat memory/$(date +%Y-%m-%d).md
```

---

### 🔧 故障排除

#### Q: 找不到脚本？

**A:** 检查路径：
```bash
# ✅ 正确
./scripts/core/add-agent.sh

# ❌ 错误
./add-agent.sh
```

#### Q: ModuleNotFoundError？

**A:** 确保在 workspace 目录：
```bash
cd ~/.openclaw/workspace-my-agent
python3 scripts/core/session_recorder.py ...
```

#### Q: Permission denied？

**A:** 使脚本可执行：
```bash
chmod +x scripts/core/*.sh
```

---

## 📞 Still need help? | 还需要帮助？

- **Documentation:** [docs/README.md](README.md)
- **Issues:** https://github.com/luoboask/evo-agents/issues
- **Discussions:** https://github.com/luoboask/evo-agents/discussions
