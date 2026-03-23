# HEARTBEAT.md - ai-baby 日常任务

## RAG 质量检查（每周一次）
每周回顾检索质量，优化配置：
```bash
python3 skills/rag/evaluate.py --report --days 7
python3 skills/rag/auto_tune.py --report
```

## 记忆维护（每周）
- 回顾本周新增记忆
- 合并重复内容
- 更新长期记忆

## 自进化检查
- 检查 self-evolution-5.0 日志
- 确认夜间任务完成
