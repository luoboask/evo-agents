# evo-agents

[English](./README.md) | [简体中文](./README.zh-CN.md)

**OpenClaw 多 Agent Workspace 模板**

可复用的自进化 Agent workspace，支持显式运行时上下文（`--workspace`, `--agent`），严格的每 Agent 数据隔离，和共享能力层。

---

## 🦞 OpenClaw 一键安装（推荐）⭐

**用 OpenClaw 自然语言安装：**

```bash
openclaw agent --message "Read https://raw.githubusercontent.com/luoboask/evo-agents/master/workspace-setup.md and help me install a workspace named demo-agent"
```

**OpenClaw 会：**
1. 读取 `workspace-setup.md` 安装指南
2. 克隆模板到 `~/.openclaw/workspace-demo-agent`
3. 创建目录结构
4. 注册 `demo-agent` 到 OpenClaw
5. 配置多 Agent 系统（可选）
6. 运行测试

---

## 🚀 快速开始

### 方式 1：手动安装

```bash
# 1. 克隆模板
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent

# 2. 创建目录结构
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent

# 3. 注册 OpenClaw agent
openclaw agents add my-agent --workspace "$(pwd)" --non-interactive

# 4. 测试
python3 scripts/session_recorder.py -t event -c 'Hello world'
python3 scripts/unified_search.py 'hello' --agent my-agent --semantic
```

---

## 🔧 功能激活

安装完成后，交互式激活高级功能：

```bash
./scripts/activate-features.sh
```

**可激活功能：**
1. 🔮 语义搜索（Ollama + 嵌入模型）
2. 📚 知识库系统
3. 🧬 自进化系统
4. 📊 RAG 评估
5. ⏰ 定时任务（Cron）
6. ✅ 全部激活
7. ❌ 跳过

**嵌入模型选择：**
- bge-m3 (1.2GB, 🇨🇳 中文)
- nomic-embed-text (274MB, 🇺🇸 英文)
- mxbai-embed-large (670MB, 🌍 多语言)
- all-minilm (46MB, 🇺🇸 英文，快速)

**文档：**
- `FEATURE_ACTIVATION_GUIDE.md` - 完整激活指南
- `workspace-setup.md` - 完整安装指南

---

## 🤖 多 Agent 脚本

### setup-multi-agent.sh - 批量创建

```bash
./scripts/setup-multi-agent.sh designer writer ops
# 创建：designer-agent, writer-agent, ops-agent
```

### add-agent.sh - 新增单个

```bash
./scripts/add-agent.sh designer UI/UX 设计师 🎨
# 创建：designer-agent (UI/UX 设计师 🎨)
```

**规则：**
1. 必须传参数（角色名）
2. 自动生成 `role-agent`
3. 如果已带 `-agent`，不再添加

---

## 📁 目录结构

```
evo-agents/
├── 📄 根目录文件
│   ├── README.md
│   ├── README.zh-CN.md
│   ├── workspace-setup.md
│   └── FEATURE_ACTIVATION_GUIDE.md
│
├── 🔧 scripts/
│   ├── activate-features.sh
│   ├── setup-multi-agent.sh
│   ├── add-agent.sh
│   └── ...
│
├── 📚 libs/
│   └── memory_hub/
│
├── 🎯 skills/
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📂 agents/
│   └── .gitkeep
│
└── 📖 docs/
    ├── ARCHITECTURE_GENERIC_CN.md
    └── PROJECT_STRUCTURE_GENERIC_CN.md
```

---

## 📚 文档

| 文档 | 用途 |
|------|------|
| `workspace-setup.md` | ⭐ 完整安装指南 |
| `FEATURE_ACTIVATION_GUIDE.md` | 功能激活指南 |
| `README.md` | 快速入门（英文） |
| `README.zh-CN.md` | 快速入门（中文） |
| `docs/ARCHITECTURE_GENERIC_CN.md` | 架构设计 |
| `docs/PROJECT_STRUCTURE_GENERIC_CN.md` | 目录结构 |

---

**最后更新：** 2026-03-26  
**GitHub:** https://github.com/luoboask/evo-agents
