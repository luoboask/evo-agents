#!/usr/bin/env python3
"""
预测性维护系统 - Predictive Maintenance
预测可能的问题并提前采取预防措施
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class PredictiveMaintenance:
    """预测性维护系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.learning_dir = self.workspace / "memory" / "learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 风险模式库
        self.risk_patterns = self._load_risk_patterns()
    
    def _load_risk_patterns(self):
        """加载已知的风险模式"""
        patterns_file = self.learning_dir / "risk_patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                return json.load(f)
        
        # 默认风险模式
        return {
            "network_timeout": {
                "description": "网络超时风险",
                "indicators": [
                    "web_search 调用时间逐渐增加",
                    "curl timeout 错误频率增加",
                    "网络相关工具成功率下降"
                ],
                "threshold": 0.8,  # 触发阈值
                "prevention": [
                    "提前切换到备选搜索引擎",
                    "增加超时时间",
                    "添加网络健康检查"
                ]
            },
            "disk_space": {
                "description": "磁盘空间不足风险",
                "indicators": [
                    "知识图谱文件快速增长",
                    "反思日志文件过大",
                    "缓存文件未清理"
                ],
                "threshold": 0.7,
                "prevention": [
                    "自动清理旧日志",
                    "压缩历史数据",
                    "归档不常用文件"
                ]
            },
            "memory_fragmentation": {
                "description": "记忆碎片化风险",
                "indicators": [
                    "每日记忆文件过多",
                    "MEMORY.md 更新频率下降",
                    "知识图谱实体孤立"
                ],
                "threshold": 0.6,
                "prevention": [
                    "定期合并记忆",
                    "归档旧记忆",
                    "重建知识图谱"
                ]
            },
            "skill_duplication": {
                "description": "技能重复/冗余风险",
                "indicators": [
                    "多个相似技能",
                    "功能重叠的工具",
                    "未使用的旧版本"
                ],
                "threshold": 0.5,
                "prevention": [
                    "合并相似技能",
                    "标记废弃版本",
                    "创建技能索引"
                ]
            }
        }
    
    def _save_risk_patterns(self):
        """保存风险模式"""
        patterns_file = self.learning_dir / "risk_patterns.json"
        with open(patterns_file, 'w') as f:
            json.dump(self.risk_patterns, f, indent=2)
    
    def analyze_health(self):
        """分析系统健康状态"""
        health_score = 100
        risks = []
        
        # 1. 检查网络工具健康度
        network_health = self._check_network_health()
        if network_health < 80:
            health_score -= (100 - network_health) * 0.3
            risks.append({
                "type": "network_timeout",
                "severity": "high" if network_health < 60 else "medium",
                "score": network_health,
                "message": f"网络工具健康度: {network_health:.0f}%"
            })
        
        # 2. 检查磁盘使用
        disk_health = self._check_disk_health()
        if disk_health < 80:
            health_score -= (100 - disk_health) * 0.2
            risks.append({
                "type": "disk_space",
                "severity": "high" if disk_health < 50 else "medium",
                "score": disk_health,
                "message": f"磁盘使用健康度: {disk_health:.0f}%"
            })
        
        # 3. 检查记忆系统健康度
        memory_health = self._check_memory_health()
        if memory_health < 70:
            health_score -= (100 - memory_health) * 0.2
            risks.append({
                "type": "memory_fragmentation",
                "severity": "medium",
                "score": memory_health,
                "message": f"记忆系统健康度: {memory_health:.0f}%"
            })
        
        # 4. 检查技能冗余
        skill_health = self._check_skill_health()
        if skill_health < 70:
            health_score -= (100 - skill_health) * 0.15
            risks.append({
                "type": "skill_duplication",
                "severity": "low",
                "score": skill_health,
                "message": f"技能系统健康度: {skill_health:.0f}%"
            })
        
        return {
            "overall_score": max(0, health_score),
            "status": "healthy" if health_score > 80 else "warning" if health_score > 60 else "critical",
            "risks": risks
        }
    
    def _check_network_health(self):
        """检查网络工具健康度"""
        # 读取最近7天的自动反思日志
        recent_logs = self._get_recent_logs(7)
        
        web_search_logs = [l for l in recent_logs if l.get("tool") == "web_search"]
        if not web_search_logs:
            return 100  # 没有数据，假设健康
        
        # 样本量过小则跳过检查，避免误报
        MIN_SAMPLE_SIZE = 5
        if len(web_search_logs) < MIN_SAMPLE_SIZE:
            return 100  # 样本不足，假设健康

        # 计算成功率
        success_count = sum(1 for l in web_search_logs if l.get("success"))
        success_rate = success_count / len(web_search_logs)
        
        # 计算平均耗时趋势
        avg_duration = sum(l.get("duration", 0) for l in web_search_logs) / len(web_search_logs)
        baseline = 10.0  # 基准时间
        duration_score = max(0, 1 - (avg_duration - baseline) / baseline)
        
        # 综合评分
        health = (success_rate * 0.7 + duration_score * 0.3) * 100
        return health
    
    def _check_disk_health(self):
        """检查磁盘使用健康度"""
        memory_dir = self.workspace / "memory"
        
        # 计算 memory 目录大小
        total_size = 0
        file_count = 0
        for file_path in memory_dir.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        # 假设 100MB 为警戒线
        max_size = 100 * 1024 * 1024
        usage_ratio = total_size / max_size
        
        health = max(0, (1 - usage_ratio) * 100)
        return health
    
    def _check_memory_health(self):
        """检查记忆系统健康度"""
        memory_dir = self.workspace / "memory"
        
        # 统计每日记忆文件数量
        daily_files = list(memory_dir.glob("*.md"))
        if len(daily_files) < 7:
            return 100  # 文件少，健康
        
        # 检查 MEMORY.md 是否更新
        memory_file = self.workspace / "MEMORY.md"
        if memory_file.exists():
            # 简化检查：假设如果存在就健康
            pass
        
        # 文件过多表示碎片化
        if len(daily_files) > 30:
            return 50  # 需要归档
        elif len(daily_files) > 14:
            return 70
        
        return 100
    
    def _check_skill_health(self):
        """检查技能系统健康度"""
        skills_dir = self.workspace / "skills"
        
        # 统计技能数量
        skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
        
        # 检查是否有重复版本（如 search.py 和 search_v2.py）
        duplicates = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                py_files = list(skill_dir.glob("*.py"))
                if len(py_files) > 2:  # 超过2个Python文件可能有冗余
                    duplicates += 1
        
        # 评分
        if duplicates > 3:
            return 50
        elif duplicates > 1:
            return 75
        
        return 100
    
    def _get_recent_logs(self, days):
        """获取最近几天的日志"""
        logs = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = self.learning_dir / f"auto_reflections_{date}.jsonl"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
        return logs
    
    def generate_prevention_plan(self, health_report):
        """生成预防性维护计划"""
        plan = []
        
        for risk in health_report.get("risks", []):
            risk_type = risk.get("type")
            if risk_type in self.risk_patterns:
                pattern = self.risk_patterns[risk_type]
                plan.append({
                    "risk": risk_type,
                    "description": pattern["description"],
                    "severity": risk["severity"],
                    "actions": pattern["prevention"],
                    "indicators": pattern["indicators"]
                })
        
        return plan
    
    def print_health_report(self):
        """打印健康报告"""
        health = self.analyze_health()
        
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "critical": "🔴"
        }
        
        print("\n" + "=" * 60)
        print(f"🏥 系统健康报告 {status_emoji.get(health['status'], '❓')}")
        print("=" * 60)
        print()
        print(f"总体健康度: {health['overall_score']:.0f}/100")
        print(f"状态: {health['status'].upper()}")
        print()
        
        if health['risks']:
            print("⚠️  检测到的风险:")
            for risk in health['risks']:
                severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                print(f"   {severity_emoji.get(risk['severity'], '⚪')} [{risk['severity'].upper()}] {risk['message']}")
            print()
            
            # 生成预防计划
            plan = self.generate_prevention_plan(health)
            if plan:
                print("🔧 预防性维护建议:")
                for item in plan:
                    print(f"   📋 {item['description']}")
                    for action in item['actions']:
                        print(f"      → {action}")
                    print()
        else:
            print("✅ 未检测到明显风险，系统运行良好！")
        
        print("=" * 60)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='预测性维护系统')
    parser.add_argument('--check', action='store_true', help='检查系统健康')
    parser.add_argument('--monitor', action='store_true', help='持续监控模式')
    
    args = parser.parse_args()
    
    pm = PredictiveMaintenance()
    
    if args.check or args.monitor:
        pm.print_health_report()
    else:
        pm.print_health_report()


if __name__ == '__main__':
    main()
