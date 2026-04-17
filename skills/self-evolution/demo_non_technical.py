#!/usr/bin/env python3
"""
非技术场景演示：工作流程优化

展示进化系统如何复用生活/工作/学习类的经验
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 确保目录存在
os.makedirs('/Users/dhr/.openclaw/workspace-ai-baby/data/demo-workflow/memory', exist_ok=True)

from self_evolution_real import RealSelfEvolution


def demo_workflow():
    print("=" * 70)
    print("🎬 非技术场景演示：工作流程优化")
    print("=" * 70)
    print()
    
    # 工作/生活类问题
    problems = [
        ("早上起不来，总是迟到", "生活习惯"),
        ("会议太多，没时间工作", "工作效率"),
        ("学习新技能很难坚持", "学习成长"),
        ("邮件太多处理不完", "工作效率"),  # 类似问题
        ("早上闹钟响了起不来", "生活习惯"),  # 类似问题
        ("学编程总是半途而废", "学习成长"),  # 类似问题
    ]
    
    print("📋 测试问题（工作/生活/学习）：")
    for i, (p, t) in enumerate(problems, 1):
        print(f"   {i}. {p} 【{t}】")
    print()
    
    # 初始化 v2
    evolution = RealSelfEvolution(agent_id="demo-workflow")
    
    print("-" * 70)
    print("🟢 v2.0 处理过程")
    print("-" * 70)
    print()
    
    reused_count = 0
    
    for i, (problem, ptype) in enumerate(problems, 1):
        def mock_solve(p):
            # 模拟给出建议
            return f"💡 建议：针对'{p}'的解决方案"
        
        solution, source = evolution.solve_with_reuse(
            problem=problem,
            problem_type=ptype,
            solve_func=mock_solve
        )
        
        if source == 'reused':
            reused_count += 1
            icon = "♻️"
        else:
            icon = "🆕"
        
        print(f"   {i}. {problem}")
        print(f"      → {icon} {source}")
        print()
    
    reuse_rate = (reused_count / len(problems)) * 100
    
    print("-" * 70)
    print("📊 结果统计")
    print("-" * 70)
    print(f"   总问题数：{len(problems)}")
    print(f"   复用方案：{reused_count}")
    print(f"   新方案：{len(problems) - reused_count}")
    print(f"   复用率：{reuse_rate:.0f}%")
    print()
    
    print("💡 关键洞察：")
    print("   - 进化系统不仅适用于技术问题")
    print("   - 工作/生活/学习经验同样可以复用")
    print("   - 语义搜索能识别'早上起不来'和'闹钟响了起不来'是类似问题")
    print("   - 随着经验积累，系统会越来越懂你的习惯和偏好")
    print()
    print("=" * 70)


if __name__ == "__main__":
    demo_workflow()
