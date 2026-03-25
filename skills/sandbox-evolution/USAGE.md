# Sandbox Evolution Skill 使用说明

**时间：** 2026-03-17  
**状态：** ✅ 已完成

---

## 🎯 这是什么？

这是一个 OpenClaw skill，让 sandbox-agent 能够：
- 记录沙箱执行过程中的进化事件
- 从测试结果中学习
- 获取基于历史经验的智能建议
- 优化沙箱配置

---

## 🚀 在 sandbox-agent 中使用

### 方法 1: 通过 OpenClaw skill 系统调用

```python
# 在 sandbox-agent 的代码中
result = await self.call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'SANDBOX_CREATED',
    'instance_id': instance_id,
    'details': {
        'requirement_id': 'REQ-001',
        'description': '创建登录功能沙箱'
    }
})
```

### 方法 2: 直接导入模块

```python
# 在 sandbox-agent 中导入
from skills.sandbox-evolution import SandboxEvolution

# 创建实例
evolution = SandboxEvolution()

# 记录事件
evolution.record_sandbox_event(
    event_type='SANDBOX_CREATED',
    instance_id=instance_id,
    details={...}
)

# 获取建议
suggestions = evolution.get_suggestions_for_requirement('REQ-001')
```

---

## 📊 可用动作

### record_event - 记录事件

```python
result = await call_skill('sandbox-evolution', {
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

**事件类型：**
- `SANDBOX_CREATED` - 沙箱创建
- `SANDBOX_STARTED` - 沙箱启动
- `INTEGRATION_STARTED` - 联调开始
- `INTEGRATION_COMPLETED` - 联调完成
- `TEST_PASSED` - 测试通过
- `TEST_FAILED` - 测试失败
- `BUG_DETECTED` - 检测到 Bug
- `BUG_FIXED` - Bug 修复

---

### learn_from_result - 从结果学习

```python
result = await call_skill('sandbox-evolution', {
    'action': 'learn_from_result',
    'instance_id': 'sandbox-REQ-001-abc',
    'test_result': {
        'validation': {
            'success': False,
            'bugs': [{'description': '空密码未处理'}]
        }
    },
    'report': {
        'summary': {'total': 10, 'passed': 8, 'failed': 2}
    }
})
```

---

### get_suggestions - 获取建议

```python
suggestions = await call_skill('sandbox-evolution', {
    'action': 'get_suggestions',
    'requirement_id': 'REQ-001'
})

# 返回：
[
    {
        'content': '所有 SQL 查询必须使用参数化',
        'confidence': 0.9,
        'source': '2026-03-17T10:00:00'
    },
    ...
]
```

---

### get_common_bugs - 获取常见 Bug

```python
bugs = await call_skill('sandbox-evolution', {
    'action': 'get_common_bugs',
    'requirement_type': '登录'
})

# 返回：
[
    {
        'description': 'SQL 注入漏洞',
        'importance': 9,
        'confidence': 0.85
    },
    ...
]
```

---

### optimize_config - 优化配置

```python
result = await call_skill('sandbox-evolution', {
    'action': 'optimize_config',
    'instance_id': 'sandbox-REQ-001-abc',
    'performance_data': {
        'response_time': 1500,
        'memory_usage': 85,
        'error_rate': 6
    }
})

# 返回：
{
    'success': True,
    'suggestions': [
        {
            'type': 'performance',
            'issue': '响应时间过长',
            'suggestion': '考虑添加缓存',
            'priority': 'high'
        }
    ]
}
```

---

### get_stats - 获取统计

```python
stats = await call_skill('sandbox-evolution', {
    'action': 'get_stats'
})

# 返回：
{
    'memory_stream': {
        'total_memories': 333,
        'by_type': {...}
    },
    'evolution_events': {
        'total_events': 285,
        'by_type': {...}
    }
}
```

---

### generate_report - 生成报告

```python
report = await call_skill('sandbox-evolution', {
    'action': 'generate_report',
    'days': 7
})

# 返回：
{
    'period': '过去 7 天',
    'memory': {
        'total': 333,
        'recent_24h': 50
    },
    'evolution': {
        'total_events': 285
    },
    'insights': [
        '反思活跃，系统正在积极学习'
    ]
}
```

---

## 📋 完整使用示例

### 在 sandbox-agent 的 create_instance 中

```python
async def create_instance(self, requirement_id, config):
    # 1. 创建实例
    instance_id = f"sandbox-{requirement_id}-{uuid.uuid4().hex[:8]}"
    
    # 2. 记录事件
    await self.call_skill('sandbox-evolution', {
        'action': 'record_event',
        'event_type': 'SANDBOX_CREATED',
        'instance_id': instance_id,
        'details': {
            'requirement_id': requirement_id,
            'description': f'创建{requirement_id}沙箱',
            'config': config
        }
    })
    
    # 3. 获取历史建议
    suggestions = await self.call_skill('sandbox-evolution', {
        'action': 'get_suggestions',
        'requirement_id': requirement_id
    })
    
    # 4. 应用建议
    if suggestions:
        print(f"\n💡 基于历史经验的建议:")
        for i, s in enumerate(suggestions[:3], 1):
            print(f"   {i}. {s['content']}")
            # 应用到沙箱配置
            apply_suggestion(config, s)
    
    return instance_id
```

### 在 sandbox-agent 的 run_integration 中

```python
async def run_integration(self, instance_id):
    # 1. 执行联调
    report = await self._execute_integration(instance_id)
    
    # 2. 从结果学习
    await self.call_skill('sandbox-evolution', {
        'action': 'learn_from_result',
        'instance_id': instance_id,
        'test_result': report['results'][0],
        'report': report
    })
    
    # 3. 获取改进建议
    improvements = await self.call_skill('sandbox-evolution', {
        'action': 'get_improvements',
        'instance_id': instance_id
    })
    
    # 4. 应用改进
    if improvements:
        print(f"\n🔧 改进建议:")
        for imp in improvements:
            print(f"   - {imp['suggestion']}")
    
    return report
```

---

## 🎯 集成到 sandbox-agent

### 步骤 1: 在 config.yaml 中添加 skill

```yaml
# agents/sandbox-agent/config.yaml
skills:
  - sandbox-evolution
```

### 步骤 2: 在代码中调用

```python
# agents/sandbox-agent/agent.py

# 在关键位置调用 skill
class SandboxAgent:
    async def create_instance(self, requirement_id, config):
        # 记录事件
        await self.call_skill('sandbox-evolution', {...})
        
        # 获取建议
        suggestions = await self.call_skill('sandbox-evolution', {...})
        
        # ...
```

---

## 📊 效果对比

### 不使用 skill

```
创建沙箱 → 执行联调 → 生成报告 → 结束

问题:
❌ 不记录历史
❌ 不学习经验
❌ 重复同样 Bug
```

### 使用 skill

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

**sandbox-evolution skill 为 sandbox-agent 提供：**

| 能力 | 说明 | API |
|------|------|-----|
| 🧠 记忆能力 | 记录沙箱执行 | `record_event()` |
| 📚 学习能力 | 从结果学习 | `learn_from_result()` |
| 💡 智能建议 | 基于历史经验 | `get_suggestions()` |
| 🔧 配置优化 | 基于性能数据 | `optimize_config()` |
| 📊 统计分析 | 生成学习报告 | `get_stats()`, `generate_report()` |

**sandbox-agent 现在是会学习、会思考的智能 Agent！** 🎉
