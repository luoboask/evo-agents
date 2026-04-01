# 技能使用规则

_何时使用什么技能？_

---

## 快速参考

| 场景 | 使用技能 |
|------|---------|
| 用户提到"之前"、"记得"、"上次" | `memory-search` |
| 用户问实时信息（新闻、天气、价格） | `web-knowledge` |
| 完成重要任务后 | `self-evolution` (evolve) |
| 学到新知识后 | `self-evolution` (KNOWLEDGE_GAINED) |
| 收到用户反馈后 | `self-evolution` (FEEDBACK_RECEIVED) |
| 使用记忆搜索后 | `rag` (记录评估) |
| 每天结束时 | `self-evolution` (nightly) |
| 普通对话 | 无需特殊技能 |

---

## 记忆相关

### memory-search
**何时用：**
- 用户提到历史对话
- 用户说"记住这个"
- 需要上下文回答问题

**何时不用：**
- 日常闲聊
- 简单事实查询

### rag
**何时用：**
- 使用记忆搜索后（记录检索质量）
- 每周例行检查（生成报告）
- 用户反馈检索不准时

---

## 自进化

### self-evolution
**何时用：**
- 完成任务 → `evolve(type="TASK_COMPLETED")`
- 学到知识 → `evolve(type="KNOWLEDGE_GAINED")`
- 每天凌晨 2 点 → `nightly()`
- 每周日 → `fractal()`

**何时不用：**
- 日常对话无需记录

---

## 知识获取

### web-knowledge
**何时用：**
- 实时信息（新闻、天气、股价）
- 你不知道的事情
- 需要验证信息

**何时不用：**
- 已知知识范围内
- 数学计算

---

## 定时任务

```bash
# 每天凌晨 2 点 - 夜间循环
0 2 * * * python3 skills/self-evolution/main.py nightly

# 每周日上午 9 点 - RAG 评估
0 9 * * 0 python3 skills/rag/main.py evaluate --days 7 --report
```

---

_版本：1.0.0 | 2026-04-01_
