# -*- coding: utf-8 -*-
"""
智能触发器 - 事件驱动 + Cron 双触发

功能:
1. 事件驱动触发（新记忆/失败/低质量）
2. Cron 定时触发（保底）
3. 优先级队列（避免同时触发）
4. 整合 active_learning_trigger
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.memory_hub import MemoryHub


class SmartTriggers:
    """智能触发器"""
    
    def __init__(self, agent_name: str = "default"):
        self.agent_name = agent_name
        self.hub = MemoryHub(agent_name=agent_name)
        
        # 触发器配置
        self.config = {
            'new_memory_threshold': 10,  # 新记忆达到 10 条 → 触发整理
            'failure_threshold': 3,       # 失败 3 次 → 触发改进
            'low_quality_threshold': 0.5, # 质量分 < 0.5 → 触发优化
            'cooldown_minutes': 30        # 冷却时间（避免频繁触发）
        }
        
        # 上次触发时间
        self.last_trigger = {}
        
        print(f"⚡ 智能触发器已初始化")
        print(f"   Agent: {agent_name}")
    
    def check_triggers(self) -> List[Dict]:
        """检查所有触发器"""
        triggers = []
        
        # 1. 检查新记忆触发
        if self._should_trigger('new_memory'):
            new_memories = self._check_new_memories()
            if new_memories:
                triggers.append(new_memories)
        
        # 2. 检查失败触发
        if self._should_trigger('failure'):
            failure = self._check_failures()
            if failure:
                triggers.append(failure)
        
        # 3. 检查低质量触发
        if self._should_trigger('low_quality'):
            low_quality = self._check_low_quality()
            if low_quality:
                triggers.append(low_quality)
        
        # 4. 整合主动学习触发器
        if self._should_trigger('active_learning'):
            active = self._check_active_learning()
            if active:
                triggers.append(active)
        
        return triggers
    
    def _should_trigger(self, trigger_type: str) -> bool:
        """检查是否应该触发（冷却时间）"""
        now = datetime.now()
        last = self.last_trigger.get(trigger_type)
        
        if last:
            cooldown = self.config['cooldown_minutes'] * 60
            if (now - last).total_seconds() < cooldown:
                return False
        
        return True
    
    def _check_new_memories(self) -> Optional[Dict]:
        """检查新记忆触发"""
        # 获取今天的记忆数量
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 简化：检查记忆数量
        stats = self.hub.storage.get_stats()
        total = stats.get('total_memories', 0)
        
        if total >= self.config['new_memory_threshold']:
            self.last_trigger['new_memory'] = datetime.now()
            
            return {
                'type': 'NEW_MEMORIES',
                'reason': f'新记忆达到{total}条',
                'action': '整理记忆，提取模式',
                'priority': 'medium'
            }
        
        return None
    
    def _check_failures(self) -> Optional[Dict]:
        """检查失败触发"""
        # 简化：从 effect_tracker 获取失败次数
        # 实际实现需要查询数据库
        
        # 示例：假设有失败
        failure_count = 0  # TODO: 实际查询
        
        if failure_count >= self.config['failure_threshold']:
            self.last_trigger['failure'] = datetime.now()
            
            return {
                'type': 'FAILURES',
                'reason': f'失败{failure_count}次',
                'action': '搜索改进方案',
                'priority': 'high'
            }
        
        return None
    
    def _check_low_quality(self) -> Optional[Dict]:
        """检查低质量触发"""
        # 简化：检查低质量内容
        # 实际实现需要查询 knowledge 或 memories
        
        low_quality_count = 0  # TODO: 实际查询
        
        if low_quality_count > 0:
            self.last_trigger['low_quality'] = datetime.now()
            
            return {
                'type': 'LOW_QUALITY',
                'reason': f'发现{low_quality_count}条低质量内容',
                'action': '优化或归档',
                'priority': 'medium'
            }
        
        return None
    
    def _check_active_learning(self) -> Optional[Dict]:
        """检查主动学习触发"""
        try:
            from libs.self_evolution.active_learning_trigger import ActiveLearningTrigger
            
            trigger = ActiveLearningTrigger(agent_name=self.agent_name)
            triggers = trigger.check_and_trigger()
            
            if triggers:
                self.last_trigger['active_learning'] = datetime.now()
                
                return {
                    'type': 'ACTIVE_LEARNING',
                    'reason': f'检测到{len(triggers)}个学习机会',
                    'action': '执行学习任务',
                    'priority': 'low',
                    'details': triggers
                }
        except Exception as e:
            print(f"⚠️  主动学习检查失败：{e}")
        
        return None
    
    def execute_triggers(self, triggers: List[Dict]):
        """执行触发器"""
        if not triggers:
            print("✅ 无触发任务")
            return
        
        print(f"\n⚡ 执行 {len(triggers)} 个触发任务...")
        
        # 按优先级排序
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        triggers.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 2))
        
        for trigger in triggers:
            print(f"\n📌 执行：{trigger['type']}")
            print(f"   原因：{trigger['reason']}")
            print(f"   动作：{trigger['action']}")
            
            # 执行相应动作
            self._execute_action(trigger)
    
    def _execute_action(self, trigger: Dict):
        """执行触发动作"""
        action = trigger.get('action', '')
        
        if '整理' in action:
            # 触发记忆整理
            print("   → 执行记忆整理...")
            # TODO: 调用整理函数
        
        elif '改进' in action:
            # 触发改进搜索
            print("   → 搜索改进方案...")
            # TODO: 调用搜索函数
        
        elif '优化' in action:
            # 触发优化
            print("   → 执行优化...")
            # TODO: 调用优化函数
        
        elif '学习' in action:
            # 执行学习任务
            print("   → 执行学习任务...")
            # TODO: 调用学习函数


def main():
    """命令行使用"""
    import argparse
    
    parser = argparse.ArgumentParser(description='智能触发器')
    parser.add_argument('--agent', type=str, default='default', help='Agent 名称')
    parser.add_argument('--check', action='store_true', help='只检查不执行')
    
    args = parser.parse_args()
    
    triggers = SmartTriggers(agent_name=args.agent)
    
    # 检查触发器
    trigger_list = triggers.check_triggers()
    
    if args.check:
        # 只检查
        if trigger_list:
            print(f"\n📋 检测到 {len(trigger_list)} 个触发任务:")
            for t in trigger_list:
                print(f"   - {t['type']}: {t['reason']}")
        else:
            print("\n✅ 无触发任务")
    else:
        # 检查并执行
        triggers.execute_triggers(trigger_list)


if __name__ == "__main__":
    main()
