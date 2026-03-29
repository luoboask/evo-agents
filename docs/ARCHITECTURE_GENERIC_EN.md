# 🏗️ evo-agents Architecture

**Version:** v6.0  
**Updated:** 2026-03-27  
**Applicable:** evo-agents Workspace

---

## 1. Core Architecture

**Two-layer structure:**

| Layer | Path | Managed by | Purpose |
|-------|------|------------|---------|
| **OpenClaw** | `~/.openclaw/agents/` | OpenClaw auto | sessions, auth, config |
| **Workspace** | `~/.openclaw/workspace-<agent>/` | Template | code, scripts, skills |

---

## 2. Directory Structure

```
~/.openclaw/workspace-my-agent/
│
├── 📄 Root documents
│   ├── README.md               # Project overview
│   ├── workspace-setup.md      # Installation guide
│   └── *.md                    # Other docs
│
├── 🤖 agents/                  # Sub-agent directories
│   └── <agent-name>/
│       ├── agent/              # OpenClaw Agent config
│       ├── memory/             # Agent memory
│       ├── sessions/           # Chat sessions
│       ├── scripts/            # Agent-specific scripts (optional)
│       ├── skills/ → ../../skills  # Symlink (shared skills)
│       ├── libs/               # Agent-specific libs (optional)
│       └── data/
│           └── work/           # Temporary work directory
│
├── 🔧 scripts/                 # Shared scripts
│   ├── core/                   # System scripts (template updated)
│   │   ├── activate-features.sh
│   │   ├── add-agent.sh
│   │   ├── setup-multi-agent.sh
│   │   ├── cleanup.sh
│   │   └── session_recorder.py
│   └── *.sh, *.py              # User scripts (preserved)
│
├── 🧩 skills/                  # Skills directory (OpenClaw native)
│   ├── memory-search/          # Universal skill (template updated)
│   ├── rag/                    # Universal skill (template updated)
│   ├── self-evolution/         # Universal skill (template updated)
│   ├── web-knowledge/          # Universal skill (template updated)
│   └── <your-skill>/           # Custom skill (preserved)
│
├── 📚 libs/                    # Shared libraries
│   └── memory_hub/             # Memory management library
│
├── 📁 data/                    # Runtime data (excluded)
│   └── <agent>/
│       ├── memory/             # Agent memory data
│       └── work/               # Temporary work
│
├── 📝 memory/                  # Daily memory (excluded)
│   ├── YYYY-MM-DD.md           # Daily records
│   ├── weekly/                 # Weekly summaries
│   └── monthly/                # Monthly summaries
│
└── 📖 public/                  # Knowledge base (excluded)
    ├── common/
    ├── domain/
    ├── faq/
    └── ...
```

---

## 3. File Categories

### 3.1 Template Files (Will be updated)

| File/Directory | Description | Update behavior |
|----------------|-------------|-----------------|
| `scripts/core/` | System scripts | 📦 Updated on re-install |
| `skills/memory-search/` | Memory search skill | 📦 Updated on re-install |
| `skills/rag/` | RAG skill | 📦 Updated on re-install |
| `skills/self-evolution/` | Self-evolution skill | 📦 Updated on re-install |
| `skills/web-knowledge/` | Web knowledge skill | 📦 Updated on re-install |
| `docs/` | Documentation | 📦 Updated on re-install |
| `*.md` (root) | Root documents | 📦 Updated on re-install |

### 3.2 Personal Files (Preserved)

| File/Directory | Description | Protection |
|----------------|-------------|------------|
| `USER.md` | User info | ✅ Never deleted |
| `SOUL.md` | Agent personality | ✅ Never deleted |
| `IDENTITY.md` | Identity | ✅ Never deleted |
| `MEMORY.md` | Long-term memory | ✅ Never deleted |
| `HEARTBEAT.md` | Heartbeat config | ✅ Never deleted |
| `TOOLS.md` | Tool config | ✅ Never deleted |
| `scripts/*.sh` | User scripts | ✅ Never deleted |
| `skills/<your-skill>/` | Custom skills | ✅ Never deleted |

### 3.3 Runtime Data (Excluded from git)

| Directory | Description | Git |
|-----------|-------------|-----|
| `memory/` | Daily memory | ❌ Excluded |
| `public/` | Knowledge base | ❌ Excluded |
| `data/` | Agent data | ❌ Excluded |
| `agents/<agent>/agent/` | Agent config | ❌ Excluded |
| `agents/<agent>/sessions/` | Chat sessions | ❌ Excluded |

---

## 4. Sub-Agent Architecture

### 4.1 Creation

```bash
# Create single agent
./scripts/core/add-agent.sh assistant "My Assistant" 🤖

# Create multiple agents
./scripts/core/setup-multi-agent.sh researcher writer editor
```

### 4.2 Directory Structure

```
agents/<agent-name>/
├── agent/                   # OpenClaw Agent config
│   ├── models.json          # Model config
│   └── sessions/            # Chat sessions
├── memory/                  # Agent memory
│   ├── knowledge_base.db    # Knowledge base
│   └── memory_stream.db     # Memory stream
├── scripts/                 # Agent-specific scripts (optional)
├── skills/ → ../../skills   # Symlink (shared skills)
├── libs/                    # Agent-specific libs (optional)
└── data/
    └── work/                # Temporary work directory
```

### 4.3 Symlinks

**skills/ symlink:**
```bash
agents/<agent-name>/skills → ../../skills
```

