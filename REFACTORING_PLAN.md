# ai-baby 整体改造计划

**创建时间：** 2026-03-23 17:40  
**状态：** 🚧 进行中

---

## 📊 改造进度

### Phase 1: Memory Hub ✅ 完成

- [x] 创建 memory-hub 模块
  - [x] hub.py - 核心记忆管理
  - [x] knowledge.py - 知识管理接口
  - [x] evaluation.py - 评估接口
  - [x] storage.py - 存储管理
  - [x] models.py - 数据模型
  - [x] __init__.py - 包初始化

**状态：** ✅ 完成  
**时间：** 2026-03-23

---

### Phase 2: 更新现有技能 ⏳ 进行中

- [ ] 更新 memory-search 使用 memory-hub
- [ ] 更新 rag-evaluation 使用 memory-hub
- [ ] 更新 self-evolution 使用 memory-hub
- [ ] 测试技能调用

**状态：** ⏳ 待实施  
**时间：** 2026-03-24

---

### Phase 3: 创建知识结构 ⏳ 待实施

- [ ] 创建 public/ 目录
- [ ] 创建公共知识分类
- [ ] 添加示例知识

**状态：** ⏳ 待实施  
**时间：** 2026-03-25

---

### Phase 4: 多 Agent 配置 ⏳ 待实施

- [ ] 创建 config/agents.yaml
- [ ] 创建 baby1/baby2/baby3 配置
- [ ] 在 OpenClaw 中注册 Agent
- [ ] 测试 Agent 间隔离

**状态：** ⏳ 待实施  
**时间：** 2026-03-26~30

---

## 📂 当前目录结构

```
workspace-ai-baby/
├── skills/
│   ├── memory-hub/          ✅ 新增
│   │   ├── __init__.py
│   │   ├── hub.py
│   │   ├── knowledge.py
│   │   ├── evaluation.py
│   │   ├── storage.py
│   │   └── models.py
│   ├── memory-search/       ⏳ 待更新
│   ├── rag-evaluation/      ⏳ 待更新
│   ├── self-evolution/      ⏳ 待更新
│   └── websearch/           ✅ 独立
│
├── data/                    ✅ 已存在
│   └── <agent>/
│       └── memory/
│
└── public/                  ⏳ 待创建
    ├── common/
    ├── faq/
    └── skills/
```

---

## 🎯 下一步行动

### 今天（2026-03-23）

- [x] ✅ 创建 Memory Hub 模块
- [ ] ⏳ 更新 memory-search 技能
- [ ] ⏳ 更新 rag-evaluation 技能
- [ ] ⏳ 测试 Memory Hub

### 明天（2026-03-24）

- [ ] 更新 self-evolution 技能
- [ ] 创建公共知识目录
- [ ] 编写使用文档

### 本周（2026-03-24~30）

- [ ] 多 Agent 配置
- [ ] Agent 注册
- [ ] 集成测试

---

## 📋 技能更新计划

### memory-search

**改动：**
```python
# 改动前
from skills.memory_search.search_sqlite import SQLiteMemorySearch

# 改动后
from skills.memory_hub import MemoryHub
hub = MemoryHub(agent_name='ai-baby')
hub.search(query, top_k=5)
```

**状态：** ⏳ 待实施

---

### rag-evaluation

**改动：**
```python
# 改动前
from skills.rag_evaluation.evaluate import RAGEvaluator

# 改动后
from skills.memory_hub import MemoryHub
hub = MemoryHub(agent_name='ai-baby')
hub.evaluation.record(...)
hub.evaluation.generate_report(days=7)
```

**状态：** ⏳ 待实施

---

### self-evolution

**改动：**
```python
# 改动前
from skills.self_evolution.memory_stream import MemoryStream

# 改动后
from skills.memory_hub import MemoryHub
hub = MemoryHub(agent_name='ai-baby')
hub.add(content="...", memory_type='reflection')
hub.record_evolution(event_type='...', content='...')
```

**状态：** ⏳ 待实施

---

## ✅ 完成内容

### Memory Hub 功能

| 功能 | 状态 | 说明 |
|------|------|------|
| **记忆 CRUD** | ✅ | add/search/get/delete/update |
| **知识管理** | ✅ | 公共/私有知识 |
| **评估记录** | ✅ | record/generate_report/analyze |
| **进化记录** | ✅ | record_evolution |
| **统计信息** | ✅ | stats |
| **数据模型** | ✅ | Memory/MemoryType/Knowledge |

---

## 📊 代码统计

| 模块 | 行数 | 说明 |
|------|------|------|
| **hub.py** | ~120 | 核心记忆管理 |
| **knowledge.py** | ~200 | 知识管理接口 |
| **evaluation.py** | ~180 | 评估接口 |
| **storage.py** | ~220 | 存储管理 |
| **models.py** | ~120 | 数据模型 |
| **总计** | **~840 行** | **Memory Hub 核心代码** |

---

## 🎯 成功标准

- [ ] Memory Hub 正常运行
- [ ] 所有技能改用 Memory Hub
- [ ] 知识管理正常
- [ ] 评估报告生成正常
- [ ] 多 Agent 配置完成
- [ ] 集成测试通过

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23 17:40  
**状态：** 🚧 Phase 1 完成，Phase 2 进行中
