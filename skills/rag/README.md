# RAG 评估框架

基于 AutoRAG 理念，为 ai-baby 定制的轻量级 RAG 评估系统。

## 核心指标

### 检索质量
- **Hit Rate**: 检索到相关记忆的比例
- **MRR**: 第一个相关结果的平均倒数排名
- **Precision@K**: 前 K 个结果的相关性

### 生成质量
- **Relevance**: 回答与问题的相关性（用户反馈）
- **Helpfulness**: 有帮助程度（用户反馈）

### 系统性能
- **Latency**: 响应时间（ms）
- **Token Cost**: 每次查询的 token 消耗

## 使用方法

```bash
# 记录一次检索
python3 skills/rag/evaluate.py --record \
  --query "用户偏好" \
  --retrieved 5 \
  --latency 120 \
  --feedback positive

# 查看本周报告
python3 skills/rag/evaluate.py --report --week

# 自动调优实验
python3 skills/rag/auto_tune.py
```

## 文件结构

```
skills/rag/
├── evaluate.py          # 评估框架主脚本
├── auto_tune.py         # 自动调优实验
├── metrics.py           # 指标计算
├── config.json          # 配置参数
└── logs/
    └── evaluations.jsonl  # 评估日志
```

## 配置参数

```json
{
  "top_k_options": [3, 5, 10],
  "similarity_thresholds": [0.6, 0.7, 0.8],
  "chunk_sizes": [256, 512, 1024],
  "weights": {
    "accuracy": 0.6,
    "latency": 0.3,
    "cost": 0.1
  }
}
```
