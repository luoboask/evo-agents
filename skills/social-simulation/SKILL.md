---
name: social-simulation
description: 多 Agent 社会模拟系统，让 Agent 自主对话、协作、发展剧情
homepage: https://github.com/luoboask/evo-agents
metadata:
  emoji: "🏛️"
  category: simulation
  version: "1.0.0"
  updated_at: "2026-03-30"
---

# 社会模拟系统 v1.0

多 Agent 社会模拟技能，支持创建角色、自主对话、关系网络、资源经济的完整社会生态系统。

## 核心架构

```
┌─────────────────────────────────────────────────────┐
│              社会模拟系统 v1.0                        │
├─────────────────────────────────────────────────────┤
│  角色系统 (Role System)                              │
│  - 角色定义（商人/学者/艺术家/工人等）               │
│  - 人格模板（性格/目标/说话风格）                    │
│  - 关系网络（ Agent 间的关系和强度）                  │
├─────────────────────────────────────────────────────┤
│  对话系统 (Dialogue System)                          │
│  - 自主对话生成（基于角色和情境）                    │
│  - 对话匹配（ proximity/goal/random）                │
│  - 对话历史追踪                                      │
├─────────────────────────────────────────────────────┤
│  环境系统 (Environment System)                       │
│  - 空间管理（市集/酒馆/工坊等）                      │
│  - 时间系统（加速/暂停/回放）                        │
│  - 资源经济（金币/声誉/物品）                        │
├─────────────────────────────────────────────────────┤
│  上帝视角 (God View)                                 │
│  - 社会状态观察                                      │
│  - 叙事生成                                          │
│  - 干预控制（可选）                                  │
└─────────────────────────────────────────────────────┘
```

## 功能

- **角色扮演** - 每个 Agent 拥有独特角色和人格
- **自主对话** - Agent 之间自主发起和进行对话
- **关系网络** - 动态建立和维护社会关系
- **资源经济** - 金币、声誉、物品的交易和积累
- **时间模拟** - 加速时间流逝，观察长期演化
- **上帝视角** - 观察和记录社会发展，生成叙事

## 可用工具

### init_society(config_path=None)

初始化社会模拟环境。

**参数：**
- `config_path` (string, optional): 社会配置文件路径，默认使用 `config/society.yaml`

**示例：**
```python
init_society()  # 使用默认配置
init_society("config/my-society.yaml")  # 自定义配置
```

### join_society(role, name=None, config=None)

让当前 Agent 加入社会，扮演特定角色。

**参数：**
- `role` (string, required): 角色类型（merchant/scholar/artist/worker）
- `name` (string, optional): 角色名称，默认根据角色生成
- `config` (dict, optional): 角色配置覆盖

**示例：**
```python
join_society("merchant", name="钱老板")
join_society("scholar", name="知教授")
join_society("artist", name="画先生")
```

### start_simulation(speed=1, duration=None)

启动社会模拟。

**参数：**
- `speed` (integer, default=1): 时间速度倍率（1 现实秒 = speed 社会分钟）
- `duration` (integer, optional): 模拟时长（社会小时），None=持续运行

**示例：**
```python
start_simulation(speed=10)  # 10 倍速
start_simulation(speed=60, duration=24)  # 60 倍速，模拟 1 天
```

### stop_simulation()

停止社会模拟。

**示例：**
```python
stop_simulation()
```

### get_society_status()

获取社会当前状态。

**返回：**
- 当前时间（天数/小时）
- Agent 列表和状态
- 活跃对话数
- 资源分布

**示例：**
```python
status = get_society_status()
print(f"第{status['day']}天 {status['hour']}:00")
print(f"人口：{status['agent_count']}")
```

### observe(agent_id=None)

上帝视角观察。

**参数：**
- `agent_id` (string, optional): 观察特定 Agent，None=观察整体

**返回：**
- 观察报告（状态/行为/关系）

**示例：**
```python
report = observe()  # 观察整体
report = observe("merchant_01")  # 观察特定 Agent
```

### generate_narrative(day=None)

生成社会演化叙事。

**参数：**
- `day` (integer, optional): 指定天数，None=最新一天

**返回：**
- 故事性叙述文本

**示例：**
```python
story = generate_narrative()
story = generate_narrative(day=5)
```

### interact_with(agent_id, message=None, action=None)

与特定 Agent 互动。

**参数：**
- `agent_id` (string, required): 目标 Agent ID
- `message` (string, optional): 对话消息
- `action` (string, optional): 行动类型（trade/cooperate/compete）

**示例：**
```python
interact_with("scholar_01", message="听说你有新研究？")
interact_with("merchant_01", action="trade")
```

## 配置

### 社会配置（config/society.yaml）

```yaml
# 社会基本信息
society:
  name: "微型社会实验 #1"
  start_date: "2026-03-30"
  
  # 时间配置
  time:
    start_hour: 8
    end_hour: 22
    speed_multiplier: 10
  
  # 模拟参数
  simulation:
    auto_dialogue: true
    max_concurrent_conv: 3
    dialogue_trigger_prob: 0.3

# 环境配置
environment:
  name: "小镇"
  locations:
    - id: "market_square"
      name: "市集广场"
      type: "public"
      capacity: 10
    - id: "tavern"
      name: "酒馆"
      type: "social"
      capacity: 5

# 经济配置
economy:
  currency: "金币"
  initial_distribution:
    merchant: 1000
    scholar: 300
    artist: 200
    worker: 100
```

### 角色配置（agents/{agent_id}/config.yaml）

