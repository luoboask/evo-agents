# evo-agents 完整目录结构

本文档详细说明 evo-agents 安装后的目录结构，帮助用户理解每个文件和目录的用途。

---

## 📁 完整目录树

```
workspace-my-agent/
│
├── 📄 根目录配置文件
│   ├── .gitignore                    # Git 忽略规则
│   ├── .install-config               # 安装配置信息
│   ├── AGENTS.md                     # Agent 系统说明
│   ├── SOUL.md                       # Agent 灵魂设定
│   ├── IDENTITY.md                   # Agent 身份信息
│   ├── USER.md                       # 用户信息配置
│   ├── TOOLS.md                      # 工具配置说明
│   ├── HEARTBEAT.md                  # 心跳配置
│   ├── README.md                     # 项目说明（英文）
│   └── README.zh-CN.md               # 项目说明（中文）
│
├── 📁 agents/                        # 子 Agent 目录
│   ├── .gitkeep
│   └── agent-name/                   # 每个子 Agent 的独立目录
│       ├── agent/
│       │   ├── agent.json            # OpenClaw Agent 配置
│       │   └── sessions/             # 会话记录
│       ├── memory/                   # Agent 记忆
│       │   └── YYYY-MM-DD.md         # 每日记忆文件
│       ├── data/                     # Agent 数据
│       │   └── memory/
│       │       ├── memory_stream.db  # 记忆流数据库
│       │       └── knowledge_base.db # 知识库数据库
│       └── config.yaml               # Agent 配置
│
├── 📁 data/                          # 数据目录
│   ├── .gitkeep
│   ├── index/
│   │   └── memory_index.db           # 记忆索引数据库
│   ├── my-agent/                     # 主 Agent 数据
│   │   └── memory/
│   ├── agent-1/                      # 子 Agent 1 数据
│   │   └── memory/
│   └── .locks/                       # 文件锁
│
├── 📁 memory/                        # 记忆文件目录
│   ├── .gitkeep
│   ├── YYYY-MM-DD.md                 # 每日记忆
│   ├── working_memory_*.jsonl        # 工作记忆
│   ├── weekly/                       # 周记忆（压缩后）
│   ├── monthly/                      # 月记忆（压缩后）
│   └── archive/                      # 归档记忆
│
├── 📁 public/                        # 公共知识库
│   ├── README.md
│   └── ...
│
├── 📁 scripts/                       # 脚本目录
│   ├── core/                         # 核心脚本
│   │   ├── activate-features.sh      # 激活高级功能
│   │   ├── add-agent.sh              # 添加子 Agent
│   │   ├── bridge/                   # 桥接脚本
│   │   │   ├── bridge_sync.py        # 双向同步
│   │   │   ├── bridge_to_knowledge.py
│   │   │   └── bridge_to_markdown.py
│   │   ├── health_check.py           # 健康检查
│   │   ├── memory_indexer.py         # 记忆索引
│   │   ├── memory_compressor.py      # 记忆压缩
│   │   ├── self-check.py             # 自检工具
│   │   ├── session_recorder.py       # 会话记录
│   │   ├── unified_search.py         # 统一搜索
│   │   ├── uninstall-agent.sh        # 卸载子 Agent
│   │   └── uninstall-workspace.sh    # 卸载 workspace
│   └── user/                         # 用户自定义脚本
│       └── .gitkeep
│
├── 📁 skills/                        # 技能目录
│   ├── README.md
│   ├── memory-search/                # 记忆搜索技能
│   ├── rag/                          # RAG 评估技能
│   ├── self-evolution/               # 自进化技能
│   └── web-knowledge/                # 网络知识技能
│
├── 📁 libs/                          # 库目录
│   ├── memory_hub/                   # 记忆中心库
│   └── path_utils/                   # 路径工具库
│
└── 📁 docs/                          # 文档目录
    ├── README.md
    ├── AGENT_INSTRUCTIONS.md
    ├── SELF_CHECK.md
    ├── UNINSTALL.md
    ├── WORKSPACE_RULES.md
    └── DIRECTORY_STRUCTURE.md        # 本文档
```

---

## 📋 关键目录详解

### **1. agents/ - 子 Agent 目录**

每个子 Agent 都有独立的配置和数据：

```
agents/assistant/
├── agent/agent.json       # OpenClaw Agent 配置
├── memory/2026-03-30.md   # 记忆文件
├── data/assistant/memory/ # 数据目录
└── config.yaml            # Agent 配置
```

**创建子 Agent：**
```bash
bash scripts/core/add-agent.sh assistant "我的助手"
```

