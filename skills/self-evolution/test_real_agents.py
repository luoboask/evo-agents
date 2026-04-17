#!/usr/bin/env python3
"""
真实 Agent 测试

测试 v2 的方案复用能力
"""

import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from self_evolution_real import RealSelfEvolution


class AgentTester:
    """Agent 测试器（v2）"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        
        # 设置 Agent
        os.environ['OPENCLAW_AGENT'] = agent_name
        
        self.evolution = RealSelfEvolution(agent_id=agent_name)
        self.results = []
    
    def test_problem(self, problem: str, problem_type: str = "测试问题"):
        """测试一个问题"""
        
        # v2: 使用方案复用
        solution, source = self.evolution.solve_with_reuse(
            problem=problem,
            problem_type=problem_type,
            solve_func=lambda p: f"解决方案：{p}"
        )
        
        self.results.append({
            'problem': problem,
            'source': source,
            'timestamp': datetime.now()
        })
        
        return solution, source
    
    def mark_feedback(self, problem: str, success: bool):
        """标记反馈"""
        self.evolution.mark_solution_effect(problem, success)
    
    def print_results(self):
        """打印结果"""
        print(f"\n{'='*60}")
        print(f"Agent: {self.agent_name}")
        print(f"{'='*60}")
        
        reused = sum(1 for r in self.results if r['source'] == 'reused')
        new = sum(1 for r in self.results if r['source'] == 'new')
        
        print(f"总问题数：{len(self.results)}")
        print(f"复用方案：{reused}")
        print(f"新方案：{new}")
        print(f"复用率：{reused/len(self.results)*100:.1f}%")
        print(f"{'='*60}\n")


def main():
    """主测试流程"""
    
    print("=" * 60)
    print("🧪 Agent v2.0 测试")
    print("=" * 60)
    
    # 测试问题
    problems = [
        ("API 调用超时", "技术问题"),
        ("数据库连接失败", "技术问题"),
        ("API 响应慢", "技术问题"),
        ("内存泄漏", "技术问题"),
        ("数据库连接超时", "技术问题"),
    ]
    
    # 创建测试器
    tester = AgentTester(agent_name="test-agent")
    
    # 测试每个问题
    print("\n📋 测试问题：")
    for i, (problem, ptype) in enumerate(problems, 1):
        print(f"  {i}. {problem}")
    
    print("\n🔬 执行测试...\n")
    
    for problem, ptype in problems:
        solution, source = tester.test_problem(problem, ptype)
        icon = "♻️" if source == 'reused' else "🆕"
        print(f"  {icon} {problem} → {source}")
    
    # 打印结果
    tester.print_results()
    
    print("✅ 测试完成！")


if __name__ == "__main__":
    main()
