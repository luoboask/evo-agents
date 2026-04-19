#!/usr/bin/env python3
"""
测试进化系统 v2.0

测试内容:
1. 效果追踪
2. 方案复用
3. 自动策略切换
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from effect_tracker import EffectTracker
from solution_reuse import SolutionReuse
from auto_strategy import AutoStrategy
from self_evolution_real import RealSelfEvolution


def test_effect_tracker():
    """测试效果追踪"""
    print("=" * 60)
    print("测试 1: 效果追踪")
    print("=" * 60)
    
    tracker = EffectTracker()
    
    # 记录解决方案
    tracker.record_solution(
        problem="API 超时",
        problem_type="性能问题",
        solution="增加重试机制",
        gene_used="repair_from_errors"
    )
    
    # 标记使用效果
    tracker.mark_used("API 超时", success=True)
    tracker.mark_used("API 超时", success=True)
    tracker.mark_used("API 超时", success=False)
    
    # 获取统计
    stats = tracker.get_stats()
    print(f"📊 统计信息:")
    print(f"  总方案数：{stats['total_solutions']}")
    print(f"  有效方案：{stats['effective_solutions']}")
    print(f"  平均成功率：{stats['average_success_rate']:.1%}")
    
    # 获取有效方案
    effective = tracker.get_effective_solutions()
    print(f"\n✅ 有效方案：{len(effective)} 个")
    
    print()


def test_solution_reuse():
    """测试方案复用"""
    print("=" * 60)
    print("测试 2: 方案复用")
    print("=" * 60)
    
    reuse = SolutionReuse()
    
    # 模拟解决问题
    def mock_solver(problem):
        return f"解决方案：{problem}"
    
    # 第一次：新方案
    solution1, source1 = reuse.solve_with_reuse(
        problem="数据库连接超时",
        problem_type="性能问题",
        solve_func=mock_solver
    )
    print(f"第 1 次：来源={source1}")
    
    # 第二次：应该复用
    solution2, source2 = reuse.solve_with_reuse(
        problem="数据库连接超时",
        problem_type="性能问题",
        solve_func=mock_solver
    )
    print(f"第 2 次：来源={source2}")
    
    print()


def test_auto_strategy():
    """测试自动策略切换"""
    print("=" * 60)
    print("测试 3: 自动策略切换")
    print("=" * 60)
    
    auto = AutoStrategy()
    
    # 获取系统状态
    state = auto.get_system_state()
    print(f"系统状态:")
    print(f"  成功率：{state['success_rate']:.1%}")
    print(f"  最近失败：{state['recent_failures']}")
    
    # 推荐策略
    recommended = auto.get_recommended_strategy()
    print(f"  推荐策略：{recommended}")
    
    # 自动切换
    switched = auto.auto_switch_if_needed()
    print(f"  是否切换：{switched}")
    
    print()


def test_full_integration():
    """测试完整集成"""
    print("=" * 60)
    print("测试 4: 完整集成")
    print("=" * 60)
    
    evolution = RealSelfEvolution()
    
    # 获取统计
    stats = evolution.get_evolution_stats()
    print(f"进化统计:")
    print(f"  总方案：{stats['total_solutions']}")
    print(f"  有效率：{stats['effective_rate']:.1%}")
    
    print()


if __name__ == '__main__':
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "进化系统 v2.0 测试" + " " * 21 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    test_effect_tracker()
    test_solution_reuse()
    test_auto_strategy()
    test_full_integration()
    
    print("=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)
    print()
