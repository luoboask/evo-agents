# evo-agents 领域专家培养指南

**如何培养一个领域的专家 Agent**

---

## 🎯 核心原理

```
专家 = 专注领域 + 持续学习 + 深度思考 + 知识积累 + 实践应用
```

---

## 📋 培养步骤

### 步骤 1: 创建专用 Agent

```bash
# 1. 创建专家 Agent 的工作区
openclaw agents add expert-agent --workspace ~/.openclaw/workspace-expert-agent

# 2. 安装 evo-agents
cd ~/.openclaw/workspace-expert-agent
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s expert-agent --force
```

**关键配置**：
- ✅ 独立 workspace
- ✅ 独立数据库
- ✅ 独立记忆系统

---

### 步骤 2: 定义领域范围

**示例：Python 开发专家**

```yaml
# config/domain.yaml
agent_name: python-expert
domain: 软件开发
specialty: Python 开发
subdomains:
  - Web 开发 (FastAPI, Django)
  - 数据分析 (Pandas, NumPy)
  - 自动化脚本
  - 最佳实践
  - 性能优化
excluded:
  - 前端开发 (HTML/CSS/JS)
  - 运维部署
  - 其他语言
```

**关键决策**：
- ✅ **专注** - 只做 Python 相关任务
- ✅ **边界** - 明确不做什么
- ✅ **深度** - 覆盖多个子领域

---

### 步骤 3: 配置 Cron 任务

```bash
# 每小时检查（学习机会）
openclaw cron add --cron "0 * * * *" \
  --agent expert-agent \
  --message "python3 skills/self-evolution/hourly_check.py" \
  --name "hourly-learning" \
  --no-deliver --session isolated

# 每日回顾（整合记忆）
openclaw cron add --cron "0 23 * * *" \
  --agent expert-agent \
  --message "python3 skills/self-evolution/nightly_cycle.py" \
  --name "daily-consolidation" \
  --no-deliver --session isolated

# 每周分形思考（提取元规则）
openclaw cron add --cron "0 10 * * 0" \
  --agent expert-agent \
  --message "python3 skills/self-evolution/fractal_thinking.py --limit 50" \
  --name "weekly-fractal" \
  --no-deliver --session isolated

# 每周基准测试（评估进步）
openclaw cron add --cron "0 11 * * 0" \
  --agent expert-agent \
  --message "python3 benchmarks/comprehensive_test.py --agent expert-agent" \
  --name "weekly-benchmark" \
  --no-deliver --session isolated
```

---

### 步骤 4: 建立领域知识库

#### 4.1 知识图谱构建

```bash
# 每次任务后自动构建
cd ~/.openclaw/workspace-expert-agent
python3 libs/knowledge_graph/builder.py --auto
```

**知识类型**：
```python
entities = {
    'concept': ['装饰器', '生成器', '上下文管理器'],
    'library': ['FastAPI', 'Pandas', 'NumPy'],
    'pattern': ['单例模式', '工厂模式', '观察者模式'],
    'best_practice': ['PEP 8', '类型注解', '单元测试'],
    'performance': ['时间复杂度', '空间复杂度', '缓存策略']
}
```

#### 4.2 每日学习记录

```python
# 每次任务后记录
from auto_learning_rich import RealLearningRecorder

recorder = RealLearningRecorder()

recorder.record_learning(
    domain='Python 开发',
    subtopic='FastAPI 性能优化',
    content='使用异步视图函数提升并发性能',
    insight='async/await 适合 I/O 密集型任务',
    thinking='CPU 密集型任务应该用进程池',
    key_point='理解 GIL 对异步的影响',
    learning_type='项目实践',
    difficulty='中级',
    time_spent='2h',
    outcome='success'
)
```

---

### 步骤 5: 实践 - 反思循环

#### 5.1 任务执行

```python
# 只接受领域相关任务
def accept_task(task):
    if 'Python' in task or 'FastAPI' in task:
        return True
    else:
        return False  # 拒绝非领域任务
```

