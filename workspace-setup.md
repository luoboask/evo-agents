# evo-agents Workspace 安装指南

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🎯 概述

evo-agents 是一个 OpenClaw Workspace 模板，提供多 Agent 协作、脚本工具链和完整文档。

---

## 🚀 安装方式

### 方式 1：OpenClaw 自然语言安装（推荐）⭐

```bash
openclaw agent --message "Read https://raw.githubusercontent.com/luoboask/evo-agents/master/workspace-setup.md and help me install"
```

### 方式 2：手动安装

```bash
# 1. 克隆 evo-agents 模板（获得 scripts/, skills/, libs/）
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent

# 2. 注册到 OpenClaw（创建 AGENTS.md, SOUL.md 等）
openclaw agents add my-agent --workspace "$(pwd)" --non-interactive

# 3. 创建目录结构
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent

# 4. 测试
python3 scripts/session_recorder.py -t event -c 'Hello world'
```

**为什么需要两步？**
- `git clone` → 获得 evo-agents 的 scripts/, skills/, libs/
- `openclaw agents add` → 创建 AGENTS.md, SOUL.md 等，并注册 agent

---

## 🚀 快速开始

安装完成后：

```bash
cd ~/.openclaw/workspace-my-agent
```

### 新增子 Agent

```bash
# 批量创建
./scripts/setup-multi-agent.sh researcher writer organizer

# 新增单个
./scripts/add-agent.sh coach "成长教练" 🌱
```

---

## 🤖 多 Agent 管理

### setup-multi-agent.sh - 批量创建

```bash
./scripts/setup-multi-agent.sh <role1> [role2] [role3] ...
```

**示例：**
```bash
./scripts/setup-multi-agent.sh researcher writer organizer
```

### add-agent.sh - 新增单个

```bash
./scripts/add-agent.sh <role> [description] [emoji]
```

**示例：**
```bash
./scripts/add-agent.sh coach "成长教练" 🌱
```

---

## 📁 目录结构

```
growth-agents/
├── 📄 根目录文件
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── MEMORY.md
│   └── USER.md
│
├── 🔧 scripts/
│   ├── setup-multi-agent.sh
│   ├── add-agent.sh
│   └── ...
│
├── 🤖 agents/ (可选)
│   └── <sub-agent>/
│
└── ...
```

---

## 🔗 参考

- evo-agents: https://github.com/luoboask/evo-agents
- OpenClaw: https://github.com/openclaw/openclaw

---

## 🔧 功能激活

安装完成后，使用交互式脚本激活高级功能：

```bash
./scripts/activate-features.sh
```

### 可激活功能

| 功能 | 说明 |
|------|------|
| **1. 语义搜索** | Ollama + 嵌入模型（支持中英文） |
| **2. 知识库** | Knowledge Base 知识管理系统 |
| **3. 自进化** | 自动学习和进化系统 |
| **4. RAG 评估** | 检索增强生成评估 |
| **5. 定时任务** | 自动执行日常任务 |

### 嵌入模型选择

| 模型 | 大小 | 语言 | 推荐 |
|------|------|------|------|
| bge-m3 | 1.2GB | 🇨🇳 中文 | 中文用户首选 |
| nomic-embed-text | 274MB | 🇺🇸 英文 | 英文用户首选 |
| mxbai-embed-large | 670MB | 🌍 多语言 | 多语言场景 |
| all-minilm | 46MB | 🇺🇸 英文 | 快速测试 |

### 定时任务

默认配置 3 个定时任务：

1. **夜间循环** - 每天 2:00，自动回顾和总结
2. **分形思考** - 每周日 3:00，深度分析记忆
3. **索引更新** - 每天 3:00，更新语义搜索索引

---

## 📚 完整文档

| 文档 | 用途 |
|------|------|
| `FEATURE_ACTIVATION_GUIDE.md` | 功能激活完整指南 |
| `README.md` | 项目说明（英文） |
| `README.zh-CN.md` | 项目说明（中文） |
| `docs/ARCHITECTURE_GENERIC_CN.md` | 架构设计 |
| `docs/PROJECT_STRUCTURE_GENERIC_CN.md` | 目录结构 |

---

**最后更新：** 2026-03-26
