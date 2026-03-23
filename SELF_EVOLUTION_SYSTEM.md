# ai-baby 自进化体系 v5.0

**最后更新：** 2026-03-23  
**状态：** ✅ RAG 评估系统集成完成  
**版本：** 5.1.0

---

## 🎯 体系定位

基于 **Generative Agents** 和 **TinkerClaw** 的自进化系统，融合 **AutoRAG** 评估方法，实现：

1. **记忆流** - 观察/反思/目标/知识四类记忆
2. **分形思考** - 4 层自动分析（Solve→Pattern→Correction→Meta-Rule）
3. **夜间循环** - 4 个自动化夜间任务
4. **RAG 评估** - 检索增强生成的质量监控与优化
5. **真实进化** - 停止假学习，记录真实事件

---

## 📊 完整架构 v5.1

```
┌─────────────────────────────────────────────────────────────────┐
│                    ai-baby 自进化系统 v5.1                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📥 输入层                                                      │
│  ├─ 进化事件 (evolution.db)                                     │
│  ├─ 学习记录 (scheduled_learning_*.jsonl)                       │
│  ├─ 用户对话                                                    │
│  └─ RAG 检索查询                                                 │
│                                                                 │
│  🧠 核心处理层                                                   │
│  ├─ 记忆流系统 (Memory Stream)                                  │
│  │   ├─ 观察记忆 (Observations)                                 │
│  │   ├─ 反思记忆 (Reflections)                                  │
│  │   ├─ 目标记忆 (Goals)                                        │
│  │   └─ 知识记忆 (Knowledge)                                    │
│  │                                                              │
│  ├─ 分形思考引擎 (Fractal Thinking)                             │
│  │   ├─ Level 0: Solve (解决问题)                               │
│  │   ├─ Level 1: Pattern (识别模式)                             │
│  │   ├─ Level 2: Correction (修正规则)                          │
│  │   └─ Level 3: Meta-Rule (编码元规则)                         │
│  │                                                              │
│  ├─ RAG 评估系统 (NEW! 2026-03-23)                              │
│  │   ├─ 检索记录器 (recorder.py)                                │
│  │   ├─ 评估框架 (evaluate.py)                                  │
│  │   └─ 自动调优 (auto_tune.py)                                 │
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
│  ├─ RAG 评估日志 (evaluations.jsonl)                            │
│  └─ 文档/报告                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 技能目录结构

```
skills/
├── memory-search/           # 记忆搜索（关键词 + 语义）
│   ├── search_sqlite.py     # SQLite 搜索（已集成 RAG 记录）
│   ├── semantic_search.py   # 语义搜索
│   └── daily_review.py      # 每日回顾
│
├── rag/                     # RAG 评估系统 (NEW! 2026-03-23)
│   ├── README.md            # 框架说明
│   ├── USAGE.md             # 使用指南
│   ├── INTEGRATION.md       # 集成文档
│   ├── config.json          # 配置文件
│   ├── evaluate.py          # 评估框架
│   ├── auto_tune.py         # 自动调优
│   ├── recorder.py          # 检索记录器
│   ├── test_integration.py  # 集成测试
│   └── logs/
│       └── evaluations.jsonl  # 评估日志
│
├── self-evolution-5.0/      # 自进化核心
│   ├── main.py              # 统一入口 CLI
│   ├── memory_stream.py     # 记忆流系统
│   ├── fractal_thinking.py  # 分形思考引擎
│   ├── nightly_cycle.py     # 夜间循环
│   ├── knowledge_base.py    # 知识库
│   └── [文档...]
│
├── aiway/                   # AIWay 社区集成
├── hybrid-memory/           # 混合记忆
├── knowledge-graph/         # 知识图谱
├── self-reflection/         # 自我反思
└── websearch/               # 网页搜索
```

---

## 🔄 数据流

### 对话流程
```
用户提问
    ↓
[记忆搜索] ←→ [RAG 记录器]
    ↓
[检索结果 + 相似度分数]
    ↓
[生成回复]
    ↓
[RAG 记录完成] → logs/evaluations.jsonl
```

### 进化流程
```
系统行为/用户交互
    ↓
[进化事件记录] → evolution.db
    ↓
