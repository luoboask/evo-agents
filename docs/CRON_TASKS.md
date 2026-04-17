# Cron 任务配置文档

**最后更新**: 2026-04-17  
**来源**: `install.sh`  
**Agent**: evo-agents

---

## 📊 总览

| 序号 | 任务名称 | 频率 | 脚本 | 状态 |
|------|----------|------|------|------|
| 1 | 实时索引 | 每 5 分钟 | `realtime_indexer.py` | ✅ |
| 2 | 会话扫描 | 每 30 分钟 | `scan_sessions.py` | ✅ |
| 3 | 每日回顾 | 每天 09:00 | `daily_review.py` | ⚠️ 需创建 |
| 4 | 夜间进化 | 每天 23:00 | `nightly_cycle.py` | ✅ |
| 5 | 主动学习触发 | 每天 04:00 | `active_learning_trigger.py` | ✅ |
| 6 | 周记忆压缩 | 每周日 03:00 | `memory_manager.py` | ✅ |
| 7 | 月记忆压缩 | 每月 1 号 04:00 | `memory_manager.py` | ✅ |
| 8 | 知识图谱扩展 | 每周日 05:00 | `auto_expander.py` | ✅ |
| 9 | 系统维护 | 每周日 02:00 | `memory_manager.py` | ✅ |

---

## 📋 详细配置

### 任务 1: 实时索引 (Realtime Indexer)

```bash
Cron:   */5 * * * *
Name:   $AGENT_NAME-realtime-index
Command: python3 skills/memory-search/realtime_indexer.py --auto
```

**功能**: 实时索引新会话和记忆到搜索引擎

**参数**:
- `--auto`: 自动模式，无需交互

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`skills/memory-search/realtime_indexer.py`
- 主函数：`main()`
- 用法：`python3 realtime_indexer.py <agent_name> <session_file.jsonl>`

---

### 任务 2: 会话扫描 (Session Scan)

```bash
Cron:   */30 * * * *
Name:   session-scan-$AGENT_NAME
Command: python3 scripts/core/scan_sessions.py --agent $AGENT_NAME
```

**功能**: 扫描 OpenClaw 会话，增量保存到数据库

**参数**:
- `--agent $AGENT_NAME`: 指定 Agent 名称

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`scripts/core/scan_sessions.py`
- 主函数：`main()`
- 支持参数：`--all-agents`, `--full-scan`, `--limit`

---

### 任务 3: 每日回顾 (Daily Review)

```bash
Cron:   0 9 * * *
Name:   daily-review-$AGENT_NAME
Command: python3 skills/memory-search/daily_review.py
```

**功能**: 创建今日记忆文件，显示昨日摘要

**参数**: 无

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`skills/memory-search/daily_review.py`
- ⚠️ **状态**: 文件不存在，需要创建

---

### 任务 4: 夜间进化 (Nightly Evolution)

```bash
Cron:   0 23 * * *
Name:   nightly-evolution-$AGENT_NAME
Command: python3 skills/self-evolution/nightly_cycle.py
```

**功能**: 完整的夜间进化循环

**参数**: 无

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`skills/self-evolution/nightly_cycle.py`
- 类：`NightlyEvolutionCycle`

**执行流程**:
1. 🍷 **Wind Down** - 每日复盘
2. 😴 **Memory Consolidation** - 记忆整合
3. 🧹 **Cleaning Lady** - 上下文清理
4. 🔍 **Auto-Evolution** - 自动进化
5. 📊 **Memory Capacity Check** - 记忆容量检查（仅周日）

---

### 任务 5: 主动学习触发 (Active Learning Trigger)

```bash
Cron:   0 4 * * *
Name:   $AGENT_NAME-active-learning
Command: python3 skills/self-evolution/active_learning_trigger.py --agent $AGENT_NAME --execute
```

**功能**: 基于触发条件自动执行进化任务

**参数**:
- `--agent $AGENT_NAME`: Agent 名称
- `--execute`: 执行触发的任务

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`skills/self-evolution/active_learning_trigger.py`
- 类：`ActiveLearningTrigger`
- 主函数：`main()`
- 支持参数：`--check-only`, `--simulate`

---

