# Sandbox Agent 集成自进化能力指南

**创建时间：** 2026-03-17  
**状态：** ✅ 已完成

---

## 🎯 目标

将自进化系统 v5.0 的记忆和学习能力集成到 sandbox-agent 中，使沙箱能够：
1. 自动记录执行过程中的进化事件
2. 从测试结果中学习
3. 生成改进建议
4. 记忆沙箱配置和经验

---

## 📁 文件结构

```
agents/sandbox-agent/
├── agent.py                          # 原有沙箱 Agent
├── evolution_integration.py          # ✨ 新增：自进化集成模块
├── INTEGRATION_GUIDE.md              # ✨ 新增：集成指南
└── config.yaml                       # 配置文件
```

---

## 🔧 集成步骤

### 步骤 1: 导入自进化模块

在 `agent.py` 顶部添加：

```python
# 导入自进化集成
from evolution_integration import SandboxEvolutionIntegration
```

### 步骤 2: 初始化自进化

在 `SandboxAgent.__init__` 中添加：

```python
def __init__(self, workspace_dir=None):
    # ... 原有代码 ...
    
    # ✨ 新增：自进化集成
    self.evolution = SandboxEvolutionIntegration()
    
    print(f"   自进化：已启用")
```

### 步骤 3: 记录沙箱事件

在关键位置记录事件：

```python
async def create_instance(self, requirement_id, config):
    # 原有代码...
    
    # ✨ 新增：记录创建事件
    self.evolution.record_sandbox_event(
        event_type='SANDBOX_CREATED',
        instance_id=instance_id,
        details={
            'requirement_id': requirement_id,
            'description': f'创建{requirement_id}沙箱',
            'config': config
        }
    )
    
    return instance_id
```

### 步骤 4: 从测试结果学习

在联调完成后：

```python
async def run_integration(self, instance_id):
    # 原有代码...
    
    # 执行联调
    report = await self._generate_report(instance, results)
    
    # ✨ 新增：从结果学习
    self.evolution.learn_from_integration_report(instance_id, report)
    
    return report
```

### 步骤 5: 获取智能建议

在创建沙箱前：

```python
async def create_instance(self, requirement_id, config):
    # ✨ 新增：获取历史建议
    suggestions = self.evolution.get_suggestions_for_requirement(requirement_id)
    
    if suggestions:
        print(f"\n💡 基于历史经验的建议:")
        for i, s in enumerate(suggestions[:3], 1):
            print(f"   {i}. {s['content']}")
    
    # 继续创建...
```

---

## 📊 使用示例

### 示例 1: 记录 Bug 并学习

```python
from sandbox_agent import SandboxAgent

agent = SandboxAgent()

# 创建沙箱
instance_id = await agent.create_instance('REQ-001', config)

# 执行联调
report = await agent.run_integration(instance_id)

# 自动记录：
# - 沙箱创建事件
# - 联调执行事件
# - 测试结果（包括 Bug）
# - 从失败中学习
```

### 示例 2: 获取历史建议

```python
# 为新需求获取建议
suggestions = agent.evolution.get_suggestions_for_requirement('REQ-002')

# 输出：
# 💡 基于历史经验的建议:
# 1. 所有 SQL 查询必须使用参数化
# 2. 登录功能需要添加验证码
# 3. 密码必须加密存储
```

### 示例 3: 生成学习报告

```python
# 生成过去 7 天的学习报告
report = agent.evolution.generate_learning_report(days=7)

print(f"过去 7 天:")
print(f"  - 记忆总数：{report['memory']['total']}")
print(f"  - 进化事件：{report['evolution']['total_events']}")
print(f"  - 洞察：{report['insights']}")
```

---

## 🎯 集成功能

### 1. 事件记录

| 事件类型 | 说明 | 自动记录位置 |
|---------|------|-------------|
| `SANDBOX_CREATED` | 沙箱创建 | `create_instance()` |
| `SANDBOX_STARTED` | 沙箱启动 | `start_instance()` |
| `INTEGRATION_STARTED` | 联调开始 | `run_integration()` |
| `INTEGRATION_COMPLETED` | 联调完成 | `run_integration()` |
| `TEST_PASSED` | 测试通过 | `_run_test_case()` |
| `TEST_FAILED` | 测试失败 | `_run_test_case()` |
| `BUG_DETECTED` | 检测到 Bug | `_run_test_case()` |
| `BUG_FIXED` | Bug 修复 | `_run_test_case()` |

