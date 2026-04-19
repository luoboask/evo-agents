#!/usr/bin/env python3
"""
主动学习触发器 - 检测到模式时自动触发学习

功能:
- 检测重复问题（触发知识整理）
- 检测 Bug 修复（触发经验总结）
- 检测新功能（触发文档化）
- 检测性能优化（触发最佳实践）

用法:
    python3 skills/self-evolution/active_learning_trigger.py --agent demo51-agent
"""

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))


class ActiveLearningTrigger:
    """主动学习触发器"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.db_path = Path(f'data/{agent_name}/memory/evolution.db')
        self.memory_path = Path(f'data/{agent_name}/memory/memory_stream.db')
        
        # 触发阈值配置
        self.thresholds = {
            'repeated_question': 3,    # 同样问题出现 3 次 → 触发知识整理
            'bug_fix': 2,              # 同类 Bug 修复 2 次 → 触发经验总结
            'feature_added': 3,         # 类似功能 3 个 → 触发文档化
            'performance_opt': 3,       # 性能优化 3 次 → 触发最佳实践
        }
    
    def check_and_trigger(self) -> list:
        """检查并触发学习"""
        print(f"🔍 检查主动学习触发条件...")
        print("=" * 70)
        
        triggers = []
        
        # 1. 检测重复问题
        repeated = self._detect_repeated_questions()
        if repeated:
            triggers.append({
                'type': 'KNOWLEDGE_ORGANIZATION',
                'reason': f'检测到 {repeated["count"]} 次类似问题：{repeated["topic"]}',
                'action': '整理常见问题解答'
            })
            print(f"  ✅ 触发：{triggers[-1]['reason']}")
        
        # 2. 检测 Bug 修复模式
        bugs = self._detect_bug_pattern()
        if bugs:
            triggers.append({
                'type': 'EXPERIENCE_SUMMARY',
                'reason': f'检测到 {bugs["count"]} 次同类 Bug：{bugs["type"]}',
                'action': '总结 Bug 修复经验'
            })
            print(f"  ✅ 触发：{triggers[-1]['reason']}")
        
        # 3. 检测功能重复
        features = self._detect_feature_duplication()
        if features:
            triggers.append({
                'type': 'DOCUMENTATION',
                'reason': f'检测到 {features["count"]} 个类似功能',
                'action': '创建统一文档'
            })
            print(f"  ✅ 触发：{triggers[-1]['reason']}")
        
        # 4. 检测性能优化
        perfs = self._detect_performance_pattern()
        if perfs:
            triggers.append({
                'type': 'BEST_PRACTICE',
                'reason': f'检测到 {perfs["count"]} 次性能优化',
                'action': '总结最佳实践'
            })
            print(f"  ✅ 触发：{triggers[-1]['reason']}")
        
        if not triggers:
            print("  ⚠️  没有检测到需要触发的学习模式")
        else:
            print(f"\n📊 共触发 {len(triggers)} 个学习任务")
        
        return triggers
    
    def _detect_repeated_questions(self) -> dict:
        """检测重复问题"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取最近的进化事件
        cursor.execute('''
        SELECT description, lesson_learned
        FROM evolution_events
        WHERE event_type IN ('KNOWLEDGE_GAINED', 'TASK_COMPLETED')
        AND timestamp >= datetime('now', '-7 days')
        ''')
        
        events = cursor.fetchall()
        conn.close()
        
        if not events:
            return None
        
        # 提取关键词
        keywords = []
        for desc, lesson in events:
            text = (desc or '') + (lesson or '')
            # 简单分词
            words = [w for w in text if '\u4e00' <= w <= '\u9fff']
            if len(words) >= 2:
                keywords.append(''.join(words[:10]))
        
        # 统计频率
        counter = Counter(keywords)
        for keyword, count in counter.most_common(5):
            if count >= self.thresholds['repeated_question']:
                return {
                    'topic': keyword[:20],
                    'count': count
                }
        
        return None
    
    def _detect_bug_pattern(self) -> dict:
        """检测 Bug 修复模式"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT description, lesson_learned
        FROM evolution_events
        WHERE event_type = 'BUG_FIX'
        AND timestamp >= datetime('now', '-14 days')
        ''')
        
        events = cursor.fetchall()
        conn.close()
        
        if len(events) >= self.thresholds['bug_fix']:
            # 分析 Bug 类型
            bug_types = []
            for desc, lesson in events:
                text = (desc or '') + (lesson or '')
                if 'SQL' in text or '数据库' in text:
                    bug_types.append('数据库')
                elif '缓存' in text or 'Cache' in text:
                    bug_types.append('缓存')
                elif '权限' in text or '认证' in text:
                    bug_types.append('权限')
                else:
                    bug_types.append('其他')
            
            counter = Counter(bug_types)
            most_common = counter.most_common(1)[0]
            
            return {
                'type': most_common[0],
                'count': most_common[1]
            }
        
        return None
    
    def _detect_feature_duplication(self) -> dict:
        """检测功能重复"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT description
        FROM evolution_events
        WHERE event_type = 'FEATURE_ADDED'
        AND timestamp >= datetime('now', '-30 days')
        ''')
        
        events = cursor.fetchall()
        conn.close()
        
        if len(events) >= self.thresholds['feature_added']:
            return {
                'count': len(events)
            }
        
        return None
    
    def _detect_performance_pattern(self) -> dict:
        """检测性能优化模式"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT description, lesson_learned
        FROM evolution_events
        WHERE event_type = 'CODE_IMPROVED'
        AND (description LIKE '%性能%' OR lesson_learned LIKE '%性能%'
             OR description LIKE '%优化%' OR lesson_learned LIKE '%优化%')
        AND timestamp >= datetime('now', '-14 days')
        ''')
        
        events = cursor.fetchall()
        conn.close()
        
        if len(events) >= self.thresholds['performance_opt']:
            return {
                'count': len(events)
            }
        
        return None
    
    def execute_trigger(self, trigger: dict):
        """执行触发的学习任务"""
        print(f"\n🎯 执行学习任务：{trigger['type']}")
        print(f"   原因：{trigger['reason']}")
        print(f"   行动：{trigger['action']}")
        
        # 记录到进化事件
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO evolution_events (timestamp, event_type, description, lesson_learned)
        VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            'EVOLUTION_TRIGGERED',
            trigger['reason'],
            trigger['action']
        ))
        
        conn.commit()
        conn.close()
        
        print(f"   ✅ 学习任务已记录")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='主动学习触发器')
    parser.add_argument('--agent', type=str, default='demo51-agent', help='Agent 名称')
    parser.add_argument('--execute', action='store_true', help='执行触发的学习任务')
    
    args = parser.parse_args()
    
    trigger = ActiveLearningTrigger(args.agent)
    triggers = trigger.check_and_trigger()
    
    if args.execute and triggers:
        print("\n" + "=" * 70)
        print("执行触发的学习任务...")
        print("=" * 70)
        for t in triggers:
            trigger.execute_trigger(t)


if __name__ == '__main__':
    main()