[记忆流存储] → memory_stream.db
    ↓
[分形思考分析]
    ↓
[夜间循环处理]
    ↓
[知识库更新] → knowledge_base.db
    ↓
[报告/洞察输出]
```

### RAG 优化流程
```
日常对话检索
    ↓
[自动记录指标]
    ↓
积累 10+ 条数据
    ↓
[auto_tune.py --report]
    ↓
[分析配置表现]
    ↓
[应用最优配置]
    ↓
[持续监控]
```

---

## 📊 数据库清单

| 数据库 | 位置 | 用途 | 状态 |
|--------|------|------|------|
| `ai-baby_memory_stream.db` | `memory/` | 记忆流存储 | ✅ 活跃 (19 条) |
| `ai-baby_knowledge_base.db` | `memory/` | 知识库 | ✅ 活跃 |
| `ai-baby_knowledge_graph.json` | `memory/` | 知识图谱 | ✅ 活跃 |
| `evaluations.jsonl` | `skills/rag/logs/` | RAG 评估日志 | ✅ 新增 |
| `evolution.db` | `skills/self-evolution-5.0/` | 进化事件 | ⏳ 待激活 |

---

## 🧠 核心模块详解

### 1. 记忆搜索系统 (`memory-search/`)

**功能：** 关键词匹配 + 向量语义搜索

**核心文件：**
- `search_sqlite.py` - SQLite 搜索（已集成 RAG 记录）
- `semantic_search.py` - Ollama 向量语义搜索

**关键方法：**
```python
search(query, top_k=5, semantic=True, record_rag=True)
add(content, memory_type='knowledge', details={}, source_url=None)
```

**RAG 集成：**
- 自动记录每次检索的延迟、结果数、相似度
- 命令行支持 `--no-record` 禁用

---

### 2. RAG 评估系统 (`rag/`) - NEW!

**功能：** 基于 AutoRAG 理念的评估与优化

**核心组件：**

| 组件 | 功能 | 命令 |
|------|------|------|
| `recorder.py` | 检索记录器 | Python import |
| `evaluate.py` | 评估框架 | `--record`, `--report` |
| `auto_tune.py` | 自动调优 | `--design`, `--report`, `--next` |

**评估指标：**
- **检索质量：** Hit Rate, MRR, Precision@K
- **生成质量：** 用户反馈 (positive/neutral/negative)
- **系统性能：** 延迟 (ms), Token 消耗

**配置参数：**
```json
{
  "top_k_options": [3, 5, 10],
  "similarity_thresholds": [0.6, 0.7, 0.8],
  "chunk_sizes": [256, 512, 1024],
  "weights": {
    "accuracy": 0.6,
    "latency": 0.3,
    "cost": 0.1
  }
}
```

---

### 3. 自进化核心 (`self-evolution-5.0/`)

**功能：** 分形思考 + 夜间循环 + 记忆流

**目录结构：** (已整理 - 2026-03-23)
```
self-evolution-5.0/
├── 📄 核心模块（7 个）
│   ├── main.py                  # 统一入口 CLI
│   ├── memory_stream.py         # 记忆流系统
│   ├── fractal_thinking.py      # 分形思考引擎
│   ├── nightly_cycle.py         # 夜间循环
│   ├── knowledge_base.py        # 知识库
│   ├── self_evolution_real.py   # 真实进化记录
│   └── install.py               # 安装脚本
│
├── 📄 辅助模块（6 个）
│   ├── advanced_learning.py
│   ├── causal_reasoning_enhanced.py
│   └── ...
│
├── 📄 配置文件
│   ├── config.yaml.example
│   └── skill.json
│
├── 📄 核心文档（5 个）
│   ├── ARCHITECTURE.md
│   ├── README_FINAL.md
│   ├── INSTALL.md
│   ├── SETUP.md
│   └── INITIAL_SETUP.md
│
└── 📂 _archive/ (归档 20 个历史文件)
```

**详见：** `skills/self-evolution-5.0/DIRECTORY_STRUCTURE.md`

**分形思考 4 层：**
```
Level 0: Solve      → 问题是什么？如何解决的？
Level 1: Pattern    → 是孤立事件还是重复模式？
Level 2: Correction → 什么规则导致了问题？如何修正？
Level 3: Meta-Rule  → 如何防止类似问题再发生？
```

**夜间循环 4 任务：**
- 🍷 Wind Down - 每日复盘
- 😴 Memory Consolidation - 记忆整合 (49% 压缩目标)
- 🧹 Cleaning Lady - 上下文清理
- 🔍 Auto-Evolution - 扫描改进机会

---

## 🚀 使用指南

### 日常对话（自动 RAG 记录）

无需额外操作，RAG 记录已集成到记忆搜索：

```python
from memory_search.search_sqlite import SQLiteMemorySearch

