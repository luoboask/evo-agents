# evo-agents Benchmarks

**记忆系统基准测试** - 受 MemPalace 启发

---

## 🎯 测试目标

评估 evo-agents 记忆系统的检索能力，包括：
- ✅ 记忆存储效率
- ✅ 语义搜索准确率
- ✅ 分形思考质量
- ✅ 知识图谱完整性

---

## 📊 测试数据集

### 1. LongMemEval 风格测试

**500 个问题，6 种类型**：

| 类型 | 数量 | 说明 |
|------|------|------|
| Knowledge Update | 78 | 随时间变化的事实 |
| Multi-Session | 133 | 跨多轮对话 |
| Temporal Reasoning | 133 | 时间推理 |
| Single-Session User | 70 | 单轮用户信息 |
| Single-Session Preference | 30 | 用户偏好 |
| Single-Session Assistant | 56 | AI 说的话 |

### 2. 自定义测试集

**evo-agents 特定场景**：

| 测试 | 问题数 | 说明 |
|------|--------|------|
| Memory Search | 50 | 记忆检索能力 |
| Fractal Thinking | 30 | 分形分析质量 |
| Knowledge Graph | 40 | 知识图谱查询 |
| Self-Evolution | 30 | 进化事件追踪 |

---

## 🔧 使用方法

### 快速开始

```bash
# 1. 进入基准测试目录
cd ~/.openclaw/workspace/benchmarks

# 2. 运行完整测试
python3 run_all_benchmarks.py

# 3. 运行单个测试
python3 longmemeval_test.py
python3 memory_search_test.py
python3 fractal_thinking_test.py
python3 knowledge_graph_test.py
```

### 配置选项

```bash
# 指定 Agent 测试
python3 run_all_benchmarks.py --agent main-agent

# 指定测试集
python3 longmemeval_test.py --limit 100

# 输出详细报告
python3 run_all_benchmarks.py --verbose

# 生成对比报告
python3 run_all_benchmarks.py --compare baseline
```

---

## 📈 评估指标

### 核心指标

| 指标 | 说明 | 计算方式 |
|------|------|----------|
| **Recall@5** | 前 5 个结果的召回率 | 正确答案在 top-5 的比例 |
| **Recall@10** | 前 10 个结果的召回率 | 正确答案在 top-10 的比例 |
| **NDCG@5** | 排序质量 | 归一化折损累积增益 |
| **NDCG@10** | 排序质量 | 归一化折损累积增益 |
| **Precision** | 准确率 | 检索结果中正确的比例 |
| **F1 Score** | 综合指标 | Precision 和 Recall 的调和平均 |

### 计算公式

```python
def recall_any(rankings, correct_ids, k):
    """至少一个正确答案在 top-k 中"""
    top_k_ids = set(rankings[:k])
    return float(any(cid in top_k_ids for cid in correct_ids))

def recall_all(rankings, correct_ids, k):
    """所有正确答案都在 top-k 中"""
    top_k_ids = set(rankings[:k])
    return float(all(cid in top_k_ids for cid in correct_ids))

def ndcg(rankings, correct_ids, k):
    """归一化折损累积增益"""
    relevances = [1.0 if idx in correct_ids else 0.0 for idx in rankings[:k]]
    dcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(relevances))
    idcg = sum(1.0 / math.log2(i + 2) for i in range(min(len(correct_ids), k)))
    return dcg / idcg if idcg > 0 else 0.0
```

---

## 📁 输出格式

### JSONL 日志

```json
{"question_id": "q001", "recall@5": 1.0, "recall@10": 1.0, "ndcg@5": 0.95, "question_type": "multi-session"}
{"question_id": "q002", "recall@5": 0.5, "recall@10": 1.0, "ndcg@5": 0.78, "question_type": "temporal"}
```

### Markdown 报告

```markdown
# evo-agents Benchmark Report

**Date:** 2026-04-11
**Agent:** main-agent
**Total Questions:** 500

## Overall Results

| Metric | Score |
|--------|-------|
| Recall@5 | 96.6% |
| Recall@10 | 98.2% |
| NDCG@5 | 0.94 |
| NDCG@10 | 0.96 |

## By Question Type

| Type | Count | Recall@5 | Recall@10 |
|------|-------|----------|-----------|
| Knowledge Update | 78 | 99.0% | 100% |
| Multi-Session | 133 | 98.5% | 100% |
| ... | ... | ... | ... |
```

---

## 🔄 持续测试

### Cron 配置

```bash
# 每周运行一次基准测试
openclaw cron add --cron "0 10 * * 0" \
  --agent main-agent \
  --message "python3 benchmarks/run_all_benchmarks.py --report" \
  --name "weekly-benchmark-test" \
  --no-deliver \
  --session isolated
```

### 趋势追踪

```python
# 记录每次测试结果
import json
from datetime import datetime

result = {
    'date': datetime.now().isoformat(),
    'agent': 'main-agent',
    'recall@5': 0.966,
    'recall@10': 0.982,
    'ndcg@5': 0.94,
    'total_questions': 500
}

# 追加到历史文件
with open('benchmark_history.jsonl', 'a') as f:
    f.write(json.dumps(result) + '\n')
```

---

## 📊 对比分析

### 版本对比

```bash
# 生成版本对比报告
python3 benchmarks/compare.py \
  --baseline v5.0 \
  --current v5.1 \
  --output report.md
```

### 模式对比

```bash
# 对比不同记忆模式
python3 benchmarks/compare_modes.py \
  --modes raw,semantic,fractal \
  --output mode_comparison.md
```

---

## 🎯 目标分数

| 指标 | 当前 | 目标 | 优秀 |
|------|------|------|------|
| Recall@5 | - | 90% | 95% |
| Recall@10 | - | 95% | 98% |
| NDCG@5 | - | 0.85 | 0.90 |
| NDCG@10 | - | 0.90 | 0.95 |

**参考基准**：
- MemPalace Raw: 96.6% Recall@5
- MemPalace Hybrid: 99.4% Recall@5
- MemPalace + Rerank: 100% Recall@5

---

## 🛠️ 开发新测试

### 添加新测试集

```python
# benchmarks/custom_test.py
from memory_hub import MemoryHub
from metrics import evaluate_retrieval

def run_custom_test():
    """运行自定义测试"""
    memory = MemoryHub(agent_name="test-agent")
    
    # 加载测试数据
    questions = load_questions('data/custom_questions.json')
    
    results = []
    for q in questions:
        # 导入记忆
        for session in q['haystack']:
            memory.add_session(session)
        
        # 查询
        retrieved = memory.search(q['question'], top_k=10)
        
        # 评估
        metrics = evaluate_retrieval(retrieved, q['ground_truth'])
        results.append(metrics)
    
    # 输出报告
    print_report(results)
```

---

## 📚 参考资料

- [MemPalace Benchmarks](https://github.com/milla-jovovich/mempalace/tree/main/benchmarks)
- [LongMemEval Paper](https://arxiv.org/abs/2401.xxxxx)
- [LoCoMo Benchmark](https://locobench.github.io/)

---

_版本：1.0.0 | 2026-04-11_
