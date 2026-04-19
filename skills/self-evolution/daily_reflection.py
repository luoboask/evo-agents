#!/usr/bin/env python3
"""
每日深度反思系统 - Daily Deep Reflection
每天深度分析、提取模式、生成洞察
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict


class DailyReflection:
    """每日深度反思"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 反思历史
        self.reflection_history = []
        
        # 深度分析结果
        self.deep_insights = []
    
    def perform_daily_reflection(self) -> dict:
        """执行每日深度反思"""
        print("=" * 70)
        print("🌙 每日深度反思")
        print("=" * 70)
        print(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
        print()
        
        reflection = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            'analysis': {},
            'insights': [],
            'improvements': [],
            'goals': []
        }
        
        # Step 1: 收集今日数据
        print("1️⃣ 收集今日数据...")
        today_data = self._collect_today_data()
        reflection['analysis']['data_summary'] = today_data
        print(f"   学习次数：{today_data.get('learning_count', 0)}")
        print(f"   交互次数：{today_data.get('interaction_count', 0)}")
        print(f"   进化检查：{today_data.get('evolution_checks', 0)}")
        print()
        
        # Step 2: 模式识别
        print("2️⃣ 模式识别...")
        patterns = self._identify_patterns(today_data)
        reflection['analysis']['patterns'] = patterns
        print(f"   发现模式：{len(patterns)} 个")
        for pattern in patterns[:3]:
            print(f"     - {pattern.get('description', 'N/A')}")
        print()
        
        # Step 3: 深度洞察
        print("3️⃣ 生成深度洞察...")
        insights = self._generate_insights(patterns)
        reflection['insights'] = insights
        print(f"   生成洞察：{len(insights)} 个")
        for insight in insights[:3]:
            print(f"     - {insight.get('description', 'N/A')[:60]}...")
        print()
        
        # Step 4: 改进建议
        print("4️⃣ 制定改进建议...")
        improvements = self._suggest_improvements(insights)
        reflection['improvements'] = improvements
        print(f"   改进建议：{len(improvements)} 个")
        for imp in improvements[:3]:
            print(f"     - {imp.get('action', 'N/A')[:60]}...")
        print()
        
        # Step 5: 明日目标
        print("5️⃣ 设定明日目标...")
        goals = self._set_goals(improvements)
        reflection['goals'] = goals
        print(f"   明日目标：{len(goals)} 个")
        for goal in goals:
            print(f"     - {goal.get('description', 'N/A')}")
        print()
        
        # 保存反思结果
        self._save_reflection(reflection)
        self.reflection_history.append(reflection)
        
        print("=" * 70)
        print("✅ 每日反思完成")
        print("=" * 70)
        
        return reflection
    
    def _collect_today_data(self) -> dict:
        """收集今日数据"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        data = {
            'learning_count': 0,
            'interaction_count': 0,
            'evolution_checks': 0,
            'success_rate': 0.0,
            'learning_types': defaultdict(int)
        }
        
        # 读取定时学习记录
        learning_file = self.learning_dir / f'scheduled_learning_{today}.jsonl'
        if learning_file.exists():
            with open(learning_file, 'r') as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        data['learning_count'] += 1
                        data['learning_types'][record.get('type', 'unknown')] += 1
                        if record.get('outcome') == 'success':
                            data['success_rate'] += 1
        
        # 读取进化检查记录
        evo_file = self.learning_dir / 'evolution_checks.jsonl'
        if evo_file.exists():
            with open(evo_file, 'r') as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        if record.get('timestamp', '').startswith(today):
                            data['evolution_checks'] += 1
        
        # 计算成功率
        if data['learning_count'] > 0:
            data['success_rate'] /= data['learning_count']
        
        # 转换为普通字典
        data['learning_types'] = dict(data['learning_types'])
        
        return data
    
    def _identify_patterns(self, data: dict) -> List[dict]:
        """识别模式"""
        patterns = []
        
        # 学习频率模式
        if data.get('learning_count', 0) >= 10:
            patterns.append({
                'type': 'high_frequency',
                'description': '学习频率高，知识积累快',
                'confidence': 0.9
            })
        
        # 成功率模式
        if data.get('success_rate', 0) >= 0.9:
            patterns.append({
                'type': 'high_success',
                'description': '学习成功率高，方法有效',
                'confidence': 0.85
            })
        
        # 学习类型模式
        learning_types = data.get('learning_types', {})
        if learning_types.get('realtime', 0) > learning_types.get('deep', 0):
            patterns.append({
                'type': 'realtime_focused',
                'description': '偏重实时学习，即时反馈好',
                'confidence': 0.75
            })
        
        # 进化检查模式
        if data.get('evolution_checks', 0) >= 3:
            patterns.append({
                'type': 'self_aware',
                'description': '自我检查频繁，元认知能力强',
                'confidence': 0.8
            })
        
        return patterns
    
    def _generate_insights(self, patterns: List[dict]) -> List[dict]:
        """生成深度洞察"""
        insights = []
        
        for pattern in patterns:
            if pattern['type'] == 'high_frequency':
                insights.append({
                    'level': 'strategic',
                    'description': '高频学习带来快速成长，但需要注意知识消化',
                    'evidence': pattern['description'],
                    'impact': 'high'
                })
            
            elif pattern['type'] == 'high_success':
                insights.append({
                    'level': 'tactical',
                    'description': '当前学习方法有效，可以继续保持',
                    'evidence': pattern['description'],
                    'impact': 'medium'
                })
            
            elif pattern['type'] == 'realtime_focused':
                insights.append({
                    'level': 'tactical',
                    'description': '实时学习能力强，但需要加强深度学习',
                    'evidence': pattern['description'],
                    'impact': 'medium'
                })
            
            elif pattern['type'] == 'self_aware':
                insights.append({
                    'level': 'meta',
                    'description': '元认知能力突出，能够持续自我优化',
                    'evidence': pattern['description'],
                    'impact': 'high'
                })
        
        # 添加通用洞察
        if len(patterns) >= 3:
            insights.append({
                'level': 'strategic',
                'description': '多维度发展模式健康，各方面能力均衡',
                'evidence': f'发现{len(patterns)}个模式',
                'impact': 'high'
            })
        
        return insights
    
    def _suggest_improvements(self, insights: List[dict]) -> List[dict]:
        """制定改进建议"""
        improvements = []
        
        for insight in insights:
            if '实时学习' in insight.get('description', '') and '深度学习' in insight.get('description', ''):
                improvements.append({
                    'priority': 'high',
                    'area': 'learning_balance',
                    'action': '增加深度学习比例，从 20% 提升到 40%',
                    'expected_impact': '+0.2 智能点'
                })
            
            if '高频学习' in insight.get('description', ''):
                improvements.append({
                    'priority': 'medium',
                    'area': 'knowledge_digestion',
                    'action': '增加知识整理时间，每日 15 分钟',
                    'expected_impact': '提高知识留存率'
                })
            
            if '元认知' in insight.get('description', ''):
                improvements.append({
                    'priority': 'low',
                    'area': 'meta_cognition',
                    'action': '保持当前反思频率，已很优秀',
                    'expected_impact': '维持优势'
                })
        
        # 默认改进建议
        if not improvements:
            improvements.append({
                'priority': 'medium',
                'area': 'general',
                'action': '继续保持当前学习节奏',
                'expected_impact': '稳定提升'
            })
        
        return improvements
    
    def _set_goals(self, improvements: List[dict]) -> List[dict]:
        """设定明日目标"""
        goals = []
        
        for imp in improvements:
            if imp['priority'] == 'high':
                goals.append({
                    'priority': 'high',
                    'description': f"重点改进：{imp['area']}",
                    'action': imp['action'],
                    'measurable': True
                })
        
        # 添加常规目标
        goals.append({
            'priority': 'medium',
            'description': '保持定时学习频率',
            'action': '每小时学习 1 次',
            'measurable': True
        })
        
        goals.append({
            'priority': 'low',
            'description': '记录创造性发现',
            'action': '至少 1 个新发现',
            'measurable': True
        })
        
        return goals
    
    def _save_reflection(self, reflection: dict):
        """保存反思结果"""
        today = datetime.now().strftime('%Y-%m-%d')
        file = self.learning_dir / f'daily_reflection_{today}.json'
        with open(file, 'w') as f:
            json.dump(reflection, f, indent=2, ensure_ascii=False)
        
        # 同时追加到汇总文件
        summary_file = self.learning_dir / 'daily_reflections.jsonl'
        with open(summary_file, 'a') as f:
            f.write(json.dumps(reflection, ensure_ascii=False) + '\n')
    
    def get_reflection_summary(self, days: int = 7) -> dict:
        """获取反思摘要"""
        recent = self.reflection_history[-days:] if self.reflection_history else []
        
        if not recent:
            return {'message': '暂无反思记录'}
        
        summary = {
            'total_reflections': len(recent),
            'total_insights': sum(len(r.get('insights', [])) for r in recent),
            'total_improvements': sum(len(r.get('improvements', [])) for r in recent),
            'common_patterns': [],
            'trend': 'stable'
        }
        
        # 统计常见模式
        pattern_counts = defaultdict(int)
        for reflection in recent:
            for pattern in reflection.get('analysis', {}).get('patterns', []):
                pattern_counts[pattern.get('type', 'unknown')] += 1
        
        summary['common_patterns'] = sorted(
            pattern_counts.items(),
            key=lambda x: -x[1]
        )[:5]
        
        return summary


# 使用示例
if __name__ == '__main__':
    reflection = DailyReflection()
    
    # 执行每日反思
    result = reflection.perform_daily_reflection()
    
    # 显示摘要
    print("\n📊 反思摘要:")
    summary = reflection.get_reflection_summary()
    print(f"   总反思次数：{summary.get('total_reflections', 0)}")
    print(f"   总洞察数：{summary.get('total_insights', 0)}")
    print(f"   总改进数：{summary.get('total_improvements', 0)}")
