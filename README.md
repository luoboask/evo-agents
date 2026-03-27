# evo-agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.13-green.svg)](https://github.com/openclaw/openclaw)

**🤖 Multi-Agent Workspace Template for OpenClaw**

A reusable, self-evolving agent workspace with strict data isolation, shared capabilities, and production-ready tooling.

---

## ⚡ Quick Start

**One-line installation:**

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

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

### 3. Use Memory Search

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
