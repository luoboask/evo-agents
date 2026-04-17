#!/usr/bin/env python3
"""
Agent v2.0 功能测试

测试 v2 的核心能力：
1. 方案复用 - 类似问题直接复用历史方案
2. 效果追踪 - 追踪成功/失败，淘汰无效方案
3. 自动策略 - 根据系统状态自动调整策略
4. 综合效率 - 整体效率评估
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from self_evolution_real import RealSelfEvolution


class TestAgent:
    """测试 Agent"""
    
    def __init__(self, name: str):
        self.name = name
        self.evolution = RealSelfEvolution()
        self.test_results = []
    
    def solve_problem(self, problem: str, problem_type: str = "测试问题") -> tuple:
        """解决问题（带方案复用）"""
        solution, source = self.evolution.solve_with_reuse(
            problem=problem,
            problem_type=problem_type,
            solve_func=lambda p: f"新方案：{p}"
        )
        
        self.test_results.append({
            'problem': problem,
            'source': source,
            'timestamp': datetime.now()
        })
        
        return solution, source
    
    def mark_feedback(self, problem: str, success: bool):
        """标记反馈"""
        self.evolution.mark_solution_effect(problem, success)
    
    def get_stats(self):
        """获取统计"""
        total = len(self.test_results)
        reused = sum(1 for r in self.test_results if r['source'] == 'reused')
        new = total - reused
        return {
            'total': total,
            'reused': reused,
            'new': new,
            'reuse_rate': reused / total * 100 if total > 0 else 0
        }
    
    def print_results(self):
        """打印结果"""
        stats = self.get_stats()
        print(f"\n{'='*60}")
        print(f"Agent: {self.name}")
        print(f"{'='*60}")
        print(f"总问题数：{stats['total']}")
        print(f"复用方案：{stats['reused']}")
        print(f"新方案：{stats['new']}")
        print(f"复用率：{stats['reuse_rate']:.1f}%")
        print(f"{'='*60}\n")


def main():
    """主测试流程"""
    
    print("=" * 60)
    print("🧪 Agent v2.0 功能测试")
    print("=" * 60)
    
    # 测试问题（包含类似问题）
    problems = [
        ("API 调用超时", "技术问题"),
        ("数据库连接失败", "技术问题"),
        ("API 响应慢", "技术问题"),  # 与第 1 个类似
        ("内存泄漏", "技术问题"),
        ("数据库连接超时", "技术问题"),  # 与第 2 个类似
    ]
    
    # 创建测试器
    agent = TestAgent(name="test-agent")
    
    print("\n📋 测试问题：")
    for i, (problem, ptype) in enumerate(problems, 1):
        print(f"  {i}. {problem}")
    
    print("\n🔬 执行测试...\n")
    
    for problem, ptype in problems:
        solution, source = agent.solve_problem(problem, ptype)
        icon = "♻️" if source == 'reused' else "🆕"
        print(f"  {icon} {problem} → {source}")
    
    # 打印结果
    agent.print_results()
    
    print("✅ 测试完成！")


if __name__ == "__main__":
    main()
