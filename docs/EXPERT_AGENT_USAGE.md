# 专家 Agent 感知系统 - 使用指南

**快速上手，真正能用**

---

## 🚀 5 分钟快速开始

### 步骤 1: 复制脚本

```bash
cd /Users/dhr/.openclaw/workspace-demo51-agent
cp /Users/dhr/cursor/evo-agents/examples/expert_agent_real.py skills/
```

### 步骤 2: 运行第一个任务

```bash
PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
  python3 skills/expert_agent_real.py "优化 Python 代码性能"
```

### 步骤 3: 看到效果

```
📚 检索到 5 条相关记忆
📜 检索到 0 条元规则
🔧 任务完成
💭 反思已记录
```

### 步骤 4: 再次运行

```bash
python3 skills/expert_agent_real.py "优化 Python 代码性能"
```

**看到变化了吗？**
- 第 1 次：检索到 0 条反思
- 第 2 次：检索到 1 条反思（第 1 次的）
- 第 3 次：检索到 2 条反思（第 1、2 次的）

**这就是知识积累！**

---

## 📋 日常使用

### 执行任务

```bash
# 格式
python3 skills/expert_agent_real.py "任务描述"

# 示例
python3 skills/expert_agent_real.py "修复用户登录 Bug"
python3 skills/expert_agent_real.py "添加购物车功能"
python3 skills/expert_agent_real.py "优化数据库查询性能"
```

### 周回顾

```bash
# 每周运行一次
python3 skills/expert_agent_real.py --weekly
```

---

## 🔧 集成到你的代码

### 方法 1: 直接调用

```python
# your_script.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'libs'))

from expert_agent_real import RealExpertAgent

# 创建 Agent
agent = RealExpertAgent('demo51-agent')

# 执行任务
result = agent.execute_task("你的任务")
```

### 方法 2: 作为库使用

```python
# 在你的任务处理函数中
from expert_agent_real import RealExpertAgent

def handle_task(task_description):
    agent = RealExpertAgent()
    
    # 任务前检索
    memories = agent.memory.search(task_description, top_k=5)
    rules = agent.memory.search('元规则', top_k=5, memory_type='goal')
    
    # 基于知识执行你的逻辑
    result = your_actual_task_logic(task_description, memories, rules)
    
    # 任务后反思
    agent._reflect(task_description, result, memories, rules)
    
    return result
```

---

## 💡 实际应用场景

### 场景 1: 客服机器人

```python
# 每次回答用户问题前
agent = RealExpertAgent('customer-service')

# 检索类似问题的处理经验
memories = agent.search_memories(user_question, top_k=5)

# 基于历史回答生成回复
if memories:
    # 参考历史回答
    response = generate_response(user_question, memories)
else:
    # 新问题，创建新回答
    response = create_new_response(user_question)

# 记录这次处理
agent.reflect(user_question, response, memories, [])
```

### 场景 2: 代码审查

```python
# 审查代码前
agent = RealExpertAgent('code-reviewer')

# 检索类似的代码问题
memories = agent.search_memories(code_diff, top_k=5)

# 基于历史审查意见
if memories:
    comments = generate_review_comments(code_diff, memories)
else:
    comments = review_code(code_diff)

# 记录审查经验
agent.reflect(code_diff, comments, memories, [])
```

### 场景 3: 数据分析

```python
# 分析数据前
agent = RealExpertAgent('data-analyst')

# 检索类似的分析任务
memories = agent.search_memories(analysis_task, top_k=5)

# 基于历史分析方法
if memories:
    insights = analyze_data(analysis_task, memories)
else:
    insights = new_analysis(analysis_task)

# 记录分析经验
agent.reflect(analysis_task, insights, memories, [])
```

---

## 📊 效果对比

### 不使用感知系统

```
任务 1: 修复登录 Bug → 搜索 StackOverflow → 修复 → 完成
任务 2: 修复登录 Bug → 搜索 StackOverflow → 修复 → 完成（重复劳动）
任务 3: 修复登录 Bug → 搜索 StackOverflow → 修复 → 完成（还是重复）
```

### 使用感知系统

```
任务 1: 修复登录 Bug
  → 检索（无历史）
  → 搜索 StackOverflow
  → 修复
  → 记录："session 过期导致登录失败，需要刷新 token"

任务 2: 修复登录 Bug
  → 检索（找到任务 1 的记录）
  → 看到"session 过期导致登录失败"
  → 直接检查 token
  → 修复（更快）
  → 记录："token 刷新频率需要调整"

任务 3: 修复登录 Bug
  → 检索（找到任务 1、2 的记录）
  → 看到两条经验
  → 直接修复
  → 记录："添加 token 自动刷新机制"
```

**效率提升：3 倍！**

---

## ⚠️ 常见问题

### Q: 检索不到相关内容？

**A:** 正常，说明是新领域。继续积累，下次就有了。

### Q: 元规则总是 0？

**A:** 需要运行分形思考提取元规则：

```bash
cd /Users/dhr/.openclaw/workspace-demo51-agent
python3 skills/self-evolution/fractal_thinking.py --limit 50
```

### Q: 如何集成到现有项目？

**A:** 参考上面的"集成到你的代码"部分，把 `execute_task` 方法改成调用你的实际逻辑。

---

## 🎯 下一步

1. **每天使用** - 每次任务都运行
2. **每周回顾** - `python3 skills/expert_agent_real.py --weekly`
3. **提取元规则** - 运行分形思考
4. **持续积累** - 3 个月后就是专家！

---

**开始使用吧！** 🚀
