# 社会模拟系统 (social-simulation)

> 🏛️ 多 Agent 社会模拟技能，让 Agent 自主对话、协作、发展剧情

---

## 🎯 功能特性

- ✅ **角色扮演** - 商人/学者/艺术家/工人等多种角色
- ✅ **自主对话** - Agent 之间自主发起和进行对话
- ✅ **关系网络** - 动态建立和维护社会关系
- ✅ **资源经济** - 金币、声誉、物品的交易和积累
- ✅ **时间模拟** - 加速时间流逝，观察长期演化
- ✅ **上帝视角** - 观察和记录社会发展，生成叙事

---

## 🚀 快速开始

### 1. 加载技能

在 Agent 的配置文件或代码中加载此技能：

```python
from skills.social_simulation import (
    init_society,
    join_society,
    start_simulation,
    get_society_status,
    generate_narrative
)
```

### 2. 初始化社会

```python
# 初始化社会环境
init_society()
```

### 3. 加入社会

```python
# 当前 Agent 扮演商人角色
join_society("merchant", name="钱老板")

# 或者创建多个 Agent
join_society("scholar", name="知教授")
join_society("artist", name="画先生")
join_society("worker", name="工师傅")
```

### 4. 启动模拟

```python
# 10 倍速，运行 24 小时（社会时间）
await start_simulation(speed=10, duration=24)

# 或者持续运行
await start_simulation(speed=60)
```

### 5. 观察和记录

```python
# 获取社会状态
status = get_society_status()
print(f"第{status['day']}天 {status['hour']}:00")

# 观察特定 Agent
report = observe("merchant_01")
print(report['summary'])

# 生成叙事报告
story = generate_narrative()
print(story)
```

---

## 📁 项目结构

```
social-simulation/
├── SKILL.md                    # 技能文档
├── skill.json                  # 技能元数据
├── social_simulation.py        # 核心实现
├── examples/
│   └── quick_start.py          # 快速开始示例
└── README.md                   # 说明文档
```

---

## 🎭 角色类型

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

---

## ⚙️ 配置

### 社会配置（config/society.yaml）

```yaml
society:
  name: "微型社会实验 #1"
  time:
    start_hour: 8
    speed_multiplier: 10

environment:
  name: "小镇"
  locations:
    - id: "market_square"
      name: "市集广场"
      type: "public"

economy:
  currency: "金币"
  initial_distribution:
    merchant: 1000
    scholar: 300
    artist: 200
    worker: 100
```

### Agent 配置（agents/{agent_id}/config.yaml）

```yaml
name: merchant_01
display_name: "钱老板"
type: social-agent

role:
  type: merchant
  traits: ["精明的", "社交的", "务实的"]
  goals: ["积累财富", "建立商业网络"]
```

---

## 📊 API 参考

### init_society(config_path=None)

初始化社会模拟环境。

### join_society(role, name=None, config=None)

加入社会，扮演特定角色。

**参数:**
- `role` (string): 角色类型 (merchant/scholar/artist/worker)
- `name` (string, optional): 角色名称
- `config` (dict, optional): 自定义配置

### start_simulation(speed=1, duration=None)

启动社会模拟。

**参数:**
- `speed` (int): 时间速度倍率
- `duration` (int, optional): 模拟时长（小时）

### stop_simulation()

停止社会模拟。

### get_society_status() → dict

获取社会当前状态。

**返回:**
```python
{
    "day": 1,
    "hour": 14,
    "agent_count": 4,
    "agents": [...],
    "active_conversations": 2,
    "events_today": 15
}
```

### observe(agent_id=None) → dict

上帝视角观察。

**参数:**
- `agent_id` (string, optional): 观察特定 Agent

### generate_narrative(day=None) → str

生成社会演化叙事。

**参数:**
- `day` (int, optional): 指定天数

### interact_with(agent_id, message=None, action=None)

与特定 Agent 互动。

---

## 🔗 与自进化系统集成

社会模拟系统可以与自进化系统协同工作：

```python
from skills.self_evolution import evolve

# 社会互动自动记录为进化事件
evolve(
    type="SOCIAL_INTERACTION",
    content="与 scholar_01 进行了知识交易",
    metadata={"partner": "scholar_01", "outcome": "success"}
)
```

---

## 📝 使用示例

### 示例 1: 单 Agent 体验

```python
from skills.social_simulation import *

# 初始化并加入
init_society()
join_society("merchant", name="钱老板")

# 启动模拟
await start_simulation(speed=10, duration=24)

# 查看状态
status = get_society_status()
print(f"社会状态：{status}")
```

### 示例 2: 多 Agent 社会

```python
# 创建多个 Agent
roles = ["merchant", "scholar", "artist", "worker"]
for role in roles:
    join_society(role)

# 启动模拟（100 倍速，模拟 1 周）
await start_simulation(speed=100, duration=168)
```

### 示例 3: 上帝视角观察者

```python
# 持续观察
while True:
    status = get_society_status()
    print(f"第{status['day']}天 {status['hour']}:00")
    
    # 每天生成叙事
    if status['hour'] == 22:
        story = generate_narrative()
        print(f"今日故事：{story}")
    
    await asyncio.sleep(60)
```

---

## 🎯 使用场景

1. **社会实验** - 观察不同角色配置下的社会演化
2. **剧情发展** - 让 Agent 自主发展剧情
3. **教育演示** - 展示社会互动和经济学原理
4. **游戏开发** - NPC 行为模拟
5. **研究工具** - 多 Agent 系统研究

---

## ⚠️ 注意事项

- 建议 5-20 个 Agent（过多影响性能）
- 时间加速会增加 API 调用频率
- 定期备份社会状态数据
- 对话生成依赖 LLM，确保模型可用

---

## 📚 相关文档

- [SKILL.md](SKILL.md) - 完整技能文档
- [examples/quick_start.py](examples/quick_start.py) - 快速开始代码

---

_版本：1.0.0 | 更新：2026-03-30_
