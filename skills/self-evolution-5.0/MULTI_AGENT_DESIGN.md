# 多 Agent 数据隔离设计

**问题：** self-evolution-5.0 被多个 Agent 使用时，是否有数据隔离问题？

**答案：** ✅ 当前设计**支持**多 Agent 使用，但需要**正确配置**。

---

## 📊 当前架构分析

### 数据存储方式

**当前使用的数据库：**
```python
# memory_stream.py
DB_PATH = '/Users/dhr/.openclaw/workspace/memory/memory_stream.db'

# knowledge_base.py  
DB_PATH = '/Users/dhr/.openclaw/workspace/memory/knowledge_base.db'

# self_evolution_real.py
DB_PATH = '/Users/dhr/.openclaw/workspace/skills/evolution-workbench/evolution.db'
```

**问题：**
- ❌ 所有 Agent 共享同一个数据库
- ❌ 数据没有 Agent 标识
- ❌ sandbox-agent 的记忆会混入 main-agent 的数据

---

## 🎯 解决方案

### 方案 1: 每个 Agent 独立数据库（推荐）

**原理：** 每个 Agent 有自己的数据库文件

**实现：**
```python
# 在初始化时指定 agent_id
class MemoryStream:
    def __init__(self, agent_id=None, db_path=None):
        if agent_id and not db_path:
            # 每个 Agent 独立的数据库
            db_path = f'/Users/dhr/.openclaw/workspace/memory/{agent_id}_memory_stream.db'
        self.db_path = db_path or '/Users/dhr/.openclaw/workspace/memory/memory_stream.db'
```

**使用：**
```python
# main-agent 使用
main_memory = MemoryStream(agent_id='main')

# sandbox-agent 使用
sandbox_memory = MemoryStream(agent_id='sandbox')

# 两个数据库完全隔离
```

**优点：**
- ✅ 完全隔离
- ✅ 互不干扰
- ✅ 易于备份和清理

**缺点：**
- ❌ 数据不共享
- ❌ 占用更多空间

---

### 方案 2: 数据中添加 agent_id 标识

**原理：** 共享数据库，但每条数据都有 agent_id

**实现：**
```python
class MemoryStream:
    def __init__(self, agent_id=None):
        self.agent_id = agent_id
        self.db_path = '/Users/dhr/.openclaw/workspace/memory/memory_stream.db'
    
    def add_memory(self, content, **kwargs):
        # 添加 agent_id 到元数据
        metadata = kwargs.get('metadata', {})
        metadata['agent_id'] = self.agent_id
        kwargs['metadata'] = metadata
        # ... 存储
```

**查询时过滤：**
```python
def get_memories(self, agent_id=None):
    # 只查询当前 Agent 的数据
    if agent_id:
        cursor.execute(
            "SELECT * FROM memories WHERE metadata LIKE ?",
            (f'%{agent_id}%',)
        )
```

**优点：**
- ✅ 数据集中管理
- ✅ 可以选择共享或隔离
- ✅ 节省空间

**缺点：**
- ❌ 查询复杂
- ❌ 可能误查其他 Agent 数据

---

### 方案 3: 混合模式（最佳实践）

**原理：** 核心数据隔离，共享数据可选

**实现：**
```python
class MemoryStream:
    def __init__(self, agent_id=None, shared=False):
        if shared:
            # 共享数据库（公共知识）
            self.db_path = '/Users/dhr/.openclaw/workspace/memory/memory_stream.db'
        else:
            # 独立数据库（私有记忆）
            self.db_path = f'/Users/dhr/.openclaw/workspace/memory/{agent_id}_memory_stream.db'
        
        self.agent_id = agent_id
        self.shared = shared
```

**使用场景：**
- **私有记忆** - 每个 Agent 自己的经验 → 独立数据库
- **公共知识** - 所有 Agent 共享的知识 → 共享数据库

**示例：**
```python
# main-agent
main_private = MemoryStream(agent_id='main', shared=False)  # 私有记忆
main_shared = MemoryStream(shared=True)  # 公共知识

# sandbox-agent
sandbox_private = MemoryStream(agent_id='sandbox', shared=False)  # 私有记忆
sandbox_shared = MemoryStream(shared=True)  # 公共知识

# sandbox 可以访问公共知识，但不能访问 main 的私有记忆
```

