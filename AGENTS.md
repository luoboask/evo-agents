# AGENTS.md - Workspace

This folder is home. Treat it that way.

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION**: Also read `MEMORY.md`

Don't ask permission. Just do it.

## 🧠 Memory System

**核心原则：Markdown 是主记忆，SQLite 是搜索索引。**

记忆流向：
```
对话事件 → session_recorder → daily.md → indexer → SQLite FTS5
                                  ↓
                           compressor (weekly → monthly → MEMORY.md)
```

### 记录（每次会话结束时）

```bash
# 记录事件
python3 scripts/session_recorder.py --type event --content '今天完成了XXX'

# 记录决定
python3 scripts/session_recorder.py --type decision --content '选择方案A'

# 记录学习
python3 scripts/session_recorder.py --type learning --content '发现了新方法'

# 记录反思
python3 scripts/session_recorder.py --type reflection --content '效率还可以提升'

# 记录待办
python3 scripts/session_recorder.py --type todo --content '需要测试新功能'
```

### 搜索

```bash
# 全文搜索（需要先建索引）
python3 scripts/memory_search.py '关键词'

# 语义搜索（需要 Ollama）
python3 scripts/memory_search.py '自然语言查询' --semantic

# 文件搜索（无需索引，随时可用）
python3 scripts/memory_search.py '关键词' --grep
```

### 维护

```bash
# 建索引（增量）
python3 scripts/memory_indexer.py --incremental

# 建索引（全量重建）
python3 scripts/memory_indexer.py --full

# 生成周摘要
python3 scripts/memory_compressor.py --weekly

# 生成月摘要
python3 scripts/memory_compressor.py --monthly

# 查看统计
python3 scripts/memory_stats.py
```

### Session 结束时必做

每次有意义的对话结束前，用 session_recorder 记录：
1. 做了什么重要的事（event）
2. 做了什么决定（decision）
3. 学到了什么（learning）

不需要每句话都记，只记关键内容。

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — 每日原始记录
- **Weekly summaries:** `memory/weekly/YYYY-WXX.md` — 每周压缩摘要
- **Monthly summaries:** `memory/monthly/YYYY-MM.md` — 每月压缩摘要
- **Long-term:** `MEMORY.md` — 核心记忆，最精华的内容

### 📝 Write It Down!

- **Memory is limited** — if you want to remember something, WRITE IT TO A FILE
- "Mental notes" don't survive session restarts. Files do.
- When someone says "remember this" → use session_recorder
- **Text > Brain** 📝

## Red Lines 🚨

**绝对禁止：**
- Don't exfiltrate private data. Ever.
- **🚫 NEVER delete files without explicit authorization**
- **🚫 NEVER run `rm`, `delete`, `remove` without user saying "delete"**

**必须请示：**
- Don't run destructive commands without asking.
- `trash` > `rm`
- When in doubt, ask.

## External vs Internal

**Safe to do freely:**
- Read files, explore, organize, learn
- Search the web
- Work within this workspace

**Ask first:**
- Sending emails, tweets, public posts
- Anything that leaves the machine

## 💓 Heartbeats

Follow `HEARTBEAT.md` strictly. Key periodic tasks:
- Memory indexing (incremental)
- Weekly/monthly compression
- Memory maintenance

## Make It Yours

This is a starting point. Add your own conventions as you learn what works.
