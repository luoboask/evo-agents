# Agent 感知系统实施指南

**如何让 Agent 感知和使用自进化成果**

---

## 🎯 问题

自进化系统在后台运行，但 Agent：
- ❌ 不知道记忆系统在增长
- ❌ 不查询知识图谱
- ❌ 不使用元规则
- ❌ 不看进化报告

---

## ✅ 解决方案：4 步实施

### 难度：⭐⭐⭐⭐（需要修改 Agent 执行逻辑）
### 时间：2-3 小时

---

## 📋 步骤 1: 添加感知代码（30 分钟）

### 1.1 复制示例代码

```bash
# 复制示例到你的 workspace
cd /Users/dhr/.openclaw/workspace-demo51-agent
cp /Users/dhr/cursor/evo-agents/examples/expert_agent_demo.py \
   skills/expert_agent.py
```

### 1.2 修改为实际任务执行

编辑 `skills/expert_agent.py`：

```python
# 修改 execute_task 方法
def execute_task(self, task, memories, rules):
    """执行实际任务"""
    
    # 1. 构建上下文
    context = {
        'task': task,
        'memories': memories,
        'rules': rules
    }
    
    # 2. 调用 LLM（或你的实际任务处理逻辑）
    # 这里可以用 OpenClaw 的 Harness Agent
    response = self.call_llm(task, context)
    
    return response
```

### 1.3 测试运行

```bash
cd /Users/dhr/.openclaw/workspace-demo51-agent
PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
  python3 skills/expert_agent.py
```

**预期输出**：
```
╔════════════════════════════════════════════════════════╗
║  专家 Agent 感知系统演示                                  ║
╚════════════════════════════════════════════════════════╝

🎯 任务：优化 Python 代码性能

📚 步骤 1: 检索相关知识
  ✅ 找到 5 条相关记忆

📜 步骤 2: 获取适用元规则
  ⚠️  没有找到元规则

🔧 步骤 3: 执行任务
  结果：...

💭 步骤 4: 任务反思
  ✅ 反思已记录
```

---

## 📋 步骤 2: 集成到任务流程（1 小时）

### 2.1 修改任务入口

找到你的任务处理入口（比如 `skills/harness-agent/SKILL.py` 或其他）：

```python
# 在任务处理前添加感知
from expert_agent import SimpleExpertAgent

agent = SimpleExpertAgent('demo51-agent')

# 任务前检索
context = agent.search_memories(task_description, top_k=5)
rules = agent.get_meta_rules()

# 然后执行实际任务
result = execute_task(task, context, rules)

# 任务后反思
agent.reflect(task, result)
```

### 2.2 配置 Cron（自动周回顾）

```bash
# 每周运行周回顾
openclaw cron add --cron "0 10 * * 0" \
  --agent demo51-agent \
  --message "python3 skills/expert_agent.py --weekly-review" \
  --name "weekly-awareness-review" \
  --no-deliver --session isolated
```

---

## 📋 步骤 3: 提取元规则（30 分钟）

### 3.1 运行分形思考

```bash
cd /Users/dhr/.openclaw/workspace-demo51-agent
python3 skills/self-evolution/fractal_thinking.py --limit 50
```

### 3.2 检查元规则

```bash
cd /Users/dhr/.openclaw/workspace-demo51-agent
PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
  python3 -c "
from memory_hub import MemoryHub
memory = MemoryHub(agent_name='demo51-agent')
rules = memory.search('元规则', top_k=10, memory_type='goal')
print(f'找到 {len(rules)} 条元规则')
for r in rules:
    print(f'  - {r.get(\"content\", \"\")[:100]}...')
"
```

---

## 📋 步骤 4: 验证效果（30 分钟）

### 4.1 运行完整测试

```bash
# 处理一个任务
cd /Users/dhr/.openclaw/workspace-demo51-agent
PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
  python3 skills/expert_agent.py

# 查看周回顾
python3 skills/expert_agent.py --weekly-review
```

### 4.2 检查改进

对比使用感知系统前后的效果：

| 指标 | 使用前 | 使用后 |
|------|--------|--------|
| 任务成功率 | ? | ? |
| 元规则使用率 | 0% | ? |
| 记忆检索次数 | 0 | ? |

---

## 🚀 完整示例代码

### expert_agent.py

```python
#!/usr/bin/env python3
"""专家 Agent - 带感知系统"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))

from memory_hub import MemoryHub

class ExpertAgent:
    def __init__(self, agent_name):
        self.memory = MemoryHub(agent_name=agent_name)
    
    def prepare_task(self, task):
        """任务准备"""
        memories = self.memory.search(task, top_k=5)
        rules = self.memory.search('元规则', top_k=5, memory_type='goal')
        return {'memories': memories, 'rules': rules}
    
    def execute(self, task):
        """执行任务"""
        context = self.prepare_task(task)
        print(f"📚 检索到 {len(context['memories'])} 条记忆")
        print(f"📜 检索到 {len(context['rules'])} 条元规则")
        # 执行实际任务...
        return "结果"
    
    def reflect(self, task, result):
        """任务反思"""
        self.memory.add(
            content=f"任务：{task}\n结果：{result}",
            memory_type='reflection',
            importance=7.0
        )

# 使用
agent = ExpertAgent('demo51-agent')
result = agent.execute("你的任务")
agent.reflect("你的任务", result)
```

---

## ✅ 验收标准

完成实施后，你应该能看到：

1. ✅ **任务前** - Agent 主动检索相关记忆和元规则
2. ✅ **任务中** - Agent 参考检索到的知识做决策
3. ✅ **任务后** - Agent 记录反思到记忆系统
4. ✅ **每周** - Agent 生成进化报告

---

## 📊 预期效果

### 使用前

```
接收任务 → 执行 → 完成
（没有检索，没有反思）
```

### 使用后

```
接收任务
  ↓
检索相关记忆（5 条）
  ↓
检索元规则（2 条）
  ↓
基于知识执行
  ↓
记录反思
  ↓
完成
```

---

## 🎯 下一步

1. **运行示例** - `python3 examples/expert_agent_demo.py`
2. **修改代码** - 集成到你的任务流程
3. **提取元规则** - 运行分形思考
4. **验证效果** - 对比使用前后的任务质量

---

**GitHub**: https://github.com/luoboask/evo-agents/commit/b889ba3

**开始实施吧！** 🚀
