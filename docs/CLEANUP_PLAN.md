# 🧹 Workspace 清理计划

**分析时间：** 2026-03-23 19:35  
**目标：** 清理冗余内容，整理知识系统

---

## 📊 当前状态概览

### 根目录文档 (20 个文件)

| 文件 | 状态 | 建议 |
|------|------|------|
| `AGENTS.md` | ✅ 核心 | 保留 - Agent 配置指南 |
| `SOUL.md` | ✅ 核心 | 保留 - 身份定义 |
| `USER.md` | ✅ 核心 | 保留 - 用户信息 |
| `IDENTITY.md` | ✅ 核心 | 保留 - 身份元数据 |
| `MEMORY.md` | ✅ 核心 | 保留 - 长期记忆 |
| `HEARTBEAT.md` | ✅ 核心 | 保留 - 日常任务 |
| `TOOLS.md` | ✅ 核心 | 保留 - 工具笔记 |
| `BOOTSTRAP.md` | ⚠️ 过期 | 可删除 - 初始化脚本已完成 |
| `README.md` | ✅ 有用 | 保留 - 项目说明 |
| `GETTING_STARTED.md` | ✅ 有用 | 保留 - 新手指南 |
| `USER_MANUAL.md` | ✅ 有用 | 保留 - 使用手册 |
| `WORKSPACE_SETUP.md` | ⚠️ 部分过期 | 合并到 docs/ |
| `MODULE_INIT.md` | ⚠️ 部分过期 | 合并到 docs/ |
| `CONFIG_SEPARATION.md` | ⚠️ 已实现 | 归档到 docs/archive/ |
| `SECURITY_REPORT.md` | ⚠️ 一次性 | 归档到 docs/archive/ |
| `SELF_EVOLUTION_SYSTEM.md` | ⚠️ 被替代 | 删除 - 已被 v5.0 替代 |
| `IMPROVEMENT_PLAN.md` | ⚠️ 已完成 | 归档到 docs/archive/ |
| `REFACTORING_PLAN.md` | ⚠️ 已完成 | 归档到 docs/archive/ |
| `REFACTORING_PROGRESS.md` | ⚠️ 已完成 | 归档到 docs/archive/ |
| `REFACTORING_SUMMARY.md` | ✅ 有用 | 保留 - 改造总结 |

---

## 📁 Skills 目录分析

### 核心技能 (保留)

| 技能 | 状态 | 说明 |
|------|------|------|
| `memory_hub/` | ✅ 核心 | 统一记忆管理中心 |
| `memory-search/` | ✅ 核心 | 记忆搜索技能 |
| `rag/` | ✅ 核心 | RAG 评估框架 |
| `self-evolution-5.0/` | ✅ 核心 | 自进化系统 v5.0 |
| `aiway/` | ✅ 有用 | AIWay 社区集成 |
| `websearch/` | ✅ 有用 | 网页搜索技能 |

### 旧版本技能 (可删除)

| 技能 | 状态 | 建议 |
|------|------|------|
| `self-evolution/` | ⚠️ 旧版 | 删除 - 已被 v5.0 替代 |
| `rag-evaluation/` | ⚠️ 旧版 | 删除 - 已被 rag/ 替代 |
| `hybrid-memory/` | ⚠️ 废弃 | 删除 - 已被 memory_hub 替代 |
| `knowledge-graph/` | ⚠️ 未使用 | 删除 - 功能未激活 |
| `self-reflection/` | ⚠️ 废弃 | 删除 - 7 个文件共 67KB 未使用 |

### 独立脚本 (评估)

| 文件 | 大小 | 建议 |
|------|------|------|
| `sync_events.py` | 10KB | ⚠️ 检查是否在用 |
| `init_system.py` | 18KB | ✅ 保留 - 初始化脚本 |
| `separate_config.py` | 7KB | ⚠️ 已完成可归档 |
| `show_structure.py` | 7KB | ⚠️ 工具脚本可归档 |
| `quick_verify.py` | 2KB | ⚠️ 工具脚本可归档 |
| `test_all.py` | 13KB | ✅ 保留 - 集成测试 |
| `init.py` | 3KB | ⚠️ 简化版可删除 |

---

## 📚 Docs 目录分析

### 核心文档 (保留)

| 文档 | 大小 | 说明 |
|------|------|------|
| `ARCHITECTURE_v5.1.md` | 33KB | ✅ 核心架构设计 |
| `TOOL_CALLING_PRINCIPLE.md` | 20KB | ✅ 工具调用原则 |
| `ARCHITECTURE_DESIGN.md` | 18KB | ⚠️ 可能被 v5.1 替代 |
| `CLEANUP_OLD_DATA.md` | 2KB | ✅ 清理指南 |

### 建议归档

- 一次性报告
- 已过期的设计方案
- 已完成的改造计划

---

## 🗂️ Self-Evolution-5.0 内部文档

### 核心文档 (保留)

