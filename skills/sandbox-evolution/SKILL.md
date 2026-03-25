# Sandbox Evolution Skill

**功能：** 为 sandbox-agent 提供自进化能力

**描述：** 让 sandbox-agent 能够记录进化事件、从结果学习、提供智能建议

---

## 🎯 功能

1. **记录沙箱事件** - 自动记录沙箱执行过程
2. **从结果学习** - 分析测试成功/失败原因
3. **智能建议** - 基于历史经验提供建议
4. **配置优化** - 基于性能数据优化配置

---

## 🚀 使用方法

### 在 sandbox-agent 中调用

```python
# 方法 1: 直接调用 skill
result = await self.call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'SANDBOX_CREATED',
    'instance_id': instance_id,
    'details': {...}
})

# 方法 2: 使用 evolution 模块
from sandbox_evolution import SandboxEvolution
evolution = SandboxEvolution()
evolution.record_event(...)
```

---

## 📊 API

### record_event

记录沙箱事件

**参数：**
- `event_type`: 事件类型
- `instance_id`: 沙箱实例 ID
- `details`: 详细信息

**事件类型：**
- `SANDBOX_CREATED` - 沙箱创建
- `SANDBOX_STARTED` - 沙箱启动
- `INTEGRATION_STARTED` - 联调开始
- `INTEGRATION_COMPLETED` - 联调完成
- `TEST_PASSED` - 测试通过
- `TEST_FAILED` - 测试失败
- `BUG_DETECTED` - 检测到 Bug
- `BUG_FIXED` - Bug 修复

**示例：**
```python
await self.call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'BUG_DETECTED',
    'instance_id': 'sandbox-REQ-001-abc',
    'details': {
        'description': 'SQL 注入漏洞',
        'severity': 'critical',
        'lesson': '所有 SQL 查询必须使用参数化'
    }
})
```

---

### learn_from_result

从测试结果学习

**参数：**
- `instance_id`: 沙箱实例 ID
- `test_result`: 测试结果
- `report`: 联调报告

**示例：**
```python
await self.call_skill('sandbox-evolution', {
    'action': 'learn_from_result',
    'instance_id': 'sandbox-REQ-001-abc',
    'test_result': {...},
    'report': {...}
})
```

---

### get_suggestions

获取智能建议

**参数：**
- `requirement_id`: 需求 ID

**返回：**
- 建议列表（基于历史经验）

**示例：**
```python
suggestions = await self.call_skill('sandbox-evolution', {
    'action': 'get_suggestions',
    'requirement_id': 'REQ-001'
})

# 返回：
[
    {
        'content': '所有 SQL 查询必须使用参数化',
        'confidence': 0.9,
        'source': 'REQ-003 的经验'
    },
    ...
]
```

---

### optimize_config

优化沙箱配置

**参数：**
- `instance_id`: 沙箱实例 ID
- `current_config`: 当前配置
- `performance_data`: 性能数据

**示例：**
```python
optimizations = await self.call_skill('sandbox-evolution', {
    'action': 'optimize_config',
    'instance_id': 'sandbox-REQ-001-abc',
    'performance_data': {
        'response_time': 1500,
        'memory_usage': 85,
        'error_rate': 6
    }
})
```

---

## 📁 文件结构

```
skills/sandbox-evolution/
├── SKILL.md              # 技能说明
├── __init__.py           # 技能入口
├── evolution.py          # 进化核心逻辑
└── integration.py        # 与 sandbox-agent 集成
```

---

## 🎯 使用场景

### 场景 1: 创建沙箱时

```python
# 1. 创建沙箱
instance_id = await create_sandbox(config)

# 2. 记录事件
await call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'SANDBOX_CREATED',
    'instance_id': instance_id,
    'details': {...}
})

# 3. 获取历史建议
suggestions = await call_skill('sandbox-evolution', {
    'action': 'get_suggestions',
    'requirement_id': config['requirement_id']
})

# 4. 应用建议到沙箱配置
apply_suggestions(instance_id, suggestions)
```

### 场景 2: 联调完成后

```python
# 1. 执行联调
report = await run_integration(instance_id)

# 2. 从结果学习
await call_skill('sandbox-evolution', {
    'action': 'learn_from_result',
    'instance_id': instance_id,
    'report': report
})

# 3. 生成改进建议
improvements = await call_skill('sandbox-evolution', {
    'action': 'get_improvements',
    'instance_id': instance_id
})
```

---

## 📊 效果

### 使用前

```
创建沙箱 → 执行联调 → 生成报告 → 结束

问题:
❌ 不记录历史
❌ 不学习经验
❌ 重复同样 Bug
❌ 没有智能建议
```

### 使用后

```
创建沙箱 → 获取建议 → 执行联调 → 生成报告
   ↓                            ↓
记录事件 ← ← ← ← ← ← ← ← ← ← 学习经验
   ↓
记忆存储 → 下次使用

优势:
✅ 记录所有历史
✅ 提供智能建议
✅ 避免重复 Bug
✅ 持续改进
```

---

## ✅ 总结

**sandbox-evolution skill 让 sandbox-agent 具有：**

| 能力 | 说明 |
|------|------|
| 🧠 记忆能力 | 记录沙箱执行过程 |
| 📚 学习能力 | 从测试结果学习 |
| 💡 智能建议 | 基于历史经验 |
| 🔄 持续改进 | 优化配置和策略 |

**sandbox-agent 现在是会学习、会思考的智能 Agent！** 🎉
