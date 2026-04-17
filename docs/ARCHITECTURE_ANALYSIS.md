# 现有记忆、知识、进化体系全面分析

**分析时间**: 2026-04-17  
**目的**: 为专家 Agent 架构转型做准备

---

## 【一】记忆体系 (Memory Stream)

### 1.1 架构

```
libs/memory_hub/
├── hub.py              # 记忆中心（统一入口）
├── storage.py          # 记忆存储（SQLite）
├── session_storage.py  # 会话记忆（独立表）
├── knowledge.py        # 知识管理接口
├── evaluation.py       # RAG 评估接口
├── embedding_cache.py  # Embedding 缓存
└── models.py           # 数据模型
```

### 1.2 核心功能

**MemoryHub 类** (`hub.py`):
```python
hub = MemoryHub(agent_name="python-expert")

# 添加记忆
hub.add(
    content="asyncio 是 Python 的异步 IO 库",
    memory_type="observation",  # observation/reflection/goal/knowledge
    importance=0.8,
    tags=["asyncio", "Python"],
    metadata={"source": "web-crawl"}
)

# 搜索记忆
results = hub.search(
    query="异步编程",
    top_k=5,
    memory_type="knowledge",
    semantic=True,  # 语义搜索
    hierarchical=True  # 分层搜索（月→周→日）
)
```

### 1.3 数据库结构

**路径**: `data/<agent_name>/memory/`

| 数据库 | 用途 | 表 |
|--------|------|-----|
| `memory_stream.db` | 记忆流 | memories, memory_tags |
| `sessions.db` | 会话记忆 | sessions, session_memories |
| `knowledge_base.db` | 知识库 | knowledge, knowledge_tags |

### 1.4 优势
- ✅ 统一的 MemoryHub 接口
- ✅ 支持语义搜索（Ollama embedding）
- ✅ 分层搜索（月→周→日）
- ✅ Embedding 缓存机制
- ✅ 多 Agent 数据隔离

### 1.5 不足
- ❌ 记忆类型扁平（只有 observation/reflection/goal/knowledge）
- ❌ 缺少领域知识分类（概念/实践/案例）
- ❌ 知识之间无关联（无图谱）
- ❌ 质量评估缺失（无评分）

---

## 【二】知识体系 (Knowledge Base)

### 2.1 架构

```
知识管理 (knowledge.py):
├── 公共知识 (workspace/public/)
│   └── <category>/<id>.json
└── 私有知识 (data/<agent>/knowledge/private/)
    └── <category>/<id>.json
```

### 2.2 知识模型

```json
{
  "id": "uuid",
  "title": "标题",
  "content": "内容",
  "category": "分类",
  "tags": ["标签 1", "标签 2"],
  "is_public": false,
  "created_at": "ISO 时间",
  "updated_at": "ISO 时间"
}
```

### 2.3 核心功能

```python
# 添加知识
knowledge_id = hub.knowledge.add(
    content="asyncio 最佳实践...",
    title="Python 异步编程最佳实践",
    category="best_practices",
    tags=["asyncio", "Python", "性能"],
    is_public=False
)

# 搜索知识
results = hub.knowledge.search(
    query="异步",
    category="best_practices",
    tags=["Python"],
    include_public=True,
    include_private=True,
    limit=10
)
```

### 2.4 优势
- ✅ 公共/私有知识分离
- ✅ 分类管理
- ✅ JSON 格式，易读易编辑
- ✅ 自动关联记忆流

### 2.5 不足
- ❌ 分类是扁平的（无层级）
- ❌ 知识之间无关联
- ❌ 缺少质量评分
- ❌ 缺少时效性管理

---

## 【三】进化体系 (Evolution System v2.0)

### 3.1 架构

```
skills/self-evolution/
├── effect_tracker.py      # 效果追踪
├── solution_reuse.py      # 方案复用
├── embedding_cache.py     # Embedding 缓存
├── auto_strategy.py       # 自动策略
├── gene_evolution.py      # Gene 进化
├── meta_learning.py       # 元学习
└── self_evolution_real.py # 主入口
```

### 3.2 核心模块

#### EffectTracker (`effect_tracker.py`)
```python
tracker = EffectTracker()

# 记录方案
tracker.record_solution(
    problem="API 超时",
    problem_type="技术问题",
    solution="增加重试机制",
    gene_used="repair_from_errors"
)

# 标记效果
tracker.mark_solution_effect(
    problem="API 超时",
    success=True,
    feedback="解决了问题"
)

# 获取统计
stats = tracker.get_stats("技术问题")
# {'total': 10, 'success': 8, 'failure': 2, 'success_rate': 0.8}
```

