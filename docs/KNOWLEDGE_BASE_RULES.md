# 知识库管理规范

_公共知识 vs 私人知识 vs Agent 专用知识_

---

## 📊 知识库分类

### 三级知识体系

```
┌─────────────────────────────────────────────────────┐
│              知识库体系                              │
├─────────────────────────────────────────────────────┤
│  L1: 公共知识库 (Public)                            │
│      - 所有 Agent 共享                               │
│      - 通用知识、技能文档                            │
│      - 位置：skills/*/SKILL.md                      │
├─────────────────────────────────────────────────────┤
│  L2: 私人知识库 (Private)                           │
│      - 用户个人数据、偏好                            │
│      - 敏感信息、隐私内容                            │
│      - 位置：MEMORY.md (主会话专用)                 │
├─────────────────────────────────────────────────────┤
│  L3: Agent 专用知识库 (Agent-Specific)              │
│      - 每个 Agent 独立                               │
│      - 任务相关、上下文专用                          │
│      - 位置：data/<agent>/*.db                      │
└─────────────────────────────────────────────────────┘
```

---

## 📁 存储位置

### 1. 公共知识库 (Public)

**位置：** `public/`、`skills/*/` 和 `docs/`

```
workspace/
├── public/                        ← 公共知识库根目录
│   ├── .gitkeep
│   ├── README.md
│   ├── projects/                  ← 公共项目文档
│   └── workflow/                  ← 公共工作流
├── skills/
│   ├── memory-search/SKILL.md     ← 公共技能文档
│   ├── rag/SKILL.md
│   ├── self-evolution/SKILL.md
│   └── web-knowledge/SKILL.md
└── docs/
    ├── SKILL_RULES.md             ← 公共规则
    ├── WORKSPACE_RULES.md
    └── ...
```

**特点：**
- ✅ 所有 Agent 可访问
- ✅ 通用知识
- ❌ 不包含个人隐私

**内容示例：**
- 技能使用文档
- 工具使用说明
- 公共规则和规范
- 技术文档
- 公共项目文档

---

### 2. 私人知识库 (Private)

**位置：** `MEMORY.md` 和 `memory/YYYY-MM-DD.md`

```
workspace/
├── MEMORY.md                       ← 长期私人记忆
└── memory/
    ├── 2026-04-01.md               ← 日常记忆
    ├── 2026-04-02.md
    └── ...
```

**特点：**
- ✅ 仅主会话 Agent 可访问
- ✅ 包含个人隐私
- ❌ 其他 Agent 不可访问

**内容示例：**
- 用户偏好（喜欢吃什么、讨厌什么）
- 个人习惯（作息时间、工作方式）
- 敏感信息（密码提示、安全问题）
- 私人对话记录

**安全规则：**
```
✅ 可以在主会话中读取
✅ 可以记录用户明确要求记住的内容
⚠️ 在群聊中不要引用 MEMORY.md 内容
❌ 不要分享给其他 Agent（除非明确授权）
```

---

### 3. Agent 专用知识库 (Agent-Specific)

**位置：** `data/<agent>/`

```
data/
├── <agent>/
│   ├── knowledge/                 ← Agent 知识库
│   │   └── private/               ← Agent 私有知识
│   │       ├── projects/          ← 项目相关
│   │       │   └── *.json
│   │       └── workflow/          ← 工作流相关
│   │           └── *.json
│   ├── memory_stream.db           ← 记忆流数据库
│   ├── knowledge_base.db          ← 知识库数据库
│   └── config.yaml                ← Agent 配置
├── main-agent/
├── sandbox-agent/
└── tao-admin/
```

**特点：**
- ✅ 每个 Agent 独立数据库
- ✅ 隔离数据，互不干扰
- ✅ 可以安全删除（不影响其他 Agent）
- ⚠️ 包含 Agent 特定的上下文

**内容示例：**
- Agent 任务历史
- Agent 学习到的技能
- Agent 特定上下文
- Agent 配置
- 私有项目文档 (`knowledge/private/projects/`)
- 私有工作流 (`knowledge/private/workflow/`)