#### 5.2 分形思考（每次任务后）

```
Level 0: Solve
  问题：FastAPI 接口响应慢
  解决：添加异步和缓存

Level 1: Pattern
  模式：I/O 密集型任务适合异步
  频率：第 3 次遇到类似问题

Level 2: Correction
  规则：默认使用同步视图
  修正：I/O 密集型用异步，CPU 密集型用同步

Level 3: Meta-Rule
  元规则：根据任务类型选择并发模型
  - I/O 密集型 → async/await
  - CPU 密集型 → multiprocessing
  - 混合型 → 任务队列
```

#### 5.3 夜间整合

```python
# 每天 23:00 自动运行
python3 skills/self-evolution/nightly_cycle.py

# 执行任务：
# 1. Wind Down - 生成今日洞察
# 2. Memory Consolidation - 压缩记忆（49% 压缩率）
# 3. Cleaning Lady - 清理临时文件
# 4. Auto-Evolution - 扫描改进机会
```

---

## 📊 成长阶段

### 新手期（1-7 天）

**目标**：建立基础

| 指标 | 目标 |
|------|------|
| 领域任务数 | 10+ |
| 记忆数 | 100+ |
| 知识图谱实体 | 20+ |
| 进化事件 | 10+ |

**关键活动**：
- ✅ 接受所有领域相关任务
- ✅ 记录每次学习
- ✅ 构建基础知识图谱

---

### 成长期（1-4 周）

**目标**：模式识别

| 指标 | 目标 |
|------|------|
| 领域任务数 | 50+ |
| 记忆数 | 500+ |
| 知识图谱实体 | 50+ |
| 元规则数 | 20+ |

**关键活动**：
- ✅ 分形思考提取模式
- ✅ 建立决策规则
- ✅ 定期基准测试

---

### 熟练期（1-3 月）

**目标**：自动化优化

| 指标 | 目标 |
|------|------|
| 领域任务数 | 200+ |
| 记忆数 | 2000+ |
| 知识图谱实体 | 100+ |
| 元规则数 | 50+ |

**关键活动**：
- ✅ 元规则指导决策
- ✅ 预测性问题解决
- ✅ 知识输出（文档/教程）

---

### 专家期（3 月+）

**目标**：预测性决策

| 指标 | 目标 |
|------|------|
| 领域任务数 | 500+ |
| 记忆数 | 5000+ |
| 知识图谱实体 | 200+ |
| 元规则数 | 100+ |

**关键特征**：
- ✅ 直觉性决策
- ✅ 跨领域类比
- ✅ 创新性解决

---

## 🔧 工具集成

### 1. 记忆系统

```python
# 会话记忆 - 记录每次交互
memory.add_session(
    content=task_result,
    memory_type='observation',
    importance=7.0,  # 领域任务提高重要性
    tags=[domain, subtopic]
)

# 反思记忆 - 深度思考
memory.add_memory(
    content=fractal_insight,
    memory_type='reflection',
    importance=9.0
)

# 目标记忆 - 元规则
memory.add_memory(
    content=meta_rule,
    memory_type='goal',
    importance=10.0
)
```

### 2. 知识图谱

```python
# 实体提取
kg.add_entity('concept', '装饰器', {
    'difficulty': '中级',
    'category': '语法特性',
    'related': ['闭包', '元编程']
})

# 关系建立
kg.add_relation('装饰器', '基于', '闭包', confidence=0.9)
kg.add_relation('装饰器', '用于', '函数增强', confidence=0.95)
```

### 3. 基准测试

```bash
# 每周运行
python3 benchmarks/comprehensive_test.py --agent expert-agent

# 追踪指标
- 会话记忆增长率
- 知识图谱扩展速度
- 元规则提取数量
- 任务成功率
```

---

## 📈 评估指标

### 记忆质量

