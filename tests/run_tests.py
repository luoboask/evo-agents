#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evo-agents 测试套件运行器
运行所有测试并生成报告
"""

import sys
import unittest
import argparse
import json
from pathlib import Path
from datetime import datetime
from io import StringIO


def run_tests(test_dir, pattern='test_*.py', verbosity=2):
    """运行测试并返回结果"""
    # 发现测试
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern=pattern)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result


def generate_report(result, output_file=None):
    """生成测试报告"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total': result.testsRun,
        'passed': result.testsRun - len(result.failures) - len(result.errors),
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'success': result.wasSuccessful(),
        'details': {
            'failures': [
                {
                    'test': str(test),
                    'error': traceback
                }
                for test, traceback in result.failures
            ],
            'errors': [
                {
                    'test': str(test),
                    'error': traceback
                }
                for test, traceback in result.errors
            ]
        }
    }
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📊 报告已保存至：{output_file}")
    
    return report


def print_summary(report):
    """打印测试总结"""
    print("\n" + "="*70)
    print("📊 测试总结")
    print("="*70)
    
    total = report['total']
    passed = report['passed']
    failures = report['failures']
    errors = report['errors']
    skipped = report['skipped']
    
    print(f"\n总测试数：{total}")
    
    if passed > 0:
        print(f"✅ 通过：{passed} ({passed/total*100:.1f}%)")
    if failures > 0:
        print(f"❌ 失败：{failures}")
    if errors > 0:
        print(f"⚠️  错误：{errors}")
    if skipped > 0:
        print(f"⏭️  跳过：{skipped}")
    
    print("\n" + "-"*70)
    if report['success']:
        print("🎉 所有测试通过！系统功能正常！")
    else:
        print(f"⚠️  {failures + errors} 个测试失败/错误，请检查")
    print("-"*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description='evo-agents 测试套件运行器')
    parser.add_argument('--test-dir', default=str(Path(__file__).parent), 
                        help='测试目录路径')
    parser.add_argument('--pattern', default='test_*.py', 
                        help='测试文件匹配模式')
    parser.add_argument('--output', '-o', help='输出报告文件路径')
    parser.add_argument('--quiet', '-q', action='store_true', 
                        help='安静模式，只显示总结')
    args = parser.parse_args()
    
    test_dir = Path(args.test_dir)
    if not test_dir.exists():
        print(f"❌ 测试目录不存在：{test_dir}")
        sys.exit(1)
    
    print("\n" + "🧪"*30)
    print(f"  evo-agents 测试套件")
    print(f"  测试目录：{test_dir}")
    print(f"  文件模式：{args.pattern}")
    print(f"  时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🧪"*30 + "\n")
    
    # 运行测试
    verbosity = 1 if args.quiet else 2
    result = run_tests(test_dir, args.pattern, verbosity)
    
    # 生成报告
    report = generate_report(result, args.output)
    
    # 打印总结
    print_summary(report)
    
    # 返回退出码
    sys.exit(0 if report['success'] else 1)


if __name__ == '__main__':
    main()
