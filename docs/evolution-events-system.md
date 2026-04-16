# 进化事件记录与策略配置系统

**创建时间**: 2026-04-16  
**版本**: v1.0  
**参考**: EvoMap Evolver GEP 协议

---

## 📦 新增文件

| 文件 | 功能 | 行数 |
|------|------|------|
| `scripts/core/evolution_events.py` | 进化事件记录器 | 240 |
| `scripts/core/evolution_strategy.py` | 策略配置系统 | 130 |
| `scripts/core/test_evolution_system.py` | 集成测试 | 140 |

---

## 🎯 核心功能

### 1. 结构化进化事件记录

**文件格式**: `data/{agent}/evolution_events.jsonl`

**每条记录包含**:
```json
{
  "run_id": "run_6c8575875a0f",
  "intent": "repair",
  "signals": ["log_error", "errsig:xxx"],
  "blast_radius": {"files": 1, "lines": 5},
  "outcome": {"status": "success", "score": 0.85},
  "genes_used": ["gene_gep_repair_from_errors"],
  "meta": {},
  "timestamp": "2026-04-16T02:38:37Z"
}
```

**API 示例**:
```python
from evolution_events import EvolutionEventRecorder

recorder = EvolutionEventRecorder('main-agent')

# 记录事件
run_id = recorder.record(
    intent='repair',
    signals=['log_error', 'errsig:tool_not_found'],
    blast_radius={'files': 1, 'lines': 5},
    outcome={'status': 'success', 'score': 0.85}
)

# 获取最近事件
events = recorder.get_recent_events(10)

# 获取统计
stats = recorder.get_stats()
# {'total': 10, 'success_rate': 0.8, 'avg_files': 1.4, ...}

# 信号分析（用于去重）
analysis = recorder.analyze_signal_frequency()
# {'suppressed_signals': {'log_error'}, 'empty_cycle_ratio': 0.25, ...}
```

---

### 2. 信号去重机制

**问题**: 同一信号反复触发，导致重复处理

**解决方案**: 统计最近 8 个事件的信号频率，抑制出现 3+ 次的信号

```python
analysis = recorder.analyze_signal_frequency()

print(analysis['suppressed_signals'])  # {'log_error', 'errsig'}
print(analysis['signal_freq'])         # {'log_error': 4, 'errsig': 3, ...}
print(analysis['empty_cycle_ratio'])   # 0.25 (25% 空转)
print(analysis['failure_ratio'])       # 0.17 (17% 失败率)
```

**使用建议**:
- 如果 `suppressed_signals` 包含某信号 → 跳过该信号的处理
- 如果 `empty_cycle_ratio > 0.5` → 系统可能饱和，应降低频率
- 如果 `consecutive_failures > 3` → 应进入修复模式

---

### 3. 进化策略配置

**4 种策略**:

| 策略 | 创新% | 优化% | 修复% | 适用场景 |
|------|-------|-------|-------|----------|
| **balanced** (默认) | 50% | 30% | 20% | 日常运行，稳步成长 |
| **innovate** | 80% | 15% | 5% | 系统稳定，快速出新功能 |
| **harden** | 20% | 40% | 40% | 大改动后，聚焦稳固 |
| **repair-only** | 0% | 20% | 80% | 紧急修复模式 |

**配置方式**:
```bash
# 查看当前策略
python3 scripts/core/evolution_strategy.py --show

# 列出所有策略
python3 scripts/core/evolution_strategy.py --list

# 切换策略（环境变量）
export EVOLUTION_STRATEGY=innovate
python3 scripts/core/evolution_strategy.py --show
```

**API 示例**:
```python
from evolution_strategy import get_strategy, get_intent_priority, should_prioritize_intent

# 获取当前策略
strategy = get_strategy()
# {'innovate': 0.5, 'optimize': 0.3, 'repair': 0.2, 'description': '日常运行，稳步成长'}

# 获取意图优先级（用于决策）
priorities = get_intent_priority()
# ['innovate', 'optimize', 'repair']

# 判断是否优先处理某意图
if should_prioritize_intent('innovate'):
    print('创新功能优先处理')
```

---

## 🔗 集成场景

### 场景 1: 根据策略决定进化方向