| 指标 | 计算方式 | 目标 |
|------|----------|------|
| 记忆密度 | 记忆数/会话数 | 5-10 条/会话 |
| 反思比例 | 反思记忆/总记忆 | >20% |
| 元规则数 | goal 类型记忆数 | 100+ |

### 知识深度

| 指标 | 计算方式 | 目标 |
|------|----------|------|
| 实体覆盖率 | 实体数/领域概念数 | >80% |
| 关系密度 | 关系数/实体数 | >2 |
| 知识更新率 | 月新增实体/总实体 | >10% |

### 决策质量

| 指标 | 计算方式 | 目标 |
|------|----------|------|
| 任务成功率 | 成功任务/总任务 | >95% |
| 元规则应用率 | 使用元规则的任务/总任务 | >50% |
| 预测准确率 | 正确预测/总预测 | >80% |

---

## ⚠️ 常见陷阱

### 1. 领域漂移

**问题**：开始接受非领域任务

**解决**：
```python
def accept_task(task):
    if not is_domain_related(task):
        log_rejection(task, reason="超出领域范围")
        return False
    return True
```

### 2. 过度泛化

**问题**：元规则太宽泛，失去指导意义

**解决**：
```python
# ❌ 坏规则："总是使用最佳实践"
# ✅ 好规则："I/O 密集型任务使用 async/await"

meta_rule = {
    'condition': 'task_type == "I/O_bound"',
    'action': 'use_async_await',
    'confidence': 0.95,
    'source': 'fractal_analysis_2026-04-11'
}
```

### 3. 记忆过载

**问题**：记忆太多，检索变慢

**解决**：
```python
# 夜间压缩
python3 skills/self-evolution/nightly_cycle.py

# 配置
config = {
    'compress_after_days': 7,
    'keep_high_importance': 7.0,
    'target_compression_rate': 0.49
}
```

---

## 🎯 快速启动模板

```bash
#!/bin/bash
# 创建专家 Agent

AGENT_NAME=$1
DOMAIN=$2

echo "🚀 创建领域专家 Agent: $AGENT_NAME"
echo "📦 领域：$DOMAIN"

# 1. 创建工作区
openclaw agents add $AGENT_NAME --workspace ~/.openclaw/workspace-$AGENT_NAME

# 2. 安装 evo-agents
cd ~/.openclaw/workspace-$AGENT_NAME
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s $AGENT_NAME --force

# 3. 创建领域配置
cat > config/domain.yaml << EOF
agent_name: $AGENT_NAME
domain: $DOMAIN
created_at: $(date -Iseconds)
EOF

# 4. 配置 Cron 任务
openclaw cron add --cron "0 * * * *" \
  --agent $AGENT_NAME \
  --message "python3 skills/self-evolution/hourly_check.py" \
  --name "hourly-learning" \
  --no-deliver --session isolated

openclaw cron add --cron "0 23 * * *" \
  --agent $AGENT_NAME \
  --message "python3 skills/self-evolution/nightly_cycle.py" \
  --name "daily-consolidation" \
  --no-deliver --session isolated

openclaw cron add --cron "0 10 * * 0" \
  --agent $AGENT_NAME \
  --message "python3 skills/self-evolution/fractal_thinking.py --limit 50" \
  --name "weekly-fractal" \
  --no-deliver --session isolated

# 5. 运行基准测试
python3 benchmarks/comprehensive_test.py --agent $AGENT_NAME

echo "✅ 专家 Agent 创建完成！"
echo "📊 初始基准测试报告：benchmarks/report_*.json"
```

---

## 📚 参考资源

- [Generative Agents](https://arxiv.org/abs/2304.03442) - 记忆系统
- [TinkerClaw](https://github.com/globalcaos/tinkerclaw) - 分形思考
- [MemPalace](https://github.com/milla-jovovich/mempalace) - 基准测试
- [evo-agents Benchmarks](benchmarks/README.md) - evo-agents 测试套件

---

_版本：1.0.0 | 2026-04-11_  
_基于 evo-agents v5.0+_
