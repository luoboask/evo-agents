# 🏗️ test-agents Workspace 架构

**版本：** v1.0  
**更新日期：** 2026-03-26  
**适用范围：** test-agents Workspace

---

## 1. 核心架构

**两层结构：**

| 层面 | 路径 | 管理方 | 用途 |
|------|------|--------|------|
| **OpenClaw** | `~/.openclaw/agents/` | OpenClaw 自动 | sessions、auth |
| **Workspace** | `workspace/agents/` | 手动管理 | 子 Agent 数据隔离 |

---

## 2. 目录结构

```
~/.openclaw/workspace-test-agents/
│
├── 📄 根目录文件
│   ├── AGENTS.md           # 会话规范 ⭐
│   ├── SOUL.md             # Agent 身份 ⭐
│   ├── MEMORY.md           # 长期记忆 ⭐
│   ├── USER.md             # 用户信息 ⭐
│   ├── IDENTITY.md         # 身份标识
│   ├── TOOLS.md            # 工具配置
│   └── HEARTBEAT.md        # 心跳检查
│
├── 🤖 agents/              # ⭐ 子 Agent 数据隔离
│   ├── analyst-agent/      # 🔍 需求分析师
│   │   ├── AGENTS.md
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   ├── config.yaml
│   │   ├── memory/         # 🔒 独立记忆
│   │   └── data/           # 🔒 独立数据库
│   ├── developer-agent/    # 💻 代码开发者
│   └── tester-agent/       # ✅ 质量测试员
│
├── 🔧 scripts/             # ⭐ 共享脚本
│   ├── session_recorder.py     # 支持 --agent
│   ├── unified_search.py       # 支持 --agent
│   ├── memory_indexer.py
│   ├── memory_compressor.py
│   ├── memory_stats.py
│   ├── health_check.py
│   └── bridge/                 # 双向同步
│
├── 📚 libs/                  # ⭐ 共享库
│   └── memory_hub/
│
├── 🎯 skills/                # ⭐ 共享技能
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📝 memory/                # 主 Agent 记忆
├── 💾 data/                  # 主 Agent 数据
├── 🌐 public/                # 公共知识库
├── ⚙️ config/                # 配置
│   └── agents.yaml
├── 📂 projects/              # Git 库管理
└── docs/                     # 文档
```

---

## 3. 多 Agent 设计

### 3.1 Agent 列表

| Agent | 角色 | 路径 | Emoji |
|-------|------|------|-------|
| **test-agents** | coordinator | `memory/` + `data/` | 🦞 |
| **analyst-agent** | analyst | `agents/analyst-agent/` | 🔍 |
| **developer-agent** | developer | `agents/developer-agent/` | 💻 |
| **tester-agent** | tester | `agents/tester-agent/` | ✅ |

### 3.2 共享与隔离

| 资源 | 共享/隔离 | 说明 |
|------|----------|------|
| `scripts/` | ✅ 共享 | 所有 Agent 共用 |
| `libs/` | ✅ 共享 | 所有 Agent 共用 |
| `skills/` | ✅ 共享 | 所有 Agent 共用 |
| `memory/` | 🔒 隔离 | 每个 Agent 独立 |
| `data/` | 🔒 隔离 | 每个 Agent 独立 |

### 3.3 协作流程

```
1️⃣  analyst-agent    需求分析
    ↓
2️⃣  developer-agent  方案实现
    ↓
3️⃣  tester-agent     质量测试
    ↓
4️⃣  test-agents      总结沉淀
```

---

## 4. 使用方式

### 记录事件

```bash
cd ~/.openclaw/workspace-test-agents

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

---

## 5. Git 库管理

### projects/ 目录

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

### 使用

```bash
# 克隆
git clone https://github.com/xxx/lib.git projects/

# 查看
ls -1 projects/

# 删除
rm -rf projects/old-lib/
```

---

## 6. 核心原则

1. **共享代码 + 隔离数据** - scripts/libs/skills 共享，memory/data 隔离
2. **参数化设计** - 所有脚本支持 `--agent` 参数
3. **扁平结构** - projects/ 不分类
4. **OpenClaw 边界** - `~/.openclaw/agents/` 由 OpenClaw 管理

---

## 7. 配置

### config/agents.yaml

```yaml
test-agents:
  name: test-agents
  role: coordinator
  data_path: data/test-agents
  memory_path: memory

analyst-agent:
  name: analyst-agent
  role: analyst
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory

developer-agent:
  name: developer-agent
  role: developer
  
tester-agent:
  name: tester-agent
  role: tester
```

---

## 8. 文档

| 文档 | 用途 |
|------|------|
| `ARCHITECTURE_GENERIC_CN.md` | 本文档 - 架构说明 |
| `ARCHITECTURE_GENERIC_EN.md` | Architecture (English) |
| `PROJECT_STRUCTURE_GENERIC_CN.md` | 目录结构规范 |
| `PROJECT_STRUCTURE_GENERIC_EN.md` | Project Structure (English) |

---

**最后更新：** 2026-03-26  
**维护者：** test-agents 🦞
