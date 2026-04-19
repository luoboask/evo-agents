# -*- coding: utf-8 -*-
"""
领域知识管理 - 结构化知识模型

支持的知识类型:
- concepts: 核心概念
- best_practices: 最佳实践
- faq: 常见问题
- code_samples: 案例代码

用法:
    # 手动添加知识
    python3 scripts/domain/domain_knowledge.py --domain "Python" --add --title "异步编程" --content "..."
    
    # 自动整理模式
    python3 scripts/domain/domain_knowledge.py --auto-organize --agent demo100-agent
    
    # 每周审查
    python3 scripts/domain/domain_knowledge.py --weekly-review --agent demo100-agent
"""

import json
import sqlite3
import uuid
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter

# 使用统一路径解析工具
try:
    from path_utils import resolve_workspace
except ImportError:
    def resolve_workspace():
        return Path(__file__).parent.parent.parent


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
        self.workspace = resolve_workspace()
        
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
        
        conn.commit()
        conn.close()
    
    def add_knowledge(self,
                     category: str,
                     title: str,
                     content: str,
                     tags: List[str] = None,
                     source: str = None,
                     metadata: Dict = None) -> str:
        """
        添加领域知识
        
        Args:
            category: 分类 (concept/best_practice/faq/code_sample)
            title: 标题
            content: 内容
            tags: 标签列表
            source: 来源
            metadata: 额外元数据
        
        Returns:
            知识 ID
        """
        knowledge_id = str(uuid.uuid4())[:8]
        tags = tags or []
        metadata = metadata or {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO knowledge 
            (id, domain, category, title, content, tags, source, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            knowledge_id,
            self.domain,
            category,
            title,
            content,
            json.dumps(tags),
            source,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            json.dumps(metadata)
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ 添加知识：{title} (ID: {knowledge_id})")
        return knowledge_id
    
    def auto_organize(self, agent_name: str = 'demo100-agent') -> Dict:
        """
        自动整理领域知识
        
        从知识图谱和记忆中提取新概念，自动分类并关联
        
        Args:
            agent_name: Agent 名称
        
        Returns:
            整理结果统计
        """
        print(f"📚 领域知识自动整理 (Agent: {agent_name})")
        print(f"   领域：{self.domain}\n")
        
        # 从知识图谱提取概念
        try:
            sys.path.insert(0, str(self.workspace / 'libs'))
            from knowledge_graph.builder import KnowledgeGraphEnhanced
            kg = KnowledgeGraphEnhanced(agent_name)
            
            print(f"🔍 从知识图谱提取概念...")
            concepts_added = 0
            
            for entity_id, entity in kg.entities.items():
                entity_type = entity.get('type', 'concept')
                entity_name = entity.get('name', '')
                
                if entity_type in ['technology', 'concept']:
                    # 检查是否已存在
                    existing = self.search(f"{entity_name}", limit=1)
                    if not existing:
                        self.add_knowledge(
                            category='concept',
                            title=entity_name,
                            content=f"{entity_type}: {entity_name}",
                            tags=[entity_type, 'auto_imported'],
                            source='knowledge_graph',
                            metadata={'entity_id': entity_id}
                        )
                        concepts_added += 1
            
            print(f"   ✅ 添加 {concepts_added} 个新概念\n")
            
        except Exception as e:
            print(f"   ⚠️  知识图谱提取失败：{e}\n")
            concepts_added = 0
        
        # 从记忆提取 FAQ
        try:
            sys.path.insert(0, str(self.workspace / 'skills' / 'memory-search'))
            from memory_stream import MemoryStream
            ms = MemoryStream(agent_id=agent_name)
            
            print(f"🔍 从记忆提取 FAQ...")
            faqs_added = 0
            
            # 获取高重要性的记忆
            memories = ms.get_memories(memory_type='observation', limit=50)
            
            for mem in memories:
                if mem.importance >= 7.0 and len(mem.content) > 20:
                    # 检查是否已存在类似 FAQ
                    existing = self.search(mem.content[:50], limit=1)
                    if not existing:
                        self.add_knowledge(
                            category='faq',
                            title=mem.content[:100],
                            content=mem.content,
                            tags=['faq', 'auto_generated'],
                            source='memory_stream',
                            metadata={'memory_id': mem.id, 'importance': mem.importance}
                        )
                        faqs_added += 1
            
            print(f"   ✅ 添加 {faqs_added} 个 FAQ\n")
            
        except Exception as e:
            print(f"   ⚠️  记忆提取失败：{e}\n")
            faqs_added = 0
        
        # 生成整理报告
        stats = self.get_stats()
        
        print(f"📊 整理完成!")
        print(f"   总知识数：{stats['total']}")
        print(f"   分类统计：{stats['by_category']}")
        print(f"   平均质量：{stats['avg_quality']:.2f}\n")
        
        return {
            'concepts_added': concepts_added,
            'faqs_added': faqs_added,
            'stats': stats
        }
    
    def weekly_review(self, agent_name: str = 'demo100-agent') -> Dict:
        """
        每周知识审查
        
        审查知识质量，合并重复知识，删除过时知识
        
        Args:
            agent_name: Agent 名称
        
        Returns:
            审查结果
        """
        print(f"📋 领域知识每周审查 (Agent: {agent_name})")
        print(f"   领域：{self.domain}\n")
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. 低质量知识审查
        print(f"🔍 审查低质量知识...")
        cursor.execute('''
            SELECT id, title, quality_score 
            FROM knowledge 
            WHERE quality_score < 0.3 AND domain = ?
        ''', (self.domain,))
        low_quality = cursor.fetchall()
        
        if low_quality:
            print(f"   发现 {len(low_quality)} 个低质量知识")
            for item in low_quality[:5]:
                print(f"     - {item['title'][:50]} (质量：{item['quality_score']:.2f})")
        else:
            print(f"   ✅ 无低质量知识")
        print()
        
        # 2. 重复知识检测
        print(f"🔍 检测重复知识...")
        cursor.execute('''
            SELECT title, COUNT(*) as count
            FROM knowledge
            WHERE domain = ?
            GROUP BY title
            HAVING count > 1
        ''', (self.domain,))
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"   发现 {len(duplicates)} 组重复知识")
            for item in duplicates[:5]:
                print(f"     - {item['title'][:50]} ({item['count']}次)")
        else:
            print(f"   ✅ 无重复知识")
        print()
        
        # 3. 过时知识审查 (30 天未更新)
        print(f"🔍 审查过时知识...")
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        cursor.execute('''
            SELECT id, title, updated_at
            FROM knowledge
            WHERE domain = ? AND updated_at < ?
        ''', (self.domain, thirty_days_ago))
        outdated = cursor.fetchall()
        
        if outdated:
            print(f"   发现 {len(outdated)} 个过时知识")
            for item in outdated[:5]:
                print(f"     - {item['title'][:50]} (更新：{item['updated_at'][:10]})")
        else:
            print(f"   ✅ 无过时知识")
        print()
        
        conn.close()
        
        # 生成审查报告
        stats = self.get_stats()
        
        print(f"📊 审查完成!")
        print(f"   总知识数：{stats['total']}")
        print(f"   低质量：{len(low_quality)}")
        print(f"   重复：{len(duplicates)}")
        print(f"   过时：{len(outdated)}\n")
        
        return {
            'low_quality': len(low_quality),
            'duplicates': len(duplicates),
            'outdated': len(outdated),
            'stats': stats
        }
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索领域知识"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM knowledge
            WHERE domain = ? AND (title LIKE ? OR content LIKE ?)
            ORDER BY quality_score DESC
            LIMIT ?
        ''', (self.domain, f'%{query}%', f'%{query}%', limit))
        
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
        """添加概念关系"""
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


# =============================================================================
# 主函数 - 支持手动和自动模式
# =============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='领域知识管理')
    parser.add_argument('--domain', type=str, help='领域名称')
    parser.add_argument('--add', action='store_true', help='添加知识')
    parser.add_argument('--title', type=str, help='知识标题')
    parser.add_argument('--content', type=str, help='知识内容')
    parser.add_argument('--category', type=str, default='concept', help='知识分类')
    parser.add_argument('--auto-organize', action='store_true', help='自动整理模式')
    parser.add_argument('--weekly-review', action='store_true', help='每周审查模式')
    parser.add_argument('--agent', type=str, default='demo100-agent', help='Agent 名称')
    
    args = parser.parse_args()
    
    if args.auto_organize:
        # 自动整理模式
        if not args.domain:
            print("❌ 需要指定 --domain 参数")
            sys.exit(1)
        
        dk = DomainKnowledge(domain=args.domain)
        result = dk.auto_organize(agent_name=args.agent)
        
    elif args.weekly_review:
        # 每周审查模式
        if not args.domain:
            print("❌ 需要指定 --domain 参数")
            sys.exit(1)
        
        dk = DomainKnowledge(domain=args.domain)
        result = dk.weekly_review(agent_name=args.agent)
        
    elif args.add and args.domain and args.title and args.content:
        # 手动添加知识
        dk = DomainKnowledge(domain=args.domain)
        dk.add_knowledge(
            category=args.category,
            title=args.title,
            content=args.content
        )
        
    else:
        parser.print_help()
