# -*- coding: utf-8 -*-
"""
统一索引 - 关联记忆、知识、进化

功能:
- 关联记忆和方案
- 关联知识和记忆
- 提供跨库统计查询
- 支持质量排序
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class UnifiedIndex:
    """统一索引 - 关联记忆、知识、进化"""
    
    def __init__(self, db_path: str = None):
        """
        初始化统一索引
        
        Args:
            db_path: 数据库路径（默认在 data/unified_index.db）
        """
        self.workspace = Path(__file__).parent.parent.parent
        self.data_path = self.workspace / "data"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = self.data_path / "unified_index.db"
        
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 记忆 - 方案关联表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_solution_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER,
                solution_id INTEGER,
                usage_count INTEGER DEFAULT 1,
                last_used TEXT,
                created_at TEXT,
                UNIQUE(memory_id, solution_id)
            )
        ''')
        
        # 知识 - 记忆关联表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_memory_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                knowledge_id TEXT,
                memory_id INTEGER,
                relation_type TEXT,
                strength REAL DEFAULT 1.0,
                created_at TEXT,
                UNIQUE(knowledge_id, memory_id)
            )
        ''')
        
        # 知识 - 方案关联表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_solution_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                knowledge_id TEXT,
                solution_id INTEGER,
                relation_type TEXT,
                created_at TEXT,
                UNIQUE(knowledge_id, solution_id)
            )
        ''')
        
        # 使用统计缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_stats_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT,  -- memory/knowledge/solution
                entity_id TEXT,
                usage_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                last_updated TEXT,
                UNIQUE(entity_type, entity_id)
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memory ON memory_solution_links(memory_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_solution ON memory_solution_links(solution_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_knowledge ON knowledge_memory_links(knowledge_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_stats ON usage_stats_cache(entity_type, entity_id)')
        
        conn.commit()
        conn.close()
    
    # ───────────────────────────────────────────────────────
    # 关联管理
    # ───────────────────────────────────────────────────────
    
    def link_memory_to_solution(self, memory_id: int, solution_id: int):
        """
        关联记忆和方案
        
        Args:
            memory_id: 记忆 ID
            solution_id: 方案 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # 插入或更新
        cursor.execute('''
            INSERT INTO memory_solution_links 
            (memory_id, solution_id, usage_count, last_used, created_at)
            VALUES (?, ?, 1, ?, ?)
            ON CONFLICT(memory_id, solution_id) 
            DO UPDATE SET 
                usage_count = usage_count + 1,
                last_used = ?
        ''', (memory_id, solution_id, now, now, now))
        
        conn.commit()
        conn.close()
        
        # 更新统计缓存
        self._update_stats('memory', memory_id)
        self._update_stats('solution', solution_id)
    
    def link_knowledge_to_memory(self, knowledge_id: str, memory_id: int, 
                                relation_type: str = "derived_from"):
        """
        关联知识和记忆
        
        Args:
            knowledge_id: 知识 ID
            memory_id: 记忆 ID
            relation_type: 关系类型 (derived_from/related_to/supports)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge_memory_links
            (knowledge_id, memory_id, relation_type, strength, created_at)
            VALUES (?, ?, ?, 1.0, ?)
        ''', (knowledge_id, memory_id, relation_type, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # 更新统计缓存
        self._update_stats('knowledge', knowledge_id)
    
    def link_knowledge_to_solution(self, knowledge_id: str, solution_id: int,
                                  relation_type: str = "supports"):
        """
        关联知识和方案
        
        Args:
            knowledge_id: 知识 ID
            solution_id: 方案 ID
            relation_type: 关系类型 (supports/derived_from/validates)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge_solution_links
            (knowledge_id, solution_id, relation_type, created_at)
            VALUES (?, ?, ?, ?)
        ''', (knowledge_id, solution_id, relation_type, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # 更新统计缓存
        self._update_stats('knowledge', knowledge_id)
        self._update_stats('solution', solution_id)
    
    # ───────────────────────────────────────────────────────
    # 统计查询
    # ───────────────────────────────────────────────────────
    
    def get_solution_stats(self, solution_id: int) -> Dict:
        """
        获取方案完整统计
        
        Args:
            solution_id: 方案 ID
        
        Returns:
            统计信息字典
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        stats = {
            'solution_id': solution_id,
            'usage_count': 0,
            'related_memories': [],
            'related_knowledge': [],
            'success_rate': 0.0
        }
        
        # 使用次数
        cursor.execute('''
            SELECT SUM(usage_count) FROM memory_solution_links
            WHERE solution_id = ?
        ''', (solution_id,))
        result = cursor.fetchone()
        stats['usage_count'] = result[0] or 0
        
        # 关联记忆
        cursor.execute('''
            SELECT memory_id, usage_count, last_used
            FROM memory_solution_links
            WHERE solution_id = ?
            ORDER BY usage_count DESC
            LIMIT 10
        ''', (solution_id,))
        stats['related_memories'] = [dict(row) for row in cursor.fetchall()]
        
        # 关联知识
        cursor.execute('''
            SELECT knowledge_id, relation_type
            FROM knowledge_solution_links
            WHERE solution_id = ?
        ''', (solution_id,))
        stats['related_knowledge'] = [dict(row) for row in cursor.fetchall()]
        
        # 成功率（从 effect_tracker 获取）
        try:
            from libs.self_evolution.effect_tracker import EffectTracker
            tracker = EffectTracker()
            # 这里需要根据实际 schema 调整
            stats['success_rate'] = 0.0  # TODO: 实现
        except:
            stats['success_rate'] = 0.0
        
        conn.close()
        return stats
    
    def get_memory_stats(self, memory_id: int) -> Dict:
        """
        获取记忆统计
        
        Args:
            memory_id: 记忆 ID
        
        Returns:
            统计信息字典
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        stats = {
            'memory_id': memory_id,
            'usage_count': 0,
            'related_solutions': [],
            'related_knowledge': []
        }
        
        # 使用次数
        cursor.execute('''
            SELECT SUM(usage_count) FROM memory_solution_links
            WHERE memory_id = ?
        ''', (memory_id,))
        result = cursor.fetchone()
        stats['usage_count'] = result[0] or 0
        
        # 关联方案
        cursor.execute('''
            SELECT solution_id, usage_count
            FROM memory_solution_links
            WHERE memory_id = ?
            ORDER BY usage_count DESC
            LIMIT 10
        ''', (memory_id,))
        stats['related_solutions'] = [dict(row) for row in cursor.fetchall()]
        
        # 关联知识
        cursor.execute('''
            SELECT knowledge_id, relation_type
            FROM knowledge_memory_links
            WHERE memory_id = ?
        ''', (memory_id,))
        stats['related_knowledge'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return stats
    
    def get_knowledge_stats(self, knowledge_id: str) -> Dict:
        """
        获取知识统计
        
        Args:
            knowledge_id: 知识 ID
        
        Returns:
            统计信息字典
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        stats = {
            'knowledge_id': knowledge_id,
            'usage_count': 0,
            'related_memories': [],
            'related_solutions': []
        }
        
        # 关联记忆数
        cursor.execute('''
            SELECT COUNT(*) FROM knowledge_memory_links
            WHERE knowledge_id = ?
        ''', (knowledge_id,))
        stats['usage_count'] = cursor.fetchone()[0]
        
        # 关联记忆
        cursor.execute('''
            SELECT memory_id, relation_type
            FROM knowledge_memory_links
            WHERE knowledge_id = ?
        ''', (knowledge_id,))
        stats['related_memories'] = [dict(row) for row in cursor.fetchall()]
        
        # 关联方案
        cursor.execute('''
            SELECT solution_id, relation_type
            FROM knowledge_solution_links
            WHERE knowledge_id = ?
        ''', (knowledge_id,))
        stats['related_solutions'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return stats
    
    def _update_stats(self, entity_type: str, entity_id):
        """更新统计缓存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if entity_type == 'memory':
            stats = self.get_memory_stats(entity_id)
        elif entity_type == 'solution':
            stats = self.get_solution_stats(entity_id)
        elif entity_type == 'knowledge':
            stats = self.get_knowledge_stats(entity_id)
        else:
            return
        
        cursor.execute('''
            INSERT INTO usage_stats_cache 
            (entity_type, entity_id, usage_count, success_rate, last_updated)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(entity_type, entity_id)
            DO UPDATE SET
                usage_count = ?,
                success_rate = ?,
                last_updated = ?
        ''', (
            entity_type, entity_id,
            stats.get('usage_count', 0), stats.get('success_rate', 0.0),
            datetime.now().isoformat(),
            stats.get('usage_count', 0), stats.get('success_rate', 0.0),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    # ───────────────────────────────────────────────────────
    # 高质量内容识别
    # ───────────────────────────────────────────────────────
    
    def get_high_value_solutions(self, limit: int = 10) -> List[Dict]:
        """获取高价值方案（使用次数多 + 成功率高）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT entity_id as solution_id, usage_count, success_rate
            FROM usage_stats_cache
            WHERE entity_type = 'solution'
            ORDER BY usage_count DESC, success_rate DESC
            LIMIT ?
        ''', (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_high_value_knowledge(self, limit: int = 10) -> List[Dict]:
        """获取高价值知识（被频繁引用）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT entity_id as knowledge_id, usage_count
            FROM usage_stats_cache
            WHERE entity_type = 'knowledge'
            ORDER BY usage_count DESC
            LIMIT ?
        ''', (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    # ───────────────────────────────────────────────────────
    # 清理和维护
    # ───────────────────────────────────────────────────────
    
    def cleanup_old_links(self, days: int = 90):
        """清理旧关联（超过指定天数未使用）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cutoff_str = datetime.fromtimestamp(cutoff).isoformat()
        
        cursor.execute('''
            DELETE FROM memory_solution_links
            WHERE last_used < ?
        ''', (cutoff_str,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
    
    def rebuild_cache(self):
        """重建统计缓存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 清空缓存
        cursor.execute('DELETE FROM usage_stats_cache')
        
        # 重建所有统计
        cursor.execute('SELECT DISTINCT solution_id FROM memory_solution_links')
        for row in cursor.fetchall():
            self._update_stats('solution', row[0])
        
        cursor.execute('SELECT DISTINCT memory_id FROM memory_solution_links')
        for row in cursor.fetchall():
            self._update_stats('memory', row[0])
        
        cursor.execute('SELECT DISTINCT knowledge_id FROM knowledge_memory_links')
        for row in cursor.fetchall():
            self._update_stats('knowledge', row[0])
        
        conn.commit()
        conn.close()
