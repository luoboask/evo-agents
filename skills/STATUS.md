# Skills Documentation Status

> 📊 Overview of skill documentation bilingual support  
> Last updated: 2026-04-06

---

## ✅ Completed (English + Chinese)

### 1. Harness Agent
- **Location**: `skills/harness-agent/`
- **English**: [SKILL.md](./harness-agent/SKILL.md) ✅ (Default)
- **Chinese**: [SKILL_CN.md](./harness-agent/SKILL_CN.md) ✅
- **README**: [README.md](./harness-agent/README.md) ✅ (Bilingual index)
- **Status**: ✅ Complete bilingual support

---

### 2. Session Report
- **Location**: `skills/session-report/`
- **English**: [SKILL.md](./session-report/SKILL.md) ✅ (Just created)
- **Chinese**: Need to backup current and create SKILL_CN.md
- **Status**: 🔄 English done, Chinese pending

---

## ⏳ Pending (Need English Version)

### 3. Web Knowledge
- **Location**: `skills/web-knowledge/`
- **Current**: SKILL.md (Chinese only)
- **Action needed**: Create SKILL.md (English) + SKILL_CN.md (Chinese)
- **Priority**: High (frequently used)

### 4. Memory Search
- **Location**: `skills/memory-search/`
- **Current**: SKILL.md (Chinese only)
- **Action needed**: Create English version
- **Priority**: High (core memory system)

### 5. Self-Evolution
- **Location**: `skills/self-evolution/`
- **Current**: SKILL.md (Chinese only)
- **Action needed**: Create English version
- **Priority**: Medium (automated, less user-facing)

---

## 📋 Action Plan

### Phase 1: Core Skills (This Week)
- [x] Harness Agent - ✅ Complete
- [x] Session Report - ✅ English done
- [ ] Web Knowledge - TODO
- [ ] Memory Search - TODO

### Phase 2: Supporting Skills (Next Week)
- [ ] Self-Evolution
- [ ] RAG
- [ ] Knowledge Graph

### Phase 3: Documentation Sync
- [ ] Update main README with bilingual links
- [ ] Create skills index page
- [ ] Add language switcher hints

---

## 🎯 File Naming Convention

```
skill-name/
├── README.md          # Bilingual index (EN + CN)
├── SKILL.md           # English (Default)
├── SKILL_CN.md        # Chinese (Optional)
└── plugins/           # Domain plugins (if any)
```

**Rationale**:
- GitHub default audience is international → English first
- Chinese users can explicitly choose CN version
- Follows open-source best practices

---

## 💡 Quick Reference

### For Users

**English**:
```bash
# Read English docs
cat skills/harness-agent/SKILL.md

# Read Chinese docs
cat skills/harness-agent/SKILL_CN.md
```

**中文**:
```bash
# 查看英文文档
cat skills/harness-agent/SKILL.md

# 查看中文文档
cat skills/harness-agent/SKILL_CN.md
```

### For Contributors

When updating skill docs:
1. Update English version first (SKILL.md)
2. Then update Chinese version (SKILL_CN.md)
3. Mark both as "Last updated: YYYY-MM-DD"
4. Ensure consistency between versions

---

_Last updated: 2026-04-06_  
_Maintainer: evo-agents Team_
