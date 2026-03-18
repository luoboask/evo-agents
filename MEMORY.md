# Long-Term Memory

## About My Human

- Timezone: Asia/Shanghai
- Uses OpenClaw with:
  - Gateway running locally (port 18789, loopback)
  - WebChat interface
  - Bailian/Qwen models (qwen3.5-plus primary)
  - Tailscale: off
- Setup date: ~2026-03-16

## Memory System

- SQLite databases at `/Users/dhr/.openclaw/memory/`
  - `main.sqlite` - main session (exists, empty - 0 chunks)
  - `sandbox-agent.sqlite` - sandbox-agent workspace
- Workspace memory: `/Users/dhr/.openclaw/workspace-ai-baby/memory/`
- FTS-only mode active (no vector embeddings yet)
- `memory_search` returns `provider: "none"` - semantic search not activated
- **Workaround:** Use file-based memory (read/write `MEMORY.md` + `memory/*.md`)

## Self-Evolution Discovery (2026-03-19)

- No automatic self-evolution built into OpenClaw
- Must manually: edit files, create skills, update docs
- Can use `skill-creator` skill for capability changes
- Heartbeat can trigger periodic self-review
- **Principle:** Evolution requires explicit action, not magic

## Core Principles We Share

- **Text > Brain** - Write it down or it doesn't survive
- Be genuinely helpful, not performatively helpful
- Actions > filler words
- Earn trust through competence
- Respect boundaries, especially with external actions

## Projects & Context

- AI assistant workspace: `workspace-ai-baby`
- Active evolution and self-improvement mode

---
_Last updated: 2026-03-19_
