#!/usr/bin/env python3
"""
元规则自动生成器 - 从进化事件自动提取元规则（纯规则，无需 LLM）

用法:
    cd /Users/dhr/.openclaw/workspace-demo51-agent
    PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
      python3 skills/self-evolution/meta_rule_generator.py
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))

from memory_hub.session_storage import SessionMemoryStorage


class MetaRuleGenerator:
    """元规则自动生成器"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.db_path = Path(f'data/{agent_name}/evolution.db')
        self.memory_path = Path(f'data/{agent_name}/memory')
        self.storage = SessionMemoryStorage(self.memory_path)
        
        # 从 lesson_learned 提取元规则的规则
        self.extraction_templates = {
            'BUG_FIX': [
                '修复 Bug 时，{lesson}',
                '遇到问题时，{lesson}',
            ],
            'FEATURE_ADDED': [
                '实现功能时，{lesson}',
                '添加新功能时，{lesson}',
            ],
            'CODE_IMPROVED': [
                '优化代码时，{lesson}',
                '重构时，{lesson}',
            ],
            'KNOWLEDGE_GAINED': [
                '{lesson}',  # 知识类直接保留
            ],
            'TASK_COMPLETED': [
                '完成任务时，{lesson}',
                '实施项目时，{lesson}',
            ],
        }
    
    def generate_meta_rules(self, limit=20):
        """从进化事件自动生成元规则"""
        print(f"🧠 从进化事件生成元规则（最多 {limit} 条）...")
        print("=" * 70)
        
        # 获取进化事件
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT event_type, description, lesson_learned, timestamp
        FROM evolution_events
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (limit,))
        
        events = cursor.fetchall()
        conn.close()
        
        if not events:
            print("⚠️  没有进化事件可分析")
            return []
        
        print(f"📊 分析 {len(events)} 个进化事件...\n")
        
        generated_rules = []
        
        for event in events:
            # 从 lesson_learned 提取元规则
            lesson = event['lesson_learned']
            
            if lesson:
                # 应用提取规则
                meta_rule = self._extract_meta_rule(lesson, event['event_type'])
                
                if meta_rule:
                    generated_rules.append({
                        'rule': meta_rule,
                        'source': event['event_type'],
                        'importance': self._calculate_importance(event['event_type']),
                        'timestamp': event['timestamp']
                    })
                    print(f"  ✅ [{event['event_type']}] {lesson[:50]}... → {meta_rule[:40]}")
        
        # 去重并保存
        unique_rules = self._deduplicate_rules(generated_rules)
        
        print(f"\n📜 保存 {len(unique_rules)} 条元规则到记忆系统...")
        for rule_info in unique_rules:
            self.storage.add_memory(
                session_id=f'meta-rule-auto-{datetime.now().strftime("%Y%m%d")}',
                content=rule_info['rule'],
                memory_type='goal',
                importance=rule_info['importance'],
                tags=['meta_rule', 'auto_generated', rule_info['source']]
            )
        
        print(f"✅ 元规则生成完成！")
        return unique_rules
    
    def _extract_meta_rule(self, lesson: str, event_type: str) -> str:
        """从 lesson 中提取元规则"""
        # 清理
        rule = lesson.strip()
        
        # 根据事件类型添加上下文
        prefixes = {
            'BUG_FIX': '修复 Bug 时，',
            'FEATURE_ADDED': '实现功能时，',
            'CODE_IMPROVED': '优化代码时，',
            'KNOWLEDGE_GAINED': '',  # 知识类不需要前缀
            'TASK_COMPLETED': '完成任务时，',
            'EVOLUTION_CHECK': '系统进化时，',
        }
        
        prefix = prefixes.get(event_type, '')
        
        # 如果 lesson 已经有主语，不加前缀
        if any(rule.startswith(s) for s in ['需要', '必须', '应该', '建议', '使用', '采用']):
            return rule
        
        return prefix + rule
    
    def _calculate_importance(self, event_type: str) -> float:
        """根据事件类型计算重要性"""
        importance_map = {
            'BUG_FIX': 9.5,      # Bug 修复最重要
            'CODE_IMPROVED': 9.0, # 代码改进
            'FEATURE_ADDED': 8.5, # 功能新增
            'KNOWLEDGE_GAINED': 8.5, # 知识获取
            'TASK_COMPLETED': 8.0, # 任务完成
            'EVOLUTION_CHECK': 7.5, # 进化检查
        }
        return importance_map.get(event_type, 8.0)
    
    def _deduplicate_rules(self, rules: list) -> list:
        """去重规则"""
        seen = set()
        unique = []
        
        for rule in rules:
            # 简化规则用于去重比较
            simple = rule['rule'][:30]
            if simple not in seen:
                seen.add(simple)
                unique.append(rule)
        
        return unique


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='元规则自动生成器')
    parser.add_argument('--agent', type=str, default='demo51-agent', help='Agent 名称')
    parser.add_argument('--limit', type=int, default=20, help='分析的进化事件数量')
    
    args = parser.parse_args()
    
    generator = MetaRuleGenerator(args.agent)
    rules = generator.generate_meta_rules(args.limit)
    
    # 打印总结
    print(f"\n📊 总结:")
    print(f"  生成元规则：{len(rules)} 条")
    
    if rules:
        print(f"\n  前 5 条元规则:")
        for i, rule in enumerate(rules[:5], 1):
            print(f"    {i}. [{rule['importance']:.1f}分] {rule['rule']}")


if __name__ == '__main__':
    main()
