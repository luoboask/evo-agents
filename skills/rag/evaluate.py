#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG 评估框架 - 使用 Memory Hub
记录、分析、优化检索增强生成系统
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import statistics

# 导入 Memory Hub (共享库)
# 添加 libs 目录到路径
LIBS_DIR = Path(__file__).parent.parent.parent / 'libs'
sys.path.insert(0, str(LIBS_DIR))

try:
    from memory_hub import MemoryHub
    MEMORY_HUB_ENABLED = True
except ImportError:
    MEMORY_HUB_ENABLED = False

# 配置
SKILLS_DIR = Path(__file__).parent
CONFIG_FILE = SKILLS_DIR / "config.json"
EVALUATIONS_FILE = SKILLS_DIR / "logs" / "evaluations.jsonl"
EVALUATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)


class RAGEvaluator:
    """RAG 评估器 - 使用 Memory Hub"""
    
    def __init__(self, agent_name='demo-agent'):
        """
        初始化 RAG 评估器
        
        Args:
            agent_name: Agent 名称（默认从环境变量获取）
        """
        self.agent_name = agent_name
        self.config = self._load_config()
        self.evaluations = []
        
        # 使用 Memory Hub
        if MEMORY_HUB_ENABLED:
            self.hub = MemoryHub(agent_name)
        else:
            self.hub = None
        
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
            feedback: 用户反馈
            used_in_response: 是否用于最终回复
            top_k: 使用的 top-k 值
            similarity_score: 最高相似度分数
            token_cost: token 消耗
        
        Returns:
            评估记录
        """
        # 使用 Memory Hub
        if self.hub:
            return self.hub.evaluation.record(
                query=query,
                retrieved_count=retrieved_count,
                latency_ms=latency_ms,
                feedback=feedback,
                similarity_score=similarity_score,
                top_k=top_k or self.config["current_config"]["top_k"],
                used_in_response=used_in_response
            )
        
        # Fallback: 直接记录
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "retrieved_count": retrieved_count,
            "latency_ms": latency_ms,
            "feedback": feedback,
            "used_in_response": used_in_response,
            "config": {
                "top_k": top_k or self.config["current_config"]["top_k"],
            },
            "similarity_score": similarity_score,
            "token_cost": token_cost
        }
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def load_evaluations(self, days: int = 7) -> List[Dict]:
        """加载最近 N 天的评估记录"""
        evaluations = []
        cutoff = datetime.now() - timedelta(days=days)
        
        # 优先使用 Memory Hub 的评估数据
        if self.hub and hasattr(self.hub, 'evaluation'):
            eval_path = self.hub.evaluation.evaluations_path
            if eval_path.exists():
                with open(eval_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            eval_data = json.loads(line.strip())
                            eval_time = datetime.fromisoformat(eval_data["timestamp"])
                            if eval_time >= cutoff:
                                evaluations.append(eval_data)
                        except:
                            continue
                return evaluations
        
        # Fallback: 本地文件
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
        if self.hub:
            return self.hub.evaluation.generate_report(days=days)
        
        # Fallback: 简单报告
        if not self.evaluations:
            return "❌ No evaluations found"
        
        return f"📊 RAG 评估报告\n   周期：过去 {days} 天\n   总查询数：{len(self.evaluations)}"
    
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
    parser.add_argument("--agent", type=str, default="demo-agent", help="Agent 名称")
    
    args = parser.parse_args()
    evaluator = RAGEvaluator(agent_name=args.agent)
    
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
