#!/usr/bin/env python3
"""
定时学习系统 - Scheduled Learning
定期自动学习、反思、进化
"""

import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import sys

sys.path.insert(0, str(Path(__file__).parent))
from advanced_learning import AdvancedLearningSystem


class ScheduledLearner:
    """定时学习者"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 学习系统
        self.learning_system = AdvancedLearningSystem(workspace)
        
        # 学习计划 (推荐频率 - 2026-03-19 调整)
        # 适用于 main-agent，降低记忆产生频率
        self.schedule = {
            'realtime': {'interval': 900, 'enabled': True},     # 每 15 分钟实时学习
            'deep': {'interval': 1800, 'enabled': True},        # 每 30 分钟深度学习
            'transfer': {'interval': 3600, 'enabled': True},    # 每 60 分钟迁移学习
            'social': {'interval': 1800, 'enabled': True},      # 每 30 分钟社交学习
            'creative': {'interval': 7200, 'enabled': True},    # 每 120 分钟创造性学习
            'reflection': {'interval': 3600, 'enabled': True}   # 每 60 分钟反思
        }
        
        # main-agent 记忆配置
        self.max_working_memory = 50
        self.importance_threshold = 3.0
        
        # 学习历史
        self.learning_history = []
        
        # 上次学习时间
        self.last_learning = {
            'realtime': datetime.now(),
            'deep': datetime.now(),
            'transfer': datetime.now(),
            'social': datetime.now(),
            'creative': datetime.now(),
            'reflection': datetime.now()
        }
        
        self._load_schedule()
    
    def _load_schedule(self):
        """加载学习计划"""
        schedule_file = self.learning_dir / 'learning_schedule.json'
        if schedule_file.exists():
            with open(schedule_file, 'r') as f:
                saved = json.load(f)
                self.schedule.update(saved.get('schedule', {}))
    
    def _save_schedule(self):
        """保存学习计划"""
        schedule_file = self.learning_dir / 'learning_schedule.json'
        with open(schedule_file, 'w') as f:
            json.dump({
                'schedule': self.schedule,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def should_learn(self, learning_type: str) -> bool:
        """判断是否应该学习"""
        if not self.schedule.get(learning_type, {}).get('enabled', False):
            return False
        
        interval = self.schedule[learning_type]['interval']
        last_time = self.last_learning.get(learning_type, datetime.now())
        
        return (datetime.now() - last_time).total_seconds() >= interval
    
    def learn(self, learning_type: str, interaction: dict = None) -> dict:
        """执行学习"""
        print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] {learning_type.upper()} 学习...")
        
        if interaction is None:
            interaction = self._generate_dummy_interaction()
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'type': learning_type,
            'outcome': 'success'
        }
        
        try:
            if learning_type == 'realtime':
                learned = self.learning_system.realtime_learner.learn_from_interaction(interaction)
                result['details'] = {'lessons': len(learned.get('lessons', []))}
            
            elif learning_type == 'deep':
                learned = self.learning_system.deep_learner.learn_pattern(interaction)
                result['details'] = {'confidence': learned.get('confidence', 0)}
            
            elif learning_type == 'transfer':
                learned = self.learning_system.transfer_learner.transfer_knowledge('general', 'coding')
                result['details'] = {'transferred': len(learned.get('transferred_knowledge', []))}
            
            elif learning_type == 'social':
                learned = self.learning_system.social_learner.learn_from_peer('user', {
                    'type': 'interaction',
                    'content': interaction.get('user_input', '')[:100]
                })
                result['details'] = {'status': learned.get('integration_status')}
            
            elif learning_type == 'creative':
                learned = self.learning_system.creative_learner.make_discovery({
                    'description': f"Pattern discovered at {datetime.now().strftime('%H:%M')}"
                })
                result['details'] = {
                    'novelty': learned.get('novelty_score', 0),
                    'impact': learned.get('impact_score', 0)
                }
            
            elif learning_type == 'reflection':
                learned = self._perform_reflection()
                result['details'] = learned
            
            # 更新上次学习时间
            self.last_learning[learning_type] = datetime.now()
            
            # 记录历史
            self.learning_history.append(result)
            self._save_learning_result(result)
            
            print(f"   ✅ 完成：{result['details']}")
            
        except Exception as e:
            result['outcome'] = 'error'
            result['error'] = str(e)
            print(f"   ❌ 错误：{e}")
        
        return result
    
    def _generate_dummy_interaction(self) -> dict:
        """生成模拟交互（用于定时学习）"""
        interactions = [
            {
                'user_input': '系统运行正常',
                'response': '持续监控中...',
                'outcome': 'success'
            },
            {
                'user_input': '检查学习状态',
                'response': '学习系统运行良好',
                'outcome': 'success'
            },
            {
                'user_input': '继续学习',
                'response': '正在从历史数据中学习...',
                'outcome': 'success'
            }
        ]
        
        import random
        return random.choice(interactions)
    
    def _perform_reflection(self) -> dict:
        """执行反思"""
        reflection = {
            'timestamp': datetime.now().isoformat(),
            'total_learnings': len(self.learning_history),
            'recent_learnings': self.learning_history[-10:] if self.learning_history else [],
            'insights': []
        }
        
        # 生成洞察
        if len(self.learning_history) >= 5:
            reflection['insights'].append('学习频率稳定')
        
        if any(l.get('type') == 'creative' for l in self.learning_history[-10:]):
            reflection['insights'].append('有创造性发现')
        
        return reflection
    
    def _save_learning_result(self, result: dict):
        """保存学习结果"""
        today = datetime.now().strftime('%Y-%m-%d')
        file = self.learning_dir / f'scheduled_learning_{today}.jsonl'
        with open(file, 'a') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    async def run_continuous(self, duration_minutes: int = 60):
        """持续运行定时学习"""
        print("=" * 70)
        print("⏰ 定时学习系统启动")
        print("=" * 70)
        print(f"运行时长：{duration_minutes} 分钟")
        print(f"学习计划：{json.dumps(self.schedule, indent=2)}")
        print()
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        while datetime.now() < end_time:
            # 检查每种学习类型
            for learning_type in self.schedule.keys():
                if self.should_learn(learning_type):
                    self.learn(learning_type)
            
            # 等待 10 秒
            await asyncio.sleep(10)
        
        # 最终报告
        self._generate_final_report()
    
    def _generate_final_report(self):
        """生成最终报告"""
        print()
        print("=" * 70)
        print("📊 定时学习最终报告")
        print("=" * 70)
        
        # 统计
        stats = {
            'total_sessions': len(self.learning_history),
            'by_type': {},
            'success_rate': 0,
            'duration': (datetime.now() - self.last_learning['realtime']).total_seconds()
        }
        
        # 按类型统计
        for result in self.learning_history:
            ltype = result.get('type', 'unknown')
            if ltype not in stats['by_type']:
                stats['by_type'][ltype] = {'count': 0, 'success': 0}
            stats['by_type'][ltype]['count'] += 1
            if result.get('outcome') == 'success':
                stats['by_type'][ltype]['success'] += 1
        
        # 计算成功率
        total_success = sum(t['success'] for t in stats['by_type'].values())
        stats['success_rate'] = total_success / max(1, stats['total_sessions']) * 100
        
        print(f"""
