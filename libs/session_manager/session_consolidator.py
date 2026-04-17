# -*- coding: utf-8 -*-
"""
会话记忆整合器 - 定期将会话记忆整合到长期记忆

功能:
- 识别需要整合的会话记忆
- 过滤低价值记忆
- 批量转移到长期记忆
- 清理已整合的会话记忆
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple
from libs.memory_hub import MemoryHub


class SessionConsolidator:
    """会话记忆整合器"""
    
    def __init__(self, agent_name: str = "default"):
        """
        初始化整合器
        
        Args:
            agent_name: Agent 名称
        """
        self.workspace = Path(__file__).parent.parent.parent
        self.agent_name = agent_name
        
        # 数据路径
        self.data_path = self.workspace / "data" / agent_name
        self.memory_path = self.data_path / "memory"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # 数据库路径
        self.session_db = self.memory_path / "memory_stream.db"
        
        # 整合配置
        self.min_importance = 6.0  # 最低重要性阈值
        self.min_age_hours = 24    # 记忆最小年龄（小时）
        self.batch_size = 50       # 批量整合大小
        
        # 初始化长期记忆 Hub
        self.hub = MemoryHub(agent_name=agent_name)
        
        print(f"📦 会话记忆整合器已初始化 (Agent: {agent_name})")
        print(f"   重要性阈值：{self.min_importance}")
        print(f"   最小年龄：{self.min_age_hours}小时")
        print(f"   批量大小：{self.batch_size}")
    
    def get_consolidation_candidates(self) -> List[Dict]:
        """
        获取待整合的会话记忆
        
        条件:
        - 重要性 >= min_importance
        - 创建时间 >= min_age_hours
        - 未被访问过（last_accessed 较旧）
        
        Returns:
            待整合记忆列表
        """
        if not self.session_db.exists():
            print("⚠️  会话数据库不存在")
            return []
        
        conn = sqlite3.connect(self.session_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cutoff_time = datetime.now() - timedelta(hours=self.min_age_hours)
        
        cursor.execute('''
            SELECT id, session_id, content, memory_type, importance, tags, metadata, created_at
            FROM session_memories
            WHERE importance >= ?
              AND created_at <= ?
              AND last_accessed <= ?
            ORDER BY importance DESC, created_at ASC
            LIMIT ?
        ''', (
            self.min_importance,
            cutoff_time.isoformat(),
            cutoff_time.isoformat(),
            self.batch_size
        ))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        print(f"📊 找到 {len(results)} 条待整合记忆")
        return results
    
    def should_consolidate(self, session_memory: Dict) -> bool:
        """
        判断会话记忆是否应该整合到长期记忆
        
        规则:
        - observation 类型：默认不整合，除非重要性 >= 8.0
        - reflection/goal/knowledge 类型：可以整合
        - 避免会话隐私泄露
        
        Args:
            session_memory: 会话记忆字典
        
        Returns:
            是否应该整合
        """
        memory_type = session_memory.get('memory_type', 'observation')
        importance = session_memory.get('importance', 5.0)
        
        # 1. 用户对话（observation）默认私有
        if memory_type == 'observation':
            # 只有重要性很高（>= 8.0）才整合
            if importance < 8.0:
                return False
            
            # 高重要性对话，标记为私有
            return True
        
        # 2. 反思、目标、知识可以整合
        if memory_type in ['reflection', 'goal', 'knowledge']:
            return True
        
        # 3. 其他类型默认不整合
        return False
    
    def consolidate_memory(self, session_memory: Dict) -> Tuple[bool, int]:
        """
        整合单条会话记忆到长期记忆
        
        Args:
            session_memory: 会话记忆字典
        
        Returns:
            (success, memory_id) - 是否成功，长期记忆 ID
        """
        try:
            # 首先判断是否应该整合
            if not self.should_consolidate(session_memory):
                print(f"   ⏭️  跳过：{session_memory['content'][:50]}... (隐私保护)")
                return False, -1
            
            # 解析标签和元数据（可能已经是列表/字典）
            tags_raw = session_memory.get('tags', '[]')
            if isinstance(tags_raw, str):
                tags = json.loads(tags_raw)
            else:
                tags = tags_raw
            
            metadata_raw = session_memory.get('metadata', '{}')
            if isinstance(metadata_raw, str):
                metadata = json.loads(metadata_raw)
            else:
                metadata = metadata_raw or {}
            
            # 添加会话来源标记和隐私标记
            metadata['source'] = 'session_consolidation'
            metadata['original_session_id'] = session_memory['session_id']
            metadata['consolidated_at'] = datetime.now().isoformat()
            
            # 隐私标记：observation 类型标记为私有
            memory_type = session_memory.get('memory_type', 'observation')
            metadata['is_private'] = (memory_type == 'observation')
            
            # 添加到长期记忆
            memory_id = self.hub.add(
                content=session_memory['content'],
                memory_type=memory_type,
                importance=session_memory.get('importance', 5.0),
                tags=tags,
                metadata=metadata
            )
            
            # 关联到统一索引
            try:
                from scripts.core.unified_index import UnifiedIndex
                index = UnifiedIndex()
                index.link_memory_to_solution(
                    memory_id=memory_id,
                    solution_id=session_memory['id']  # 使用会话记忆 ID 作为临时方案 ID
                )
            except Exception as e:
                print(f"   ⚠️  统一索引关联失败：{e}")
            
            return True, memory_id
        
        except Exception as e:
            print(f"   ❌ 整合失败：{e}")
            return False, -1
    
    def cleanup_consolidated(self, session_memory_ids: List[int]):
        """
        清理已整合的会话记忆
        
        Args:
            session_memory_ids: 已整合的会话记忆 ID 列表
        """
        if not session_memory_ids:
            return
        
        conn = sqlite3.connect(self.session_db)
        cursor = conn.cursor()
        
        # 删除已整合的记忆
        placeholders = ','.join('?' * len(session_memory_ids))
        cursor.execute(f'''
            DELETE FROM session_memories
            WHERE id IN ({placeholders})
        ''', session_memory_ids)
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"🧹 已清理 {deleted} 条已整合的会话记忆")
    
    def run_consolidation(self) -> Dict:
        """
        执行完整整合流程
        
        Returns:
            整合统计
        """
        print("\n" + "="*60)
        print("🔄 开始会话记忆整合")
        print("="*60)
        
        stats = {
            'candidates': 0,
            'consolidated': 0,
            'failed': 0,
            'cleaned': 0
        }
        
        # 1. 获取候选记忆
        candidates = self.get_consolidation_candidates()
        stats['candidates'] = len(candidates)
        
        if not candidates:
            print("✅ 无需整合")
            return stats
        
        # 2. 批量整合
        print(f"\n📝 开始整合 {len(candidates)} 条记忆...")
        print(f"   🔒 隐私保护：只整合 reflection/goal/knowledge，或重要性 >= 8.0 的 observation")
        
        consolidated_ids = []
        failed_ids = []
        skipped_ids = []
        
        for i, memory in enumerate(candidates, 1):
            # 预检查
            if not self.should_consolidate(memory):
                skipped_ids.append(memory['id'])
                continue
            
            success, mem_id = self.consolidate_memory(memory)
            
            if success:
                consolidated_ids.append(memory['id'])
                stats['consolidated'] += 1
                
                if i % 10 == 0:
                    print(f"   已整合 {i}/{len(candidates)} 条")
            else:
                failed_ids.append(memory['id'])
                stats['failed'] += 1
        
        stats['skipped'] = len(skipped_ids)
        
        # 3. 清理已整合的会话记忆
        if consolidated_ids:
            self.cleanup_consolidated(consolidated_ids)
            stats['cleaned'] = len(consolidated_ids)
        
        # 4. 输出统计
        print("\n" + "="*60)
        print("📊 整合完成")
        print("="*60)
        print(f"   候选记忆：{stats['candidates']}")
        print(f"   成功整合：{stats['consolidated']}")
        print(f"   跳过（隐私保护）：{stats.get('skipped', 0)}")
        print(f"   失败：{stats['failed']}")
        print(f"   已清理：{stats['cleaned']}")
        
        if stats['failed'] > 0:
            print(f"\n⚠️  {stats['failed']} 条记忆整合失败，请检查日志")
        
        return stats
    
    def get_stats(self) -> Dict:
        """获取会话记忆统计"""
        if not self.session_db.exists():
            return {'total': 0, 'by_type': {}, 'avg_importance': 0}
        
        conn = sqlite3.connect(self.session_db)
        cursor = conn.cursor()
        
        stats = {}
        
        # 总量
        cursor.execute('SELECT COUNT(*) FROM session_memories')
        stats['total'] = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute('''
            SELECT memory_type, COUNT(*) 
            FROM session_memories 
            GROUP BY memory_type
        ''')
        stats['by_type'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 平均重要性
        cursor.execute('SELECT AVG(importance) FROM session_memories')
        stats['avg_importance'] = cursor.fetchone()[0] or 0.0
        
        # 最旧记忆
        cursor.execute('SELECT MIN(created_at) FROM session_memories')
        stats['oldest'] = cursor.fetchone()[0]
        
        conn.close()
        return stats


def main():
    """命令行使用"""
    import argparse
    
    parser = argparse.ArgumentParser(description='会话记忆整合器')
    parser.add_argument('--agent', type=str, default='default', help='Agent 名称')
    parser.add_argument('--min-importance', type=float, default=6.0, help='最低重要性阈值')
    parser.add_argument('--min-age', type=int, default=24, help='最小年龄（小时）')
    parser.add_argument('--batch-size', type=int, default=50, help='批量大小')
    parser.add_argument('--stats', action='store_true', help='只显示统计')
    
    args = parser.parse_args()
    
    # 创建整合器
    consolidator = SessionConsolidator(agent_name=args.agent)
    consolidator.min_importance = args.min_importance
    consolidator.min_age_hours = args.min_age
    consolidator.batch_size = args.batch_size
    
    if args.stats:
        # 只显示统计
        stats = consolidator.get_stats()
        print("\n📊 会话记忆统计")
        print("="*60)
        print(f"总量：{stats['total']}")
        print(f"平均重要性：{stats['avg_importance']:.2f}")
        print(f"按类型：{stats['by_type']}")
        print(f"最旧记忆：{stats['oldest']}")
    else:
        # 执行整合
        result = consolidator.run_consolidation()
        
        # 返回退出码
        if result['failed'] > 0:
            exit(1)


if __name__ == "__main__":
    main()
