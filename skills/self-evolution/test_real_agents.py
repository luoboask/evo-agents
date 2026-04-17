#!/usr/bin/env python3
"""
真实 Agent 对比测试

测试流程:
1. 用 Agent v1 (旧) 回答 5 个问题
2. 用 Agent v2 (新) 回答同样的 5 个问题
3. 对比结果
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 设置环境变量选择 Agent
os.environ['OPENCLAW_AGENT'] = 'agent-test-v1'

sys.path.insert(0, str(Path(__file__).parent))


class AgentTester:
    """Agent 测试器"""
    
    def __init__(self, agent_name: str, use_v2: bool = False):
        self.agent_name = agent_name
        self.use_v2 = use_v2
        
        # 设置 Agent
        os.environ['OPENCLAW_AGENT'] = agent_name
        
        # 导入对应的进化系统
        if use_v2:
            from self_evolution_real import RealSelfEvolution
        else:
            # 临时切换到 v1
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "self_evolution_v1",
                Path(__file__).parent / "self_evolution_real_v1.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            RealSelfEvolution = module.RealSelfEvolution
        
        self.evolution = RealSelfEvolution(agent_id=agent_name)
        self.results = []
    
    def test_problem(self, problem: str, problem_type: str = "测试问题"):
        """测试一个问题"""
        
        if self.use_v2:
            # v2: 使用方案复用
            solution, source = self.evolution.solve_with_reuse(
                problem=problem,
                problem_type=problem_type,
                solve_func=lambda p: f"解决方案：{p}"
            )
        else:
            # v1: 直接记录 (无复用)
            solution = f"解决方案：{problem}"
            source = 'new'
            self.evolution.record_evolution(
                event_type='TEST',
                description=problem,
                lesson_learned=solution
            )
        
        self.results.append({
            'problem': problem,
            'source': source,
            'timestamp': datetime.now()
        })
        
        return solution, source
    
    def mark_feedback(self, problem: str, success: bool):
        """标记反馈"""
        if self.use_v2:
            self.evolution.mark_solution_effect(problem, success)
    
    def get_stats(self):
        """获取统计"""
        if self.use_v2:
            return self.evolution.get_evolution_stats()
        else:
            return self.evolution.get_stats()
    
    def get_reuse_rate(self):
        """计算复用率"""
        if not self.results:
            return 0.0
        reused = sum(1 for r in self.results if r['source'] == 'reused')
        return reused / len(self.results)


def run_real_test():
    """运行真实测试"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "真实 Agent 对比测试" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # 测试问题
    problems = [
        ("API 调用超时", "性能问题"),
        ("API 响应慢", "性能问题"),
        ("数据库连接超时", "性能问题"),
        ("内存泄漏", "代码质量"),
        ("功能需求变更", "功能需求"),
    ]
    
    # 测试 Agent v1 (旧)
    print("=" * 70)
    print("Agent v1 (旧版本) - 无方案复用功能")
    print("=" * 70)
    
    agent_v1 = AgentTester('agent-test-v1', use_v2=False)
    
    for i, (problem, ptype) in enumerate(problems, 1):
        print(f"\n{i}. {problem}")
        solution, source = agent_v1.test_problem(problem, ptype)
        print(f"   来源：{source}")
        print(f"   方案：{solution[:50]}...")
    
    # 标记反馈
    print("\n标记反馈:")
    for problem, _ in problems[:3]:
        agent_v1.mark_feedback(problem, True)
        print(f"  ✅ {problem}")
    
    if len(problems) > 3:
        agent_v1.mark_feedback(problems[3][0], False)
        print(f"  ❌ {problems[3][0]}")
    
    stats_v1 = agent_v1.get_stats()
    reuse_v1 = agent_v1.get_reuse_rate()
    
    print(f"\n统计:")
    print(f"  总方案：{stats_v1.get('total_solutions', stats_v1.get('total_events', 0))}")
    print(f"  复用率：{reuse_v1:.1%}")
    
    # 测试 Agent v2 (新)
    print("\n" + "=" * 70)
    print("Agent v2 (新版本) - 有方案复用功能")
    print("=" * 70)
    
    agent_v2 = AgentTester('agent-test-v2', use_v2=True)
    
    for i, (problem, ptype) in enumerate(problems, 1):
        print(f"\n{i}. {problem}")
        solution, source = agent_v2.test_problem(problem, ptype)
        print(f"   来源：{source}")
        print(f"   方案：{solution[:50]}...")
    
    # 标记反馈
    print("\n标记反馈:")
    for problem, _ in problems[:3]:
        agent_v2.mark_feedback(problem, True)
        print(f"  ✅ {problem}")
    
    if len(problems) > 3:
        agent_v2.mark_feedback(problems[3][0], False)
        print(f"  ❌ {problems[3][0]}")
    
    stats_v2 = agent_v2.get_stats()
    reuse_v2 = agent_v2.get_reuse_rate()
    
    print(f"\n统计:")
    print(f"  总方案：{stats_v2.get('total_solutions', 0)}")
    print(f"  复用率：{reuse_v2:.1%}")
    
    # 对比结果
    print("\n" + "=" * 70)
    print("对比结果")
    print("=" * 70)
    
    print(f"""
┌─────────────────┬─────────────┬─────────────┐
│ 指标            │ Agent v1    │ Agent v2    │
├─────────────────┼─────────────┼─────────────┤
│ 复用率          │ {reuse_v1:>8.1%}   │ {reuse_v2:>8.1%}   │
│ 总方案数        │ {stats_v1.get('total_solutions', stats_v1.get('total_events', 0)):>8}   │ {stats_v2.get('total_solutions', 0):>8}   │
└─────────────────┴─────────────┴─────────────┘
""")
    
    # 综合评分
    score_v1 = reuse_v1 * 100
    score_v2 = reuse_v2 * 100
    
    print(f"""
综合评分 (复用率 × 100):
  Agent v1: {score_v1:.1f} / 100
  Agent v2: {score_v2:.1f} / 100
""")
    
    if score_v2 > score_v1:
        print("🏆 获胜者：Agent v2 (新)")
        print(f"   优势：{score_v2 - score_v1:.1f} 分")
        print(f"   复用率提升：{(reuse_v2 - reuse_v1) * 100:.1f}%")
    else:
        print("🏆 获胜者：Agent v1 (旧)")
    
    print("\n✅ 真实测试完成!")
    print()


if __name__ == '__main__':
    run_real_test()