```python
from evolution_events import EvolutionEventRecorder
from evolution_strategy import get_intent_priority

recorder = EvolutionEventRecorder('main-agent')
priorities = get_intent_priority()

# 检测到的信号
detected_signals = ['log_error', 'perf_bottleneck', 'user_feature_request']

# 根据策略优先级决定处理顺序
for intent in priorities:
    if intent == 'repair' and 'log_error' in detected_signals:
        # 优先处理修复
        handle_repair()
    elif intent == 'optimize' and 'perf_bottleneck' in detected_signals:
        # 其次处理优化
        handle_optimize()
    elif intent == 'innovate' and 'user_feature_request' in detected_signals:
        # 最后处理创新
        handle_innovate()
```

---

### 场景 2: 信号去重避免重复处理

```python
from evolution_events import EvolutionEventRecorder

recorder = EvolutionEventRecorder('main-agent')
analysis = recorder.analyze_signal_frequency()

# 检测新信号
new_signals = detect_signals()

# 过滤掉应抑制的信号
filtered_signals = [
    sig for sig in new_signals 
    if sig.split(':')[0] not in analysis['suppressed_signals']
]

# 只处理未抑制的信号
if filtered_signals:
    process_signals(filtered_signals)
else:
    print('所有信号都被抑制，跳过本次进化')
```

---

### 场景 3: 空转检测与降级

```python
from evolution_events import EvolutionEventRecorder

recorder = EvolutionEventRecorder('main-agent')
analysis = recorder.analyze_signal_frequency()

# 检测空转
if analysis['empty_cycle_ratio'] > 0.5:
    print('⚠️ 空转比例过高，系统可能饱和')
    
    # 自动切换到修复模式
    os.environ['EVOLUTION_STRATEGY'] = 'repair-only'

# 检测连续失败
if analysis['consecutive_failures'] > 3:
    print('⚠️ 连续失败，进入保守模式')
    
    # 降低进化频率
    os.environ['EVOLUTION_INTERVAL'] = '3600'  # 1 小时
```

---

## 📊 统计与监控

### 命令行工具

```bash
# 查看进化事件统计
python3 scripts/core/evolution_events.py --agent main-agent --stats

# 查看最近 10 个事件
python3 scripts/core/evolution_events.py --agent main-agent --recent 10

# 分析信号频率
python3 scripts/core/evolution_events.py --agent main-agent --analyze
```

### 输出示例

```json
{
  "total": 42,
  "by_intent": {"repair": 20, "optimize": 12, "innovate": 10},
  "by_outcome": {"success": 35, "failed": 7},
  "avg_files": 1.8,
  "avg_lines": 12.5,
  "success_rate": 0.83
}
```

---

## 🚀 下一步集成

### 待修改的现有脚本

1. **scan_sessions.py** - 在提取进化事件时调用 `recorder.record()`
2. **nightly_cycle.py** - 在分形思考前调用 `get_intent_priority()`
3. **fractal_thinking.py** - 在生成元规则后记录事件

### 集成示例 (scan_sessions.py)

```python
# 在 scan_sessions.py 中添加
from evolution_events import EvolutionEventRecorder

class SessionScanner:
    def __init__(self, ...):
        self.evolution_recorder = EvolutionEventRecorder(agent_name)
    
    def extract_evolution_events(self, messages):
        # ... 现有的提取逻辑 ...
        
        # 记录事件
        self.evolution_recorder.record(
            intent=event_type.lower(),
            signals=signals,
            blast_radius={'files': 0, 'lines': 0},  # 仅记录，未实际变更
            outcome={'status': 'success', 'score': 1.0}
        )
```

---

## 💡 设计原则

1. **向后兼容**: 不影响现有功能，新增模块独立运行
2. **渐进式采用**: 可以先记录事件，再逐步集成策略
3. **本地优先**: 所有数据存储在本地，不依赖网络
4. **简洁至上**: 保持 Pythonic 风格，避免过度工程

---

## 📝 测试记录

```bash
# 运行集成测试
python3 scripts/core/test_evolution_system.py

# 测试结果
✅ 事件记录：正常
✅ 信号分析：正常（检测到抑制信号）
✅ 策略配置：正常（4 种策略可切换）
✅ 集成场景：正常（根据策略决定优先级）
```

---

_文档生成时间：2026-04-16 11:00_
