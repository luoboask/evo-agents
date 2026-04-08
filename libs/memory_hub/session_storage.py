# -*- coding: utf-8 -*-
"""
会话记忆存储管理器 - 负责会话级别的记忆存储

特点:
- 独立表存储会话记忆
- 每个会话固定最多 50 条记录
- 超出时自动删除最老的记录
"""

from pathlib import Path
import sqlite3
import json
import urllib.request
from typing import List, Dict, Optional
from datetime import datetime

# 导入 Embedding 缓存
try:
    from .embedding_cache import EmbeddingCache
except ImportError:
    from embedding_cache import EmbeddingCache


class SessionMemoryStorage:
    """会话记忆存储 - 独立表存储会话级别的记忆"""
    
    MAX_SESSION_MEMORIES = 100  # 每个会话最多保留 100 条（增加容量）
    
    def __init__(self, memory_path: Path):
        self.memory_path = memory_path
        self.db_path = memory_path / 'memory_stream.db'
        self._init_database()
        
        # 初始化 Embedding 缓存
        self.embedding_cache = EmbeddingCache(
            cache_file=memory_path / 'embedding_cache.pkl'
        )
    
    def _init_database(self):
        """初始化数据库表结构"""
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # 创建会话记忆表（独立表）
        cur.execute('''
            CREATE TABLE IF NOT EXISTS session_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                content TEXT NOT NULL,
                memory_type TEXT DEFAULT 'observation',
                importance REAL DEFAULT 5.0,
                tags TEXT DEFAULT '[]',
                embedding TEXT DEFAULT '[]',
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引 - 性能优化
        cur.execute('CREATE INDEX IF NOT EXISTS idx_session_memories_session ON session_memories(session_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_session_memories_type ON session_memories(memory_type)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_session_memories_created ON session_memories(created_at)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_session_memories_importance ON session_memories(importance)')
        
        # 启用 WAL 模式 - 提高并发性能
        cur.execute('PRAGMA journal_mode=WAL')
        
        # 增加缓存大小 - 提高查询性能（64MB）
        cur.execute('PRAGMA cache_size=-64000')
        
        conn.commit()
        conn.close()
    
    def add_memory(self, 
                   session_id: str,
                   content: str,
                   memory_type: str = 'observation',
                   importance: float = 5.0,
                   tags: List[str] = None,
                   metadata: Dict = None) -> int:
        """
        添加会话记忆（自动清理超出限制的旧记录）
        
        Args:
            session_id: 会话 ID（必填）
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性
            tags: 标签列表
            metadata: 元数据
        
        Returns:
            memory_id: 新记忆 ID
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        try:
            # 开始事务
            cur.execute('BEGIN IMMEDIATE')
            
            # 插入新记忆
            cur.execute('''
                INSERT INTO session_memories (session_id, content, memory_type, importance, tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                content,
                memory_type,
                importance,
                json.dumps(tags or []),
                json.dumps(metadata or {})
            ))
            
            memory_id = cur.lastrowid
            
            # 检查并清理超出限制的旧记录
            self._cleanup_old_memories(cur, session_id)
            
            # 提交事务
            conn.commit()
            
            return memory_id
            
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            conn.close()
    
    def _cleanup_old_memories(self, cur: sqlite3.Cursor, session_id: str):
        """
        清理超出限制的旧记录（保留最新的 MAX_SESSION_MEMORIES 条）
        
        Args:
            cur: 数据库游标
            session_id: 会话 ID
        """
        # 查询当前会话的记忆数量
        cur.execute('''
            SELECT COUNT(*) FROM session_memories WHERE session_id = ?
        ''', (session_id,))
        count = cur.fetchone()[0]
        
        # 如果超出限制，删除最老的记录
        if count > self.MAX_SESSION_MEMORIES:
            excess = count - self.MAX_SESSION_MEMORIES
            cur.execute('''
                DELETE FROM session_memories
                WHERE session_id = ? AND id IN (
                    SELECT id FROM session_memories
                    WHERE session_id = ?
                    ORDER BY created_at ASC
                    LIMIT ?
                )
            ''', (session_id, session_id, excess))
    
    def search_memories(self, 
                       session_id: str,
                       top_k: int = 5,
                       memory_type: Optional[str] = None,
                       semantic: bool = False,
                       include_all: bool = False) -> List[Dict]:
        """
        搜索会话记忆
        
        Args:
            session_id: 会话 ID
            top_k: 返回数量
            memory_type: 记忆类型过滤
            semantic: 是否使用语义搜索
            include_all: 是否返回全部（不按 top_k 限制）
        
        Returns:
            记忆列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 构建查询条件
        if memory_type:
            if include_all:
                cur.execute('''
                    SELECT * FROM session_memories
                    WHERE session_id = ? AND memory_type = ?
                    ORDER BY created_at DESC
                ''', (session_id, memory_type))
            else:
                cur.execute('''
                    SELECT * FROM session_memories
                    WHERE session_id = ? AND memory_type = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (session_id, memory_type, top_k))
        else:
            if include_all:
                cur.execute('''
                    SELECT * FROM session_memories
                    WHERE session_id = ?
                    ORDER BY created_at DESC
                ''', (session_id,))
            else:
                cur.execute('''
                    SELECT * FROM session_memories
                    WHERE session_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (session_id, top_k))
        
        results = [dict(row) for row in cur.fetchall()]
        
        # 更新访问时间
        if results:
            ids = [r['id'] for r in results]
            cur.execute('''
                UPDATE session_memories
                SET last_accessed = CURRENT_TIMESTAMP
                WHERE id IN ({})
            '''.format(','.join('?' * len(ids))), ids)
            conn.commit()
        
        conn.close()
        
        # 语义搜索（可选）
        if semantic:
            results = self._semantic_search(session_id, results)
        
        return results
    
    def get_memory(self, memory_id: int, session_id: str = None) -> Optional[Dict]:
        """获取单条记忆"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        if session_id:
            cur.execute('SELECT * FROM session_memories WHERE id = ? AND session_id = ?', 
                       (memory_id, session_id))
        else:
            cur.execute('SELECT * FROM session_memories WHERE id = ?', (memory_id,))
        
        row = cur.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def delete_memory(self, memory_id: int, session_id: str) -> bool:
        """删除记忆"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('DELETE FROM session_memories WHERE id = ? AND session_id = ?', 
                   (memory_id, session_id))
        deleted = cur.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def update_memory(self, memory_id: int, session_id: str, **kwargs) -> bool:
        """更新记忆"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # 动态构建 UPDATE 语句
        updates = []
        values = []
        for key, value in kwargs.items():
            if key in ['content', 'memory_type', 'importance', 'tags', 'metadata']:
                updates.append(f'{key} = ?')
                if key in ['tags', 'metadata']:
                    values.append(json.dumps(value))
                else:
                    values.append(value)
        
        if not updates:
            return False
        
        values.extend([memory_id, session_id])
        cur.execute(f'''
            UPDATE session_memories
            SET {', '.join(updates)}
            WHERE id = ? AND session_id = ?
        ''', values)
        
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def get_stats(self, session_id: str) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # 总数
        cur.execute('SELECT COUNT(*) FROM session_memories WHERE session_id = ?', 
                   (session_id,))
        total = cur.fetchone()[0]
        
        # 按类型统计
        cur.execute('''
            SELECT memory_type, COUNT(*) as count
            FROM session_memories
            WHERE session_id = ?
            GROUP BY memory_type
        ''', (session_id,))
        by_type = {row[0]: row[1] for row in cur.fetchall()}
        
        # 平均重要性
        cur.execute('SELECT AVG(importance) FROM session_memories WHERE session_id = ?', 
                   (session_id,))
        avg_importance = cur.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'session_id': session_id,
            'total': total,
            'by_type': by_type,
            'avg_importance': round(avg_importance, 2),
            'max_limit': self.MAX_SESSION_MEMORIES
        }
    
    def get_all_sessions(self) -> List[str]:
        """获取所有有记忆的会话 ID"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('''
            SELECT DISTINCT session_id FROM session_memories
        ''')
        sessions = [row[0] for row in cur.fetchall()]
        
        conn.close()
        return sessions
    
    def clear_session(self, session_id: str) -> int:
        """清空会话的所有记忆"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('DELETE FROM session_memories WHERE session_id = ?', (session_id,))
        deleted = cur.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def _get_embedding(self, text: str) -> List[float]:
        """获取 Ollama embedding（带缓存）"""
        # 先尝试从缓存获取
        cached = self.embedding_cache.get(text)
        if cached:
            return cached
        
        # 缓存未命中，调用 Ollama
        try:
            payload = {
                "model": "nomic-embed-text",
                "prompt": text
            }
            req = urllib.request.Request(
                'http://localhost:11434/api/embeddings',
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            embedding = data.get('embedding', [])
            
            # 缓存 embedding
            if embedding:
                self.embedding_cache.set(text, embedding)
            
            return embedding
        except Exception as e:
            print(f"⚠️  Ollama Embedding 失败：{e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _semantic_search(self, session_id: str, candidates: List[Dict]) -> List[Dict]:
        """语义搜索"""
        # TODO: 实现语义搜索逻辑（与 storage.py 类似）
        # 为简洁起见，这里先返回原列表
        return candidates
