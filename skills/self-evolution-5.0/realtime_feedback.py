#!/usr/bin/env python3
"""
实时反馈学习系统 - Real-time Feedback Learning
每次交互后立即收集反馈，实时调整策略
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class RealtimeFeedbackLearner:
    """实时反馈学习器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 用户偏好模型
        self.user_preferences = {
            'response_length': 'medium',  # short/medium/long
            'detail_level': 'high',       # low/medium/high
            'tone': 'professional',       # casual/professional/technical
            'format': 'structured'        # free/structured
        }
        
        # 反馈历史
        self.feedback_history = []
        
        # 策略调整记录
        self.strategy_adjustments = []
        
        self._load_preferences()
    
    def _load_preferences(self):
        """加载用户偏好"""
        pref_file = self.learning_dir / 'user_preferences.json'
        if pref_file.exists():
            with open(pref_file, 'r') as f:
                saved = json.load(f)
                self.user_preferences.update(saved)
    
    def _save_preferences(self):
        """保存用户偏好"""
        pref_file = self.learning_dir / 'user_preferences.json'
        with open(pref_file, 'w') as f:
            json.dump(self.user_preferences, f, indent=2, ensure_ascii=False)
    
    def collect_feedback(self, interaction: dict, feedback: dict) -> dict:
        """
        收集反馈
        
        Args:
            interaction: 交互信息
            feedback: 反馈信息 {
                'satisfaction': 1-5,
                'helpful': bool,
                'too_long': bool,
                'too_short': bool,
                'too_technical': bool,
                'suggestions': str
            }
        """
        print(f"📝 收集反馈：满意度 {feedback.get('satisfaction', 0)}/5")
        
        feedback_record = {
            'timestamp': datetime.now().isoformat(),
            'interaction_id': interaction.get('id', 'unknown'),
            'feedback': feedback,
            'adjustments': []
        }
        
        # 分析反馈
        adjustments = self._analyze_feedback(feedback)
        feedback_record['adjustments'] = adjustments
        
        # 更新用户偏好
        self._update_preferences(feedback, adjustments)
        
        # 保存反馈
        self.feedback_history.append(feedback_record)
        self._save_feedback(feedback_record)
        
        # 应用调整
        self._apply_adjustments(adjustments)
        
        return feedback_record
    
    def _analyze_feedback(self, feedback: dict) -> List[dict]:
        """分析反馈，生成调整建议"""
        adjustments = []
        
        # 满意度分析
        satisfaction = feedback.get('satisfaction', 3)
        if satisfaction <= 2:
            adjustments.append({
                'type': 'quality_alert',
                'priority': 'high',
                'action': '需要改进回答质量',
                'reason': f'满意度 {satisfaction}/5 较低'
            })
        elif satisfaction >= 5:
            adjustments.append({
                'type': 'positive_reinforcement',
                'priority': 'low',
                'action': '保持当前策略',
                'reason': f'满意度 {satisfaction}/5 很高'
            })
        
        # 长度反馈
        if feedback.get('too_long'):
            adjustments.append({
                'type': 'response_length',
                'priority': 'medium',
                'action': '缩短回答',
                'reason': '用户认为回答太长'
            })
            self.user_preferences['response_length'] = 'short'
        
        elif feedback.get('too_short'):
            adjustments.append({
                'type': 'response_length',
                'priority': 'medium',
                'action': '延长回答',
                'reason': '用户认为回答太短'
            })
            self.user_preferences['response_length'] = 'long'
        
        # 技术深度反馈
        if feedback.get('too_technical'):
            adjustments.append({
                'type': 'technical_level',
                'priority': 'medium',
                'action': '降低技术深度',
                'reason': '用户认为太技术化'
            })
            self.user_preferences['tone'] = 'casual'
        
        # 建议处理
        if feedback.get('suggestions'):
            adjustments.append({
                'type': 'user_suggestion',
                'priority': 'high',
                'action': f"实施建议：{feedback['suggestions'][:100]}",
                'reason': '用户明确建议'
            })
        
        return adjustments
    
    def _update_preferences(self, feedback: dict, adjustments: List[dict]):
        """更新用户偏好"""
        # 基于反馈调整偏好
        for adj in adjustments:
            if adj['type'] == 'response_length':
                if '缩短' in adj['action']:
                    self.user_preferences['response_length'] = 'short'
                elif '延长' in adj['action']:
                    self.user_preferences['response_length'] = 'long'
                else:
                    self.user_preferences['response_length'] = 'medium'
            
            elif adj['type'] == 'technical_level':
                if '降低' in adj['action']:
                    self.user_preferences['tone'] = 'casual'
                else:
                    self.user_preferences['tone'] = 'technical'
        
        # 保存偏好
        self._save_preferences()
    
    def _apply_adjustments(self, adjustments: List[dict]):
        """应用调整"""
        for adj in adjustments:
            self.strategy_adjustments.append({
                'timestamp': datetime.now().isoformat(),
                'adjustment': adj
            })
            print(f"   🔧 应用调整：{adj['action']}")
    
    def _save_feedback(self, feedback: dict):
        """保存反馈"""
        today = datetime.now().strftime('%Y-%m-%d')
        file = self.learning_dir / f'feedback_{today}.jsonl'
        with open(file, 'a') as f:
            f.write(json.dumps(feedback, ensure_ascii=False) + '\n')
    
    def get_feedback_statistics(self) -> dict:
        """获取反馈统计"""
        if not self.feedback_history:
            return {
                'total_feedback': 0,
                'avg_satisfaction': 0,
                'trend': 'stable'
            }
        
        satisfactions = [
            f['feedback'].get('satisfaction', 3) 
            for f in self.feedback_history
        ]
        
        avg_sat = sum(satisfactions) / len(satisfactions)
        
        # 计算趋势
        if len(satisfactions) >= 2:
            recent = sum(satisfactions[-5:]) / min(5, len(satisfactions))
            older = sum(satisfactions[:-5]) / max(1, len(satisfactions) - 5)
            if recent > older:
                trend = 'improving'
            elif recent < older:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'total_feedback': len(self.feedback_history),
            'avg_satisfaction': round(avg_sat, 2),
            'trend': trend,
            'adjustments_count': len(self.strategy_adjustments),
            'user_preferences': self.user_preferences
        }
    
    def should_ask_feedback(self, interaction: dict) -> bool:
        """判断是否应该询问反馈"""
        # 简单规则：每 3 次交互询问一次
        today = datetime.now().strftime('%Y-%m-%d')
        today_feedback = sum(
            1 for f in self.feedback_history 
            if f['timestamp'].startswith(today)
        )
        
        # 每天最多询问 5 次
        return today_feedback < 5


# 使用示例
if __name__ == '__main__':
    learner = RealtimeFeedbackLearner()
    
    print("=" * 70)
    print("📝 实时反馈学习演示")
    print("=" * 70)
    print()
    
    # 模拟交互
    interaction = {
        'id': 'interaction-001',
        'user_input': '怎么优化搜索性能？',
        'response': '使用缓存和索引...'
    }
    
    # 模拟反馈
    feedback = {
        'satisfaction': 4,
        'helpful': True,
        'too_long': False,
        'too_short': False,
        'too_technical': False,
        'suggestions': '希望能提供更多代码示例'
    }
    
    # 收集反馈
    result = learner.collect_feedback(interaction, feedback)
    
    print()
    print("📊 反馈统计:")
    stats = learner.get_feedback_statistics()
    print(f"   总反馈数：{stats['total_feedback']}")
    print(f"   平均满意度：{stats['avg_satisfaction']}/5")
    print(f"   趋势：{stats['trend']}")
    print(f"   策略调整：{stats['adjustments_count']} 次")
    print()
    print("用户偏好:")
    for key, value in stats['user_preferences'].items():
        print(f"   {key}: {value}")
