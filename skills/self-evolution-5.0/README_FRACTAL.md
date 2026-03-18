# 分形思考引擎 (Fractal Thinking Engine)

## 🧠 系统概述

参考 TinkerClaw 的分形思考设计，实现从问题到元规则的 4 层自动分析。

**核心思想：** 每个问题都包含多个层次的学习机会，自动挖掘这些层次实现自我进化。

## 📊 4 层分析架构

```
Level 0 - Solve (解决问题)
    ↓
Level 1 - Pattern (识别模式)
    ↓
Level 2 - Correction (修正规则)
    ↓
Level 3 - Meta-Rule (编码元规则)
```

### Level 0: Solve - 解决问题

**输入：** 进化事件  
**输出：** 问题描述 + 解决方案  
**问题：** "问题是什么？如何解决的？"

示例：
```
问题：Bug - 修复知识库表结构
解决：已添加 thinking 和 key_point 字段
```

### Level 1: Pattern - 识别模式

**输入：** Level 0 分析 + 历史事件  
**输出：** 模式识别结果  
**问题：** "为什么这个问题存在？是孤立事件还是重复模式？"

检测的模式：
- 🔴 重复出现的 Bug（≥2 次）
- 🟡 功能快速增加（≥3 次）
- 🟢 知识获取频繁（≥3 次）
- 🔵 持续代码改进（≥2 次）
- 🟣 系统自进化活跃期（≥3 次）

### Level 2: Correction - 修正规则

**输入：** Level 1 模式分析  
**输出：** 规则缺陷 + 修正建议  
**问题：** "什么规则/限制导致了这个问题？如何修正？"

示例：
```
规则缺陷：Bug 重复出现 → 测试覆盖不足或代码审查缺失
修正建议：建立自动化测试 + 代码审查流程
```

### Level 3: Meta-Rule - 编码元规则

**输入：** Level 2 规则修正  
**输出：** 元规则（防止再犯的原则）  
**问题：** "如何设计元规则防止类似问题再次发生？"

生成的元规则：
```
1. 任何代码变更必须伴随测试更新
2. 重要变更需要同行评审
3. 功能开发前先设计架构
4. 学习新知识时更新知识图谱
5. 实现功能时先考虑边界情况
```

## 🚀 使用方法

### 手动运行

```bash
cd /Users/dhr/.openclaw/workspace/skills/self-evolution-5.0
python3 fractal_thinking.py
```

### 编程调用

```python
from fractal_thinking import FractalThinkingEngine

engine = FractalThinkingEngine()

# 分析最近的进化事件
results = engine.process_events(limit=10)

# 获取分形洞察
insights = engine.get_fractal_insights(query="Bug 修复", limit=5)

# 显示报告
print(results['report'])
```

## 📁 文件位置

- **核心代码**: `fractal_thinking.py`
- **依赖模块**: 
  - `memory_stream.py` - 记忆流存储
  - `self_evolution_real.py` - 进化事件记录

## 📊 输出示例

```
======================================================================
🧠 分形思考引擎
======================================================================

📊 分析 10 个进化事件...
======================================================================

事件 1/10: BUG_FIX
   修复知识库表结构...
  L0 🎯 Bug: 修复知识库表结构... → 已修复...
  L1 🔍 检测到模式：重复出现的 Bug, 持续代码改进...
  L2 🔧 规则缺陷：测试覆盖不足... → 建立自动化测试...
  L3 📜 元规则：任何代码变更必须伴随测试更新...

======================================================================
📊 分形分析总结
======================================================================

总分析数：40
   Level 0 (Solve): 10 个
   Level 1 (Pattern): 10 个
   Level 2 (Correction): 10 个
   Level 3 (Meta-Rule): 10 个

检测到的模式:
   - 重复出现的 Bug: 10 次
   - 持续代码改进，技术债务累积: 10 次

生成的元规则:
   1. 任何代码变更必须伴随测试更新
   2. 重要变更需要同行评审
```

## 🔧 配置选项

### 模式识别规则

在 `fractal_thinking.py` 中修改：

```python
self.pattern_rules = {
    'recurring_bug': {
        'keywords': ['BUG_FIX', 'BUG', '修复', '错误', '问题'],
        'threshold': 2,  # 出现次数阈值
        'pattern_description': '重复出现的 Bug'
    },
    # ... 其他模式
}
```

### 元规则生成

在 `_analyze_level_3()` 方法中自定义元规则生成逻辑。

## 📈 效果指标

| 指标 | 当前值 | 目标 |
|------|--------|------|
| 分析事件数 | 10 | 持续积累 |
| 检测模式数 | 5 | 5-10 个 |
| 生成元规则 | 2 | 持续积累 |
| 元规则应用 | 待追踪 | 100% |

## 🔗 与记忆流集成

分形分析结果自动存入记忆流：

```python
# 每个层级的分析都作为反思记忆存储
self.memory_stream.add_memory(
    content=analysis.description,
    memory_type='reflection',
    tags=[f'Fractal_L{analysis.level}', analysis.level_name],
    importance=8.0 if analysis.level >= 2 else 6.0,
    metadata=analysis.metadata
)
```

这样可以通过记忆流检索历史分形洞察。

## 🎯 与夜间循环集成

分形思考可以集成到夜间进化循环中：

```python
# 在 nightly_cycle.py 的 Auto-Evolution 任务中
from fractal_thinking import FractalThinkingEngine

engine = FractalThinkingEngine()
results = engine.process_events(limit=10)

# 将元规则作为目标记忆存储
for rule in results['meta_rules']:
    self.memory_stream.add_memory(
        content=rule,
        memory_type='goal',
        tags=['元规则', '分形思考'],
        importance=9.0
    )
```

## 📚 参考项目

**TinkerClaw** - 分形思考原创设计
- https://github.com/globalcaos/tinkerclaw
- 核心思想：从问题求解到元规则编码的自动分析

## 🚀 下一步优化

1. **增强模式识别**
   - 使用语义相似度而非关键词匹配
   - 添加更多模式类型

2. **元规则应用追踪**
   - 记录元规则如何影响后续决策
   - 评估元规则的有效性

3. **自动化应用**
   - 将元规则编码为自动化检查
   - 在代码提交时自动验证
