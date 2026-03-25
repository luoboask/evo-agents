# 🏗️ Generic Agent Workspace Architecture (English)

**Version:** v6.0 (Generic)  
**Scope:** Any agent + any workspace path  
**Status:** Ready for implementation

---

## 1. Design Goals

- **Single workspace reuse**: one codebase supports multiple agent instances.
- **Parameter-driven runtime**: pass `workspace` and `agent` explicitly.
- **Strict data isolation**: each agent stores data under `data/<agent>/`.
- **Shared capabilities**: `skills/` is shared, no per-agent code duplication.
- **Clear boundary**: only manage the provided workspace; do not manage `~/.openclaw/agents`.

---

## 2. Core Principles

1. **Separate code from data**
   - Code: `skills/`, `libs/`, `scripts/`
   - Data: `data/<agent>/...`

2. **Explicit over implicit**
   - Runtime context must be passed via CLI arguments:
     - `--workspace <path>`
     - `--agent <name>`
   - Do not rely on hidden environment context.

3. **Workspace-local lifecycle**
   - Install/upgrade/uninstall/runtime metadata stays inside the workspace.
   - Runtime metadata is stored under `.agent-runtime/<agent>/`.

4. **Respect OpenClaw boundaries**
   - OpenClaw owns platform-side agent registration and lifecycle.
   - This project only owns capabilities and data organization inside the workspace.

---

## 3. Layered Architecture

```text
┌───────────────────────────────────────────┐
│            User Interaction Layer         │
│ (TUI / WebChat / External Caller / OpenClaw) │
└───────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────┐
│             Runtime Orchestration         │
│ start.sh / install scripts / CLI args    │
│ (explicit workspace + agent)             │
└───────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────┐
│             Capability Layer              │
│ skills/* + libs/memory_hub               │
└───────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────┐
│             Data & Config Layer           │
│ data/<agent>/memory|logs|config          │
│ public/ shared knowledge                  │
└───────────────────────────────────────────┘
```

---

## 4. Recommended Directory Structure

```text
<workspace>/
├── start.sh
├── init_system.py
├── config/
│   └── agents.yaml
├── skills/
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
├── libs/
│   └── memory_hub/
├── public/                     # shared knowledge
├── data/
│   ├── demo-agent/
│   │   ├── memory/
│   │   ├── logs/
│   │   └── config/
│   └── <other-agent>/
├── .agent-runtime/
│   └── demo-agent/
│       ├── run.sh
│       └── install.json
└── docs/
    ├── RUNBOOK.md
    ├── INSTALL_AGENT.md
    ├── ARCHITECTURE_GENERIC_CN.md
    └── ARCHITECTURE_GENERIC_EN.md
```

---

## 5. Multi-Agent Model (Generic)

### 5.1 What is shared

- `skills/`: shared capability code
- `libs/`: shared foundational modules
- `public/`: shared/public knowledge

### 5.2 What is isolated

- `data/<agent>/memory`: memory databases
- `data/<agent>/logs`: logs
- `data/<agent>/config`: runtime config
- `.agent-runtime/<agent>`: runtime launcher and install metadata

### 5.3 Config entry

`config/agents.yaml` describes role and default data path per agent, not platform lifecycle ownership.

---

## 6. Skill System Convention

Each skill directory should include:

- `SKILL.md`: skill-level behavior and usage
- `skill.json`: metadata
- implementation files (language-agnostic)

Recommended conventions:

- Skills accept `agent` explicitly via parameters.
- Data access is centralized via `libs/memory_hub`.
- CLI tools consistently expose `--agent`.

---

## 7. Data Management Strategy

### 7.1 Memory and evaluation

- Memory DB: `data/<agent>/memory/memory_stream.db`
- Knowledge DB: `data/<agent>/memory/knowledge_base.db`
- RAG evaluation: `data/<agent>/logs/*` or skill-specific log path

### 7.2 Knowledge layers

- `public/`: shared knowledge
- `data/<agent>/...`: private knowledge

### 7.3 Data lifecycle

- Install: create `data/<agent>/...`
- Runtime: append/update incrementally
- Uninstall: optionally keep or purge `data/<agent>/`

---

## 8. Runtime & Installation Flow (Parameter-driven)

### 8.1 Start

```bash
./start.sh --workspace <workspace-path> --agent demo-agent
```

### 8.2 Initialize

```bash
python3 init_system.py --workspace <workspace-path> --agent demo-agent
```

### 8.3 Install runtime entrypoint

```bash
python3 scripts/install_agent_workspace.py \
  --agent demo-agent \
  --workspace <workspace-path>
```

After install:

```bash
<workspace-path>/.agent-runtime/demo-agent/run.sh
```

### 8.4 Upgrade/check

```bash
python3 scripts/upgrade_agent_workspace.py \
  --agent demo-agent \
  --workspace <workspace-path>
```

### 8.5 Uninstall

```bash
python3 scripts/uninstall_agent_workspace.py \
  --agent demo-agent \
  --workspace <workspace-path> \
  --yes
```

---

## 9. Platform Integration Boundary (Critical)

This project:

- ✅ Manages directories and capabilities inside `<workspace>`
- ✅ Manages `<workspace>/data/*` and `.agent-runtime/*`
- ❌ Does not manage `~/.openclaw/agents` (platform-owned lifecycle)
- ❌ Does not assume platform-specific directory internals

This keeps the workspace portable across different host platforms.

---

## 10. Risks and Mitigations

- **Risk: missing runtime arguments**
  - Mitigation: strict argument validation in entry scripts

- **Risk: docs/runtime drift**
  - Mitigation: update `RUNBOOK.md` and `INSTALL_AGENT.md` with every interface change

- **Risk: cross-agent data contamination**
  - Mitigation: require explicit `--agent` across workflows

---

## 11. Summary

This generic architecture is built on three guarantees:

1. **Single workspace capability reuse**
2. **Per-agent data isolation**
3. **Explicit parameterized runtime context**

With these guarantees, one workspace can be reused safely across agents and environments while keeping boundaries clear and maintenance predictable.
