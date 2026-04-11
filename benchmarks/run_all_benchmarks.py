#!/usr/bin/env python3
"""
运行所有基准测试

一键执行完整的基准测试套件
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_test(script_name: str, args: list = None) -> bool:
    """
    运行单个测试脚本
    
    Args:
        script_name: 脚本名称
        args: 额外参数
    
    Returns:
        是否成功
    """
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ 脚本不存在：{script_path}")
        return False
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    print(f"\n{'='*60}")
    print(f"🧪 运行测试：{script_name}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd)
    return result.returncode == 0


def generate_report(all_results: dict):
    """生成 Markdown 报告"""
    report = f"""# evo-agents 基准测试报告

**测试时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 总览

| 测试 | 状态 | Recall@5 | Recall@10 | NDCG@5 |
|------|------|----------|-----------|--------|
"""
    
    for test_name, result in all_results.items():
        status = "✅" if result.get('success', False) else "❌"
        recall5 = f"{result.get('recall@5', 0):.1%}" if result.get('recall@5') else "N/A"
        recall10 = f"{result.get('recall@10', 0):.1%}" if result.get('recall@10') else "N/A"
        ndcg5 = f"{result.get('ndcg@5', 0):.3f}" if result.get('ndcg@5') else "N/A"
        
        report += f"| {test_name} | {status} | {recall5} | {recall10} | {ndcg5} |\n"
    
    report += f"""
## 详细说明

详见各测试脚本的输出文件。

## 历史对比

运行以下命令生成历史对比报告：

```bash
python3 benchmarks/compare.py --baseline last_week --current this_week
```
"""
    
    # 保存报告
    report_file = Path(__file__).parent / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n💾 报告已保存：{report_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='运行所有基准测试')
    parser.add_argument('--agent', type=str, default='test-agent', help='Agent 名称')
    parser.add_argument('--limit', type=int, default=None, help='限制测试问题数量')
    parser.add_argument('--test', type=str, nargs='*', help='指定运行的测试（默认全部）')
    parser.add_argument('--report', action='store_true', help='生成报告')
    
    args = parser.parse_args()
    
    print("╔════════════════════════════════════════════════════════╗")
    print("║  evo-agents 基准测试套件                                ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    print(f"📦 Agent: {args.agent}")
    print(f"📊 限制：{args.limit if args.limit else '全部'}")
    print()
    
    # 定义测试套件
    tests = {
        'longmemeval': 'longmemeval_test.py',
        # 可以添加更多测试
        # 'memory_search': 'memory_search_test.py',
        # 'fractal_thinking': 'fractal_thinking_test.py',
        # 'knowledge_graph': 'knowledge_graph_test.py',
    }
    
    # 选择要运行的测试
    if args.test:
        tests = {k: v for k, v in tests.items() if k in args.test}
    
    # 运行测试
    all_results = {}
    
    for test_name, script in tests.items():
        success = run_test(script, ['--agent', args.agent])
        all_results[test_name] = {'success': success}
    
    # 生成报告
    if args.report:
        generate_report(all_results)
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试完成总结")
    print("="*60)
    
    success_count = sum(1 for r in all_results.values() if r['success'])
    total_count = len(all_results)
    
    print(f"成功：{success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查输出")


if __name__ == '__main__':
    main()
