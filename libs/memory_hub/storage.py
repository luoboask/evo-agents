# -*- coding: utf-8 -*-
"""
存储管理器 - 负责数据库操作
支持关键词搜索 + Ollama 语义搜索
"""

from pathlib import Path
import sqlite3
import json
import urllib.request
from typing import List, Dict, Optional


class StorageManager:
    """存储管理器 - 负责数据库操作"""
    
    def __init__(self, memory_path: Path):
        self.memory_path = memory_path
        self.db_path = memory_path / 'memory_stream.db'
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # 创建记忆表
        cur.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
        # 创建索引
        cur.execute('CREATE INDEX IF NOT EXISTS idx_type ON memories(memory_type)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        
        conn.commit()
        conn.close()
    
    def add_memory(self, **kwargs) -> int:
        """添加记忆"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('''
            INSERT INTO memories (content, memory_type, importance, tags, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            kwargs['content'],
            kwargs.get('memory_type', 'observation'),
            kwargs.get('importance', 5.0),
            json.dumps(kwargs.get('tags', [])),
            json.dumps(kwargs.get('metadata', {}))
        ))
        
        memory_id = cur.lastrowid
        conn.commit()
        conn.close()
        
        return memory_id
    
    def search_memories(self, 
                       query: str, 
                       top_k: int = 5,
                       memory_type: Optional[str] = None,
                       semantic: bool = False) -> List[Dict]:
        """搜索记忆"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 基础查询
        if memory_type:
            cur.execute('''
                SELECT * FROM memories
                WHERE memory_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (memory_type, top_k))
        else:
            cur.execute('''
                SELECT * FROM memories
                ORDER BY created_at DESC
                LIMIT ?
            ''', (top_k,))
        
        results = [dict(row) for row in cur.fetchall()]
        
        # 更新访问时间
        if results:
            ids = [r['id'] for r in results]
            cur.execute('''
                UPDATE memories
                SET last_accessed = CURRENT_TIMESTAMP
                WHERE id IN ({})
            '''.format(','.join('?' * len(ids))), ids)
            conn.commit()
        
        conn.close()
        
        # 语义搜索（可选）
        if semantic:
            results = self._semantic_search(query, results)
        
        return results
    
    def get_memory(self, memory_id: int) -> Optional[Dict]:
        """获取单条记忆"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
        row = cur.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def delete_memory(self, memory_id: int) -> bool:
        """删除记忆"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
        deleted = cur.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def update_memory(self, memory_id: int, **kwargs) -> bool:
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
        
        values.append(memory_id)
        cur.execute(f'''
            UPDATE memories
            SET {', '.join(updates)}
            WHERE id = ?
        ''', values)
        
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # 总数
        cur.execute('SELECT COUNT(*) FROM memories')
        total = cur.fetchone()[0]
        
        # 按类型统计
        cur.execute('''
            SELECT memory_type, COUNT(*) as count
            FROM memories
            GROUP BY memory_type
        ''')
        by_type = {row[0]: row[1] for row in cur.fetchall()}
        
        # 平均重要性
        cur.execute('SELECT AVG(importance) FROM memories')
        avg_importance = cur.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total': total,
            'by_type': by_type,
            'avg_importance': round(avg_importance, 2)
        }
    
    def _get_embedding(self, text: str) -> List[float]:
        """获取 Ollama embedding"""
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
            return data.get('embedding', [])
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
    
    def _semantic_search(self, query: str, candidates: List[Dict]) -> List[Dict]:
        """
        语义搜索 - 使用 Ollama embedding + 余弦相似度
        
        Args:
            query: 查询文本
            candidates: 候选记忆列表
        
        Returns:
            按相似度排序的结果
        """
        if not candidates:
            return []
        
        # 获取查询的 embedding
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            # Ollama 不可用，降级到关键词匹配
            query_lower = query.lower()
            return [c for c in candidates if query_lower in c.get('content', '').lower()]
        
        # 计算每个候选的相似度
        results = []
        for candidate in candidates:
            content = candidate.get('content', '')
            
            # 尝试使用缓存的 embedding
            embedding_str = candidate.get('embedding', '[]')
            if isinstance(embedding_str, str):
                try:
                    candidate_embedding = json.loads(embedding_str)
                except:
                    candidate_embedding = []
            else:
                candidate_embedding = embedding_str
            
            # 如果没有缓存，实时计算并缓存
            if not candidate_embedding:
                candidate_embedding = self._get_embedding(content)
                if candidate_embedding:
                    self._cache_embedding(candidate['id'], candidate_embedding)
            
            # 计算相似度
            similarity = self._cosine_similarity(query_embedding, candidate_embedding)
            candidate_with_score = {**candidate, 'similarity_score': similarity}
            results.append(candidate_with_score)
        
        # 按相似度排序
        results.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
        
        return results
    
    def _cache_embedding(self, memory_id: int, embedding: List[float]):
        """缓存 embedding 到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('''
                UPDATE memories
                SET embedding = ?
                WHERE id = ?
            ''', (json.dumps(embedding), memory_id))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️  缓存 embedding 失败：{e}")
