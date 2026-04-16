#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_evolution_system.py - 测试进化事件记录 + 策略配置

演示完整的进化系统工作流程
"""

import sys
from pathlib import Path

# 添加 scripts/core 到路径
sys.path.insert(0, str(Path(__file__).parent))

from evolution_events import EvolutionEventRecorder
from evolution_strategy import get_strategy, get_intent_priority, should_prioritize_intent


def test_recorder():
    """测试事件记录器"""
    print('=' * 60)
    print('📝 测试进化事件记录器')
    print('=' * 60)
    
    recorder = EvolutionEventRecorder('main-agent', Path.cwd())
    
    # 清空测试数据（可选）
    # if recorder.events_file.exists():
    #     recorder.events_file.unlink()
    
    # 模拟进化循环
    test_events = [
        {
            'intent': 'repair',
            'signals': ['log_error', 'errsig:tool_not_found'],
            'blast_radius': {'files': 1, 'lines': 3},
            'outcome': {'status': 'success', 'score': 0.9},
            'genes_used': ['gene_gep_repair_from_errors']
        },
        {
            'intent': 'optimize',
            'signals': ['perf_bottleneck', 'slow_query'],
            'blast_radius': {'files': 2, 'lines': 15},
            'outcome': {'status': 'success', 'score': 0.85},
        },
        {
            'intent': 'innovate',
            'signals': ['user_feature_request'],
            'blast_radius': {'files': 3, 'lines': 50},
            'outcome': {'status': 'success', 'score': 0.95},
        },
        {
            'intent': 'repair',
            'signals': ['log_error'],
            'blast_radius': {'files': 0, 'lines': 0},  # 空转
            'outcome': {'status': 'failed', 'score': 0.0},
        },
    ]
    
    print(f'\n记录 {len(test_events)} 个进化事件...')
    for evt in test_events:
        run_id = recorder.record(**evt)
        print(f'  ✓ {run_id}: {evt["intent"]} - {evt["outcome"]["status"]}')
    
    # 获取统计
    stats = recorder.get_stats()
    print(f'\n📊 统计信息:')
    print(f'  总事件数：{stats["total"]}')
    print(f'  成功率：{stats["success_rate"]:.1%}')
    print(f'  平均变更：{stats["avg_files"]:.1f} 文件 / {stats["avg_lines"]:.1f} 行')
    
    # 信号分析
    analysis = recorder.analyze_signal_frequency()
    print(f'\n🔍 信号分析:')
    print(f'  应抑制信号：{analysis["suppressed_signals"]}')
    print(f'  空转比例：{analysis["empty_cycle_ratio"]:.1%}')
    print(f'  失败比例：{analysis["failure_ratio"]:.1%}')
    
    return recorder


def test_strategy():
    """测试策略配置"""
    print()
    print('=' * 60)
    print('🎯 测试进化策略配置')
    print('=' * 60)
    
    strategy = get_strategy()
    print(f'\n当前策略：{list(strategy.keys())[0] if "description" in strategy else "balanced"}')
    print(f'描述：{strategy.get("description", "N/A")}')
    
    priorities = get_intent_priority()
    print(f'\n意图优先级:')
    for i, intent in enumerate(priorities, 1):
        weight = strategy.get(intent, 0.0)
        print(f'  {i}. {intent} ({weight:.1%})')
    
    print(f'\n优先级判断:')
    for intent in ['innovate', 'optimize', 'repair']:
        prioritized = should_prioritize_intent(intent)
        print(f'  {intent}: {"✓ 优先" if prioritized else "○ 普通"}')


def test_integration():
    """测试集成场景"""
    print()
    print('=' * 60)
    print('🔗 集成场景：根据策略决定进化方向')
    print('=' * 60)
    
    recorder = EvolutionEventRecorder('main-agent', Path.cwd())
    strategy = get_strategy()
    priorities = get_intent_priority()
    
    # 模拟检测到的信号
    detected_signals = ['log_error', 'perf_bottleneck', 'user_feature_request']
    
    print(f'\n检测到信号：{detected_signals}')
    print(f'当前策略优先级：{priorities}')
    
    # 根据策略决定处理顺序
    print(f'\n处理顺序:')
    for i, intent in enumerate(priorities, 1):
        # 根据信号匹配意图
        if intent == 'repair' and 'log_error' in detected_signals:
            print(f'  {i}. {intent} ← 检测到错误信号')
        elif intent == 'optimize' and 'perf_bottleneck' in detected_signals:
            print(f'  {i}. {intent} ← 检测到性能瓶颈')
        elif intent == 'innovate' and 'user_feature_request' in detected_signals:
            print(f'  {i}. {intent} ← 检测到功能请求')
        else:
            print(f'  {i}. {intent} (无匹配信号)')


def main():
    """主函数"""
    print()
    print('╔' + '═' * 58 + '╗')
    print('║' + ' ' * 10 + '进化事件记录 + 策略配置 测试' + ' ' * 16 + '║')
    print('╚' + '═' * 58 + '╝')
    print()
    
    test_recorder()
    test_strategy()
    test_integration()
    
    print()
    print('=' * 60)
    print('✅ 测试完成!')
    print('=' * 60)
    print()
    print('💡 使用方法:')
    print('  # 记录进化事件')
    print('  from evolution_events import EvolutionEventRecorder')
    print('  recorder = EvolutionEventRecorder("main-agent")')
    print('  recorder.record(intent="repair", signals=[...], ...)')
    print()
    print('  # 获取当前策略')
    print('  from evolution_strategy import get_strategy')
    print('  strategy = get_strategy()')
    print()
    print('  # 切换策略')
    print('  export EVOLUTION_STRATEGY=innovate')
    print()


if __name__ == '__main__':
    main()
