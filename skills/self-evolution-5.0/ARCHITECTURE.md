# 自进化系统架构 v5.0

**最后更新：** 2026-03-17  
**参考项目：** Generative Agents, TinkerClaw, AutoGen

---

## 📊 系统全景图

```
┌─────────────────────────────────────────────────────────────────┐
│                    自进化系统 v5.0                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📥 输入层                                                      │
│  ├─ 进化事件 (evolution_events.db)                              │
│  ├─ 学习记录 (scheduled_learning_*.jsonl)                       │
│  └─ 用户输入                                                    │
│                                                                 │
│  🧠 核心处理层                                                   │
│  ├─ 记忆流系统 (Memory Stream)                                  │
│  │   ├─ 观察记忆 (Observations)                                 │
│  │   ├─ 反思记忆 (Reflections)                                  │
│  │   └─ 目标记忆 (Goals)                                        │
│  │                                                              │
│  ├─ 分形思考引擎 (Fractal Thinking)                             │
│  │   ├─ Level 0: Solve (解决问题)                               │
│  │   ├─ Level 1: Pattern (识别模式)                             │
│  │   ├─ Level 2: Correction (修正规则)                          │
│  │   └─ Level 3: Meta-Rule (编码元规则)                         │
│  │                                                              │
│  └─ 夜间进化循环 (Nightly Cycle)                                │
│      ├─ 🍷 Wind Down (每日复盘)                                 │
│      ├─ 😴 Memory Consolidation (记忆整合)                      │
│      ├─ 🧹 Cleaning Lady (上下文清理)                           │
│      └─ 🔍 Auto-Evolution (自动进化)                            │
│                                                                 │
│  📤 输出层                                                      │
│  ├─ 知识库 (knowledge_base.db)                                  │
│  ├─ 记忆流 (memory_stream.db)                                   │
│  ├─ 进化事件 (evolution.db)                                     │
│  └─ 文档/报告                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 核心模块

### 1. 记忆流系统 (`memory_stream.py`)

**功能：** 基于 Generative Agents 的记忆架构

**核心类：**
- `Memory` - 记忆数据类
- `MemoryStream` - 记忆流管理

**关键方法：**
```python
add_memory(content, memory_type, importance, tags)
get_memories(memory_type, limit, recent_hours)
retrieve_by_relevance(query, limit)  # 近因性 + 重要性 + 相关性
generate_reflections(lookback_hours, min_memories)
```

**数据库：** `memory/memory_stream.db`

---

### 2. 分形思考引擎 (`fractal_thinking.py`)

**功能：** 4 层自动分析（TinkerClaw 核心）

**核心类：**
- `FractalAnalysis` - 分析结果数据类
- `FractalThinkingEngine` - 分形思考引擎

**4 层分析：**
```
Level 0: Solve      → 问题是什么？如何解决的？
Level 1: Pattern    → 是孤立事件还是重复模式？
Level 2: Correction → 什么规则导致了问题？如何修正？
Level 3: Meta-Rule  → 如何防止类似问题再发生？
```

**模式识别：**
- recurring_bug (重复 Bug)
- feature_bloat (功能膨胀)
- learning_gap (知识空白)
- code_improvement (技术债务)
- system_evolution (系统进化)

**Embedding 支持：**
- 优先使用 Ollama nomic-embed-text
- 降级到本地 TF-IDF 算法

---

### 3. 夜间进化循环 (`nightly_cycle.py`)

**功能：** 自动化夜间任务（TinkerClaw 启发）

**核心类：**
- `NightlyEvolutionCycle` - 夜间循环管理

**4 个任务：**

| 任务 | 功能 | 频率 |
|------|------|------|
| 🍷 Wind Down | 每日复盘，生成洞察 | 每日 |
| 😴 Memory Consolidation | 记忆整合，49% 压缩 | 每日 |
| 🧹 Cleaning Lady | 清理临时文件 | 每日 |
| 🔍 Auto-Evolution | 扫描改进机会 | 每日 |

**配置：**
```python
config = {
    'memory_consolidation': {
        'compress_after_days': 7,
        'keep_high_importance': 7.0,
        'target_compression_rate': 0.49
    },
    'cleaning': {
        'max_learning_files': 30,
        'max_log_size_mb': 100
    }
}
```

---

### 4. 真实进化记录 (`self_evolution_real.py`)

**功能：** 记录真实的进化事件（停止假学习）

**核心类：**
- `RealSelfEvolution` - 进化记录管理

**事件类型：**
- BUG_FIX - Bug 修复
- FEATURE_ADDED - 功能新增
- CODE_IMPROVED - 代码优化
- KNOWLEDGE_GAINED - 知识获取
- EVOLUTION_CHECK - 进化检查

**数据库：** `evolution-workbench/evolution.db`

---

### 5. 知识库系统 (`knowledge_base.py`)

**功能：** 结构化知识存储

**核心类：**
- `KnowledgeBase` - 知识库管理

**表结构：**
```sql
knowledge (
    id, timestamp, domain, subtopic,
    content, insight, thinking, key_point,
    difficulty, time_spent, learning_type, outcome
)
```

**数据库：** `memory/knowledge_base.db`

---

### 6. Embedding 模块（复用 `memory-search/semantic_search.py`）

**功能：** 语义相似度计算

**核心函数：**
- `get_embedding(text)` - 获取 Ollama embedding
- `cosine_similarity(a, b)` - 余弦相似度计算

**特性：**
- 使用 Ollama nomic-embed-text 模型
- 已存在于 `memory-search` 技能
- 直接复用，避免重复造轮子

**位置：** `../memory-search/semantic_search.py`

---

## 🔄 数据流

```
用户/系统行为
    ↓
