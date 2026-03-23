---
name: self_evolution
description: 自进化系统，分形思考和夜间循环
homepage: https://github.com/ai-baby/workspace-ai-baby
metadata:
  emoji: "🧬"
  category: evolution
  version: "1.0.0"
  updated_at: "2026-03-23"
---

# 自进化技能

自进化系统提供分形思考、夜间循环和进化事件记录功能，实现 AI 助手的持续自我改进。

## 功能

- **分形思考** - 4 层自动分析（Solve → Pattern → Correction → Meta-Rule）
- **夜间循环** - 4 个自动化夜间任务
- **记忆流管理** - 观察/反思/目标/知识四类记忆
- **进化记录** - 记录真实的进化事件

## 可用工具

### run_fractal_analysis(limit=10)

运行分形思考分析。

**参数：**
- `limit` (integer, default=10): 分析的事件数量

**分形思考 4 层：**
- **Level 0: Solve** - 问题是什么？如何解决的？
- **Level 1: Pattern** - 是孤立事件还是重复模式？
- **Level 2: Correction** - 什么规则导致了问题？如何修正？
- **Level 3: Meta-Rule** - 如何防止类似问题再发生？

**返回：**
- 识别的模式
- 生成的洞察
- 建议的改进

**示例：**
```
run_fractal_analysis(limit=10)
```

### run_nightly_cycle(tasks=[])

运行夜间进化循环。

**参数：**
- `tasks` (array, optional): 执行的任务列表

**夜间循环 4 任务：**
- 🍷 **Wind Down** - 每日复盘，生成洞察
- 😴 **Memory Consolidation** - 记忆整合（49% 压缩目标）
- 🧹 **Cleaning Lady** - 上下文清理
- 🔍 **Auto-Evolution** - 扫描改进机会

**示例：**
```
run_nightly_cycle(tasks=["wind_down", "memory_consolidation"])
```

### record_evolution(event_type, content, metadata=null)

记录进化事件。

**参数：**
- `event_type` (string, required): 事件类型
  - `BUG_FIX` - Bug 修复
  - `FEATURE_ADDED` - 功能新增
  - `CODE_IMPROVED` - 代码优化
  - `KNOWLEDGE_GAINED` - 知识获取
  - `EVOLUTION_CHECK` - 进化检查
- `content` (string, required): 事件内容
- `metadata` (object, optional): 元数据

**示例：**
```
record_evolution(event_type="KNOWLEDGE_GAINED", content="学习了 MCP 协议")
```

### get_evolution_stats()

获取进化统计信息。

**返回：**
- 总事件数
- 按类型分布
- 最近事件

**示例：**
```
get_evolution_stats()
```

## 记忆类型

- **Observation** - 观察记忆（日常经历）
- **Reflection** - 反思记忆（从观察抽象）
- **Knowledge** - 知识记忆（结构化知识）
- **Goal** - 目标记忆（待办事项）

## 数据存储

进化数据存储在：
```
~/.openclaw/workspace-ai-baby-config/data/self-evolution/
├── evolution.db          # 进化事件数据库
├── memory_stream.db      # 记忆流数据库
└── nightly_logs/         # 夜间循环日志
```

## 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "self-evolution": {
        "enabled": true,
        "env": {
          "NIGHTLY_CYCLE_ENABLED": "true",
          "FRACTAL_ANALYSIS_ENABLED": "true"
        }
      }
    }
  }
}
```

## 使用场景

1. **日常反思** - 每天运行分形思考
2. **夜间整理** - 自动运行夜间循环
3. **知识沉淀** - 将经验转化为知识
4. **持续改进** - 记录进化事件

## 最佳实践

- **每日反思** - 每天至少运行一次分形思考
- **夜间循环** - 建议在低峰期运行
- **及时记录** - 重要事件立即记录
- **定期回顾** - 每周回顾进化历史

## 注意事项

- 夜间循环可能耗时较长，建议在空闲时运行
- 分形思考需要足够的历史数据才能识别模式
- 建议定期备份进化数据库
