---
name: websearch
description: 'Search the web using intelligent engine selection. No API key required. Auto-evolution enabled.'
---

# Web Search Skill (Auto-Evolution v3)

Intelligent web search with auto-evolution capabilities.

## Features

- ✅ **智能引擎选择** - 自动选择最佳搜索引擎
- ✅ **健康监控** - 实时监控引擎状态
- ✅ **自动切换** - 引擎故障时自动切换备选
- ✅ **自适应超时** - 基于历史表现动态调整
- ✅ **失败预测** - 预处理潜在问题

## Usage

```bash
# Basic search (auto-select best engine)
python3 skills/websearch/search.py "your search query"

# Limit results
python3 skills/websearch/search.py "your search query" --limit 3

# JSON output
python3 skills/websearch/search.py "your search query" --json
```

## Evolution History

- **v1**: Basic Bing search
- **v2**: Added retry mechanism and fallback
- **v3**: Smart engine selection, health monitoring, adaptive timeout (auto-evolved 2026-03-16)

## Examples

```bash
python3 skills/websearch/search.py "OpenClaw AI framework"
python3 skills/websearch/search.py "Python 3.14 features" --limit 5
python3 skills/websearch/search.py "latest AI news" --json
```