[进化事件记录]
    ↓
[记忆流存储] ←→ [Embedding 计算]
    ↓
[分形思考分析]
    ↓
[夜间循环处理]
    ↓
[知识库更新]
    ↓
[报告/洞察输出]
```

---

## 📊 数据库清单

| 数据库 | 位置 | 用途 |
|--------|------|------|
| `memory_stream.db` | `memory/` | 记忆流存储 |
| `knowledge_base.db` | `memory/` | 知识库 |
| `evolution.db` | `skills/evolution-workbench/` | 进化事件 |
| `embedding_cache.pkl` | `memory/` | Embedding 缓存 |

---

## 🚀 使用指南

### 快速开始

```bash
cd /Users/dhr/.openclaw/workspace/skills/self-evolution-5.0

# 1. 运行分形思考
python3 fractal_thinking.py

# 2. 运行夜间循环
python3 nightly_cycle.py

# 3. 测试 Embedding
python3 embedding.py

# 4. 测试记忆流
python3 memory_stream.py
```

### 编程调用

```python
from fractal_thinking import FractalThinkingEngine
from nightly_cycle import NightlyEvolutionCycle
from memory_stream import MemoryStream

# 分形思考
engine = FractalThinkingEngine()
results = engine.process_events(limit=10)

# 夜间循环
cycle = NightlyEvolutionCycle()
cycle.run_full_cycle()

# 记忆流
ms = MemoryStream()
ms.add_memory("内容", memory_type='observation')
```

### 定时任务配置

```bash
# Crontab 配置（每天凌晨 2 点）
0 2 * * * cd /workspace/skills/self-evolution-5.0 && python3 nightly_cycle.py

# 每 4 小时运行分形分析
0 */4 * * * cd /workspace/skills/self-evolution-5.0 && python3 fractal_thinking.py
```

---

## 📈 效果指标

| 指标 | 当前值 | 目标 |
|------|--------|------|
| 记忆总数 | 28 条 | 持续增长 |
| 进化事件 | 240+ 次 | 持续增长 |
| 检测模式 | 4 个 | 5-10 个 |
| 生成元规则 | 2 个 | 持续增长 |
| 夜间循环 | 4 个任务 | 15+ 任务 |
| 压缩率 | 0% | 49% |

---

## 🔧 配置管理

所有配置文件集中在 `config/` 目录（待创建）：

```yaml
# config/settings.yaml
embedding:
  model: nomic-embed-text
  ollama_url: http://localhost:11434
  use_cache: true

memory:
  compress_after_days: 7
  keep_high_importance: 7.0

patterns:
  recurring_bug_threshold: 2
  feature_bloat_threshold: 3
  min_similarity: 0.35
```

---

## 🎯 与参考项目对比

| 功能 | Generative Agents | TinkerClaw | 我们的实现 |
|------|-------------------|------------|-----------|
| 记忆流 | ✅ | ⚠️ 简化版 | ✅ 完整实现 |
| 反思生成 | ✅ | ⚠️ 简化版 | ✅ 完整实现 |
| 分形思考 | ❌ | ✅ | ✅ 完整实现 |
| 夜间循环 | ❌ | ✅ | ✅ 4 个核心任务 |
| Embedding | ✅ | ❌ | ✅ (支持 Ollama) |
| 晨间简报 | ❌ | ✅ | ⏳ 待实现 |
| 多 Agent | ❌ | ❌ | ⏳ 待实现 |

---

## 📝 待办事项

### 短期 (本周)
- [ ] 创建统一配置文件
- [ ] 添加日志系统
- [ ] 优化 Embedding 算法
- [ ] 添加单元测试

### 中期 (本月)
- [ ] 实现晨间简报
- [ ] 集成 Ollama embedding
- [ ] 添加 Web UI
- [ ] 部署定时任务

### 长期 (下季度)
- [ ] 多 Agent 协作
- [ ] 自适应阈值学习
- [ ] 模式演化追踪
- [ ] 跨项目知识共享

---

## 📚 参考资料

1. **Generative Agents 论文**: https://arxiv.org/abs/2304.03442
2. **TinkerClaw**: https://github.com/globalcaos/tinkerclaw
3. **Ollama Embeddings**: https://ollama.com/library/nomic-embed-text
4. **ENGRAM 论文** (记忆压缩): 待补充

---

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交 PR
4. 通过代码审查

**代码风格：** PEP 8  
**测试：** 运行 `python3 -m pytest tests/`  
**文档：** 更新对应的 README
