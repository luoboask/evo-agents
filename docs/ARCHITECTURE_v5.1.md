# 🏗️ ai-baby Workspace 架构设计 v5.1

**创建时间：** 2026-03-23  
**最后更新：** 2026-03-23 13:52  
**状态：** ✅ 设计完成，待实施  
**维护者：** ai-baby

---

## 📋 目录

1. [概述](#概述)
2. [核心架构](#核心架构)
3. [目录结构](#目录结构)
4. [多 Agent 设计](#多-agent-设计)
5. [技能系统](#技能系统)
6. [数据管理](#数据管理)
7. [配置管理](#配置管理)
8. [与 OpenClaw 集成](#与-openclaw-集成)
9. [实施计划](#实施计划)

---

## 概述

### 设计目标

- ✅ **单一 Workspace** - 所有 Agent 共享同一个 workspace
- ✅ **技能共享** - skills/ 目录所有 Agent 共用
- ✅ **配置集中** - config/agents.yaml 管理所有 Agent
- ✅ **数据隔离** - 每个 Agent 独立数据目录
- ✅ **OpenClaw 集成** - 利用 OpenClaw 原生能力

### 核心原则

1. **不重复造轮子** - 利用 OpenClaw 原生的 Agent/Session 管理
2. **代码与数据分离** - 技能代码在 workspace，数据在 data/
3. **配置集中管理** - 所有 Agent 配置在 config/agents.yaml
4. **灵活可扩展** - 新 Agent/新技能快速添加

---

## 核心架构

### 架构分层

```
┌─────────────────────────────────────────────────────────┐
│                    用户层                                │
│  (通过 Telegram/Discord/WebChat/OpenClaw TUI 访问)        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              OpenClaw Gateway 层                         │
│  - Agent 管理 (main, baby1, baby2...)                    │
│  - 路由 (Agent → workspace)                              │
│  - 记忆管理                                              │
│  - 工具调用                                              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│         workspace-ai-baby (唯一工作区) ⭐                │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  技能层 (skills/) - 所有 Agent 共享                │  │
│  │  - memory-search                                   │  │
│  │  - rag-evaluation                                  │  │
│  │  - self-evolution                                  │  │
│  │  - websearch                                       │  │
│  │  - specialized/ (专用技能)                         │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  配置层 (config/agents.yaml) ⭐                    │  │
│  │  - main: 主 Agent 配置                             │  │
│  │  - baby1: 沙箱 Agent 配置                          │  │
│  │  - baby2: 电商 Agent 配置                          │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  数据层 (data/) - 所有 Agent 数据                  │  │
│  │  - data/main/         # 主 Agent 数据              │  │
│  │  - data/baby1/        # baby1 数据                 │  │
│  │  - data/baby2/        # baby2 数据                 │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 职责划分

| 层级 | 职责 | 技术选型 |
|------|------|----------|
| **用户层** | 用户交互 | OpenClaw TUI/WebChat/Telegram |
| **Gateway 层** | Agent/路由管理 | OpenClaw Gateway |
| **技能层** | 业务逻辑实现 | Python + SQLite |
| **配置层** | Agent 配置管理 | YAML |
| **数据层** | 数据存储 | SQLite + 文件系统 |

---

## 目录结构

### 完整结构

```
~/.openclaw/
├── agents/                    # ⭐ OpenClaw 管理的 Agent
│   ├── main/
│   │   ├── agent.yaml         # OpenClaw Agent 配置
│   │   ├── SOUL.md            # OpenClaw 标准文档
│   │   ├── USER.md
│   │   └── agent.db           # OpenClaw 状态数据库
│   ├── baby1/
│   │   ├── agent.yaml
│   │   ├── SOUL.md
│   │   └── agent.db
│   └── baby2/
│       ├── agent.yaml
│       └── agent.db
│
└── workspace-ai-baby/         # ⭐ 你的工作区（所有 Agent 共享）
    │
    ├── skills/                # ⭐ 技能（所有 Agent 共享）
    │   ├── memory-search/
    │   │   ├── __init__.py
    │   │   ├── search_sqlite.py
    │   │   ├── README.md
    │   │   └── tests/
    │   ├── rag-evaluation/
    │   │   ├── __init__.py
    │   │   ├── evaluate.py
    │   │   ├── auto_tune.py
    │   │   └── README.md
    │   ├── self-evolution/
    │   │   └── ...
    │   ├── websearch/
    │   │   └── ...
    │   └── specialized/       # 专用技能
    │       ├── baby1-sandbox/
    │       ├── baby2-ecommerce/
    │       └── baby3-content/
    │
    ├── config/                # ⭐ 配置
    │   ├── agents.yaml        # ⭐ 所有 Agent 配置
    │   └── skills/            # 技能配置
    │       ├── memory-search.yaml
    │       └── rag-evaluation.yaml
    │
    ├── agents/                # ⭐ 子 Agent 配置（workspace 下）
    │   ├── baby1/
    │   │   └── agent.yaml     # baby1 的配置
    │   ├── baby2/
    │   │   └── agent.yaml     # baby2 的配置
    │   └── baby3/
    │       └── agent.yaml
    │
    ├── data/                  # ⭐ 所有 Agent 数据
    │   ├── main/              # 主 Agent 数据
    │   │   ├── memory/
    │   │   │   ├── memory_stream.db
    │   │   │   └── knowledge_base.db
    │   │   ├── logs/
    │   │   │   ├── agent.log
    │   │   │   └── skills.log
    │   │   └── cache/
    │   │       └── embedding_cache.pkl
    │   ├── baby1/             # baby1 数据
    │   │   ├── memory/
    │   │   ├── logs/
    │   │   └── cache/
    │   ├── baby2/             # baby2 数据
    │   │   ├── memory/
    │   │   └── logs/
    │   └── baby3/             # baby3 数据
    │
    ├── docs/                  # ⭐ 文档
    │   ├── ARCHITECTURE_DESIGN.md
    │   ├── TOOL_CALLING_PRINCIPLE.md
    │   ├── WORKSPACE_SETUP.md
    │   └── ...
    │
    ├── scripts/               # ⭐ 工具脚本
    │   ├── create_agent.py    # 创建子 Agent
    │   ├── init_system.py     # 系统初始化
    │   └── test_all.py        # 完整测试
    │
    └── README.md              # ⭐ 工作区说明
```

---

## 多 Agent 设计

### Agent 关系

```
ai-baby (主 Agent)
├─ baby1 (沙箱测试)
│   - 角色：tester
│   - 技能：memory-search, rag-evaluation
│   - 数据：data/baby1/
│   - 特点：限制记忆数量，自动清理
│
├─ baby2 (电商运营)
│   - 角色：ecommerce
│   - 技能：memory-search, rag-evaluation, self-evolution, ecommerce
│   - 数据：data/baby2/
│   - 特点：电商平台集成
│
└─ baby3 (内容创作)
    - 角色：creator
    - 技能：memory-search, rag-evaluation, self-evolution, websearch, content
    - 数据：data/baby3/
    - 特点：内容创作工具
```

### Agent 配置示例

```yaml
# config/agents.yaml

# ───────────────────────────────────────────────────────
# 主 Agent
# ───────────────────────────────────────────────────────
main:
  name: ai-baby
  role: assistant
  emoji: "🍼"
  description: "主 Agent - 日常 AI 助手"
  
  # OpenClaw Agent 名称
  openclaw_agent: main
  
  # 技能配置
  skills:
    memory-search:
      enabled: true
      config:
        semantic_search: true
    
    rag-evaluation:
      enabled: true
      config:
        auto_record: true
    
    self-evolution:
      enabled: true
      config:
        fractal_thinking: true
        nightly_cycle: false
    
    websearch:
      enabled: true
  
  # 数据路径（相对于 workspace）
  data_path: data/main

# ───────────────────────────────────────────────────────
# baby1 - 沙箱测试 Agent
# ───────────────────────────────────────────────────────
baby1:
  name: baby1-sandbox
  role: tester
  emoji: "🧪"
  description: "沙箱 Agent - 测试和实验"
  parent: main
  
  openclaw_agent: baby1
  
  skills:
    memory-search:
      enabled: true
      config:
        max_memories: 100  # 限制记忆数量
    
    rag-evaluation:
      enabled: true
    
    # 禁用的技能
    self-evolution:
      enabled: false
      reason: "沙箱环境不需要自进化"
    
    websearch:
      enabled: false
      reason: "沙箱环境不需要联网"
  
  data_path: data/baby1
  
  # 沙箱特定配置
  sandbox:
    auto_cleanup: true
    max_memories: 100
    max_age_days: 7
    isolated: true

# ───────────────────────────────────────────────────────
# baby2 - 电商运营 Agent
# ───────────────────────────────────────────────────────
baby2:
  name: baby2-ecommerce
  role: ecommerce
  emoji: "🛒"
  description: "电商 Agent - 自营平台运营"
  parent: main
  
  openclaw_agent: baby2
  
  skills:
    memory-search:
      enabled: true
    
    rag-evaluation:
      enabled: true
    
    self-evolution:
      enabled: true
    
    specialized/ecommerce:
      enabled: true
      config:
        platform: taobao
        auto_sync: true
  
  data_path: data/baby2
  
  # 电商特定配置
  ecommerce:
    platform: taobao
    auto_sync: true
```

---

## 技能系统

### 技能格式

**统一使用 OpenClaw 原生技能格式（SKILL.md）**

```
skills/
├── memory-search/
│   ├── SKILL.md          # ⭐ 技能说明和工具定义
│   ├── skill.json        # ⭐ 元数据
│   ├── search_sqlite.py  # 技能实现
│   └── ...
├── rag-evaluation/
│   ├── SKILL.md
│   ├── skill.json
│   ├── evaluate.py
│   └── ...
└── ...
```

**SKILL.md 结构：**

```markdown
---
name: memory_search
description: 记忆搜索技能，支持关键词和语义搜索
homepage: https://...
metadata:
  emoji: "🧠"
  category: memory
  api_base: "local"
---

# 记忆搜索技能

## 功能
- 关键词搜索记忆
- 向量语义搜索（需要 Ollama）
- 添加/删除/修改记忆
- 统计分析

## 可用工具
- search(query, top_k=5, semantic=false)
- add(content, type="observation", tags=[])
- delete(memory_id)
- stats()

## 使用方法
当用户要搜索记忆时，使用 search 工具...
```

**skill.json 结构：**

```json
{
  "name": "memory-search",
  "version": "1.0.0",
  "description": "记忆搜索技能",
  "homepage": "https://...",
  "updated_at": "2026-03-23"
}
```

---

### 技能分类

```
skills/
├── core/                    # 核心技能（所有 Agent 共享）
│   ├── memory-search/       # 记忆搜索
│   ├── rag-evaluation/      # RAG 评估
│   ├── self-evolution/      # 自进化
│   └── websearch/           # 网页搜索
│
└── specialized/             # 专用技能（按需启用）
    ├── baby1-sandbox/       # 沙箱测试
    ├── baby2-ecommerce/     # 电商运营
    └── baby3-content/       # 内容创作
```

---

### 核心技能详解

#### 1. memory-search（记忆搜索）

**位置：** `skills/memory-search/`

**SKILL.md 示例：**

```markdown
---
name: memory_search
description: 记忆搜索技能，支持关键词和语义搜索
metadata:
  emoji: "🧠"
  category: memory
---

# 记忆搜索技能

## 功能
- 关键词搜索记忆
- 向量语义搜索（需要 Ollama）
- 添加/删除/修改记忆
- 统计分析

## 可用工具
- search(query, top_k=5, semantic=false)
- add(content, type="observation", tags=[])
- delete(memory_id)
- stats()

## 数据存储
~/.openclaw/workspace-ai-baby-config/memory/
```

**文件结构：**
```
skills/memory-search/
├── SKILL.md              # ⭐ 技能说明
├── skill.json            # ⭐ 元数据
├── search_sqlite.py      # SQLite 搜索实现
├── semantic_search.py    # 语义搜索（Ollama）
└── daily_review.py       # 每日回顾
```

**OpenClaw 配置：**
```json
// ~/.openclaw/openclaw.json
{
  "skills": {
    "load": {
      "extraDirs": ["~/.openclaw/workspace-ai-baby/skills"]
    },
    "entries": {
      "memory-search": {
        "enabled": true
      }
    }
  }
}
```

---

#### 2. rag-evaluation（RAG 评估）

**位置：** `skills/rag-evaluation/`

**SKILL.md 示例：**

```markdown
---
name: rag_evaluation
description: RAG 检索质量评估与优化
metadata:
  emoji: "📊"
  category: evaluation
---

# RAG 评估技能

## 功能
- 检索质量评估
- 自动调优
- 检索记录
- 报告生成

## 可用工具
- rag_report(days=7)
- rag_auto_tune(min_samples=10)
- rag_record(query, retrieved_count, latency_ms)

## 评估指标
- 延迟：< 50ms 优秀
- 正面反馈率：> 70% 优秀
- 检索使用率：> 80% 优秀
```

**文件结构：**
```
skills/rag-evaluation/
├── SKILL.md
├── skill.json
├── evaluate.py
├── auto_tune.py
└── recorder.py
```

---

#### 3. self-evolution（自进化）

**位置：** `skills/self-evolution/`

**SKILL.md 示例：**

```markdown
---
name: self_evolution
description: 自进化系统，分形思考和夜间循环
metadata:
  emoji: "🧬"
  category: evolution
---

# 自进化技能

## 功能
- 分形思考（4 层分析）
- 夜间循环（4 个任务）
- 记忆流管理
- 进化事件记录

## 可用工具
- run_fractal_analysis(limit=10)
- run_nightly_cycle(tasks=[])
- record_evolution(event_type, content)

## 分形思考 4 层
Level 0: Solve      → 问题是什么？
Level 1: Pattern    → 是孤立事件还是重复模式？
Level 2: Correction → 什么规则导致了问题？
Level 3: Meta-Rule  → 如何防止类似问题再发生？
```

**文件结构：**
```
skills/self-evolution/
├── SKILL.md
├── skill.json
├── fractal_thinking.py
├── nightly_cycle.py
└── memory_stream.py
```

---

#### 4. websearch（网页搜索）

**位置：** `skills/websearch/`

**SKILL.md 示例：**

```markdown
---
name: web_search
description: 网页搜索技能，基于 Bing
metadata:
  emoji: "🌐"
  category: search
---

# 网页搜索技能

## 功能
- 基于 Bing 的网页搜索
- 无需 API key
- 自动提取页面内容

## 可用工具
- web_search(query, count=10, freshness="week")
```

---

### 技能配置

**OpenClaw 配置：**

```json
// ~/.openclaw/openclaw.json
{
  "skills": {
    "load": {
      "extraDirs": [
        "~/.openclaw/workspace-ai-baby/skills"
      ],
      "watch": true,
      "watchDebounceMs": 250
    },
    "entries": {
      "memory-search": {
        "enabled": true
      },
      "rag-evaluation": {
        "enabled": true
      },
      "self-evolution": {
        "enabled": true
      },
      "websearch": {
        "enabled": true
      }
    }
  }
}
```

**Agent 特定配置：**

```json
// ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "memory-search": {
        "enabled": true,
        "env": {
          "MAX_MEMORIES": "100"
        }
      },
      "self-evolution": {
        "enabled": false  // baby1 禁用自进化
      }
    }
  }
}
```

### 技能上下文

```python
# skills/skill_context.py

from pathlib import Path
import os

class SkillContext:
    """技能上下文 - 自动适配当前 Agent"""
    
    WORKSPACE_ROOT = Path(__file__).parent.parent
    
    @staticmethod
    def get_current_agent():
        """获取当前 Agent 名称"""
        return os.environ.get('OPENCLAW_AGENT', 'main')
    
    @staticmethod
    def get_config():
        """加载当前 Agent 的配置"""
        agent_name = SkillContext.get_current_agent()
        
        config_file = SkillContext.WORKSPACE_ROOT / "config" / "agents.yaml"
        import yaml
        with open(config_file, 'r') as f:
            all_config = yaml.safe_load(f)
        
        return all_config.get(agent_name, {})
    
    @staticmethod
    def get_data_path():
        """获取当前 Agent 的数据路径"""
        config = SkillContext.get_config()
        data_path_rel = config.get('data_path', f'data/{SkillContext.get_current_agent()}')
        
        return SkillContext.WORKSPACE_ROOT / data_path_rel
    
    @staticmethod
    def is_skill_enabled(skill_name):
        """检查技能是否启用"""
        config = SkillContext.get_config()
        skills = config.get('skills', {})
        skill_config = skills.get(skill_name, {})
        
        if isinstance(skill_config, dict):
            return skill_config.get('enabled', True)
        return bool(skill_config)
```

---

## 数据管理

### 数据存储结构

```
workspace-ai-baby/data/
├── main/                    # 主 Agent 数据
│   ├── memory/
│   │   ├── memory_stream.db
│   │   └── knowledge_base.db
│   ├── logs/
│   │   ├── agent.log
│   │   └── skills.log
│   └── cache/
│       └── embedding_cache.pkl
│
├── baby1/                   # baby1 数据
│   ├── memory/
│   ├── logs/
│   └── cache/
│
├── baby2/                   # baby2 数据
│   ├── memory/
│   └── logs/
│
└── baby3/                   # baby3 数据
    ├── memory/
    └── logs/
```

### 数据隔离策略

| 数据类型 | 隔离级别 | 说明 |
|----------|----------|------|
| **记忆数据** | 严格隔离 | 每个 Agent 独立数据库 |
| **日志** | 严格隔离 | 每个 Agent 独立日志 |
| **缓存** | 可选共享 | 公共缓存可共享 |
| **知识** | 可选共享 | public 可共享，private 隔离 |

---

## 配置管理

### 配置文件结构

```
config/
├── agents.yaml              # ⭐ 所有 Agent 配置
└── skills/                  # 技能配置
    ├── memory-search.yaml
    ├── rag-evaluation.yaml
    ├── self-evolution.yaml
    └── websearch.yaml
```

### 配置加载顺序

```
1. 默认配置 (skills/*/config.example.yaml)
   ↓
2. 技能配置 (config/skills/*.yaml)
   ↓
3. Agent 配置 (config/agents.yaml)
   ↓
4. 环境变量 (覆盖所有配置)
```

---

## 与 OpenClaw 集成

### OpenClaw 管理机制

**当前 OpenClaw 使用方式：**

- **配置格式**: JSON (`~/.openclaw/openclaw.json`)
- **Agent 管理**: `~/.openclaw/agents/<name>/`
- **技能管理**: 原生技能 (`nativeSkills: "auto"`)
- **会话管理**: `~/.openclaw/agents/<name>/sessions/`
- **记忆管理**: `~/.openclaw/memory/` + Agent 专属记忆

**Agent 配置示例：**

```json
// ~/.openclaw/agents/ai-baby/agent.json
{
  "name": "ai-baby",
  "model": "bailian/qwen3.5-plus",
  "thinking": "off",
  "timeoutSeconds": 120,
  "contextWindow": 100000,
  "description": "AI Baby Agent - 轻量级学习代理"
}
```

---

### MCP 集成方案

#### MCP Server 架构

**运行位置：** 🏠 **本地进程**（不是网络服务）

```
┌─────────────────────────────────────────────────────────┐
│  本地电脑                                                │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  MCP Server (本地 Python 进程)                      │  │
│  │  - 命令：python3 -m skills.mcp_server             │  │
│  │  - 位置：workspace-ai-baby/                        │  │
│  │  - 访问：本地文件、数据库、网络                    │  │
│  └───────────────────────────────────────────────────┘  │
│                         ↑↓                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  OpenClaw Gateway (本地 Node.js 进程)               │  │
│  │  - 启动 MCP Server 作为子进程                       │  │
│  │  - 通过 STDIN/STDOUT 通信                          │  │
│  └───────────────────────────────────────────────────┘  │
│                         ↑↓                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  云端 LLM (HTTPS API)                              │  │
│  │  - Bailian/Qwen (阿里云)                           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### MCP Server 实现

```python
# skills/mcp_server.py

from mcp.server import Server
import sqlite3
from pathlib import Path

# 创建 MCP 服务器（本地进程）
server = Server("ai-baby-skills")

@server.list_tools()
async def list_tools():
    """告诉 OpenClaw 有哪些技能可用"""
    return [
        Tool(
            name="memory_search",
            description="搜索本地记忆库",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 5},
                    "semantic": {"type": "boolean", "default": False}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="rag_report",
            description="生成 RAG 评估报告",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "default": 7}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, args: dict):
    """执行技能 - 在本地运行"""
    
    if name == "memory_search":
        # ✅ 访问本地数据库
        db_path = Path.home() / '.openclaw/workspace-ai-baby-config/memory/memory_stream.db'
        conn = sqlite3.connect(db_path)
        
        # ✅ 访问本地文件
        config_file = Path('config/agents.yaml')
        
        # ✅ 访问本地网络
        # requests.get('http://localhost:11434/api/embeddings')
        
        return results
    
    elif name == "rag_report":
        # 生成 RAG 报告
        from skills.rag_evaluation import generate_report
        report = generate_report(days=args.get("days", 7))
        return [TextContent(type="text", text=report)]
    
    else:
        raise ValueError(f"未知技能：{name}")

# 启动服务器（作为本地进程运行）
if __name__ == "__main__":
    server.run()
```

#### 配置到 OpenClaw

```json
// ~/.openclaw/openclaw.json
{
  "mcp": {
    "servers": [
      {
        "name": "ai-baby-skills",
        "command": "python3",
        "args": ["-m", "skills.mcp_server"],
        "cwd": "/Users/dhr/.openclaw/workspace-ai-baby",
        "env": {
          "OPENCLAW_WORKSPACE": "/Users/dhr/.openclaw/workspace-ai-baby"
        }
      }
    ]
  }
}
```

**配置说明：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | MCP Server 名称 | `ai-baby-skills` |
| `command` | 启动命令（本地） | `python3` |
| `args` | 命令参数 | `["-m", "skills.mcp_server"]` |
| `cwd` | 工作目录（本地路径） | `workspace-ai-baby/` |
| `env` | 环境变量 | `OPENCLAW_WORKSPACE=...` |

---

### MCP 工作流程

```
1. OpenClaw Gateway 启动
   ↓
2. 启动 MCP Server (本地 Python 进程)
   ↓
3. Gateway 请求技能列表：list_tools()
   ↓
4. MCP Server 返回：[memory_search, rag_report, ...]
   ↓
5. Gateway 发送技能定义给云端 LLM
   ↓
6. 用户发送消息："搜索 RAG 相关的记忆"
   ↓
7. 云端 LLM 决定调用：memory_search(query="RAG")
   ↓
8. Gateway 调用 MCP Server: call_tool("memory_search", {...})
   ↓
9. MCP Server 在本地执行（访问本地数据库）
   ↓
10. 返回结果给 Gateway
    ↓
11. Gateway 发送给云端 LLM
    ↓
12. LLM 生成自然语言回复
    ↓
13. 返回给用户
```

---

### 安全边界

**MCP Server 可以访问：**

- ✅ 本地文件（workspace-ai-baby/ 下）
- ✅ 本地数据库（SQLite）
- ✅ 本地网络（localhost:* 端口）
- ✅ 环境变量

**MCP Server 不能直接访问：**

- ❌ 云端 LLM（需要通过 Gateway）
- ❌ 用户消息（需要通过 Gateway 传递）
- ❌ 其他进程（除非明确配置）

---

### 创建子 Agent 流程

```bash
# Step 1: 在 OpenClaw 中注册 Agent
openclaw agents add baby1 \
  --workspace ~/.openclaw/workspace-ai-baby \
  --name "Baby1 Sandbox" \
  --emoji "🧪"

# Step 2: 在 workspace 下创建子 Agent 配置
cd ~/.openclaw/workspace-ai-baby

python3 scripts/create_agent.py baby1 tester --emoji "🧪"

# Step 3: 配置 MCP（如果需要）
# 编辑 ~/.openclaw/openclaw.json
# 添加 mcp.servers[]

# Step 4: 验证
openclaw agents list

# Step 5: 测试
openclaw agent baby1 "测试记忆搜索"
```

---

## 实施计划

### Phase 1: 基础架构（已完成 ✅）

- [x] 技能系统实现
- [x] 配置分离实现
- [x] 文档体系建立
- [x] 测试套件建立

**时间：** 2026-03-23  
**状态：** ✅ 完成

---

### Phase 2: 多 Agent 支持（待实施 ⏳）

- [ ] 创建 `config/agents.yaml`
- [ ] 实现 `skills/skill_context.py`
- [ ] 创建 baby1/baby2/baby3 配置
- [ ] 在 OpenClaw 中注册 Agent
- [ ] 测试 Agent 间隔离

**时间：** 2026-03-24 ~ 2026-03-30  
**优先级：** P0

**实施步骤：**

```bash
# 1. 创建 Agent 配置
python3 scripts/create_agent.py baby1 tester
python3 scripts/create_agent.py baby2 ecommerce
python3 scripts/create_agent.py baby3 creator

# 2. 在 OpenClaw 中注册
openclaw agents add baby1 --workspace ~/.openclaw/workspace-ai-baby
openclaw agents add baby2 --workspace ~/.openclaw/workspace-ai-baby
openclaw agents add baby3 --workspace ~/.openclaw/workspace-ai-baby

# 3. 测试
openclaw agent baby1 "测试"
openclaw agent baby2 "测试"
openclaw agent baby3 "测试"
```

---

### Phase 3: 技能优化（待实施 ⏳）

- [ ] 实现 MCP 服务器
- [ ] 注册所有技能
- [ ] 测试工具调用
- [ ] 性能优化

**时间：** 2026-04-01 ~ 2026-04-15  
**优先级：** P1

---

### Phase 4: 知识共享（待实施 ⏳）

- [ ] 实现知识共享机制
- [ ] 创建公共知识库
- [ ] 实现访问控制
- [ ] 知识流转审批流程

**时间：** 2026-04-16 ~ 2026-04-30  
**优先级：** P2

---

## 关键决策

### 决策 1：单一 Workspace

**决策：** ✅ 只有一个 workspace-ai-baby，所有 Agent 共享

**理由：**
- 维护简单
- 技能代码不重复
- 配置集中管理

**影响：**
- 数据通过 data/<agent>/ 隔离
- 配置通过 config/agents.yaml 区分

---

### 决策 2：利用 OpenClaw 原生能力

**决策：** ✅ 使用 OpenClaw 的 Agent 管理，不重复造轮子

**理由：**
- OpenClaw 已有完整的 Agent 管理
- 避免维护两套系统
- 更好的兼容性

**影响：**
- workspace 专注于技能提供
- Agent 路由由 OpenClaw 管理

---

### 决策 3：技能可选配置

**决策：** ✅ 每个 Agent 可独立配置启用的技能

**理由：**
- 灵活性强
- 资源优化
- 安全隔离

**影响：**
- 需要实现 skill_context.py
- 配置管理复杂度增加

---

## 风险与缓解

### 风险 1：配置复杂度

**风险：** 多 Agent + 多技能导致配置复杂

**缓解：**
- 提供配置模板
- 实现配置验证
- 文档完善

---

### 风险 2：数据一致性

**风险：** 知识共享可能导致数据不一致

**缓解：**
- 实现版本控制
- 审批流程
- 冲突解决机制

---

### 风险 3：性能问题

**风险：** 多 Agent 并发可能影响性能

**缓解：**
- 性能监控
- 资源限制
- 缓存优化

---

## 总结

### 架构优势

- ✅ **简单** - 单一 workspace，维护成本低
- ✅ **灵活** - 技能可选，Agent 可扩展
- ✅ **安全** - 数据隔离，配置分离
- ✅ **可维护** - 模块化设计，文档完善
- ✅ **可扩展** - 新 Agent/新技能快速添加

### 下一步行动

1. **Phase 2** - 实施多 Agent 支持（本周）
2. **Phase 3** - 技能优化与 MCP 集成（下周）
3. **Phase 4** - 知识共享机制（下月）

### 成功标准

- [ ] 所有 Agent 正常运行
- [ ] 技能按需启用
- [ ] 数据正确隔离
- [ ] 知识共享正常
- [ ] 性能达标

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23 13:52  
**版本：** v5.1  
**状态：** ✅ 设计完成，待实施
