# -*- coding: utf-8 -*-
"""
领域知识管理 - 结构化知识模型

支持的知识类型:
- concepts: 核心概念
- best_practices: 最佳实践
- faq: 常见问题
- code_samples: 案例代码
"""

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class DomainKnowledge:
    """领域知识管理"""
    
    def __init__(self, domain: str, db_path: str = None):
        """
        初始化领域知识
        
        Args:
            domain: 领域名称（如 "Python 异步编程"）
            db_path: 数据库路径（默认在 domain 目录下）
        """
        self.domain = domain
        self.workspace = Path(__file__).parent.parent.parent
        
        if db_path:
            self.db_path = Path(db_path)
        else:
            # 默认路径：data/<domain>/domain_knowledge.db
            domain_safe = domain.replace(" ", "_").lower()
            self.db_path = self.workspace / "data" / domain_safe / "domain_knowledge.db"
        
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 领域知识表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id TEXT PRIMARY KEY,
                domain TEXT,
                category TEXT,
                title TEXT,
                content TEXT,
                tags TEXT,
                quality_score REAL DEFAULT 0.5,
                source TEXT,
                created_at TEXT,
                updated_at TEXT,
                metadata TEXT
            )
        ''')
        
        # 概念关系表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_concept_id TEXT,
                to_concept_id TEXT,
                relation_type TEXT,
                strength REAL DEFAULT 1.0,
                created_at TEXT,
                FOREIGN KEY (from_concept_id) REFERENCES knowledge(id),
                FOREIGN KEY (to_concept_id) REFERENCES knowledge(id)
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domain ON knowledge(domain)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON knowledge(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON knowledge(tags)')
        
        conn.commit()
        conn.close()
    
    def add(self,
            content: str,
            title: str,
            category: str = "general",
            tags: List[str] = None,
            quality_score: float = 0.5,
            source: str = None,
            metadata: Dict = None) -> str:
        """
        添加领域知识
        
        Args:
            content: 知识内容
            title: 标题
            category: 分类 (concept/best_practice/faq/code_sample/general)
            tags: 标签列表
            quality_score: 质量评分 (0.0-1.0)
            source: 来源（URL 或文件名）
            metadata: 额外元数据
        
        Returns:
            知识 ID
        """
        knowledge_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO knowledge 
            (id, domain, category, title, content, tags, quality_score, source, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            knowledge_id,
            self.domain,
            category,
            title,
            content,
            json.dumps(tags or [], ensure_ascii=False),
            quality_score,
            source,
            now,
            now,
            json.dumps(metadata or {}, ensure_ascii=False)
        ))
        
        conn.commit()
        conn.close()
        
        return knowledge_id
    
    def search(self,
               query: str = None,
               category: Optional[str] = None,
               tags: Optional[List[str]] = None,
               min_quality: float = 0.0,
               limit: int = 10) -> List[Dict]:
        """
        搜索领域知识
        
        Args:
            query: 搜索关键词（标题或内容）
            category: 分类过滤
            tags: 标签过滤
            min_quality: 最低质量分
            limit: 返回数量
        
        Returns:
            知识列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 构建查询
        conditions = ["domain = ?"]
        params = [self.domain]
        
        if query:
            conditions.append("(title LIKE ? OR content LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        if min_quality > 0:
            conditions.append("quality_score >= ?")
            params.append(min_quality)
        
        where_clause = " AND ".join(conditions)
        
        cursor.execute(f'''
            SELECT * FROM knowledge
            WHERE {where_clause}
            ORDER BY quality_score DESC, updated_at DESC
            LIMIT ?
        ''', params + [limit])
        
        results = []
        for row in cursor.fetchall():
            result = dict(row)
            result['tags'] = json.loads(result['tags'])
            result['metadata'] = json.loads(result['metadata'])
            results.append(result)
        
        conn.close()
        return results
    
    def get_by_id(self, knowledge_id: str) -> Optional[Dict]:
        """根据 ID 获取知识"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM knowledge WHERE id = ?', (knowledge_id,))
        row = cursor.fetchone()
        
        if row:
            result = dict(row)
            result['tags'] = json.loads(result['tags'])
            result['metadata'] = json.loads(result['metadata'])
        else:
            result = None
        
        conn.close()
        return result
    
    def update_quality(self, knowledge_id: str, quality_score: float):
        """更新质量评分"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE knowledge 
            SET quality_score = ?, updated_at = ?
            WHERE id = ?
        ''', (quality_score, datetime.now().isoformat(), knowledge_id))
        
        conn.commit()
        conn.close()
    
    def add_relationship(self,
                        from_concept_id: str,
                        to_concept_id: str,
                        relation_type: str,
                        strength: float = 1.0):
        """
        添加概念关系
        
        Args:
            from_concept_id: 源概念 ID
            to_concept_id: 目标概念 ID
            relation_type: 关系类型 (related_to/depends_on/is_a/part_of)
            strength: 关系强度 (0.0-1.0)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO relationships 
            (from_concept_id, to_concept_id, relation_type, strength, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (from_concept_id, to_concept_id, relation_type, strength, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """获取领域统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # 总量统计
        cursor.execute('SELECT COUNT(*) FROM knowledge WHERE domain = ?', (self.domain,))
        stats['total'] = cursor.fetchone()[0]
        
        # 分类统计
        cursor.execute('''
            SELECT category, COUNT(*) 
            FROM knowledge 
            WHERE domain = ? 
            GROUP BY category
        ''', (self.domain,))
        stats['by_category'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 平均质量分
        cursor.execute('''
            SELECT AVG(quality_score) 
            FROM knowledge 
            WHERE domain = ?
        ''', (self.domain,))
        stats['avg_quality'] = cursor.fetchone()[0] or 0.0
        
        conn.close()
        return stats
