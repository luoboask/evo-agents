# OpenClaw 统一记忆系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

[English](./README.md) | [简体中文](./README.zh-CN.md)

> **让你的 OpenClaw Agent 真正拥有记忆。**
>
> Markdown 为主数据源。SQLite 为搜索索引。双向同步。语义搜索。无需外部 API Key。

**⚠️ 这是 Workspace 模板，不是 Skill。** 如需 SubAgent/Skill 安装，请使用 [unified-memory-skill](https://github.com/luoboask/unified-memory-skill)。

**统一记忆系统**将 OpenClaw 原生 Markdown 记忆与高性能 SQLite 后端桥接，实现语义搜索、自动压缩、并发安全的多会话操作——全部本地运行，只需 Ollama。

## 🚀 安装

### 方式一：一键安装（推荐）

```bash
# 使用默认名称 'my-agent' 安装
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash

# 或指定你自己的 agent 名称
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s your-agent-name
```

示例：
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s growth-assistant
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s demo-agent
```

这将自动完成：
1. 克隆模板到 `~/.openclaw/workspace-{agent-name}`
2. 创建目录结构
3. 注册 OpenClaw agent（`openclaw agents add`）
4. 运行快速测试

**OpenClaw 识别：**
安装后，OpenClaw 会自动识别你的 agent：
```bash
openclaw agents list  # 显示: your-agent-name
openclaw agent --agent your-agent-name --message "你好"
```

### 方式二：手动安装

```bash
# 1. 克隆模板
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent

# 2. 创建目录结构
cd ~/.openclaw/workspace-my-agent
mkdir -p memory/weekly memory/monthly memory/archive data/index

# 3. 注册 OpenClaw agent
openclaw agents add my-agent --workspace $(pwd) --non-interactive

# 4. 测试
python3 scripts/session_recorder.py -t event -c 'Hello world'
python3 scripts/unified_search.py 'hello' --agent my-agent --semantic
```

## ❌ 不适合 SubAgent/Skill 使用

本仓库是**完整的 Workspace 模板**，包含：
- Agent 生命周期文件（AGENTS.md, SOUL.md, MEMORY.md, USER.md）
- 多个集成的技能（self-evolution, rag, websearch）
- Agent 运行时的完整目录结构

**如需 SubAgent 或纯 Skill 安装**，请使用轻量级的 Skill 仓库：

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/luoboask/unified-memory-skill.git unified-memory
```

SubAgent/Skill 用法详见 [unified-memory-skill](https://github.com/luoboask/unified-memory-skill)。

## ✨ 为什么需要这个？

| 特性 | 说明 |
|------|------|
| **双向桥接** | Markdown ↔ SQLite 自动同步，两边数据一致 |
| **语义搜索** | 自然语言提问，bge-m3 理解语义（本地 Ollama，无需 API key） |
| **FTS5 中文** | jieba 分词，精确匹配中文关键词 |
| **智能评分** | 自动判断重要性（决定 8+，学习 6+，事件 5） |
| **自动压缩** | 日→周→月→长期，防止数据膨胀 |
| **并发安全** | fcntl 锁 + SQLite WAL，多会话不丢数据 |

## 📁 目录结构

```
workspace/
├── MEMORY.md                    # 长期核心记忆（LLM 每次读取）
├── memory/
│   ├── 2026-03-25.md            # 每日记录
│   ├── weekly/2026-W13.md       # 周摘要
│   └── monthly/2026-03.md       # 月摘要
├── data/
│   ├── <agent>/memory/          # SQLite 知识系统
│   └── index/memory_index.db    # FTS5 + 向量索引
├── scripts/
│   ├── session_recorder.py      # 记录事件（5 种类型）
│   ├── unified_search.py        # 统一搜索（FTS5 + 语义 + grep）
│   ├── memory_indexer.py        # 建索引（可选 --embed 语义向量）
│   ├── memory_compressor.py     # 压缩 + 沉淀
│   ├── memory_stats.py          # 系统统计
│   ├── health_check.py          # 健康检查 + 自动修复
│   └── bridge/                  # 双向同步
│       ├── bridge_sync.py
│       ├── bridge_to_markdown.py
│       └── bridge_to_knowledge.py
├── libs/memory_hub/             # 原有知识系统（保留兼容）
└── skills/                      # 原有技能（保留兼容）
```

## 🛠️ 快速开始

### 最小安装（零依赖）

只需要 Python 3.10+，开箱即用。

```bash
# 记录事件
python3 scripts/session_recorder.py -t event -c '今天完成了重要工作'

# 搜索（自动选择最佳方式）
python3 scripts/unified_search.py '重要工作' --agent my-agent
```

### 推荐增强（可选）

**1. FTS5 中文分词（推荐）**

```bash
pip3 install jieba  # 或 pip3 install --user --break-system-packages jieba
python3 scripts/memory_indexer.py --full
```

**2. 语义搜索（推荐，中文效果好）**

```bash
# 安装 Ollama
brew install ollama  # macOS
# 或访问 https://ollama.com/download

# 启动并下载模型
ollama serve
ollama pull bge-m3  # 1.2GB，中文好
# 或 ollama pull nomic-embed-text  # 274MB，英文好

# 建立语义索引
python3 scripts/memory_indexer.py --full --embed

# 语义搜索
python3 scripts/unified_search.py '昨天做了什么' --semantic
```

## 💬 对话中的记忆流程

**AGENTS.md 已集成完整规范**，每次对话自动遵循：

### 对话开始时：搜记忆
用户提到之前的事 → 先搜再答：
```bash
python3 scripts/unified_search.py '相关关键词' --agent my-agent --semantic
```

### 对话过程中：实时记录
发现重要信息 → 立刻记录：
```bash
python3 scripts/session_recorder.py -t decision -c '用户决定使用 X 方案' --sync
python3 scripts/session_recorder.py -t learning -c '学到了 Y 知识点' --sync
python3 scripts/session_recorder.py -t event -c '发生了 Z 事件' --sync
```

### 对话结束时：同步
如果记录了内容 → 自动同步（`--sync` 已后台执行）

## 🔧 常用命令

| 命令 | 说明 |
|------|------|
| `session_recorder.py -t event -c '...'` | 记录事件 |
| `session_recorder.py -t decision -c '...' --sync` | 记录决定并自动同步 |
| `unified_search.py '关键词'` | 关键词搜索 |
| `unified_search.py '问题' --semantic` | 语义搜索 |
| `bridge_sync.py --agent my-agent` | 双向同步 |
| `memory_indexer.py --incremental --embed` | 增量索引+向量 |
| `memory_compressor.py --weekly` | 生成周摘要 |
| `memory_stats.py --agent my-agent` | 系统统计 |
| `health_check.py --agent my-agent` | 健康检查 |

## ⏰ 定时任务（推荐）

```bash
# 每天 03:00：增量索引
openclaw cron add --name "daily-index" --cron "0 3 * * *" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_indexer.py --incremental --embed"

# 每 6 小时：双向同步
openclaw cron add --name "bridge-sync" --every "6h" \
  --system-event "cd /path/to/workspace && python3 scripts/bridge/bridge_sync.py --agent my-agent"

# 每周一 04:00：周摘要
openclaw cron add --name "weekly-compress" --cron "0 4 * * 1" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_compressor.py --weekly"
```

## 🔄 功能降级

| 依赖 | 安装了 | 没安装 |
|------|--------|--------|
| **jieba** | FTS5 中文分词 | 退回 grep（能用但慢） |
| **Ollama + 模型** | 语义搜索（自然语言） | 退回 FTS5 或 grep |
| **两者都没有** | grep + SQLite LIKE | 基本功能完整可用 |

**最小安装零依赖** — 只要有 Python 3.10+ 就能跑。

## 📚 文档

- `README.md` / `README.zh-CN.md` — 本文档
- `workspace-setup.md` — 完整安装指南
- `AGENTS.md` — 对话中的记忆流程规范
- `docs/ARCHITECTURE_GENERIC_EN.md` — 架构设计

## 📝 License

MIT