#### SolutionReuse (`solution_reuse.py`)
```python
reuse = SolutionReuse()

# 解决问题（优先复用）
solution, source = reuse.solve_with_reuse(
    problem="API 超时",
    problem_type="技术问题",
    solve_func=lambda p: "思考新方案..."
)

# source: 'reused' 或 'new'
```

### 3.3 数据库结构

**路径**: `skills/self-evolution/evolution_effects.db`

| 表 | 用途 |
|----|------|
| `solutions` | 解决方案（问题哈希、方案内容、成功率） |
| `usage_records` | 使用记录（时间、成功/失败、反馈） |
| `strategy_switches` | 策略切换记录 |

### 3.4 优势
- ✅ 效果追踪完整（成功/失败统计）
- ✅ 语义级方案复用（embedding 相似度）
- ✅ Embedding 缓存（15000 倍性能提升）
- ✅ 自动策略切换（4 种策略）
- ✅ Gene 进化分析

### 3.5 不足
- ❌ 与记忆体系分离（独立数据库）
- ❌ 与知识体系分离（无关联）
- ❌ 缺少领域分类（只有 problem_type）
- ❌ 质量评估维度单一（只有成功/失败）

---

## 【四】三体系关系图

```
当前架构:

┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Memory Hub    │      │  Knowledge DB   │      │  Evolution DB   │
│                 │      │                 │      │                 │
│ memory_stream   │      │ knowledge.json  │      │ solutions       │
│ sessions        │      │ (JSON files)    │      │ usage_records   │
│ knowledge_base  │      │                 │      │                 │
│                 │      │                 │      │                 │
│ 独立 SQLite     │      │ 文件系统        │      │ 独立 SQLite     │
└─────────────────┘      └─────────────────┘      └─────────────────┘
       ↓                        ↓                        ↓
   无直接关联              无直接关联              无直接关联

问题:
1. 三个体系独立，数据不互通
2. 知识无法指导进化
3. 进化无法反哺知识
4. 记忆流成了"日志"，不是"智慧"
```

---

## 【五】专家 Agent 架构改造建议

### 5.1 统一索引层

```
新增: scripts/domain/unified_index.py

功能:
- 统一的 knowledge_id 贯穿三库
- 知识更新时自动触发记忆更新
- 进化事件自动关联相关知识
```

### 5.2 领域知识模型

```
新增: scripts/domain/domain_knowledge_schema.py

结构化领域知识:
├─ concepts (核心概念)
│   ├─ id, title, definition, related_concepts
├─ best_practices (最佳实践)
│   ├─ id, title, steps, success_rate, tags
├─ faq (常见问题)
│   ├─ id, question, answer, difficulty, tags
├─ code_samples (案例代码)
│   ├─ id, title, code, explanation, tags
└─ relationships (概念关系)
    ├─ from_concept, to_concept, relation_type
```

### 5.3 质量评估体系

```
新增: scripts/domain/knowledge_quality_scorer.py

多维度评分:
- 方案成功率 (40%) - 来自 effect_tracker
- 用户满意度 (20%) - 反馈评分
- 知识时效性 (15%) - 发布时间
- 来源权威性 (15%) - 网站权重
- 内容完整性 (10%) - 覆盖度

综合质量分 = Σ(维度分 × 权重)
```

### 5.4 专家决策流程

```
新增: scripts/domain/expert_solver.py

流程:
1. 问题分类 (属于哪个子领域？)
2. 方案检索 (语义搜索 + 质量排序)
3. 方案评估 (成功率 + 时效性)
4. 方案生成 (复用 or 创新？)
5. 效果追踪 (记录反馈)
6. 知识沉淀 (成功案例入库)
```

---

## 【六】实施优先级

| 优先级 | 改造 | 工作量 | 影响 |
|--------|------|--------|------|
| P0 | crawl.py --agent 集成 | 0.5 天 | 高 |
| P0 | domain_knowledge_schema.py | 1 天 | 高 |
| P1 | unified_index.py | 1 天 | 中 |
| P1 | knowledge_quality_scorer.py | 0.5 天 | 中 |
| P2 | expert_solver.py | 1.5 天 | 高 |

---

## 【七】总结

### 现有体系优势
- ✅ MemoryHub 统一接口
- ✅ 语义搜索能力
- ✅ 进化追踪完整
- ✅ 多 Agent 隔离

### 现有体系不足
- ❌ 三库独立，数据不互通
- ❌ 知识扁平，无结构化
- ❌ 质量评估缺失
- ❌ 缺少主动学习机制

### 转型方向
从"工具集合" → "智能体"
- 知识结构化（领域知识模型）
- 三库联动（统一索引）
- 质量评估（多维度评分）
- 主动学习（知识空白检测）
- 专家决策（完整流程）

---

**下一步**: 开始 P0 改造（crawl.py --agent 集成 + domain_knowledge_schema.py）
