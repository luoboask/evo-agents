# Agent 自进化感知与使用指南

**问题：** 自进化系统在后台运行，但 Agent 如何感知自己的进化？如何在任务中使用进化成果？

---

## 🎯 核心问题

```
❌ 现状：
1. 记忆系统在增长 → Agent 不知道
2. 知识图谱在扩展 → Agent 不查询
3. 元规则在提取 → Agent 不使用
4. 基准测试在运行 → Agent 不看报告

✅ 目标：
1. 任务前主动检索相关记忆
2. 决策时参考元规则
3. 任务后对比预期和结果
4. 定期查看进化报告
```

---

## 🔧 解决方案

### 方案 1: 任务前检索（Pre-Task Retrieval）

**在每次任务执行前，主动检索相关知识：**

```python
# skills/task_executor.py
class ExpertTaskExecutor:
    def __init__(self, agent_name):
        self.memory = MemoryHub(agent_name=agent_name)
        self.kg = KnowledgeGraph()
    
    def prepare_for_task(self, task_description):
        """任务准备：检索相关知识"""
        
        # 1. 检索相关记忆
        related_memories = self.memory.search(
            query=task_description,
            top_k=10,
            semantic=True
        )
        
        # 2. 检索知识图谱
        kg_results = self.kg.search_entities(task_description)
        
        # 3. 检索元规则
        meta_rules = self.memory.search(
            query="元规则 OR 原则 OR 最佳实践",
            top_k=5,
            memory_type='goal'
        )
        
        # 4. 生成任务上下文
        context = {
            'task': task_description,
            'related_memories': related_memories,
            'knowledge': kg_results,
            'meta_rules': meta_rules
        }
        
        return context
    
    def execute(self, task_description):
        # 任务前检索
        context = self.prepare_for_task(task_description)
        
        # 打印检索结果（让 Agent 感知）
        print(f"📚 检索到 {len(context['related_memories'])} 条相关记忆")
        print(f"🕸️ 检索到 {len(context['knowledge'])} 个相关知识")
        print(f"📜 检索到 {len(context['meta_rules'])} 条元规则")
        
        # 基于上下文执行任务
        # ...
```

**使用示例：**

```python
executor = ExpertTaskExecutor('python-expert')

# 执行任务前，Agent 会看到：
context = executor.prepare_for_task("优化 FastAPI 接口性能")

# 输出：
# 📚 检索到 5 条相关记忆
#   - 2026-04-10: 使用异步视图提升性能
#   - 2026-04-08: 添加 Redis 缓存
#   - ...
# 🕸️ 检索到 3 个相关知识
#   - 实体：FastAPI, 异步，缓存
#   - 关系：FastAPI 支持异步，缓存提升性能
# 📜 检索到 2 条元规则
#   - I/O 密集型任务使用 async/await
#   - 数据库查询添加缓存层
```

---

### 方案 2: 决策时参考元规则（Rule-Guided Decision）

**在决策时，主动检索和应用元规则：**

```python
# skills/meta_rule_engine.py
class MetaRuleEngine:
    def __init__(self, agent_name):
        self.memory = MemoryHub(agent_name=agent_name)
    
    def get_applicable_rules(self, situation):
        """获取适用于当前情况的元规则"""
        
        # 检索元规则
        rules = self.memory.search(
            query=situation,
            top_k=10,
            memory_type='goal'
        )
        
        # 过滤和排序
        applicable = []
        for rule in rules:
            if self.is_applicable(rule, situation):
                applicable.append({
                    'rule': rule['content'],
                    'confidence': rule.get('importance', 5.0) / 10.0,
                    'source': rule.get('metadata', {}).get('source', '')
                })
        
        return applicable
    
    def is_applicable(self, rule, situation):
        """判断元规则是否适用"""
        # 简单的关键词匹配
        # 可以用更复杂的语义匹配
        rule_keywords = extract_keywords(rule['content'])
        situation_keywords = extract_keywords(situation)
        
        overlap = len(set(rule_keywords) & set(situation_keywords))
        return overlap > 0


# 使用示例
rule_engine = MetaRuleEngine('python-expert')

# 决策时
situation = "需要优化数据库查询性能"
rules = rule_engine.get_applicable_rules(situation)

print(f"📜 适用的元规则:")
for r in rules:
    print(f"  ✅ {r['rule']} (置信度：{r['confidence']:.0%})")
    print(f"     来源：{r['source']}")

# 输出：
# 📜 适用的元规则:
#   ✅ 数据库查询添加缓存层 (置信度：90%)
#      来源：fractal_analysis_2026-04-08
#   ✅ 使用 EXPLAIN 分析慢查询 (置信度：85%)
#      来源：fractal_analysis_2026-04-05
```

---

### 方案 3: 任务后反思（Post-Task Reflection）

**任务完成后，对比预期和结果，记录学习：**

