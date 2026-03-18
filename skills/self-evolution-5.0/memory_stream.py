#!/usr/bin/env python3
"""
记忆流系统 - 基于 Generative Agents 论文
https://github.com/joonspk-research/generative_agents

核心架构：
1. 记忆流 (Memory Stream) - 按时间存储所有经历
2. 反思生成 (Reflection Generation) - 定期从记忆生成抽象洞察
3. 检索函数 (Retrieval Function) - 根据近因性、重要性、相关性检索
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import math


@dataclass
class Memory:
    """单条记忆"""
    id: int
    content: str
    created_at: str
    memory_type: str  # observation, reflection, goal
    importance: float  # 1-10
    tags: List[str]
    last_accessed: str = None
    
    def to_dict(self):
        return asdict(self)


class MemoryStream:
    """
    记忆流系统（支持多 Agent 数据隔离）
    
    记忆类型：
    - observation: 原始观察/经历
    - reflection: 反思/洞察（从 observation 生成）
    - goal: 目标/意图
    
    数据隔离模式：
    - agent_id 指定：独立数据库（私有记忆）
    - shared=True: 共享数据库（公共知识）
    - 都不指定：默认数据库
    """
    
    def __init__(self, agent_id: str = None, shared: bool = False, db_path: str = None):
        if db_path:
            # 显式指定路径
            self.db_path = db_path
        elif shared:
            # 共享数据库（公共知识）
            self.db_path = '/Users/dhr/.openclaw/workspace-ai-baby/memory/memory_stream_shared.db'
        elif agent_id:
            # 独立数据库（私有记忆）
            self.db_path = f'/Users/dhr/.openclaw/workspace-ai-baby/memory/{agent_id}_memory_stream.db'
        else:
            # 默认数据库
            self.db_path = '/Users/dhr/.openclaw/workspace-ai-baby/memory/memory_stream.db'
        
        self.agent_id = agent_id
        self.shared = shared
        self.init_db()
        
        if agent_id:
            print(f"🧠 记忆流已初始化（Agent: {agent_id}）")
        elif shared:
            print(f"🧠 记忆流已初始化（共享模式）")
        else:
            print(f"🧠 记忆流已初始化（默认）")
        print(f"   数据库：{self.db_path}")
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 记忆表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance REAL DEFAULT 5.0,
                tags TEXT,
                last_accessed TEXT,
                embedding TEXT,
                metadata TEXT
            )
        ''')
        
        # 反思关联表（记录哪些记忆生成了哪些反思）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reflection_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_memory_ids TEXT NOT NULL,
                reflection_memory_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reflection_memory_id) REFERENCES memories(id)
            )
        ''')
        
        # 索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON memories(memory_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON memories(tags)')
        
        conn.commit()
        conn.close()
        print(f"✅ 记忆流数据库已初始化：{self.db_path}")
    
    def add_memory(self, content: str, memory_type: str = 'observation',
                   importance: float = None, tags: List[str] = None,
                   metadata: Dict = None) -> int:
        """
        添加记忆到记忆流
        
        Args:
            content: 记忆内容
            memory_type: observation/reflection/goal
            importance: 重要性 1-10（可选，自动计算）
            tags: 标签列表
            metadata: 额外元数据
        
        Returns:
            记忆 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        tags_json = json.dumps(tags or [], ensure_ascii=False)
        metadata_json = json.dumps(metadata or {}, ensure_ascii=False)
        
        # 自动计算重要性（如果没有提供）
        if importance is None:
            importance = self._calculate_importance(content, memory_type)
        
        cursor.execute('''
            INSERT INTO memories 
            (content, created_at, memory_type, importance, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (content, now, memory_type, importance, tags_json, metadata_json))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"  📝 [{memory_type}] {content[:50]}... (重要性：{importance:.1f})")
        return memory_id
    
    def _calculate_importance(self, content: str, memory_type: str) -> float:
        """
        自动计算记忆重要性（1-10）
        
        规则：
        - reflection > observation
        - 包含情感词汇 → 更高
        - 包含行动词汇 → 更高
        - 长度适中 → 更高
        """
        base_score = 5.0
        
        # 类型基础分
        if memory_type == 'reflection':
            base_score += 2.0
        elif memory_type == 'goal':
            base_score += 1.5
        
        # 关键词加分
        importance_keywords = ['必须', '重要', '关键', '紧急', '决定', '发现', '突破', '教训']
        for kw in importance_keywords:
            if kw in content:
                base_score += 0.5
        
        # 行动词汇
        action_keywords = ['开始', '完成', '修复', '创建', '实现', '改进']
        for kw in action_keywords:
            if kw in content:
                base_score += 0.3
        
        return min(10.0, max(1.0, base_score))
    
    def get_memories(self, memory_type: str = None, limit: int = 50,
                     recent_hours: int = None) -> List[Memory]:
        """获取记忆"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM memories WHERE 1=1'
        params = []
        
        if memory_type:
            query += ' AND memory_type = ?'
            params.append(memory_type)
        
        if recent_hours:
            cutoff = (datetime.now() - timedelta(hours=recent_hours)).isoformat()
            query += ' AND created_at >= ?'
            params.append(cutoff)
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [Memory(
            id=row['id'],
            content=row['content'],
            created_at=row['created_at'],
            memory_type=row['memory_type'],
            importance=row['importance'],
            tags=json.loads(row['tags'] or '[]'),
            last_accessed=row['last_accessed']
        ) for row in rows]
    
    def retrieve_by_relevance(self, query: str, limit: int = 10) -> List[Tuple[Memory, float]]:
        """
        根据相关性检索记忆（Generative Agents 核心算法）
        
        检索分数 = 近因性 × 0.3 + 重要性 × 0.3 + 相关性 × 0.4
        
        Returns:
            [(Memory, score), ...] 按分数降序
        """
        memories = self.get_memories(limit=100)
        
        scored_memories = []
        now = datetime.now()
        
        for mem in memories:
            # 1. 近因性 (Recency) - 越近越高
            mem_time = datetime.fromisoformat(mem.created_at)
            hours_ago = (now - mem_time).total_seconds() / 3600
            recency_score = math.exp(-hours_ago / 24)  # 24 小时半衰期
            
            # 2. 重要性 (Importance) - 归一化
            importance_score = mem.importance / 10.0
            
            # 3. 相关性 (Relevance) - 简单关键词匹配
            query_words = set(query.lower().split())
            content_words = set(mem.content.lower().split())
            overlap = len(query_words & content_words)
            relevance_score = min(1.0, overlap / max(1, len(query_words)))
            
            # 综合分数
            total_score = (
                recency_score * 0.3 +
                importance_score * 0.3 +
                relevance_score * 0.4
            )
            
            scored_memories.append((mem, total_score))
        
        # 按分数降序
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        # 更新最后访问时间
        for mem, _ in scored_memories[:limit]:
            self._update_last_accessed(mem.id)
        
        return scored_memories[:limit]
    
    def _update_last_accessed(self, memory_id: int):
        """更新最后访问时间"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE memories SET last_accessed = ? WHERE id = ?
        ''', (datetime.now().isoformat(), memory_id))
        conn.commit()
        conn.close()
    
    def generate_reflections(self, lookback_hours: int = 24, 
                            min_memories: int = 5) -> List[int]:
        """
        从观察记忆生成反思（核心认知机制）
        
        算法：
        1. 获取过去 N 小时的观察记忆
        2. 聚类相似记忆
        3. 为每个聚类生成反思
        4. 将反思存回记忆流
        
        Returns:
            新生成的反思记忆 ID 列表
        """
        observations = self.get_memories(
            memory_type='observation',
            recent_hours=lookback_hours,
            limit=100
        )
        
        if len(observations) < min_memories:
            print(f"  ⚠️ 观察记忆不足 {min_memories} 条，跳过反思生成")
            return []
        
        print(f"  🧠 从 {len(observations)} 条观察记忆生成反思...")
        
        # 简单聚类：按领域/主题分组
        clusters = self._cluster_memories(observations)
        
        reflection_ids = []
        for cluster_topic, cluster_memories in clusters.items():
            # 生成反思
            reflection_content = self._generate_reflection_from_cluster(
                cluster_topic, cluster_memories
            )
            
            if reflection_content:
                # 存回记忆流
                reflection_id = self.add_memory(
                    content=reflection_content,
                    memory_type='reflection',
                    tags=[cluster_topic],
                    metadata={
                        'source_count': len(cluster_memories),
                        'source_ids': [m.id for m in cluster_memories]
                    }
                )
                reflection_ids.append(reflection_id)
                
                # 记录关联
                self._link_reflection(reflection_id, [m.id for m in cluster_memories])
        
        return reflection_ids
    
    def _cluster_memories(self, memories: List[Memory]) -> Dict[str, List[Memory]]:
        """简单聚类：按标签/领域分组"""
        clusters = {}
        
        for mem in memories:
            # 从标签或内容提取主题
            if mem.tags:
                topic = mem.tags[0]
            else:
                # 简单提取：假设内容格式为"领域/主题：内容"
                if '/' in mem.content:
                    topic = mem.content.split('/')[0].strip()
                else:
                    topic = 'general'
            
            if topic not in clusters:
                clusters[topic] = []
            clusters[topic].append(mem)
        
        return clusters
    
    def _generate_reflection_from_cluster(self, topic: str, 
                                          memories: List[Memory]) -> Optional[str]:
        """从记忆聚类生成反思"""
        if not memories:
            return None
        
        # 提取共同模式
        contents = [m.content for m in memories]
        avg_importance = sum(m.importance for m in memories) / len(memories)
        
        # 生成反思模板
        reflection = f"在{topic}领域：基于{len(memories)}次经历，发现模式 - "
        
        # 提取关键洞察
        if len(memories) >= 3:
            reflection += f"反复出现的主题需要重点关注。平均重要性：{avg_importance:.1f}/10。"
        
        # 行动建议
        if avg_importance >= 7:
            reflection += "建议：这是高优先级领域，应该投入更多时间。"
        elif avg_importance <= 4:
            reflection += "建议：考虑是否需要继续投入精力。"
        
        return reflection
    
    def _link_reflection(self, reflection_id: int, source_ids: List[int]):
        """记录反思与源记忆的关联"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reflection_links (source_memory_ids, reflection_memory_id)
            VALUES (?, ?)
        ''', (json.dumps(source_ids), reflection_id))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """获取记忆统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute('SELECT COUNT(*) FROM memories')
        total = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute('''
            SELECT memory_type, COUNT(*) as count, AVG(importance) as avg_importance
            FROM memories
            GROUP BY memory_type
        ''')
        by_type = {
            row[0]: {'count': row[1], 'avg_importance': row[2]}
            for row in cursor.fetchall()
        }
        
        # 最近 24 小时
        cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute('SELECT COUNT(*) FROM memories WHERE created_at >= ?', (cutoff,))
        recent_24h = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_memories': total,
            'by_type': by_type,
            'recent_24h': recent_24h
        }


