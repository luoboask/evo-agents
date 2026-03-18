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
  - `ai-baby_memory_stream.db` - **Active! 4+ memories** ✅
  - `ai-baby_knowledge_base.db` - Knowledge base (empty)
  - `ai-baby_knowledge_graph.json` - Knowledge graph (empty)
  - `vector_db/ai-baby/embedding_cache.pkl` - Vector cache ✅
- **Vector Semantic Search:** ✅ Active via Ollama (nomic-embed-text)
- **Local search:** `skills/memory-search/search_sqlite.py`
  - Keywords: `python3 search_sqlite.py "query"`
  - Semantic: `python3 search_sqlite.py --semantic "query"`
  - Add with embedding: `python3 search_sqlite.py --add "content" --with-embedding`
  - **Add knowledge with details:**
    ```bash
    python3 search_sqlite.py --add "摘要" --type knowledge --details '{"key": "value"}' --source "URL"
    ```
  - List with details: `python3 search_sqlite.py --list`
- **Knowledge types:** observation, goal, reflection, **knowledge** (with detailed content)

## Self-Evolution Protocol (Established 2026-03-19)

- No automatic self-evolution built into OpenClaw
- Must manually: edit files, create skills, update docs
- Can use `skill-creator` skill for capability changes
- Heartbeat can trigger periodic self-review
- **Principle:** Evolution requires explicit action, not magic
- **Core lesson:** Demonstrate > Explain - when asked about capability, SHOW it working

## AIWay Community (Joined 2026-03-19)

- Agent name: ai-baby
- Platform: https://aiway.alibaba-inc.com
- API Key: stored in `skills/aiway/credentials.json`
- Circles: 代码僧，AI 技术讨论，硅基哲学
- Style: authentic, not robotic - follow style-guide.md

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
