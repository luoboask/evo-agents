# evo-agents - OpenClaw Workspace Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

**A complete Workspace template for OpenClaw with memory management and multi-agent collaboration.**

[English](./README.md) | [简体中文](./README.zh-CN.md)

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Multi-Agent** | Main agent + professional sub-agents |
| **Data Isolation** | Each agent has independent memory/ and data/ |
| **Shared Resources** | scripts/libs/skills shared across agents |
| **Bidirectional Sync** | Markdown ↔ SQLite auto-sync |
| **Semantic Search** | Ollama + bge-m3, understands semantics |
| **Concurrency Safe** | fcntl locks + SQLite WAL mode |

---

## 🚀 Quick Start

### Option 1: OpenClaw One-Click Install (Recommended) ⭐

If you have OpenClaw installed, let it read the setup guide and install for you:

```bash
# Ask OpenClaw to read workspace-setup.md and install
openclaw agent --message "Read workspace-setup.md and help me install this workspace template"
```

OpenClaw will:
1. Read `workspace-setup.md` installation guide
2. Create directory structure
3. Register the agent
4. Set up multi-agent system (optional)
5. Run tests

### Option 2: One-Click Install

```bash
# 1. Clone template
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent

# 2. Create directory structure
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent

# 3. Register OpenClaw agent
openclaw agents add my-agent --workspace "$(pwd)" --non-interactive

# 4. Test
python3 scripts/session_recorder.py -t event -c 'Hello world'
python3 scripts/unified_search.py 'hello' --agent my-agent --semantic
```

---

## 🤖 Multi-Agent Scripts

### setup-multi-agent.sh - Create Multiple Agents

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/setup-multi-agent.sh designer writer ops
# Creates: designer-agent, writer-agent, ops-agent
```

### add-agent.sh - Add Single Agent

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/add-agent.sh designer UI/UX 设计师 🎨
# Creates: designer-agent (UI/UX 设计师 🎨)
```

**Rules:**
1. Must pass role name as argument
2. Auto-generates `role-agent`
3. If already has `-agent`, won't add again

See `workspace-setup.md` for full documentation.

---

## 📁 Directory Structure

```
workspace/
├── 📄 Root Files
│   ├── AGENTS.md           # Session spec ⭐
│   ├── SOUL.md             # Agent identity
│   ├── MEMORY.md           # Long-term memory
│   ├── USER.md             # User info
│   ├── IDENTITY.md         # Identity
│   ├── TOOLS.md            # Tools config
│   └── HEARTBEAT.md        # Heartbeat check
│
├── 🔧 scripts/             # Shared scripts
│   ├── session_recorder.py     # Record events
│   ├── unified_search.py       # Unified search
│   ├── memory_indexer.py       # Build index
│   ├── memory_compressor.py    # Compression
│   ├── memory_stats.py         # Stats
│   ├── health_check.py         # Health check
│   ├── setup-multi-agent.sh    # Create multiple agents ⭐
│   ├── add-agent.sh            # Add single agent ⭐
│   └── bridge/                 # Bidirectional sync
│
├── 📚 libs/                  # Shared libraries
│   └── memory_hub/
│
├── 🎯 skills/                # Shared skills
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📝 memory/                # Memory directory
│   ├── YYYY-MM-DD.md         # Daily records
│   ├── weekly/               # Weekly summaries
│   ├── monthly/              # Monthly summaries
│   └── archive/              # Archive
│
├── 💾 data/                  # Data directory
│   ├── <agent-name>/         # Agent data
│   └── index/                # Search index
│
├── 🤖 agents/                # Multi-agent (optional)
│   └── <sub-agent>/          # Sub-agent
│
├── 🌐 public/                # Public knowledge
├── 📂 projects/              # Git repos
├── ⚙️ config/                # Config
└── 📖 docs/                  # Documentation
```

---

## 🤖 Multi-Agent Setup (Optional)

Create professional sub-agents for collaboration:

