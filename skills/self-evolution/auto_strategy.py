#!/usr/bin/env python3
"""
自动策略切换 - 根据系统状态自动调整进化策略

核心功能:
- 实时感知系统状态
- 自动切换策略
- 无需人工干预
"""

import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Tuple


class AutoStrategy:
    """自动策略切换器"""
    
    STRATEGIES = {
        'balanced': {
            'innovate': 0.50, 'optimize': 0.30, 'repair': 0.20,
            'description': '日常运行，稳步成长'
        },
        'innovate': {
            'innovate': 0.80, 'optimize': 0.15, 'repair': 0.05,
            'description': '系统稳定，快速出新功能'
        },
        'harden': {
            'innovate': 0.20, 'optimize': 0.40, 'repair': 0.40,
            'description': '大改动后，聚焦稳固'
        },
        'repair-only': {
            'innovate': 0.00, 'optimize': 0.20, 'repair': 0.80,
            'description': '紧急修复模式'
        }
    }
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Path(__file__).parent / 'evolution_effects.db'
    
    def get_system_state(self, hours: int = 24) -> Dict:
        """获取最近 N 小时的系统状态"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 统计最近效果
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                SUM(CASE WHEN success THEN 0 ELSE 1 END) as failures,
                COUNT(*) as total
            FROM usage_records
            WHERE timestamp > ?
        ''', (cutoff.isoformat(),))
        
        row = cursor.fetchone()
        conn.close()
        
        successes = row[0] or 0
        failures = row[1] or 0
        total = row[2] or 0
        
        success_rate = successes / total if total > 0 else 0.5
        
        return {
            'success_rate': success_rate,
            'recent_failures': failures,
            'recent_successes': successes,
            'total_events': total,
            'time_window_hours': hours
        }
    
    def get_recommended_strategy(self) -> str:
        """根据系统状态推荐策略"""
        state = self.get_system_state(hours=24)
        
        # 紧急修复模式：失败次数多
        if state['recent_failures'] > 5:
            return 'repair-only'
        
        # 创新模式：成功率高
        if state['success_rate'] > 0.8:
            return 'innovate'
        
        # 稳固模式：成功率低
        if state['success_rate'] < 0.5:
            return 'harden'
        
        # 默认：平衡模式
        return 'balanced'
    
    def get_current_strategy(self) -> str:
        """获取当前策略"""
        return os.getenv('EVOLUTION_STRATEGY', 'balanced')
    
    def should_switch_strategy(self) -> Tuple[bool, str, str]:
        """检查是否应该切换策略"""
        current = self.get_current_strategy()
        recommended = self.get_recommended_strategy()
        
        if current != recommended:
            return True, current, recommended
        
        return False, current, current
    
    def switch_strategy(self, new_strategy: str) -> bool:
        """切换策略"""
        if new_strategy not in self.STRATEGIES:
            print(f"❌ 未知策略：{new_strategy}")
            return False
        
        # 设置环境变量
        os.environ['EVOLUTION_STRATEGY'] = new_strategy
        
        # 记录切换事件
        self._log_switch(new_strategy)
        
        print(f"📊 策略切换：{self.get_current_strategy()} → {new_strategy}")
        print(f"   描述：{self.STRATEGIES[new_strategy]['description']}")
        
        return True
    
    def auto_switch_if_needed(self) -> bool:
        """自动切换策略 (如果需要)"""
        should_switch, current, recommended = self.should_switch_strategy()
        
        if should_switch:
            print(f"⚠️  系统状态变化，建议切换策略")
            print(f"   当前：{current}")
            print(f"   推荐：{recommended}")
            
            # 自动切换 (也可改为人工确认)
            return self.switch_strategy(recommended)
        
        return False
    
    def _log_switch(self, new_strategy: str):
        """记录策略切换事件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO strategy_switches 
            (timestamp, old_strategy, new_strategy, reason)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), 
              self.get_current_strategy(),
              new_strategy,
              'auto_switch'))
        
        conn.commit()
        conn.close()
    
    def get_strategy_history(self, days: int = 7) -> list:
        """获取策略切换历史"""
        cutoff = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM strategy_switches 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
        ''', (cutoff.isoformat(),))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'timestamp': row[1],
                'old_strategy': row[2],
                'new_strategy': row[3],
                'reason': row[4]
            }
            for row in rows
        ]


# 集成到 nightly_cycle.py
if __name__ == '__main__':
    auto_strategy = AutoStrategy()
    
    # 每次执行分形思考前检查
    if auto_strategy.auto_switch_if_needed():
        print("✅ 策略已自动切换")
    else:
        print(f"✓ 当前策略合适：{auto_strategy.get_current_strategy()}")
