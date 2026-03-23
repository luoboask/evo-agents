#!/usr/bin/env python3
"""
真正的自我进化系统
- 从实际任务执行中学习
- 从代码变更中学习
- 从错误修复中学习
- 从用户反馈中学习
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

class RealSelfEvolution:
    """真实自我进化系统（支持多 Agent 数据隔离）"""
    
    def __init__(self, agent_id: str = None, db_path: str = None):
        self.workspace = Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.memory_dir = self.workspace / 'memory'
        
        if db_path:
            self.evolution_db = Path(db_path)
        elif agent_id:
            # 每个 Agent 独立的进化数据库
            self.evolution_db = self.workspace / 'skills' / 'evolution-workbench' / f'{agent_id}_evolution.db'
        else:
            # 默认数据库
            self.evolution_db = self.workspace / 'skills' / 'evolution-workbench' / 'evolution.db'
        
        self.agent_id = agent_id
        
        # 初始化数据库表
        self._init_db()
        
        if agent_id:
            print(f"📈 进化系统已初始化（Agent: {agent_id}）")
        else:
            print(f"📈 进化系统已初始化（默认）")
        print(f"   数据库：{self.evolution_db}")
    
    def _init_db(self):
        """初始化数据库表"""
        import sqlite3
        with sqlite3.connect(self.evolution_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS evolution_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    instance_id TEXT,
                    event_type TEXT,
                    description TEXT,
                    data TEXT
                )
            ''')
            conn.commit()
        
        # 进化事件类型
        self.event_types = {
            'BUG_FIX': 'Bug 修复',
            'FEATURE_ADDED': '功能新增',
            'CODE_IMPROVED': '代码优化',
            'KNOWLEDGE_GAINED': '知识获取',
            'SKILL_IMPROVED': '技能提升',
            'WORKFLOW_OPTIMIZED': '流程优化'
        }
    
    def record_evolution(self, event_type: str, description: str, 
                        before: str = None, after: str = None,
                        lesson_learned: str = None, files_changed: List[str] = None):
        """
        记录一次真实的进化事件
        
        Args:
            event_type: 事件类型 (BUG_FIX, FEATURE_ADDED, etc.)
            description: 事件描述
            before: 之前的状态/代码
            after: 之后的状态/代码
            lesson_learned: 学到的经验
            files_changed: 修改的文件列表
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'description': description,
            'before': before,
            'after': after,
            'lesson_learned': lesson_learned,
            'files_changed': files_changed or []
        }
        
        # 写入进化日志
        self._write_evolution_log(event)
        
        # 写入数据库
        self._write_to_db(event)
        
        # 如果有经验教训，写入知识库
        if lesson_learned:
            self._write_to_knowledge(event)
        
        return event
    
    def _write_evolution_log(self, event):
        """写入进化日志文件"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.memory_dir / f'evolution_{today}.jsonl'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    
    def _write_to_db(self, event):
        """写入进化数据库"""
        conn = sqlite3.connect(self.evolution_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO evolution_events 
            (timestamp, instance_id, event_type, description, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            event['timestamp'],
            'SELF-EVOL-001',
            event['event_type'],
            event['description'],
            json.dumps(event, ensure_ascii=False)
        ))
        
        conn.commit()
        conn.close()
    
    def _write_to_knowledge(self, event):
        """写入知识库"""
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        
        learning = {
            'timestamp': event['timestamp'],
            'type': '实践学习',
            'content': event['description'],
            'outcome': 'completed',
            '收获': event['lesson_learned'],
            '知识点': event['event_type'],
            'details': {
                'domain': '系统进化',
                'subtopic': event['event_type'],
                'difficulty': '中级',
                'time_spent': '未知'
            }
        }
        
        try:
            kb.add_knowledge(learning)
        except Exception as e:
            print(f"⚠️ 知识库写入失败：{e}")
    
    def get_evolution_history(self, days=7, limit=50):
        """获取进化历史"""
        conn = sqlite3.connect(self.evolution_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM evolution_events 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return events
    
    def get_summary(self):
        """获取进化摘要"""
        conn = sqlite3.connect(self.evolution_db)
        cursor = conn.cursor()
        
        # 总事件数
        cursor.execute('SELECT COUNT(*) FROM evolution_events')
        total = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute('''
            SELECT event_type, COUNT(*) as count 
            FROM evolution_events 
            GROUP BY event_type
        ''')
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_events': total,
            'by_type': by_type
        }


# 使用示例
if __name__ == '__main__':
    evolution = RealSelfEvolution()
    
    # 示例：记录一次真实的进化
    event = evolution.record_evolution(
        event_type='FEATURE_ADDED',
        description='添加了/api/knowledge 端点，支持知识库内容查询',
        before='工作台无法展示知识库内容',
        after='可以通过/api/knowledge 获取 273 条知识记录',
        lesson_learned='RESTful API 设计：新增端点需要在路由中注册，返回数据结构要包含分页和统计信息',
        files_changed=[
            'skills/evolution-workbench/integrated_server.py',
            'skills/self-evolution/knowledge_base.py'
        ]
    )
    
    print(f"✅ 进化事件已记录：{event['description']}")
    print(f"   类型：{event['event_type']}")
    print(f"   经验：{event['lesson_learned']}")
    print(f"   文件：{', '.join(event['files_changed'])}")
