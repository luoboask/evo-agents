# -*- coding: utf-8 -*-
"""
评估接口 - 记录和分析检索质量
"""

from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class EvaluationInterface:
    """评估接口 - 记录和分析检索质量"""
    
    def __init__(self, hub):
        self.hub = hub
        self.evaluations_path = self.hub.data_path / 'logs' / 'evaluations.jsonl'
        self.evaluations_path.parent.mkdir(parents=True, exist_ok=True)
    
    def record(self,
               query: str,
               retrieved_count: int,
               latency_ms: float,
               feedback: Optional[str] = None,
               similarity_score: Optional[float] = None,
               top_k: int = 5,
               used_in_response: bool = True) -> Dict:
        """记录一次检索评估"""
        evaluation = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'retrieved_count': retrieved_count,
            'latency_ms': latency_ms,
            'feedback': feedback,
            'similarity_score': similarity_score,
            'config': {
                'top_k': top_k,
                'similarity_threshold': similarity_score
            },
            'used_in_response': used_in_response
        }
        
        # 追加到日志文件
        with open(self.evaluations_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evaluation, ensure_ascii=False) + '\n')
        
        return evaluation
    
    def generate_report(self, days: int = 7) -> str:
        """生成评估报告"""
        evaluations = self._load_evaluations(days)
        
        if not evaluations:
            return "❌ 没有评估数据"
        
        # 统计
        total = len(evaluations)
        latencies = [e['latency_ms'] for e in evaluations]
        feedback_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        for e in evaluations:
            fb = e.get('feedback', 'neutral')
            if fb in feedback_counts:
                feedback_counts[fb] += 1
        
        # 生成报告
        report = []
        report.append("=" * 60)
        report.append("📊 RAG 评估报告")
        report.append(f"   周期：过去 {days} 天")
        report.append("=" * 60)
        report.append("")
        
        report.append("📈 基础统计")
        report.append(f"   总查询数：{total}")
        report.append(f"   检索使用率：{sum(1 for e in evaluations if e['used_in_response']) / total * 100:.1f}%")
        report.append("")
        
        report.append("⏱️  延迟性能")
        report.append(f"   平均：{sum(latencies) / len(latencies):.2f}ms")
        report.append(f"   中位数：{sorted(latencies)[len(latencies)//2]:.2f}ms")
        report.append(f"   范围：{min(latencies):.2f} - {max(latencies):.2f}ms")
        report.append("")
        
        report.append("💬 用户反馈")
        report.append(f"   正面：{feedback_counts['positive']} ({feedback_counts['positive'] / total * 100:.1f}%)")
        report.append(f"   中性：{feedback_counts['neutral']}")
        report.append(f"   负面：{feedback_counts['negative']}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def analyze(self, min_samples: int = 10) -> Dict:
        """分析评估数据，推荐最优配置"""
        evaluations = self._load_evaluations(days=30)
        
        if len(evaluations) < min_samples:
            return {
                'error': f'数据不足，需要至少 {min_samples} 条记录',
                'current_count': len(evaluations)
            }
        
        # 按配置分组分析
        config_groups = {}
        for e in evaluations:
            config_key = f"top{e['config']['top_k']}"
            if config_key not in config_groups:
                config_groups[config_key] = []
            config_groups[config_key].append(e)
        
        # 计算每组表现
        results = {}
        for config_key, evals in config_groups.items():
            if len(evals) < 3:
                continue
            
            latencies = [e['latency_ms'] for e in evals]
            positive = sum(1 for e in evals if e.get('feedback') == 'positive')
            
            results[config_key] = {
                'count': len(evals),
                'avg_latency': sum(latencies) / len(latencies),
                'positive_rate': positive / len(evals) * 100
            }
        
        # 推荐最优配置
        best_config = max(results.items(), key=lambda x: x[1]['positive_rate'])
        
        return {
            'total_evaluations': len(evaluations),
            'configs_tested': len(results),
            'results': results,
            'recommendation': {
                'config': best_config[0],
                'positive_rate': best_config[1]['positive_rate']
            }
        }
    
    def _load_evaluations(self, days: int) -> List[Dict]:
        """加载指定天数的评估记录"""
        evaluations = []
        cutoff = datetime.now() - timedelta(days=days)
        
        if not self.evaluations_path.exists():
            return evaluations
        
        with open(self.evaluations_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    eval_data = json.loads(line.strip())
                    eval_time = datetime.fromisoformat(eval_data['timestamp'])
                    if eval_time >= cutoff:
                        evaluations.append(eval_data)
                except:
                    continue
        
        return evaluations
