#!/usr/bin/env python3
"""
基准测试评估指标

受 MemPalace 启发实现
"""

import math
from typing import List, Set, Dict, Tuple


def dcg(relevances: List[float], k: int) -> float:
    """
    Discounted Cumulative Gain (折损累积增益)
    
    Args:
        relevances: 相关性分数列表（0 或 1）
        k: 截断位置
    
    Returns:
        DCG 分数
    """
    score = 0.0
    for i, rel in enumerate(relevances[:k]):
        score += rel / math.log2(i + 2)
    return score


def ndcg(rankings: List[int], correct_ids: Set[int], corpus_ids: List[int], k: int) -> float:
    """
    Normalized DCG (归一化折损累积增益)
    
    Args:
        rankings: 检索结果的索引列表
        correct_ids: 正确答案的 ID 集合
        corpus_ids: 语料库 ID 列表
        k: 截断位置
    
    Returns:
        NDCG 分数 (0-1)
    """
    # 计算相关性
    relevances = [1.0 if corpus_ids[idx] in correct_ids else 0.0 for idx in rankings[:k]]
    
    # 计算 DCG
    dcg_score = dcg(relevances, k)
    
    # 计算理想 DCG（所有正确答案排在最前）
    ideal_relevances = sorted(relevances, reverse=True)
    idcg_score = dcg(ideal_relevances, k)
    
    # 归一化
    return dcg_score / idcg_score if idcg_score > 0 else 0.0


def evaluate_retrieval(
    rankings: List[int],
    correct_ids: Set[int],
    corpus_ids: List[int],
    k_values: List[int] = [5, 10]
) -> Dict[str, float]:
    """
    评估检索结果
    
    Args:
        rankings: 检索结果的索引列表（按相关性排序）
        correct_ids: 正确答案的 ID 集合
        corpus_ids: 语料库 ID 列表
        k_values: 要评估的 k 值列表
    
    Returns:
        评估指标字典
    """
    metrics = {}
    
    for k in k_values:
        # Recall@k (Any) - 至少一个正确答案在 top-k 中
        top_k_ids = set(corpus_ids[idx] for idx in rankings[:k])
        recall_any = float(any(cid in top_k_ids for cid in correct_ids))
        
        # Recall@k (All) - 所有正确答案都在 top-k 中
        recall_all = float(all(cid in top_k_ids for cid in correct_ids))
        
        # NDCG@k
        ndcg_score = ndcg(rankings, correct_ids, corpus_ids, k)
        
        metrics[f'recall_any@{k}'] = recall_any
        metrics[f'recall_all@{k}'] = recall_all
        metrics[f'ndcg@{k}'] = ndcg_score
    
    return metrics


def calculate_precision(rankings: List[int], correct_ids: Set[int], corpus_ids: List[int], k: int) -> float:
    """
    计算精确率
    
    Args:
        rankings: 检索结果的索引列表
        correct_ids: 正确答案的 ID 集合
        corpus_ids: 语料库 ID 列表
        k: 截断位置
    
    Returns:
        Precision@k
    """
    top_k_ids = [corpus_ids[idx] for idx in rankings[:k]]
    correct_count = sum(1 for cid in top_k_ids if cid in correct_ids)
    return correct_count / k


def calculate_f1(precision: float, recall: float) -> float:
    """
    计算 F1 分数
    
    Args:
        precision: 精确率
        recall: 召回率
    
    Returns:
        F1 分数
    """
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)


def aggregate_metrics(all_results: List[Dict[str, float]]) -> Dict[str, float]:
    """
    聚合多个问题的评估结果
    
    Args:
        all_results: 每个问题的评估结果列表
    
    Returns:
        平均指标字典
    """
    if not all_results:
        return {}
    
    # 初始化累加器
    metrics_sum = {}
    for result in all_results:
        for key, value in result.items():
            if isinstance(value, (int, float)):
                metrics_sum[key] = metrics_sum.get(key, 0) + value
    
    # 计算平均值
    num_results = len(all_results)
    return {key: value / num_results for key, value in metrics_sum.items()}


def print_report(metrics: Dict[str, float], question_type: str = None):
    """
    打印评估报告
    
    Args:
        metrics: 评估指标字典
        question_type: 问题类型（可选）
    """
    prefix = f"[{question_type}] " if question_type else ""
    
    print(f"\n{prefix}评估结果:")
    print(f"  Recall@5:  {metrics.get('recall_any@5', 0):.1%}")
    print(f"  Recall@10: {metrics.get('recall_any@10', 0):.1%}")
    print(f"  NDCG@5:    {metrics.get('ndcg@5', 0):.3f}")
    print(f"  NDCG@10:   {metrics.get('ndcg@10', 0):.3f}")
    
    if 'precision@5' in metrics:
        print(f"  Precision@5: {metrics['precision@5']:.1%}")
        print(f"  F1@5:        {metrics.get('f1@5', 0):.3f}")


# =============================================================================
# 使用示例
# =============================================================================

if __name__ == '__main__':
    # 示例数据
    rankings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # 检索结果索引
    correct_ids = {2, 5, 7}  # 正确答案 ID
    corpus_ids = [f'doc_{i}' for i in range(100)]  # 语料库 ID
    
    # 评估
    metrics = evaluate_retrieval(rankings, correct_ids, corpus_ids, k_values=[5, 10])
    
    # 打印报告
    print_report(metrics)
    
    # 聚合多个问题的结果
    all_results = [
        {'recall_any@5': 1.0, 'recall_any@10': 1.0, 'ndcg@5': 0.95},
        {'recall_any@5': 0.5, 'recall_any@10': 1.0, 'ndcg@5': 0.78},
        {'recall_any@5': 1.0, 'recall_any@10': 1.0, 'ndcg@5': 1.0},
    ]
    
    avg_metrics = aggregate_metrics(all_results)
    print(f"\n平均结果:")
    print(f"  Recall@5:  {avg_metrics.get('recall_any@5', 0):.1%}")
    print(f"  NDCG@5:    {avg_metrics.get('ndcg@5', 0):.3f}")
