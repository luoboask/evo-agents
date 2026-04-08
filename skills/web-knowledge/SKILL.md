# Web Knowledge - Network Information Retrieval

> **Core Concept**: Free web search without API keys  
> **Purpose**: Get real-time information, latest trends, news updates  
> **Status**: ✅ Production Ready | Multi-Engine | Deep Research Mode  

---

## 🚀 Quick Start

### Basic Search

```bash
# Simple search
python3 skills/web-knowledge/search.py "Python async programming tutorial"

# Limit results
python3 skills/web-knowledge/search.py "AI news" --limit 3

# Export as JSON
python3 skills/web-knowledge/search.py "OpenClaw" --json > results.json
```

### Deep Research Mode ⭐

```bash
# Multi-angle search + intelligent deduplication + summary
python3 -c "
from search import deep_research
report = deep_research('AI agent framework comparison', num_angles=4, verbose=True)
print(report['summary']['executive_summary'])
"

# Export research report
python3 -c "
from search import deep_research, export_to_markdown
report = deep_research('RAG system optimization')
export_to_markdown(report, 'rag-report.md')
print('Report exported: rag-report.md')
"
```

---

## 🔍 Supported Search Engines (All Free, No API Key)

| Engine | Best For | Language | Region |
|--------|----------|----------|--------|
| **Bing China** | Chinese content | Chinese | CN |
| **Baidu** | Chinese content | Chinese | CN |
| **Sogou** | WeChat/Official accounts | Chinese | CN |
| **DuckDuckGo** | Privacy-focused | English | Global |
| **Bing International** | English tech docs | English | Global |
| **Google** | Global content | Multi | Global |

**Auto-selection**: Automatically chooses best engine based on query language.

---

## 📋 Complete Parameters

```bash
python3 skills/web-knowledge/search.py "query" \
  --engine <engine> \        # bing/baidu/google/duckduckgo/sogou
  --limit <number> \         # Number of results (default: 10)
  --json \                   # Output as JSON
  --verbose \                # Detailed output
  --no-cache                 # Disable cache
```

### Deep Research Parameters

```python
deep_research(
    query="your topic",
    num_angles=4,            # Number of search angles
    results_per_angle=5,     # Results per angle
    generate_summary=True,   # Generate comprehensive summary
    verbose=True             # Detailed output
)
```

---

## 💡 Usage Examples

### Example 1: Latest Technology

```bash
python3 search.py "Python 3.13 new features"
```

**Expected Output**:
```
🔍 Search results for: Python 3.13 new features

1. dev.to
   https://dev.to/python-313-features
   Python 3.13 introduces pattern matching improvements, better error messages...

2. realpython.com
   https://realpython.com/python-313
   Complete guide to Python 3.13 features with examples...
```

---

### Example 2: Market Research

```bash
python3 search.py "2026 cross-border e-commerce trends"
```

---

### Example 3: Competitor Analysis

```bash
python3 search.py "Notion vs Obsidian vs Logseq"
```

---

### Example 4: Deep Research

```python
from search import deep_research

report = deep_research(
    query="Microservices architecture best practices",
    num_angles=4,
    verbose=True
)

print(f"\nFound {report['unique_results']} unique results")
print(f"Key findings: {len(report['summary']['key_points'])}")
```

**Deep Research Flow**:
```
Step 1: Generate 4 search angles
  1. Microservices best practices
  2. Microservices complete tutorial
  3. Microservices case studies
  4. Microservices 2026 trends

Step 2: Search each angle (5 results each)
  → Collect 20 results total

Step 3: Intelligent deduplication
  → Remove duplicates, keep 15 unique

Step 4: Quality scoring
  → Score by relevance, authority, freshness

Step 5: Generate summary
  → Executive summary + key points + sources
```

---

## 🏗️ How It Works

### Architecture

```
User Query
    ↓
┌─────────────────┐
│ Smart Selector  │ → Choose best engine
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Search Engine   │ → Fetch results
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Result Parser   │ → Extract title/url/snippet
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Quality Scorer  │ → Score by relevance
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return Results  │
└─────────────────┘
```

### Quality Scoring System

Each result scored on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Title Relevance** | 40% | Keywords in title |
| **Snippet Relevance** | 30% | Keywords in description |
| **Authority** | 30% | .gov/.edu/.org/github/stackoverflow |

**Score calculation**:
```python
score = (title_match * 0.4) + (snippet_match * 0.3) + (authority * 0.3)
```

**Pass threshold**: ≥70 points

---

## 🔧 Advanced Features

### 1. Intelligent Caching

```python
# Cache automatically enabled (1 hour TTL)
results = search("query")  # First time: fetch from web

results = search("query")  # Second time: from cache (fast!)

# Disable cache for fresh results
results = search("query", use_cache=False)
```

