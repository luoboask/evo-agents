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

#### Fresh Install (New Agent)

**Just one command:**

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**That's it!** The script will:
1. Clone evo-agents template
2. Register agent to OpenClaw
3. Create directory structure
4. Run tests

---

### 🔄 Re-installation (Existing Agent)

**Already have a workspace for this agent?**

#### Option 1: Interactive (Recommended) ⭐

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s existing-agent
```

**What happens:**
- ⚠️ Detects existing workspace
- ❓ Asks for confirmation (y/n)
- ✅ Preserves your data (USER.md, SOUL.md, memory/, public/, skills/, scripts/)
- 📦 Updates template files (skills/core/, scripts/core/, docs/)

**What's preserved:**
- ✅ Personal configs (USER.md, SOUL.md, etc.)
- ✅ Memory data (memory/ directory)
- ✅ Knowledge base (public/ directory)
- ✅ Your skills (skills/ directory)
- ✅ Your scripts (scripts/ root directory)

**What's updated:**
- 📦 Universal skills (skills/core/)
- 📦 System scripts (scripts/core/)
- 📦 Documentation (README.md, etc.)

#### Option 2: Download First

```bash
curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh
bash install.sh existing-agent
```

#### Option 3: Force (Skip Confirmation)

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s existing-agent --force
```

---

### 📋 Manual Installation

#### Step 1: Clone Template

```bash
git clone https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent
```

#### Step 2: Register to OpenClaw

```bash
openclaw agents add my-agent --workspace ~/.openclaw/workspace-my-agent
```

#### Step 3: Create Directories

```bash
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent
```

#### Step 4: Test

```bash
python3 scripts/core/session_recorder.py -t event -c "Test" --agent my-agent
```

---

### 📁 Directory Structure

```
workspace/
├── skills/
│   ├── core/              # System skills (updated)
│   │   ├── memory-search/
│   │   ├── rag/
│   │   ├── self-evolution/
│   │   └── web-knowledge/
│   │
│   └── your-skill/        # Your skills (safe) ✅
│
├── scripts/
│   ├── core/              # System scripts (updated)
│   │   ├── activate-features.sh
│   │   ├── add-agent.sh
│   │   └── ...
│   │
│   └── your-script.sh     # Your scripts (safe) ✅
│
├── memory/                # Your memory data (preserved) ✅
├── public/                # Your knowledge base (preserved) ✅
├── data/                  # Your agent data (preserved) ✅
├── USER.md                # Your config (preserved) ✅
├── SOUL.md                # Your config (preserved) ✅
└── README.md              # Template (updated) 📦
```

---

### 🛠️ Post-Installation

#### Activate Features

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/activate-features.sh
```

**Available features:**
1. 🔮 Semantic Search (Ollama + embedding models)
2. 📚 Knowledge Base System
3. 🧬 Self-Evolution System
4. 📊 RAG Evaluation
5. ⏰ Scheduled Tasks (Cron)

#### Add More Agents

```bash
# Single agent
./scripts/core/add-agent.sh coach "Life Coach" 🌱

# Multiple agents
./scripts/core/setup-multi-agent.sh researcher writer organizer
```

---

### 📞 Troubleshooting

**Workspace already exists?**
- Use interactive mode: `bash -c "$(curl ...)" -s agent`
- Or force: `curl ... | bash -s agent --force`

**Agent already registered?**
- Script skips registration automatically
- Your config is preserved

**Scripts not found?**
- Check `scripts/core/` directory
- Update your paths to `scripts/core/script.sh`

---

## 中文 {#中文}

### 🎯 概述

evo-agents 是一个 OpenClaw Workspace 模板，提供多 Agent 协作、脚本工具链和完整文档。

---

### 🚀 一键安装（推荐）⭐

#### 新安装（新 Agent）

**只需一个命令：**

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**就这么简单！** 脚本会自动：
1. 克隆 evo-agents 模板
2. 注册 agent 到 OpenClaw
3. 创建目录结构
4. 运行测试

---

### 🔄 重新安装（现有 Agent）

**已经为这个 Agent 安装过 workspace？**

#### 选项 1: 交互式（推荐）⭐

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s existing-agent
```

**会发生什么：**
- ⚠️ 检测到现有 workspace
- ❓ 询问确认（y/n）
- ✅ 保留你的数据（USER.md, SOUL.md, memory/, public/, skills/, scripts/）
- 📦 更新模板文件（skills/core/, scripts/core/, docs/）

**保留的内容：**
- ✅ 个人配置（USER.md, SOUL.md 等）
- ✅ 记忆数据（memory/ 目录）
- ✅ 知识库（public/ 目录）
- ✅ 你的技能（skills/ 目录）
- ✅ 你的脚本（scripts/ 根目录）

**更新的内容：**
- 📦 通用技能（skills/core/）
- 📦 系统脚本（scripts/core/）
- 📦 文档（README.md 等）

#### 选项 2: 先下载

```bash
curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh
bash install.sh existing-agent
```

#### 选项 3: 强制（跳过确认）

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s existing-agent --force
```

---

### 📋 手动安装

#### 第一步：克隆模板

```bash
git clone https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent
```

#### 第二步：注册到 OpenClaw

```bash
openclaw agents add my-agent --workspace ~/.openclaw/workspace-my-agent
```

#### 第三步：创建目录

```bash
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent
```

#### 第四步：测试

```bash
python3 scripts/core/session_recorder.py -t event -c "Test" --agent my-agent
```

---

### 📁 目录结构

```
workspace/
├── skills/
│   ├── core/              # 系统技能（会更新）
│   │   ├── memory-search/
│   │   ├── rag/
│   │   ├── self-evolution/
│   │   └── web-knowledge/
│   │
│   └── your-skill/        # 你的技能（安全）✅
│
├── scripts/
│   ├── core/              # 系统脚本（会更新）
│   │   ├── activate-features.sh
│   │   ├── add-agent.sh
│   │   └── ...
│   │
│   └── your-script.sh     # 你的脚本（安全）✅
│
├── memory/                # 你的记忆数据（保留）✅
├── public/                # 你的知识库（保留）✅
├── data/                  # 你的 Agent 数据（保留）✅
├── USER.md                # 你的配置（保留）✅
├── SOUL.md                # 你的配置（保留）✅
└── README.md              # 模板（更新）📦
```

---

### 🛠️ 安装后

#### 激活功能

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/activate-features.sh
```

**可用功能：**
1. 🔮 语义搜索（Ollama + 嵌入模型）
2. 📚 知识库系统
3. 🧬 自进化系统
4. 📊 RAG 评估
5. ⏰ 定时任务（Cron）

#### 添加更多 Agent

```bash
# 单个 Agent
./scripts/core/add-agent.sh coach "成长教练" 🌱

# 多个 Agent
./scripts/core/setup-multi-agent.sh researcher writer organizer
```

---

### 📞 故障排除

**Workspace 已存在？**
- 使用交互模式：`bash -c "$(curl ...)" -s agent`
- 或强制：`curl ... | bash -s agent --force`

**Agent 已注册？**
- 脚本自动跳过注册
- 保留你的配置

**找不到脚本？**
- 检查 `scripts/core/` 目录
- 更新路径为 `scripts/core/script.sh`

---

**🎉 准备开始！/ Ready to start!**
