# Knowledge Graph - Structured Memory System

> **Core Concept**: Store knowledge as entities and relationships (graph structure)  
> **Purpose**: Enable reasoning, fact verification, and structured queries  
> **Status**: ✅ Production Ready | Entity-Relationship Model | SPARQL Queries  

---

## 🚀 Quick Start

### Basic Usage

```bash
# Add entity
python3 libs/knowledge-graph/add_entity.py \
  --id "user_001" \
  --type "User" \
  --properties '{"name": "Current User", "role": "Developer"}'

# Add relationship
python3 libs/knowledge-graph/add_relation.py \
  --from "user_001" \
  --to "ts_001" \
  --type "PREFERS" \
  --properties '{"reason": "Type safety", "since": "2026-04-01"}'

# Query graph
python3 libs/knowledge-graph/query.py \
  "SELECT ?tech WHERE { user_001 :PREFERS ?tech . }"
```

### Visualize Graph

```bash
# Export to visualization format
python3 libs/knowledge-graph/export.py --format graphml > graph.graphml

# Open in Gephi or other graph visualization tools
```

---

## 🏗️ Architecture Overview

### Data Model

```
┌─────────────────────────────────────────┐
│         Knowledge Graph                  │
├─────────────────────────────────────────┤
│  Entities (Nodes)                       │
│  ┌──────────┐  ┌──────────┐            │
│  │  User    │  │ Project  │            │
│  │ (u1)     │  │ (p1)     │            │
│  └────┬─────┘  └────┬─────┘            │
│       │             │                   │
│       │ WORKS_ON    │                   │
│       └──────┬──────┘                   │
│              │                          │
│       Relationships (Edges)             │
└─────────────────────────────────────────┘
```

### Three-Layer Structure

```
Layer 1: Schema Layer (本体层)
  - Define entity types: User, Project, Technology
  - Define relationship types: PREFERS, WORKS_ON, USES
  - Define constraints and rules

Layer 2: Data Layer (数据层)
  - Actual entities: user_001, project_alpha
  - Actual relationships: user_001 → WORKS_ON → project_alpha
  - Properties and attributes

Layer 3: Application Layer (应用层)
  - Query interface (SPARQL/Cypher)
  - Reasoning engine
  - Integration with RAG system
```

---

## 📋 Core Concepts

### 1. Entity (实体)

**Definition**: Objects or concepts in the domain

**Example**:
```json
{
  "id": "user_001",
  "type": "User",
  "properties": {
    "name": "John Doe",
    "role": "Senior Developer",
    "joined_date": "2026-01-15"
  }
}
```

**Common Entity Types**:
- `User` - System users
- `Project` - Projects or tasks
- `Technology` - Programming languages, frameworks
- `Decision` - Architectural or technical decisions
- `Resource` - External resources (URLs, documents)

---

### 2. Relationship (关系)

**Definition**: Connections between entities

**Example**:
```json
{
  "from": "user_001",
  "to": "ts_001",
  "type": "PREFERS",
  "properties": {
    "reason": "Type safety",
    "confidence": 0.9,
    "since": "2026-04-01"
  }
}
```

**Common Relationship Types**:
- `PREFERS` - User preferences
- `WORKS_ON` - User-project assignments
- `USES` - Technology usage
- `DECIDED_ON` - Decision records
- `RELATED_TO` - General connections

---

### 3. Property (属性)

**Definition**: Additional information about entities or relationships

**Types**:
- **String**: `"TypeScript"`
- **Number**: `0.9` (confidence score)
- **Date**: `"2026-04-01"`
- **Boolean**: `true/false`

---

## 🔍 Query Examples

### Simple Query

**Question**: "What technologies does the user prefer?"

**SPARQL Query**:
```sparql
SELECT ?tech ?reason WHERE {
  :user_001 :PREFERS ?tech .
  ?pref :from :user_001 ;
        :to ?tech ;
        :reason ?reason .
}
```

**Result**:
```json
[
  {
    "tech": "TypeScript",
    "reason": "Type safety"
  },
  {
    "tech": "Python",
    "reason": "Data analysis"
  }
]
```

---

### Complex Query (Multi-hop)

**Question**: "Which projects use technologies the user prefers?"

