#!/usr/bin/env python3
"""
智能改进建议生成器 - Improvement Generator
基于模式识别自动生成改进方案
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class ImprovementGenerator:
    """智能改进建议生成器"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.learning_dir = self.workspace / "memory" / "learning"
        self.improvements_dir = self.workspace / "skills"
        
        # 改进模式库
        self.improvement_patterns = self._load_patterns()
    
    def _load_patterns(self):
        """加载改进模式库"""
        return {
            "timeout_issue": {
                "pattern": r"timeout|timed out|超时",
                "category": "reliability",
                "solutions": [
                    {
                        "name": "添加重试机制",
                        "template": """
# 改进：添加重试机制
def {func_name}_with_retry(*args, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return {func_name}(*args, **kwargs)
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
""",
                        "effort": "medium",
                        "impact": "high"
                    },
                    {
                        "name": "增加超时时间",
                        "template": "将 timeout 从 {current}s 增加到 {improved}s",
                        "effort": "low",
                        "impact": "medium"
                    },
                    {
                        "name": "添加备选方案",
                        "template": """
# 改进：添加备选方案
def {func_name}_with_fallback(*args, **kwargs):
    try:
        return {func_name}_primary(*args, **kwargs)
    except TimeoutError:
        return {func_name}_backup(*args, **kwargs)
""",
                        "effort": "high",
                        "impact": "high"
                    }
                ]
            },
            "performance_issue": {
                "pattern": r"slow|performance|耗时|慢",
                "category": "performance",
                "solutions": [
                    {
                        "name": "添加缓存",
                        "template": """
# 改进：添加结果缓存
@lru_cache(maxsize=100)
def {func_name}_cached(*args, **kwargs):
    return {func_name}(*args, **kwargs)
""",
                        "effort": "low",
                        "impact": "high"
                    },
                    {
                        "name": "并行化处理",
                        "template": """
# 改进：并行处理
from concurrent.futures import ThreadPoolExecutor

def {func_name}_parallel(items, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map({func_name}, items))
""",
                        "effort": "medium",
                        "impact": "high"
                    },
                    {
                        "name": "异步化改造",
                        "template": """
# 改进：异步化
import asyncio

async def {func_name}_async(*args, **kwargs):
    return await asyncio.to_thread({func_name}, *args, **kwargs)
""",
                        "effort": "high",
                        "impact": "medium"
                    }
                ]
            },
            "error_handling": {
                "pattern": r"error|exception|失败|错误",
                "category": "robustness",
                "solutions": [
                    {
                        "name": "完善错误处理",
                        "template": """
# 改进：完善错误处理
def {func_name}_safe(*args, **kwargs):
    try:
        return {func_name}(*args, **kwargs)
    except SpecificError as e:
        logger.error(f"Known error: {{e}}")
        return default_value
    except Exception as e:
        logger.error(f"Unexpected error: {{e}}")
        raise
""",
                        "effort": "medium",
                        "impact": "high"
                    },
                    {
                        "name": "添加输入验证",
                        "template": """
# 改进：输入验证
def {func_name}_validated(*args, **kwargs):
    # 验证输入
    if not validate_input(*args, **kwargs):
        raise ValueError("Invalid input")
    return {func_name}(*args, **kwargs)
""",
                        "effort": "low",
                        "impact": "medium"
                    }
                ]
            },
            "duplication_issue": {
                "pattern": r"duplicate|redundant|重复|冗余",
                "category": "maintainability",
                "solutions": [
                    {
                        "name": "合并相似功能",
                        "template": """
# 改进：合并版本
# 将 {old_version} 和 {new_version} 合并为统一接口
def {func_name}_unified(*args, version='auto', **kwargs):
    if version == 'auto':
        version = select_best_version(*args, **kwargs)
    if version == 'v2':
        return {func_name}_v2(*args, **kwargs)
    return {func_name}(*args, **kwargs)
""",
                        "effort": "high",
                        "impact": "medium"
                    }
                ]
            }
        }
    
    def analyze_reflections(self, days=7):
        """分析反思日志，识别改进机会"""
        opportunities = []
        
        # 读取反思日志
        logs = self._get_reflection_logs(days)
        
        # 按工具分组
        tool_issues = defaultdict(list)
        for log in logs:
            tool = log.get("tool", "unknown")
            
            # 检查各种模式
            notes = log.get("notes", "") + " " + str(log.get("lesson", ""))
            
            for pattern_name, pattern_info in self.improvement_patterns.items():
                if re.search(pattern_info["pattern"], notes, re.IGNORECASE):
                    tool_issues[tool].append({
                        "pattern": pattern_name,
                        "category": pattern_info["category"],
                        "log": log,
                        "solutions": pattern_info["solutions"]
                    })
        
        # 生成改进机会
        for tool, issues in tool_issues.items():
            # 统计问题频率
            pattern_counts = defaultdict(int)
            for issue in issues:
                pattern_counts[issue["pattern"]] += 1
            
            # 找出最常见的问题
            most_common = max(pattern_counts.items(), key=lambda x: x[1])
            pattern_name, count = most_common
            
            # 找到对应的解决方案
            for issue in issues:
                if issue["pattern"] == pattern_name:
                    opportunities.append({
                        "tool": tool,
                        "issue_type": pattern_name,
                        "category": issue["category"],
                        "frequency": count,
                        "solutions": issue["solutions"],
                        "priority": self._calculate_priority(count, issue["category"])
                    })
                    break
        
        return sorted(opportunities, key=lambda x: -x["priority"])
    
    def _get_reflection_logs(self, days):
        """获取反思日志"""
        logs = []
        from datetime import timedelta
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            # 自动反思日志
            auto_log = self.learning_dir / f"auto_reflections_{date}.jsonl"
            if auto_log.exists():
                with open(auto_log, 'r') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
            
            # 手动反思日志
            manual_log = self.learning_dir / f"reflections_{date}.jsonl"
            if manual_log.exists():
                with open(manual_log, 'r') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
        
        return logs
    
    def _calculate_priority(self, frequency, category):
        """计算优先级"""
        category_weights = {
            "reliability": 1.5,
            "performance": 1.3,
            "robustness": 1.2,
            "maintainability": 1.0
        }
        return frequency * category_weights.get(category, 1.0)
    
    def generate_improvement_plan(self, days=7):
        """生成改进计划"""
        opportunities = self.analyze_reflections(days)
        
        if not opportunities:
            return []
        
        plan = []
        for opp in opportunities[:5]:  # 取前5个
            best_solution = max(opp["solutions"], 
                              key=lambda x: (x["impact"], -ord(x["effort"][0])))
            
            plan.append({
                "tool": opp["tool"],
                "issue": opp["issue_type"],
                "frequency": opp["frequency"],
                "priority": opp["priority"],
                "solution": best_solution["name"],
                "template": best_solution["template"],
                "effort": best_solution["effort"],
                "impact": best_solution["impact"]
            })
        
        return plan
    
    def print_improvement_plan(self):
        """打印改进计划"""
        plan = self.generate_improvement_plan()
        
        if not plan:
            print("✅ 未检测到需要改进的问题！")
            return
        
        print("\n" + "=" * 70)
        print("🚀 智能改进计划")
        print("=" * 70)
        print()
        
        for i, item in enumerate(plan, 1):
            priority_emoji = "🔴" if item["priority"] > 5 else "🟡" if item["priority"] > 2 else "🟢"
            print(f"{i}. {priority_emoji} [{item['tool']}] {item['issue']}")
            print(f"   发生频率: {item['frequency']} 次")
            print(f"   建议方案: {item['solution']}")
            print(f"   工作量: {item['effort']} | 影响: {item['impact']}")
            print()
            print("   代码模板:")
            print("   " + "-" * 60)
            template_lines = item['template'].strip().split('\n')
            for line in template_lines[:10]:  # 只显示前10行
                print(f"   {line}")
            if len(template_lines) > 10:
                print(f"   ... ({len(template_lines) - 10} more lines)")
            print("   " + "-" * 60)
            print()
        
        print("=" * 70)
        print(f"💡 共识别 {len(plan)} 个改进机会")
        print("=" * 70)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='智能改进建议生成器')
    parser.add_argument('--generate', action='store_true', help='生成改进计划')
    parser.add_argument('--days', type=int, default=7, help='分析天数')
    
    args = parser.parse_args()
    
    gen = ImprovementGenerator()
    
    if args.generate:
        gen.print_improvement_plan()
    else:
        gen.print_improvement_plan()


if __name__ == '__main__':
    main()
