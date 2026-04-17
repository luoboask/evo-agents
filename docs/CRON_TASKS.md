# Cron 任务及执行脚本

| # | Cron | 任务名 | 执行脚本 | 功能 |
|---|------|--------|----------|------|
| 1 | `*/5 * * * *` | realtime-index | `python3 skills/memory-search/realtime_indexer.py --auto` | 实时索引新会话和记忆 |
| 2 | `*/30 * * * *` | session-scan | `python3 scripts/core/scan_sessions.py --agent $AGENT_NAME` | 扫描 OpenClaw 会话并增量保存 |
| 3 | `0 9 * * *` | daily-review | `python3 skills/memory-search/daily_review.py` | 创建今日记忆文件 + 显示昨日摘要 |
| 4 | `0 9:30 * * *` | daily-compress | `python3 scripts/core/memory_manager.py --daily` | 每日增量记忆压缩 |
| 5 | `0 23 * * *` | nightly-evolution | `python3 skills/self-evolution/nightly_cycle.py` | 夜间进化循环：每日复盘 → 记忆整合 → 上下文清理 → 自动进化 |
| 6 | `0 4 * * *` | active-learning | `python3 skills/self-evolution/active_learning_trigger.py --agent $AGENT_NAME --execute` | 基于触发条件自动执行进化任务 |
| 7 | `0 3 * * 0` | weekly-compress | `python3 scripts/core/memory_manager.py --weekly` | 每周记忆压缩，生成周摘要 |
| 8 | `0 4 1 * *` | monthly-compress | `python3 scripts/core/memory_manager.py --monthly` | 每月记忆压缩，生成月摘要 |
| 9 | `0 5 * * 0` | kg-expansion | `python3 skills/knowledge-graph/auto_expander.py --agent $AGENT_NAME --limit 100` | 自动扩展知识图谱，发现实体关系 |
| 10 | `0 2 * * 0` | weekly-maintenance | `python3 scripts/core/memory_manager.py --cleanup --stats` | 系统清理 + 生成统计报告 |

---

## 脚本详情

### skills/memory-search/realtime_indexer.py
```python
class RealtimeIndexer:
    """实时记忆索引器"""
    def index(self, agent_name, session_file): ...
```

### scripts/core/scan_sessions.py
```python
class SessionScanner:
    """会话扫描器 - 扫描并增量保存会话历史"""
    def scan(self, agent_name, full_scan=False, limit=50): ...
```

### skills/memory-search/daily_review.py
```python
# ⚠️ 脚本不存在
# 功能：创建今日记忆文件，显示昨日摘要
```

### skills/self-evolution/nightly_cycle.py
```python
class NightlyEvolutionCycle:
    """夜间进化循环系统"""
    def run_full_cycle(self):
        1. wind_down()          # 每日复盘
        2. memory_consolidation()  # 记忆整合
        3. cleaning_lady()      # 上下文清理
        4. auto_evolution()     # 自动进化
        5. capacity_check()     # 记忆容量检查 (仅周日)
```

### skills/self-evolution/active_learning_trigger.py
```python
class ActiveLearningTrigger:
    """主动学习触发器"""
    def check_and_trigger(self, agent_name, execute=False): ...
```

### scripts/core/memory_manager.py
```python
# 统一记忆管理器
# 支持模式：--daily (每日压缩), --weekly, --monthly, --cleanup, --stats
```

### skills/knowledge-graph/auto_expander.py
```python
class KnowledgeGraphAutoExpander:
    """知识图谱自动扩展器"""
    def expand(self, agent_name, limit=100): ...
```

---

## 执行时间分布

**每日**: 04:00 主动学习 | 09:00 每日回顾 → 09:30 每日压缩 | 23:00 夜间进化

**周日**: 02:00 系统维护 → 03:00 周压缩 → 05:00 知识图谱扩展

**每月**: 1 号 04:00 月压缩

**高频**: 每 5 分钟 实时索引 | 每 30 分钟 会话扫描
