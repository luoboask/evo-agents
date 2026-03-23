# 🧹 Python 代码文件清理计划

**分析时间：** 2026-03-23 19:40  
**目标：** 清理冗余代码，保留核心功能

---

## 📊 当前状态

### 根目录脚本 (6 个)

| 文件 | 大小 | 用途 | 状态 |
|------|------|------|------|
| `init.py` | 3KB | 初始化脚本 | ⚠️ 被 `init_system.py` 替代 |
| `init_system.py` | 18KB | 完整初始化 | ✅ 保留 |
| `quick_verify.py` | 2KB | 快速验证 | ⚠️ 功能重复 |
| `separate_config.py` | 7KB | 配置分离 | ✅ 已完成，可归档 |
| `show_structure.py` | 7KB | 展示结构 | ⚠️ 工具脚本 |
| `test_all.py` | 13KB | 集成测试 | ✅ 保留 |

### Scripts 目录 (2 个)

| 文件 | 大小 | 用途 | 状态 |
|------|------|------|------|
| `migrate_data.py` | 3KB | 数据迁移 | ✅ 已完成，可归档 |
| `test_agents.py` | 3KB | Agent 测试 | ✅ 保留 |

### Memory-Search 技能 (7 个)

| 文件 | 大小 | 用途 | 状态 |
|------|------|------|------|
| `search_sqlite.py` | 5KB | **主入口** | ✅ 保留 |
| `search.py` | 14KB | 旧版主入口 | ⚠️ 被替代 |
| `semantic_search.py` | 6KB | 语义搜索 | ⚠️ 功能已集成 |
| `auto_record.py` | 1KB | 自动记录 | ⚠️ 功能已集成 |
| `daily_review.py` | 4KB | 每日回顾 | ⚠️ 未使用 |
| `startup.py` | 3KB | 启动脚本 | ⚠️ 未使用 |
| `search_backup_old.py` | 2KB | 旧版备份 | ❌ 删除 |

### Self-Evolution-5.0 (14 个核心 + 9 个归档)

#### 核心模块 (保留)

| 文件 | 大小 | 用途 | 状态 |
|------|------|------|------|
| `main.py` | 9KB | **主入口** | ✅ 保留 |
| `memory_stream.py` | 7KB | **记忆流** | ✅ 保留 |
| `self_evolution_real.py` | 7KB | **进化引擎** | ✅ 保留 |
| `fractal_thinking.py` | 26KB | **分形思考** | ✅ 保留 |
| `nightly_cycle.py` | 18KB | **夜间循环** | ✅ 保留 |
| `knowledge_base.py` | 9KB | **知识库** | ✅ 保留 |
| `install.py` | 9KB | **安装脚本** | ✅ 保留 |

#### 辅助模块 (评估)

| 文件 | 大小 | 用途 | 状态 |
|------|------|------|------|
| `advanced_learning.py` | 19KB | 高级学习 | ⚠️ 未被 main.py 引用 |
| `causal_reasoning_enhanced.py` | 13KB | 因果推理 | ⚠️ 未被引用 |
| `creative_learning_enhanced.py` | 12KB | 创造性学习 | ⚠️ 未被引用 |
| `reinforcement_learning_enhanced.py` | 12KB | 强化学习 | ⚠️ 未被引用 |
| `specialist_agents.py` | 14KB | 专业 Agent | ⚠️ 未被引用 |
| `sync_to_kb.py` | 2KB | 同步知识库 | ⚠️ 未被引用 |
| `cleanup.py` | 5KB | 清理脚本 | ⚠️ 一次性 |

#### _archive/ (已归档 9 个)

```
_archive/
├── auto_learning_demo.py
├── auto_learning_rich.py
├── daily_reflection.py
├── fractal_thinking_v2.py
├── knowledge_graph_expansion.py
├── quick_evolve.py
├── realtime_feedback.py
├── scheduled_learning.py
└── self_learning_showcase.py
```

---

## 🎯 清理建议

### 立即删除 (明确废弃)

**根目录:**
- `init.py` - 被 `init_system.py` 替代
- `quick_verify.py` - 功能重复

**Memory-Search:**
- `search.py` - 被 `search_sqlite.py` 替代
- `search_backup_old.py` - 明确标注 old
- `semantic_search.py` - 功能已集成到 search_sqlite.py
- `auto_record.py` - 功能已集成
- `daily_review.py` - 未使用
- `startup.py` - 未使用

**Self-Evolution-5.0:**
- `cleanup.py` - 一次性脚本

### 归档到 _archive/ (历史参考)

**根目录:**
- `separate_config.py` - 已完成，历史参考
- `show_structure.py` - 工具脚本

**Scripts:**
- `migrate_data.py` - 已完成

**Self-Evolution-5.0 辅助模块:**
- `advanced_learning.py` - 未被引用
- `causal_reasoning_enhanced.py` - 未被引用
- `creative_learning_enhanced.py` - 未被引用
- `reinforcement_learning_enhanced.py` - 未被引用
- `specialist_agents.py` - 未被引用
- `sync_to_kb.py` - 未被引用

---

## 📊 预期效果

| 类别 | 清理前 | 清理后 | 减少 |
|------|--------|--------|------|
| **根目录脚本** | 6 个 | 3 个 | -50% |
| **Memory-Search** | 7 个 | 1 个 | -86% |
| **Self-Evolution-5.0** | 14 个 | 7 个 | -50% |
| **总代码行数** | ~250KB | ~100KB | -60% |

---

## 🚀 执行命令

```bash
# 1. 删除根目录废弃脚本
rm init.py quick_verify.py

# 2. 归档根目录工具脚本
mkdir -p docs/archive/scripts
mv separate_config.py show_structure.py docs/archive/scripts/

# 3. 删除 Memory-Search 旧代码 (保留主入口)
cd skills/memory-search
rm search.py search_backup_old.py semantic_search.py auto_record.py daily_review.py startup.py

# 4. 归档 Self-Evolution-5.0 辅助模块
cd ../self-evolution-5.0
mv advanced_learning.py causal_reasoning_enhanced.py creative_learning_enhanced.py \
   reinforcement_learning_enhanced.py specialist_agents.py sync_to_kb.py cleanup.py \
   _archive/

# 5. 归档 Scripts 目录已完成脚本
cd ../../scripts
mv migrate_data.py ../docs/archive/scripts/
```

---

## ⚠️ 验证步骤

清理后运行测试：

```bash
# 测试记忆搜索
python3 skills/memory-search/search_sqlite.py "测试" --limit 5

# 测试自进化系统
python3 skills/self-evolution-5.0/main.py status

# 测试 Agent 集成
python3 scripts/test_agents.py
```

---

## 📝 保留原则

**保留:**
- ✅ 主入口脚本 (main.py, search_sqlite.py)
- ✅ 核心功能模块
- ✅ 集成测试脚本
- ✅ 初始化脚本

**归档:**
- ⚠️ 已完成的迁移/配置脚本
- ⚠️ 未被引用的辅助模块
- ⚠️ 工具脚本

**删除:**
- ❌ 明确标注 old/backup 的文件
- ❌ 被完全替代的旧版本
- ❌ 功能重复的脚本

---

**维护者：** ai-baby  
**创建时间：** 2026-03-23 19:40  
**状态：** ⏳ 待执行
