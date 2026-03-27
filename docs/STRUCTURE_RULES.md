# evo-agents Structure Rules | 模板结构规则

[English](#english) | [中文](#中文)

---

## English {#english}

### 📁 Root Directory Structure

```
evo-agents/
├── 📁 .github/              # GitHub configuration
│   ├── ISSUE_TEMPLATE/      # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
│
├── 📁 agents/               # Agent configs (empty, .gitkeep only)
├── 📁 config/               # Configuration templates (empty)
├── 📁 data/                 # Runtime data (excluded from git)
├── 📁 docs/                 # Documentation
├── 📁 libs/                 # Shared libraries
├── 📁 memory/               # Memory data (excluded from git)
├── 📁 public/               # Knowledge base (excluded from git)
├── 📁 scripts/              # Scripts
│   ├── core/                # System scripts (updated by template)
│   └── *.sh, *.py           # User scripts (safe)
│
├── 📁 skills/               # Skills
│   ├── core/                # Universal skills (updated)
│   └── */                   # Custom skills (safe)
│
├── 📄 .gitignore            # Git ignore rules
├── 📄 install.sh            # One-click install script
│
├── 📄 AGENTS.md             # Workspace guide (local)
├── 📄 CHANGELOG.md          # Changelog
├── 📄 CODE_OF_CONDUCT.md    # Code of conduct
├── 📄 CONTRIBUTING.md       # Contributing guide
├── 📄 FEATURE_ACTIVATION_GUIDE.md
├── 📄 GITHUB_PUSH_RULES.md  # GitHub push guidelines
├── 📄 LICENSE               # License
├── 📄 README.md             # Main readme (English)
├── 📄 README.zh-CN.md       # Main readme (Chinese)
├── 📄 SECURITY.md           # Security policy
├── 📄 workspace-setup.md    # Setup guide
│
└── 📄 USER.md               # User info (local, excluded)
└── 📄 SOUL.md               # Agent personality (local, excluded)
└── 📄 IDENTITY.md           # Identity (local, excluded)
└── 📄 MEMORY.md             # Long-term memory (local, excluded)
└── 📄 HEARTBEAT.md          # Heartbeat config (local, excluded)
└── 📄 TOOLS.md              # Tool configs (local, excluded)
```

---

### 📋 File Categories

#### 1. Template Files (Updated by install)

**Location:** Root directory, `scripts/core/`, `skills/core/`, `docs/`

**Behavior:**
- 📦 Updated during re-installation
- 🔄 Managed by template
- ✏️ Can be modified, but will be overwritten

**Files:**
```
README.md, README.zh-CN.md
workspace-setup.md
CHANGELOG.md, CONTRIBUTING.md
scripts/core/*.sh, scripts/core/*.py
skills/core/*/
docs/*.md
install.sh
```

#### 2. Local Files (Preserved)

**Location:** Root directory

**Behavior:**
- ✅ Never deleted or overwritten
- 👤 Personal configuration
- 🔒 Excluded from git (in `.gitignore`)

**Files:**
```
USER.md, SOUL.md, IDENTITY.md
MEMORY.md, HEARTBEAT.md, TOOLS.md
AGENTS.md (may have local modifications)
```

#### 3. Runtime Data (Excluded)

**Location:** `memory/`, `public/`, `data/`, `agents/`

**Behavior:**
- ✅ Generated at runtime
- 📁 Excluded from git
- 💾 Backed up before install

**Directories:**
```
memory/         # Daily memory files, databases
public/         # Knowledge base (RAG)
data/           # Agent-specific data
agents/         # Registered agent configs
```

#### 4. User Scripts (Safe)

**Location:** `scripts/` root directory

**Behavior:**
- ✅ Never overwritten
- 🛠️ User's custom scripts
- 📝 Not in `.gitignore` (can commit if desired)

**Example:**
```
scripts/
├── core/              # System scripts (updated)
├── my-backup.sh       # User script (safe) ✅
├── custom-tool.py     # User script (safe) ✅
└── deploy.sh          # User script (safe) ✅
```

#### 5. User Skills (Safe)

**Location:** `skills/` root directory

**Behavior:**
- ✅ Never deleted
- 🧩 Custom skills
- 📦 Not updated by template

**Example:**
```
skills/
├── core/                  # Universal skills (updated)
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── web-knowledge/
│
├── my-custom-skill/       # User skill (safe) ✅
├── xhs-agent/             # Agent-specific skill (safe) ✅
└── pinterest-bot/         # Agent-specific skill (safe) ✅
```

---

### 🔒 .gitignore Rules

```gitignore
# Personal configs (local only)
USER.md
SOUL.md
IDENTITY.md
MEMORY.md
HEARTBEAT.md
TOOLS.md

# Runtime data
memory/
public/
data/
agents/

# Python
__pycache__/
*.py[cod]
*.egg-info/

# User scripts (optional - can commit)
scripts/*.py
scripts/*.sh
!scripts/core/

# User skills (optional - can commit)
skills/aura-*/
skills/*-agent/
skills/*-bot/
```

---

### 📝 Naming Conventions

#### Scripts
- **System:** `scripts/core/script-name.sh` or `scripts/core/script_name.py`
- **User:** `scripts/my-script.sh` or `scripts/my_tool.py`
- **Style:** lowercase, hyphens for shell, underscores for Python

#### Skills
- **Universal:** `skills/core/memory-search/`
- **Custom:** `skills/my-skill/` or `skills/agent-name/`
- **Required files:** `SKILL.md`, `skill.json`

#### Agents
- **Workspace:** `~/.openclaw/workspace-<agent-name>/`
- **Agent dir:** `~/.openclaw/agents/<agent-name>/`
- **Style:** lowercase, hyphens

#### Memory Files
- **Daily:** `memory/YYYY-MM-DD.md`
- **Weekly:** `memory/weekly/YYYY-Www.md`
- **Monthly:** `memory/monthly/YYYY-MM.md`

---

### 🚀 Installation Flow

```
1. Check if workspace exists
   ├─ No → Fresh install
   │  └─ Clone template, register agent
   │
   └─ Yes → Re-installation
      ├─ Ask: Backup before install? (y/n)
      │  └─ Yes → Backup to /tmp/workspace-backup-<agent>-<timestamp>/
      │
      ├─ Show: What will be preserved/updated
      │
      ├─ Ask: Continue? (y/n)
      │
      └─ Yes → Update template files only
         ├─ Update: scripts/core/, skills/core/, docs/
         └─ Preserve: USER.md, memory/, public/, scripts/*, skills/*
```

---

### 🛡️ Safety Rules

1. **Never delete user data**
   - `memory/`, `public/`, `data/` always preserved
   - Personal configs (USER.md, SOUL.md) never touched

2. **Never delete user scripts**
   - `scripts/` root directory safe
   - Only `scripts/core/` updated

3. **Never delete user skills**
   - `skills/` root directory safe
   - Only `skills/core/` updated

4. **Always backup before changes**
   - Auto backup before re-installation
   - Backup before restore operations

5. **Clear communication**
   - Show what will be preserved
   - Show what will be updated
   - Ask for confirmation

---

## 中文 {#中文}

### 📁 根目录结构

```
evo-agents/
├── 📁 .github/              # GitHub 配置
│   ├── ISSUE_TEMPLATE/      # Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md
│
├── 📁 agents/               # Agent 配置（空，仅.gitkeep）
├── 📁 config/               # 配置模板（空）
├── 📁 data/                 # 运行时数据（不提交）
├── 📁 docs/                 # 文档
├── 📁 libs/                 # 共享库
├── 📁 memory/               # 记忆数据（不提交）
├── 📁 public/               # 知识库（不提交）
├── 📁 scripts/              # 脚本
│   ├── core/                # 系统脚本（模板更新）
│   └── *.sh, *.py           # 用户脚本（安全）
│
├── 📁 skills/               # 技能
│   ├── core/                # 通用技能（更新）
│   └── */                   # 自定义技能（安全）
│
├── 📄 .gitignore            # Git 忽略规则
├── 📄 install.sh            # 一键安装脚本
│
├── 📄 AGENTS.md             # 工作区说明（本地）
├── 📄 CHANGELOG.md          # 更新日志
├── 📄 CODE_OF_CONDUCT.md    # 行为准则
├── 📄 CONTRIBUTING.md       # 贡献指南
├── 📄 FEATURE_ACTIVATION_GUIDE.md
├── 📄 GITHUB_PUSH_RULES.md  # GitHub 推送规范
├── 📄 LICENSE               # 许可证
├── 📄 README.md             # 主说明（英文）
├── 📄 README.zh-CN.md       # 主说明（中文）
├── 📄 SECURITY.md           # 安全策略
├── 📄 workspace-setup.md    # 安装指南
│
└── 📄 USER.md               # 用户信息（本地，不提交）
└── 📄 SOUL.md               # Agent 人格（本地，不提交）
└── 📄 IDENTITY.md           # 身份标识（本地，不提交）
└── 📄 MEMORY.md             # 长期记忆（本地，不提交）
└── 📄 HEARTBEAT.md          # 心跳配置（本地，不提交）
└── 📄 TOOLS.md              # 工具配置（本地，不提交）
```

---

### 📋 文件分类

#### 1. 模板文件（安装时更新）

**位置：** 根目录，`scripts/core/`, `skills/core/`, `docs/`

**行为：**
- 📦 重新安装时更新
- 🔄 由模板管理
- ✏️ 可修改，但会被覆盖

**文件：**
```
README.md, README.zh-CN.md
workspace-setup.md
CHANGELOG.md, CONTRIBUTING.md
scripts/core/*.sh, scripts/core/*.py
skills/core/*/
docs/*.md
install.sh
```

#### 2. 本地文件（保留）

**位置：** 根目录

**行为：**
- ✅ 永不删除或覆盖
- 👤 个人配置
- 🔒 在 `.gitignore` 中排除

**文件：**
```
USER.md, SOUL.md, IDENTITY.md
MEMORY.md, HEARTBEAT.md, TOOLS.md
AGENTS.md（可能有本地修改）
```

#### 3. 运行时数据（排除）

**位置：** `memory/`, `public/`, `data/`, `agents/`

**行为：**
- ✅ 运行时生成
- 📁 不提交到 git
- 💾 安装前备份

**目录：**
```
memory/         # 日常记忆文件、数据库
public/         # 知识库（RAG）
data/           # Agent 特定数据
agents/         # 已注册的 Agent 配置
```

#### 4. 用户脚本（安全）

**位置：** `scripts/` 根目录

**行为：**
- ✅ 永不被覆盖
- 🛠️ 用户自定义脚本
- 📝 不在 `.gitignore` 中（可选择提交）

**示例：**
```
scripts/
├── core/              # 系统脚本（更新）
├── my-backup.sh       # 用户脚本（安全）✅
├── custom-tool.py     # 用户脚本（安全）✅
└── deploy.sh          # 用户脚本（安全）✅
```

#### 5. 用户技能（安全）

**位置：** `skills/` 根目录

**行为：**
- ✅ 永不删除
- 🧩 自定义技能
- 📦 模板不更新

**示例：**
```
skills/
├── core/                  # 通用技能（更新）
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── web-knowledge/
│
├── my-custom-skill/       # 用户技能（安全）✅
├── xhs-agent/             # Agent 特定技能（安全）✅
└── pinterest-bot/         # Agent 特定技能（安全）✅
```

---

### 🔒 .gitignore 规则

```gitignore
# 个人配置（仅本地）
USER.md
SOUL.md
IDENTITY.md
MEMORY.md
HEARTBEAT.md
TOOLS.md

# 运行时数据
memory/
public/
data/
agents/

# Python
__pycache__/
*.py[cod]
*.egg-info/

# 用户脚本（可选 - 可提交）
scripts/*.py
scripts/*.sh
!scripts/core/

# 用户技能（可选 - 可提交）
skills/aura-*/
skills/*-agent/
skills/*-bot/
```

---

### 📝 命名规范

#### 脚本
- **系统：** `scripts/core/script-name.sh` 或 `scripts/core/script_name.py`
- **用户：** `scripts/my-script.sh` 或 `scripts/my_tool.py`
- **风格：** 小写，Shell 用连字符，Python 用下划线

#### 技能
- **通用：** `skills/core/memory-search/`
- **自定义：** `skills/my-skill/` 或 `skills/agent-name/`
- **必需文件：** `SKILL.md`, `skill.json`

#### Agent
- **Workspace：** `~/.openclaw/workspace-<agent-name>/`
- **Agent 目录：** `~/.openclaw/agents/<agent-name>/`
- **风格：** 小写，连字符

#### 记忆文件
- **每日：** `memory/YYYY-MM-DD.md`
- **每周：** `memory/weekly/YYYY-Www.md`
- **每月：** `memory/monthly/YYYY-MM.md`

---

### 🚀 安装流程

```
1. 检查 workspace 是否存在
   ├─ 否 → 新安装
   │  └─ 克隆模板，注册 Agent
   │
   └─ 是 → 重新安装
      ├─ 询问：安装前备份？(y/n)
      │  └─ 是 → 备份到 /tmp/workspace-backup-<agent>-<timestamp>/
      │
      ├─ 显示：保留/更新的内容
      │
      ├─ 询问：继续？(y/n)
      │
      └─ 是 → 仅更新模板文件
         ├─ 更新：scripts/core/, skills/core/, docs/
         └─ 保留：USER.md, memory/, public/, scripts/*, skills/*
```

---

### 🛡️ 安全规则

1. **永不删除用户数据**
   - `memory/`, `public/`, `data/` 始终保留
   - 个人配置（USER.md, SOUL.md）永不触碰

2. **永不删除用户脚本**
   - `scripts/` 根目录安全
   - 只更新 `scripts/core/`

3. **永不删除用户技能**
   - `skills/` 根目录安全
   - 只更新 `skills/core/`

4. **更改前始终备份**
   - 重新安装前自动备份
   - 恢复操作前备份

5. **清晰沟通**
   - 显示保留内容
   - 显示更新内容
   - 询问确认

---

**记住：模板是为了提供通用框架，不是覆盖用户的个性化配置！**