| 文档 | 状态 |
|------|------|
| `ARCHITECTURE.md` | ✅ 保留 |
| `DIRECTORY_STRUCTURE.md` | ✅ 保留 |
| `README_FINAL.md` | ✅ 保留 |
| `README_FRACTAL.md` | ✅ 保留 |
| `README_NIGHTLY.md` | ✅ 保留 |

### 可精简

| 文档 | 建议 |
|------|------|
| `INSTALL.md` + `SETUP.md` + `INITIAL_SETUP.md` | 合并为 1 个 |
| `_archive/` (12 个文件) | ✅ 已归档，可压缩 |

---

## 📦 Public 知识目录

### 当前状态

```
public/
├── common/greetings.json      ✅ 问候语
├── faq/general.json           ✅ FAQ
├── skills/memory-hub.json     ✅ 技能文档
└── domain/ai.json             ✅ AI 基础概念
```

### 建议扩充

从以下文档提取知识：
1. `MEMORY.md` → 公共知识
2. `GETTING_STARTED.md` → 使用指南
3. `USER_MANUAL.md` → FAQ
4. `REFACTORING_SUMMARY.md` → 改造历史

---

## 🎯 清理行动计划

### Phase 1: 删除明确废弃的内容

```bash
# 旧版本技能
rm -rf skills/self-evolution/
rm -rf skills/rag-evaluation/
rm -rf skills/hybrid-memory/
rm -rf skills/knowledge-graph/
rm -rf skills/self-reflection/

# 根目录过期文档
rm SELF_EVOLUTION_SYSTEM.md
rm BOOTSTRAP.md  # 已完成初始化
```

### Phase 2: 归档历史文档

```bash
# 创建归档目录
mkdir -p docs/archive/2026-03-refactoring

# 移动已完成的改造文档
mv REFACTORING_PLAN.md docs/archive/2026-03-refactoring/
mv REFACTORING_PROGRESS.md docs/archive/2026-03-refactoring/
mv CONFIG_SEPARATION.md docs/archive/2026-03-refactoring/
mv SECURITY_REPORT.md docs/archive/2026-03-refactoring/
mv IMPROVEMENT_PLAN.md docs/archive/2026-03-refactoring/
```

### Phase 3: 合并重复文档

```bash
# 合并安装文档 (self-evolution-5.0)
# INSTALL.md + SETUP.md + INITIAL_SETUP.md → SETUP_GUIDE.md
```

### Phase 4: 知识提取

从以下文档提取内容到 `public/`:
- `MEMORY.md` → `public/domain/openclaw.json`
- `GETTING_STARTED.md` → `public/skills/getting-started.json`
- `REFACTORING_SUMMARY.md` → `public/history/refactoring-2026-03.json`

---

## 📊 预期效果

### 清理前

| 类别 | 数量 | 大小 |
|------|------|------|
| 根目录文档 | 20 个 | ~150KB |
| Skills 目录 | 14 个 | ~500KB |
| 文档总数 | 50+ | ~1MB |

### 清理后

| 类别 | 数量 | 减少 |
|------|------|------|
| 根目录文档 | 12 个 | -40% |
| Skills 目录 | 6 个 | -57% |
| 文档总数 | 30+ | -40% |

---

## ⚠️ 注意事项

### 删除前确认

1. **Git 提交** - 确保所有变更已提交
2. **备份** - 重要文档先归档再删除
3. **验证** - 删除后运行测试确认功能正常

### 保留原则

- ✅ 核心架构文档
- ✅ 使用指南和手册
- ✅ 技能 SKILL.md
- ✅ 改造总结
- ⚠️ 一次性报告 → 归档
- ⚠️ 过期设计 → 归档
- ❌ 旧版本代码 → 删除

---

## 🚀 执行命令

```bash
# 1. 创建归档目录
mkdir -p docs/archive/2026-03-refactoring
mkdir -p docs/archive/old-skills

# 2. 删除旧技能
rm -rf skills/self-evolution
rm -rf skills/rag-evaluation
rm -rf skills/hybrid-memory
rm -rf skills/knowledge-graph
rm -rf skills/self-reflection

# 3. 归档历史文档
mv SELF_EVOLUTION_SYSTEM.md docs/archive/
mv BOOTSTRAP.md docs/archive/
mv REFACTORING_PLAN.md docs/archive/2026-03-refactoring/
mv REFACTORING_PROGRESS.md docs/archive/2026-03-refactoring/
mv CONFIG_SEPARATION.md docs/archive/2026-03-refactoring/
mv SECURITY_REPORT.md docs/archive/2026-03-refactoring/
mv IMPROVEMENT_PLAN.md docs/archive/2026-03-refactoring/
mv WORKSPACE_SETUP.md docs/archive/2026-03-refactoring/
mv MODULE_INIT.md docs/archive/2026-03-refactoring/

# 4. 验证
python3 scripts/test_agents.py
```

---

**维护者：** ai-baby  
**创建时间：** 2026-03-23 19:35  
**状态：** ⏳ 待执行