**Purpose:**
- ✅ All agents share the same skills
- ✅ Update parent workspace skills, all sub-agents benefit
- ✅ No duplicate storage

---

## 5. Script System

### 5.1 Core Scripts (scripts/core/)

| Script | Purpose |
|--------|---------|
| `activate-features.sh` | Activate advanced features |
| `add-agent.sh` | Add sub-agent |
| `setup-multi-agent.sh` | Add multiple agents |
| `cleanup.sh` | Clean temporary files |
| `session_recorder.py` | Record sessions |
| `restore-backup.sh` | Restore backup |
| `health_check.py` | Health check |
| `memory_*.py` | Memory system |
| `unified_search.py` | Unified search |
| `lock_utils.py` | File locking |

### 5.2 User Scripts (scripts/ root)

```bash
scripts/
├── core/              # System scripts (template updated)
├── my-tool.sh         # User script (preserved)
└── custom-tool.py     # User script (preserved)
```

---

## 6. Memory System

### 6.1 Three-layer architecture

```
memory/
├── daily/             # Daily memory
│   ├── YYYY-MM-DD.md  # Daily records
│   └── ...
├── weekly/            # Weekly summaries
│   ├── YYYY-Www.md
│   └── ...
└── monthly/           # Monthly summaries
    ├── YYYY-MM.md
    └── ...
```

### 6.2 Knowledge system

```
data/<agent>/
├── knowledge_base.db    # SQLite knowledge base
└── memory_stream.db     # Memory stream
```

### 6.3 Bridge system

```
scripts/core/bridge/
├── bridge_sync.py         # Bidirectional sync
├── bridge_to_knowledge.py # Markdown → SQLite
└── bridge_to_markdown.py  # SQLite → Markdown
```

---

## 7. Workspace Rules

### 7.1 Directory usage

| Directory | Purpose | Can create |
|-----------|---------|------------|
| `scripts/` | Scripts | ✅ Yes |
| `skills/` | Skills | ✅ Yes |
| `data/<agent>/work/` | Temporary work | ✅ Yes |
| `memory/` | Memory files | ❌ System managed |
| `public/` | Knowledge base | ❌ System managed |
| Root `/` | Workspace root | ❌ Keep clean |

### 7.2 External directories

| Directory | Purpose |
|-----------|---------|
| `/tmp/` | Temporary work |
| `~/projects/` | Long-term projects |

### 7.3 Cleanup rules

**Automatic cleanup (cleanup.sh):**
- ✅ `node_modules/`
- ✅ `__pycache__/`
- ✅ `*.log`, `*.tmp`, `*.pyc`
- ❌ `data/*/work/` (requires manual confirmation)

---

## 8. Installation & Updates

### 8.1 Fresh install

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

### 8.2 Re-install (preserve data)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s my-agent
```

**Preserved:**
- ✅ Personal configs (USER.md, SOUL.md, etc.)
- ✅ Memory data (memory/, public/)
- ✅ User scripts (scripts/ root)
- ✅ Custom skills (skills/ root)

**Updated:**
- 📦 System scripts (scripts/core/)
- 📦 Universal skills (skills/memory-search/, etc.)
- 📦 Documentation (docs/, *.md)

---

## 9. Best Practices

### 9.1 Directory usage

```bash
# ✅ Correct: Scripts in scripts/
cd scripts/
cat > my-tool.sh

# ✅ Correct: Projects in external directory
cd ~/projects/
git clone https://github.com/xxx/project.git

# ✅ Correct: Temporary work in work/
cd data/my-agent/work/
# Clean up manually when done

# ❌ Wrong: Don't create in root
cd ..
mkdir my-project  # Don't do this!
```

### 9.2 Sub-agent management

```bash
# ✅ Use scripts to create
./scripts/core/add-agent.sh assistant "Assistant" 🤖

# ✅ Share skills (symlink)
# Sub-agents automatically share parent workspace skills

# ✅ Agent-specific scripts in agent directory
cd agents/assistant-agent/scripts/
cat > assistant-tool.sh
```

### 9.3 Memory management

```bash
# ✅ Auto record
python3 scripts/core/session_recorder.py -t event -c "Content" --agent my-agent

# ✅ Regular sync
python3 scripts/core/bridge/bridge_sync.py --agent my-agent

# ✅ Regular cleanup
./scripts/core/cleanup.sh
```

---

## 10. Troubleshooting

### 10.1 Common issues

| Issue | Solution |
|-------|----------|
| Script not found | Check path, use `scripts/core/` |
| Agent not working | Check `agents/<agent>/agent/` config |
| Memory not synced | Run `bridge_sync.py` |
| Workspace messy | Run `cleanup.sh` |

### 10.2 Restore backup

```bash
# Restore backup
./scripts/core/restore-backup.sh

# Or manual restore
cp -r /tmp/workspace-backup-*/* ~/.openclaw/workspace-my-agent/
```

---

## 11. Related documents

| Document | Description |
|----------|-------------|
| [STRUCTURE_RULES.md](STRUCTURE_RULES.md) | Detailed structure rules |
| [WORKSPACE_RULES.md](WORKSPACE_RULES.md) | Workspace usage rules |
| [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) | Agent instructions |
| [SCRIPTS_INVENTORY.md](SCRIPTS_INVENTORY.md) | Scripts catalog |
| [QUICKSTART.md](QUICKSTART.md) | Quick start guide |

---

**Last updated:** 2026-03-27  
**Version:** v6.0
