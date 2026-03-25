---
name: rag
description: RAG 评估系统，记录、分析和优化检索增强生成性能
homepage: https://github.com/luoboask/evo-agents
metadata:
  emoji: "📊"
  category: evaluation
  version: "1.0.0"
  updated_at: "2026-03-24"
---

# RAG 评估技能

RAG（Retrieval-Augmented Generation）评估系统，用于记录、分析和优化检索增强生成性能。

## 功能

- **自动记录** - 记录每次检索的指标（延迟、检索数量、相似度分数）
- **性能分析** - 分析 RAG 系统性能趋势
- **自动调优** - 基于历史数据推荐最优配置（Top-K、相似度阈值等）
- **可视化报告** - 生成 HTML 评估报告

## 可用工具

### evaluate(agent=null, days=7, report=false)

评估 RAG 系统性能。

**参数：**
- `agent` (string, optional): Agent 名称（默认从环境变量获取）
- `days` (integer, default=7): 分析最近 N 天的数据
- `report` (boolean, default=false): 是否生成 HTML 报告

**示例：**
```
evaluate(days=7)
evaluate(days=30, report=true)
```

### auto_tune(agent=null)

自动调优 RAG 配置。

**参数：**
- `agent` (string, optional): Agent 名称

**返回：**
- 推荐的最优配置（Top-K、相似度阈值、Chunk 大小）
- 综合得分和正面反馈率

**示例：**
```
auto_tune()
```

### get_metrics(agent=null, days=7)

获取 RAG 性能指标。

**参数：**
- `agent` (string, optional): Agent 名称
- `days` (integer, default=7): 最近 N 天

**返回：**
- 平均延迟、平均检索数量、平均相似度分数
- 总评估次数

**示例：**
```
get_metrics(days=7)
```

## 配置

在 `config.json` 中配置：

```json
{
  "top_k": 5,
  "similarity_threshold": 0.7,
  "chunk_size": 512,
  "max_history": 100
}
```

## 数据存储

评估记录存储在：
```
skills/rag/logs/evaluations.jsonl
```

每条记录包含：
- 时间戳
- 查询内容
- 检索结果数量
- 相似度分数
- 延迟（ms）
- 配置参数（Top-K、阈值等）
- Token 消耗

## 使用场景

1. **性能监控** - 定期检查 RAG 系统健康状况
2. **配置优化** - 基于数据调整检索参数
3. **问题诊断** - 分析检索失败或低质量结果
4. **趋势分析** - 观察系统性能随时间变化

## 最佳实践

- **积累足够数据** - 建议至少 20+ 条评估记录进入成熟期
- **定期生成报告** - 每周一次 HTML 报告
- **关注负面反馈** - 相似度分数低于阈值时检查检索质量
- **结合语义搜索** - 使用 Ollama Embedding 提升检索质量

## 依赖

- **Memory Hub** - 共享记忆库（必需）
- **SQLite3** - 数据库（必需）
- **Ollama** - 语义搜索（可选）

## 注意事项

- 评估记录会自动追加，不会覆盖历史数据
- 生成 HTML 报告需要足够的评估数据
- 自动调优建议基于历史表现，实际效果需验证

---

_版本：1.0.0 | 更新：2026-03-24_
