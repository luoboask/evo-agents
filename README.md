# evo-agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.13-green.svg)](https://github.com/openclaw/openclaw)

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

**Production-ready OpenClaw agent template** with advanced memory management and domain-specific plugins.

---

## 🏗️ Architecture

### Overall Structure

```
evo-agents/
├── agents/                    # Isolated agent instances
│   ├── main-agent/
│   ├── sandbox-agent/
│   └── tao-admin/
│
├── skills/                    # Shared skills
│   ├── memory-search/        # Memory management
│   ├── harness-agent/        # Domain plugins
│   ├── self-evolution/       # Self-improvement
│   └── web-knowledge/        # Web search
│
├── memory/                    # Memory files
│   ├── YYYY-MM-DD.md         # Daily memories
│   ├── weekly/               # Week summaries
│   ├── monthly/              # Month summaries
│   └── MEMORY.md             # Long-term memory
│
├── libs/                      # Shared libraries
│   ├── memory_hub/           # Memory storage (SQLite)
│   ├── rag_eval/             # RAG evaluation
│   └── knowledge_graph/      # Knowledge graph
│
└── scripts/                   # Utility scripts
    ├── core/
    │   ├── memory_manager.py # Memory compression
    │   ├── scan_sessions.py  # Session scanner
    │   └── ...
    └── ...
```

---

## 📚 Memory Architecture

### Hierarchical Memory System

```
┌─────────────────────────────────────────────────────────┐
│                    User Query                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Search Strategy                             │
│  Month → Week → Day → Full Scan                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Memory Layers                               │
├─────────────────────────────────────────────────────────┤
│  Month Summary (2 months)    → Overview                 │
│  Week Summary  (8 weeks)     → Summary                  │
│  Day Summary   (14 days)     → Details                  │
│  MEMORY.md   (Permanent)     → Long-term                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Storage                                     │
├─────────────────────────────────────────────────────────┤
│  memory/monthly/*.md        (Month summaries)           │
│  memory/weekly/*.md         (Week summaries)            │
│  memory/YYYY-MM-DD.md       (Daily memories)            │
│  data/*/memory/memory_stream.db  (Shared memory)        │
└─────────────────────────────────────────────────────────┘
```

### Memory Compression Flow

```
Daily Memory (memory/YYYY-MM-DD.md)
         ↓ (Daily 09:30)
   Incremental Compress
         ↓
   Shared Memory (memory_hub)
         ↓ (Weekly Sun 03:00)
   Week Summary (memory/weekly/)
         ↓ (Monthly 1st 04:00)
   Month Summary (memory/monthly/)
         ↓
   Auto Cleanup (14d/8w/2m)
```

### Compression Schedule

| Type | Schedule | Retention | Auto Cleanup |
|------|----------|-----------|--------------|
| **Daily** | 09:30 daily | 14 days | ✅ Yes |
| **Weekly** | Sun 03:00 | 8 weeks | ✅ Yes |
| **Monthly** | 1st 04:00 | 2 months | ✅ Yes |

---

## 🧠 Knowledge Architecture

### Knowledge Graph Integration

```
┌─────────────────────────────────────────────────────────┐
│              Knowledge Sources                           │
├─────────────────────────────────────────────────────────┤
│  memory/           Markdown files                       │
│  MEMORY.md         Long-term memory                     │
│  Web Search        Real-time information                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│           Knowledge Processing                           │
├─────────────────────────────────────────────────────────┤
│  Extract Entities    →    Build Relationships           │
│  (Ollama/NLP)             (Graph DB)                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Knowledge Graph                             │
├─────────────────────────────────────────────────────────┤
│  Entities: User, Project, Technology, Decision          │
│  Relations: USES, PREFERS, DECIDES, WORKS_ON           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Query & Reasoning                           │
├─────────────────────────────────────────────────────────┤
│  SPARQL Queries    →    Inference                       │
│  Entity Search     →    Relationship Discovery          │
└─────────────────────────────────────────────────────────┘
```

### RAG Pipeline

```
User Question
     ↓
┌─────────────────────────────────────┐
│  1. Query Understanding             │
│     - Intent classification         │
│     - Entity extraction             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Multi-Source Retrieval          │
├─────────────────────────────────────┤
│  Vector Search   Knowledge Graph    │
│  (Semantic)      (Structured)       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. LLM Generation                  │
│     Context-aware answer            │
└─────────────────────────────────────┘
```

---

## ✨ Core Features

### 1. Multi-Agent Architecture

- 🔒 **Data Isolation** - Each agent has independent workspace and database
- 📦 **Shared Skills** - Common capabilities across all agents
- 🛠️ **Easy Setup** - One-line installation

### 2. Harness Agent Plugins

**8 Domain Plugins:**

| Domain | Use Case | Example |
|--------|----------|---------|
| **Programming** 💻 | Software development | `--domain programming` |
| **E-commerce** 🛒 | Product management | `--domain ecommerce` |
| **Data Analysis** 📊 | BI & Visualization | `--domain data_analysis` |
| **DevOps** 🔧 | CI/CD & Deployment | `--domain devops` |
| **Marketing** 📢 | Campaigns | `--domain marketing` |
| **Content** ✍️ | Articles & Scripts | `--domain content_creation` |
| **Self-Media** 📱 | Social media ops | `--domain self_media` |

### 3. Advanced Memory System

- 📅 **Hierarchical Compression** - Day → Week → Month
- 🔍 **Layered Search** - Month → Week → Day → Full
- 🗑️ **Auto Cleanup** - 14d/8w/2m retention
- 💾 **Shared Storage** - SQLite memory_hub

### 4. Self-Evolution

- 📊 **RAG Evaluation** - Track retrieval quality
- 🔧 **Auto Tuning** - Optimize parameters
- 📈 **Continuous Improvement** - Learn from interactions

---

## 🔧 Usage

### Installation

```bash
# Install
./install.sh my-agent

# Activate features
./scripts/core/activate-features.sh
```

### Memory Management

```bash
# Daily compression
python3 scripts/core/memory_manager.py --daily

# Weekly compression
python3 scripts/core/memory_manager.py --weekly

# Monthly compression
python3 scripts/core/memory_manager.py --monthly

# Search memory
python3 scripts/core/memory_manager.py --search "keyword"
```

### Cron Jobs (Auto-configured)

```
*/30 * * * *   Session scan
0 9:30 * * *   Daily memory compress
0 3 * * 0      Weekly memory compress
0 4 1 * *      Monthly memory compress
0 23 * * *     Nightly evolution
```

---

## 📚 Documentation

- **[Quick Start](docs/QUICKSTART.md)** - 5 minute guide
- **[FAQ](docs/FAQ.md)** - Common questions
- **[Skills Guide](docs/SKILLS_GUIDE.md)** - Skill usage
- **[Memory System](docs/MEMORY_SYSTEMS_COMPARISON.md)** - Memory architecture

---

## 📊 Status

- ✅ Memory Manager (Daily/Weekly/Monthly)
- ✅ Hierarchical Search
- ✅ Incremental Compression
- ✅ Auto Cleanup
- ✅ Knowledge Graph
- ✅ RAG Evaluation

---

**License:** MIT | **Created:** 2026-04 | **Last Update:** 2026-04-10
