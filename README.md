# evo-agents

[English](./README.md) | [简体中文](./README.zh-CN.md)

Reusable self-evolving agent workspace with explicit runtime context (`--workspace`, `--agent`), strict per-agent data isolation, and shared capability layers.

## 🦞 OpenClaw One-Click Bootstrap

For clone -> install -> healthcheck -> full verification in one flow, use `workspace-setup.md`.

## Why This Repository

`evo-agents` is designed to make one workspace reusable across multiple agents while keeping runtime behavior deterministic:

- explicit context passing over implicit environment coupling
- code/data separation by design
- workspace-local runtime metadata
- clean boundary with platform-owned lifecycle

Detailed design docs:

- `docs/ARCHITECTURE_GENERIC_EN.md`
- `docs/PROJECT_STRUCTURE_GENERIC_EN.md`

## Architecture Snapshot

Layered model:

- **Interaction**: OpenClaw / external callers
- **Orchestration**: `start.sh`, install/upgrade scripts, CLI argument parsing
- **Capabilities**: `skills/*` + `libs/memory_hub`
- **Data/Config**: `data/<agent>/...` + `public/`

Core rules:

- **Code/Data Separation**: code in `skills/`, `libs/`, `scripts/`; runtime data in `data/<agent>/...`
- **Explicit Runtime Context**: pass `--workspace` and `--agent` to entrypoints
- **Workspace-local Runtime**: metadata in `.agent-runtime/<agent>/`
- **Boundary Safety**: do not manage `~/.openclaw/agents`

## Repository Layout

```text
evo-agents/
├── start.sh
├── init_system.py
├── skills/                      # callable capability modules
├── libs/memory_hub/             # shared infra library
├── scripts/                     # install/upgrade/uninstall/test helpers
├── data/<agent>/                # isolated runtime data per agent
├── .agent-runtime/<agent>/      # run.sh + install metadata
├── public/                      # shared knowledge assets
├── docs/                        # architecture and structure docs
└── workspace-setup.md           # OpenClaw bootstrap playbook
```

Dependency direction:

- `skills/*` -> `libs/*`: allowed
- `skills/*` -> `skills/*`: avoid (extract shared logic to `libs/`)
- `libs/*` -> `skills/*`: forbidden

## Quick Start

```bash
# 1) Initialize (first run)
python3 init_system.py --workspace <workspace-root> --agent demo-agent

# 2) Health check / status
./start.sh --workspace <workspace-root> --agent demo-agent
```

## Agent Runtime Lifecycle

```bash
# Install runtime entrypoint for one agent
python3 scripts/install_agent_workspace.py \
  --workspace <workspace-root> \
  --agent demo-agent

# Upgrade/check
python3 scripts/upgrade_agent_workspace.py \
  --workspace <workspace-root> \
  --agent demo-agent

# Uninstall (optional data purge)
python3 scripts/uninstall_agent_workspace.py \
  --workspace <workspace-root> \
  --agent demo-agent \
  --purge-data \
  --yes
```

## Common Commands

```bash
# Memory search
python3 skills/memory-search/search_sqlite.py "query" --agent demo-agent
python3 skills/memory-search/search_sqlite.py "query" --semantic --agent demo-agent

# RAG evaluation
python3 skills/rag/evaluate.py --report --days 7 --agent demo-agent

# Self-evolution
python3 skills/self-evolution/main.py --agent demo-agent status
python3 skills/self-evolution/main.py --agent demo-agent fractal --limit 10
python3 skills/self-evolution/main.py --agent demo-agent nightly
```

## Verification

```bash
python3 scripts/test_features.py --agent demo-agent
python3 test_all.py --workspace <workspace-root> --agent demo-agent
python3 scripts/test_agents.py --workspace <workspace-root> --agent demo-agent
```

