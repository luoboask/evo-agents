# 子 Agent 数据目录结构

本文档说明子 Agent 的数据存储结构。

---

## 📁 正确的目录结构

```
workspace-my-agent/
├── agents/                    # Agent 配置目录
│   └── sub-agent/
│       ├── agent/agent.json   # OpenClaw 配置
│       ├── config.yaml        # Agent 配置
│       └── sessions/          # 会话记录
│
└── data/                      # 统一数据目录
    └── sub-agent/
        └── memory/
            ├── memory_stream.db    # 记忆流数据库
            └── knowledge_base.db   # 知识库数据库
```

---

## ⚠️ 重要说明

### **不要创建 agents/sub-agent/data/**

`add-agent.sh` 可能会创建 `agents/sub-agent/data/` 目录，但这是**空的，不使用**。

**正确的数据目录是：** `data/sub-agent/`（在 workspace 根目录下）

---

## 🔧 初始化子 Agent 数据

### **方法 1: 自动初始化**

使用子 Agent 时会自动创建数据目录。

### **方法 2: 手动初始化**

```bash
cd ~/.openclaw/workspace-my-agent
bash scripts/core/init-agent-data.sh sub-agent-name
```

---

## ❌ 常见问题

### **问题：记忆系统不可用**

**错误：** `database is not open`

**原因：** 数据目录未创建

**解决：**
```bash
bash scripts/core/init-agent-data.sh sub-agent-name
```

---

## 📝 相关文档

- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - 完整目录结构
- [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) - Agent 指令

---

**最后更新：** 2026-03-30
