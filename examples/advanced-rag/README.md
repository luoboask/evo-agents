# Advanced RAG Example | 高级 RAG 示例

This example shows how to use RAG (Retrieval-Augmented Generation) features.

## Features | 功能

- ✅ Semantic search with embeddings
- ✅ RAG evaluation
- ✅ Auto-tuning
- ✅ Memory bridge (SQLite ↔ Markdown)

## Setup | 配置

```bash
# Install with activation
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s rag-agent --activate

# Or activate manually
cd ~/.openclaw/workspace-rag-agent
./scripts/core/activate-features.sh
```

## Usage | 使用

### Search | 搜索
```bash
# Semantic search
python3 skills/memory-search/search.py "your query"
```

### RAG Evaluation | RAG 评估
```bash
# Run evaluation
python3 skills/rag/evaluate.py

# Auto-tune
python3 skills/rag/auto_tune.py
```

### Memory Bridge | 记忆桥接
```bash
# Sync memory
python3 scripts/core/bridge/bridge_sync.py --agent rag-agent
```
