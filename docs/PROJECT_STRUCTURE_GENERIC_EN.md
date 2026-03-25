# 📁 Project Structure Standard (Generic / English)

**Version:** v6.0  
**Scope:** Any agent + any workspace  
**Purpose:** Define folder layering, naming rules, dependency boundaries, and temp-script policy

---

## 1. Architecture Principles

### 1.1 Separation of concerns

```text
┌─────────────────────────────────────────┐
│          Capability Layer (skills/)      │
│ Independent features, callable, with docs │
└─────────────────────────────────────────┘
                    ▲ depends on
┌─────────────────────────────────────────┐
│            Library Layer (libs/)         │
│ Shared infrastructure, not skill entry   │
└─────────────────────────────────────────┘
```

### 1.2 Runtime context principle

- Runtime context must be explicit:
  - `--workspace <path>`
  - `--agent <name>`
- Avoid hidden implicit context.

### 1.3 Boundary principle

- Manage only the provided workspace.
- Do not manage platform-owned paths like `~/.openclaw/agents`.

---

## 2. Naming Conventions

| Directory Type | Convention | Example | Why |
|---|---|---|---|
| `libs/` modules | snake_case | `memory_hub` | import-friendly |
| `skills/` modules | kebab-case | `memory-search` | human/URL friendly |
| `scripts/` files | verb-object | `install_agent_workspace.py` | explicit behavior |
| `docs/` files | topic-based | `PROJECT_STRUCTURE_GENERIC_EN.md` | easy indexing |

---

## 3. Recommended Generic Layout

```text
<workspace>/
├── libs/
│   └── memory_hub/
│       ├── __init__.py
│       ├── hub.py
│       ├── storage.py
│       ├── knowledge.py
│       ├── evaluation.py
│       └── models.py
│
├── skills/
│   ├── memory-search/
│   │   ├── SKILL.md
│   │   ├── skill.json
│   │   └── search_sqlite.py
│   ├── rag/
│   │   ├── SKILL.md (optional)
│   │   ├── skill.json
│   │   └── evaluate.py
│   ├── self-evolution/
│   │   ├── SKILL.md (optional)
│   │   ├── skill.json
│   │   └── main.py
│   └── websearch/
│       ├── SKILL.md
│       ├── skill.json
│       └── search.py
│
├── scripts/
├── docs/
├── public/
├── data/
│   └── <agent>/
│       ├── memory/
│       ├── logs/
│       └── config/
├── .agent-runtime/
│   └── <agent>/
│       ├── run.sh
│       └── install.json
└── temp/
```

---

## 4. Directory Responsibilities

### 4.1 `libs/` (shared libraries)

- Reusable low-level capabilities (storage/model/evaluation).
- Not a skill entrypoint.
- Shared by multiple skills.

### 4.2 `skills/` (capabilities)

- User-facing callable features.
- Recommended content:
  - `SKILL.md`
  - `skill.json`
  - implementation files

### 4.3 `scripts/` (tooling entrypoints)

- Operational workflows: install/upgrade/test.
- Should be repeatable and idempotent.

### 4.4 `data/` (per-agent isolation)

- `data/<agent>/...` is the primary runtime data boundary.
- No cross-agent write access.

### 4.5 `.agent-runtime/` (workspace runtime metadata)

- Contains run entrypoint and install metadata.
- Scope is only the current workspace.

---

## 5. Dependency Direction Rules

```text
skills/*  ─────► libs/*
skills/*  ✖────► skills/*   (avoid tight lateral coupling)
libs/*    ✖────► skills/*   (no reverse dependency)
```

Rules:

- Skills may depend on libs.
- If skills share logic, extract it into `libs/`.
- Libs must not depend on skills.

---

## 6. Import and Invocation Standards

### 6.1 Library import (recommended)

```python
from libs.memory_hub import MemoryHub
```

### 6.2 Skill invocation (parameterized)

```bash
python3 skills/memory-search/search_sqlite.py "query" --agent demo-agent
python3 skills/rag/evaluate.py --report --days 7 --agent demo-agent
python3 skills/self-evolution/main.py --agent demo-agent status
```

---

## 7. Temporary Script Policy (`temp/`)

### 7.1 Typical use cases

- Debug helpers
- One-off migration scripts
- Quick experiments

### 7.2 Rules

- Keep temporary scripts in `temp/`, not `scripts/`.
- Suggested naming: `YYYY-MM-DD_xxx.py`.
- Promote useful scripts to stable locations, remove the rest.

### 7.3 Cleanup suggestion

```bash
# Inspect temp scripts
ls -lt temp/

# Remove scripts older than 7 days (example)
find temp/ -name "*.py" -mtime +7 -delete
```

---

## 8. New Module Checklist

### New Lib

- [ ] snake_case name
- [ ] clear exported API in `__init__.py`
- [ ] no dependency on `skills/`

### New Skill

- [ ] kebab-case name
- [ ] includes `SKILL.md` and `skill.json`
- [ ] has parameterized entrypoint (at least `--agent`)
- [ ] no direct dependency on other skill implementation files

### Review Checks

- [ ] layering is clear
- [ ] dependency direction is correct
- [ ] runtime context is explicit via CLI params

---

## 9. Summary

This generic structure ensures:

1. **Reusable capabilities** (`skills/` + `libs/`)
2. **Isolated data per agent** (`data/<agent>/`)
3. **Predictable runtime context** (explicit `workspace + agent`)
4. **Clear ownership boundary** (workspace-managed only)
