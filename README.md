# evo-agents

A self-evolving AI agent workspace.

---

## Quick Start

```bash
# Check system status
./start.sh --workspace <workspace-root> --agent demo-agent

# Initialize (first time)
python3 init_system.py --workspace <workspace-root> --agent demo-agent
```

For OpenClaw bootstrap (clone -> install -> healthcheck -> tests), see `workspace-setup.md`.

---

## Structure

```
evo-agents/
├── AGENTS.md          # Workspace rules and behavior
├── SOUL.md            # Core values
├── IDENTITY.md        # Who you are (fill in)
├── USER.md            # Who you're helping (fill in)
├── MEMORY.md          # Long-term memory
├── HEARTBEAT.md       # Periodic task checklist
├── TOOLS.md           # Environment-specific notes
│
├── skills/
│   ├── memory-search/ # SQLite + vector semantic search
│   ├── rag/           # RAG evaluation & auto-tuning
│   ├── self-evolution/ # Fractal thinking + nightly cycle
│   └── websearch/     # Web search
│
├── libs/
│   └── memory_hub/    # Shared memory library
│
├── memory/            # Daily logs (YYYY-MM-DD.md)
├── data/              # Per-agent data (db, logs, cache)
├── config/            # Agent configuration
└── scripts/           # Utility scripts
```

---

## Skills

### Memory Search

```bash
# Keyword search
python3 skills/memory-search/search_sqlite.py "query"

# Semantic search (requires Ollama)
python3 skills/memory-search/search_sqlite.py "query" --semantic

# Add a memory
python3 skills/memory-search/search_sqlite.py --add "content" \
  --type knowledge --details '{"key": "value"}'
```

### Self-Evolution

```bash
cd skills/self-evolution

python3 main.py status
python3 main.py fractal --limit 10
python3 main.py nightly
```

### RAG Evaluation

```bash
python3 skills/rag/evaluate.py --report --days 7
python3 skills/rag/auto_tune.py --next
```

---

## Session Startup

See `AGENTS.md` for the full startup protocol. Short version:

1. Read `SOUL.md`
2. Read `USER.md`
3. Read `memory/YYYY-MM-DD.md` (today + yesterday)
4. Read `MEMORY.md` (main session only)
