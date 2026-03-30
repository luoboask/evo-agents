# evo-agents 完整目录结构

本文档详细说明 evo-agents 安装后的目录结构。

---

## 📁 完整目录树

```
workspace-my-agent/
│
├── 📄 根目录配置文件
│   ├── .gitignore              # Git 忽略规则
│   ├── .install-config         # 安装配置
│   ├── AGENTS.md               # Agent 系统说明
│   ├── SOUL.md                 # Agent 灵魂设定
│   ├── IDENTITY.md             # Agent 身份信息
│   ├── USER.md                 # 用户信息
│   ├── TOOLS.md                # 工具配置
│   ├── HEARTBEAT.md            # 心跳配置
│   ├── README.md               # 项目说明（英文）
│   └── README.zh-CN.md         # 项目说明（中文）
│
├── 📁 agents/                  # 子 Agent 配置目录
│   ├── .gitkeep
│   └── agent-name/             # 子 Agent 配置
│       ├── agent/
│       │   ├── agent.json      # OpenClaw Agent 配置
│       │   └── sessions/       # 会话记录（JSONL）
│       └── config.yaml         # Agent 配置
│
├── 📁 data/                    # 统一数据目录
│   ├── .gitkeep
│   ├── index/
│   │   └── memory_index.db     # 共享索引数据库
│   ├── my-agent/               # 主 Agent 数据
│   │   └── memory/
│   │       ├── memory_stream.db    # 记忆流数据库
│   │       └── knowledge_base.db   # 知识库数据库
│   ├── agent-1/                # 子 Agent 1 数据
│   │   └── memory/
│   │       ├── memory_stream.db
│   │       └── knowledge_base.db
│   └── .locks/                 # 文件锁
│
├── 📁 memory/                  # 记忆文件目录（Markdown）
│   ├── .gitkeep
│   ├── YYYY-MM-DD.md           # 每日记忆文件
│   ├── working_memory_*.jsonl  # 工作记忆
│   ├── weekly/                 # 周记忆（压缩后）
│   ├── monthly/                # 月记忆（压缩后）
│   └── archive/                # 归档记忆
│
├── 📁 public/                  # 公共知识库
│   └── ...
│
├── 📁 scripts/                 # 脚本目录
│   ├── core/                   # 核心脚本
│   │   ├── activate-features.sh
│   │   ├── add-agent.sh
│   │   ├── bridge/
│   │   ├── health_check.py
│   │   ├── memory_indexer.py
│   │   ├── self-check.py
│   │   ├── session_recorder.py
│   │   ├── unified_search.py
│   │   ├── uninstall-agent.sh
│   │   └── uninstall-workspace.sh
│   └── user/                   # 用户自定义脚本
│       └── .gitkeep
│
├── 📁 skills/                  # 技能目录
│   ├── README.md
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── web-knowledge/
│
├── 📁 libs/                    # 库目录
│   ├── memory_hub/
│   └── path_utils/
│
└── 📁 docs/                    # 文档目录
    ├── README.md
    ├── DIRECTORY_STRUCTURE.md
    ├── AGENT_INSTRUCTIONS.md
    ├── SELF_CHECK.md
    └── UNINSTALL.md
```

---

## 📋 关键目录详解

### **1. agents/ vs data/ 的区别**

这是最容易混淆的地方：

| 目录 | 用途 | 内容 |
|------|------|------|
| **`agents/agent-name/`** | Agent 配置 | agent.json, config.yaml, sessions/ |
| **`data/agent-name/`** | Agent 数据 | memory_stream.db, knowledge_base.db |

**为什么分开？**
- `agents/` - OpenClaw 管理的 Agent 配置
- `data/` - 应用层的数据存储（数据库文件）

**示例：**
```
agents/assistant/
├── agent/agent.json       # OpenClaw 配置
├── sessions/*.jsonl       # 会话记录
└── config.yaml            # Agent 配置

data/assistant/
└── memory/
    ├── memory_stream.db   # 记忆流数据库
    └── knowledge_base.db  # 知识库数据库
```

---

### **2. data/ - 统一数据目录**

所有 Agent 的数据都存放在这里，按 Agent 隔离：

```
data/
├── index/memory_index.db    # 共享索引（所有 Agent 共用）
├── my-agent/memory/         # 主 Agent 数据
├── assistant/memory/        # 子 Agent assistant 数据
├── researcher/memory/       # 子 Agent researcher 数据
└── .locks/                  # 文件锁
```

**每个 Agent 的数据：**
- `memory_stream.db` - 记忆流数据库
- `knowledge_base.db` - 知识库数据库

---

### **3. memory/ - 记忆文件目录**

存储 Markdown 格式的记忆文件：

```
memory/
├── 2026-03-30.md           # 每日记忆
├── working_memory.jsonl    # 工作记忆（JSONL）
├── weekly/2026-W14.md      # 周记忆
├── monthly/2026-03.md      # 月记忆
└── archive/2025/           # 归档
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
```

---

### **4. agents/ - 子 Agent 配置目录**

每个子 Agent 的配置：

```
agents/assistant/
├── agent/
│   ├── agent.json          # OpenClaw Agent 配置
│   └── sessions/           # 会话记录
│       ├── sessions.json
│       └── *.jsonl
└── config.yaml             # Agent 配置
```

**创建子 Agent：**
```bash
bash scripts/core/add-agent.sh assistant "我的助手"
```

这会自动创建：
- `agents/assistant/` - 配置目录
- `data/assistant/` - 数据目录

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
│   └── assistant/      # 新增：配置
│       ├── agent/agent.json
│       └── config.yaml
├── data/
│   └── assistant/      # 新增：数据
│       └── memory/
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
| **配置文件** | ~5 个 | .install-config, agent.json, config.yaml |
| **记忆文件** | 每日 1 个 | Markdown 格式 |
| **数据库** | 每 Agent 2 个 | memory_stream + knowledge_base |
| **核心脚本** | ~12 个 | scripts/core/ |
| **技能** | 4 个基础 | memory-search, rag, self-evolution, web-knowledge |

---

## 💡 常见问题

### **Q: agents/ 和 data/ 都有 agent-name，有什么区别？**
**A:** 
- `agents/agent-name/` - OpenClaw 管理的配置
- `data/agent-name/` - 应用层的数据存储

### **Q: 为什么数据不放在 agents/agent-name/ 下？**
**A:** 
- 数据统一存放在 `data/` 便于管理和备份
- `agents/` 只存放配置，由 OpenClaw 管理

### **Q: memory/ 目录的文件会很多吗？**
**A:** 
- 每天一个文件，定期压缩成周记忆、月记忆
- 不会无限增长

---

## 📝 相关文档

- [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) - Agent 指令
- [SELF_CHECK.md](SELF_CHECK.md) - 自检工具
- [UNINSTALL.md](UNINSTALL.md) - 卸载指南

---

**最后更新：** 2026-03-30
