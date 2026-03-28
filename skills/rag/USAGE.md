# RAG 评估系统使用指南

## 快速开始

### 1. 记录检索
在记忆搜索前后调用记录器：

```python
from skills.rag.recorder import start_recording, finish_recording

# 开始记录
start_recording("用户的问题")

# 执行记忆搜索...
results = search_memory("用户的问题")

# 完成记录
finish_recording(
    retrieved_count=len(results),
    similarity_score=results[0].score if results else None,
    feedback=None,  # 可选：positive/negative/neutral
    top_k=5
)
```

### 2. 查看报告
```bash
# 查看本周报告
python3 skills/rag/evaluate.py --report --days 7

# 查看本月报告
python3 skills/rag/evaluate.py --report --days 30
```

### 3. 自动调优
```bash
# 生成调优报告
python3 skills/rag/auto_tune.py --report

# 建议下一个实验配置
python3 skills/rag/auto_tune.py --next
```

---

## 集成到对话流程

### 在 ai-baby 主对话中

每次用户提问时：

```python
# 1. 开始记录
start_recording(user_query)

# 2. 执行检索
memories = search_memories(user_query, top_k=5)

# 3. 生成回复（使用检索到的记忆）
response = generate_response(user_query, memories)

# 4. 完成记录
finish_recording(
    retrieved_count=len(memories),
    similarity_score=memories[0].similarity if memories else None,
    used_in_response=len(memories) > 0
)

# 5. 发送回复
send_response(response)
```

### 收集用户反馈

隐式反馈（推荐）：
- 用户继续追问 → positive
- 用户切换话题 → neutral
- 用户表达不满 → negative

显式反馈（如果用户直接评价）：
```python
record_feedback(query="用户的问题", feedback="positive")
```

---

## 配置说明

### config.json 参数

```json
{
  "top_k_options": [3, 5, 10],        // 要测试的 Top-K 值
  "similarity_thresholds": [0.6, 0.7, 0.8],  // 相似度阈值
  "chunk_sizes": [256, 512, 1024],    // Chunk 大小
  "weights": {
    "accuracy": 0.6,   // 准确率权重
    "latency": 0.3,    // 延迟权重
    "cost": 0.1        // 成本权重
  },
  "current_config": {
    "top_k": 5,
    "similarity_threshold": 0.7,
    "chunk_size": 512
  }
}
```

### 调整权重

如果你的场景更注重某一方面，调整 weights：

**注重准确率：**
```json
"weights": {"accuracy": 0.8, "latency": 0.15, "cost": 0.05}
```

**注重速度：**
```json
"weights": {"accuracy": 0.4, "latency": 0.5, "cost": 0.1}
```

---

## 实验策略

### 阶段 1：数据收集（1-2 周）
- 使用默认配置
- 记录所有检索
- 不主动改变参数

### 阶段 2：配置对比（2-4 周）
- 每周切换一次配置
- 对比不同 Top-K 和阈值的表现
- 记录每种配置的指标

### 阶段 3：自动调优（长期）
- 运行 `auto_tune.py --report`
- 应用推荐配置
- 持续监控和改进

---

## 指标解读

### 延迟 (Latency)
- **< 50ms**: 优秀
- **50-150ms**: 良好
- **150-300ms**: 可接受
- **> 300ms**: 需要优化

### 正面反馈率 (Positive Rate)
- **> 70%**: 优秀
- **50-70%**: 良好
- **30-50%**: 需要改进
- **< 30%**: 严重问题

### 检索使用率 (Usage Rate)
- **> 80%**: 检索很常用
- **50-80%**: 正常使用
- **< 50%**: 可能检索策略有问题

---

## 常见问题

### Q: 数据量多少才够？
A: 至少 10 条记录才能做有意义的对比，建议积累 50+ 条。

### Q: 多久运行一次调优？
A: 每周一次报告，每月一次配置调整。

### Q: 如何判断检索质量？
A: 综合看三个指标：
1. 用户反馈（最重要）
2. 检索结果是否用于回复
3. 相似度分数

### Q: 要不要记录所有查询？
A: 是的，包括没有检索到结果的查询。这有助于发现知识盲区。

---

## 最佳实践

1. **持续记录**：不要中断，数据越多越准确
2. **定期回顾**：每周看报告，发现趋势
3. **小步迭代**：每次只改一个参数
4. **用户优先**：指标是参考，用户满意度是核心
5. **文档化**：记录每次配置变更的原因和结果

---

## 下一步

1. ✅ 创建评估框架（已完成）
2. ✅ 创建自动调优（已完成）
3. ⏳ 集成到记忆搜索流程
4. ⏳ 积累数据（1-2 周）
5. ⏳ 第一次配置优化

有任何问题，查看 `skills/rag/README.md` 或运行 `--help`。
