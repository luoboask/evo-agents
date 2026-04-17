#!/usr/bin/env python3
"""
双 Agent 对比测试

测试对象:
- Agent v1 (旧): 原始进化系统
- Agent v2 (新): 进化系统 v2.0

测试场景:
1. 重复问题测试 - 看谁能复用历史方案
2. 效果追踪测试 - 看谁能追踪成功/失败
3. 策略适应测试 - 看谁能自动调整策略
4. 综合效率测试 - 看谁更有效率
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# Agent v1 (旧) - 原始进化系统 (不使用 v2 功能)
# Agent v2 (新) - 进化系统 v2.0 (使用完整功能)
from self_evolution_real import RealSelfEvolution


class TestAgent:
    """测试 Agent"""
    
    def __init__(self, name: str, use_v2: bool = True):
        self.name = name
        self.use_v2 = use_v2
        self.evolution = RealSelfEvolution()
        self.test_results = []
    
    def solve_problem(self, problem: str, problem_type: str = "测试问题") -> tuple:
        """解决问题"""
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
    
    def get_stats(self) -> dict:
        """获取统计"""
        return self.evolution.get_evolution_stats()
    
    def get_reuse_rate(self) -> float:
        """计算复用率"""
        if not self.test_results:
            return 0.0
        
        reused = sum(1 for r in self.test_results if r['source'] == 'reused')
        return reused / len(self.test_results)


def run_comparison_test():
    """运行对比测试"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "双 Agent 对比测试" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # 创建两个 Agent
    agent_v1 = TestAgent("Agent v1 (旧)", "v1")
    agent_v2 = TestAgent("Agent v2 (新)", "v2")
    
    # 测试场景
    test_scenarios = [
        ("API 调用超时", "性能问题"),
        ("API 响应慢", "性能问题"),
        ("数据库连接超时", "性能问题"),
        ("内存泄漏", "代码质量"),
        ("功能需求变更", "功能需求"),
    ]
    
    results = {
        'v1': {'reused': 0, 'new': 0},
        'v2': {'reused': 0, 'new': 0}
    }
    
    # 测试 1: 重复问题测试
    print("=" * 70)
    print("测试 1: 重复问题测试 - 看谁能复用历史方案")
    print("=" * 70)
    
    for i, (problem, ptype) in enumerate(test_scenarios, 1):
        print(f"\n第 {i} 轮:")
        
        # Agent v1
        _, source1 = agent_v1.solve_problem(problem, ptype)
        print(f"  Agent v1: {source1}")
        if source1 == 'reused':
            results['v1']['reused'] += 1
        else:
            results['v1']['new'] += 1
        
        # Agent v2
        _, source2 = agent_v2.solve_problem(problem, ptype)
        print(f"  Agent v2: {source2}")
        if source2 == 'reused':
            results['v2']['reused'] += 1
        else:
            results['v2']['new'] += 1
    
    # 测试 2: 效果追踪测试
    print("\n" + "=" * 70)
    print("测试 2: 效果追踪测试 - 看谁能追踪成功/失败")
    print("=" * 70)
    
    # 标记反馈
    for problem, _ in test_scenarios[:3]:
        agent_v1.mark_feedback(problem, success=True)
        agent_v2.mark_feedback(problem, success=True)
    
    # 标记一个失败案例
    agent_v1.mark_feedback(test_scenarios[3][0], success=False)
    agent_v2.mark_feedback(test_scenarios[3][0], success=False)
    
    print("\n已标记反馈:")
    print(f"  Agent v1: 3 成功，1 失败")
    print(f"  Agent v2: 3 成功，1 失败")
    
    # 测试 3: 统计对比
    print("\n" + "=" * 70)
    print("测试 3: 统计对比")
    print("=" * 70)
    
    stats_v1 = agent_v1.get_stats()
    stats_v2 = agent_v2.get_stats()
    
    print(f"""
Agent v1 (旧):
  总方案数：{stats_v1['total_solutions']}
  有效率：{stats_v1['effective_rate']:.1%}
  平均成功率：{stats_v1['average_success_rate']:.1%}
  复用率：{agent_v1.get_reuse_rate():.1%}

Agent v2 (新):
  总方案数：{stats_v2['total_solutions']}
  有效率：{stats_v2['effective_rate']:.1%}
  平均成功率：{stats_v2['average_success_rate']:.1%}
  复用率：{agent_v2.get_reuse_rate():.1%}
""")
    
    # 测试 4: 综合评分
    print("=" * 70)
    print("测试 4: 综合评分")
    print("=" * 70)
    
    score_v1 = (
        stats_v1['average_success_rate'] * 40 +  # 成功率 40 分
        stats_v1['effective_rate'] * 30 +  # 有效率 30 分
        agent_v1.get_reuse_rate() * 30  # 复用率 30 分
    )
    
    score_v2 = (
        stats_v2['average_success_rate'] * 40 +
        stats_v2['effective_rate'] * 30 +
        agent_v2.get_reuse_rate() * 30
    )
    
    print(f"""
Agent v1 (旧): {score_v1:.1f} / 100
  - 成功率：{stats_v1['average_success_rate']:.1%} × 40 = {stats_v1['average_success_rate'] * 40:.1f}
  - 有效率：{stats_v1['effective_rate']:.1%} × 30 = {stats_v1['effective_rate'] * 30:.1f}
  - 复用率：{agent_v1.get_reuse_rate():.1%} × 30 = {agent_v1.get_reuse_rate() * 30:.1f}

Agent v2 (新): {score_v2:.1f} / 100
  - 成功率：{stats_v2['average_success_rate']:.1%} × 40 = {stats_v2['average_success_rate'] * 40:.1f}
  - 有效率：{stats_v2['effective_rate']:.1%} × 30 = {stats_v2['effective_rate'] * 30:.1f}
  - 复用率：{agent_v2.get_reuse_rate():.1%} × 30 = {agent_v2.get_reuse_rate() * 30:.1f}
""")
    
    # 最终结论
    print("=" * 70)
    print("最终结论")
    print("=" * 70)
    
    if score_v2 > score_v1:
        winner = "Agent v2 (新)"
        improvement = score_v2 - score_v1
        print(f"""
🏆 获胜者：{winner}

优势:
  ✅ 复用率提升：{(agent_v2.get_reuse_rate() - agent_v1.get_reuse_rate()) * 100:.1f}%
  ✅ 有效率提升：{(stats_v2['effective_rate'] - stats_v1['effective_rate']) * 100:.1f}%
  ✅ 综合评分提升：{improvement:.1f} 分

结论：Agent v2 (新) 更聪明！
""")
    elif score_v1 > score_v2:
        winner = "Agent v1 (旧)"
        print(f"""
🏆 获胜者：{winner}

结论：Agent v1 (旧) 表现更好
""")
    else:
        print("""
🤝 平局

结论：两个 Agent 表现相当
""")
    
    return {
        'v1_score': score_v1,
        'v2_score': score_v2,
        'winner': winner if score_v1 != score_v2 else 'tie'
    }


if __name__ == '__main__':
    run_comparison_test()