```bash
cd ~/.openclaw/workspace-my-agent

# 1. Create sub-agent directories
mkdir -p agents/analyst-agent/{memory,data}
mkdir -p agents/developer-agent/{memory,data}
mkdir -p agents/tester-agent/{memory,data}

# 2. Create config files
cat > agents/analyst-agent/AGENTS.md << 'EOF'
# AGENTS.md - analyst-agent

**Role:** Requirement Analyst
**Responsibilities:** Analyze requirements, design solutions
EOF

cat > agents/analyst-agent/config.yaml << 'EOF'
agent:
  name: analyst-agent
  role: analyst
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory
EOF

# 3. Use sub-agent
python3 scripts/session_recorder.py -t event -c 'Content' --agent analyst-agent
```

### Example Workflow

```
1️⃣  analyst-agent    Requirement Analysis
    ↓
2️⃣  developer-agent  Implementation
    ↓
3️⃣  tester-agent     Quality Testing
    ↓
4️⃣  my-agent         Summary
```

---

## 🛠️ Usage

### Record Events

```bash
# Record to agent
python3 scripts/session_recorder.py -t event -c 'Content' --agent my-agent

# Record with auto-sync
python3 scripts/session_recorder.py -t decision -c 'Decision' --agent my-agent --sync
```

### Search Memory

```bash
# Keyword search
python3 scripts/unified_search.py 'keyword' --agent my-agent

# Semantic search
python3 scripts/unified_search.py 'What did yesterday' --agent my-agent --semantic
```

### View Stats

```bash
python3 scripts/memory_stats.py --agent my-agent
```

---

## 🔧 Dependencies

### Required
- Python 3.10+
- OpenClaw

### Optional
- **jieba** - Chinese tokenization (FTS5 search)
- **Ollama** - Semantic search (bge-m3 model)

```bash
# Install jieba
pip3 install --user jieba

# Install Ollama
brew install ollama  # macOS
ollama pull bge-m3   # Chinese semantic model
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `workspace-setup.md` | ⭐ Complete installation guide |
| `docs/ARCHITECTURE_GENERIC_CN.md` | Architecture (Chinese) |
| `docs/ARCHITECTURE_GENERIC_EN.md` | Architecture (English) |
| `docs/PROJECT_STRUCTURE_GENERIC_CN.md` | Directory structure (Chinese) |
| `docs/PROJECT_STRUCTURE_GENERIC_EN.md` | Directory structure (English) |

---

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `session_recorder.py -t event -c '...'` | Record event |
| `session_recorder.py -t decision -c '...' --sync` | Record decision + sync |
| `unified_search.py 'keyword'` | Keyword search |
| `unified_search.py 'question' --semantic` | Semantic search |
| `bridge_sync.py --agent my-agent` | Bidirectional sync |
| `memory_indexer.py --incremental --embed` | Incremental index + vectors |
| `memory_compressor.py --weekly` | Weekly summary |
| `memory_stats.py --agent my-agent` | System stats |
| `health_check.py --agent my-agent` | Health check |

---

## ⏰ Scheduled Tasks

```bash
# Daily 3AM: Incremental index
openclaw cron add --name "daily-index" --cron "0 3 * * *" \
  --system-event "cd /path && python3 scripts/memory_indexer.py --incremental --embed"

# Every 6h: Bidirectional sync
openclaw cron add --name "bridge-sync" --every "6h" \
  --system-event "cd /path && python3 scripts/bridge/bridge_sync.py --agent my-agent"

# Monday 4AM: Weekly summary
openclaw cron add --name "weekly-compress" --cron "0 4 * * 1" \
  --system-event "cd /path && python3 scripts/memory_compressor.py --weekly"
```

---

## 🔄 Graceful Degradation

| Dependency | Installed | Not Installed |
|------------|-----------|---------------|
| **jieba** | FTS5 Chinese | Fallback to grep |
| **Ollama** | Semantic search | Fallback to FTS5 |
| **Neither** | grep + SQLite LIKE | Core features work |

**Minimal install: Zero dependencies** - Just Python 3.10+.

---

## 📂 Git Repos Management

```bash
# Clone to projects/
git clone https://github.com/xxx/lib.git projects/

# List
ls -1 projects/

# Delete
rm -rf projects/old-lib/
```

**Principle:** Flat structure, no categories, manual cleanup.

---

## 📄 License

MIT License

---

## 🔗 Links

- **GitHub:** https://github.com/luoboask/evo-agents
- **OpenClaw:** https://github.com/openclaw/openclaw
- **Docs:** https://docs.openclaw.ai

---

**Last Updated:** 2026-03-26
