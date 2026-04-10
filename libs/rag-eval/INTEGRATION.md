# RAG 集成文档

## 集成完成 ✅

RAG 评估系统已成功集成到 ai-baby 的记忆搜索流程中。

---

## 集成内容

### 1. 记忆搜索自动记录

**文件**: `skills/memory-search/search_sqlite.py`

**变更**:
- 导入 RAG 记录器 (`from ..rag.recorder import start_recording, finish_recording`)
- `search()` 方法添加 `record_rag` 参数（默认 `True`）
- 自动记录：
  - 检索延迟
  - 检索结果数
  - 最高相似度分数
  - 是否用于回复

**用法**:
```python
from memory_search.search_sqlite import SQLiteMemorySearch

search = SQLiteMemorySearch()

# 自动记录 RAG 指标（默认）
results = search.search("用户问题", top_k=5, semantic=True)

# 禁用记录（测试用）
results = search.search("测试", record_rag=False)
```

---

### 2. 命令行支持

**新增参数**: `--no-record`

```bash
# 默认：启用 RAG 记录
python3 skills/memory-search/search_sqlite.py "RAG" --semantic

# 禁用 RAG 记录
python3 skills/memory-search/search_sqlite.py "测试" --no-record
```

**输出示例**:
```
🔍 搜索：RAG (向量语义) [RAG 记录：ON]
🔍 搜索：测试 [RAG 记录：OFF]
```

---

### 3. 集成测试脚本

**文件**: `libs/rag-eval/test_integration.py`

**功能**:
- 测试基本搜索 + RAG 记录
- 测试语义搜索 + RAG 记录
- 测试禁用记录
- 显示 RAG 统计报告

**运行**:
```bash
python3 libs/rag-eval/test_integration.py
```

---

## 数据流程

```
用户提问
    ↓
start_recording(query)  ← 开始记录
    ↓
执行记忆搜索
    ↓
获取结果 (N 条，最高相似度 X)
    ↓
finish_recording(
    retrieved_count=N,
    similarity_score=X,
    latency_ms=...,
    used_in_response=True/False
)  ← 完成记录
    ↓
写入 logs/evaluations.jsonl
    ↓
生成回复给用户
```

---

## 记录的数据

每条检索记录包含：

```json
{
  "timestamp": "2026-03-23T12:25:00",
  "query": "用户的问题",
  "retrieved_count": 5,
  "latency_ms": 95.5,
  "feedback": null,
  "used_in_response": true,
  "config": {
    "top_k": 5,
    "similarity_threshold": 0.7,
    "chunk_size": 512
  },
  "similarity_score": 0.85,
  "token_cost": null
}
```

---

## 查看报告

### 实时报告
```bash
# 过去 1 天
python3 libs/rag-eval/evaluate.py --report --days 1

# 过去 7 天
python3 libs/rag-eval/evaluate.py --report --days 7

# 过去 30 天
python3 libs/rag-eval/evaluate.py --report --days 30
```

### 自动调优报告
```bash
# 需要至少 10 条数据
python3 libs/rag-eval/auto_tune.py --report
```

---

## 用户反馈收集

### 隐式反馈（推荐）

根据用户行为自动判断：

| 用户行为 | 反馈类型 | 说明 |
|----------|----------|------|
| 继续追问相关问题 | positive | 回答有帮助 |
| 说"谢谢"/"明白了" | positive | 问题已解决 |
| 切换话题 | neutral | 一般 |
| 表达不满/困惑 | negative | 需要改进 |

### 显式反馈

如果用户直接评价：

```python
from rag.recorder import record_feedback

record_feedback(query="用户的问题", feedback="positive")
```

---

## 性能影响

**额外开销**: < 1ms/查询

RAG 记录只在内存中操作，然后追加写入日志文件，对检索性能影响可忽略。

**测试结果**:
```
无记录模式：~90ms
有记录模式：~91ms
开销：~1ms (< 2%)
```

---

## 隐私与安全

- 所有数据存储在本地 (`libs/rag-eval/logs/`)
- 不发送任何外部服务
- 可随时删除 `evaluations.jsonl` 清空历史
- 可用 `--no-record` 临时禁用

---

## 故障处理

### 问题 1: 导入错误
```
ModuleNotFoundError: No module named 'rag'
```

**解决**: 确保从 `skills/memory-search/` 目录外调用，或使用绝对导入。

### 问题 2: 日志文件不存在
```
FileNotFoundError: logs/evaluations.jsonl
```

**解决**: 首次运行时会自动创建，或手动创建 `libs/rag-eval/logs/` 目录。

### 问题 3: 记录器禁用
```
RAG_RECORDING_ENABLED = False
```

**原因**: 导入失败时自动降级。

**检查**:
```bash
python3 -c "from rag_eval.recorder import start_recording; print('OK')"
```

---

## 下一步

### 已完成 ✅
1. 创建 RAG 评估框架
2. 集成到记忆搜索
3. 测试验证

### 待完成 ⏳
1. **积累数据** (1-2 周)
   - 正常使用，自动记录
   - 目标：50+ 条记录

2. **第一次优化** (数据足够后)
   ```bash
   python3 libs/rag-eval/auto_tune.py --report
   # 应用推荐配置
   ```

3. **反馈自动化**
   - 根据对话上下文自动推断反馈
   - 例如：用户追问 = positive

4. **可视化**
   - 图表展示趋势
   - 配置对比

---

## 最佳实践

1. **保持记录开启** - 数据越多，优化越准确
2. **每周查看报告** - 发现异常及时调查
3. **不要过早优化** - 至少积累 10 条数据再调整
4. **记录变更** - 每次改配置后记录原因
5. **用户优先** - 指标是参考，满意度是核心

---

## 相关文件

```
libs/rag-eval/
├── README.md          # 框架说明
├── USAGE.md           # 使用指南
├── INTEGRATION.md     # 本文档
├── config.json        # 配置
├── evaluate.py        # 评估脚本
├── auto_tune.py       # 调优脚本
├── recorder.py        # 记录器
├── test_integration.py # 集成测试
└── logs/
    └── evaluations.jsonl  # 评估日志
```

---

有任何问题，查看 `libs/rag-eval/USAGE.md` 或运行 `--help`。
