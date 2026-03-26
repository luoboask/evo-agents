# evo-agents Workspace 安装指南

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🎯 概述

evo-agents 是一个 OpenClaw Workspace 模板，提供多 Agent 协作、脚本工具链和完整文档。

---

## 🚀 一键安装（推荐）⭐

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
