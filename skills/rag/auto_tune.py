#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG 自动调优 - 基于 AutoRAG 理念
自动实验不同配置，选择最优方案
"""

import json
import os
import sys
import time
import random
from datetime import datetime
from pathlib import Path
from path_utils import resolve_workspace, resolve_data_dir
from typing import Dict, List, Tuple
import statistics

# 配置
SKILLS_DIR = Path(__file__).parent
# 使用 memory_hub 的相同路径：data/${agent_name}/logs/evaluations.jsonl
DATA_DIR = SKILLS_DIR.parent.parent / "data" / os.environ.get("OPENCLAW_AGENT", os.path.basename(str(resolve_workspace())).replace("workspace-", ""))"
LOGS_DIR = DATA_DIR / "logs"
CONFIG_FILE = SKILLS_DIR / "config.json"
EVALUATIONS_FILE = LOGS_DIR / "evaluations.jsonl"
EXPERIMENTS_FILE = LOGS_DIR / "experiments.jsonl"

# 确保目录存在
LOGS_DIR.mkdir(parents=True, exist_ok=True)


class AutoTuner:
    """RAG 自动调优器"""
    
    def __init__(self):
        self.config = self._load_config()
        self.experiments = []
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_evaluations(self, days: int = 7) -> List[Dict]:
        """加载评估记录"""
        from datetime import timedelta
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
    
    def design_experiments(self) -> List[Dict]:
        """设计实验配置"""
        experiments = []
        
        # 全因子设计（所有组合）
        for top_k in self.config["top_k_options"]:
            for threshold in self.config["similarity_thresholds"]:
                for chunk_size in self.config["chunk_sizes"]:
                    experiments.append({
                        "top_k": top_k,
                        "similarity_threshold": threshold,
                        "chunk_size": chunk_size,
                        "status": "pending",
                        "created_at": datetime.now().isoformat()
                    })
        
        # 随机打乱顺序
        random.shuffle(experiments)
        
        return experiments
    
    def calculate_score(self, evaluations: List[Dict], weights: Dict = None) -> float:
        """
        计算配置的综合得分
        
        分数 = w1 * 准确率 + w2 * (1/延迟归一化) + w3 * (1/成本归一化)
        """
        if not evaluations:
            return 0.0
        
        weights = weights or self.config["weights"]
        
        # 准确率（正面反馈率）
        positive = sum(1 for e in evaluations if e.get("feedback") == "positive")
        accuracy = positive / len(evaluations) if evaluations else 0
        
        # 延迟（归一化到 0-1，假设 500ms 为最差）
        latencies = [e["latency_ms"] for e in evaluations]
        avg_latency = statistics.mean(latencies) if latencies else 500
        latency_score = max(0, 1 - (avg_latency / 500))
        
        # 成本（如果有 token 数据，过滤 None 值）
        token_costs = [e.get("token_cost") for e in evaluations if e.get("token_cost") is not None]
        avg_cost = statistics.mean(token_costs) if token_costs else 100
        cost_score = max(0, 1 - (avg_cost / 1000))
        
        # 加权总分
        total_score = (
            weights["accuracy"] * accuracy +
            weights["latency"] * latency_score +
            weights["cost"] * cost_score
        )
        
        return round(total_score, 4)
    
    def analyze_results(self) -> Dict:
        """分析实验结果"""
        evaluations = self._load_evaluations(days=30)
        
        if len(evaluations) < self.config.get("min_samples_for_comparison", 10):
            return {
                "error": f"数据不足，需要至少 {self.config.get('min_samples_for_comparison', 10)} 条记录",
                "current_count": len(evaluations)
            }
        
        # 按配置分组（兼容旧数据，缺少 chunk_size 时使用默认值 512）
        config_groups = {}
        for e in evaluations:
            cfg = e.get('config', {})
            top_k = cfg.get('top_k', 5)
            threshold = cfg.get('similarity_threshold', 0.7)
            chunk_size = cfg.get('chunk_size', 512)
            config_key = f"top{top_k}_thresh{threshold}_chunk{chunk_size}"
            if config_key not in config_groups:
                config_groups[config_key] = []
            config_groups[config_key].append(e)
        
        # 计算每组得分
        results = []
        for config_key, evals in config_groups.items():
            if len(evals) < 3:
                continue
            
            score = self.calculate_score(evals)
            latencies = [e["latency_ms"] for e in evals]
            positive = sum(1 for e in evals if e.get("feedback") == "positive")
            
            results.append({
                "config_key": config_key,
                "config": evals[0]["config"],
                "samples": len(evals),
                "score": score,
                "avg_latency": round(statistics.mean(latencies), 2),
                "positive_rate": round(positive / len(evals) * 100, 1)
            })
        
        # 按得分排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # 推荐最优配置
        recommendation = None
        if results:
            best = results[0]
            recommendation = {
                "best_config": best["config"],
                "score": best["score"],
                "improvement": "需要基线对比"
            }
        
        return {
            "total_configs_tested": len(results),
            "total_evaluations": len(evaluations),
            "results": results,
            "recommendation": recommendation
        }
    
    def record_experiment(self, config: Dict, metrics: Dict):
        """记录实验结果"""
        experiment = {
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "metrics": metrics,
            "status": "completed"
        }
        
        with open(EXPERIMENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(experiment, ensure_ascii=False) + '\n')
        
        self.experiments.append(experiment)
    
    def suggest_next_experiment(self) -> Dict:
        """建议下一个实验配置"""
        # 简单策略：选择还没测试过的配置
        evaluations = self._load_evaluations(days=30)
        
        tested_configs = set()
        for e in evaluations:
            cfg = e.get('config', {})
            config_key = f"{cfg.get('top_k', 5)}_{cfg.get('similarity_threshold', 0.7)}_{cfg.get('chunk_size', 512)}"
            tested_configs.add(config_key)
        
        # 找到未测试的配置
        for top_k in self.config["top_k_options"]:
            for threshold in self.config["similarity_thresholds"]:
                for chunk_size in self.config["chunk_sizes"]:
                    config_key = f"{top_k}_{threshold}_{chunk_size}"
                    if config_key not in tested_configs:
                        return {
                            "top_k": top_k,
                            "similarity_threshold": threshold,
                            "chunk_size": chunk_size,
                            "reason": "未测试过的配置"
                        }
        
        # 所有配置都测试过了，建议重新测试表现最好的
        analysis = self.analyze_results()
        if "recommendation" in analysis and analysis["recommendation"]:
            best = analysis["recommendation"]["best_config"]
            return {
                **best,
                "reason": "验证最优配置"
            }
        
        return {"error": "所有配置已测试"}
    
    def generate_report(self) -> str:
        """生成调优报告"""
        analysis = self.analyze_results()
        
        if "error" in analysis:
            return f"❌ {analysis['error']}\n当前数据量：{analysis.get('current_count', 0)}"
        
        report = []
        report.append("=" * 60)
        report.append("🔬 RAG 自动调优报告")
        report.append("=" * 60)
        report.append("")
        report.append(f"📊 总配置数：{analysis['total_configs_tested']}")
        report.append(f"📈 总评估数：{analysis['total_evaluations']}")
        report.append("")
        
        report.append("🏆 Top 3 配置:")
        report.append("-" * 60)
        
        for i, result in enumerate(analysis["results"][:3], 1):
            cfg = result['config']
            report.append(f"\n#{i}: {result['config_key']}")
            report.append(f"    综合得分：{result['score']}")
            report.append(f"    样本数：{result['samples']}")
            report.append(f"    平均延迟：{result['avg_latency']}ms")
            report.append(f"    正面反馈：{result['positive_rate']}%")
            report.append(f"    配置:")
            report.append(f"      - Top-K: {cfg.get('top_k', 5)}")
            report.append(f"      - 相似度阈值：{cfg.get('similarity_threshold', 0.7)}")
            report.append(f"      - Chunk 大小：{cfg.get('chunk_size', 512)}")
        
        if analysis["recommendation"]:
            report.append("")
            report.append("=" * 60)
            report.append("💡 推荐配置:")
            best = analysis["recommendation"]["best_config"]
            report.append(f"   Top-K: {best.get('top_k', 5)}")
            report.append(f"   相似度阈值：{best.get('similarity_threshold', 0.7)}")
            report.append(f"   Chunk 大小：{best.get('chunk_size', 512)}")
            report.append(f"   综合得分：{analysis['recommendation']['score']}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG 自动调优")
    parser.add_argument("--design", action="store_true", help="设计实验")
    parser.add_argument("--analyze", action="store_true", help="分析结果")
    report_group = parser.add_mutually_exclusive_group()
    report_group.add_argument("--report", action="store_true", help="生成报告")
    report_group.add_argument("--next", action="store_true", help="建议下一个实验")
    
    args = parser.parse_args()
    tuner = AutoTuner()
    
    if args.design:
        experiments = tuner.design_experiments()
        print(f"设计了 {len(experiments)} 个实验配置:")
        for i, exp in enumerate(experiments[:5], 1):
            print(f"  {i}. top_k={exp['top_k']}, threshold={exp['similarity_threshold']}, chunk={exp['chunk_size']}")
        if len(experiments) > 5:
            print(f"  ... 还有 {len(experiments) - 5} 个配置")
    
    elif args.analyze:
        analysis = tuner.analyze_results()
        if "error" in analysis:
            print(f"❌ {analysis['error']}")
        else:
            print(f"✅ 分析了 {analysis['total_evaluations']} 条评估记录")
            print(f"   测试了 {analysis['total_configs_tested']} 种配置")
    
    elif args.report:
        report = tuner.generate_report()
        print(report)
    
    elif args.next:
        suggestion = tuner.suggest_next_experiment()
        if "error" in suggestion:
            print(f"❌ {suggestion['error']}")
        else:
            print("💡 建议下一个实验:")
            print(f"   Top-K: {suggestion['top_k']}")
            print(f"   相似度阈值：{suggestion['similarity_threshold']}")
            print(f"   Chunk 大小：{suggestion['chunk_size']}")
            print(f"   原因：{suggestion['reason']}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
