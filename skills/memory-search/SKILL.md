---
name: memory-search
description: 'Hybrid memory system with 3-layer architecture: working memory + vector memory + knowledge graph. Auto-records and retrieves context.'
---

# Memory Search Skill (Hybrid v2)

三层混合记忆系统，自动记录和智能检索。

## Architecture

```
┌─────────────────────────────────────────┐
│         三层混合记忆系统                 │
├─────────────────────────────────────────┤
│ L3: Knowledge Graph (长期)              │
│     - 实体关系网络                       │
│     - 结构化知识                         │
├─────────────────────────────────────────┤
│ L2: Vector Memory (语义)                │
│     - Ollama 嵌入                        │
│     - 语义相似度检索                     │
├─────────────────────────────────────────┤
│ L1: Working Memory (短期)               │
│     - 最近50条交互                       │
│     - 关键词匹配                         │
└─────────────────────────────────────────┘
```

## Features

- ✅ **自动记录** - 智能评估重要性，自动分发到三层
- ✅ **语义检索** - 理解意图，不只是关键词匹配
- ✅ **混合搜索** - 三层联合检索，综合排序
- ✅ **智能评估** - critical/high/medium/low 自动分级
- ✅ **持久化** - 自动保存到文件

## Usage

### 记录记忆

```python
from integrated_memory import IntegratedHybridMemory

memory = IntegratedHybridMemory()

# 自动记录（评估重要性）
memory.record_interaction("user", "用户说的话")
memory.record_interaction("assistant", "AI的回复")
```

### 搜索记忆

```python
# 混合检索
results = memory.search("查询内容", context="medium")

# context: small (L1) / medium (L1+L2) / large (L1+L2+L3)
```

### 命令行

```bash
# 记录
python3 search.py --record "内容" --role user

# 搜索
python3 search.py "查询内容"

# 统计
python3 search.py --stats
```

## Importance Levels

自动评估：
- **critical** - 规则、决策、敏感信息
- **high** - 偏好、习惯、技能
- **medium** - 一般信息
- **low** - 简短对话

## Evolution

- v1: Basic keyword search
- v2: Hybrid 3-layer memory with semantic search (2026-03-16)
