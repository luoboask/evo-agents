#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evolution_strategy.py - 进化策略配置

功能:
- 定义 4 种进化策略（balanced/innovate/harden/repair-only）
- 通过环境变量配置策略
- 提供策略选择和权重查询

策略说明:
| 策略 | 创新% | 优化% | 修复% | 适用场景 |
|------|-------|-------|-------|----------|
| balanced (默认) | 50% | 30% | 20% | 日常运行，稳步成长 |
| innovate | 80% | 15% | 5% | 系统稳定，快速出新功能 |
| harden | 20% | 40% | 40% | 大改动后，聚焦稳固 |
| repair-only | 0% | 20% | 80% | 紧急修复模式 |

用法:
    from evolution_strategy import get_strategy, get_intent_priority
    
    # 获取当前策略
    strategy = get_strategy()
    print(strategy)  # {'innovate': 0.5, 'optimize': 0.3, 'repair': 0.2, ...}
    
    # 获取意图优先级（用于决策）
    priorities = get_intent_priority()
    print(priorities)  # ['innovate', 'optimize', 'repair']
    
环境变量:
    EVOLUTION_STRATEGY: 策略名称 (balanced/innovate/harden/repair-only)
"""

import os
from typing import Dict, List


# 策略定义
STRATEGIES = {
    'balanced': {
        'innovate': 0.50,
        'optimize': 0.30,
        'repair': 0.20,
        'description': '日常运行，稳步成长',
    },
    'innovate': {
        'innovate': 0.80,
        'optimize': 0.15,
        'repair': 0.05,
        'description': '系统稳定，快速出新功能',
    },
    'harden': {
        'innovate': 0.20,
        'optimize': 0.40,
        'repair': 0.40,
        'description': '大改动后，聚焦稳固',
    },
    'repair-only': {
        'innovate': 0.00,
        'optimize': 0.20,
        'repair': 0.80,
        'description': '紧急修复模式',
    },
}


def get_strategy_name() -> str:
    """获取当前策略名称"""
    return os.getenv('EVOLUTION_STRATEGY', 'balanced').lower()


def get_strategy() -> Dict[str, float]:
    """
    获取当前策略配置
    
    Returns:
        {'innovate': 0.5, 'optimize': 0.3, 'repair': 0.2, 'description': '...'}
    """
    name = get_strategy_name()
    return STRATEGIES.get(name, STRATEGIES['balanced']).copy()


def get_intent_priority() -> List[str]:
    """
    获取意图优先级列表（按权重降序）
    
    Returns:
        ['innovate', 'optimize', 'repair']  # 按权重从高到低排序
    """
    strategy = get_strategy()
    # 排除 description
    weights = {k: v for k, v in strategy.items() if k != 'description'}
    # 按权重降序排序
    sorted_intents = sorted(weights.keys(), key=lambda x: weights[x], reverse=True)
    return sorted_intents


def should_prioritize_intent(intent: str) -> bool:
    """
    判断是否应该优先处理某个意图（权重 > 0.4）
    
    Args:
        intent: 意图名称 (innovate/optimize/repair)
    
    Returns:
        True if this intent should be prioritized
    """
    strategy = get_strategy()
    return strategy.get(intent, 0.0) > 0.4


def get_available_strategies() -> Dict[str, Dict]:
    """获取所有可用策略"""
    return STRATEGIES.copy()


def main():
    """命令行工具"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='进化策略配置工具')
    parser.add_argument('--show', action='store_true', help='显示当前策略')
    parser.add_argument('--list', action='store_true', help='列出所有策略')
    parser.add_argument('--priority', action='store_true', help='显示意图优先级')
    
    args = parser.parse_args()
    
    if args.show:
        name = get_strategy_name()
        strategy = get_strategy()
        print(f'当前策略：{name}')
        print(f'描述：{strategy.get("description", "N/A")}')
        print(f'配置:')
        for intent in ['innovate', 'optimize', 'repair']:
            weight = strategy.get(intent, 0.0)
            bar = '█' * int(weight * 20)
            print(f'  {intent:10s} {weight:5.1%} {bar}')
    
    elif args.list:
        strategies = get_available_strategies()
        print('可用策略:')
        for name, config in strategies.items():
            current = ' (当前)' if name == get_strategy_name() else ''
            print(f'  {name}{current}: {config["description"]}')
    
    elif args.priority:
        priorities = get_intent_priority()
        print('意图优先级（从高到低）:')
        strategy = get_strategy()
        for i, intent in enumerate(priorities, 1):
            weight = strategy.get(intent, 0.0)
            print(f'  {i}. {intent} ({weight:.1%})')
    
    else:
        parser.print_help()
        print()
        print('环境变量:')
        print('  EVOLUTION_STRATEGY=balanced   # 默认策略')
        print('  EVOLUTION_STRATEGY=innovate   # 创新优先')
        print('  EVOLUTION_STRATEGY=harden     # 稳固优先')
        print('  EVOLUTION_STRATEGY=repair-only  # 仅修复')


if __name__ == '__main__':
    main()
