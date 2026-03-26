# 📁 test-agents Workspace - 目录结构规范

**版本：** v1.0  
**更新日期：** 2026-03-26  
**适用范围：** test-agents Workspace

---

## 1. 架构原则

### 1.1 分离关注点

```
┌─────────────────────────────────────────┐
│          共享层 (scripts/libs/skills)    │
│  所有 Agent 共用，支持 --agent 参数        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          隔离层 (agents/*/memory/data)  │
│  每个 Agent 独立记忆和数据                 │
└─────────────────────────────────────────┘
```

### 1.2 核心原则

- **共享代码** - scripts/libs/skills 所有 Agent 共用
- **隔离数据** - 每个 Agent 独立 memory/ 和 data/
- **参数化** - 所有脚本支持 `--agent` 参数

---

## 2. 完整目录结构

```
workspace/
│
├── 📄 根目录文件
│   ├── AGENTS.md           # 会话规范 ⭐
│   ├── SOUL.md             # Agent 身份
│   ├── MEMORY.md           # 长期记忆
│   ├── USER.md             # 用户信息
│   ├── IDENTITY.md         # 身份标识
│   ├── TOOLS.md            # 工具配置
│   └── HEARTBEAT.md        # 心跳检查
│
├── 🤖 agents/              # ⭐ 子 Agent 数据隔离
│   ├── analyst-agent/
│   │   ├── AGENTS.md
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   ├── config.yaml
│   │   ├── memory/         # 🔒 独立记忆
│   │   └── data/           # 🔒 独立数据库
│   ├── developer-agent/
│   └── tester-agent/
│
├── 🔧 scripts/             # ⭐ 共享脚本
│   ├── session_recorder.py
│   ├── unified_search.py
│   ├── memory_indexer.py
│   ├── memory_compressor.py
│   ├── memory_stats.py
│   ├── health_check.py
│   └── bridge/
│
├── 📚 libs/                # ⭐ 共享库
│   └── memory_hub/
│
├── 🎯 skills/              # ⭐ 共享技能
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📝 memory/              # 主 Agent 记忆
├── 💾 data/                # 主 Agent 数据
├── 🌐 public/              # 公共知识库
├── ⚙️ config/              # 配置
├── 📂 projects/            # Git 库管理
└── docs/                   # 文档
```

---

## 3. 目录职责

### 3.1 根目录文件

| 文件 | 用途 |
|------|------|
| `AGENTS.md` | 会话行为规范（搜索、记录、同步） |
| `SOUL.md` | Agent 身份和个性 |
| `MEMORY.md` | 长期记忆（重要事件、决定） |
| `USER.md` | 用户信息 |
| `IDENTITY.md` | 身份标识（名称、emoji、头像） |
| `TOOLS.md` | 工具配置（相机、SSH、TTS 等） |
| `HEARTBEAT.md` | 心跳检查清单 |

### 3.2 agents/ - 子 Agent 数据隔离

| Agent | 路径 | 用途 |
|-------|------|------|
| analyst-agent | `agents/analyst-agent/` | 需求分析 🔍 |
| developer-agent | `agents/developer-agent/` | 代码实现 💻 |
| tester-agent | `agents/tester-agent/` | 质量测试 ✅ |

每个子 Agent 包含：
- `AGENTS.md` - 行为规范
- `SOUL.md` - 身份
- `MEMORY.md` - 记忆
- `config.yaml` - 配置
- `memory/` - 独立记忆目录
- `data/` - 独立数据库

### 3.3 scripts/ - 共享脚本

| 脚本 | 功能 | 支持 --agent |
|------|------|-------------|
| `session_recorder.py` | 记录事件 | ✅ |
| `unified_search.py` | 统一搜索 | ✅ |
| `memory_indexer.py` | 构建索引 | ✅ |
| `memory_compressor.py` | 压缩沉淀 | ✅ |
| `memory_stats.py` | 系统统计 | ✅ |
| `health_check.py` | 健康检查 | ✅ |
| `bridge/*.py` | 双向同步 | ✅ |

