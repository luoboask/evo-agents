#!/usr/bin/env python3
"""
同步学习事件到 SQLite
将学习系统、进化系统的事件同步到工作台数据库
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'self-evolution-5.0'))


class EventSyncer:
    """事件同步器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.db_path = Path(__file__).parent / 'evolution.db'
        
        # 同步记录
        self.synced_count = 0
        self.sync_log = []
    
    def sync_all(self):
        """同步所有事件"""
        print("=" * 70)
        print("🔄 同步学习事件到 SQLite")
        print("=" * 70)
        print()
        
        # 1. 同步定时学习事件
        print("1️⃣ 同步定时学习事件...")
        self._sync_scheduled_learning()
        print(f"   已同步：{self.synced_count} 个事件")
        print()
        
        # 2. 同步进化检查事件
        print("2️⃣ 同步进化检查事件...")
        self._sync_evolution_checks()
        print(f"   已同步：{self.synced_count} 个事件")
        print()
        
        # 3. 同步每日反思事件
        print("3️⃣ 同步每日反思事件...")
        self._sync_daily_reflections()
        print(f"   已同步：{self.synced_count} 个事件")
        print()
        
        # 4. 显示数据库状态
        print("4️⃣ 数据库状态:")
        self._show_db_status()
        print()
        
        print("=" * 70)
        print("✅ 同步完成")
        print("=" * 70)
        
        return self.sync_log
    
    def _sync_scheduled_learning(self):
        """同步定时学习事件"""
        today = datetime.now().strftime('%Y-%m-%d')
        learning_file = self.learning_dir / f'scheduled_learning_{today}.jsonl'
        
        if not learning_file.exists():
            print(f"   文件不存在：{learning_file}")
            return
        
        with open(learning_file, 'r') as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    self._add_to_db({
                        'timestamp': record.get('timestamp'),
                        'type': f"LEARNING_{record.get('type', 'UNKNOWN').upper()}",
                        'description': f"定时学习：{record.get('type', 'unknown')}",
                        'data': json.dumps(record.get('details', {}), ensure_ascii=False)
                    })
    
    def _sync_evolution_checks(self):
        """同步进化检查事件"""
        evo_file = self.learning_dir / 'evolution_checks.jsonl'
        
        if not evo_file.exists():
            print(f"   文件不存在：{evo_file}")
            return
        
        with open(evo_file, 'r') as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    decision = record.get('decision', 'unknown')
                    self._add_to_db({
                        'timestamp': record.get('timestamp'),
                        'type': 'EVOLUTION_CHECK',
                        'description': f"进化检查：{decision}",
                        'data': json.dumps(record.get('stats', {}), ensure_ascii=False)
                    })
    
    def _sync_daily_reflections(self):
        """同步每日反思事件"""
        today = datetime.now().strftime('%Y-%m-%d')
        reflection_file = self.learning_dir / f'daily_reflection_{today}.json'
        
        if not reflection_file.exists():
            print(f"   文件不存在：{reflection_file}")
            return
        
        with open(reflection_file, 'r') as f:
            reflection = json.load(f)
            
            # 添加反思完成事件
            self._add_to_db({
                'timestamp': reflection.get('timestamp'),
                'type': 'DAILY_REFLECTION',
                'description': f"每日深度反思：{len(reflection.get('insights', []))} 个洞察",
                'data': json.dumps({
                    'insights_count': len(reflection.get('insights', [])),
                    'improvements_count': len(reflection.get('improvements', [])),
                    'goals_count': len(reflection.get('goals', []))
                }, ensure_ascii=False)
            })
            
            # 添加洞察事件
            for insight in reflection.get('insights', [])[:3]:  # 最多 3 个
                self._add_to_db({
                    'timestamp': reflection.get('timestamp'),
                    'type': 'INSIGHT',
                    'description': f"深度洞察：{insight.get('description', '')[:50]}",
                    'data': json.dumps({
                        'level': insight.get('level'),
                        'impact': insight.get('impact')
                    }, ensure_ascii=False)
                })
    
    def _add_to_db(self, event: dict):
        """添加事件到数据库"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 检查是否已存在（避免重复）
                cursor.execute('''
                    SELECT COUNT(*) FROM evolution_events 
                    WHERE timestamp = ? AND event_type = ?
                ''', (event['timestamp'], event['type']))
                
                if cursor.fetchone()[0] > 0:
                    return  # 已存在，跳过
                
                # 插入事件
                cursor.execute('''
                    INSERT INTO evolution_events 
                    (timestamp, instance_id, event_type, description, data)
                    VALUES (?, NULL, ?, ?, ?)
                ''', (
                    event['timestamp'],
                    event['type'],
                    event['description'],
                    event.get('data', '{}')
                ))
                
                conn.commit()
                self.synced_count += 1
                self.sync_log.append(event)
                
        except Exception as e:
            print(f"   ❌ 错误：{e}")
    
    def _show_db_status(self):
        """显示数据库状态"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 总数
            cursor.execute('SELECT COUNT(*) FROM evolution_events')
            total = cursor.fetchone()[0]
            print(f"   总事件数：{total}")
            
            # 按类型统计
            cursor.execute('''
                SELECT event_type, COUNT(*) as count 
                FROM evolution_events 
                GROUP BY event_type 
                ORDER BY count DESC
                LIMIT 5
            ''')
            types = cursor.fetchall()
            print(f"   事件类型分布:")
            for t in types:
                print(f"     - {t[0]}: {t[1]} 个")
            
            # 今日事件
            cursor.execute('''
                SELECT COUNT(*) FROM evolution_events 
                WHERE date(timestamp) = date('now')
            ''')
            today = cursor.fetchone()[0]
            print(f"   今日事件：{today}")


# 使用示例
if __name__ == '__main__':
    syncer = EventSyncer()
    syncer.sync_all()
