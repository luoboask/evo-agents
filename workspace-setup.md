# growth-agents Workspace 安装指南

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🎯 概述

growth-agents 是一个基于 evo-agents 架构的 OpenClaw Workspace，专注于个人成长和自进化。

---

## 🚀 快速开始

### 使用已有安装

```bash
cd ~/.openclaw/workspace-growth-agents
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
