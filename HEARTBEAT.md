# HEARTBEAT.md - Daily Checklist

Run at each heartbeat to check periodic tasks.

## Daily First Session Check

At the first heartbeat of each day:
1. Run daily review to show yesterday's summary
2. Create today's memory file if not exists

## Memory Maintenance

Weekly (every 7 days):
- Review memory files from past week
- Update MEMORY.md with important events
- Archive old daily files if needed

## How to Check

```bash
# Check if first session today
python3 skills/memory-search/daily_review.py

# Search memory
python3 skills/memory-search/search.py "关键词"

# Semantic search (requires Ollama)
python3 skills/memory-search/semantic_search.py "自然语言查询"
```
