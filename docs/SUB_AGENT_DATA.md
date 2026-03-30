# 子 Agent 数据初始化指南

本文档说明如何为子 Agent 初始化数据目录和数据库。

---

## 📁 子 Agent 数据结构

每个子 Agent 都有独立的数据目录：

```
data/
├── index/memory_index.db        # 共享索引
├── my-agent/                    # 主 Agent 数据
│   └── memory/
│       ├── memory_stream.db
│       └── knowledge_base.db
└── sub-agent/                   # 子 Agent 数据
    └── memory/
        ├── memory_stream.db     # 记忆流数据库
        └── knowledge_base.db    # 知识库数据库
```

---

## 🔧 初始化方法

### **方法 1: 自动初始化（推荐）**

创建子 Agent 后，系统会自动初始化数据目录。

### **方法 2: 手动初始化**

```bash
cd ~/.openclaw/workspace-my-agent
bash scripts/core/init-agent-data.sh sub-agent-name
```

### **方法 3: 使用 OpenClaw 命令**

```bash
openclaw agent --agent sub-agent-name --message "初始化"
```

这会自动创建必要的数据目录和数据库。

---

## 📋 初始化内容

初始化脚本会创建：

1. **数据目录**
   ```
   data/sub-agent-name/memory/
   ```

2. **数据库文件**
   - `memory_stream.db` - 记忆流数据库
   - `knowledge_base.db` - 知识库数据库

3. **数据库表**
   - `memories` 表 - 存储记忆
   - `knowledge` 表 - 存储知识

---

## ❌ 常见问题

### **问题 1: 记忆系统不可用**

**错误：** `database is not open`

**原因：** 子 Agent 数据目录未创建

**解决：**
```bash
bash scripts/core/init-agent-data.sh sub-agent-name
```

### **问题 2: 知识库不可用**

**错误：** `knowledge_base.db not found`

**原因：** 知识库数据库未初始化

**解决：** 同上，运行初始化脚本

---

## 📝 相关文档

- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - 完整目录结构
- [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) - Agent 指令

---

**最后更新：** 2026-03-30
