# 🏗️ ai-baby Workspace 架构设计方案

**版本：** v5.1  
**创建时间：** 2026-03-23  
**状态：** ✅ 设计完成，待实施

---

## 📋 目录

1. [背景与目标](#背景与目标)
2. [核心架构](#核心架构)
3. [技能系统](#技能系统)
4. [多 Agent 架构](#多-agent-架构)
5. [数据管理](#数据管理)
6. [配置管理](#配置管理)
7. [实施计划](#实施计划)

---

## 背景与目标

### 当前状态

- ✅ **单一 Agent** - ai-baby 主 Agent
- ✅ **技能系统** - memory-search, rag-evaluation, self-evolution, websearch
- ✅ **配置分离** - 个人数据与代码分离
- ✅ **文档体系** - 18 个完整文档
- ✅ **测试覆盖** - 10 项功能测试全部通过

### 目标架构

- 🎯 **多 Agent 支持** - 主 Agent + 子 Agent (baby1, baby2, baby3...)
- 🎯 **技能可选** - 每个 Agent 按需启用技能
- 🎯 **数据隔离** - Agent 间数据独立，可选共享
- 🎯 **OpenClaw 集成** - 利用 OpenClaw 原生能力
- 🎯 **易于扩展** - 新 Agent/新技能快速添加

---

## 核心架构

### 架构分层

```
┌─────────────────────────────────────────────────────────┐
│                    用户层                                │
│  (通过 OpenClaw TUI/WebChat/Gateway 访问)                │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                  OpenClaw Gateway 层                     │
│  - Session 管理                                          │
│  - Agent 路由                                            │
│  - 记忆管理                                              │
│  - 工具调用                                              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              workspace-ai-baby 层                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  技能层 (skills/)                                  │  │
│  │  - memory-search                                   │  │
│  │  - rag-evaluation                                  │  │
│  │  - self-evolution                                  │  │
│  │  - websearch                                       │  │
│  │  - specialized/ (专用技能)                         │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  配置层 (config/)                                  │  │
│  │  - workspace.yaml     # 工作区配置                │  │
│  │  - agents.yaml        # Agent 配置                │  │
│  │  - skills/            # 技能配置                  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                  数据存储层                              │
│  (~/.openclaw/workspace-*-config/)                      │
│  - memory/        # 记忆数据                            │
│  - knowledge/     # 知识库                              │
│  - logs/          # 日志                                │
│  - cache/         # 缓存                                │
└─────────────────────────────────────────────────────────┘
```

### 职责划分

| 层级 | 职责 | 技术选型 |
|------|------|----------|
| **用户层** | 用户交互 | OpenClaw TUI/WebChat |
| **Gateway 层** | Session/Agent管理 | OpenClaw Gateway |
| **技能层** | 业务逻辑实现 | Python + SQLite |
| **配置层** | 配置管理 | YAML |
| **数据层** | 数据存储 | SQLite + 文件系统 |

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

### 技能配置

```yaml
# config/skills/memory-search.yaml

skill:
  name: memory-search
  version: "1.0"
  description: "关键词 + 语义记忆搜索"

# 技能实现
implementation:
  module: skills.memory_search
  class: MemorySearchSkill

# 数据存储
storage:
  database:
    type: sqlite
    path_pattern: "~/.openclaw/workspace-{agent}-config/memory/memory_stream.db"
  
# 功能配置
features:
  semantic_search:
    enabled: true
    model: nomic-embed-text
    ollama_url: http://localhost:11434
  
# 性能配置
performance:
  max_results: 100
  cache_ttl: 3600
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

---

## 多 Agent 架构

### Agent 配置

```yaml
# config/agents.yaml

# ───────────────────────────────────────────────────────
# 主 Agent
# ───────────────────────────────────────────────────────
ai-baby:
  name: ai-baby
  role: assistant
  description: "主 Agent - 日常 AI 助手"
  
  # 启用的技能（可选配置）
  skills:
    - name: memory-search
      enabled: true
      config:
        semantic_search: true
    
    - name: rag-evaluation
      enabled: true
      config:
        auto_record: true
    
    - name: self-evolution
      enabled: true
      config:
        fractal_thinking: true
        nightly_cycle: false
    
    - name: websearch
      enabled: true
  
  # 数据路径
  data_path: "~/.openclaw/workspace-ai-baby-config/"
  
  # 可以管理子 Agent
  can_manage:
    - baby1
    - baby2
    - baby3

# ───────────────────────────────────────────────────────
# baby1 - 沙箱测试 Agent
# ───────────────────────────────────────────────────────
baby1:
  name: baby1-sandbox
  role: tester
  description: "沙箱 Agent - 测试和实验"
  parent: ai-baby
  
  skills:
    - name: memory-search
      enabled: true
      config:
        max_memories: 100  # 限制记忆数量
    
    - name: rag-evaluation
      enabled: true
    
    # 禁用不需要的技能
    - name: self-evolution
      enabled: false
    
    - name: websearch
      enabled: false
  
  data_path: "~/.openclaw/workspace-baby1-config/"
  
  # 沙箱特定配置
  sandbox:
    auto_cleanup: true
    max_memories: 100

# ───────────────────────────────────────────────────────
# baby2 - 电商运营 Agent
# ───────────────────────────────────────────────────────
baby2:
  name: baby2-ecommerce
  role: ecommerce
  description: "电商 Agent - 自营平台运营"
  parent: ai-baby
  
  skills:
    - name: memory-search
      enabled: true
    
    - name: rag-evaluation
      enabled: true
    
    - name: self-evolution
      enabled: true
    
    # 电商专用技能
    - name: specialized/baby2-ecommerce
      enabled: true
      config:
        platform: taobao
        auto_sync: true
  
  data_path: "~/.openclaw/workspace-baby2-config/"

# ───────────────────────────────────────────────────────
# baby3 - 内容创作 Agent
# ───────────────────────────────────────────────────────
baby3:
  name: baby3-content
  role: creator
  description: "内容 Agent - 内容创作"
  parent: ai-baby
  
  skills:
    - name: memory-search
      enabled: true
    
    - name: rag-evaluation
      enabled: true
    
    - name: self-evolution
      enabled: true
    
    - name: websearch
      enabled: true
      config:
        engine: bing
    
    # 内容创作专用技能
    - name: specialized/baby3-content
      enabled: true
      config:
        auto_save: true
        style: creative
  
  data_path: "~/.openclaw/workspace-baby3-config/"
```

### Agent 关系图

```
ai-baby (主 Agent)
├─ baby1 (沙箱测试)
│   - 技能：memory-search, rag-evaluation
│   - 数据隔离：✅
│   - 自进化：❌
│
├─ baby2 (电商运营)
│   - 技能：memory-search, rag-evaluation, self-evolution, ecommerce
│   - 数据隔离：✅
│   - 电商平台：taobao
│
└─ baby3 (内容创作)
    - 技能：memory-search, rag-evaluation, self-evolution, websearch, content
    - 数据隔离：✅
    - 创作风格：creative
```

---

## 数据管理

### 数据存储结构

```
~/.openclaw/
├── workspace-ai-baby-config/    # 主 Agent 数据
│   ├── memory/
│   │   ├── memory_stream.db
│   │   └── knowledge_base.db
│   ├── knowledge/
│   │   ├── public/          # 公共知识（可共享）
│   │   └── private/         # 私有知识
│   ├── logs/
│   └── cache/
│
├── workspace-baby1-config/    # baby1 数据
│   ├── memory/
│   ├── logs/
│   └── cache/
│
├── workspace-baby2-config/    # baby2 数据
│   ├── memory/
│   ├── knowledge/
│   └── logs/
│
└── workspace-baby3-config/    # baby3 数据
    ├── memory/
    ├── knowledge/
    └── logs/
```

### 数据隔离策略

| 数据类型 | 隔离级别 | 说明 |
|----------|----------|------|
| **记忆数据** | 严格隔离 | 每个 Agent 独立数据库 |
| **知识库** | 可选共享 | public 可共享，private 隔离 |
| **日志** | 严格隔离 | 每个 Agent 独立日志 |
| **缓存** | 可选共享 | 公共缓存可共享 |

### 知识共享机制

```yaml
# config/knowledge-sharing.yaml

sharing:
  # 公共知识库（所有 Agent 可访问）
  public:
    enabled: true
    path: "~/.openclaw/workspace-ai-baby-config/knowledge/public/"
    access: all_agents
  
  # 项目知识库（指定 Agent 可访问）
  projects:
    enabled: true
    path: "~/.openclaw/workspace-ai-baby-config/knowledge/projects/"
    access:
      project-a: [ai-baby, baby1]
      project-b: [ai-baby, baby2]
  
  # 私有知识库（Agent 独立）
  private:
    enabled: true
    path_pattern: "~/.openclaw/workspace-{agent}-config/knowledge/private/"
    access: owner_only
```

---

## 配置管理

### 配置文件结构

```
config/
├── workspace.yaml           # 工作区配置
├── agents.yaml              # Agent 配置
├── skills/                  # 技能配置
│   ├── memory-search.yaml
│   ├── rag-evaluation.yaml
│   ├── self-evolution.yaml
│   └── websearch.yaml
└── knowledge-sharing.yaml   # 知识共享配置
```

### 配置加载顺序

```
1. 默认配置 (skills/*/config.example.yaml)
   ↓
2. 工作区配置 (config/workspace.yaml)
   ↓
3. Agent 配置 (config/agents.yaml)
   ↓
4. 环境变量 (覆盖所有配置)
```

### 配置验证

```python
# config/validator.py

class ConfigValidator:
    """配置验证器"""
    
    @staticmethod
    def validate_agent_config(config):
        """验证 Agent 配置"""
        required_fields = ['name', 'role', 'skills']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"缺少必需字段：{field}")
        
        # 验证技能配置
        for skill in config['skills']:
            if isinstance(skill, dict) and 'name' not in skill:
                raise ValueError("技能配置缺少 name 字段")
        
        return True
    
    @staticmethod
    def validate_skill_config(config):
        """验证技能配置"""
        required_fields = ['name', 'version']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"缺少必需字段：{field}")
        
        return True
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
- [ ] 实现技能加载器
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
openclaw agents add baby1
openclaw agents add baby2
openclaw agents add baby3

# 3. 初始化 Agent 数据
python3 scripts/init_agent_data.py baby1
python3 scripts/init_agent_data.py baby2
python3 scripts/init_agent_data.py baby3

# 4. 测试
python3 scripts/test_agent.py baby1
python3 scripts/test_agent.py baby2
python3 scripts/test_agent.py baby3
```

---

### Phase 3: 知识共享（待实施 ⏳）

- [ ] 实现知识共享机制
- [ ] 创建公共知识库
- [ ] 实现访问控制
- [ ] 知识流转审批流程

**时间：** 2026-04-01 ~ 2026-04-15  
**优先级：** P1

---

### Phase 4: MCP 集成（待实施 ⏳）

- [ ] 实现 MCP 服务器
- [ ] 注册所有技能
- [ ] 测试工具调用
- [ ] 性能优化

**时间：** 2026-04-16 ~ 2026-04-30  
**优先级：** P2

---

### Phase 5: 监控与优化（待实施 ⏳）

- [ ] 实现监控仪表板
- [ ] 性能分析工具
- [ ] 自动化测试
- [ ] 文档完善

**时间：** 2026-05-01 ~ 2026-05-15  
**优先级：** P3

---

## 关键决策

### 决策 1：使用 OpenClaw 原生能力

**决策：** ✅ 利用 OpenClaw 的 Session/Agent 管理，不重复造轮子

**理由：**
- OpenClaw 已有完整的 Session/Agent 管理
- 避免维护两套系统
- 更好的兼容性

**影响：**
- workspace-ai-baby 专注于技能提供
- 不负责 Agent/Session 管理

---

### 决策 2：技能可选配置

**决策：** ✅ 每个 Agent 可独立配置启用的技能

**理由：**
- 灵活性强
- 资源优化
- 安全隔离

**影响：**
- 需要实现技能加载器
- 配置管理复杂度增加

---

### 决策 3：数据严格隔离

**决策：** ✅ Agent 间数据默认隔离，可选共享

**理由：**
- 安全性
- 隐私保护
- 避免数据污染

**影响：**
- 需要实现知识共享机制
- 数据同步复杂度增加

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

- ✅ **灵活** - 技能可选，Agent 可扩展
- ✅ **安全** - 数据隔离，配置分离
- ✅ **可维护** - 模块化设计，文档完善
- ✅ **可扩展** - 新 Agent/新技能快速添加

### 下一步行动

1. **Phase 2** - 实施多 Agent 支持（本周）
2. **Phase 3** - 实现知识共享（下周）
3. **Phase 4** - MCP 集成（下月）

### 成功标准

- [ ] 所有 Agent 正常运行
- [ ] 技能按需启用
- [ ] 数据正确隔离
- [ ] 知识共享正常
- [ ] 性能达标

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23  
**版本：** v5.1  
**状态：** ✅ 设计完成，待实施
