# 📁 test-agents Workspace - Directory Structure

**Version:** v1.0  
**Updated:** 2026-03-26  
**Scope:** test-agents Workspace

---

## 1. Architecture Principles

### 1.1 Separation of Concerns

```
┌─────────────────────────────────────────┐
│       Shared Layer (scripts/libs/skills) │
│   All Agents share, supports --agent     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     Isolated Layer (agents/*/memory)    │
│   Each Agent has independent memory      │
└─────────────────────────────────────────┘
```

### 1.2 Core Principles

- **Shared Code** - scripts/libs/skills shared by all Agents
- **Isolated Data** - Each Agent has independent memory/ and data/
- **Parameterized** - All scripts support `--agent` parameter

---

## 2. Complete Directory Structure

```
workspace/
│
├── 📄 Root Files
│   ├── AGENTS.md           # Session spec ⭐
│   ├── SOUL.md             # Agent identity
│   ├── MEMORY.md           # Long-term memory
│   ├── USER.md             # User info
│   ├── IDENTITY.md         # Identity
│   ├── TOOLS.md            # Tools config
│   └── HEARTBEAT.md        # Heartbeat check
│
├── 🤖 agents/              # ⭐ Sub-Agent isolation
│   ├── analyst-agent/
│   │   ├── AGENTS.md
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   ├── config.yaml
│   │   ├── memory/         # 🔒 Independent memory
│   │   └── data/           # 🔒 Independent database
│   ├── developer-agent/
│   └── tester-agent/
│
├── 🔧 scripts/             # ⭐ Shared scripts
│   ├── session_recorder.py
│   ├── unified_search.py
│   ├── memory_indexer.py
│   ├── memory_compressor.py
│   ├── memory_stats.py
│   ├── health_check.py
│   └── bridge/
│
├── 📚 libs/                # ⭐ Shared libraries
│   └── memory_hub/
│
├── 🎯 skills/              # ⭐ Shared skills
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📝 memory/              # Main Agent memory
├── 💾 data/                # Main Agent data
├── 🌐 public/              # Public knowledge base
├── ⚙️ config/              # Config
├── 📂 projects/            # Git repos
└── docs/                   # Documentation
```

---

## 3. Directory Responsibilities

### 3.1 Root Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Session行为规范 (search, record, sync) |
| `SOUL.md` | Agent identity and personality |
| `MEMORY.md` | Long-term memory (events, decisions) |
| `USER.md` | User information |
| `IDENTITY.md` | Identity (name, emoji, avatar) |
| `TOOLS.md` | Tools config (cameras, SSH, TTS) |
| `HEARTBEAT.md` | Heartbeat checklist |

### 3.2 agents/ - Sub-Agent Isolation

| Agent | Path | Purpose |
|-------|------|---------|
| analyst-agent | `agents/analyst-agent/` | Requirement Analysis 🔍 |
| developer-agent | `agents/developer-agent/` | Code Implementation 💻 |
| tester-agent | `agents/tester-agent/` | Quality Testing ✅ |

Each sub-Agent contains:
- `AGENTS.md` -行为规范
- `SOUL.md` - Identity
- `MEMORY.md` - Memory
- `config.yaml` - Config
- `memory/` - Independent memory directory
- `data/` - Independent database

### 3.3 scripts/ - Shared Scripts

| Script | Function | Supports --agent |
|--------|----------|------------------|
| `session_recorder.py` | Record events | ✅ |
| `unified_search.py` | Unified search | ✅ |
| `memory_indexer.py` | Build index | ✅ |
| `memory_compressor.py` | Compression | ✅ |
| `memory_stats.py` | System stats | ✅ |
| `health_check.py` | Health check | ✅ |
| `bridge/*.py` | Bidirectional sync | ✅ |

### 3.4 skills/ - Shared Skills

| Skill | Function |
|-------|----------|
| `memory-search/` | Memory search (keyword + semantic) |
| `rag/` | RAG evaluation |
| `self-evolution/` | Self-evolution system |
| `websearch/` | Web search |

### 3.5 memory/ - Main Agent Memory

```
memory/
├── YYYY-MM-DD.md        # Daily records
├── weekly/              # Weekly summaries
├── monthly/             # Monthly summaries
├── archive/             # Archive
└── knowledge/           # Knowledge
```

### 3.6 data/ - Main Agent Data

```
data/
├── .locks/              # File locks
├── index/               # Search index
└── test-agents/         # test-agents SQLite data
```

### 3.7 public/ - Public Knowledge Base

| Category | Purpose |
|----------|---------|
| `common/` | General knowledge |
| `domain/` | Domain knowledge |
| `faq/` | FAQ |
| `openclaw/` | OpenClaw related |
| `operations/` | Operations knowledge |
| `prompt/` | Prompt templates |
| `rag/` | RAG related |
| `security/` | Security knowledge |
| `skills/` | Skill documentation |
| `tutorial/` | Tutorials |

### 3.8 projects/ - Git Repos Management

```
projects/
├── lib-a/          # Flat, no categories
├── app-b/
└── test-repo/
```

**Principles:**
- ✅ Flat structure - All repos in `projects/`
- ✅ No categories - Avoid decision cost
- ✅ Manual cleanup - Delete when not needed

---

## 4. Naming Conventions

| Directory Type | Convention | Example |
|---------------|------------|---------|
| `libs/` subdirs | Underscore `_` | `memory_hub` |
| `skills/` subdirs | Hyphen `-` | `memory-search` |
| `scripts/` files | Verb+Object | `session_recorder.py` |
| `agents/` subdirs | Hyphen `-` | `analyst-agent` |
| `docs/` files | Topic naming | `ARCHITECTURE_GENERIC_CN.md` |

---

## 5. Dependencies

```
skills/*  ─────► libs/*
skills/*  ✖────► skills/*   (avoid horizontal coupling)
libs/*    ✖────► skills/*   (no reverse dependencies)
```

---

## 6. Usage Examples

### Record Events

```bash
# Record to sub-Agent
python3 scripts/session_recorder.py -t event -c 'content' --agent analyst-agent

# Record to main Agent
python3 scripts/session_recorder.py -t decision -c 'content' --agent test-agents --sync
```

### Search Memory

```bash
# Search sub-Agent
python3 scripts/unified_search.py 'keyword' --agent developer-agent --semantic

# Search main Agent
python3 scripts/unified_search.py 'keyword' --agent test-agents --semantic
```

### Git Repos

```bash
# Clone
git clone https://github.com/xxx/lib.git projects/

# List
ls -1 projects/

# Delete
rm -rf projects/old-lib/
```

---

## 7. Summary

| Directory | Shared/Isolated | Description |
|-----------|-----------------|-------------|
| `scripts/` | ✅ Shared | All Agents share |
| `libs/` | ✅ Shared | All Agents share |
| `skills/` | ✅ Shared | All Agents share |
| `agents/*/` | 🔒 Isolated | Each sub-Agent independent |
| `memory/` | 🔒 Isolated | Main Agent independent |
| `data/` | 🔒 Isolated | Main Agent independent |
| `public/` | ✅ Shared | Public knowledge |
| `projects/` | ✅ Shared | Git repos |

---

**Last Updated:** 2026-03-26  
**Maintainer:** test-agents 🦞
