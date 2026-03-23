#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG 评估框架 - ai-baby 专用
记录、分析、优化检索增强生成系统
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import sqlite3
import statistics

# 配置
SKILLS_DIR = Path(__file__).parent
CONFIG_FILE = SKILLS_DIR / "config.json"

# 从个人配置加载日志路径
def get_evaluations_file():
    """获取评估日志文件路径（从配置文件）"""
    config_paths = [
        Path.home() / ".openclaw" / "workspace-ai-baby-config" / "config.yaml",
        Path("config.yaml"),
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                log_path = config.get('rag', {}).get('log_path')
                if log_path:
                    return Path(log_path)
            except:
                pass
    
    # fallback 到默认路径
    return SKILLS_DIR / "logs" / "evaluations.jsonl"

EVALUATIONS_FILE = get_evaluations_file()
LOGS_DIR = EVALUATIONS_FILE.parent

# 确保目录存在
LOGS_DIR.mkdir(exist_ok=True)


class RAGEvaluator:
    """RAG 评估器"""
    
    def __init__(self):
        self.config = self._load_config()
        self.evaluations = []
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        # 默认配置
        return {
            "top_k_options": [3, 5, 10],
            "similarity_thresholds": [0.6, 0.7, 0.8],
            "chunk_sizes": [256, 512, 1024],
            "weights": {
                "accuracy": 0.6,
                "latency": 0.3,
                "cost": 0.1
            },
            "current_config": {
                "top_k": 5,
                "similarity_threshold": 0.7,
                "chunk_size": 512
            }
        }
    
    def save_config(self):
        """保存配置"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def record(self, query: str, retrieved_count: int, latency_ms: float,
               feedback: Optional[str] = None, used_in_response: bool = True,
               top_k: Optional[int] = None, similarity_score: Optional[float] = None,
               token_cost: Optional[int] = None) -> Dict:
        """
        记录一次检索评估
        
        Args:
            query: 检索查询
            retrieved_count: 检索到的结果数
            latency_ms: 延迟（毫秒）
            feedback: 用户反馈 (positive/negative/neutral)
            used_in_response: 是否用于最终回复
            top_k: 使用的 top-k 值
            similarity_score: 最高相似度分数
            token_cost: token 消耗
        """
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "retrieved_count": retrieved_count,
            "latency_ms": latency_ms,
            "feedback": feedback,
            "used_in_response": used_in_response,
            "config": {
                "top_k": top_k or self.config["current_config"]["top_k"],
                "similarity_threshold": similarity_score or self.config["current_config"]["similarity_threshold"],
                "chunk_size": self.config["current_config"]["chunk_size"]
            },
            "similarity_score": similarity_score,
            "token_cost": token_cost
        }
        
        # 追加到日志文件
        with open(EVALUATIONS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evaluation, ensure_ascii=False) + '\n')
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def load_evaluations(self, days: int = 7) -> List[Dict]:
        """加载最近 N 天的评估记录"""
        evaluations = []
        cutoff = datetime.now() - timedelta(days=days)
        
        if not EVALUATIONS_FILE.exists():
            return []
        
        with open(EVALUATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    eval_data = json.loads(line.strip())
                    eval_time = datetime.fromisoformat(eval_data["timestamp"])
                    if eval_time >= cutoff:
                        evaluations.append(eval_data)
                except:
                    continue
        
        return evaluations
    
    def calculate_metrics(self, evaluations: List[Dict]) -> Dict:
        """计算评估指标"""
        if not evaluations:
            return {"error": "No evaluations found"}
        
        # 基础统计
        total = len(evaluations)
        latencies = [e["latency_ms"] for e in evaluations]
        retrieved_counts = [e["retrieved_count"] for e in evaluations]
        
        # 反馈统计
        feedback_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for e in evaluations:
            fb = e.get("feedback", "neutral")
            if fb in feedback_counts:
                feedback_counts[fb] += 1
        
        # 使用率
        used_count = sum(1 for e in evaluations if e.get("used_in_response", True))
        
        # 相似度统计（如果有）
        similarity_scores = [e["similarity_score"] for e in evaluations if e.get("similarity_score")]
        
        metrics = {
            "period": f"{total} evaluations",
            "total_queries": total,
            "latency": {
                "avg_ms": round(statistics.mean(latencies), 2) if latencies else 0,
                "median_ms": round(statistics.median(latencies), 2) if latencies else 0,
                "min_ms": min(latencies) if latencies else 0,
                "max_ms": max(latencies) if latencies else 0
            },
            "retrieval": {
                "avg_results": round(statistics.mean(retrieved_counts), 2) if retrieved_counts else 0,
                "usage_rate": round(used_count / total * 100, 1) if total > 0 else 0
            },
            "feedback": {
                "positive": feedback_counts["positive"],
                "neutral": feedback_counts["neutral"],
                "negative": feedback_counts["negative"],
                "positive_rate": round(feedback_counts["positive"] / total * 100, 1) if total > 0 else 0
            },
            "similarity": {
                "avg_score": round(statistics.mean(similarity_scores), 3) if similarity_scores else None,
                "min_score": round(min(similarity_scores), 3) if similarity_scores else None,
                "max_score": round(max(similarity_scores), 3) if similarity_scores else None
            }
        }
        
        return metrics
    
    def generate_report(self, days: int = 7) -> str:
        """生成评估报告"""
        evaluations = self.load_evaluations(days)
        metrics = self.calculate_metrics(evaluations)
        
        if "error" in metrics:
            return f"❌ {metrics['error']}"
        
        report = []
        report.append("=" * 60)
        report.append("📊 RAG 评估报告")
        report.append(f"   周期：过去 {days} 天")
        report.append("=" * 60)
        report.append("")
        
        # 基础统计
        report.append("📈 基础统计")
        report.append(f"   总查询数：{metrics['total_queries']}")
        report.append(f"   检索使用率：{metrics['retrieval']['usage_rate']}%")
        report.append("")
        
        # 延迟
        report.append("⏱️  延迟性能")
        report.append(f"   平均：{metrics['latency']['avg_ms']}ms")
        report.append(f"   中位数：{metrics['latency']['median_ms']}ms")
        report.append(f"   范围：{metrics['latency']['min_ms']} - {metrics['latency']['max_ms']}ms")
        report.append("")
        
        # 检索
        report.append("🔍 检索效果")
        report.append(f"   平均结果数：{metrics['retrieval']['avg_results']}")
        report.append("")
        
        # 反馈
        report.append("💬 用户反馈")
        report.append(f"   正面：{metrics['feedback']['positive']} ({metrics['feedback']['positive_rate']}%)")
        report.append(f"   中性：{metrics['feedback']['neutral']}")
        report.append(f"   负面：{metrics['feedback']['negative']}")
        report.append("")
        
        # 相似度
        if metrics['similarity']['avg_score']:
            report.append("📏 相似度")
            report.append(f"   平均：{metrics['similarity']['avg_score']}")
            report.append(f"   范围：{metrics['similarity']['min_score']} - {metrics['similarity']['max_score']}")
            report.append("")
        
        # 当前配置
        report.append("⚙️  当前配置")
        current = self.config["current_config"]
        report.append(f"   Top-K: {current['top_k']}")
        report.append(f"   相似度阈值：{current['similarity_threshold']}")
        report.append(f"   Chunk 大小：{current['chunk_size']}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def compare_configs(self) -> Dict:
        """比较不同配置的表现"""
        evaluations = self.load_evaluations(days=30)
        
        if len(evaluations) < 10:
            return {"error": "Not enough data for comparison"}
        
        # 按配置分组
        config_groups = {}
        for e in evaluations:
            config_key = f"top{k}_thresh{t}".format(
                k=e["config"]["top_k"],
                t=e["config"]["similarity_threshold"]
            )
            if config_key not in config_groups:
                config_groups[config_key] = []
            config_groups[config_key].append(e)
        
        # 计算每组的表现
        results = {}
        for config_key, evals in config_groups.items():
            if len(evals) < 3:
                continue
            
            latencies = [e["latency_ms"] for e in evals]
            positive = sum(1 for e in evals if e.get("feedback") == "positive")
            
            results[config_key] = {
                "count": len(evals),
                "avg_latency": round(statistics.mean(latencies), 2),
                "positive_rate": round(positive / len(evals) * 100, 1),
                "config": evals[0]["config"]
            }
        
        return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG 评估框架")
    parser.add_argument("--record", action="store_true", help="记录一次检索")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--compare", action="store_true", help="比较配置")
    parser.add_argument("--query", type=str, help="检索查询")
    parser.add_argument("--retrieved", type=int, default=0, help="检索结果数")
    parser.add_argument("--latency", type=float, default=0.0, help="延迟 (ms)")
    parser.add_argument("--feedback", type=str, choices=["positive", "negative", "neutral"], help="用户反馈")
    parser.add_argument("--days", type=int, default=7, help="报告天数")
    parser.add_argument("--top-k", type=int, help="Top-K 值")
    parser.add_argument("--similarity", type=float, help="相似度分数")
    
    args = parser.parse_args()
    evaluator = RAGEvaluator()
    
    if args.record:
        if not args.query:
            print("❌ 需要 --query 参数")
            sys.exit(1)
        
        result = evaluator.record(
            query=args.query,
            retrieved_count=args.retrieved,
            latency_ms=args.latency,
            feedback=args.feedback,
            top_k=args.top_k,
            similarity_score=args.similarity
        )
        print(f"✅ 已记录：{result['timestamp']}")
        print(f"   Query: {result['query']}")
        print(f"   Retrieved: {result['retrieved_count']}")
        print(f"   Latency: {result['latency_ms']}ms")
    
    elif args.report:
        report = evaluator.generate_report(days=args.days)
        print(report)
    
    elif args.compare:
        comparison = evaluator.compare_configs()
        if "error" in comparison:
            print(f"❌ {comparison['error']}")
        else:
            print("=" * 60)
            print("🔬 配置对比")
            print("=" * 60)
            for config_key, data in comparison.items():
                print(f"\n{config_key}:")
                print(f"   样本数：{data['count']}")
                print(f"   平均延迟：{data['avg_latency']}ms")
                print(f"   正面反馈：{data['positive_rate']}%")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
