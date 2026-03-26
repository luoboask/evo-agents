# evo-agents - OpenClaw Workspace 模板

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

**一个完整的 OpenClaw Workspace 模板，包含记忆管理和多 Agent 协作能力。**

[English](./README.md) | [简体中文](./README.zh-CN.md)

---

## 🎯 特性

| 特性 | 说明 |
|------|------|
| **多 Agent 架构** | 主 Agent + 专业子 Agent |
| **数据隔离** | 每个 Agent 独立 memory/ 和 data/ |
| **共享资源** | scripts/libs/skills 所有 Agent 共用 |
| **双向同步** | Markdown ↔ SQLite 自动同步 |
| **语义搜索** | Ollama + bge-m3，理解中文语义 |
| **并发安全** | fcntl 锁 + SQLite WAL 模式 |

---

## 🚀 快速开始

### 方式 1：OpenClaw 一键安装（推荐）⭐

如果你已经安装了 OpenClaw，可以让它读取安装指南并帮你安装：

```bash
# 让 OpenClaw 读取 workspace-setup.md 并安装
openclaw agent --message "Read workspace-setup.md and help me install this workspace template"
```

OpenClaw 会：
1. 读取 `workspace-setup.md` 安装指南
2. 创建目录结构
3. 注册 Agent
4. 配置多 Agent 体系（可选）
5. 运行测试

### 方式 2：一键安装

```bash
# 安装默认名称 'my-agent'
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash

# 或指定自己的 agent 名称
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s your-agent-name
```

### 方式 2：手动安装

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

## 🤖 多 Agent 脚本

### setup-multi-agent.sh - 批量创建多 Agent

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/setup-multi-agent.sh designer writer ops
# 创建：designer-agent, writer-agent, ops-agent
```

### add-agent.sh - 新增单个 Agent

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/add-agent.sh designer UI/UX 设计师 🎨
# 创建：designer-agent (UI/UX 设计师 🎨)
```

**规则：**
1. 必须传参数（角色名）
2. 自动生成 `role-agent`
3. 如果已带 `-agent`，不再添加

详见 `workspace-setup.md` 完整文档。

---

## 📁 目录结构

```
workspace/
├── 📄 根目录文件
│   ├── AGENTS.md           # 会话规范 ⭐
│   ├── SOUL.md             # Agent 身份
│   ├── MEMORY.md           # 长期记忆
│   ├── USER.md             # 用户信息
│   ├── IDENTITY.md         # 身份标识
│   ├── TOOLS.md            # 工具配置
│   └── HEARTBEAT.md        # 心跳检查
│
├── 🔧 scripts/             # 共享脚本
│   ├── session_recorder.py     # 记录事件
│   ├── unified_search.py       # 统一搜索
│   ├── memory_indexer.py       # 构建索引
│   ├── memory_compressor.py    # 压缩沉淀
│   ├── memory_stats.py         # 系统统计
│   ├── health_check.py         # 健康检查
│   ├── setup-multi-agent.sh    # 批量创建 Agent ⭐
│   ├── add-agent.sh            # 新增单个 Agent ⭐
│   └── bridge/                 # 双向同步
│
├── 📚 libs/                  # 共享库
│   └── memory_hub/
│
├── 🎯 skills/                # 共享技能
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📝 memory/                # 记忆目录
│   ├── YYYY-MM-DD.md         # 每日记录
│   ├── weekly/               # 周摘要
│   ├── monthly/              # 月摘要
│   └── archive/              # 归档
│
├── 💾 data/                  # 数据目录
│   ├── <agent-name>/         # Agent 数据
│   └── index/                # 搜索索引
│
├── 🤖 agents/                # 多 Agent（可选）
│   └── <sub-agent>/          # 子 Agent
│
├── 🌐 public/                # 公共知识库
├── 📂 projects/              # Git 库管理
├── ⚙️ config/                # 配置
└── 📖 docs/                  # 文档
```

---

## 🤖 多 Agent 配置（可选）

创建专业子 Agent，实现协作：

```bash
cd ~/.openclaw/workspace-my-agent

# 1. 创建子 Agent 目录
mkdir -p agents/analyst-agent/{memory,data}
mkdir -p agents/developer-agent/{memory,data}
mkdir -p agents/tester-agent/{memory,data}

# 2. 创建配置文件
cat > agents/analyst-agent/AGENTS.md << 'EOF'
# AGENTS.md - analyst-agent

**角色：** 需求分析师  
**职责：** 分析需求、设计方案
EOF

cat > agents/analyst-agent/config.yaml << 'EOF'
agent:
  name: analyst-agent
  role: analyst
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory
EOF

# 3. 使用子 Agent
python3 scripts/session_recorder.py -t event -c '内容' --agent analyst-agent
```

