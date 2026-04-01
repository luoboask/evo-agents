# docs/ 目录索引

_文档分类和用途说明_

---

## 📚 文档分类

### 🤖 Agent 规则文档（Agent 需要感知）

**这些文档让 Agent 启动时读取，了解行为规范。**

| 文档 | 作用 | 优先级 |
|------|------|--------|
| [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) | **Agent 主指令**（必读） | ⭐⭐⭐⭐⭐ |
| [AGENT_BEHAVIOR.md](AGENT_BEHAVIOR.md) | 核心行为规范 | ⭐⭐⭐⭐⭐ |
| [SKILL_RULES.md](SKILL_RULES.md) | 技能使用规则 | ⭐⭐⭐⭐⭐ |
| [WORKSPACE_RULES.md](WORKSPACE_RULES.md) | Workspace 规范 | ⭐⭐⭐⭐⭐ |
| [KNOWLEDGE_BASE_RULES.md](KNOWLEDGE_BASE_RULES.md) | 知识库管理 | ⭐⭐⭐⭐⭐ |
| [SUBAGENT_RULES.md](SUBAGENT_RULES.md) | 子 Agent 规则 | ⭐⭐⭐⭐ |
| [SCHEDULER.md](SCHEDULER.md) | 定时任务配置 | ⭐⭐⭐⭐ |

**安装流程：**
```bash
# install.sh 自动配置
1. OpenClaw 创建 Agent → 生成 AGENTS.md
2. install.sh 追加规则引用到 AGENTS.md
3. 复制 docs/ 规则文档
4. Agent 启动时读取 AGENTS.md → 看到规则引用 → 读取 docs/
```

---

### 📖 用户文档（用户参考）

**这些文档供用户参考，Agent 不需要主动读取。**

| 文档 | 作用 | 读者 |
|------|------|------|
| [README.md](README.md) | 项目介绍 | 用户 |
| [QUICKSTART.md](QUICKSTART.md) | 快速开始 | 用户 |
| [FAQ.md](FAQ.md) | 常见问题 | 用户 |
| [UNINSTALL.md](UNINSTALL.md) | 卸载指南 | 用户 |
| [FEATURE_ACTIVATION_GUIDE.md](FEATURE_ACTIVATION_GUIDE.md) | 功能激活 | 用户 |

---

### 🏗️ 架构文档（开发参考）

**这些文档描述系统架构，供开发参考。**

| 文档 | 作用 | 读者 |
|------|------|------|
| [ARCHITECTURE_GENERIC_CN.md](ARCHITECTURE_GENERIC_CN.md) | 中文架构文档 | 开发者 |
| [ARCHITECTURE_GENERIC_EN.md](ARCHITECTURE_GENERIC_EN.md) | English architecture | Developer |
| [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) | 目录结构说明 | 开发者 |
| [SUB_AGENT_STRUCTURE.md](SUB_AGENT_STRUCTURE.md) | 子 Agent 结构 | 开发者 |
| [SUB_AGENT_DATA.md](SUB_AGENT_DATA.md) | 子 Agent 数据 | 开发者 |

---

### 🔧 内部文档（系统使用）

**这些文档用于系统内部，用户和 Agent 都不需要主动读取。**

| 文档 | 作用 |
|------|------|
| [INDEX.md](INDEX.md) | 本文档（索引） |
| [SELF_CHECK.md](SELF_CHECK.md) | 系统自检 |
| [PERFORMANCE_OPTIMIZATION_PLAN.md](PERFORMANCE_OPTIMIZATION_PLAN.md) | 性能优化计划 |
| [AGENT_RULES_INDEX.md](AGENT_RULES_INDEX.md) | 规则索引（旧版） |
| [CONFIG_FLOW.md](CONFIG_FLOW.md) | 配置流程（旧版） |
| [RULES_CHECKLIST.md](RULES_CHECKLIST.md) | 规则检查清单（旧版） |
| [AGENT_SKILL_RULES.md](AGENT_SKILL_RULES.md) | 技能规则（旧版） |
| [SKILL_SCHEDULER.md](SKILL_SCHEDULER.md) | 定时任务（旧版） |
| [SKILL_USAGE_RULES.md](SKILL_USAGE_RULES.md) | 技能使用（旧版） |

