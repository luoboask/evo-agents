# Workspace 规则

_目录结构、文件存放、工作规范_

---

## 📁 目录结构

```
workspace/
├── AGENTS.md                  # Agent 行为规范（启动必读）
├── SOUL.md                    # Agent 人格定义
├── USER.md                    # 用户信息
├── MEMORY.md                  # 长期记忆
├── HEARTBEAT.md               # 心跳检查配置
├── IDENTITY.md                # Agent 身份
│
├── docs/                      # 📚 文档目录
│   ├── SKILL_RULES.md         # 技能使用规则
│   ├── SCHEDULER.md           # 定时任务配置
│   └── WORKSPACE_RULES.md     # 本文档
│
├── memory/                    # 🧠 记忆存储
│   ├── YYYY-MM-DD.md          # 日常记忆（每天一个文件）
│   └── memory_stream.db       # 记忆流数据库
│
├── skills/                    # 🛠️ 技能目录
│   ├── memory-search/         # 记忆搜索
│   ├── rag/                   # RAG 评估
│   ├── self-evolution/        # 自进化系统
│   └── web-knowledge/         # 网页搜索
│
├── data/                      # 📦 数据存储
│   ├── <agent>/               # 各 Agent 专用数据
│   │   ├── memory_stream.db   # 记忆数据库
│   │   └── knowledge_base.db  # 知识库
│   └── index/                 # 索引文件
│
├── libs/                      # 📚 共享库
│   └── memory_hub/            # 记忆管理核心库
│
├── agents/                    # 🤖 子 Agent 配置
│   ├── sandbox-agent/         # 沙箱 Agent
│   └── tao-admin/             # 电商 Agent
│
├── scripts/                   # 🔧 脚本工具
│   ├── init_agent.py          # Agent 初始化
│   └── batch_embeddings.py    # 批量嵌入
│
├── projects/                  # 📂 临时项目（短期）
│   └── <project-name>/        # 项目目录
│
└── logs/                      # 📝 日志目录（如需要）
```

---

## 📥 文件存放规则

### 1. 临时下载文件

**位置：** `/tmp/` 或 `projects/`

```bash
# ✅ 正确：下载到 /tmp/
cd /tmp && wget https://example.com/file.zip

# ✅ 正确：下载到 projects/
cd ~/workspace/projects && wget https://example.com/file.zip

# ❌ 错误：不要下载到 workspace 根目录
cd ~/workspace && wget ...  # 会污染 workspace
```

**清理规则：**
- `/tmp/` - 系统定期清理，无需手动
- `projects/` - 项目完成后询问用户是否删除

---

### 2. Git 项目

**位置：** `/tmp/` 或 `~/projects/` 或 `data/<agent>/work/`

```bash
# ✅ 正确：临时项目
cd /tmp && git clone https://github.com/user/repo.git

# ✅ 正确：长期项目
cd ~/projects && git clone https://github.com/user/repo.git

# ✅ 正确：Agent 专用项目
cd ~/.openclaw/workspace/data/<agent>/work && git clone ...

# ❌ 错误：不要克隆到 workspace 根目录
cd ~/workspace && git clone ...  # 会污染 workspace
```

**选择指南：**

| 项目类型 | 位置 | 清理时机 |
|---------|------|---------|
| 临时查看 | `/tmp/` | 系统自动清理 |
| 短期开发 | `projects/` | 完成后删除 |
| 长期使用 | `~/projects/` | 保留 |
| Agent 专用 | `data/<agent>/work/` | 根据需求 |

---

### 3. 知识库

**位置：** `data/<agent>/knowledge_base.db`

```
data/
└── main-agent/
    ├── knowledge_base.db      # 结构化知识
    ├── memory_stream.db       # 记忆流
    └── config.yaml            # Agent 配置
```

**规则：**
- ✅ 每个 Agent 独立数据库
- ✅ 自动创建，无需手动
- ✅ 通过 `self-evolution` 技能管理
- ❌ 不要直接修改数据库文件

---

### 4. 记忆存储

**位置：** `memory/` 和 `data/<agent>/`

```
# 日常记忆（文本）
memory/
├── 2026-04-01.md
├── 2026-04-02.md
└── ...

# 数据库记忆（结构化）
data/<agent>/
├── memory_stream.db
└── knowledge_base.db
```

**规则：**
- ✅ 每天自动创建 `memory/YYYY-MM-DD.md`
- ✅ 重要事件记录到 `MEMORY.md`
- ✅ 数据库由系统自动管理
- ❌ 不要手动修改数据库

---

### 5. 配置文件

**位置：** workspace 根目录 或 `data/<agent>/`

```
# 全局配置
~/workspace/
├── AGENTS.md
├── SOUL.md
└── config.yaml (如有)

# Agent 专用配置
data/<agent>/
└── config.yaml
```

---

## 🚫 禁止操作

### 根目录禁止

```bash
# ❌ 不要在 workspace 根目录创建文件
cd ~/workspace
touch new-file.txt          # ❌
mkdir new-folder            # ❌
git clone ...               # ❌
wget ...                    # ❌

# ✅ 正确做法
cd /tmp                     # 临时文件
cd ~/workspace/projects     # 项目
cd ~/workspace/data/<agent>/work  # Agent 专用
```

### 敏感目录禁止

```bash
# ❌ 不要修改
.git/                       # Git 配置
.openclaw/                  # OpenClaw 系统
data/<agent>/*.db           # 数据库文件（除非明确需要）
```

---

## ✅ 推荐操作

### 创建新文件

```bash
# ✅ 文档
cd ~/workspace/docs && touch new-doc.md

# ✅ 脚本
cd ~/workspace/scripts && touch new-script.py

# ✅ 数据
cd ~/workspace/data/<agent>/ && ...

# ✅ 记忆
cd ~/workspace/memory/ && touch YYYY-MM-DD.md
```

### 组织项目

```bash
# 1. 临时项目 → /tmp/
cd /tmp && git clone ... && 完成后删除

# 2. 短期项目 → projects/
cd ~/workspace/projects && git clone ... && 完成后归档

# 3. 长期项目 → ~/projects/
cd ~/projects && git clone ... && 保留
```

---

## 📊 快速参考

| 文件类型 | 存放位置 | 清理时机 |
|---------|---------|---------|
| 临时下载 | `/tmp/` | 系统自动 |
| 临时项目 | `projects/` | 完成后 |
| Git 项目（临时） | `/tmp/` | 完成后 |
| Git 项目（长期） | `~/projects/` | 保留 |
| Agent 数据 | `data/<agent>/` | 根据需要 |
| 记忆文件 | `memory/` | 定期归档 |
| 知识库 | `data/<agent>/*.db` | 系统管理 |
| 文档 | `docs/` | 保留 |
| 脚本 | `scripts/` | 保留 |

---

## 🔍 诊断命令

```bash
# 查看 workspace 结构
cd ~/workspace && tree -L 2

# 查看大文件
cd ~/workspace && du -sh * | sort -h

# 查看 projects 目录
ls -la ~/workspace/projects/

# 查看 data 目录
ls -la ~/workspace/data/
```

---

## 🎯 核心原则

1. **workspace 是工作区，不是仓库** - 保持整洁，只放必要文件
2. **临时文件去 /tmp/** - 系统会自动清理
3. **项目分类存放** - 临时/短期/长期分开
4. **数据隔离** - 每个 Agent 独立数据目录
5. **记忆自动管理** - 系统自动创建和维护

---

_版本：1.0.0 | 2026-04-01_