学习统计:
  总学习次数：{stats['total_sessions']}
  成功率：{stats['success_rate']:.1f}%
  运行时长：{stats['duration']:.0f} 秒

按类型:
""")
        
        for ltype, data in stats['by_type'].items():
            print(f"  {ltype}: {data['count']} 次 (成功 {data['success']} 次)")
        
        print()
        print("=" * 70)
        
        # 保存报告
        report_file = self.learning_dir / 'scheduled_learning_report.json'
        with open(report_file, 'w') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"报告已保存：{report_file}")


# 使用示例
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='定时学习系统')
    parser.add_argument('--duration', type=int, default=5, help='运行时长（分钟）')
    parser.add_argument('--continuous', action='store_true', help='持续运行模式')
    args = parser.parse_args()
    
    learner = ScheduledLearner()
    
    if args.continuous:
        # 持续运行
        asyncio.run(learner.run_continuous(args.duration))
    else:
        # 单次学习演示
        print("=" * 70)
        print("⏰ 定时学习演示")
        print("=" * 70)
        print()
        
        # 执行所有类型的学习
        for learning_type in learner.schedule.keys():
            learner.learn(learning_type)
            print()
        
        # 显示统计
        print("=" * 70)
        print("📊 学习统计")
        print("=" * 70)
        print(f"总学习次数：{len(learner.learning_history)}")
        print(f"学习计划：{json.dumps(learner.schedule, indent=2)}")
