# evo-agents Workspace 安装指南

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🎯 概述

evo-agents 是一个完整的 OpenClaw Workspace 模板，包含：
- Agent 生命周期文件（AGENTS.md, SOUL.md, MEMORY.md, USER.md）
- 多个集成技能（self-evolution, rag, websearch, memory-search）
- 完整的多 Agent 目录结构
- 双向同步系统（Markdown ↔ SQLite）
- 语义搜索支持（Ollama）

---

## 🚀 安装方式

### 方式 1：一键安装（推荐）

```bash
# 安装默认名称 'my-agent'
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash

# 或指定自己的 agent 名称
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s your-agent-name
```

**示例：**
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s growth-assistant
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s demo-agent
```

**这将：**
1. 克隆模板到 `~/.openclaw/workspace-{agent-name}`
2. 创建目录结构
3. 注册 OpenClaw agent（`openclaw agents add`）
4. 运行快速测试

**OpenClaw 识别：**
安装后，OpenClaw 会识别你的 agent：
```bash
openclaw agents list  # 显示：your-agent-name
openclaw agent --agent your-agent-name --message "Hello"
```

---

### 方式 2：手动安装

```bash
# 1. 克隆模板
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent

# 2. 创建目录结构
cd ~/.openclaw/workspace-my-agent
mkdir -p memory/weekly memory/monthly memory/archive data/index

# 3. 注册 OpenClaw agent
openclaw agents add my-agent --workspace "$(pwd)" --non-interactive

# 4. 测试
python3 scripts/session_recorder.py -t event -c 'Hello world'
python3 scripts/unified_search.py 'hello' --agent my-agent --semantic
```

---

## ❌ 不适用于 SubAgent/Skill

本仓库是**完整的 Workspace 模板**，包含：
- Agent 生命周期文件（AGENTS.md, SOUL.md, MEMORY.md, USER.md）
- 多个集成技能（self-evolution, rag, websearch）
- 完整的运行时目录结构

**对于 SubAgent 或仅 Skill 安装**，使用轻量级 skill 仓库：

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/luoboask/unified-memory-skill.git unified-memory
```

查看 [unified-memory-skill](https://github.com/luoboask/unified-memory-skill) 了解 SubAgent/Skill 用法。

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| **双向桥接** | Markdown ↔ SQLite 自动同步，数据一致 |
| **语义搜索** | 自然语言查询，bge-m3 理解语义（本地 Ollama，无需 API key） |
| **FTS5 中文** | jieba 分词，精确中文关键词匹配 |
| **智能评分** | 自动重要性（决策 8+，学习 6+，事件 5+） |
| **自动压缩** | 日→周→月→长期，防止数据膨胀 |
| **并发安全** | fcntl 锁 + SQLite WAL，多会话无数据丢失 |

---

## 📁 目录结构

```
workspace/
├── MEMORY.md                    # 长期核心记忆（LLM 每次会话读取）
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
│   ├── memory_indexer.py        # 构建索引（可选 --embed 向量）
│   ├── memory_compressor.py     # 压缩 + 沉淀
│   ├── memory_stats.py          # 系统统计
│   ├── health_check.py          # 健康检查 + 自动修复
│   └── bridge/                  # 双向同步
│       ├── bridge_sync.py
│       ├── bridge_to_markdown.py
│       └── bridge_to_knowledge.py
├── libs/memory_hub/             # 原始知识系统（向后兼容）
└── skills/                      # 原始技能（向后兼容）
```

---

## 🛠️ 快速开始

### 最小安装（零依赖）

只需 Python 3.10+，开箱即用。

```bash
# 记录事件
python3 scripts/session_recorder.py -t event -c '今天完成了重要工作'

# 搜索（自动选择最佳方法）
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
ollama pull bge-m3  # 1.2GB，中文效果好
# 或 ollama pull nomic-embed-text  # 274MB，英文效果好

# 构建语义索引
python3 scripts/memory_indexer.py --full --embed

# 语义搜索
python3 scripts/unified_search.py '我昨天做了什么' --semantic
```

---

## 💬 会话中的记忆流

**AGENTS.md 包含完整的规范**，每次会话自动遵循：

### 会话开始：搜索记忆

当用户提到之前的事情 → 先搜索，再回答：
```bash
python3 scripts/unified_search.py '相关关键词' --agent my-agent --semantic
```

### 会话中：实时记录

发现重要信息 → 立即记录：
```bash
python3 scripts/session_recorder.py -t decision -c '用户决定使用 X 方案' --sync
python3 scripts/session_recorder.py -t learning -c '学习了 Y 知识点' --sync
python3 scripts/session_recorder.py -t event -c '发生了 Z 事件' --sync
```

### 会话结束：同步

如果记录了内容 → 自动同步（`--sync` 后台运行）

---

## 🔧 常用命令

| 命令 | 说明 |
|------|------|
| `session_recorder.py -t event -c '...'` | 记录事件 |
| `session_recorder.py -t decision -c '...' --sync` | 记录决策并自动同步 |
| `unified_search.py '关键词'` | 关键词搜索 |
| `unified_search.py '问题' --semantic` | 语义搜索 |
| `bridge_sync.py --agent my-agent` | 双向同步 |
| `memory_indexer.py --incremental --embed` | 增量索引 + 向量 |
| `memory_compressor.py --weekly` | 生成周摘要 |
| `memory_stats.py --agent my-agent` | 系统统计 |
| `health_check.py --agent my-agent` | 健康检查 |

---

## ⏰ 定时任务（推荐）

```bash
# 每天凌晨 3 点：增量索引
openclaw cron add --name "daily-index" --cron "0 3 * * *" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_indexer.py --incremental --embed"

# 每 6 小时：双向同步
openclaw cron add --name "bridge-sync" --every "6h" \
  --system-event "cd /path/to/workspace && python3 scripts/bridge/bridge_sync.py --agent my-agent"

# 周一凌晨 4 点：周摘要
openclaw cron add --name "weekly-compress" --cron "0 4 * * 1" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_compressor.py --weekly"
```

---

## 🔄 优雅降级

| 依赖 | 已安装 | 未安装 |
|------|--------|--------|
| **jieba** | FTS5 中文分词 | 降级到 grep（慢但可用） |
| **Ollama + 模型** | 语义搜索（自然语言） | 降级到 FTS5 或 grep |
| **都没有** | grep + SQLite LIKE | 核心功能完全可用 |

**最小安装零依赖** — 只需 Python 3.10+。

---

## 📚 文档

- `README.md` / `README.zh-CN.md` — 本文档
- `workspace-setup.md` — 完整安装指南
- `AGENTS.md` — 会话记忆流规范
- `docs/ARCHITECTURE_GENERIC_CN.md` — 架构设计

---

## 📄 许可证

MIT