---

## 🎯 Agent 启动流程

```
Agent 启动
    ↓
读取 AGENTS.md（OpenClaw 生成 + install.sh 追加）
    ↓
看到规则引用：
  - docs/AGENT_BEHAVIOR.md
  - docs/SKILL_RULES.md
  - docs/WORKSPACE_RULES.md
  - docs/KNOWLEDGE_BASE_RULES.md
  - docs/SUBAGENT_RULES.md
    ↓
根据需要读取详细文档
    ↓
遵守规则执行任务
```

---

## 📋 install.sh 配置流程

```bash
# 1. 克隆 evo-agents 仓库
git clone https://gitee.com/luoboask/evo-agents.git

# 2. 清理开发文件
rm -rf .github/ docs/dev/ examples/

# 3. 注册到 OpenClaw（生成 AGENTS.md）
openclaw agents add my-agent

# 4. 追加规则到 AGENTS.md
cat >> AGENTS.md << 'EOF'
## 🎯 Agent Rules
...
EOF

# 5. 复制规则文档
cp docs/AGENT_INSTRUCTIONS.md docs/
cp docs/AGENT_BEHAVIOR.md docs/
cp docs/SKILL_RULES.md docs/
cp docs/WORKSPACE_RULES.md docs/
cp docs/KNOWLEDGE_BASE_RULES.md docs/
cp docs/SUBAGENT_RULES.md docs/
cp docs/SCHEDULER.md docs/
```

---

## 📊 文档优先级

### ⭐⭐⭐⭐⭐ 必须（Agent 启动必读）
- AGENT_INSTRUCTIONS.md
- AGENT_BEHAVIOR.md
- SKILL_RULES.md
- WORKSPACE_RULES.md
- KNOWLEDGE_BASE_RULES.md

### ⭐⭐⭐⭐ 重要（需要时读取）
- SUBAGENT_RULES.md
- SCHEDULER.md

### ⭐⭐⭐ 参考（用户/开发者）
- README.md
- QUICKSTART.md
- FAQ.md
- ARCHITECTURE_*.md

### ⭐⭐ 内部（系统使用）
- SELF_CHECK.md
- PERFORMANCE_OPTIMIZATION_PLAN.md
- 旧版文档（*_OLD.md）

---

## 🗂️ 建议的目录结构

```
docs/
├── 🤖 Agent Rules（Agent 规则）
│   ├── AGENT_INSTRUCTIONS.md      ← 主指令（必读）
│   ├── AGENT_BEHAVIOR.md          ← 行为规范
│   ├── SKILL_RULES.md             ← 技能使用
│   ├── WORKSPACE_RULES.md         ← Workspace 规范
│   ├── KNOWLEDGE_BASE_RULES.md    ← 知识库管理
│   ├── SUBAGENT_RULES.md          ← 子 Agent 规则
│   └── SCHEDULER.md               ← 定时任务
│
├── 📖 User Docs（用户文档）
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── FAQ.md
│   └── UNINSTALL.md
│
├── 🏗️ Architecture（架构文档）
│   ├── ARCHITECTURE_GENERIC_CN.md
│   ├── ARCHITECTURE_GENERIC_EN.md
│   ├── DIRECTORY_STRUCTURE.md
│   ├── SUB_AGENT_STRUCTURE.md
│   └── SUB_AGENT_DATA.md
│
└── 🔧 Internal（内部文档）
    ├── INDEX.md                   ← 本文档
    ├── SELF_CHECK.md
    ├── PERFORMANCE_OPTIMIZATION_PLAN.md
    └── (旧版文档)
```

---

## 🎯 核心原则

1. **Agent 规则文档** - 精简、清晰、可执行
2. **用户文档** - 易懂、实用、示例丰富
3. **架构文档** - 详细、准确、技术导向
4. **内部文档** - 不干扰 Agent 和用户

**install.sh 只复制 Agent 规则文档，其他文档由用户按需阅读。**

---

_版本：1.0.0 | 2026-04-01_
