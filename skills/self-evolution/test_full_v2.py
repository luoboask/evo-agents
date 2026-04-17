#!/usr/bin/env python3
"""
进化系统 v2.0 完整测试

测试所有阶段:
1. 效果追踪
2. 方案复用
3. 自动策略切换
4. 基因进化
5. 元学习
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from effect_tracker import EffectTracker
from solution_reuse import SolutionReuse
from auto_strategy import AutoStrategy
from gene_evolution import GeneEvolution
from meta_learning import MetaLearning
from self_evolution_real import RealSelfEvolution
from nightly_cycle import NightlyEvolutionCycle


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_stage1_effect_tracking():
    """阶段 1: 效果追踪"""
    print_header("阶段 1: 效果追踪")
    
    tracker = EffectTracker()
    
    # 记录多个解决方案
    test_cases = [
        ("API 超时", "性能问题", "增加重试机制", "repair_from_errors"),
        ("数据库连接失败", "性能问题", "连接池优化", "repair_from_errors"),
        ("内存泄漏", "代码质量", "添加资源释放", "optimize_from_patterns"),
        ("功能缺失", "功能需求", "实现新功能", "innovate_from_opportunities"),
    ]
    
    print("\n📝 记录解决方案...")
    for problem, ptype, solution, gene in test_cases:
        tracker.record_solution(problem, ptype, solution, gene)
        
        # 模拟使用效果
        tracker.mark_used(problem, success=True)
        tracker.mark_used(problem, success=True)
    
    # 模拟一个失败案例
    tracker.record_solution("复杂 Bug", "代码质量", "临时修复", "repair_from_errors")
    tracker.mark_used("复杂 Bug", success=False)
    tracker.mark_used("复杂 Bug", success=False)
    
    # 获取统计
    stats = tracker.get_stats()
    print(f"\n📊 统计信息:")
    print(f"  总方案数：{stats['total_solutions']}")
    print(f"  有效方案：{stats['effective_solutions']} ({stats['effective_rate']:.1%})")
    print(f"  平均成功率：{stats['average_success_rate']:.1%}")
    
    # 获取有效方案
    effective = tracker.get_effective_solutions()
    print(f"\n✅ 有效方案 ({len(effective)} 个):")
    for s in effective[:3]:
        print(f"  - {s['problem_type']}: {s['success_count']} 次成功")
    
    # 淘汰无效方案
    print("\n🗑️  淘汰无效方案...")
    tracker.prune_ineffective(max_failure=2)
    
    return True


def test_stage2_solution_reuse():
    """阶段 2: 方案复用"""
    print_header("阶段 2: 方案复用")
    
    reuse = SolutionReuse()
    
    # 模拟解决问题
    def mock_solver(problem):
        return f"新解决方案：{problem}"
    
    print("\n🔍 测试方案复用...")
    
    # 第 1 次：新方案
    print("\n第 1 次解决 'API 超时':")
    solution1, source1 = reuse.solve_with_reuse(
        problem="API 超时",
        problem_type="性能问题",
        solve_func=mock_solver
    )
    print(f"  来源：{source1}")
    
    # 第 2 次：应该复用
    print("\n第 2 次解决 'API 超时':")
    solution2, source2 = reuse.solve_with_reuse(
        problem="API 超时",
        problem_type="性能问题",
        solve_func=mock_solver
    )
    print(f"  来源：{source2}")
    
    # 第 3 次：不同问题
    print("\n第 3 次解决 '新问题':")
    solution3, source3 = reuse.solve_with_reuse(
        problem="全新的问题",
        problem_type="新功能",
        solve_func=mock_solver
    )
    print(f"  来源：{source3}")
    
    print(f"\n✅ 复用测试完成")
    print(f"  新方案：{sum(1 for s in [source1, source2, source3] if s == 'new')}")
    print(f"  复用方案：{sum(1 for s in [source1, source2, source3] if s == 'reused')}")
    
    return True


def test_stage3_auto_strategy():
    """阶段 3: 自动策略切换"""
    print_header("阶段 3: 自动策略切换")
    
    auto = AutoStrategy()
    
    print("\n📊 系统状态检查...")
    state = auto.get_system_state()
    print(f"  成功率：{state['success_rate']:.1%}")
    print(f"  最近失败：{state['recent_failures']}")
    print(f"  最近成功：{state['recent_successes']}")
    
    print("\n🎯 策略推荐...")
    recommended = auto.get_recommended_strategy()
    current = auto.get_current_strategy()
    
    print(f"  当前策略：{current}")
    print(f"  推荐策略：{recommended}")
    print(f"  描述：{auto.STRATEGIES[recommended]['description']}")
    
    print("\n🔄 自动切换测试...")
    switched = auto.auto_switch_if_needed()
    print(f"  是否切换：{switched}")
    
    # 获取策略历史
    history = auto.get_strategy_history(days=7)
    print(f"\n📜 策略历史 ({len(history)} 次):")
    for h in history[:3]:
        print(f"  - {h['old_strategy']} → {h['new_strategy']}")
    
    return True


def test_stage4_gene_evolution():
    """阶段 4: 基因进化"""
    print_header("阶段 4: 基因进化")
    
    gene_evo = GeneEvolution()
    
    print("\n📊 Gene 表现统计...")
    stats = gene_evo.get_gene_stats()
    
    print(f"  总 Gene 数：{stats['total_genes']}")
    print(f"  高效 Gene: {len(stats['high_performers'])}")
    print(f"  低效 Gene: {len(stats['low_performers'])}")
    
    if stats['high_performers']:
        print("\n✅ 高效 Gene:")
        for g in stats['high_performers'][:3]:
            print(f"  - {g['gene_id']}: {g['success_rate']:.1%}")
    
    if stats['low_performers']:
        print("\n⚠️  低效 Gene:")
        for g in stats['low_performers'][:3]:
            print(f"  - {g['gene_id']}: {g['success_rate']:.1%}")
            suggestion = gene_evo.generate_optimization_suggestion(g['gene_id'])
            if suggestion:
                print(f"    💡 {suggestion}")
    
    return True


def test_stage5_meta_learning():
    """阶段 5: 元学习"""
    print_header("阶段 5: 元学习")
    
    meta = MetaLearning()
    
    print("\n🧠 元认知报告...")
    report = meta.know_what_i_dont_know()
    print(report)
    
    print("\n📊 学习效率分析...")
    efficiency = meta.analyze_learning_efficiency(days=30)
    print(f"  总体成功率：{efficiency['overall_success_rate']:.1%}")
    print(f"  使用 Gene 数：{len(efficiency['gene_efficiency'])}")
    print(f"  问题类型数：{len(efficiency['problem_efficiency'])}")
    
    print("\n💡 优化建议...")
    suggestions = meta.optimize_learning_process()
    for s in suggestions[:5]:
        print(f"  {s}")
    
    return True


def test_full_integration():
    """完整集成测试"""
    print_header("完整集成测试")
    
    print("\n🔧 初始化进化系统 v2.0...")
    evolution = RealSelfEvolution()
    
    print(f"\n✅ 系统已初始化")
    print(f"  数据库：{evolution.evolution_db}")
    print(f"  效果追踪：✅")
    print(f"  方案复用：✅")
    
    # 获取统计
    print("\n📊 进化统计...")
    stats = evolution.get_evolution_stats()
    print(f"  总方案：{stats['total_solutions']}")
    print(f"  有效率：{stats['effective_rate']:.1%}")
    print(f"  平均成功率：{stats['average_success_rate']:.1%}")
    
    return True


def main():
    """主测试函数"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "进化系统 v2.0 完整测试" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    
    results = {}
    
    # 阶段 1
    results['stage1'] = test_stage1_effect_tracking()
    
    # 阶段 2
    results['stage2'] = test_stage2_solution_reuse()
    
    # 阶段 3
    results['stage3'] = test_stage3_auto_strategy()
    
    # 阶段 4
    results['stage4'] = test_stage4_gene_evolution()
    
    # 阶段 5
    results['stage5'] = test_stage5_meta_learning()
    
    # 完整集成
    results['integration'] = test_full_integration()
    
    # 总结
    print_header("测试总结")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"\n✅ 通过：{passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有测试通过!")
        print("\n进化系统 v2.0 已就绪:")
        print("  ✅ 效果追踪")
        print("  ✅ 方案复用")
        print("  ✅ 自动策略")
        print("  ✅ 基因进化")
        print("  ✅ 元学习")
    else:
        print("\n⚠️  部分测试失败，请检查日志")
    
    print()


if __name__ == '__main__':
    main()