# 使用示例
if __name__ == '__main__':
    ms = MemoryStream()
    
    print("=" * 60)
    print("🧠 记忆流系统演示")
    print("=" * 60)
    
    # 添加观察记忆
    print("\n📝 添加观察记忆:")
    ms.add_memory(
        content="实现了/api/knowledge 端点，支持知识库内容查询",
        memory_type='observation',
        tags=['系统进化', 'API 开发']
    )
    
    ms.add_memory(
        content="修复知识库表结构，添加 thinking 和 key_point 字段",
        memory_type='observation',
        tags=['系统进化', 'Bug 修复']
    )
    
    ms.add_memory(
        content="学习 Generative Agents 记忆架构，理解记忆流 + 反思生成机制",
        memory_type='observation',
        tags=['学习', 'AI 架构'],
        importance=8.0
    )
    
    ms.add_memory(
        content="将假学习系统改为真实记录器，停止自动生成假数据",
        memory_type='observation',
        tags=['系统进化', '代码改进'],
        importance=9.0
    )
    
    # 添加目标记忆
    print("\n🎯 添加目标记忆:")
    ms.add_memory(
        content="本周实现分形思考 Level 1 模式识别模块",
        memory_type='goal',
        tags=['目标', '系统进化'],
        importance=8.0
    )
    
    # 生成反思
    print("\n🤔 生成反思:")
    reflection_ids = ms.generate_reflections(lookback_hours=24, min_memories=2)
    print(f"   生成了 {len(reflection_ids)} 条反思")
    
    # 检索相关记忆
    print("\n🔍 检索相关记忆 (查询：'API 开发'):")
    results = ms.retrieve_by_relevance("API 开发", limit=5)
    for mem, score in results:
        print(f"   [{score:.2f}] {mem.content[:60]}...")
    
    # 统计
    print("\n📊 记忆统计:")
    stats = ms.get_stats()
    print(f"   总记忆数：{stats['total_memories']}")
    print(f"   最近 24 小时：{stats['recent_24h']}")
    for mtype, data in stats['by_type'].items():
        print(f"   - {mtype}: {data['count']}条 (平均重要性：{data['avg_importance']:.1f})")
    
    print("\n" + "=" * 60)
