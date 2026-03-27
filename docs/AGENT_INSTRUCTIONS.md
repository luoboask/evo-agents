# Agent Instructions | Agent 指令

[English](#english) | [中文](#中文)

---

## English {#english}

### 🎯 Your Role

You are an AI assistant working in this workspace. Follow these rules to keep the workspace clean and organized.

---

### 📋 Workspace Rules

**When working in this workspace:**

#### 1. Scripts | 脚本
- ✅ **Create in:** `scripts/` directory
- ❌ **Don't create in:** Root directory

```bash
# ✅ Correct
cd scripts/
cat > my-tool.sh

# ❌ Wrong
cd ..
cat > my-tool.sh
```

#### 2. Skills | 技能
- ✅ **Create in:** `skills/` directory
- ❌ **Don't create in:** Root directory

```bash
# ✅ Correct
cd skills/
mkdir my-skill/

# ❌ Wrong
cd ..
mkdir my-skill/
```

#### 3. Git Projects | Git 项目
- ✅ **Use:** `/tmp/` or `~/projects/` or `data/<agent>/work/`
- ❌ **Don't clone in:** Root directory

```bash
# ✅ Correct
cd /tmp/
git clone https://github.com/xxx/project.git

# Or
cd ~/projects/
git clone https://github.com/xxx/project.git

# Or (for agent-specific work)
cd data/my-agent/work/
git clone https://github.com/xxx/project.git

# ❌ Wrong
cd ..
git clone https://github.com/xxx/project.git
```

#### 4. Projects/Engineering | 项目/工程
- ✅ **Create in:** `~/projects/` or `data/<agent>/work/`
- ❌ **Don't create in:** Root directory

```bash
# ✅ Correct
cd ~/projects/my-project/
npm init

# Or
cd data/my-agent/work/my-project/
npm init

# ❌ Wrong
cd ..
npm init
```

#### 5. Temporary Files | 临时文件
- ✅ **Use:** `/tmp/` or `data/<agent>/work/`
- ❌ **Don't leave in:** Root directory

```bash
# ✅ Correct
cd /tmp/
# Work with temporary files

# Or
cd data/my-agent/work/
# Work with temporary files

# ❌ Wrong
cd ..
# Don't leave temporary files here
```

#### 6. Cleanup | 清理
- ✅ **Clean up** after completing tasks
- ✅ **Remove** temporary files
- ✅ **Remove** build artifacts (`node_modules/`, `__pycache__/`, `*.log`)

---

### 📁 Directory Structure

```
workspace/
├── scripts/           # Your scripts go here ✅
├── skills/            # Your skills go here ✅
├── memory/            # Memory files only
├── public/            # Knowledge base only
├── data/
│   └── <agent>/
│       └── work/      # Temporary work here ✅
└── agents/            # Sub-agents only
```

**External:**
```
~/projects/            # Your projects (recommended) ✅
/tmp/                  # Temporary work ✅
```

---

### 🚫 Never Do This

```bash
# ❌ Don't clone in workspace root
cd ~/.openclaw/workspace-my-agent/
git clone https://github.com/xxx/project.git

# ❌ Don't create projects in root
mkdir my-project
npm init

# ❌ Don't create scripts in root
cat > script.sh

# ❌ Don't leave temporary files
ls *.tmp *.log
```

---

### ✅ Always Do This

```bash
# ✅ Use external directories for projects
cd ~/projects/
git clone https://github.com/xxx/project.git

# ✅ Use scripts/ for scripts
cd scripts/
cat > my-script.sh

# ✅ Use data/<agent>/work/ for agent-specific work
cd data/my-agent/work/
# Work here

# ✅ Clean up after work
rm -rf /tmp/temp-*
rm -rf data/my-agent/work/temp-*
```

---

## 中文 {#中文}

### 🎯 你的角色

你是工作在这个 workspace 的 AI 助手。遵守以下规则保持 workspace 整洁有序。

---

### 📋 Workspace 规则

**在这个 workspace 工作时：**

#### 1. 脚本
- ✅ **创建在：** `scripts/` 目录
- ❌ **不要创建在：** 根目录

```bash
# ✅ 正确
cd scripts/
cat > my-tool.sh

# ❌ 错误
cd ..
cat > my-tool.sh
```

#### 2. 技能
- ✅ **创建在：** `skills/` 目录
- ❌ **不要创建在：** 根目录

```bash
# ✅ 正确
cd skills/
mkdir my-skill/

# ❌ 错误
cd ..
mkdir my-skill/
```

#### 3. Git 项目
- ✅ **使用：** `/tmp/` 或 `~/projects/` 或 `data/<agent>/work/`
- ❌ **不要克隆在：** 根目录

```bash
# ✅ 正确
cd /tmp/
git clone https://github.com/xxx/project.git

# 或
cd ~/projects/
git clone https://github.com/xxx/project.git

# 或（Agent 特定工作）
cd data/my-agent/work/
git clone https://github.com/xxx/project.git

# ❌ 错误
cd ..
git clone https://github.com/xxx/project.git
```

#### 4. 项目/工程
- ✅ **创建在：** `~/projects/` 或 `data/<agent>/work/`
- ❌ **不要创建在：** 根目录

```bash
# ✅ 正确
cd ~/projects/my-project/
npm init

# 或
cd data/my-agent/work/my-project/
npm init

# ❌ 错误
cd ..
npm init
```

#### 5. 临时文件
- ✅ **使用：** `/tmp/` 或 `data/<agent>/work/`
- ❌ **不要留在：** 根目录

```bash
# ✅ 正确
cd /tmp/
# 处理临时文件

# 或
cd data/my-agent/work/
# 处理临时文件

# ❌ 错误
cd ..
# 不要把临时文件留在这里
```

#### 6. 清理
- ✅ **完成后清理**
- ✅ **删除**临时文件
- ✅ **删除**构建产物（`node_modules/`, `__pycache__/`, `*.log`）

---

### 📁 目录结构

```
workspace/
├── scripts/           # 你的脚本放这里 ✅
├── skills/            # 你的技能放这里 ✅
├── memory/            # 仅记忆文件
├── public/            # 仅知识库
├── data/
│   └── <agent>/
│       └── work/      # 临时工作放这里 ✅
└── agents/            # 仅子 Agent
```

**外部：**
```
~/projects/            # 你的项目（推荐）✅
/tmp/                  # 临时工作 ✅
```

---

### 🚫 永远不要这样做

```bash
# ❌ 不要在 workspace 根目录克隆
cd ~/.openclaw/workspace-my-agent/
git clone https://github.com/xxx/project.git

# ❌ 不要在根目录创建项目
mkdir my-project
npm init

# ❌ 不要在根目录创建脚本
cat > script.sh

# ❌ 不要留下临时文件
ls *.tmp *.log
```

---

### ✅ 永远这样做

```bash
# ✅ 使用外部目录进行项目
cd ~/projects/
git clone https://github.com/xxx/project.git

# ✅ 在 scripts/ 创建脚本
cd scripts/
cat > my-script.sh

# ✅ 在 data/<agent>/work/ 进行 Agent 特定工作
cd data/my-agent/work/
# 在这里工作

# ✅ 工作后清理
rm -rf /tmp/temp-*
rm -rf data/my-agent/work/temp-*
```

---

**记住：保持 workspace 整洁，让所有 Agent 高效工作！** 🚀
