# evo-agents Workspace Setup Guide | 安装指南

[English](#english) | [中文](#中文)

**Version:** v1.0 | **版本：** v1.0  
**Updated:** 2026-03-27 | **更新日期：** 2026-03-27

---

## English {#english}

### 🎯 Overview

evo-agents is an OpenClaw Workspace template providing multi-agent collaboration, script tooling, and complete documentation.

---

### 🚀 One-Click Install (Recommended) ⭐

**Just one command:**

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**That's it!** The script will automatically:
1. Clone evo-agents template
2. Register agent to OpenClaw (**automatically creates AGENTS.md, SOUL.md, etc.**)
3. Create directory structure
4. Run tests

**No manual steps needed!** 🎉

---

### 🔄 Migration (Existing Agent)

**Already have an evo-agents or test-agents workspace?**

If you're migrating an existing Agent (not a fresh install), the install script will detect this and ask for confirmation:

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s existing-agent
```

**The script will:**
1. ⚠️ Detect existing workspace
2. ❓ Ask for migration confirmation
3. ✅ Preserve your personal data (USER.md, SOUL.md, memory/, public/)
4. 🗑️ Clean up agent-specific skills
5. 📦 Update to universal template structure

**⚠️ Important:** Before migrating:
- Backup your workspace: `cp -r ~/.openclaw/workspace-xxx /tmp/backup`
- Review [Migration Guide](docs/MIGRATION.md) for details

**What gets preserved:**
- ✅ USER.md, SOUL.md, IDENTITY.md (personal configs)
- ✅ memory/*.md (conversation history)
- ✅ public/*.json (knowledge base)
- ✅ data/ (agent data)
- ✅ agents/ (registered agents)

**What gets cleaned:**
- ❌ Agent-specific skills (e.g., `aura-*`, `danger-*`)
- ❌ Agent-specific projects (e.g., `MediaCrawler`, `baoyu-skills`)

---

### 📋 Manual Installation

If you prefer manual control:

#### Step 1: Clone Template

```bash
git clone https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent
```

#### Step 2: Register to OpenClaw

```bash
openclaw agents add my-agent --workspace ~/.openclaw/workspace-my-agent
```

This creates:
- `~/.openclaw/agents/my-agent/agent/` - Agent directory
- `AGENTS.md`, `SOUL.md`, `IDENTITY.md` - Configuration files

#### Step 3: Create Directory Structure

```bash
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent
```

#### Step 4: Initialize Personal Configs

Edit these files to define your agent:

```bash
# Agent identity
nano IDENTITY.md

# User information
nano USER.md

# Agent personality
nano SOUL.md
```

#### Step 5: Test

```bash
# Test memory system
python3 scripts/session_recorder.py -t event -c "Test event" --agent my-agent

# Check status
openclaw agents list | grep my-agent
```

---

### 🆚 Fresh Install vs Migration

| Aspect | Fresh Install | Migration |
|--------|--------------|-----------|
| **Backup needed** | ❌ No | ✅ **Required** |
| **Preserve USER.md** | ❌ No (template) | ✅ **Yes** |
| **Preserve memory/** | ❌ No | ✅ **Yes** |
| **Preserve public/** | ❌ No | ✅ **Yes** |
| **Clean skills** | ✅ Already clean | ✅ Required |
| **Confirmation** | ❌ Not needed | ✅ **Required** |

---

### 📚 Documentation

- **[README.md](README.md)** - Quick start guide
- **[docs/MIGRATION.md](docs/MIGRATION.md)** - Detailed migration guide
- **[GITHUB_PUSH_RULES.md](GITHUB_PUSH_RULES.md)** - GitHub push guidelines
- **[FEATURE_ACTIVATION_GUIDE.md](FEATURE_ACTIVATION_GUIDE.md)** - Feature activation

---

### 🛠️ Post-Installation

After installation:

```bash
cd ~/.openclaw/workspace-my-agent

# Activate advanced features
./scripts/activate-features.sh

# Check installed skills
ls skills/

# View documentation
cat README.md
```

---

### 📞 Troubleshooting

**Workspace already exists?**
- The install script will ask for confirmation
- Choose 'y' to migrate (preserves data)
- Choose 'n' to cancel

**Agent already registered?**
- Script skips registration
- Your existing config is preserved

**Missing files after install?**
- Check `git status` for untracked files
- Personal configs may be in `.gitignore`

---

## 中文 {#中文}

### 🎯 概述

evo-agents 是一个 OpenClaw Workspace 模板，提供多 Agent 协作、脚本工具链和完整文档。

---

### 🚀 一键安装（推荐）⭐

**只需一个命令：**

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**就这么简单！** 脚本会自动：
1. 克隆 evo-agents 模板
2. 注册 agent 到 OpenClaw（**自动创建 AGENTS.md, SOUL.md 等文件**）
3. 创建目录结构
4. 运行测试

**无需关心步骤！** 🎉

---

### 🔄 迁移改造（现有 Agent）

**已经有 evo-agents 或 test-agents workspace？**

如果您是在改造现有 Agent（不是全新安装），安装脚本会检测到并询问确认：

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s existing-agent
```

**脚本会：**
1. ⚠️ 检测已存在的 workspace
2. ❓ 询问迁移确认
3. ✅ 保留个人数据（USER.md, SOUL.md, memory/, public/）
4. 🗑️ 清理特定 Agent 技能
5. 📦 更新为通用模板结构

**⚠️ 重要：** 迁移前先备份：
- 备份 workspace: `cp -r ~/.openclaw/workspace-xxx /tmp/backup`
- 查看 [迁移指南](docs/MIGRATION.md) 了解详情

**保留的内容：**
- ✅ USER.md, SOUL.md, IDENTITY.md（个人配置）
- ✅ memory/*.md（对话历史）
- ✅ public/*.json（知识库）
- ✅ data/（Agent 数据）
- ✅ agents/（已注册 Agent）

**清理的内容：**
- ❌ 特定 Agent 技能（如 `aura-*`, `danger-*`）
- ❌ 特定项目（如 `MediaCrawler`, `baoyu-skills`）

---

### 📋 手动安装

如果需要手动控制：

#### 第一步：克隆模板

```bash
git clone https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent
```

#### 第二步：注册到 OpenClaw

```bash
openclaw agents add my-agent --workspace ~/.openclaw/workspace-my-agent
```

这会创建：
- `~/.openclaw/agents/my-agent/agent/` - Agent 目录
- `AGENTS.md`, `SOUL.md`, `IDENTITY.md` - 配置文件

#### 第三步：创建目录结构

```bash
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent
```

#### 第四步：初始化个人配置

编辑这些文件来定义你的 Agent：

```bash
# Agent 身份
nano IDENTITY.md

# 用户信息
nano USER.md

# Agent 人格
nano SOUL.md
```

#### 第五步：测试

```bash
# 测试记忆系统
python3 scripts/session_recorder.py -t event -c "Test event" --agent my-agent

# 检查状态
openclaw agents list | grep my-agent
```

---

### 🆚 新安装 vs 迁移改造

| 方面 | 新安装 | 迁移改造 |
|------|--------|---------|
| **需要备份** | ❌ 不需要 | ✅ **必须** |
| **保留 USER.md** | ❌ 不需要（模板） | ✅ **必须** |
| **保留 memory/** | ❌ 不需要 | ✅ **必须** |
| **保留 public/** | ❌ 不需要 | ✅ **必须** |
| **清理技能** | ✅ 已干净 | ✅ 必须 |
| **需要确认** | ❌ 不需要 | ✅ **必须** |

---

### 📚 文档

- **[README.md](README.md)** - 快速入门指南
- **[docs/MIGRATION.md](docs/MIGRATION.md)** - 详细迁移指南
- **[GITHUB_PUSH_RULES.md](GITHUB_PUSH_RULES.md)** - GitHub 推送规范
- **[FEATURE_ACTIVATION_GUIDE.md](FEATURE_ACTIVATION_GUIDE.md)** - 功能激活指南

---

### 🛠️ 安装后

安装完成后：

```bash
cd ~/.openclaw/workspace-my-agent

# 激活高级功能
./scripts/activate-features.sh

# 查看已安装的技能
ls skills/

# 查看文档
cat README.md
```

---

### 📞 故障排除

**Workspace 已存在？**
- 安装脚本会询问确认
- 选择 'y' 进行迁移（保留数据）
- 选择 'n' 取消

**Agent 已注册？**
- 脚本跳过注册步骤
- 保留现有配置

**安装后缺少文件？**
- 检查 `git status` 查看未追踪文件
- 个人配置可能在 `.gitignore` 中

---

## Quick Reference | 快速参考

```bash
# Fresh install | 新安装
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent

# Migration | 迁移改造
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s existing-agent

# Manual install | 手动安装
git clone https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent
openclaw agents add my-agent --workspace ~/.openclaw/workspace-my-agent

# Check status | 检查状态
openclaw agents list
git status
```

---

**🎉 Ready to start! | 准备开始！**
