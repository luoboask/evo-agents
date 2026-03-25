#!/usr/bin/env python3
"""
Sandbox Evolution Skill

为 sandbox-agent 提供自进化能力
"""

import sys
from pathlib import Path

# 添加自进化系统路径
EVOLUTION_PATH = Path(__file__).parent.parent / 'self-evolution-5.0'
sys.path.insert(0, str(EVOLUTION_PATH))

MEMORY_SEARCH_PATH = Path(__file__).parent.parent / 'memory-search'
sys.path.insert(0, str(MEMORY_SEARCH_PATH))

from evolution import SandboxEvolution

# 导出主要类
__all__ = ['SandboxEvolution']

# 创建全局实例
_evolution_instance = None


def get_evolution():
    """获取或创建 SandboxEvolution 实例"""
    global _evolution_instance
    if _evolution_instance is None:
        _evolution_instance = SandboxEvolution()
    return _evolution_instance


def handle_skill_action(action, params):
    """
    处理 skill 调用
    
    Args:
        action: 动作名称
        params: 参数
    
    Returns:
        执行结果
    """
    evolution = get_evolution()
    
    if action == 'record_event':
        return evolution.record_sandbox_event(
            event_type=params.get('event_type'),
            instance_id=params.get('instance_id'),
            details=params.get('details', {})
        )
    
    elif action == 'learn_from_result':
        return evolution.learn_from_test_result(
            instance_id=params.get('instance_id'),
            test_result=params.get('test_result', {}),
            report=params.get('report', {})
        )
    
    elif action == 'get_suggestions':
        return evolution.get_suggestions_for_requirement(
            requirement_id=params.get('requirement_id')
        )
    
    elif action == 'get_common_bugs':
        return evolution.get_common_bugs_for_requirement_type(
            requirement_type=params.get('requirement_type')
        )
    
    elif action == 'optimize_config':
        return evolution.optimize_sandbox_config(
            instance_id=params.get('instance_id'),
            current_config=params.get('current_config', {}),
            performance_data=params.get('performance_data', {})
        )
    
    elif action == 'get_stats':
        return evolution.get_evolution_stats()
    
    elif action == 'generate_report':
        return evolution.generate_learning_report(
            days=params.get('days', 7)
        )
    
    else:
        return {
            'success': False,
            'error': f'Unknown action: {action}'
        }


# Skill 入口
def main(action, params):
    """
    Skill 主入口
    
    Args:
        action: 动作名称
        params: 参数
    
    Returns:
        执行结果
    """
    try:
        result = handle_skill_action(action, params)
        return {
            'success': True,
            'result': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == '__main__':
    # 测试
    print("Sandbox Evolution Skill")
    print("=" * 70)
    
    evolution = get_evolution()
    
    # 测试记录事件
    print("\n1. 测试记录事件")
    result = main('record_event', {
        'event_type': 'SANDBOX_CREATED',
        'instance_id': 'test-001',
        'details': {'description': '测试沙箱'}
    })
    print(f"   结果：{result}")
    
    # 测试获取建议
    print("\n2. 测试获取建议")
    result = main('get_suggestions', {
        'requirement_id': 'REQ-001'
    })
    print(f"   结果：{result}")
    
    # 测试获取统计
    print("\n3. 测试获取统计")
    result = main('get_stats', {})
    print(f"   结果：{result}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
