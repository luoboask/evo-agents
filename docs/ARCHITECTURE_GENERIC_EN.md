# 🏗️ test-agents Workspace Architecture

**Version:** v1.0  
**Updated:** 2026-03-26  
**Scope:** test-agents Workspace

---

## 1. Core Architecture

**Two-Layer Structure:**

| Layer | Path | Managed By | Purpose |
|-------|------|------------|---------|
| **OpenClaw** | `~/.openclaw/agents/` | OpenClaw Auto | sessions, auth |
| **Workspace** | `workspace/agents/` | Manual | Sub-Agent data isolation |

---

## 2. Directory Structure

```
~/.openclaw/workspace-test-agents/
│
├── 📄 Root Files
│   ├── AGENTS.md           # Session spec ⭐
│   ├── SOUL.md             # Agent identity ⭐
│   ├── MEMORY.md           # Long-term memory ⭐
│   ├── USER.md             # User info ⭐
│   ├── IDENTITY.md         # Identity
│   ├── TOOLS.md            # Tools config
│   └── HEARTBEAT.md        # Heartbeat check
│
├── 🤖 agents/              # ⭐ Sub-Agent isolation
│   ├── analyst-agent/      # 🔍 Requirement Analyst
│   │   ├── AGENTS.md
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   ├── config.yaml
│   │   ├── memory/         # 🔒 Independent memory
│   │   └── data/           # 🔒 Independent database
│   ├── developer-agent/    # 💻 Code Developer
│   └── tester-agent/       # ✅ Quality Tester
│
├── 🔧 scripts/             # ⭐ Shared scripts
│   ├── session_recorder.py     # Supports --agent
│   ├── unified_search.py       # Supports --agent
│   ├── memory_indexer.py
│   ├── memory_compressor.py
│   ├── memory_stats.py
│   ├── health_check.py
│   └── bridge/                 # Bidirectional sync
│
├── 📚 libs/                  # ⭐ Shared libraries
│   └── memory_hub/
│
├── 🎯 skills/                # ⭐ Shared skills
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📝 memory/                # Main Agent memory
├── 💾 data/                  # Main Agent data
├── 🌐 public/                # Public knowledge base
├── ⚙️ config/                # Config
│   └── agents.yaml
├── 📂 projects/              # Git repos management
└── docs/                     # Documentation
```

---

## 3. Multi-Agent Design

### 3.1 Agent List

| Agent | Role | Path | Emoji |
|-------|------|------|-------|
| **test-agents** | coordinator | `memory/` + `data/` | 🦞 |
| **analyst-agent** | analyst | `agents/analyst-agent/` | 🔍 |
| **developer-agent** | developer | `agents/developer-agent/` | 💻 |
| **tester-agent** | tester | `agents/tester-agent/` | ✅ |

### 3.2 Shared vs Isolated

| Resource | Shared/Isolated | Description |
|----------|-----------------|-------------|
| `scripts/` | ✅ Shared | All Agents use same scripts |
| `libs/` | ✅ Shared | All Agents use same libraries |
| `skills/` | ✅ Shared | All Agents use same skills |
| `memory/` | 🔒 Isolated | Each Agent has independent memory |
| `data/` | 🔒 Isolated | Each Agent has independent database |

### 3.3 Collaboration Flow

```
1️⃣  analyst-agent    Requirement Analysis
    ↓
2️⃣  developer-agent  Implementation
    ↓
3️⃣  tester-agent     Quality Testing
    ↓
4️⃣  test-agents      Summary & Documentation
```

---

## 4. Usage

### Record Events

```bash
cd ~/.openclaw/workspace-test-agents

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

---

## 5. Git Repos Management

### projects/ Directory

```
projects/
├── lib-a/          # Flat structure, no categories
├── app-b/
└── test-repo/
```

**Principles:**
- ✅ Flat structure - All repos in `projects/`
- ✅ No categories - Avoid decision cost
- ✅ Manual cleanup - Delete when not needed

### Usage

```bash
# Clone
git clone https://github.com/xxx/lib.git projects/

# List
ls -1 projects/

# Delete
rm -rf projects/old-lib/
```

---

## 6. Core Principles

1. **Shared Code + Isolated Data** - scripts/libs/skills shared, memory/data isolated
2. **Parameterized Design** - All scripts support `--agent` parameter
3. **Flat Structure** - projects/ without categories
4. **OpenClaw Boundary** - `~/.openclaw/agents/` managed by OpenClaw

---

## 7. Configuration

### config/agents.yaml

```yaml
test-agents:
  name: test-agents
  role: coordinator
  data_path: data/test-agents
  memory_path: memory

analyst-agent:
  name: analyst-agent
  role: analyst
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory

developer-agent:
  name: developer-agent
  role: developer
  
tester-agent:
  name: tester-agent
  role: tester
```

---

## 8. Documentation

| Document | Purpose |
|----------|---------|
| `ARCHITECTURE_GENERIC_CN.md` | Architecture (Chinese) |
| `ARCHITECTURE_GENERIC_EN.md` | This document - Architecture (English) |
| `PROJECT_STRUCTURE_GENERIC_CN.md` | Directory Structure (Chinese) |
| `PROJECT_STRUCTURE_GENERIC_EN.md` | Directory Structure (English) |

---

**Last Updated:** 2026-03-26  
**Maintainer:** test-agents 🦞
