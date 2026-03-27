# Workspace Rules | Workspace 使用规范

[English](#english) | [中文](#中文)

---

## English {#english}

### 🎯 Purpose

Prevent workspace pollution from Agent tasks (git clones, scripts, projects, etc.)

---

### 📁 Directory Usage Rules

#### ✅ Allowed Directories

| Directory | Purpose | Examples |
|-----------|---------|----------|
| `scripts/` | Scripts only | `backup.sh`, `tool.py` |
| `skills/` | Skills only | `my-skill/SKILL.md` |
| `data/<agent>/` | Agent runtime data | Auto-created |
| `memory/` | Memory files only | `2026-03-27.md` |
| `public/` | Knowledge base only | RAG data |

#### ⚠️ Restricted Directories

| Directory | Rule | Reason |
|-----------|------|--------|
| **Root `/`** | ❌ No git clones, no projects | Keeps workspace clean |
| **`agents/`** | ⚠️ Only via scripts | Use `add-agent.sh` |
| **`config/`** | ⚠️ Only config files | Don't store data here |

---

### 🛠️ Working Directory Rules

#### For Git Projects

**❌ Don't:**
```bash
# Don't clone in workspace root
cd ~/.openclaw/workspace-my-agent/
git clone https://github.com/xxx/project.git  # ❌ WRONG
```

**✅ Do:**
```bash
# Option 1: Use /tmp for temporary work
cd /tmp/
git clone https://github.com/xxx/project.git
cd project.git
# Work here...

# Option 2: Use dedicated projects directory
mkdir -p ~/projects/
cd ~/projects/
git clone https://github.com/xxx/project.git

# Option 3: Use data/<agent>/work/ for agent-specific work
cd ~/.openclaw/workspace-my-agent/data/my-agent/work/
git clone https://github.com/xxx/project.git
```

#### For Scripts

**❌ Don't:**
```bash
# Don't create scripts in root
cd ~/.openclaw/workspace-my-agent/
cat > my-script.sh  # ❌ WRONG
```

**✅ Do:**
```bash
# Create in scripts/ directory
cd ~/.openclaw/workspace-my-agent/scripts/
cat > my-script.sh  # ✅ CORRECT
chmod +x my-script.sh
```

#### For Projects/Engineering

**❌ Don't:**
```bash
# Don't create projects in root
cd ~/.openclaw/workspace-my-agent/
npm init  # ❌ WRONG
mkdir my-project  # ❌ WRONG
```

**✅ Do:**
```bash
# Use external directory
cd ~/projects/my-project/
npm init  # ✅ CORRECT

# Or use data/<agent>/work/
cd ~/.openclaw/workspace-my-agent/data/my-agent/work/
npm init  # ✅ CORRECT
```

---

### 📋 Recommended Structure

```
~/.openclaw/workspace-my-agent/     # Workspace (clean)
├── scripts/                        # Scripts only
├── skills/                         # Skills only
├── memory/                         # Memory files only
├── public/                         # Knowledge base only
├── data/
│   └── my-agent/
│       └── work/                   # Agent working directory (optional)
│           └── project/            # Temporary projects here
│
└── agents/                         # Sub-agents only
    └── sub-agent/
        ├── scripts/                # Agent-specific scripts
        ├── skills/ → ../../skills  # Symlink to parent
        └── data/
            └── work/               # Sub-agent working directory
                └── project/        # Temporary projects here
```

**External:**
```
~/projects/                         # Your projects (recommended)
├── project-a/
└── project-b/

/tmp/                               # Temporary work
└── temp-project/
```

---

### 🧹 Cleanup Rules

#### Automatic Cleanup

**Add to `.gitignore`:**
```gitignore
# Temporary work directories
data/*/work/
agents/*/data/*/work/

# Build artifacts
*.log
*.tmp
__pycache__/
node_modules/
dist/
build/
*.egg-info/
```

#### Manual Cleanup

**Weekly cleanup script:**
```bash
#!/bin/bash
# cleanup.sh - Clean workspace

WORKSPACE="$1"

echo "🧹 Cleaning workspace: $WORKSPACE"

# Clean temporary work directories
find "$WORKSPACE/data" -type d -name "work" -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE/agents" -type d -name "work" -exec rm -rf {} + 2>/dev/null || true

# Clean build artifacts
find "$WORKSPACE" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" -name "*.log" -delete 2>/dev/null || true

echo "✅ Cleanup complete"
```

---

### 📝 Agent Instructions

**Tell your agents:**

```markdown
## Workspace Rules

When working in this workspace:

1. **Scripts**: Only create in `scripts/` directory
2. **Skills**: Only create in `skills/` directory
3. **Git projects**: Use `/tmp/` or `~/projects/` or `data/<agent>/work/`
4. **Don't clone** in workspace root
5. **Don't create** project directories in root
6. **Clean up** temporary files after completion
```

---

## 中文 {#中文}

### 🎯 目的

防止 Agent 执行任务时污染 workspace（git 克隆、脚本、工程等）

---

### 📁 目录使用规则

#### ✅ 允许的目录

| 目录 | 用途 | 示例 |
|------|------|------|
| `scripts/` | 仅脚本 | `backup.sh`, `tool.py` |
| `skills/` | 仅技能 | `my-skill/SKILL.md` |
| `data/<agent>/` | Agent 运行时数据 | 自动创建 |
| `memory/` | 仅记忆文件 | `2026-03-27.md` |
| `public/` | 仅知识库 | RAG 数据 |

#### ⚠️ 限制的目录

| 目录 | 规则 | 原因 |
|------|------|------|
| **根目录 `/`** | ❌ 禁止 git clone、禁止项目 | 保持 workspace 整洁 |
| **`agents/`** | ⚠️ 仅通过脚本创建 | 使用 `add-agent.sh` |
| **`config/`** | ⚠️ 仅配置文件 | 不要存储数据 |

---

### 🛠️ 工作目录规则

#### Git 项目

**❌ 不要：**
```bash
# 不要在 workspace 根目录克隆
cd ~/.openclaw/workspace-my-agent/
git clone https://github.com/xxx/project.git  # ❌ 错误
```

**✅ 要：**
```bash
# 方式 1: 使用 /tmp 临时工作
cd /tmp/
git clone https://github.com/xxx/project.git
cd project.git
# 在这里工作...

# 方式 2: 使用专用项目目录
mkdir -p ~/projects/
cd ~/projects/
git clone https://github.com/xxx/project.git

# 方式 3: 使用 data/<agent>/work/ 存放 Agent 特定工作
cd ~/.openclaw/workspace-my-agent/data/my-agent/work/
git clone https://github.com/xxx/project.git
```

#### 脚本创建

**❌ 不要：**
```bash
# 不要在根目录创建脚本
cd ~/.openclaw/workspace-my-agent/
cat > my-script.sh  # ❌ 错误
```

**✅ 要：**
```bash
# 在 scripts/ 目录下创建
cd ~/.openclaw/workspace-my-agent/scripts/
cat > my-script.sh  # ✅ 正确
chmod +x my-script.sh
```

#### 项目/工程创建

**❌ 不要：**
```bash
# 不要在根目录创建项目
cd ~/.openclaw/workspace-my-agent/
npm init  # ❌ 错误
mkdir my-project  # ❌ 错误
```

**✅ 要：**
```bash
# 使用外部目录
cd ~/projects/my-project/
npm init  # ✅ 正确

# 或使用 data/<agent>/work/
cd ~/.openclaw/workspace-my-agent/data/my-agent/work/
npm init  # ✅ 正确
```

---

### 📋 推荐结构

```
~/.openclaw/workspace-my-agent/     # Workspace（保持整洁）
├── scripts/                        # 仅脚本
├── skills/                         # 仅技能
├── memory/                         # 仅记忆文件
├── public/                         # 仅知识库
├── data/
│   └── my-agent/
│       └── work/                   # Agent 工作目录（可选）
│           └── project/            # 临时项目放这里
│
└── agents/                         # 仅子 Agent
    └── sub-agent/
        ├── scripts/                # Agent 特定脚本
        ├── skills/ → ../../skills  # 符号链接到父
        └── data/
            └── work/               # 子 Agent 工作目录
                └── project/        # 临时项目放这里
```

**外部：**
```
~/projects/                         # 你的项目（推荐）
├── project-a/
└── project-b/

/tmp/                               # 临时工作
└── temp-project/
```

---

### 🧹 清理规则

#### 自动清理

**添加到 `.gitignore`：**
```gitignore
# 临时工作目录
data/*/work/
agents/*/data/*/work/

# 构建产物
*.log
*.tmp
__pycache__/
node_modules/
dist/
build/
*.egg-info/
```

#### 手动清理

**使用清理脚本：**
```bash
# 运行清理脚本
./scripts/core/cleanup.sh

# 或指定 workspace
./scripts/core/cleanup.sh ~/.openclaw/workspace-my-agent
```

**清理脚本会询问：**
```
❓ 要清理哪些内容？
   1) 只清理构建产物 (node_modules, __pycache__, *.log 等)
   2) 清理构建产物 + work/ 目录（请确认 work/ 是临时的）
   3) 取消
```

**构建产物（安全清理）：**
- ✅ `node_modules/` - npm 依赖
- ✅ `__pycache__/` - Python 缓存
- ✅ `*.log`, `*.tmp`, `*.pyc` - 临时文件

**work/ 目录（需要确认）：**
- ⚠️ 脚本**无法判断**是临时还是长期项目
- ⚠️ 需要**手动确认**后再清理
- ✅ 只有你确认是临时的才清理

---

**work/ 目录说明：**

`work/` 是**工作目录**，可能包含：
- 📦 临时项目（分析完就删除）
- 📦 长期项目（持续开发）
- 📦 测试数据

**脚本无法区分，需要你手动决定！**

**建议做法：**
```bash
# 方式 1: 使用 /tmp/ 存放真正的临时工作
cd /tmp/
git clone https://github.com/xxx/project.git
# 用完就删除

# 方式 2: 使用 ~/projects/ 存放长期项目
cd ~/projects/
git clone https://github.com/xxx/project.git
# 长期保存

# 方式 3: 使用 data/<agent>/work/ 但要手动清理
cd data/my-agent/work/
git clone https://github.com/xxx/project.git
# 完成后手动删除
rm -rf work/project/
```

---

### 📝 Agent 指令

**告诉你的 Agent：**

```markdown
## Workspace 使用规则

在这个 workspace 工作时：

1. **脚本**：只在 `scripts/` 目录创建
2. **技能**：只在 `skills/` 目录创建
3. **Git 项目**：使用 `/tmp/` 或 `~/projects/` 或 `data/<agent>/work/`
4. **不要在根目录克隆** git 仓库
5. **不要在根目录创建** 项目目录
6. **完成后清理** 临时文件
```

---

### 💡 最佳实践

1. **分离工作和配置** - Workspace 用于配置，外部目录用于工作
2. **使用符号链接** - 需要访问时创建符号链接
3. **定期清理** - 每周运行清理脚本
4. **明确规则** - 在 Agent 的系统提示中说明规则

---

**保持 workspace 整洁，让 Agent 高效工作！** 🚀
