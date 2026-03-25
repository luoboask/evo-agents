#!/usr/bin/env python3
"""
知识库系统 - Knowledge Base
基于 SQLite 存储学习内容，支持查询和检索
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

class KnowledgeBase:
    """知识库系统（支持多 Agent 数据隔离）"""
    
    def __init__(self, agent_id: str = None, shared: bool = False, db_path: str = None):
        workspace = Path(__file__).resolve().parents[2]
        memory_dir = workspace / 'memory'
        memory_dir.mkdir(parents=True, exist_ok=True)

        if db_path:
            self.db_path = db_path
        elif shared:
            self.db_path = str(memory_dir / 'knowledge_base_shared.db')
        elif agent_id:
            self.db_path = str(memory_dir / f'{agent_id}_knowledge_base.db')
        else:
            self.db_path = str(memory_dir / 'knowledge_base.db')
        
        self.agent_id = agent_id
        self.shared = shared
        self.init_db()
        
        if agent_id:
            print(f"📚 知识库已初始化（Agent: {agent_id}）")
        elif shared:
            print(f"📚 知识库已初始化（共享模式）")
        else:
            print(f"📚 知识库已初始化（默认）")
        print(f"   数据库：{self.db_path}")
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 知识表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                domain TEXT NOT NULL,
                subtopic TEXT NOT NULL,
                content TEXT NOT NULL,
                insight TEXT NOT NULL,
                thinking TEXT,
                key_point TEXT,
                difficulty TEXT,
                time_spent TEXT,
                learning_type TEXT,
                outcome TEXT,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 知识关联表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_knowledge_id INTEGER,
                to_knowledge_id INTEGER,
                relation_type TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_knowledge_id) REFERENCES knowledge(id),
                FOREIGN KEY (to_knowledge_id) REFERENCES knowledge(id)
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domain ON knowledge(domain)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_subtopic ON knowledge(subtopic)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON knowledge(tags)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON knowledge(created_at)')
        
        conn.commit()
        conn.close()
        print("✅ 知识库数据库已初始化")
    
    def add_knowledge(self, learning):
        """添加知识到知识库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        details = learning.get('details', {})
        tags = json.dumps([
            details.get('domain', ''),
            details.get('subtopic', ''),
            details.get('difficulty', '')
        ], ensure_ascii=False)
        
        cursor.execute('''
            INSERT INTO knowledge 
            (timestamp, domain, subtopic, content, insight, thinking, key_point, difficulty, time_spent, learning_type, outcome, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            learning.get('timestamp'),
            details.get('domain', ''),
            details.get('subtopic', ''),
            learning.get('content', ''),
            learning.get('收获', ''),
            learning.get('思考', ''),
            learning.get('知识点', ''),
            details.get('difficulty', ''),
            details.get('time_spent', ''),
            learning.get('type', ''),
            learning.get('outcome', ''),
            tags
        ))
        
        knowledge_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return knowledge_id
    
    def query_by_domain(self, domain, limit=10):
        """按领域查询知识"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM knowledge 
            WHERE domain = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (domain, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def query_by_subtopic(self, subtopic, limit=10):
        """按子主题查询知识"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM knowledge 
            WHERE subtopic = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (subtopic, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def search(self, keyword, limit=20):
        """搜索知识"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM knowledge 
            WHERE content LIKE ? OR insight LIKE ? OR domain LIKE ? OR subtopic LIKE ?
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_statistics(self):
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 总知识数
        cursor.execute('SELECT COUNT(*) as total FROM knowledge')
        total = cursor.fetchone()['total']
        
        # 按领域统计
        cursor.execute('''
            SELECT domain, COUNT(*) as count 
            FROM knowledge 
            GROUP BY domain 
            ORDER BY count DESC
        ''')
        by_domain = [dict(row) for row in cursor.fetchall()]
        
        # 按难度统计
        cursor.execute('''
            SELECT difficulty, COUNT(*) as count 
            FROM knowledge 
            GROUP BY difficulty 
            ORDER BY 
                CASE difficulty 
                    WHEN '入门' THEN 1 
                    WHEN '初级' THEN 2 
                    WHEN '中级' THEN 3 
                    WHEN '高级' THEN 4 
                    WHEN '专家' THEN 5 
                END
        ''')
        by_difficulty = [dict(row) for row in cursor.fetchall()]
        
        # 最近学习
        cursor.execute('''
            SELECT * FROM knowledge 
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        recent = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total': total,
            'by_domain': by_domain,
            'by_difficulty': by_difficulty,
            'recent': recent
        }
    
    def export_to_json(self, output_path=None):
        """导出为 JSON"""
        if output_path is None:
            output_path = str((Path(__file__).resolve().parents[2] / 'memory' / 'knowledge_base.json'))
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM knowledge ORDER BY created_at DESC')
        knowledge = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'exported_at': datetime.now().isoformat(),
                'total': len(knowledge),
                'knowledge': knowledge
            }, f, ensure_ascii=False, indent=2)
        
        return output_path

# 使用示例
if __name__ == '__main__':
    kb = KnowledgeBase()
    
    print("=" * 80)
    print("📚 知识库系统")
    print("=" * 80)
    
    stats = kb.get_statistics()
    print(f"\n总知识数：{stats['total']}")
    print(f"\n按领域统计:")
    for item in stats['by_domain'][:5]:
        print(f"  - {item['domain']}: {item['count']} 条")
    
    print(f"\n按难度统计:")
    for item in stats['by_difficulty']:
        print(f"  - {item['difficulty']}: {item['count']} 条")
    
    print(f"\n最近学习:")
    for item in stats['recent'][:3]:
        print(f"  - {item['content']}")
    
    print("\n✅ 知识库系统已就绪")
