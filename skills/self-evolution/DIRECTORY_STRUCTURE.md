# 自进化系统 v5.0 - 目录结构

**整理时间：** 2026-03-23  
**版本：** 5.1.0

---

## 📁 完整目录结构

```
self-evolution/
│
├── 📄 核心模块（7 个）
│   ├── main.py                    ⭐ 统一入口 CLI
│   ├── memory_stream.py           ⭐ 记忆流系统
│   ├── fractal_thinking.py        ⭐ 分形思考引擎
│   ├── nightly_cycle.py           ⭐ 夜间循环
│   ├── knowledge_base.py          ⭐ 知识库
│   ├── self_evolution_real.py     ⭐ 真实进化记录
│   └── install.py                 ⭐ 安装脚本
│
├── 📄 辅助模块（6 个）
│   ├── advanced_learning.py       高级学习
│   ├── causal_reasoning_enhanced.py 因果推理
│   ├── creative_learning_enhanced.py 创造性学习
│   ├── reinforcement_learning_enhanced.py 强化学习
│   ├── specialist_agents.py       专家 Agent
│   └── sync_to_kb.py              同步到知识库
│
├── 📄 配置文件（2 个）
│   ├── config.yaml.example        配置模板
│   └── skill.json                 技能元数据
│
├── 📄 核心文档（5 个）
│   ├── ARCHITECTURE.md            ⭐ 架构详解
│   ├── README_FINAL.md            ⭐ 功能总结
│   ├── INSTALL.md                 ⭐ 安装指南
│   ├── SETUP.md                   ⭐ 部署指南
│   └── INITIAL_SETUP.md           ⭐ 初始化配置
│
├── 📂 _archive/ (归档的历史文件 - 20 个)
│   ├── fractal_thinking_v2.py
│   ├── auto_learning_demo.py
│   ├── quick_evolve.py
│   ├── GITHUB_RESEARCH.md
│   └── ... (其他研究和旧版本文件)
│
└── 📂 __pycache__/ (Python 缓存)
```

---

## 🎯 文件分类说明

### 核心模块（必须）

| 文件 | 功能 | 行数 | 说明 |
|------|------|------|------|
| **main.py** | 统一 CLI 入口 | ~200 | 所有功能的统一入口 |
| **memory_stream.py** | 记忆流系统 | ~400 | Generative Agents 架构 |
| **fractal_thinking.py** | 分形思考引擎 | ~500 | 4 层自动分析 |
| **nightly_cycle.py** | 夜间循环 | ~400 | 4 个自动化任务 |
| **knowledge_base.py** | 知识库 | ~250 | 结构化知识存储 |
| **self_evolution_real.py** | 真实进化记录 | ~150 | 记录真实事件 |
| **install.py** | 安装脚本 | ~300 | 自动化安装 |

**使用频率：** 高  
**维护优先级：** P0

---

### 辅助模块（可选）

| 文件 | 功能 | 说明 |
|------|------|------|
| **advanced_learning.py** | 高级学习 | 复杂学习场景 |
| **causal_reasoning_enhanced.py** | 因果推理 | 因果关系分析 |
| **creative_learning_enhanced.py** | 创造性学习 | 创新思维 |
| **reinforcement_learning_enhanced.py** | 强化学习 | 奖励机制 |
| **specialist_agents.py** | 专家 Agent | 多 Agent 协作 |
| **sync_to_kb.py** | 同步到知识库 | 数据同步 |

**使用频率：** 中  
**维护优先级：** P1

---

### 配置文件

| 文件 | 用途 |
|------|------|
| **config.yaml.example** | 配置文件模板（复制为 config.yaml 使用） |
| **skill.json** | 技能元数据（名称、描述、版本） |

---

### 核心文档

| 文档 | 用途 | 读者 |
|------|------|------|
| **ARCHITECTURE.md** | 完整架构详解 | 开发者 |
| **README_FINAL.md** | 功能总结和使用指南 | 所有用户 |
| **INSTALL.md** | 安装指南 | 新用户 |
| **SETUP.md** | 部署指南 | 运维 |
| **INITIAL_SETUP.md** | 初始化配置 | 新用户 |

---

### 归档目录 (_archive/)

**包含：** 20 个历史文件

