# 去重优化检查清单

**日期：** 2026-03-17  
**目标：** 确保不自相重复，复用现有功能

---

## ✅ 已识别并解决的重复

### 1. 多个版本并存 ❌ → ✅

**问题：**
- `self-evolution-2.0/`
- `self-evolution-3.0/`
- `self-evolution-4.0/`
- `self-evolution/`

**解决：**
- ✅ 统一使用 v5.0
- ✅ 旧版本保留但不维护
- ✅ 文档明确说明

---

### 2. Embedding 模块重复 ❌ → ✅

**问题：**
- `memory-search/semantic_search.py` 已有 Ollama embedding
- `self-evolution/embedding.py` 又实现了一遍

**解决：**
- ✅ 删除 `embedding.py`
- ✅ 直接复用 `memory-search/semantic_search.py`
- ✅ 代码导入：`from semantic_search import get_embedding, cosine_similarity`

**复用关系：**
```
self-evolution/fractal_thinking.py
    ↓ imports
memory-search/semantic_search.py
    ↓ uses
Ollama API (nomic-embed-text)
```

---

### 3. 假学习 vs 真学习 ❌ → ✅

**问题：**
- `auto_learning_rich.py` 生成假学习数据
- `self_evolution_real.py` 记录真实事件

**解决：**
- ✅ 重写 `auto_learning_rich.py` 为真实学习记录器
- ✅ 停止自动生成假数据
- ✅ 只记录真实输入和任务执行结果

---

### 4. 记忆存储重复 ❌ → ✅

**问题：**
- `knowledge_base.db` 存储知识
- `memory_stream.db` 也存储记忆
- 两者功能重叠

**解决：**
- ✅ 明确分工：
  - `knowledge_base.db` - 结构化知识（领域/主题/内容）
  - `memory_stream.db` - 认知记忆（观察/反思/目标）
- ✅ 双向同步：反思同时写入两个库

---

### 5. 模式识别算法 ❌ → ✅

**问题：**
- 简单关键词匹配（容易漏检）
- 语义相似度（更准确）
- 两种实现并存

**解决：**
- ✅ 统一使用语义相似度
- ✅ 降级方案：Ollama 不可用时用 Jaccard
- ✅ 单一实现：`_calculate_text_similarity()`

---

## 📊 复用关系图

```
自进化系统 v5.0
│
├─ 复用 memory-search
│   ├─ semantic_search.py → Ollama embedding
│   └─ search.py → 向量检索
│
├─ 复用 evolution-workbench
│   └─ evolution.db → 进化事件存储
│
└─ 自研模块
    ├─ memory_stream.py (Generative Agents 启发)
    ├─ fractal_thinking.py (TinkerClaw 启发)
    ├─ nightly_cycle.py (TinkerClaw 启发)
    └─ main.py (统一 CLI)
```

---

## 🔍 当前依赖关系

### 外部依赖
| 模块 | 用途 | 位置 |
|------|------|------|
| `memory-search/semantic_search` | Ollama embedding | ✅ 复用 |
| `memory-search/search` | 向量检索 | ✅ 复用 |
| `evolution-workbench/evolution.db` | 事件存储 | ✅ 复用 |

### 内部模块
| 模块 | 依赖 | 状态 |
|------|------|------|
| `main.py` | 所有模块 | ✅ 统一入口 |
| `fractal_thinking.py` | memory_stream, semantic_search | ✅ |
| `nightly_cycle.py` | memory_stream, evolution | ✅ |
| `memory_stream.py` | SQLite | ✅ |
| `self_evolution_real.py` | SQLite | ✅ |

---

## 📋 去重检查清单

- [x] 无重复的 embedding 实现
- [x] 无重复的记忆存储
- [x] 无冲突的版本号
- [x] 统一的 CLI 入口
- [x] 清晰的模块分工
- [x] 文档明确说明复用关系
- [x] 删除冗余代码

---

## 🎯 原则

1. **复用优先** - 已有功能不再造轮子
2. **单一职责** - 每个模块只做一件事
3. **明确分工** - 文档说明谁负责什么
4. **降级策略** - 外部依赖不可用时有备选

---

## 📝 未来注意事项

### 新增功能前检查
1. [ ] memory-search 是否已有类似功能？
2. [ ] evolution-workbench 是否能复用？
3. [ ] 是否会与现有模块职责重叠？

### 维护原则
1. [ ] 优先修复现有代码，而非新增
2. [ ] 如需新增，先文档化职责边界
3. [ ] 定期（每月）检查重复

---

## ✅ 结论

**自进化系统 v5.0 已完成去重优化：**
- ✅ Embedding 复用 memory-search
- ✅ 事件存储复用 evolution-workbench
- ✅ 停止假学习，统一真实记录
- ✅ 单一 CLI 入口管理所有功能

**系统现在更加简洁、可维护！**
