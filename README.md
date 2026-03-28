# evo-agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.13-green.svg)](https://github.com/openclaw/openclaw)

**🌐 Language:** [English](README.md) | [简体中文](README.zh-CN.md)

**🤖 Multi-Agent Workspace Template for OpenClaw**

A reusable, self-evolving agent workspace with strict data isolation, shared capabilities, and production-ready tooling.

---

## ⚡ Quick Start

### One-line Installation

**Global:**
```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**China (Faster):**
```bash
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s my-agent
```

**中文说明：**
- 🌏 海外用户：使用 GitHub 源
- 🇨🇳 国内用户：使用 Gitee 源（快 50 倍）
- ⚡ 安装脚本会自动选择最快的源

**That's it!** You'll have a fully functional agent workspace in seconds.

---

## 🎯 What is evo-agents?

evo-agents is a **production-ready template** for creating isolated OpenClaw agents with:

- 📦 **Pre-configured skills** - Memory search, RAG, self-evolution, web knowledge
- 🔒 **Data isolation** - Each agent has its own workspace, memory, and config
- 🛠️ **Ready-to-use scripts** - Install, activate, cleanup, uninstall
- 📚 **Complete documentation** - Installation, usage, migration guides
- 🧪 **Tested workflows** - Backup, restore, multi-agent setup

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Semantic Search** | Ollama-powered vector search with embedding cache |
| 📚 **Knowledge Base** | SQLite + Markdown dual storage with auto-sync |
| 🧬 **Self-Evolution** | Fractal thinking + nightly reflection cycles |
| 📊 **RAG Evaluation** | Auto-evaluation + auto-tuning |
| 🌐 **Web Knowledge** | Multi-engine search + page crawling |
| 🤖 **Multi-Agent** | Create and manage multiple isolated agents |

---

## 📦 Installation

### New Installation

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

### Update Existing

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

### Interactive Mode

```bash
curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh
bash install.sh my-agent
```

### Force Install

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent --force
```

---

## 🚀 Usage

### 1. Activate Features

After installation, activate advanced features:

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/activate-features.sh
```

### 2. Create Sub-Agents

```bash
./scripts/core/add-agent.sh assistant "My Assistant" 🤖
./scripts/core/setup-multi-agent.sh researcher writer editor
```

### 3. Uninstall Agent

**Uninstall entire workspace:**

```bash
# Interactive (recommended)
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-workspace.sh

# Or specify agent name
./scripts/core/uninstall-workspace.sh my-agent
```

**What it does:**
1. ⚠️  Asks for confirmation (type agent name)
2. 📝  Unregisters from OpenClaw (`openclaw agents delete --force`)
3. 🗑️  Deletes workspace directory
4. 💾  Optional backup before deletion

**Uninstall sub-agent:**

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-agent.sh assistant-agent
```

**⚠️  Warnings:**
- Backup your data first: `cp -r ~/.openclaw/workspace-my-agent /tmp/backup`
- Uninstall is permanent (workspace goes to trash, but OpenClaw config is deleted)
- Sub-agents inside workspace won't be auto-uninstalled

### 4. Self-Check & Auto-Repair

**Check workspace health:**

```bash
cd ~/.openclaw/workspace-my-agent
python3 scripts/core/self_check.py
```

**Auto-fix issues:**

```bash
# Preview fixes
python3 scripts/core/self_check.py --dry-run

# Apply fixes
python3 scripts/core/self_check.py --fix
```

**What it checks:**
- ✅ Directory structure integrity
- ✅ Critical files existence
- ✅ Runtime data (forbidden directories)
- ✅ Git configuration
- ✅ OpenClaw registration
- ✅ Path system functionality
- ✅ Skills completeness
- ✅ Database health

**What it can auto-fix:**
- 🔧 Create missing directories (with .gitkeep)
- 🔧 Delete forbidden directories (scripts/data, scripts/memory)
- 🔧 Clean data/ directory
- 🔧 Rebuild index database

---

### 5. Use Memory Search

```bash
python3 skills/memory-search/search.py "your query"
```

### 4. Record Sessions

```bash
python3 scripts/core/session_recorder.py -t event -c "Your content" --agent my-agent
```

---

## 📁 Project Structure

```
~/.openclaw/workspace-my-agent/
├── scripts/           # Shared scripts
│   └── core/          # Core utilities
├── skills/            # Skills (4 universal + your custom)
│   ├── memory-search/ # Semantic search
│   ├── rag/           # RAG evaluation
│   ├── self-evolution/# Self-evolution
│   └── web-knowledge/ # Web search + crawl
├── memory/            # Daily memory files
├── data/              # Agent-specific data
└── docs/              # Documentation
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[Installation](workspace-setup.md)** | Complete installation guide |
| **[Migration](docs/MIGRATION.md)** | Update from old versions |
| **[Features](FEATURE_ACTIVATION_GUIDE.md)** | Activate advanced features |
| **[Structure](docs/STRUCTURE_RULES.md)** | Project structure rules |
| **[Workspace](docs/WORKSPACE_RULES.md)** | Workspace usage rules |
| **[Agent](docs/AGENT_INSTRUCTIONS.md)** | Agent instructions |
| **[FAQ](docs/FAQ.md)** | Frequently asked questions |
| **[Performance](docs/PERFORMANCE_OPTIMIZATION_PLAN.md)** | Performance optimization |

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Start

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

### Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## 🐛 Issues

Found a bug or have a feature request?

- 🐛 [Report a bug](https://github.com/luoboask/evo-agents/issues/new?template=bug_report.md)
- 💡 [Request a feature](https://github.com/luoboask/evo-agents/issues/new?template=feature_request.md)
- ❓ [Ask a question](https://github.com/luoboask/evo-agents/discussions)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenClaw](https://github.com/openclaw/openclaw) - The agent framework
- [Ollama](https://ollama.com/) - Local LLM and embeddings
- [SQLite](https://www.sqlite.org/) - Lightweight database

---

## 📬 Contact

- 🌐 Website: https://github.com/luoboask/evo-agents
- 📧 Email: [Your email]
- 💬 Discord: [Your Discord]

---

**Made with ❤️ by the evo-agents team**

---

## 🔧 重装/修复

如果 skills 有问题或需要更新：

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/reinstall.sh
```

**选项：**
1. 🔧 仅修复 skills（推荐）- 更新并修复硬编码
2. 🔄 完全重装（保留数据）- 重新拉取代码，保留记忆数据
3. 🗑️ 完全重置（删除所有数据）- 清空所有数据（带备份）