**分类：**
- **旧版本代码** (9 个)
  - fractal_thinking_v2.py
  - auto_learning_demo.py
  - auto_learning_rich.py
  - self_learning_showcase.py
  - quick_evolve.py
  - scheduled_learning.py
  - realtime_feedback.py
  - daily_reflection.py
  - knowledge_graph_expansion.py

- **研究文档** (11 个)
  - GITHUB_RESEARCH.md
  - THINKING_FRAMEWORKS_RESEARCH.md
  - INTELLIGENCE_REPORT.md
  - MULTI_AGENT_DESIGN.md
  - PATTERN_RECOGNITION_OPTIMIZATION.md
  - DUPLEX_CHECK.md
  - AUTO_RECORD_SUMMARY.md
  - AUTOMATION_SETUP.md
  - OLLAMA_SETUP.md
  - FINAL_STATUS.md
  - IMPROVEMENT_PLAN.md

**说明：** 归档文件保留历史参考，不再主动维护。需要时可以恢复。

---

## 🔄 数据流

```
📥 输入
│
├─ 进化事件 → self_evolution_real.py → evolution.db
├─ 学习记录 → advanced_learning.py → scheduled_learning_*.jsonl
└─ 用户输入 → main.py
│
├─ 记忆流处理 → memory_stream.py → memory_stream.db
├─ 分形思考 → fractal_thinking.py → 分析报告
├─ 夜间循环 → nightly_cycle.py → 整合结果
│
└─ 知识库更新 → knowledge_base.py → knowledge_base.db
     ↓
   📤 输出（报告/洞察）
```

---

## 🚀 使用指南

### 快速开始

```bash
# 1. 安装
python3 install.py

# 2. 查看状态
python3 main.py status

# 3. 运行功能
python3 main.py fractal --limit 10
python3 main.py nightly
python3 main.py memory list --limit 20
```

### 编程调用

```python
# 记忆流
from memory_stream import MemoryStream
ms = MemoryStream()
ms.add_memory("内容", memory_type='observation')

# 分形思考
from fractal_thinking import FractalThinkingEngine
engine = FractalThinkingEngine()
results = engine.process_events(limit=10)

# 夜间循环
from nightly_cycle import NightlyEvolutionCycle
cycle = NightlyEvolutionCycle()
cycle.run_full_cycle()
```

---

## 📊 代码统计

| 类别 | 文件数 | 总行数 | 平均行数 |
|------|--------|--------|----------|
| **核心模块** | 7 | ~2,200 | ~314 |
| **辅助模块** | 6 | ~4,500 | ~750 |
| **配置文件** | 2 | ~50 | ~25 |
| **核心文档** | 5 | ~2,500 | ~500 |
| **归档文件** | 20 | ~8,000 | ~400 |

**总计：** 约 17,250 行代码 + 文档

---

## 🎯 维护策略

### P0 - 核心模块
- **频率：** 每周检查
- **重点：** 稳定性、性能
- **测试：** 每次变更必测

### P1 - 辅助模块
- **频率：** 每月检查
- **重点：** 功能完整性
- **测试：** 回归测试

### P2 - 文档
- **频率：** 按需更新
- **重点：** 准确性
- **审查：** 季度审查

### P3 - 归档文件
- **频率：** 不主动维护
- **重点：** 保留参考
- **访问：** 按需查阅

---

## 📝 整理历史

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-03-23 | 首次整理 | 归档 20 个冗余文件 |
| 2026-03-23 | 创建文档 | 本文档记录结构 |

---

## 💡 最佳实践

### 文件组织
1. **核心优先** - 核心模块保持简洁
2. **功能分离** - 每个模块单一职责
3. **文档同步** - 代码变更同步更新文档

### 版本控制
1. **主干稳定** - main 分支始终保持可运行
2. **特性分支** - 新功能在特性分支开发
3. **归档历史** - 旧版本归档不删除

### 代码质量
1. **注释清晰** - 关键逻辑必须有注释
2. **类型提示** - 使用 Python 类型提示
3. **错误处理** - 完善的异常处理

---

## 🔗 相关文档

- `ARCHITECTURE.md` - 架构详解
- `README_FINAL.md` - 功能总结
- `INSTALL.md` - 安装指南
- `../../SELF_EVOLUTION_SYSTEM.md` - 体系总览
- `../../USER_MANUAL.md` - 使用手册

---

**维护者：** evo-agents  
**最后更新：** 2026-03-23  
**下次审查：** 2026-04-23