### 3.4 skills/ - 共享技能

| Skill | 功能 |
|-------|------|
| `memory-search/` | 记忆搜索（关键词 + 语义） |
| `rag/` | RAG 评估 |
| `self-evolution/` | 自进化系统 |
| `websearch/` | 网页搜索 |

### 3.5 memory/ - 主 Agent 记忆

```
memory/
├── YYYY-MM-DD.md        # 每日记录
├── weekly/              # 周摘要
├── monthly/             # 月摘要
├── archive/             # 归档
└── knowledge/           # 知识
```

### 3.6 data/ - 主 Agent 数据

```
data/
├── .locks/              # 文件锁
├── index/               # 搜索索引
└── test-agents/         # test-agents 的 SQLite 数据
```

### 3.7 public/ - 公共知识库

| 分类 | 用途 |
|------|------|
| `common/` | 通用知识 |
| `domain/` | 领域知识 |
| `faq/` | FAQ |
| `openclaw/` | OpenClaw 相关 |
| `operations/` | 运维知识 |
| `prompt/` | Prompt 模板 |
| `rag/` | RAG 相关 |
| `security/` | 安全知识 |
| `skills/` | 技能文档 |
| `tutorial/` | 教程 |

### 3.8 projects/ - Git 库管理

```
projects/
├── lib-a/          # 直接放，不分类
├── app-b/
└── test-repo/
```

**原则：**
- ✅ 扁平结构 - 所有库直接放 `projects/`
- ✅ 不分类 - 避免决策成本
- ✅ 手动清理 - 不需要时手动删除

---

## 4. 命名规范

| 目录类型 | 命名规范 | 示例 |
|---------|---------|------|
| `libs/` 子目录 | 下划线 `_` | `memory_hub` |
| `skills/` 子目录 | 连字符 `-` | `memory-search` |
| `scripts/` 文件 | 动词 + 对象 | `session_recorder.py` |
| `agents/` 子目录 | 连字符 `-` | `analyst-agent` |
| `docs/` 文件 | 主题命名 | `ARCHITECTURE_GENERIC_CN.md` |

---

## 5. 依赖关系

```
skills/*  ─────► libs/*
skills/*  ✖────► skills/*   (避免横向强耦合)
libs/*    ✖────► skills/*   (禁止反向依赖)
```

---

## 6. 使用示例

### 记录事件

```bash
# 记录到子 Agent
python3 scripts/session_recorder.py -t event -c '内容' --agent analyst-agent

# 记录到主 Agent
python3 scripts/session_recorder.py -t decision -c '内容' --agent test-agents --sync
```

### 搜索记忆

```bash
# 搜索子 Agent
python3 scripts/unified_search.py '关键词' --agent developer-agent --semantic

# 搜索主 Agent
python3 scripts/unified_search.py '关键词' --agent test-agents --semantic
```

### Git 库管理

```bash
# 克隆
git clone https://github.com/xxx/lib.git projects/

# 查看
ls -1 projects/

# 删除
rm -rf projects/old-lib/
```

---

## 7. 总结

| 目录 | 共享/隔离 | 说明 |
|------|----------|------|
| `scripts/` | ✅ 共享 | 所有 Agent 共用 |
| `libs/` | ✅ 共享 | 所有 Agent 共用 |
| `skills/` | ✅ 共享 | 所有 Agent 共用 |
| `agents/*/` | 🔒 隔离 | 每个子 Agent 独立 |
| `memory/` | 🔒 隔离 | 主 Agent 独立 |
| `data/` | 🔒 隔离 | 主 Agent 独立 |
| `public/` | ✅ 共享 | 公共知识库 |
| `projects/` | ✅ 共享 | Git 库管理 |

---

**最后更新：** 2026-03-26  
**维护者：** test-agents 🦞
