# 🏗️ evo-agents 架构

**版本：** v6.0  
**更新日期：** 2026-03-27  
**适用范围：** evo-agents Workspace

---

## 1. 核心架构

**两层结构：**

| 层面 | 路径 | 管理方 | 用途 |
|------|------|--------|------|
| **OpenClaw** | `~/.openclaw/agents/` | OpenClaw 自动 | sessions、auth、配置 |
| **Workspace** | `~/.openclaw/workspace-<agent>/` | 模板管理 | 代码、脚本、技能 |

---

## 2. 目录结构

```
~/.openclaw/workspace-my-agent/
│
├── 📄 根目录文档
│   ├── README.md               # 项目说明
│   ├── workspace-setup.md      # 安装指南
│   └── *.md                    # 其他文档
│
├── 🤖 agents/                  # 子 Agent 目录
│   └── <agent-name>/
│       ├── agent/              # OpenClaw Agent 配置
│       ├── memory/             # Agent 记忆
│       ├── sessions/           # 聊天会话
│       ├── scripts/            # Agent 特定脚本（可选）
│       ├── skills/ → ../../skills  # 符号链接（共享技能）
│       ├── libs/               # Agent 特定库（可选）
│       └── data/
│           └── work/           # 临时工作目录
│
├── 🔧 scripts/                 # 共享脚本
│   ├── core/                   # 系统脚本（模板更新）
│   │   ├── activate-features.sh
│   │   ├── add-agent.sh
│   │   ├── setup-multi-agent.sh
│   │   ├── cleanup.sh
│   │   └── session_recorder.py
│   └── *.sh, *.py              # 用户脚本（保留）
│
├── 🧩 skills/                  # 技能目录（OpenClaw 原生）
│   ├── memory-search/          # 通用技能（模板更新）
│   ├── rag/                    # 通用技能（模板更新）
│   ├── self-evolution/         # 通用技能（模板更新）
│   ├── web-knowledge/          # 通用技能（模板更新）
│   └── <your-skill>/           # 自定义技能（保留）
│
├── 📚 libs/                    # 共享库
│   └── memory_hub/             # 记忆管理库
│
├── 📁 data/                    # 运行时数据（不提交）
│   └── <agent>/
│       ├── memory/             # Agent 记忆数据
│       └── work/               # 临时工作
│
├── 📝 memory/                  # 日常记忆（不提交）
│   ├── YYYY-MM-DD.md           # 每日记忆
│   ├── weekly/                 # 每周总结
│   └── monthly/                # 每月总结
│
└── 📖 public/                  # 知识库（不提交）
    ├── common/
    ├── domain/
    ├── faq/
    └── ...
```

---

## 3. 文件分类

### 3.1 模板文件（会被更新）

| 文件/目录 | 说明 | 更新行为 |
|-----------|------|----------|
| `scripts/core/` | 系统脚本 | 📦 重新安装时更新 |
| `skills/memory-search/` | 记忆搜索技能 | 📦 重新安装时更新 |
| `skills/rag/` | RAG 技能 | 📦 重新安装时更新 |
| `skills/self-evolution/` | 自进化技能 | 📦 重新安装时更新 |
| `skills/web-knowledge/` | 网络知识技能 | 📦 重新安装时更新 |
| `docs/` | 文档 | 📦 重新安装时更新 |
| `*.md` (根目录) | 根目录文档 | 📦 重新安装时更新 |

### 3.2 个人文件（保留）

| 文件/目录 | 说明 | 保护 |
|-----------|------|------|
| `USER.md` | 用户信息 | ✅ 永不删除 |
| `SOUL.md` | Agent 人格 | ✅ 永不删除 |
| `IDENTITY.md` | 身份标识 | ✅ 永不删除 |
| `MEMORY.md` | 长期记忆 | ✅ 永不删除 |
| `HEARTBEAT.md` | 心跳配置 | ✅ 永不删除 |
| `TOOLS.md` | 工具配置 | ✅ 永不删除 |
| `scripts/*.sh` | 用户脚本 | ✅ 永不删除 |
| `skills/<your-skill>/` | 自定义技能 | ✅ 永不删除 |

### 3.3 运行时数据（不提交）

| 目录 | 说明 | Git |
|------|------|-----|
| `memory/` | 日常记忆 | ❌ 排除 |
| `public/` | 知识库 | ❌ 排除 |
| `data/` | Agent 数据 | ❌ 排除 |
| `agents/<agent>/agent/` | Agent 配置 | ❌ 排除 |
| `agents/<agent>/sessions/` | 聊天会话 | ❌ 排除 |

---

## 4. 子 Agent 架构

### 4.1 创建方式

```bash
# 创建单个 Agent
./scripts/core/add-agent.sh assistant "My Assistant" 🤖

# 批量创建 Agent
./scripts/core/setup-multi-agent.sh researcher writer editor
```

### 4.2 目录结构

```
agents/<agent-name>/
├── agent/                   # OpenClaw Agent 配置
│   ├── models.json          # 模型配置
│   └── sessions/            # 聊天会话
├── memory/                  # Agent 记忆
│   ├── knowledge_base.db    # 知识库
│   └── memory_stream.db     # 记忆流
├── scripts/                 # Agent 特定脚本（可选）
├── skills/ → ../../skills   # 符号链接（共享技能）
├── libs/                    # Agent 特定库（可选）
└── data/
    └── work/                # 临时工作目录
```

### 4.3 符号链接

**skills/ 符号链接：**
```bash
agents/<agent-name>/skills → ../../skills
```