### 任务 6: 周记忆压缩 (Weekly Memory Compress)

```bash
Cron:   0 3 * * 0
Name:   weekly-compress-$AGENT_NAME
Command: python3 scripts/core/memory_manager.py --weekly
```

**功能**: 每周记忆压缩，生成周摘要

**参数**:
- `--weekly`: 周模式

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`scripts/core/memory_manager.py`
- 主函数：`main()`
- 支持模式：`--daily`, `--weekly`, `--monthly`, `--cleanup`, `--stats`

---

### 任务 7: 月记忆压缩 (Monthly Memory Compress)

```bash
Cron:   0 4 1 * *
Name:   monthly-compress-$AGENT_NAME
Command: python3 scripts/core/memory_manager.py --monthly
```

**功能**: 每月记忆压缩，生成月摘要，深度归档

**参数**:
- `--monthly`: 月模式

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`scripts/core/memory_manager.py`
- 同任务 6，使用 `--monthly` 参数

---

### 任务 8: 知识图谱扩展 (Knowledge Graph Expansion)

```bash
Cron:   0 5 * * 0
Name:   $AGENT_NAME-kg-expansion
Command: python3 skills/knowledge-graph/auto_expander.py --agent $AGENT_NAME --limit 100
```

**功能**: 自动扩展知识图谱，发现实体关系，建立新连接

**参数**:
- `--agent $AGENT_NAME`: Agent 名称
- `--limit 100`: 每次最多处理 100 个实体

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`skills/knowledge-graph/auto_expander.py`
- 类：`KnowledgeGraphAutoExpander`
- 主函数：`main()`
- 支持模式：`--manual`, `--auto`

---

### 任务 9: 系统维护 (Weekly Maintenance)

```bash
Cron:   0 2 * * 0
Name:   weekly-maintenance-$AGENT_NAME
Command: python3 scripts/core/memory_manager.py --cleanup --stats
```

**功能**: 系统清理和统计，删除过期数据，生成健康报告

**参数**:
- `--cleanup`: 清理模式
- `--stats`: 生成统计报告

**配置**:
- `--no-deliver`: 不发送通知
- `--session isolated`: 隔离会话执行

**脚本详情**:
- 路径：`scripts/core/memory_manager.py`
- 同任务 6，使用 `--cleanup --stats` 参数

---

## 📅 执行时间分布

### 每日任务
| 时间 | 任务 |
|------|------|
| 04:00 | 主动学习触发 |
| 09:00 | 每日回顾 |
| 23:00 | 夜间进化 |

### 周日任务（错峰执行）
| 时间 | 任务 |
|------|------|
| 02:00 | 系统维护 |
| 03:00 | 周记忆压缩 |
| 05:00 | 知识图谱扩展 |

### 每月任务
| 时间 | 任务 |
|------|------|
| 1 号 04:00 | 月记忆压缩 |

### 高频任务
| 频率 | 任务 |
|------|------|
| 每 5 分钟 | 实时索引 |
| 每 30 分钟 | 会话扫描 |

---

## 🔧 共同配置

所有任务均使用以下配置：

```bash
--agent $AGENT_NAME      # 绑定到当前 Agent
--no-deliver             # 不发送通知
--session isolated       # 隔离会话执行
```

---

## ⚠️ 注意事项

1. **每日回顾脚本缺失**: `skills/memory-search/daily_review.py` 不存在，需要创建或从其他仓库同步

2. **周日任务错峰**: 系统维护 (02:00) → 周记忆压缩 (03:00) → 知识图谱扩展 (05:00)，避免资源竞争

3. **夜间进化包含周日特殊任务**: Memory Capacity Check 仅在周日执行

---

## 📝 安装脚本位置

- 文件：`install.sh`
- 配置段落：第 698-800 行（中文安装流程）
- 配置段落：第 845-950 行（英文安装流程）

---

## 🔄 管理命令

### 查看任务
```bash
openclaw cron list --json | jq -r '.[] | select(.agentId | contains("evo-agents"))'
```

### 删除任务
```bash
openclaw cron remove <job-id>
```

### 手动触发
```bash
openclaw cron run <job-id>
```

### 查看执行历史
```bash
openclaw cron runs <job-id>
```
