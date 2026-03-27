# Documentation TODO | 文档待办

[English](#english) | [中文](#中文)

---

## English {#english}

### 🔴 High Priority

#### 1. Remove Duplicate Structure Documents

**Current:**
- `docs/STRUCTURE_RULES.md` (10KB) - Complete structure rules
- `docs/PROJECT_STRUCTURE_GENERIC_CN.md` (7KB) - Project structure (Chinese)
- `docs/PROJECT_STRUCTURE_GENERIC_EN.md` (7KB) - Project structure (English)

**Issue:** Content overlap, maintenance burden

**Action:**
- Keep `STRUCTURE_RULES.md` (most complete)
- Delete `PROJECT_STRUCTURE_GENERIC_*.md`
- Update references

#### 2. Clean Up Root Directory Files

**Files to remove from root:**
- `AGENTS.md` - Should be agent-specific, not in template
- `TOOLS.md` - Should be agent-specific, not in template
- `.openclaw/` - Runtime data, should be in .gitignore

**Action:**
- Move to `.github/` or delete
- Update `.gitignore`

---

### 🟡 Medium Priority

#### 3. Consolidate Agent Documentation

**Current:**
- `docs/AGENT_INSTRUCTIONS.md` (6KB) - Full instructions
- `docs/AGENT_RULES.md` (2KB) - Quick reference

**Status:** ✅ Keep both (different purposes)

**Action:**
- Add cross-references between them

#### 4. Update Architecture Documents

**Current:**
- `docs/ARCHITECTURE_GENERIC_CN.md`
- `docs/ARCHITECTURE_GENERIC_EN.md`

**Issue:** May be outdated after recent changes

**Action:**
- Review and update
- Ensure consistency with `STRUCTURE_RULES.md`

---

### 🟢 Low Priority

#### 5. Add Quick Start Guide

**Missing:** Simple 5-minute getting started guide

**Action:**
- Create `QUICKSTART.md`
- Include: Install, Add agent, Run first task

#### 6. Add Changelog

**Current:** `CHANGELOG.md` exists but may not be up to date

**Action:**
- Update with recent changes
- Add format (Keep a Changelog style)

---

## 中文 {#中文}

### 🔴 高优先级

#### 1. 删除重复的结构文档

**当前：**
- `docs/STRUCTURE_RULES.md` (10KB) - 完整结构规则
- `docs/PROJECT_STRUCTURE_GENERIC_CN.md` (7KB) - 项目结构（中文）
- `docs/PROJECT_STRUCTURE_GENERIC_EN.md` (7KB) - 项目结构（英文）

**问题：** 内容重复，维护负担

**行动：**
- 保留 `STRUCTURE_RULES.md`（最完整）
- 删除 `PROJECT_STRUCTURE_GENERIC_*.md`
- 更新引用

#### 2. 清理根目录文件

**需要删除的文件：**
- `AGENTS.md` - 应该是 Agent 特定的，不在模板中
- `TOOLS.md` - 应该是 Agent 特定的，不在模板中
- `.openclaw/` - 运行时数据，应该在 .gitignore 中

**行动：**
- 移到 `.github/` 或删除
- 更新 `.gitignore`

---

### 🟡 中优先级

#### 3. 整合 Agent 文档

**当前：**
- `docs/AGENT_INSTRUCTIONS.md` (6KB) - 完整指令
- `docs/AGENT_RULES.md` (2KB) - 快速参考

**状态：** ✅ 保留两个（不同用途）

**行动：**
- 添加相互引用

#### 4. 更新架构文档

**当前：**
- `docs/ARCHITECTURE_GENERIC_CN.md`
- `docs/ARCHITECTURE_GENERIC_EN.md`

**问题：** 最近改动后可能过时

**行动：**
- 审查并更新
- 确保与 `STRUCTURE_RULES.md` 一致

---

### 🟢 低优先级

#### 5. 添加快速入门指南

**缺失：** 简单的 5 分钟入门指南

**行动：**
- 创建 `QUICKSTART.md`
- 包含：安装、添加 Agent、运行第一个任务

#### 6. 更新更新日志

**当前：** `CHANGELOG.md` 存在但可能不是最新

**行动：**
- 用最近的更新更新
- 添加格式（Keep a Changelog 风格）

---

## 📋 Summary | 总结

| Priority | Task | Files | Status |
|----------|------|-------|--------|
| 🔴 High | Remove duplicate structure docs | PROJECT_STRUCTURE_*.md | ⏳ Pending |
| 🔴 High | Clean up root directory | AGENTS.md, TOOLS.md, .openclaw/ | ⏳ Pending |
| 🟡 Medium | Update architecture docs | ARCHITECTURE_*.md | ⏳ Pending |
| 🟡 Medium | Add cross-references | AGENT_*.md | ⏳ Pending |
| 🟢 Low | Add quick start guide | QUICKSTART.md | ⏳ Pending |
| 🟢 Low | Update changelog | CHANGELOG.md | ⏳ Pending |

---

**Next Steps:**
1. Delete `PROJECT_STRUCTURE_GENERIC_*.md`
2. Remove `AGENTS.md`, `TOOLS.md` from root
3. Update `.gitignore` for `.openclaw/`
4. Review and update architecture docs
