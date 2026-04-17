#!/usr/bin/env python3
"""
双 Agent 对比测试 - 简化版

测试对象:
- Agent v1 (旧): 不使用方案复用
- Agent v2 (新): 使用方案复用 + 效果追踪

测试场景:
1. 重复问题测试 - 看谁能复用历史方案
2. 效果追踪测试 - 看谁能追踪成功/失败
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from self_evolution_real import RealSelfEvolution


def test_agent(name: str, problems: list, use_reuse: bool = True):
    """测试 Agent"""
    
    print(f"\n{name}:")
    print("-" * 50)
    
    evolution = RealSelfEvolution()
    results = []
    
    for problem, ptype in problems:
        if use_reuse:
            # v2: 使用方案复用
            solution, source = evolution.solve_with_reuse(
                problem=problem,
                problem_type=ptype,
                solve_func=lambda p: f"新方案：{p}"
            )
        else:
            # v1: 直接记录新方案
            solution = f"新方案：{problem}"
            source = 'new'
            evolution.effect_tracker.record_solution(problem, ptype, solution)
        
        results.append({
            'problem': problem,
            'source': source
        })
        
        print(f"  {problem[:30]:<30} → {source}")
    
    # 标记反馈
    print("\n  标记反馈...")
    for problem, _ in problems[:3]:
        evolution.mark_solution_effect(problem, success=True)
        print(f"    ✅ {problem[:20]}")
    
    if len(problems) > 3:
        evolution.mark_solution_effect(problems[3][0], success=False)
        print(f"    ❌ {problems[3][0][:20]}")
    
    # 获取统计
    stats = evolution.get_evolution_stats()
    reuse_rate = sum(1 for r in results if r['source'] == 'reused') / len(results) if results else 0
    
    print(f"\n  统计:")
    print(f"    总方案：{stats['total_solutions']}")
    print(f"    复用率：{reuse_rate:.1%}")
    print(f"    平均成功率：{stats['average_success_rate']:.1%}")
    
    return {
        'reuse_rate': reuse_rate,
        'success_rate': stats['average_success_rate'],
        'total': stats['total_solutions']
    }


def main():
    """主测试"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "双 Agent 对比测试 - 简化版" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # 测试问题
    problems = [
        ("API 调用超时", "性能问题"),
        ("API 响应慢", "性能问题"),
        ("数据库连接超时", "性能问题"),
        ("内存泄漏", "代码质量"),
        ("功能需求变更", "功能需求"),
    ]
    
    # 测试 Agent v1 (旧) - 不使用复用
    print("\n" + "=" * 70)
    print("Agent v1 (旧) - 不使用方案复用")
    print("=" * 70)
    
    stats_v1 = test_agent("Agent v1", problems, use_reuse=False)
    
    # 测试 Agent v2 (新) - 使用复用
    print("\n" + "=" * 70)
    print("Agent v2 (新) - 使用方案复用 + 效果追踪")
    print("=" * 70)
    
    stats_v2 = test_agent("Agent v2", problems, use_reuse=True)
    
    # 对比结果
    print("\n" + "=" * 70)
    print("对比结果")
    print("=" * 70)
    
    print(f"""
┌─────────────────┬─────────────┬─────────────┐
│ 指标            │ Agent v1    │ Agent v2    │
├─────────────────┼─────────────┼─────────────┤
│ 复用率          │ {stats_v1['reuse_rate']:>8.1%}   │ {stats_v2['reuse_rate']:>8.1%}   │
│ 平均成功率      │ {stats_v1['success_rate']:>8.1%}   │ {stats_v2['success_rate']:>8.1%}   │
│ 总方案数        │ {stats_v1['total']:>8}   │ {stats_v2['total']:>8}   │
└─────────────────┴─────────────┴─────────────┘
""")
    
    # 综合评分
    score_v1 = stats_v1['success_rate'] * 50 + stats_v1['reuse_rate'] * 50
    score_v2 = stats_v2['success_rate'] * 50 + stats_v2['reuse_rate'] * 50
    
    print(f"""
综合评分 (成功率 50% + 复用率 50%):
  Agent v1: {score_v1:.1f} / 100
  Agent v2: {score_v2:.1f} / 100
""")
    
    if score_v2 > score_v1:
        print("🏆 获胜者：Agent v2 (新)")
        print(f"   优势：{score_v2 - score_v1:.1f} 分")
        print(f"   复用率提升：{(stats_v2['reuse_rate'] - stats_v1['reuse_rate']) * 100:.1f}%")
    else:
        print("🏆 获胜者：Agent v1 (旧)")
    
    print("\n✅ 测试完成!")
    print()


if __name__ == '__main__':
    main()
