# Agent Instructions | Agent 指令

[English](#english) | [中文](#中文)

---

## English {#english}

### 🎯 Your Role

You are an AI assistant working in this workspace. Follow these rules to keep the workspace clean and organized.

---

### 📋 Quick Rules | 快速规则

**✅ Always Do:**
- Scripts → `scripts/` directory
- Git projects → `/tmp/` or `~/projects/` or `data/<agent>/work/`
- Clean up after completing tasks

**❌ Never Do:**
- Don't clone git in workspace root
- Don't create projects in root
- Don't leave temporary files in root

**Full rules:** [WORKSPACE_RULES.md](WORKSPACE_RULES.md)

---

### 📁 Directory Usage

| Directory | Purpose | Can I use? |
|-----------|---------|------------|
| `scripts/` | Scripts only | ✅ Yes - for your scripts |
| `skills/` | Skills only | ✅ Yes - for your skills |
| `data/<agent>/work/` | Temporary work | ✅ Yes - for agent work |
| `memory/` | Memory files | ❌ No - system use only |
| `public/` | Knowledge base | ❌ No - system use only |
| Root `/` | Workspace root | ❌ No - keep clean |

**External directories:**
- `/tmp/` - Temporary work ✅
- `~/projects/` - Long-term projects ✅

---

### 🛠️ Common Tasks

#### Creating Scripts

```bash
# ✅ Correct
cd scripts/
cat > my-tool.sh
chmod +x my-tool.sh

# ❌ Wrong
cd ..
cat > my-tool.sh  # Don't create in root!
```

#### Git Projects

```bash
# ✅ Correct - Temporary
cd /tmp/
git clone https://github.com/xxx/project.git
# Work here, then delete when done

# ✅ Correct - Long-term
cd ~/projects/
git clone https://github.com/xxx/project.git
# Keep here

# ✅ Correct - Agent-specific
cd data/my-agent/work/
git clone https://github.com/xxx/project.git
# Clean up when done

# ❌ Wrong
cd ..
git clone https://github.com/xxx/project.git  # Don't clone in root!
```

#### Creating Projects

```bash
# ✅ Correct
cd ~/projects/my-project/
npm init

# Or
cd data/my-agent/work/my-project/
npm init

# ❌ Wrong
cd ..
npm init  # Don't create in root!
```

---

### 🧹 Cleanup

**After completing tasks:**

```bash
# Clean temporary files
rm -rf /tmp/temp-*
rm -rf data/my-agent/work/temp-*

# Or run cleanup script
./scripts/core/cleanup.sh
```

**What cleanup script does:**
- ✅ Cleans `node_modules/`, `__pycache__/`
- ✅ Cleans `*.log`, `*.tmp`, `*.pyc`
- ❌ Does NOT clean `work/` directories (you decide)

---

### 📖 More Information

| Topic | Document |
|-------|----------|
| Full workspace rules | [WORKSPACE_RULES.md](WORKSPACE_RULES.md) |
| Structure overview | [STRUCTURE_RULES.md](STRUCTURE_RULES.md) |
| Quick reference | [AGENT_RULES.md](AGENT_RULES.md) |

---

## 中文 {#中文}

### 🎯 你的角色

你是工作在这个 workspace 的 AI 助手。遵守以下规则保持 workspace 整洁有序。

---

### 📋 快速规则

**✅ 永远这样做：**
- 脚本 → `scripts/` 目录
- Git 项目 → `/tmp/` 或 `~/projects/` 或 `data/<agent>/work/`
- 完成后清理

**❌ 永远不要：**
- 不要在根目录克隆 git
- 不要在根目录创建项目
- 不要把临时文件留在根目录

**完整规则：** [WORKSPACE_RULES.md](WORKSPACE_RULES.md)

---

### 📁 目录使用

| 目录 | 用途 | 可以用吗？ |
|------|------|-----------|
| `scripts/` | 仅脚本 | ✅ 可以 - 放你的脚本 |
| `skills/` | 仅技能 | ✅ 可以 - 放你的技能 |
| `data/<agent>/work/` | 临时工作 | ✅ 可以 - Agent 工作 |
| `memory/` | 记忆文件 | ❌ 不行 - 系统使用 |
| `public/` | 知识库 | ❌ 不行 - 系统使用 |
| 根目录 `/` | Workspace 根 | ❌ 不行 - 保持整洁 |

**外部目录：**
- `/tmp/` - 临时工作 ✅
- `~/projects/` - 长期项目 ✅

---

### 🛠️ 常见任务

#### 创建脚本

```bash
# ✅ 正确
cd scripts/
cat > my-tool.sh
chmod +x my-tool.sh

# ❌ 错误
cd ..
cat > my-tool.sh  # 不要在根目录创建！
```

#### Git 项目

```bash
# ✅ 正确 - 临时
cd /tmp/
git clone https://github.com/xxx/project.git
# 在这里工作，完成后删除

# ✅ 正确 - 长期
cd ~/projects/
git clone https://github.com/xxx/project.git
# 保存在这里

# ✅ 正确 - Agent 特定
cd data/my-agent/work/
git clone https://github.com/xxx/project.git
# 完成后清理

# ❌ 错误
cd ..
git clone https://github.com/xxx/project.git  # 不要在根目录克隆！
```

#### 创建项目

```bash
# ✅ 正确
cd ~/projects/my-project/
npm init

# 或
cd data/my-agent/work/my-project/
npm init

# ❌ 错误
cd ..
npm init  # 不要在根目录创建！
```

---

### 🧹 清理

**完成任务后：**

```bash
# 清理临时文件
rm -rf /tmp/temp-*
rm -rf data/my-agent/work/temp-*

# 或运行清理脚本
./scripts/core/cleanup.sh
```

**清理脚本做什么：**
- ✅ 清理 `node_modules/`, `__pycache__/`
- ✅ 清理 `*.log`, `*.tmp`, `*.pyc`
- ❌ 不清理 `work/` 目录（你自己决定）

---

### 📖 更多信息

| 主题 | 文档 |
|------|------|
| 完整 workspace 规则 | [WORKSPACE_RULES.md](WORKSPACE_RULES.md) |
| 结构概览 | [STRUCTURE_RULES.md](STRUCTURE_RULES.md) |
| 快速参考 | [AGENT_RULES.md](AGENT_RULES.md) |

---

**Remember: Keep the workspace clean for everyone!**  
**记住：保持 workspace 整洁，让大家高效工作！** 🚀