```python
# skills/task_reflection.py
class TaskReflection:
    def __init__(self, agent_name):
        self.memory = MemoryHub(agent_name=agent_name)
        self.recorder = RealLearningRecorder()
    
    def reflect(self, task, result, expected):
        """任务后反思"""
        
        # 1. 对比预期和结果
        success = result == expected
        gap = self.analyze_gap(result, expected)
        
        # 2. 记录学习
        if success:
            learning_type = '成功经验'
        else:
            learning_type = '失败教训'
        
        self.recorder.record_learning(
            domain='领域名称',
            subtopic='具体主题',
            content=f"任务：{task}\n结果：{result}\n预期：{expected}",
            insight=gap['insight'],
            thinking=gap['thinking'],
            key_point=gap['key_point'],
            learning_type=learning_type
        )
        
        # 3. 生成反思记忆
        reflection = f"""
任务反思：{task}
✅ 成功 / ❌ 失败
差距分析：{gap['analysis']}
关键学习：{gap['key_point']}
元规则更新：{gap['rule_update']}
"""
        
        self.memory.add_memory(
            content=reflection,
            memory_type='reflection',
            importance=8.0 if success else 9.0,  # 失败更重要
            tags=['reflection', task]
        )
        
        return reflection
    
    def analyze_gap(self, result, expected):
        """分析差距"""
        # 实际实现可以用 LLM 分析
        return {
            'insight': '...',
            'thinking': '...',
            'key_point': '...',
            'rule_update': '...'
        }


# 使用示例
reflector = TaskReflection('python-expert')

# 任务完成后
reflection = reflector.reflect(
    task="优化 FastAPI 接口",
    result="响应时间从 500ms 降到 200ms",
    expected="响应时间降到 100ms 以下"
)

print(reflection)
# 输出：
# 任务反思：优化 FastAPI 接口
# ❌ 失败
# 差距分析：性能提升 60%，但未达到目标 80%
# 关键学习：缓存命中率只有 50%，需要优化缓存策略
# 元规则更新：添加"缓存预热"规则
```

---

### 方案 4: 定期进化报告（Evolution Report）

**每周生成进化报告，让 Agent 了解自己的进步：**

```python
# skills/evolution_report.py
class EvolutionReport:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.memory = MemoryHub(agent_name=agent_name)
    
    def generate_weekly_report(self):
        """生成周进化报告"""
        
        # 1. 统计记忆增长
        memories = self.get_all_memories()
        new_memories = [m for m in memories if is_new_this_week(m)]
        
        # 2. 统计知识图谱增长
        kg = self.get_knowledge_graph()
        
        # 3. 统计元规则
        meta_rules = self.get_meta_rules()
        
        # 4. 统计任务
        tasks = self.get_completed_tasks()
        
        # 5. 生成报告
        report = f"""
# 周进化报告 ({self.agent_name})

**时间：** {get_date_range()}

## 📊 成长指标

| 指标 | 本周 | 累计 | 增长率 |
|------|------|------|--------|
| 记忆数 | {len(new_memories)} | {len(memories)} | +{len(new_memories)/max(len(memories)-len(new_memories),1):.0%} |
| 知识实体 | {kg['new']} | {kg['total']} | +{kg['growth_rate']} |
| 元规则 | {len([r for r in meta_rules if is_new(r)])} | {len(meta_rules)} | - |
| 任务完成 | {len(tasks)} | - | - |

## 🧠 关键洞察

{self.generate_insights(new_memories)}

## 📜 新增元规则

{self.format_meta_rules([r for r in meta_rules if is_new(r)])}

## 🎯 下周目标

{self.suggest_goals()}
"""
        
        # 6. 保存报告
        self.save_report(report)
        
        # 7. 让 Agent 感知（添加到记忆）
        self.memory.add_memory(
            content=report,
            memory_type='reflection',
            importance=7.0,
            tags=['weekly_report']
        )
        
        return report
    
    def generate_insights(self, memories):
        """生成洞察"""
        # 分析记忆模式
        # 识别高频主题
        # 提取趋势
        return "..."
    
    def format_meta_rules(self, rules):
        """格式化元规则"""
        return "\n".join([f"- {r['content']}" for r in rules])
    
    def suggest_goals(self):
        """建议目标"""
        return "1. ...\n2. ...\n3. ..."
    
    def save_report(self, report):
        """保存报告"""
        report_file = f"reports/weekly_{get_week_number()}.md"
        with open(report_file, 'w') as f:
            f.write(report)


# 使用示例（每周自动运行）
reporter = EvolutionReport('python-expert')
report = reporter.generate_weekly_report()

print(report)
# 输出完整的周进化报告
```

---

## 🚀 完整集成示例