---

### **2. data/ - 数据目录**

按 Agent 隔离存储数据：

```
data/
├── index/memory_index.db    # 共享索引数据库
├── my-agent/memory/         # 主 Agent 数据
├── assistant/memory/        # 子 Agent 数据
└── .locks/                  # 文件锁
```

**每个 Agent 的数据：**
- `memory_stream.db` - 记忆流数据库
- `knowledge_base.db` - 知识库数据库

---

### **3. memory/ - 记忆目录**

存储所有记忆文件：

```
memory/
├── 2026-03-30.md           # 每日记忆
├── working_memory.jsonl    # 工作记忆（JSONL 格式）
├── weekly/2026-W14.md      # 周记忆（压缩后）
├── monthly/2026-03.md      # 月记忆（压缩后）
└── archive/2025/           # 归档记忆
```

**每日记忆文件格式：**
```markdown
# 2026-03-30 - 会话记录

## 📌 事件
- [09:00] 用户说...

## 🔨 决定
- [09:05] 决定...

## 📚 学习
- [09:10] 学习到...

## 💭 反思
- [09:15] 反思...
```

---

### **4. scripts/core/ - 核心脚本**

| 脚本 | 功能 | 常用命令 |
|------|------|---------|
| `activate-features.sh` | 激活高级功能 | 交互式选择 |
| `add-agent.sh` | 添加子 Agent | `./add-agent.sh name "描述"` |
| `memory_indexer.py` | 索引记忆 | `--full`, `--incremental`, `--embed` |
| `unified_search.py` | 搜索记忆 | `关键词` |
| `self-check.py` | 自检工具 | 无参数 |
| `uninstall-agent.sh` | 卸载子 Agent | `agent-name` |
| `uninstall-workspace.sh` | 卸载 workspace | 交互式 |

---

### **5. skills/ - 技能目录**

| 技能 | 用途 |
|------|------|
| `memory-search/` | 记忆搜索（关键词 + 语义） |
| `rag/` | RAG 评估系统 |
| `self-evolution/` | 自进化系统 |
| `web-knowledge/` | 网络知识获取 |

---

## 🎯 典型使用场景

### **场景 1: 刚安装后**
```
workspace-my-agent/
├── agents/.gitkeep     # 空
├── data/.gitkeep       # 空
├── memory/.gitkeep     # 空
└── scripts/            # 核心脚本
```

### **场景 2: 创建 1 个子 Agent 后**
```bash
bash scripts/core/add-agent.sh assistant "我的助手"
```

```
workspace-my-agent/
├── agents/
│   └── assistant/      # 新增子 Agent
├── data/
│   └── assistant/      # 新增数据目录
└── memory/
    └── 2026-03-30.md   # 开始记录记忆
```

### **场景 3: 使用一段时间后**
```
workspace-my-agent/
├── agents/
│   ├── assistant/
│   └── researcher/
├── data/
│   ├── index/memory_index.db
│   ├── my-agent/
│   ├── assistant/
│   └── researcher/
├── memory/
│   ├── 2026-03-30.md
│   ├── 2026-03-31.md
│   └── working_memory.jsonl
└── data/*/memory/*.db
```

---

## 📊 文件统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **配置文件** | ~5 个 | 安装配置、Agent 配置 |
| **记忆文件** | 每日 1 个 | Markdown 格式 |
| **数据库** | 每 Agent 2 个 | memory_stream + knowledge_base |
| **核心脚本** | ~15 个 | scripts/core/ |
| **技能** | 4 个基础 | memory-search, rag, self-evolution, web-knowledge |
| **文档** | ~12 个 | docs/ 目录 |

---

## 💡 常见问题

### **Q: agents/ 目录什么时候创建？**
A: 使用 `add-agent.sh` 创建子 Agent 时自动创建。

### **Q: data/ 目录为什么有多个子目录？**
A: 每个 Agent 有独立的数据目录，实现数据隔离。

### **Q: memory/ 目录的文件会很多吗？**
A: 每天一个文件，定期会压缩成周记忆、月记忆。

### **Q: 可以手动修改记忆文件吗？**
A: 可以，但建议使用 `session_recorder.py` 记录。

---

## 📝 相关文档

- [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) - Agent 指令
- [SELF_CHECK.md](SELF_CHECK.md) - 自检工具说明
- [UNINSTALL.md](UNINSTALL.md) - 卸载指南
- [WORKSPACE_RULES.md](WORKSPACE_RULES.md) - workspace 规则

---

**最后更新：** 2026-03-30