### 2. 学习功能

| 功能 | 说明 | 调用方法 |
|------|------|---------|
| 从测试结果学习 | 分析成功/失败原因 | `learn_from_test_result()` |
| 从联调报告学习 | 分析整体通过率 | `learn_from_integration_report()` |
| 获取历史建议 | 基于经验提供建议 | `get_suggestions_for_requirement()` |
| 获取常见 Bug | 某类需求的常见 Bug | `get_common_bugs_for_requirement_type()` |
| 建议测试用例 | 基于历史结果 | `suggest_test_cases()` |

### 3. 优化功能

| 功能 | 说明 | 调用方法 |
|------|------|---------|
| 配置优化 | 基于性能数据 | `optimize_sandbox_config()` |
| 性能分析 | 分析响应时间/资源使用 | `optimize_sandbox_config()` |
| 错误率分析 | 分析错误模式 | `optimize_sandbox_config()` |

---

## 📈 效果对比

### 集成前

```
创建沙箱 → 执行联调 → 生成报告 → 结束

问题：
- 不记录历史经验
- 每次都从头开始
- 同样的 Bug 重复出现
- 无法提供智能建议
```

### 集成后

```
创建沙箱 → 获取历史建议 → 执行联调 → 生成报告
   ↓                              ↓
记录事件 ← ← ← ← ← ← ← ← ← ← 学习经验
   ↓
记忆存储 → 下次使用

优势：
✅ 记录所有历史经验
✅ 提供智能建议
✅ 避免重复 Bug
✅ 持续改进
```

---

## 🔍 实际效果示例

### 场景 1: 第一次执行登录功能联调

```
创建 REQ-001 (登录功能) 沙箱
  ↓
执行联调
  ↓
检测到 SQL 注入漏洞
  ↓
记录：
  - 事件：BUG_DETECTED
  - 教训：所有 SQL 查询必须使用参数化
  - 重要性：9/10
```

### 场景 2: 第二次执行支付功能联调

```
创建 REQ-005 (支付功能) 沙箱
  ↓
获取历史建议
  ↓
💡 基于历史经验的建议:
  1. 所有 SQL 查询必须使用参数化（来自 REQ-001）
  2. 支付金额必须验证范围（来自 REQ-003）
  3. 必须添加事务回滚（来自 REQ-002）
  ↓
执行联调（已避免历史 Bug）
```

---

## 📊 统计数据

集成后可获取的统计：

```python
stats = agent.evolution.get_evolution_stats()

print(f"记忆流统计:")
print(f"  - 总记忆：{stats['memory_stream']['total_memories']}")
print(f"  - 观察：{stats['memory_stream']['by_type']['observation']}")
print(f"  - 反思：{stats['memory_stream']['by_type']['reflection']}")

print(f"进化事件:")
print(f"  - 总事件：{stats['evolution_events']['total_events']}")
print(f"  - Bug 检测：{stats['evolution_events']['by_type']['BUG_DETECTED']}")
print(f"  - 测试失败：{stats['evolution_events']['by_type']['TEST_FAILED']}")
```

---

## 🎯 下一步优化

### 短期（本周）
- [ ] 在 `agent.py` 中完全集成所有调用点
- [ ] 测试所有集成功能
- [ ] 优化重要性评分算法

### 中期（下周）
- [ ] 添加分形思考到沙箱分析
- [ ] 集成模式检测（检测重复 Bug）
- [ ] 生成元规则（从沙箱经验）

### 长期（本月）
- [ ] 沙箱间的知识共享
- [ ] 跨项目经验迁移
- [ ] 自动化配置优化

---

## 💡 总结

**集成自进化能力后，Sandbox Agent 变得：**

| 特性 | 集成前 | 集成后 |
|------|--------|--------|
| 记忆 | ❌ 无 | ✅ 完整记忆流 |
| 学习 | ❌ 无 | ✅ 从结果学习 |
| 建议 | ❌ 无 | ✅ 智能建议 |
| 改进 | ❌ 无 | ✅ 持续优化 |
| 经验 | ❌ 丢失 | ✅ 永久保存 |

**Sandbox Agent 现在是一个会学习、会思考、会改进的智能 Agent！** 🎉