---

## 📊 当前状态评估

### self-evolution-5.0

**当前问题：**
- ❌ 没有 agent_id 参数
- ❌ 所有数据存到同一个数据库
- ❌ sandbox-agent 和 main-agent 数据混合

**需要改进：**
```python
# 修改前
memory = MemoryStream()

# 修改后
memory = MemoryStream(agent_id='sandbox')  # 指定 Agent ID
```

---

### sandbox-evolution skill

**当前设计：**
```python
class SandboxEvolution:
    def __init__(self):
        self.memory_stream = MemoryStream()  # ❌ 没有 agent_id
        self.evolution = RealSelfEvolution()
```

**需要改进：**
```python
class SandboxEvolution:
    def __init__(self, agent_id='sandbox'):
        self.agent_id = agent_id
        self.memory_stream = MemoryStream(agent_id=agent_id)
        self.evolution = RealSelfEvolution(agent_id=agent_id)
```

---

## 🎯 推荐方案

### 对于 self-evolution-5.0

**使用方案 3（混合模式）：**

1. **私有数据** - 每个 Agent 独立数据库
   - 个人记忆
   - 个人经验
   - 个人反思

2. **共享数据** - 所有 Agent 共享
   - 公共知识库
   - 通用元规则
   - 跨 Agent 经验

**实现步骤：**
```python
# 1. 修改 MemoryStream 支持 agent_id
class MemoryStream:
    def __init__(self, agent_id=None, shared=False):
        if shared:
            self.db_path = SHARED_DB_PATH
        elif agent_id:
            self.db_path = f"{AGENT_DB_DIR}/{agent_id}_memory.db"
        else:
            self.db_path = DEFAULT_DB_PATH

# 2. 修改所有调用
# main-agent
main_memory = MemoryStream(agent_id='main')
main_shared = MemoryStream(shared=True)

# sandbox-agent
sandbox_memory = MemoryStream(agent_id='sandbox')
sandbox_shared = MemoryStream(shared=True)
```

---

### 对于 sandbox-evolution skill

**使用方案 1（完全隔离）：**

```python
# sandbox-agent 有自己的数据库
class SandboxEvolution:
    def __init__(self):
        # sandbox 的独立数据库
        self.memory_stream = MemoryStream(agent_id='sandbox')
        self.evolution = RealSelfEvolution(agent_id='sandbox')
```

**原因：**
- ✅ sandbox 的数据是特定于沙箱执行的
- ✅ 不应该混入 main-agent 的数据
- ✅ 沙箱清理时一起删除

---

## 📋 实施清单

### 短期（本周）

- [ ] 修改 `MemoryStream` 支持 `agent_id` 参数
- [ ] 修改 `KnowledgeBase` 支持 `agent_id` 参数
- [ ] 修改 `RealSelfEvolution` 支持 `agent_id` 参数
- [ ] 为 sandbox-agent 创建独立数据库
- [ ] 测试数据隔离

### 中期（下周）

- [ ] 实现共享数据库模式
- [ ] 添加跨 Agent 数据共享机制
- [ ] 添加数据迁移工具
- [ ] 完善文档

### 长期（本月）

- [ ] 添加数据库加密
- [ ] 添加访问控制
- [ ] 添加数据同步机制
- [ ] 性能优化

---

## ✅ 总结

**当前状态：**
- ❌ 没有数据隔离
- ❌ 所有 Agent 共享数据库
- ⚠️ 存在数据混合风险

**推荐方案：**
- ✅ 私有数据：每个 Agent 独立数据库
- ✅ 共享数据：可选的共享数据库
- ✅ sandbox-agent：完全独立数据库

**实施优先级：**
1. 高：为 sandbox-agent 创建独立数据库
2. 中：修改 self-evolution-5.0 支持 agent_id
3. 低：实现共享数据库模式

---

**需要我立即实施数据隔离吗？** 🔒