**SPARQL Query**:
```sparql
SELECT ?project ?tech WHERE {
  :user_001 :PREFERS ?tech .
  ?project :USES ?tech .
}
```

**Result**:
```json
[
  {"project": "ecommerce_platform", "tech": "TypeScript"},
  {"project": "data_pipeline", "tech": "Python"}
]
```

---

### Aggregation Query

**Question**: "How many projects is the user working on?"

**SPARQL Query**:
```sparql
SELECT (COUNT(?project) AS ?count) WHERE {
  :user_001 :WORKS_ON ?project .
}
```

**Result**:
```json
{"count": 5}
```

---

## 💡 Usage Patterns

### Pattern 1: Store User Preferences

```python
# Add user
kg.add_entity(
    id="user_001",
    type="User",
    properties={"name": "Current User"}
)

# Add technology
kg.add_entity(
    id="ts_001",
    type="Technology",
    properties={"name": "TypeScript"}
)

# Add preference relationship
kg.add_relationship(
    from_entity="user_001",
    to_entity="ts_001",
    type="PREFERS",
    properties={
        "reason": "Type safety",
        "confidence": 0.9,
        "source": "session_2026-04-06"
    }
)
```

---

### Pattern 2: Track Project Dependencies

```python
# Project uses technology
kg.add_relationship(
    from_entity="project_alpha",
    to_entity="react_001",
    type="USES",
    properties={"version": "18.2", "critical": True}
)

# Project depends on another project
kg.add_relationship(
    from_entity="project_alpha",
    to_entity="project_beta",
    type="DEPENDS_ON",
    properties={"type": "API", "strength": 0.8}
)
```

---

### Pattern 3: Record Decisions

```python
# Decision entity
kg.add_entity(
    id="decision_001",
    type="Decision",
    properties={
        "title": "Choose TypeScript over JavaScript",
        "date": "2026-04-01",
        "status": "Approved"
    }
)

# Decision makers
kg.add_relationship(
    from_entity="user_001",
    to_entity="decision_001",
    type="MADE",
    properties={"role": "Lead"}
)

# Decision rationale
kg.add_relationship(
    from_entity="decision_001",
    to_entity="ts_001",
    type="CHOOSE",
    properties={"reason": "Type safety requirements"}
)
```

---

## 🔧 Advanced Features

### 1. Reasoning Engine

**Inference Rules**:
```python
# Rule: If user prefers X, and X is similar to Y, suggest Y
IF user_001 PREFERS ts_001
AND ts_001 SIMILAR_TO js_001
THEN SUGGEST user_001 js_001

# Execute inference
inferred = kg.reason(
    rule="transitive_preference",
    start_entity="user_001"
)
```

---

### 2. Path Finding

**Find connections between entities**:
```python
path = kg.find_path(
    from_entity="user_001",
    to_entity="project_gamma",
    max_depth=3
)

# Result:
# user_001 → WORKS_ON → project_alpha
# project_alpha → DEPENDS_ON → project_gamma
```

---

### 3. Community Detection

**Identify clusters**:
```python
communities = kg.detect_communities()

# Result:
# Community 1: {user_001, project_alpha, ts_001}
# Community 2: {user_002, project_beta, py_001}
```

---

### 4. Centrality Analysis

**Find important entities**:
```python
central = kg.calculate_centrality(metric="betweenness")

# Top 3 most central entities:
# 1. project_alpha (connects multiple teams)
# 2. ts_001 (used by many projects)
# 3. user_001 (works on multiple projects)
```

---

## 📊 Integration with Other Systems

### With RAG System

```
User Question: "Why did we choose TypeScript?"
    ↓
┌─────────────────────────────────────┐
│        Hybrid Retrieval             │
├─────────────────────────────────────┤
│ 1. KG Query (Facts)                 │
│    :decision_001 :CHOOSE :ts_001 .  │
│    → "Type safety requirements"     │
│                                     │
│ 2. Vector Search (Context)          │
│    "TypeScript decision discussion" │
│    → Meeting notes, chat history    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        LLM Generation               │
│ "The team chose TypeScript primarily│
│ for type safety. This decision was  │
│ made on April 1st after discussing  │
│ the need for better error catching."│
└─────────────────────────────────────┘
```

