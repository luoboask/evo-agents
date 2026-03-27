# evo-agents Structure Rules | 模板结构规则

[English](#english) | [中文](#中文)

---

## English {#english}

### 📁 Root Directory Structure

```
evo-agents/
├── 📁 .github/              # GitHub configuration
├── 📁 agents/               # Sub-agents (created by scripts)
├── 📁 config/               # Configuration
├── 📁 data/                 # Runtime data (excluded)
├── 📁 docs/                 # Documentation
├── 📁 libs/                 # Shared libraries
├── 📁 memory/               # Memory data (excluded)
├── 📁 public/               # Knowledge base (excluded)
├── 📁 scripts/              # Scripts (all agents share)
│   ├── core/                # System scripts (updated)
│   └── *.sh, *.py           # Your scripts
├── 📁 skills/               # Skills (OpenClaw native)
│   ├── memory-search/       # Template skill (updated)
│   ├── rag/                 # Template skill (updated)
│   ├── self-evolution/      # Template skill (updated)
│   ├── web-knowledge/       # Template skill (updated)
│   └── <your-skill>/        # Your skill (preserved)
├── 📄 .gitignore
├── 📄 install.sh
└── 📄 *.md                  # Documentation
```

---

### 📋 File Categories

#### 1. Template Files (Updated)

**Location:** Root, `scripts/core/`, `skills/` (4 universal), `docs/`

**Files:**
- README.md, workspace-setup.md
- scripts/core/*.sh, scripts/core/*.py
- skills/memory-search/, skills/rag/
- skills/self-evolution/, skills/web-knowledge/
- docs/*.md

#### 2. Your Files (Preserved)

**Location:** Anywhere

**Files:**
- Personal configs: USER.md, SOUL.md, etc. (excluded by .gitignore)
- Your scripts: scripts/*.sh, scripts/*.py
- Your skills: skills/<your-skill>/
- Runtime data: memory/, public/, data/

#### 3. Sub-Agents

**Created by:** `scripts/core/add-agent.sh` or `scripts/core/setup-multi-agent.sh`

**Location:** `agents/<agent-name>/`

**Structure:**
```
agents/<agent-name>/
├── agent/                   # Agent config
├── memory/                  # Agent memory
├── sessions/                # Chat sessions
├── AGENTS.md, SOUL.md
└── data/
```

**Note:** Sub-agents share parent's scripts/ and skills/ (no symlinks needed)

---

### 📝 Naming Conventions

#### Scripts
- **System:** `scripts/core/script-name.sh` or `script_name.py`
- **User:** `scripts/my-script.sh` or `my_tool.py`
- **Style:** Lowercase, hyphens for shell, underscores for Python

#### Skills
- **Universal:** `skills/memory-search/`, `skills/rag/`, etc.
- **Custom:** `skills/my-skill/`
- **Required:** `SKILL.md`, `skill.json`

#### Agents
- **Workspace:** `~/.openclaw/workspace-<agent-name>/`
- **Sub-agent:** `agents/<agent-name>/`
- **Style:** Lowercase, hyphens

---

### 🚀 Installation Flow

```
1. Check workspace exists
   ├─ No → Fresh install (clone + register)
   └─ Yes → Re-install
      ├─ Backup? (y/n)
      ├─ Show preserve/update list
      ├─ Confirm? (y/n)
      └─ Update template files only
         ├─ Update: scripts/core/, 4 universal skills, docs/
         └─ Preserve: USER.md, memory/, public/, scripts/*, skills/*
```

---

### 🛡️ Safety Rules

1. **Never delete user data** - memory/, public/, data/ always preserved
2. **Never delete user scripts** - scripts/ root is safe
3. **Never delete user skills** - skills/ root is safe (except 4 universal)
4. **Always backup** - Auto backup before re-install
5. **Clear communication** - Show what's preserved/updated

---

## 中文 {#中文}

### 📁 根目录结构

```
evo-agents/
├── 📁 .github/              # GitHub 配置
├── 📁 agents/               # 子 Agent（脚本创建）
│   └── <agent-name>/        # 子 Agent 目录
│       ├── agent/           # Agent 配置
│       ├── memory/          # Agent 记忆
│       ├── sessions/        # 聊天会话
│       ├── scripts/         # Agent 特定脚本（可选）
│       ├── skills/          # Agent 特定技能（可选）
│       ├── libs/            # Agent 特定库（可选）
│       └── data/            # Agent 数据
├── 📁 config/               # 配置
├── 📁 data/                 # 运行时数据（不提交）
├── 📁 docs/                 # 文档
├── 📁 libs/                 # 共享库
├── 📁 memory/               # 记忆数据（不提交）
├── 📁 public/               # 知识库（不提交）
├── 📁 scripts/              # 脚本（所有 Agent 共享）
│   ├── core/                # 系统脚本（更新）
│   └── *.sh, *.py           # 你的脚本
├── 📁 skills/               # 技能（OpenClaw 原生）
│   ├── memory-search/       # 模板技能（更新）
│   ├── rag/                 # 模板技能（更新）
│   ├── self-evolution/      # 模板技能（更新）
│   ├── web-knowledge/       # 模板技能（更新）
│   └── <your-skill>/        # 你的技能（保留）
├── 📄 .gitignore
├── 📄 install.sh
└── 📄 *.md                  # 文档
```

---

### 📋 文件分类

#### 1. 模板文件（更新）

**位置：** 根目录，`scripts/core/`, `skills/`（4 个通用）, `docs/`

**文件：**
- README.md, workspace-setup.md
- scripts/core/*.sh, scripts/core/*.py
- skills/memory-search/, skills/rag/
- skills/self-evolution/, skills/web-knowledge/
- docs/*.md

#### 2. 你的文件（保留）

**位置：** 任意位置

**文件：**
- 个人配置：USER.md, SOUL.md 等（.gitignore 排除）
- 你的脚本：scripts/*.sh, scripts/*.py
- 你的技能：skills/<your-skill>/
- 运行时数据：memory/, public/, data/

#### 3. 子 Agent

**创建：** `scripts/core/add-agent.sh` 或 `scripts/core/setup-multi-agent.sh`

**位置：** `agents/<agent-name>/`

**结构：**
```
agents/<agent-name>/
├── agent/                   # Agent 配置
├── memory/                  # Agent 记忆
├── sessions/                # 聊天会话
├── scripts/                 # Agent 特定脚本（可选）
├── skills/                  # Agent 特定技能（可选）
├── libs/                    # Agent 特定库（可选）
├── AGENTS.md, SOUL.md
└── data/
```

**说明：**
- ✅ 子 Agent 可以有自己的 `scripts/`, `skills/`, `libs/`
- ✅ 也可以使用父 workspace 的资源
- ✅ 灵活选择，无强制要求

---

### 📝 命名规范

#### 脚本
- **系统：** `scripts/core/script-name.sh` 或 `script_name.py`
- **用户：** `scripts/my-script.sh` 或 `my_tool.py`
- **风格：** 小写，Shell 用连字符，Python 用下划线

#### 技能
- **通用：** `skills/memory-search/`, `skills/rag/` 等
- **自定义：** `skills/my-skill/`
- **必需：** `SKILL.md`, `skill.json`

#### Agent
- **Workspace：** `~/.openclaw/workspace-<agent-name>/`
- **子 Agent：** `agents/<agent-name>/`
- **风格：** 小写，连字符

---

### 🚀 安装流程

```
1. 检查 workspace 是否存在
   ├─ 否 → 新安装（克隆 + 注册）
   └─ 是 → 重新安装
      ├─ 备份？(y/n)
      ├─ 显示保留/更新列表
      ├─ 确认？(y/n)
      └─ 仅更新模板文件
         ├─ 更新：scripts/core/, 4 个通用技能，docs/
         └─ 保留：USER.md, memory/, public/, scripts/*, skills/*
```

---

### 🛡️ 安全规则

1. **永不删除用户数据** - memory/, public/, data/ 始终保留
2. **永不删除用户脚本** - scripts/ 根目录安全
3. **永不删除用户技能** - skills/ 根目录安全（除了 4 个通用技能）
4. **始终备份** - 重新安装前自动备份
5. **清晰沟通** - 显示保留/更新内容

---

## ❓ FAQ | 常见问题

### Q: Agent 执行时创建的脚本放在哪里？

**A:** 有两种选择：

**选项 1: 共享脚本（推荐）**
```bash
# 放在父 workspace 的 scripts/ 根目录
cat > scripts/backup.sh
# 所有 Agent 都可以使用
```

**选项 2: Agent 特定脚本**
```bash
# 放在子 Agent 自己的 scripts/ 目录
cd agents/<agent-name>/
cat > scripts/agent-backup.sh
# 只有这个 Agent 使用
```

**规则：**
- ✅ 可以放在父 workspace 的 `scripts/`（所有 Agent 共享）
- ✅ 可以放在子 Agent 的 `agents/<agent>/scripts/`（Agent 特定）
- ✅ 灵活选择，无强制要求

---

### Q: 子 Agent 如何访问脚本？

**A:** 子 Agent 直接使用父 workspace 的 scripts/：
```bash
# 在 agents/<agent-name>/ 目录下
python3 scripts/session_recorder.py  # 使用父 workspace 的脚本
```

---

### Q: skills 目录结构是怎样的？

**A:** OpenClaw 原生结构，所有技能在一个目录：
```
skills/
├── memory-search/         # 模板技能（更新）
├── rag/                   # 模板技能（更新）
├── self-evolution/        # 模板技能（更新）
├── web-knowledge/         # 模板技能（更新）
└── my-custom-skill/       # 你的技能（保留）
```

---

**记住：模板是为了提供通用框架，不是覆盖用户的个性化配置！**