search = SQLiteMemorySearch()
results = search.search("用户问题", top_k=5, semantic=True)
# 自动记录 RAG 指标
```

### RAG 评估

```bash
# 查看本周报告
python3 skills/rag/evaluate.py --report --days 7

# 记录一次检索
python3 skills/rag/evaluate.py --record \
  --query "测试查询" \
  --retrieved 5 \
  --latency 100 \
  --feedback positive

# 自动调优报告（需要 10+ 条数据）
python3 skills/rag/auto_tune.py --report

# 建议下一个实验
python3 skills/rag/auto_tune.py --next
```

### 自进化功能

```bash
cd skills/self-evolution-5.0

# 查看系统状态
python3 main.py status

# 运行分形思考
python3 main.py fractal --limit 10

# 运行夜间循环
python3 main.py nightly

# 查看记忆
python3 main.py memory list --limit 20

# 记录进化事件
python3 main.py evolve --type KNOWLEDGE_GAINED --content "RAG 系统集成完成"
```

### 记忆搜索

```bash
# 关键词搜索
python3 skills/memory-search/search_sqlite.py "RAG"

# 语义搜索（需要 Ollama）
python3 skills/memory-search/search_sqlite.py "优化检索" --semantic

# 添加知识
python3 skills/memory-search/search_sqlite.py --add "RAG 评估方法" \
  --type knowledge --details '{"source": "AutoRAG"}' --source "https://..."
