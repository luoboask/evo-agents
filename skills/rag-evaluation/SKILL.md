---
name: rag_evaluation
description: RAG 检索质量评估与优化技能
homepage: https://github.com/ai-baby/workspace-ai-baby
metadata:
  emoji: "📊"
  category: evaluation
  version: "1.0.0"
  updated_at: "2026-03-23"
---

# RAG 评估技能

RAG（Retrieval-Augmented Generation）评估技能提供检索质量监控、评估和优化功能。

## 功能

- **检索评估** - 记录和分析每次检索的质量
- **自动调优** - 基于历史数据推荐最优配置
- **报告生成** - 生成详细的评估报告
- **实时监控** - 跟踪检索性能指标

## 可用工具

### rag_report(days=7)

生成 RAG 评估报告。

**参数：**
- `days` (integer, default=7): 报告天数

**返回：**
- 总查询数
- 延迟统计（平均、中位数、范围）
- 反馈统计（正面、中性、负面）
- 相似度统计
- 当前配置

**示例：**
```
rag_report(days=7)
```

### rag_auto_tune(min_samples=10)

分析 RAG 配置并推荐最优方案。

**参数：**
- `min_samples` (integer, default=10): 最小样本数

**返回：**
- 测试的配置数量
- 推荐的最优配置
- 各配置的表现对比

**示例：**
```
rag_auto_tune(min_samples=10)
```

### rag_record(query, retrieved_count, latency_ms, feedback=null, similarity_score=null)

记录一次检索的评估数据。

**参数：**
- `query` (string, required): 检索查询
- `retrieved_count` (integer, required): 检索结果数
- `latency_ms` (number, required): 延迟（毫秒）
- `feedback` (string, optional): 用户反馈 (positive/neutral/negative)
- `similarity_score` (number, optional): 最高相似度分数

**示例：**
```
rag_record(query="RAG 优化", retrieved_count=5, latency_ms=95.0, feedback="positive")
```

## 评估指标

| 指标 | 说明 | 优秀 | 良好 | 需改进 |
|------|------|------|------|--------|
| **延迟** | 检索响应时间 | <50ms | 50-150ms | >150ms |
| **正面反馈率** | 用户满意度 | >70% | 50-70% | <50% |
| **检索使用率** | 结果使用比例 | >80% | 50-80% | <50% |
| **平均相似度** | 语义相似度 | >0.8 | 0.6-0.8 | <0.6 |

## 数据存储

评估数据存储在：
```
~/.openclaw/workspace-ai-baby-config/logs/evaluations.jsonl
```

## 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "rag-evaluation": {
        "enabled": true,
        "env": {
          "RAG_LOG_PATH": "~/.openclaw/workspace-ai-baby-config/logs/evaluations.jsonl",
          "AUTO_RECORD": "true"
        }
      }
    }
  }
}
```

## 使用场景

1. **性能监控** - 定期检查 RAG 系统性能
2. **配置优化** - 自动调优找到最优配置
3. **问题诊断** - 分析检索质量问题
4. **趋势分析** - 跟踪性能变化趋势

## 最佳实践

- **持续记录** - 每次检索都记录评估数据
- **定期回顾** - 每周生成评估报告
- **小步优化** - 每次只调整一个配置参数
- **用户优先** - 用户反馈胜过指标

## 注意事项

- 至少需要 10 条记录才能进行自动调优
- 建议积累 50+ 条记录后再做重大配置调整
- 评估数据包含敏感信息，注意保护隐私
