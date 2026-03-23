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

### 技能接口

```python
# skills/base.py

class BaseSkill:
    """技能基类"""
    
    name = "base"
    version = "1.0"
    description = "基础技能"
    
    def __init__(self, config):
        self.config = config
        self.initialized = False
    
    def initialize(self):
        """初始化技能"""
        self.initialized = True
    
    def cleanup(self):
        """清理资源"""
        pass
    
    def get_capabilities(self):
        """返回技能能力列表"""
        return []
    
    def execute(self, action, **kwargs):
        """执行技能动作"""
        raise NotImplementedError
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

### OpenClaw Agents 配置

```yaml
# ~/.openclaw/agents/baby1/agent.yaml

name: baby1
workspace: ~/.openclaw/workspace-ai-baby
model: bailian/qwen3.5-plus

routing:
  rules:
    - channel: telegram
      account: test-account

env:
  OPENCLAW_AGENT: baby1
  OPENCLAW_WORKSPACE: ~/.openclaw/workspace-ai-baby
  OPENCLAW_DATA_PATH: ~/.openclaw/workspace-ai-baby/data/baby1
```

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

# Step 3: 验证
openclaw agents list

# Step 4: 测试
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