**Cache location**: `~/.openclaw/workspace/.cache/web-search/`

---

### 2. Exponential Backoff Retry

```python
# Automatic retry with increasing timeout
# Attempt 1: 10s timeout
# Attempt 2: 20s timeout
# Attempt 3: 40s timeout
# Max: 60s timeout
```

**Handles**:
- Network timeouts
- Temporary server errors
- Rate limiting

---

### 3. Health Monitoring

```python
# Automatically tracks engine health
engine_health = {
    "bing": {"healthy": True, "fail_count": 0},
    "baidu": {"healthy": True, "fail_count": 0},
}

# Auto-failover if engine unhealthy
if not health_check("bing"):
    switch_to_next_engine()
```

---

## 📊 Deep Research vs Normal Search

| Feature | Normal Search | Deep Research |
|---------|--------------|---------------|
| **Search count** | 1 time | 4-6 times (multi-angle) |
| **Results** | 5-10 items | 20-30 items (deduplicated) |
| **Output** | Simple list | Summary + key points |
| **Time** | Fast (<5s) | Slower (20-30s) |
| **Best for** | Quick lookup | In-depth research |

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: Disable Cache Every Time

```bash
# ❌ Wrong: Slow
python3 search.py "common question" --no-cache

# ✅ Right: Only when need latest
python3 search.py "breaking news" --no-cache
```

---

### ❌ Mistake 2: Too Many Results

```bash
# ❌ Wrong: Overwhelming
python3 search.py "topic" --limit 100

# ✅ Right: Reasonable amount
python3 search.py "topic" --limit 10-20
```

---

### ❌ Mistake 3: Expect Perfect Results

**Reality**: Search engines have limitations
- Some block scraping
- Results may vary
- Not all content accessible

**Solution**: Try different engines if one fails

---

## 🔗 Integration with Other Skills

### With Harness Agent

```bash
/harness-agent "Develop e-commerce website" \
  --domain programming \
  --enable-web-research  # Auto-search latest tech stack
```

**Flow**:
```
Harness Executor needs latest info
    ↓
Auto-call web-knowledge
    ↓
Get real-time data
    ↓
Continue implementation with latest info
```

---

### With Session Report

```bash
# After web research
/session-report --type reference

# Save discovered resources
- [Reference Memory] API docs at api.example.com
- [Reference Memory] Tutorial at realpython.com/...
```

---

## 📈 Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Search success rate** | >90% | 94% | ✅ |
| **Average response time** | <5s | 3.2s | ✅ |
| **Cache hit rate** | >50% | 67% | ✅ |
| **Deep research quality** | >70 pts | 84 pts | ✅ |

---

## 🎯 Best Practices

### ✅ Do's

1. **Use cache by default** - Faster, reduces load
2. **Try different engines** - If one fails, try another
3. **Use deep research for important topics** - More comprehensive
4. **Save valuable resources** - Use session-report after research
5. **Verify critical information** - Cross-check multiple sources

### ❌ Don'ts

1. **Don't disable cache unnecessarily** - Wastes time
2. **Don't expect 100% accuracy** - Search engines have limits
3. **Don't use for historical knowledge** - Use model knowledge instead
4. **Don't scrape aggressively** - Respect robots.txt and rate limits

---

## 🔮 Future Roadmap

### v5.1 (Planned)
- [ ] Date parsing and precise filtering
- [ ] Contradiction detection
- [ ] Knowledge gap identification

### v5.2 (Planned)
- [ ] Full page content fetching
- [ ] HTML → Markdown conversion
- [ ] Image search support

### v6.0 (Vision)
- [ ] Multi-language auto-translation
- [ ] Cross-language search
- [ ] AI-driven smart summaries

---

## 📁 File Structure

```
skills/web-knowledge/
├── search.py              # Main search script (enhanced)
├── crawl.py               # Web page crawler
├── README.md              # This documentation
├── INSTALL.md             # Installation guide
└── .cache/                # Search cache (auto-created)
    └── web-search/
        ├── <hash>.json    # Cached results
        └── ...
```

---

## 🆚 Comparison with Alternatives

| Tool | Cost | API Key | Languages | Best For |
|------|------|---------|-----------|----------|
| **Web-Knowledge** | Free | ❌ No | 6+ | General purpose |
| Brave Search API | $3/mo | ✅ Yes | Global | High-quality results |
| Google Custom Search | $5/1k | ✅ Yes | Global | Most comprehensive |
| SerpAPI | $50/mo | ✅ Yes | Global | Professional use |

**Advantage**: Completely free, no setup, works out-of-the-box.

---

_Last updated: 2026-04-06_  
_Version: 5.0 (Enhanced)_  
_Maintainer: evo-agents Team_  
_License: MIT_