**使用规则：**
```
✅ 每个 Agent 只能访问自己的数据库
⚠️ 跨 Agent 数据共享需要明确授权
❌ 不要混用不同 Agent 的数据库
```

**知识存储格式：**
```json
// knowledge/private/projects/*.json
{
  "id": "b5d9ebc0-b3ba-40cc-9570-65ddf53bcb2b",
  "title": "项目名称",
  "content": "项目详情...",
  "tags": ["tag1", "tag2"],
  "created_at": "2026-04-02T10:48:00+08:00",
  "updated_at": "2026-04-02T10:48:00+08:00"
}
```

---

## 🔐 访问权限

### 权限矩阵

| 知识库 | 主 Agent | 子 Agent | 其他 Agent |
|--------|---------|---------|-----------|
| Public (skills/) | ✅ | ✅ | ✅ |
| Private (MEMORY.md) | ✅ | ❌ | ❌ |
| Agent-Specific (data/) | ✅ | ⚠️ | ❌ |

### 访问规则

```python
# ✅ 正确：访问公共知识库
read("skills/memory-search/SKILL.md")

# ✅ 正确：主会话访问私人知识库
if session_type == "main":
    read("MEMORY.md")

# ✅ 正确：Agent 访问自己的数据库
db_path = f"data/{agent_name}/knowledge_base.db"

# ❌ 错误：子 Agent 访问私人知识库
if session_type != "main":
    # 不要读取 MEMORY.md
    pass

# ❌ 错误：访问其他 Agent 的数据库
# 不要读取 data/other-agent/*.db
```

---

## 🗂️ 知识分类指南

### 如何判断知识类型

**问自己三个问题：**

1. **其他 Agent 需要知道吗？**
   - 是 → Public 或 Agent-Specific
   - 否 → Private

2. **包含个人隐私吗？**
   - 是 → Private
   - 否 → Public 或 Agent-Specific

3. **只对这个 Agent 有用吗？**
   - 是 → Agent-Specific
   - 否 → Public

### 分类示例

| 内容 | 类型 | 位置 |
|------|------|------|
| 技能使用文档 | Public | skills/SKILL.md |
| 用户喜欢吃寿司 | Private | MEMORY.md |
| Agent 任务历史 | Agent-Specific | data/<agent>/*.db |
| Workspace 规则 | Public | docs/WORKSPACE_RULES.md |
| 用户密码提示 | Private | MEMORY.md |
| Agent 配置 | Agent-Specific | data/<agent>/config.yaml |
| 错误处理规范 | Public | docs/ERROR_HANDLING.md |
| 用户作息时间 | Private | MEMORY.md |

---

## 🔄 知识流转

### Private → Agent-Specific

**场景：** 用户告诉主 Agent 一个偏好，需要让子 Agent 也知道

```
1. 用户在主会话说："记住我喜欢吃寿司"
2. 主 Agent 记录到 MEMORY.md
3. Spawn 子 Agent 时，通过 task 传递：
   subagent = spawn(
       task="帮用户找寿司店，用户喜欢吃寿司",
       workspace="..."
   )
4. 子 Agent 从 task 中获取信息，记录到自己的数据库
```

**注意：** 不是直接共享数据库，而是通过任务描述传递

---

## ⚠️ 安全警告

### 绝对禁止

```
❌ 在群聊中引用私人记忆
❌ 让子 Agent 直接访问主 Agent 数据库
❌ 把用户密码、密钥写入任何文件
❌ 在 Public 文档中包含个人信息
```

### 必须确认

```
⚠️ 跨 Agent 分享私人信息前询问用户
⚠️ 删除 Agent 数据前确认是否还需要
```

### 最佳实践

```
✅ 敏感信息只保存在 MEMORY.md
✅ Agent 数据定期备份
✅ 公共文档定期清理个人信息
```

---

## 🎯 核心原则

1. **Public** - 通用知识，所有 Agent 共享
2. **Private** - 个人隐私，仅主会话访问
3. **Agent-Specific** - Agent 专用，数据隔离

**记住：安全第一，不确定时选择更保守的方案。**

---

_版本：1.0.0 | 2026-04-01_