```

---

## 📈 当前状态

### 数据统计（截至 2026-03-23 12:25）

| 类别 | 数量 | 说明 |
|------|------|------|
| **记忆总数** | 19 条 | ai-baby_memory_stream.db |
| **知识库** | 4 条 | knowledge 类型 |
| **观察** | 6 条 | observation 类型 |
| **反思** | 6 条 | reflection 类型 |
| **目标** | 3 条 | goal 类型 |
| **RAG 评估记录** | 5 条 | evaluations.jsonl |
| **进化事件** | 237 次 | 主工作区历史数据 |

### RAG 评估现状

```
总查询数：5
检索使用率：100.0%
平均延迟：100.0ms
正面反馈：66.7%
平均相似度：0.77
```

### 配置状态

```
Top-K: 5
相似度阈值：0.7
Chunk 大小：512
```

---

## 🎯 与参考项目对比

| 功能 | Generative Agents | TinkerClaw | AutoRAG | ai-baby v5.1 |
|------|-------------------|------------|---------|--------------|
| 记忆流 | ✅ | ⚠️ | ❌ | ✅ 完整 |
| 反思生成 | ✅ | ⚠️ | ❌ | ✅ 完整 |
| 分形思考 (4 层) | ❌ | ✅ | ❌ | ✅ 完整 |
| 夜间循环 | ❌ | ✅(15+) | ❌ | ✅(4 核心) |
| RAG 评估 | ❌ | ❌ | ✅ | ✅ 集成 |
| 自动调优 | ❌ | ❌ | ✅ | ✅ 实现 |
| 统一 CLI | ❌ | ❌ | ❌ | ✅ |
| 架构文档 | ❌ | ❌ | ❌ | ✅ 完整 |

**结论：** ai-baby v5.1 融合了三大系统的核心能力，形成独特的自进化体系。

---

## 📋 待办事项

### P0 - 本周
- [x] 创建 RAG 评估框架
- [x] 集成到记忆搜索
- [x] 测试验证
- [ ] 积累数据（目标：50+ 条，当前：5 条）
- [ ] 第一次配置优化（需要 10+ 条）

### P1 - 本月
- [ ] 实现用户反馈自动推断（根据对话上下文）
- [ ] 添加 RAG 可视化报告（图表展示趋势）
- [ ] 激活自进化核心（定期运行分形思考 + 夜间循环）
- [ ] 配置 Crontab 定时任务

### P2 - 下季度
- [ ] 多 Agent 协作（main-agent, sandbox-agent, tao-admin）
- [ ] 跨工作区知识共享
- [ ] 自适应阈值学习
- [ ] Web UI 界面

---

## 💡 核心原则

### 学习原则
1. **Text > Brain** 📝 - 写下来才能存活
2. **Learn → Record → Apply** - 学习闭环
3. **Demonstrate > Explain** - 展示胜过解释

### 进化原则
1. **评估驱动** - 没有度量就没有优化
2. **小步迭代** - 每次只改一个参数
3. **用户优先** - 满意度胜过指标

### 工程原则
1. **复用优先** - 避免重复造轮子
2. **文档即代码** - 详细记录设计决策
3. **自动化** - 能自动就不手动

---

## 📚 关键文档

### 体系文档
- `SELF_EVOLUTION_SYSTEM.md` - 本文档（体系总览）
- `skills/self-evolution-5.0/ARCHITECTURE.md` - 架构详解
- `skills/self-evolution-5.0/README_FINAL.md` - 功能总结

### RAG 评估文档
- `skills/rag/README.md` - 框架说明
- `skills/rag/USAGE.md` - 使用指南
- `skills/rag/INTEGRATION.md` - 集成文档

### 使用指南
- `skills/memory-search/SEARCH_USAGE.md` - 记忆搜索用法
- `HEARTBEAT.md` - 日常任务清单

---

## 🔧 配置管理

### RAG 配置 (`skills/rag/config.json`)
```json
{
  "top_k_options": [3, 5, 10],
  "similarity_thresholds": [0.6, 0.7, 0.8],
  "chunk_sizes": [256, 512, 1024],
  "weights": {
    "accuracy": 0.6,
    "latency": 0.3,
    "cost": 0.1
  },
  "current_config": {
    "top_k": 5,
    "similarity_threshold": 0.7,
    "chunk_size": 512
  }
}
```

### 自进化配置 (`skills/self-evolution-5.0/config.yaml`)
```yaml
workspace: /Users/dhr/.openclaw/workspace-ai-baby

ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text

memory:
  compress_after_days: 7
  keep_high_importance: 7.0
```

---

## 🆘 故障处理

### RAG 记录未生效
```bash
# 检查导入
python3 -c "from skills.rag.recorder import start_recording; print('OK')"

# 查看日志文件
ls -la skills/rag/logs/evaluations.jsonl
```

### 记忆搜索失败
```bash
# 检查数据库
ls -la memory/ai-baby_memory_stream.db

# 测试搜索
python3 skills/memory-search/search_sqlite.py "测试" --stats
```

### 自进化功能异常
```bash
# 检查状态
cd skills/self-evolution-5.0 && python3 main.py status

# 查看日志
tail -20 /tmp/nightly.log
```

---

## 📊 演进历史

| 版本 | 日期 | 关键变更 |
|------|------|----------|
| v5.0 | 2026-03-17 | 自进化系统核心完成 |
| v5.0.1 | 2026-03-18 | 多 Agent 数据隔离 |
| v5.1 | 2026-03-23 | RAG 评估系统集成 |
| v5.1.1 | 2026-03-23 | 集成测试通过 |

---

## 🎉 总结

**ai-baby 自进化体系 v5.1 核心功能已完成！**

- ✅ 记忆流系统（Generative Agents 启发）
- ✅ 分形思考引擎（TinkerClaw 核心）
- ✅ 夜间进化循环（TinkerClaw 启发）
- ✅ RAG 评估系统（AutoRAG 理念）
- ✅ 向量语义搜索（Ollama 集成）
- ✅ 统一 CLI 入口
- ✅ 完整架构文档

**系统已可投入使用，当前重点是积累 RAG 评估数据，为第一次自动优化做准备。**

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23  
**许可证：** MIT  
**社区：** AIWay (https://aiway.alibaba-inc.com)
