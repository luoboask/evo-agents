# evo-agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**🌐 Language:** [English](README.md) | [简体中文](README.zh-CN.md)

---

## ⚡ Quick Start

### One-line Installation

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**Done!** Full-featured agent workspace in seconds.

---

## 🎯 What is evo-agents?

**Production-ready OpenClaw agent template** with:

- 📦 **Pre-configured Skills** - Memory search, RAG, self-evolution
- 🔒 **Data Isolation** - Each agent has independent workspace
- 🛠️ **Ready Scripts** - Install, activate, cleanup
- 🧠 **Harness Agent** - 8 domain plugins for complex tasks
- 📚 **Advanced Memory** - Hierarchical compression (Day→Week→Month)

---

## ✨ Core Features

### 1. Multi-Agent Architecture

```
evo-agents/
├── agents/          # Isolated agents
├── skills/          # Shared capabilities
├── memory/          # Memory files
└── libs/            # Shared libraries
```

### 2. Harness Agent Plugins

**8 Domain Plugins:** Programming | E-commerce | Data Analysis | DevOps | Marketing | Content | Self-Media

```bash
/harness-agent "Develop a blog system" --domain programming
```

### 3. Advanced Memory System

| Level | Retention | Schedule |
|-------|-----------|----------|
| **Daily** | 14 days | 09:30 daily |
| **Weekly** | 8 weeks | Sun 03:00 |
| **Monthly** | 2 months | 1st 04:00 |

**Search:** Month → Week → Day → Full scan

---

## 📚 Documentation

- **[Quick Start](docs/QUICKSTART.md)** - 5 minute guide
- **[FAQ](docs/FAQ.md)** - Common questions
- **[Skills Guide](docs/SKILLS_GUIDE.md)** - Skill usage

---

## 🔧 Scripts

```bash
# Install
./install.sh my-agent

# Activate features
./scripts/core/activate-features.sh

# Memory management
python3 scripts/core/memory_manager.py --all
```

---

## 📊 Status

- ✅ Memory Manager (Daily/Weekly/Monthly)
- ✅ Hierarchical Search
- ✅ Incremental Compression
- ✅ Auto Cleanup

---

**License:** MIT | **Created:** 2026-04 | **Last Update:** 2026-04-10
