# Unified Memory System for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

[English](./README.md) | [简体中文](./README.zh-CN.md)

> **Give your OpenClaw agent real memory.**
>
> Markdown as primary source. SQLite as search index. Bidirectional sync. Semantic search. Zero external API keys required.

**⚠️ This is a Workspace Template, not a Skill.** For SubAgent/Skill installation, use [unified-memory-skill](https://github.com/luoboask/unified-memory-skill) instead.

**Unified Memory System** bridges OpenClaw's native Markdown memory with a high-performance SQLite backend, enabling semantic search, automatic compression, and concurrent-safe multi-session operation — all running locally with Ollama.

## 🚀 Installation

### Option 1: One-Click Install (Recommended)

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/test-agents/init-agent.sh | bash -s my-agent
```

This will:
1. Clone the template to `~/.openclaw/workspace-my-agent`
2. Create directory structure
3. Register the agent with OpenClaw
4. Run a quick test

### Option 2: Manual Install

```bash
# 1. Clone the template
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent

# 2. Create directory structure
cd ~/.openclaw/workspace-my-agent
mkdir -p memory/weekly memory/monthly memory/archive data/index

# 3. Register with OpenClaw
openclaw agents add my-agent --workspace $(pwd) --non-interactive

# 4. Test
python3 scripts/session_recorder.py -t event -c 'Hello world'
python3 scripts/unified_search.py 'hello' --agent my-agent --semantic
```

## ❌ Not for SubAgent/Skill Use

This repository is a **complete Workspace Template** that includes:
- Agent lifecycle files (AGENTS.md, SOUL.md, MEMORY.md, USER.md)
- Multiple integrated skills (self-evolution, rag, websearch)
- Full directory structure for agent runtime

**For SubAgent or Skill-only installation**, use the lightweight skill repository instead:

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/luoboask/unified-memory-skill.git unified-memory
```

See [unified-memory-skill](https://github.com/luoboask/unified-memory-skill) for SubAgent/Skill usage.

## ✨ Why This?

| Feature | Description |
|---------|-------------|
| **Bidirectional Bridge** | Auto-sync Markdown ↔ SQLite, consistent data on both sides |
| **Semantic Search** | Natural language queries, bge-m3 understands semantics (local Ollama, no API key needed) |
| **FTS5 Chinese** | jieba tokenization, precise Chinese keyword matching |
| **Smart Scoring** | Auto-importance (decisions 8+, learnings 6+, events 5) |
| **Auto Compression** | Daily → Weekly → Monthly → Long-term, prevents data bloat |
| **Concurrency Safe** | fcntl locks + SQLite WAL, no data loss in multi-session |

## 📁 Directory Structure

```
workspace/
├── MEMORY.md                    # Long-term core memory (LLM reads every session)
├── memory/
│   ├── 2026-03-25.md            # Daily notes
│   ├── weekly/2026-W13.md       # Weekly summaries
│   └── monthly/2026-03.md       # Monthly summaries
├── data/
│   ├── <agent>/memory/          # SQLite knowledge system
│   └── index/memory_index.db    # FTS5 + vector index
├── scripts/
│   ├── session_recorder.py      # Record events (5 types)
│   ├── unified_search.py        # Unified search (FTS5 + semantic + grep)
│   ├── memory_indexer.py        # Build index (optional --embed for vectors)
│   ├── memory_compressor.py     # Compression + sedimentation
│   ├── memory_stats.py          # System statistics
│   ├── health_check.py          # Health check + auto-fix
│   └── bridge/                  # Bidirectional sync
│       ├── bridge_sync.py
│       ├── bridge_to_markdown.py
│       └── bridge_to_knowledge.py
├── libs/memory_hub/             # Original knowledge system (backward compatible)
└── skills/                      # Original skills (backward compatible)
```

## 🛠️ Quick Start

### Minimal Install (Zero Dependencies)

Only Python 3.10+ required, works out of the box.

```bash
# Record event
python3 scripts/session_recorder.py -t event -c 'Completed important work today'

# Search (auto-selects best method)
python3 scripts/unified_search.py 'important work' --agent my-agent
```

### Recommended Enhancements (Optional)

**1. FTS5 Chinese Tokenization (Recommended)**

```bash
pip3 install jieba  # or pip3 install --user --break-system-packages jieba
python3 scripts/memory_indexer.py --full
```

**2. Semantic Search (Recommended, good for Chinese)**

```bash
# Install Ollama
brew install ollama  # macOS
# Or visit https://ollama.com/download

# Start and download model
ollama serve
ollama pull bge-m3  # 1.2GB, good for Chinese
# or ollama pull nomic-embed-text  # 274MB, good for English

# Build semantic index
python3 scripts/memory_indexer.py --full --embed

# Semantic search
python3 scripts/unified_search.py 'what did I do yesterday' --semantic
```

## 💬 Memory Flow in Conversations

**AGENTS.md includes complete specifications**, automatically followed in every conversation:

### At Conversation Start: Search Memory
When user mentions previous things → search first, then answer:
```bash
python3 scripts/unified_search.py 'relevant keywords' --agent my-agent --semantic
```

### During Conversation: Real-time Recording
When important info found → record immediately:
```bash
python3 scripts/session_recorder.py -t decision -c 'User decided to use X solution' --sync
python3 scripts/session_recorder.py -t learning -c 'Learned Y knowledge point' --sync
python3 scripts/session_recorder.py -t event -c 'Z event happened' --sync
```

### At Conversation End: Sync
If content was recorded → auto-sync (`--sync` runs in background)

## 🔧 Common Commands

| Command | Description |
|---------|-------------|
| `session_recorder.py -t event -c '...'` | Record event |
| `session_recorder.py -t decision -c '...' --sync` | Record decision and auto-sync |
| `unified_search.py 'keywords'` | Keyword search |
| `unified_search.py 'question' --semantic` | Semantic search |
| `bridge_sync.py --agent my-agent` | Bidirectional sync |
| `memory_indexer.py --incremental --embed` | Incremental index + vectors |
| `memory_compressor.py --weekly` | Generate weekly summary |
| `memory_stats.py --agent my-agent` | System statistics |
| `health_check.py --agent my-agent` | Health check |

## ⏰ Scheduled Tasks (Recommended)

```bash
# Daily 03:00: Incremental index
openclaw cron add --name "daily-index" --cron "0 3 * * *" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_indexer.py --incremental --embed"

# Every 6 hours: Bidirectional sync
openclaw cron add --name "bridge-sync" --every "6h" \
  --system-event "cd /path/to/workspace && python3 scripts/bridge/bridge_sync.py --agent my-agent"

# Monday 04:00: Weekly summary
openclaw cron add --name "weekly-compress" --cron "0 4 * * 1" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_compressor.py --weekly"
```

## 🔄 Graceful Degradation

| Dependency | Installed | Not Installed |
|------------|-----------|---------------|
| **jieba** | FTS5 Chinese tokenization | Fallback to grep (slower but works) |
| **Ollama + model** | Semantic search (natural language) | Fallback to FTS5 or grep |
| **Neither** | grep + SQLite LIKE | Core features fully functional |

**Minimal install has zero dependencies** — just Python 3.10+.

## 📚 Documentation

- `README.md` / `README.zh-CN.md` — This document
- `workspace-setup.md` — Complete installation guide
- `AGENTS.md` — Memory flow specifications for conversations
- `docs/ARCHITECTURE_GENERIC_EN.md` — Architecture design

## 📝 License

MIT
