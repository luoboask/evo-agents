# Harness Agent - AI Task Execution Framework

> 🌍 **Default: English** | 中文版本可用  
> 📦 Production-Ready Multi-Agent Orchestration System  
> ⚡ Auto-Detect Domain | Three-Role Closed Loop | Quality Assurance

---

## 🚀 Quick Start

```bash
# Auto-detect domain & execute
/harness-agent "Develop a Todo List app with React + localStorage"

# Specify domain
/harness-agent "Analyze Q1 sales data" --domain data-analysis

# Preview mode (see plan without execution)
/harness-agent "Refactor payment module" --dry-run

# With parallelism
/harness-agent "Build e-commerce website" --parallelism 4
```

---

## 📖 Documentation

### English (Default)
- **[SKILL.md](./SKILL.md)** - Complete English documentation
  - Architecture & Core Concepts
  - Usage Examples (Programming/Data Analysis/Marketing)
  - Domain Plugins System
  - Best Practices & Troubleshooting

### 中文 (Chinese Version)
- **[SKILL_CN.md](./SKILL_CN.md)** - 完整中文文档
  - 架构与核心概念
  - 使用示例（编程/数据分析/营销）
  - 领域插件系统
  - 最佳实践与故障排查

---

## 🎯 When to Use Harness

### ✅ Recommended

| Scenario | Example | Expected Time |
|----------|---------|---------------|
| **Complex System** | E-commerce site, CRM, Blog platform | 5-30 hours |
| **Large Refactoring** | Microservices migration, Codebase reorg | 10-50 hours |
| **Cross-Domain** | Data analysis + Visualization + Report | 3-15 hours |
| **Long-Term Project** | Multi-phase development | Days to weeks |

### ❌ Not Recommended

| Scenario | Better Alternative |
|----------|-------------------|
| Simple task (<1 hour) | Normal conversation |
| Urgent request (<5 min) | Direct implementation |
| Exploratory task | Free-form discussion |

---

## 🏗️ Core Architecture

```
┌──────────────────────────────────────┐
│         Harness Agent System          │
├──────────────────────────────────────┤
│  ┌─────────────┐                     │
│  │  Planner    │ → Analyze & Plan   │
│  └──────┬──────┘                     │
│         │                             │
│         ▼                             │
│  ┌─────────────┐                     │
│  │  Executor   │ → Execute Tasks    │
│  └──────┬──────┘                     │
│         │                             │
│         ▼                             │
│  ┌─────────────┐                     │
│  │  Evaluator  │ → QA & Deliver     │
│  └─────────────┘                     │
│                                       │
│  ✅ Pass → Deliver                   │
│  ❌ Fail → Iterate                   │
└──────────────────────────────────────┘
```

**Key Features**:
- ✅ Three-role closed loop (Planner → Executor → Evaluator)
- ✅ Automatic domain detection (100% accuracy)
- ✅ Progress tracking with auto-save
- ✅ Quality scoring system (≥70 to pass)
- ✅ Context reset mechanism
- ✅ Domain-specific plugins

---

## 📦 Available Domain Plugins

| Plugin | Description | Language |
|--------|-------------|----------|
| **programming** | Software development (Web/Mobile/Backend) | EN/CN |
| **data-analysis** | Data analysis, BI reports, Statistics | EN/CN |
| **content-creation** | Articles, Video scripts, Social media | EN/CN |
| **ecommerce-operations** | E-commerce dev & operations | EN/CN |
| **self-media-content** | Self-media content creation | CN |

**Custom Plugins**: Supported! Create your own domain plugin.

---

## 💡 Usage Examples

### Example 1: Programming Task

```bash
/harness-agent "Develop a blog system with article publishing, comments, and tags" \
  --domain programming \
  --parallelism 3
```

**Expected Flow**:
```
📋 Planner: Database → API → Frontend → Testing
🔨 Executors (parallel): Team A/B/C
✅ Evaluator: Tests + Code review
📁 Deliverables: Complete codebase + docs
```

### Example 2: Data Analysis

```bash
/harness-agent "Analyze Q1 sales decline reasons and propose improvements" \
  --domain data-analysis
```

**Expected Output**:
- Analysis report with charts
- Root cause identification
- Actionable recommendations

### Example 3: Marketing Campaign

```bash
/harness-agent "Plan product launch with 50k budget, targeting 500k reach" \
  --domain marketing \
  --parallelism 4
```

**Deliverables**:
- Marketing calendar
- Content materials (posts/videos/articles)
- Budget allocation table

---

## 📊 Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Domain detection accuracy | >90% | **100%** | ✅ |
| Task success rate | >80% | **87%** | ✅ |
| Average quality score | >70 | **84.2** | ✅ |
| Context reset success | 100% | **100%** | ✅ |

---

## 🔧 Advanced Features

### Quality Scoring System

Each deliverable scored on:
- **Functionality** (40%)
- **Code Quality** (30%)
- **Documentation** (20%)
- **Testing Coverage** (10%)

**Pass threshold**: ≥70 points

### Context Reset

Solves "context anxiety" (AI rushes when context window is full):

```python
if context_usage > 80%:
    save_state()
    reset_session()
    restore_state()
    continue()
```

### Domain Plugins

Load custom plugins:
```bash
/harness-agent "task" --custom-plugin ./my-plugin.py
```

---

## ⚠️ Common Mistakes

### ❌ Don't: Use for Simple Tasks
```bash
# Wrong
/harness-agent "Write hello world function"

# Right
"Write hello world function"  # Normal conversation
```

### ❌ Don't: Skip Evaluation
```bash
# Wrong
/harness-agent "task" --no-evaluate

# Right
/harness-agent "task"  # Always evaluate
```

### ❌ Don't: Manual Progress Edits
```bash
# Wrong
echo "Done" >> .harness/progress.md

# Right
# Let Harness auto-update
```

---

## 📁 Deliverables Structure

After completion:

```
.harness/
├── progress.md           # Real-time progress tracking
└── deliverables/
    ├── source_code/      # Complete source code
    ├── documentation/    # README, API docs, guides
    ├── tests/           # Unit & integration tests
    └── reports/         # Test reports, metrics
```

---

## 🔮 Roadmap

### v5.1 (Planned)
- [ ] Adaptive domain detection (semantic)
- [ ] More plugins (Healthcare/Finance/Legal)
- [ ] Multi-Harness collaboration

### v5.2 (Planned)
- [ ] Real-time dashboard
- [ ] Interactive approval workflow
- [ ] Cost estimation

### v6.0 (Vision)
- [ ] Zero-config adaptation
- [ ] Cross-org collaboration
- [ ] Self-evolving system

---

## 🎯 Best Practices

### ✅ Do's
1. Use for complex tasks (>1 hour, >10 steps)
2. Review progress file regularly
3. Trust the Evaluator (quality over speed)
4. Save lessons learned after completion
5. Start with medium tasks, build confidence

### ❌ Don'ts
1. Don't use for simple tasks
2. Don't skip evaluation
3. Don't manually edit progress
4. Don't ignore failures
5. Don't set unrealistic timeouts

---

## 🔗 Resources

- [Main Repository](https://github.com/luoboask/evo-agents)
- [Full Skills Guide](../../docs/SKILLS_GUIDE.md)
- [Test Reports](./TEST_REPORT.md)
- [First Task Demo](./FIRST_TASK_REPORT.md)

---

_Last updated: 2026-04-06_  
_Version: 5.0.0 (Production Ready)_  
_License: MIT_  
_Maintainer: evo-agents Team_
