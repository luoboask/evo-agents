# Sandbox Evolution Skill

**为 sandbox-agent 提供自进化能力**

---

## 🎯 功能

- ✅ 记录沙箱执行过程中的进化事件
- ✅ 从测试结果中学习经验
- ✅ 基于历史经验提供智能建议
- ✅ 基于性能数据优化配置
- ✅ 生成学习报告和统计

---

## 🚀 快速开始

### 1. 在 sandbox-agent 中调用

```python
# 记录事件
await self.call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'SANDBOX_CREATED',
    'instance_id': instance_id,
    'details': {...}
})

# 获取建议
suggestions = await self.call_skill('sandbox-evolution', {
    'action': 'get_suggestions',
    'requirement_id': 'REQ-001'
})

# 从结果学习
await self.call_skill('sandbox-evolution', {
    'action': 'learn_from_result',
    'instance_id': instance_id,
    'report': report
})
```

---

## 📊 可用动作

| 动作 | 说明 | 参数 |
|------|------|------|
| `record_event` | 记录沙箱事件 | event_type, instance_id, details |
| `learn_from_result` | 从测试结果学习 | instance_id, test_result, report |
| `get_suggestions` | 获取智能建议 | requirement_id |
| `get_common_bugs` | 获取常见 Bug | requirement_type |
| `optimize_config` | 优化配置 | instance_id, performance_data |
| `get_stats` | 获取统计 | - |
| `generate_report` | 生成报告 | days |

---

## 📁 文件结构

```
skills/sandbox-evolution/
├── SKILL.md          # 技能说明
├── README.md         # 快速开始
├── USAGE.md          # 详细使用说明
├── __init__.py       # Skill 入口
└── evolution.py      # 核心逻辑
```

---

## 🎯 使用场景

### 场景 1: 创建沙箱时获取历史建议

```python
# 创建沙箱
instance_id = await create_sandbox(config)

# 记录事件
await call_skill('sandbox-evolution', {
    'action': 'record_event',
    'event_type': 'SANDBOX_CREATED',
    'instance_id': instance_id,
    'details': {...}
})

# 获取历史建议
suggestions = await call_skill('sandbox-evolution', {
    'action': 'get_suggestions',
    'requirement_id': config['requirement_id']
})

# 应用建议
for suggestion in suggestions:
    print(f"💡 建议：{suggestion['content']}")
```

### 场景 2: 联调完成后学习

```python
# 执行联调
report = await run_integration(instance_id)

# 从结果学习
await call_skill('sandbox-evolution', {
    'action': 'learn_from_result',
    'instance_id': instance_id,
    'report': report
})

# 生成改进建议
improvements = await call_skill('sandbox-evolution', {
    'action': 'get_improvements',
    'instance_id': instance_id
})
```

---

## 📊 效果

**使用 skill 后：**

| 方面 | 使用前 | 使用后 |
|------|--------|--------|
| 记忆 | ❌ 无 | ✅ 完整记录 |
| 学习 | ❌ 无 | ✅ 从结果学习 |
| 建议 | ❌ 无 | ✅ 智能建议 |
| 改进 | ❌ 无 | ✅ 持续优化 |

---

## 📖 详细文档

- **SKILL.md** - 技能详细说明
- **USAGE.md** - 详细使用指南
- **README.md** - 快速开始

---

## ✅ 总结

**sandbox-evolution skill 让 sandbox-agent 具有：**

- 🧠 记忆能力
- 📚 学习能力
- 💡 智能建议
- 🔄 持续改进

**sandbox-agent 现在是会学习、会思考的智能 Agent！** 🎉