### 协作流程示例

```
1️⃣  analyst-agent    需求分析
    ↓
2️⃣  developer-agent  方案实现
    ↓
3️⃣  tester-agent     质量测试
    ↓
4️⃣  my-agent         总结沉淀
```

---

## 🛠️ 使用方式

### 记录事件

```bash
# 记录到 Agent
python3 scripts/session_recorder.py -t event -c '内容' --agent my-agent

# 记录并自动同步
python3 scripts/session_recorder.py -t decision -c '决策' --agent my-agent --sync
```

### 搜索记忆

```bash
# 关键词搜索
python3 scripts/unified_search.py '关键词' --agent my-agent

# 语义搜索
python3 scripts/unified_search.py '昨天做了什么' --agent my-agent --semantic
```

### 查看统计

```bash
python3 scripts/memory_stats.py --agent my-agent
```

---

## 🔧 依赖

### 必需
- Python 3.10+
- OpenClaw

### 可选
- **jieba** - 中文分词（FTS5 搜索）
- **Ollama** - 语义搜索（bge-m3 模型）

```bash
# 安装 jieba
pip3 install --user jieba

# 安装 Ollama
brew install ollama  # macOS
ollama pull bge-m3   # 中文语义模型
```

---

## 📚 文档

| 文档 | 用途 |
|------|------|
| `workspace-setup.md` | ⭐ 完整安装指南 |
| `docs/ARCHITECTURE_GENERIC_CN.md` | 架构说明（中文） |
| `docs/ARCHITECTURE_GENERIC_EN.md` | Architecture (English) |
| `docs/PROJECT_STRUCTURE_GENERIC_CN.md` | 目录结构（中文） |
| `docs/PROJECT_STRUCTURE_GENERIC_EN.md` | Directory Structure (English) |

---

## 📋 常用命令

| 命令 | 说明 |
|------|------|
| `session_recorder.py -t event -c '...'` | 记录事件 |
| `session_recorder.py -t decision -c '...' --sync` | 记录决策 + 同步 |
| `unified_search.py '关键词'` | 关键词搜索 |
| `unified_search.py '问题' --semantic` | 语义搜索 |
| `bridge_sync.py --agent my-agent` | 双向同步 |
| `memory_indexer.py --incremental --embed` | 增量索引 + 向量 |
| `memory_compressor.py --weekly` | 周摘要 |
| `memory_stats.py --agent my-agent` | 系统统计 |
| `health_check.py --agent my-agent` | 健康检查 |

---

## ⏰ 定时任务

```bash
# 每天凌晨 3 点：增量索引
openclaw cron add --name "daily-index" --cron "0 3 * * *" \
  --system-event "cd /path && python3 scripts/memory_indexer.py --incremental --embed"

# 每 6 小时：双向同步
openclaw cron add --name "bridge-sync" --every "6h" \
  --system-event "cd /path && python3 scripts/bridge/bridge_sync.py --agent my-agent"

# 周一凌晨 4 点：周摘要
openclaw cron add --name "weekly-compress" --cron "0 4 * * 1" \
  --system-event "cd /path && python3 scripts/memory_compressor.py --weekly"
```

---

## 🔄 优雅降级

| 依赖 | 已安装 | 未安装 |
|------|--------|--------|
| **jieba** | FTS5 中文分词 | 降级到 grep |
| **Ollama** | 语义搜索 | 降级到 FTS5 |
| **都没有** | grep + SQLite LIKE | 核心功能可用 |

**最小安装：零依赖** — 只需 Python 3.10+。

---

## 📂 Git 库管理

```bash
# 克隆到 projects/
git clone https://github.com/xxx/lib.git projects/

# 查看
ls -1 projects/

# 删除
rm -rf projects/old-lib/
```

**原则：** 扁平结构，不分类，手动清理。

---

## 📄 许可证

MIT License

---

## 🔗 链接

- **GitHub:** https://github.com/luoboask/evo-agents
- **OpenClaw:** https://github.com/openclaw/openclaw
- **文档:** https://docs.openclaw.ai

---

**最后更新：** 2026-03-26
