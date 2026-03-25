#!/usr/bin/env python3
"""
Evolution Database - SQLite 存储
动态存储所有进化相关数据
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path


class EvolutionDatabase:
    """进化数据库"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent / 'evolution.db'
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 实例表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS instances (
                    id TEXT PRIMARY KEY,
                    requirement_id TEXT,
                    status TEXT,
                    created_at TIMESTAMP,
                    started_at TIMESTAMP,
                    stopped_at TIMESTAMP,
                    config TEXT,
                    port INTEGER,
                    results TEXT
                )
            ''')
            
            # 进化事件表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS evolution_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    instance_id TEXT,
                    event_type TEXT,
                    description TEXT,
                    data TEXT,
                    FOREIGN KEY (instance_id) REFERENCES instances(id)
                )
            ''')
            
            # 指标表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metric_name TEXT,
                    metric_value REAL,
                    labels TEXT
                )
            ''')
            
            # Bug 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bugs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    instance_id TEXT,
                    bug_type TEXT,
                    severity TEXT,
                    description TEXT,
                    fixed BOOLEAN DEFAULT 0,
                    fix_data TEXT,
                    FOREIGN KEY (instance_id) REFERENCES instances(id)
                )
            ''')
            
            # 预测表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    prediction_type TEXT,
                    prediction_text TEXT,
                    confidence INTEGER,
                    action TEXT,
                    fulfilled BOOLEAN DEFAULT 0,
                    fulfilled_at TIMESTAMP
                )
            ''')
            
            # 智能评分历史
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS intelligence_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_score INTEGER,
                    max_score INTEGER,
                    percentage REAL,
                    grade TEXT,
                    dimensions TEXT
                )
            ''')
            
            conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # 实例操作
    # ═══════════════════════════════════════════════════════════
    
    def create_instance(self, instance_id, requirement_id, config, port):
        """创建实例记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO instances (id, requirement_id, status, created_at, config, port)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                instance_id,
                requirement_id,
                'CREATED',
                datetime.now().isoformat(),
                json.dumps(config),
                port
            ))
            conn.commit()
    
    def update_instance_status(self, instance_id, status, **kwargs):
        """更新实例状态"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            updates = ['status = ?']
            params = [status]
            
            if 'started_at' in kwargs:
                updates.append('started_at = ?')
                params.append(kwargs['started_at'])
            
            if 'stopped_at' in kwargs:
                updates.append('stopped_at = ?')
                params.append(kwargs['stopped_at'])
            
            if 'results' in kwargs:
                updates.append('results = ?')
                params.append(json.dumps(kwargs['results']))
            
            params.append(instance_id)
            
            cursor.execute(f'''
                UPDATE instances SET {', '.join(updates)}
                WHERE id = ?
            ''', params)
            conn.commit()
    
    def get_instance(self, instance_id):
        """获取实例信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM instances WHERE id = ?', (instance_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'requirement_id': row[1],
                    'status': row[2],
                    'created_at': row[3],
                    'started_at': row[4],
                    'stopped_at': row[5],
                    'config': json.loads(row[6]) if row[6] else {},
                    'port': row[7],
                    'results': json.loads(row[8]) if row[8] else {}
                }
            return None
    
    def list_instances(self, status=None, limit=100):
        """列出实例"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if status:
                cursor.execute('''
                    SELECT * FROM instances WHERE status = ?
                    ORDER BY created_at DESC LIMIT ?
                ''', (status, limit))
            else:
                cursor.execute('''
                    SELECT * FROM instances
                    ORDER BY created_at DESC LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'requirement_id': row[1],
                'status': row[2],
                'created_at': row[3],
                'started_at': row[4],
                'stopped_at': row[5],
                'config': json.loads(row[6]) if row[6] else {},
                'port': row[7],
                'results': json.loads(row[8]) if row[8] else {}
            } for row in rows]
    
    # ═══════════════════════════════════════════════════════════
    # 进化事件
    # ═══════════════════════════════════════════════════════════
    
    def log_event(self, event_type, description, instance_id=None, data=None):
        """记录进化事件"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO evolution_events (timestamp, instance_id, event_type, description, data)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                instance_id,
                event_type,
                description,
                json.dumps(data) if data else None
            ))
            conn.commit()
    
    def get_recent_events(self, limit=20):
        """获取最近事件"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM evolution_events
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'timestamp': row[1],
                'instance_id': row[2],
                'type': row[3],
                'description': row[4],
                'data': json.loads(row[5]) if row[5] else {}
            } for row in rows]
    
    # ═══════════════════════════════════════════════════════════
    # 指标
    # ═══════════════════════════════════════════════════════════
    
    def record_metric(self, name, value, labels=None):
        """记录指标"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO metrics (timestamp, metric_name, metric_value, labels)
                VALUES (?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                name,
                value,
                json.dumps(labels) if labels else None
            ))
            conn.commit()
    
    def get_metrics_history(self, name, hours=24):
        """获取指标历史"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM metrics
                WHERE metric_name = ?
                AND timestamp > datetime('now', '-' || ? || ' hours')
                ORDER BY timestamp
            ''', (name, hours))
            
            rows = cursor.fetchall()
            return [{
                'timestamp': row[1],
                'value': row[3],
                'labels': json.loads(row[4]) if row[4] else {}
            } for row in rows]
    
    # ═══════════════════════════════════════════════════════════
    # Bug
    # ═══════════════════════════════════════════════════════════
    
    def record_bug(self, bug_type, severity, description, instance_id=None):
        """记录 Bug"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bugs (timestamp, instance_id, bug_type, severity, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                instance_id,
                bug_type,
                severity,
                description
            ))
            conn.commit()
            return cursor.lastrowid
    
    def fix_bug(self, bug_id, fix_data):
        """标记 Bug 已修复"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bugs SET fixed = 1, fix_data = ?
                WHERE id = ?
            ''', (json.dumps(fix_data), bug_id))
            conn.commit()
    
    def get_bugs(self, fixed=None, severity=None, limit=50):
        """获取 Bug 列表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = 'SELECT * FROM bugs WHERE 1=1'
            params = []
            
            if fixed is not None:
                query += ' AND fixed = ?'
                params.append(1 if fixed else 0)
            
            if severity:
                query += ' AND severity = ?'
                params.append(severity)
            
            query += ' ORDER BY timestamp DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'timestamp': row[1],
                'instance_id': row[2],
                'type': row[3],
                'severity': row[4],
                'description': row[5],
                'fixed': bool(row[6]),
                'fix_data': json.loads(row[7]) if row[7] else {}
            } for row in rows]
    
    # ═══════════════════════════════════════════════════════════
    # 预测
    # ═══════════════════════════════════════════════════════════
    
    def add_prediction(self, prediction_type, text, confidence, action):
        """添加预测"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions (prediction_type, prediction_text, confidence, action)
                VALUES (?, ?, ?, ?)
            ''', (prediction_type, text, confidence, action))
            conn.commit()
            return cursor.lastrowid
    
    def fulfill_prediction(self, prediction_id):
        """标记预测已实现"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE predictions SET fulfilled = 1, fulfilled_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), prediction_id))
            conn.commit()
    
    def get_predictions(self, fulfilled=None, limit=10):
        """获取预测"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if fulfilled is not None:
                cursor.execute('''
                    SELECT * FROM predictions
                    WHERE fulfilled = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (1 if fulfilled else 0, limit))
            else:
                cursor.execute('''
                    SELECT * FROM predictions
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'timestamp': row[1],
                'type': row[2],
                'text': row[3],
                'confidence': row[4],
                'action': row[5],
                'fulfilled': bool(row[6]),
                'fulfilled_at': row[7]
            } for row in rows]
    
    # ═══════════════════════════════════════════════════════════
    # 智能评分
    # ═══════════════════════════════════════════════════════════
    
    def record_intelligence_score(self, total, max_score, percentage, grade, dimensions):
        """记录智能评分"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO intelligence_scores (total_score, max_score, percentage, grade, dimensions)
                VALUES (?, ?, ?, ?, ?)
            ''', (total, max_score, percentage, grade, json.dumps(dimensions)))
            conn.commit()
    
    def get_intelligence_history(self, limit=30):
        """获取智能评分历史"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM intelligence_scores
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            return [{
                'timestamp': row[1],
                'total': row[2],
                'max': row[3],
                'percentage': row[4],
                'grade': row[5],
                'dimensions': json.loads(row[6]) if row[6] else {}
            } for row in rows]
    
    def get_latest_intelligence(self):
        """获取最新智能评分"""
        history = self.get_intelligence_history(limit=1)
        return history[0] if history else None
    
    # ═══════════════════════════════════════════════════════════
    # 统计
    # ═══════════════════════════════════════════════════════════
    
    def get_stats(self):
        """获取统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # 实例统计
            cursor.execute('SELECT COUNT(*), status FROM instances GROUP BY status')
            stats['instances'] = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Bug 统计
            cursor.execute('SELECT COUNT(*), severity FROM bugs WHERE fixed = 0 GROUP BY severity')
            stats['bugs'] = {row[1]: row[0] for row in cursor.fetchall()}
            
            # 预测统计
            cursor.execute('SELECT COUNT(*) FROM predictions WHERE fulfilled = 0')
            stats['pending_predictions'] = cursor.fetchone()[0]
            
            # 今日事件
            cursor.execute('''
                SELECT COUNT(*) FROM evolution_events
                WHERE date(timestamp) = date('now')
            ''')
            stats['today_events'] = cursor.fetchone()[0]
            
            return stats


if __name__ == '__main__':
    # 测试
    db = EvolutionDatabase()
    print("✅ 数据库初始化完成")
    print(f"   数据库: {db.db_path}")
