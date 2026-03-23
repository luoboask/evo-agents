# HEARTBEAT.md - ai-baby 日常任务

## 每日任务

### 早晨检查
- [ ] 运行 `./start.sh` 查看系统状态
- [ ] 检查 RAG 数据积累（目标：每天 5+ 条）
- [ ] 查看昨日记忆摘要

### 对话中（自动）
- [x] RAG 记录自动开启（无需手动操作）
- [x] 记忆搜索自动记录指标

### 晚上检查
- [ ] 回顾今日对话质量
- [ ] 记录重要事件到记忆

---

## 每周任务

### RAG 质量检查（每周一）
```bash
# 查看上周报告
python3 skills/rag/evaluate.py --report --days 7

# 如果数据足够（10+ 条），运行自动调优
python3 skills/rag/auto_tune.py --report
python3 skills/rag/auto_tune.py --next
```

### 记忆维护（每周日）
- [ ] 回顾本周新增记忆
- [ ] 合并重复内容
- [ ] 更新 MEMORY.md

### 自进化检查（每周日）
```bash
cd skills/self-evolution-5.0
python3 main.py status
python3 main.py fractal --limit 10
```

---

## 数据积累目标

| 阶段 | RAG 数据量 | 目标 |
|------|-----------|------|
| 初期 | 0-10 条 | 验证系统正常 |
| 成长期 | 10-50 条 | 第一次自动调优 |
| 成熟期 | 50+ 条 | 稳定优化 |

**当前状态**: 5 条（初期 → 成长期）

---

## 快速命令

```bash
# 系统状态
./start.sh

# RAG 报告
python3 skills/rag/evaluate.py --report --days 7

# 记忆搜索
python3 skills/memory-search/search_sqlite.py "查询" --semantic

# 自动调优（需要 10+ 条）
python3 skills/rag/auto_tune.py --report
```