```python
# skills/expert_agent.py
class ExpertAgent:
    """领域专家 Agent - 集成所有进化感知机制"""
    
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.executor = ExpertTaskExecutor(agent_name)
        self.rule_engine = MetaRuleEngine(agent_name)
        self.reflector = TaskReflection(agent_name)
        self.reporter = EvolutionReport(agent_name)
    
    def handle_task(self, task_description):
        """处理任务（完整流程）"""
        
        print(f"\n🎯 接收任务：{task_description}")
        
        # 1. 任务前检索
        print("\n📚 任务准备...")
        context = self.executor.prepare_for_task(task_description)
        self.print_context(context)
        
        # 2. 获取适用元规则
        print("\n📜 应用元规则...")
        rules = self.rule_engine.get_applicable_rules(task_description)
        self.print_rules(rules)
        
        # 3. 执行任务
        print("\n🔧 执行任务...")
        result = self.execute_task(task_description, context, rules)
        
        # 4. 任务后反思
        print("\n💭 任务反思...")
        reflection = self.reflector.reflect(
            task=task_description,
            result=result,
            expected="预期结果"
        )
        print(reflection)
        
        return result
    
    def print_context(self, context):
        """打印检索到的上下文"""
        print(f"  检索到 {len(context['related_memories'])} 条相关记忆")
        for m in context['related_memories'][:3]:
            print(f"    - {m['content'][:50]}...")
        
        print(f"  检索到 {len(context['knowledge'])} 个相关知识")
        for k in context['knowledge'][:3]:
            print(f"    - {k}")
        
        print(f"  检索到 {len(context['meta_rules'])} 条元规则")
        for r in context['meta_rules'][:2]:
            print(f"    - {r['content'][:50]}...")
    
    def print_rules(self, rules):
        """打印适用的元规则"""
        for r in rules:
            print(f"  ✅ {r['rule']} (置信度：{r['confidence']:.0%})")
    
    def execute_task(self, task, context, rules):
        """执行任务（实际逻辑）"""
        # 基于上下文和元规则执行
        # ...
        return "任务结果"
    
    def weekly_review(self):
        """周回顾"""
        print("\n📊 生成周进化报告...")
        report = self.reporter.generate_weekly_report()
        print(report)


# 使用示例
agent = ExpertAgent('python-expert')

# 处理任务
result = agent.handle_task("优化 FastAPI 接口性能")

# 周回顾（每周运行）
agent.weekly_review()
```

---

## 📋 Cron 配置

```bash
# 每小时检查（检索新知识）
openclaw cron add --cron "0 * * * *" \
  --agent expert-agent \
  --message "python3 skills/expert_agent.py --check" \
  --name "hourly-knowledge-check" \
  --no-deliver --session isolated

# 每周报告（周进化报告）
openclaw cron add --cron "0 9 * * 0" \
  --agent expert-agent \
  --message "python3 skills/expert_agent.py --weekly-review" \
  --name "weekly-evolution-report" \
  --no-deliver --session isolated
```

---

## 📊 感知效果

### 任务执行时

```
🎯 接收任务：优化 FastAPI 接口性能

📚 任务准备...
  检索到 5 条相关记忆
    - 2026-04-10: 使用异步视图提升性能...
    - 2026-04-08: 添加 Redis 缓存...
  检索到 3 个相关知识
    - FastAPI 支持异步
    - 缓存提升性能
  检索到 2 条元规则
    - I/O 密集型任务使用 async/await...

📜 应用元规则...
  ✅ I/O 密集型任务使用 async/await (置信度：95%)
  ✅ 数据库查询添加缓存层 (置信度：90%)

🔧 执行任务...
[任务执行中...]

💭 任务反思...
任务反思：优化 FastAPI 接口
✅ 成功
差距分析：性能提升 75%，接近目标 80%
关键学习：异步 + 缓存组合效果最好
元规则更新：添加"优先使用异步 + 缓存组合"规则
```

### 周回顾时

```
📊 生成周进化报告...

# 周进化报告 (python-expert)

**时间：** 2026-04-05 ~ 2026-04-11

## 📊 成长指标

| 指标 | 本周 | 累计 | 增长率 |
|------|------|------|--------|
| 记忆数 | 50 | 200 | +33% |
| 知识实体 | 15 | 60 | +33% |
| 元规则 | 5 | 25 | +25% |
| 任务完成 | 12 | 50 | - |

## 🧠 关键洞察

本周主要优化方向：性能优化、异步编程、缓存策略

## 📜 新增元规则

- I/O 密集型任务使用 async/await
- 数据库查询添加缓存层
- 使用连接池管理数据库连接
- 优先使用异步 + 缓存组合
- 监控慢查询并优化

## 🎯 下周目标

1. 深入学习 FastAPI 高级特性
2. 完善性能监控体系
3. 整理最佳实践文档
```

---

## ✅ 总结

**让 Agent 感知进化的关键：**

1. **任务前主动检索** - 让 Agent 看到已有的知识
2. **决策时参考元规则** - 让 Agent 使用积累的智慧
3. **任务后反思对比** - 让 Agent 知道哪里可以改进
4. **定期生成报告** - 让 Agent 了解自己的成长

**实现方式：**
- ✅ `ExpertTaskExecutor` - 任务前检索
- ✅ `MetaRuleEngine` - 元规则应用
- ✅ `TaskReflection` - 任务后反思
- ✅ `EvolutionReport` - 定期进化报告

**结果：** Agent 不再是"黑盒"进化，而是**有意识地成长**！🎓