---

### With Memory-Search

```python
from memory_search import search_memory
from knowledge_graph import query_graph

# Semantic search finds relevant sessions
sessions = search_memory("TypeScript preference")

# KG provides structured facts
facts = query_graph("""
  SELECT ?tech ?reason WHERE {
    :user_001 :PREFERS ?tech .
    ?rel :reason ?reason .
  }
""")

# Combine both for comprehensive answer
answer = combine(sessions, facts)
```

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: Over-modeling

```python
# ❌ Wrong: Too many entity types
class EntityType:
    USER = "User"
    DEVELOPER = "Developer"  # Redundant!
    SENIOR_DEVELOPER = "SeniorDeveloper"  # Too specific!
    JUNIOR_DEVELOPER = "JuniorDeveloper"  # Too specific!

# ✅ Right: Use properties
entity = {
    "type": "User",
    "properties": {
        "role": "Senior Developer",
        "level": "L5"
    }
}
```

**Rule**: Keep schema simple, use properties for variations.

---

### ❌ Mistake 2: Ignoring Relationship Direction

```python
# ❌ Wrong: Ambiguous direction
kg.add_relationship(
    from_entity="user_001",
    to_entity="project_001",
    type="RELATED"  # Too vague!
)

# ✅ Right: Clear semantics
kg.add_relationship(
    from_entity="user_001",
    to_entity="project_001",
    type="WORKS_ON",  # Clear meaning
    properties={"role": "Lead", "start_date": "2026-01"}
)
```

---

### ❌ Mistake 3: Not Updating Graph

```python
# ❌ Wrong: Stale information
# User changes preference, but KG not updated

# ✅ Right: Version relationships
kg.add_relationship(
    from_entity="user_001",
    to_entity="ts_001",
    type="PREFERS",
    properties={
        "valid_from": "2026-04-01",
        "valid_until": "2026-12-31",  # Expiration
        "supersedes": "js_001"  # Link to old preference
    }
)
```

---

## 📈 Performance Optimization

### 1. Indexing

```python
# Create indexes for common queries
kg.create_index(entity_type="User", property="name")
kg.create_index(relationship_type="PREFERS", property="confidence")

# Query speed improvement: 10x faster
```

---

### 2. Caching

```python
# Cache frequent queries
@kg.cache(ttl=3600)  # 1 hour cache
def get_user_preferences(user_id):
    return kg.query(f"""
        SELECT ?tech WHERE {{
            :{user_id} :PREFERS ?tech .
        }}
    """)

# First call: Query database
# Subsequent calls: Return cached result
```

---

### 3. Partitioning

```python
# Partition by entity type
kg.partition(by="entity_type")

# Benefits:
# - Faster queries (smaller search space)
# - Better scalability
# - Easier maintenance
```

---

## 🎯 Best Practices

### ✅ Do's

1. **Start simple** - Begin with few entity types, expand gradually
2. **Use clear semantics** - Relationship names should be self-explanatory
3. **Add metadata** - Include source, confidence, timestamps
4. **Version relationships** - Track changes over time
5. **Validate input** - Check entity existence before adding relationships
6. **Document schema** - Maintain ontology documentation
7. **Backup regularly** - Export graph periodically

### ❌ Don'ts

1. **Don't over-engineer** - Avoid excessive entity types upfront
2. **Don't ignore direction** - Always define clear from/to
3. **Don't store raw text** - Use KG for structure, Vector DB for text
4. **Don't forget updates** - Keep graph current
5. **Don't mix concerns** - Separate schema from data

---

## 🔮 Future Roadmap

### v2.1 (Planned)
- [ ] GraphQL interface
- [ ] Real-time synchronization with sessions
- [ ] Automatic entity extraction from conversations

### v2.2 (Planned)
- [ ] Collaborative editing (multi-user)
- [ ] Conflict resolution
- [ ] Audit trail

### v3.0 (Vision)
- [ ] Federated knowledge graphs (cross-org)
- [ ] ML-based link prediction
- [ ] Automated schema evolution

---

_Last updated: 2026-04-06_  
_Version: 2.0 (Production Ready)_  
_Maintainer: evo-agents Team_  
_License: MIT_
