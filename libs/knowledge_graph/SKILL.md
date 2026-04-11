# Knowledge Graph - 知识图谱共享库

> **Core Concept**: Store knowledge as entities and relationships (graph structure)  
> **Purpose**: Enable reasoning, fact verification, and structured queries  
> **Status**: ✅ Production Ready | Auto-build from Memory | Entity-Relationship Model  
> **Location**: `libs/knowledge-graph/` (shared library, not a skill)  
> **Used by**: memory-search, self-evolution, and other skills  

---

## 🚀 Quick Start

### Basic Usage

```bash
# Build knowledge graph (auto-extract from memory files)
python3 libs/knowledge-graph/builder.py

# Build without AI (faster, rules only)
python3 libs/knowledge-graph/builder.py --no-ai

# View statistics
python3 libs/knowledge-graph/builder.py --stats
```

### Integration in Skills

```python
# Example: memory-search/search_with_kg.py
from knowledge_graph.builder import KnowledgeGraph

# Load existing graph
kg = KnowledgeGraph()

# Access entities and relations
entities = kg.entities      # Dict of entities
relations = kg.relations    # List of relationships

# Query by entity type
tech_entities = [e for e in entities.values() if e['type'] == 'Technology']
```

---

## 🏗️ Architecture

### Data Model

```json
{
  "entities": {
    "Technology:openclaw": {
      "type": "Technology",
      "name": "OpenClaw",
      "mentions": 48,
      "created_at": "2026-03-16"
    }
  },
  "relations": [
    {
      "source": "Technology:openclaw",
      "relation": "基于",
      "target": "Technology:jvs_claw",
      "confidence": 0.9
    }
  ]
}
```

### Build Process

```
memory/*.md (记忆文件)
    ↓
builder.py (规则提取 + AI 提取)
    ↓
knowledge_graph.json (知识图谱)
    ↓
memory-search/search_with_kg.py (查询使用)
```

---

## 📊 Features

| Feature | Description |
|---------|-------------|
| **Rule-based extraction** | Fast entity extraction using regex patterns |
| **AI-assisted extraction** | Optional LLM-based extraction (requires Ollama) |
| **Relationship inference** | Auto-discover implied relationships |
| **Compression** | Smart summarization for large graphs |

---

## 🔧 Usage

### Manual Build

```bash
# Build with AI (complete)
python3 libs/knowledge-graph/builder.py

# Build without AI (fast)
python3 libs/knowledge-graph/builder.py --no-ai
```

### Automated Build (Recommended)

Add to crontab for weekly auto-build:

```bash
crontab -e

# Every Saturday at 4 AM
0 4 * * 6 cd /Users/dhr/.openclaw/workspace && python3 libs/knowledge-graph/builder.py --no-ai
```

---

## 📝 Output

**File**: `memory/knowledge_graph.json`

**Structure**:
- `entities` - Dict of entities (keyed by `Type:name`)
- `relations` - List of relationships
- `updated_at` - Last build timestamp

---

## 🔗 Related

- **memory-search** - Uses knowledge graph for enhanced search
- **rag-eval** - Evaluation framework (separate library)
- **memory_hub** - Memory storage system

---

**Last Updated**: 2026-04-10  
**Version**: v2.0 (Enhanced with AI)
