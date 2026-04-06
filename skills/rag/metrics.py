#!/usr/bin/env python3
"""
RAG 评估指标计算
基于 AutoRAG 理念
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import math

SKILLS_DIR = Path(__file__).parent
LOGS_DIR = SKILLS_DIR / "logs"
EVALUATIONS_FILE = LOGS_DIR / "evaluations.jsonl"


class RAGMetrics:
    """RAG 评估指标计算器"""
    
    def __init__(self, days=7):
        self.days = days
        self.evaluations = self._load_evaluations()
    
    def _load_evaluations(self) -> List[Dict]:
        """加载评估记录"""
        evals = []
        cutoff = datetime.now() - timedelta(days=self.days)
        
        if EVALUATIONS_FILE.exists():
            with open(EVALUATIONS_FILE, 'r') as f:
                for line in f:
                    try:
                        eval_data = json.loads(line)
                        eval_time = datetime.fromisoformat(eval_data["timestamp"])
                        if eval_time >= cutoff:
                            evals.append(eval_data)
                    except:
                        continue
        return evals
    
    def hit_rate(self) -> float:
        """命中率 (Hit Rate)"""
        if not self.evaluations:
            return 0.0
        hits = sum(1 for e in self.evaluations if e.get('retrieved_count', 0) > 0)
        return hits / len(self.evaluations)
    
    def mrr(self) -> float:
        """平均倒数排名 (Mean Reciprocal Rank)"""
        if not self.evaluations:
            return 0.0
        
        # 简化版：假设正面反馈的查询，排名为 1
        positive = [e for e in self.evaluations if e.get('feedback') == 'positive']
        if not positive:
            return 0.0
        
        reciprocal_ranks = [1.0 / 1 for _ in positive]  # 简化假设
        return sum(reciprocal_ranks) / len(self.evaluations)
    
    def precision_at_k(self, k=5) -> float:
        """Precision@K"""
        if not self.evaluations:
            return 0.0
        
        # 简化版：使用 retrieved_count 和反馈计算
        relevant = sum(1 for e in self.evaluations 
                      if e.get('retrieved_count', 0) >= k 
                      and e.get('feedback') == 'positive')
        return relevant / len(self.evaluations)
    
    def satisfaction_rate(self) -> float:
        """用户满意度"""
        if not self.evaluations:
            return 0.0
        
        positive = sum(1 for e in self.evaluations if e.get('feedback') == 'positive')
        return positive / len(self.evaluations)
    
    def avg_latency(self) -> float:
        """平均延迟"""
        if not self.evaluations:
            return 0.0
        
        latencies = [e.get('latency_ms', 0) for e in self.evaluations]
        return sum(latencies) / len(latencies)
    
    def report(self) -> Dict:
        """生成完整报告"""
        return {
            'period': f'{self.days} days',
            'total_queries': len(self.evaluations),
            'hit_rate': self.hit_rate(),
            'mrr': self.mrr(),
            'precision_at_5': self.precision_at_k(5),
            'satisfaction_rate': self.satisfaction_rate(),
            'avg_latency_ms': self.avg_latency(),
        }


if __name__ == '__main__':
    metrics = RAGMetrics(days=7)
    report = metrics.report()
    
    print("=" * 60)
    print("📊 RAG 评估指标报告")
    print("=" * 60)
    print(f"周期：{report['period']}")
    print(f"总查询数：{report['total_queries']}")
    print(f"命中率 (Hit Rate): {report['hit_rate']:.1%}")
    print(f"平均倒数排名 (MRR): {report['mrr']:.3f}")
    print(f"Precision@5: {report['precision_at_5']:.1%}")
    print(f"用户满意度：{report['satisfaction_rate']:.1%}")
    print(f"平均延迟：{report['avg_latency_ms']:.1f}ms")
    print("=" * 60)