**目的：**
- ✅ 所有 Agent 共享同一套技能
- ✅ 更新父 workspace 技能，所有子 Agent 自动受益
- ✅ 不占用额外空间

---

## 5. 脚本系统

### 5.1 核心脚本（scripts/core/）

| 脚本 | 用途 |
|------|------|
| `activate-features.sh` | 激活高级功能 |
| `add-agent.sh` | 添加子 Agent |
| `setup-multi-agent.sh` | 批量添加 Agent |
| `cleanup.sh` | 清理临时文件 |
| `session_recorder.py` | 记录会话 |
| `restore-backup.sh` | 恢复备份 |
| `health_check.py` | 健康检查 |
| `memory_*.py` | 记忆系统相关 |
| `unified_search.py` | 统一搜索 |
| `lock_utils.py` | 文件锁工具 |

### 5.2 用户脚本（scripts/ 根目录）

```bash
scripts/
├── core/              # 系统脚本（模板更新）
├── my-tool.sh         # 用户脚本（保留）
└── custom-tool.py     # 用户脚本（保留）
```

---

## 6. 记忆系统

### 6.1 三层架构

```
memory/
├── daily/             # 日常记忆
│   ├── YYYY-MM-DD.md  # 每日记录
│   └── ...
├── weekly/            # 每周总结
│   ├── YYYY-Www.md
│   └── ...
└── monthly/           # 每月总结
    ├── YYYY-MM.md
    └── ...
```

### 6.2 知识系统

```
data/<agent>/
├── knowledge_base.db    # SQLite 知识库
└── memory_stream.db     # 记忆流
```

### 6.3 桥接系统

```
scripts/core/bridge/
├── bridge_sync.py         # 双向同步
├── bridge_to_knowledge.py # Markdown → SQLite
└── bridge_to_markdown.py  # SQLite → Markdown
```

---

## 7. Workspace 规则

### 7.1 目录使用

| 目录 | 用途 | 可以创建 |
|------|------|----------|
| `scripts/` | 脚本 | ✅ 是 |
| `skills/` | 技能 | ✅ 是 |
| `data/<agent>/work/` | 临时工作 | ✅ 是 |
| `memory/` | 记忆文件 | ❌ 系统管理 |
| `public/` | 知识库 | ❌ 系统管理 |
| 根目录 `/` | Workspace 根 | ❌ 保持整洁 |

### 7.2 外部目录

| 目录 | 用途 |
|------|------|
| `/tmp/` | 临时工作 |
| `~/projects/` | 长期项目 |

### 7.3 清理规则

**自动清理（cleanup.sh）：**
- ✅ `node_modules/`
- ✅ `__pycache__/`
- ✅ `*.log`, `*.tmp`, `*.pyc`
- ❌ `data/*/work/`（需要手动确认）

---

## 8. 安装与更新

### 8.1 新安装

```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

### 8.2 重新安装（保留数据）

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh)" -s my-agent
```

**保留内容：**
- ✅ 个人配置（USER.md, SOUL.md 等）
- ✅ 记忆数据（memory/, public/）
- ✅ 用户脚本（scripts/ 根目录）
- ✅ 自定义技能（skills/ 根目录）

**更新内容：**
- 📦 系统脚本（scripts/core/）
- 📦 通用技能（skills/memory-search/ 等）
- 📦 文档（docs/, *.md）

---

## 9. 最佳实践

### 9.1 目录使用

```bash
# ✅ 正确：脚本放在 scripts/
cd scripts/
cat > my-tool.sh

# ✅ 正确：项目放在外部
cd ~/projects/
git clone https://github.com/xxx/project.git

# ✅ 正确：临时工作用 work/
cd data/my-agent/work/
# 完成后手动清理

# ❌ 错误：不要在根目录创建
cd ..
mkdir my-project  # 不要这样做！
```

### 9.2 子 Agent 管理

```bash
# ✅ 使用脚本创建
./scripts/core/add-agent.sh assistant "助手" 🤖

# ✅ 共享技能（符号链接）
# 子 Agent 自动共享父 workspace 的技能

# ✅ 特定脚本放在 Agent 目录
cd agents/assistant-agent/scripts/
cat > assistant-tool.sh
```

### 9.3 记忆管理

```bash
# ✅ 自动记录
python3 scripts/core/session_recorder.py -t event -c "内容" --agent my-agent

# ✅ 定期同步
python3 scripts/core/bridge/bridge_sync.py --agent my-agent

# ✅ 定期清理
./scripts/core/cleanup.sh
```

---

## 10. 故障排除

### 10.1 常见问题

| 问题 | 解决方案 |
|------|----------|
| 脚本找不到 | 检查路径，使用 `scripts/core/` |
| Agent 不工作 | 检查 `agents/<agent>/agent/` 配置 |
| 记忆不同步 | 运行 `bridge_sync.py` |
| workspace 太乱 | 运行 `cleanup.sh` |

### 10.2 恢复备份

```bash
# 恢复备份
./scripts/core/restore-backup.sh

# 或手动恢复
cp -r /tmp/workspace-backup-*/* ~/.openclaw/workspace-my-agent/
```

---

## 11. 相关文档

| 文档 | 说明 |
|------|------|
| [STRUCTURE_RULES.md](STRUCTURE_RULES.md) | 详细结构规则 |
| [WORKSPACE_RULES.md](WORKSPACE_RULES.md) | Workspace 使用规范 |
| [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) | Agent 指令 |
| [SCRIPTS_INVENTORY.md](SCRIPTS_INVENTORY.md) | 脚本清单 |
| [QUICKSTART.md](QUICKSTART.md) | 快速入门 |

---

**最后更新：** 2026-03-27  
**版本：** v6.0
