# Unified Memory System

[English](./README.md) | [简体中文](./README.zh-CN.md)

**OpenClaw 统一记忆系统** — 让 AI 真正拥有记忆。

Markdown 为主数据源，SQLite 为搜索索引，双向桥接，语义搜索，自动压缩。

## 🚀 一键安装

```bash
# 1. Clone 模板
openclaw agent add my-agent --workspace ~/.openclaw/workspace-my-agent

# 2. 进入 workspace 初始化
cd ~/.openclaw/workspace-my-agent
mkdir -p memory/weekly memory/monthly memory/archive data/index

# 3. 测试
python3 scripts/session_recorder.py -t event -c '系统初始化完成'
python3 scripts/unified_search.py '初始化' --agent my-agent
```

## ✨ 核心特性

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

- `workspace-setup.md` — 完整安装指南
- `AGENTS.md` — 对话中的记忆流程规范
- `docs/ARCHITECTURE_GENERIC_EN.md` — 架构设计

## 📝 License

MIT
