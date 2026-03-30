# 子 Agent 目录结构

本文档详细说明子 Agent 的目录结构。

---

## 📁 完整目录结构

```
workspace-my-agent/
│
├── agents/                        # 子 Agent 配置目录
│   ├── .gitkeep
│   └── sub-agent/                 # 子 Agent 目录
│       ├── agent/
│       │   ├── agent.json         # OpenClaw Agent 配置
│       │   └── sessions/          # 会话记录
│       ├── skills/                # 子 Agent 专属技能
│       │   └── custom-skill/      # 自定义技能
│       ├── skills-parent/         # 父 Agent 技能（符号链接）
│       │   └── -> ../../skills/
│       ├── scripts/               # 子 Agent 专属脚本
│       ├── libs/                  # 子 Agent 专属库
│       ├── memory/                # 子 Agent 记忆
│       │   └── YYYY-MM-DD.md
│       ├── data/                  # 子 Agent 数据
│       │   └── memory/
│       │       ├── memory_stream.db
│       │       └── knowledge_base.db
│       └── config.yaml            # Agent 配置
│
├── data/                          # 统一数据目录
│   ├── index/memory_index.db      # 共享索引
│   ├── my-agent/                  # 主 Agent 数据
│   └── sub-agent/                 # 子 Agent 数据
│       └── memory/
│
├── skills/                        # 父 Agent 技能
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── web-knowledge/
│
└── memory/                        # 父 Agent 记忆
    └── YYYY-MM-DD.md
```

---

## 📋 关键目录说明

### **1. agents/sub-agent/ - 子 Agent 配置**

| 目录/文件 | 用途 | 说明 |
|----------|------|------|
| `agent/agent.json` | OpenClaw 配置 | OpenClaw 管理的 Agent 配置 |
| `agent/sessions/` | 会话记录 | OpenClaw 会话记录（JSONL） |
| `config.yaml` | Agent 配置 | Agent 角色、描述等配置 |

### **2. agents/sub-agent/skills/ - 专属技能**

**用途：** 存放子 Agent 专属技能

**示例：**
```
agents/sub-agent/skills/
└── my-custom-skill/
    ├── SKILL.md
    └── ...
```

### **3. agents/sub-agent/skills-parent/ - 共享父 Agent 技能**

**用途：** 符号链接，指向父 Agent 的 `skills/` 目录

**结构：**
```
agents/sub-agent/skills-parent/ -> ../../skills/
```

**访问方式：**
```bash
cd agents/sub-agent
ls skills-parent/  # 查看父 Agent 技能
```

### **4. data/sub-agent/ - 子 Agent 数据**

**用途：** 存储子 Agent 的数据（数据库文件）

**结构：**
```
data/sub-agent/memory/
├── memory_stream.db    # 记忆流数据库
└── knowledge_base.db   # 知识库数据库
```

---

## 🔧 创建子 Agent

### **自动创建**

```bash
cd ~/.openclaw/workspace-my-agent
bash scripts/core/add-agent.sh sub-agent "描述"
```

这会自动创建：
- ✅ `agents/sub-agent/` - 配置目录
- ✅ `agents/sub-agent/skills/` - 专属技能目录
- ✅ `agents/sub-agent/skills-parent/` - 共享技能链接
- ✅ `data/sub-agent/` - 数据目录

### **手动初始化数据**

```bash
bash scripts/core/init-agent-data.sh sub-agent
```

---

## 💡 使用示例

### **1. 创建专属技能**

```bash
cd agents/sub-agent/skills/
mkdir my-skill
cd my-skill
# 创建 SKILL.md 等文件
```

### **2. 访问父 Agent 技能**

```bash
cd agents/sub-agent/
ls skills-parent/  # 查看父 Agent 技能
cd skills-parent/memory-search/  # 访问父 Agent 技能
```

### **3. 记录子 Agent 记忆**

```bash
python3 scripts/core/session_recorder.py -t event -c "内容" --agent sub-agent
```

---

## ❌ 常见问题

### **问题 1: 找不到子 Agent 技能**

**原因：** 技能放在错误的位置

**解决：**
- 专属技能放在 `agents/sub-agent/skills/`
- 共享技能通过 `agents/sub-agent/skills-parent/` 访问

### **问题 2: 数据目录不存在**

**原因：** 未初始化数据目录

**解决：**
```bash
bash scripts/core/init-agent-data.sh sub-agent
```

---

## 📝 相关文档

- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - 完整目录结构
- [SUB_AGENT_DATA.md](SUB_AGENT_DATA.md) - 子 Agent 数据初始化
- [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) - Agent 指令

---

**最后更新：** 2026-03-30
