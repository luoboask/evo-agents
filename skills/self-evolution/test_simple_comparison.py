#!/usr/bin/env python3
"""
方案复用测试 - 简化版

测试 v2 的核心能力：方案复用
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from self_evolution_real import RealSelfEvolution


def test_reuse(name: str, problems: list):
    """测试方案复用能力"""
    
    print(f"\n{name}:")
    print("-" * 50)
    
    evolution = RealSelfEvolution()
    results = []
    
    for problem, ptype in problems:
        # 使用方案复用
        solution, source = evolution.solve_with_reuse(
            problem=problem,
            problem_type=ptype,
            solve_func=lambda p: f"新方案：{p}"
        )
        
        results.append({
            'problem': problem,
            'source': source
        })
        
        icon = "♻️" if source == 'reused' else "🆕"
        print(f"  {icon} {problem} → {source}")
    
    # 统计
    total = len(results)
    reused = sum(1 for r in results if r['source'] == 'reused')
    
    print(f"\n  总计：{total}个问题")
    print(f"  复用：{reused}个 ({reused/total*100:.0f}%)")
    print(f"  新解：{total - reused}个")
    
    return reused / total * 100


def main():
    """主测试"""
    
    print("=" * 60)
    print("🧪 方案复用测试")
    print("=" * 60)
    
    # 测试问题（包含类似问题）
    problems = [
        ("API 调用超时", "技术问题"),
        ("数据库连接失败", "技术问题"),
        ("API 响应慢", "技术问题"),  # 与第 1 个类似
        ("数据库连接超时", "技术问题"),  # 与第 2 个类似
    ]
    
    print("\n📋 测试问题：")
    for i, (p, t) in enumerate(problems, 1):
        print(f"  {i}. {p}")
    
    # 测试
    reuse_rate = test_reuse("v2.0（带方案复用）", problems)
    
    print(f"\n✅ 复用率：{reuse_rate:.0f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