```yaml
name: merchant_01
display_name: "钱老板"
type: social-agent

role:
  type: merchant
  traits: ["精明的", "社交的", "务实的"]
  goals: ["积累财富", "建立商业网络"]
  speech_style: "直接、谈利益、喜欢讨价还价"

initial_state:
  location: "market_square"
  resources:
    gold: 1000
    reputation: 50

relationships:
  - agent: scholar_01
    type: "business_partner"
    strength: 0.6
```

## 使用场景

### 1. 单 Agent 加入现有社会

```python
# 当前 Agent 作为新角色加入
join_society("merchant", name="新商人")
start_simulation(speed=10)
```

### 2. 创建多 Agent 社会

```python
# 初始化社会
init_society()

# 创建多个 Agent（通过配置或 API）
# 每个 Agent 加载此 skill 后自动成为社会成员

# 启动模拟
start_simulation(speed=60, duration=168)  # 模拟 1 周
```

### 3. 上帝视角观察

```python
# 定期观察社会状态
status = get_society_status()
print(f"社会状态：{status}")

# 生成叙事报告
story = generate_narrative()
print(f"今日故事：{story}")
```

### 4. 干预社会演化

```python
# 与特定 Agent 互动
interact_with("scholar_01", message="我想投资你的研究")

# 观察互动结果
report = observe("scholar_01")
```

## 角色类型

### 商人 (merchant)
- **性格**: 精明、社交、务实
- **目标**: 积累财富、建立商业网络
- **能力**: 交易、谈判、市场分析

### 学者 (scholar)
- **性格**: 好奇、理性、孤僻
- **目标**: 追求真理、发表研究
- **能力**: 研究、教学、写作

### 艺术家 (artist)
- **性格**: 感性、创意、情绪化
- **目标**: 创作杰作、获得认可
- **能力**: 创作、表演、鉴赏

### 工人 (worker)
- **性格**: 勤劳、实际、团结
- **目标**: 稳定收入、提升技能
- **能力**: 建造、维修、生产

## 对话触发机制

| 触发类型 | 概率 | 描述 |
|---------|------|------|
| proximity | 0.3 | 在同一空间相遇 |
| shared_goal | 0.6 | 有共同目标/话题 |
| relationship | 0.5 | 已有关系网络 |
| random | 0.1 | 随机相遇 |

## 数据存储

```
data/
├── social/
│   ├── society_state.json    # 社会整体状态
│   ├── relationships.json    # 关系网络
│   ├── events_log.json       # 事件日志
│   └── reports/              # 生成的叙事报告
└── <agent>/
    └── memory/               # Agent 个人记忆
```

## 与自进化系统集成

社会模拟系统可以与自进化系统协同工作：

```python
# 社会互动自动记录为进化事件
evolve(
    type="SOCIAL_INTERACTION",
    content="与 scholar_01 进行了知识交易",
    metadata={"partner": "scholar_01", "outcome": "success"}
)

# 分形思考分析社会模式
fractal(limit=50)  # 分析最近 50 条社会互动记忆

# 夜间循环整合社会经验
nightly()  # 回顾当天的社会互动
```

## 最佳实践

- **角色一致性** - 保持角色性格和目标的连贯性
- **适度干预** - 让社会自主演化，避免过度干预
- **定期观察** - 使用上帝视角定期记录社会状态
- **叙事生成** - 定期生成叙事报告，捕捉涌现行为
- **数据备份** - 定期备份社会状态数据

## 性能建议

- **Agent 数量**: 建议 5-20 个 Agent（过多影响性能）
- **时间速度**: 建议 10-60 倍速（过快可能错过细节）
- **对话并发**: 限制最大并发对话数（默认 3）
- **日志级别**: 生产环境使用 INFO，调试使用 DEBUG

## 依赖

- **Python 3.10+** - 运行环境
- **SQLite3** - 数据存储
- **PyYAML** - 配置解析
- **自进化系统** - 记忆和进化功能（可选，强烈推荐）

## 注意事项

- 社会模拟需要足够的 Agent 数量才能产生涌现行为（建议 5+）
- 对话生成依赖 LLM，确保模型可用
- 时间加速会增加 API 调用频率
- 定期清理过期事件日志，避免数据膨胀

## 示例脚本

### 快速开始

```python
#!/usr/bin/env python3
"""快速启动社会模拟"""

from skills.social_simulation import (
    init_society,
    join_society,
    start_simulation,
    get_society_status,
    generate_narrative
)

# 初始化社会
init_society()

# 加入社会（扮演商人）
join_society("merchant", name="钱老板")

# 启动模拟（10 倍速，运行 1 天）
start_simulation(speed=10, duration=24)

# 查看状态
status = get_society_status()
print(f"社会状态：{status}")

# 生成叙事
story = generate_narrative()
print(f"今日故事：{story}")
```

### 上帝视角观察者

```python
#!/usr/bin/env python3
"""上帝视角观察者 - 只观察不干预"""

from skills.social_simulation import (
    init_society,
    observe,
    generate_narrative,
    get_society_status
)

# 初始化（作为观察者）
init_society()

# 持续观察
import time
while True:
    # 获取状态
    status = get_society_status()
    print(f"\n📊 第{status['day']}天 {status['hour']}:00")
    print(f"   人口：{status['agent_count']}")
    print(f"   对话：{status['active_conversations']}")
    
    # 观察整体
    report = observe()
    print(f"   观察：{report['summary']}")
    
    # 每天生成叙事
    if status['hour'] == 22:
        story = generate_narrative()
        print(f"\n📖 今日故事:\n{story}")
    
    time.sleep(60)  # 每分钟检查一次
```

---

_版本：1.0.0 | 更新：2026-03-30_
