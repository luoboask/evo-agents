#!/usr/bin/env python3
"""
记忆清理任务 - Memory Cleanup Task
定期清理旧记录，保持索引健康
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta


class MemoryCleanupTask:
    """记忆清理任务"""
    
    def __init__(self, workspace):
        self.workspace = Path(workspace) if isinstance(workspace, str) else workspace
        self.vector_dir = self.workspace / 'memory' / 'vector_db'
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.workspace / 'data' / 'memory_index.db'
    
    def cleanup_old_memories(self, days_old=90, min_importance=3.0):
        """清理旧记忆"""
        cleaned = {
            'sqlite': 0,
            'vector': 0
        }
        
        cutoff = datetime.now() - timedelta(days=days_old)
        
        # 1. 清理 SQLite 索引
        if self.db_path.exists():
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # 删除旧的低重要性记录
            cursor.execute("""
                DELETE FROM memories
                WHERE created_at < ? AND importance < ?
            """, (cutoff.isoformat(), min_importance))
            
            cleaned['sqlite'] = cursor.rowcount
            conn.commit()
            conn.close()
        
        # 2. 清理向量缓存
        cache_file = self.vector_dir / "integrated_cache.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            if isinstance(cache, list):
                original_count = len(cache)
                new_cache = []
                
                for entry in cache:
                    if isinstance(entry, dict):
                        timestamp = entry.get('timestamp', '')
                        importance = entry.get('metadata', {}).get('importance', 5.0)
                        
                        try:
                            ts = datetime.fromisoformat(timestamp)
                            if ts >= cutoff or importance >= min_importance:
                                new_cache.append(entry)
                        except:
                            new_cache.append(entry)
                    else:
                        new_cache.append(entry)
                
                if len(new_cache) < original_count:
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(new_cache, f, ensure_ascii=False, indent=2)
                    
                    cleaned['vector'] = original_count - len(new_cache)
        
        # 输出结果
        if cleaned['sqlite'] > 0 or cleaned['vector'] > 0:
            print(f"✅ 清理完成:")
            print(f"   SQLite 索引：清理 {cleaned['sqlite']} 条")
            print(f"   向量缓存：清理 {cleaned['vector']} 条")
            print(f"   总计：清理 {cleaned['sqlite'] + cleaned['vector']} 条")
        else:
            print("ℹ️  没有需要清理的记录")
        
        return cleaned
    
    def cleanup_empty_files(self):
        """清理空文件"""
        cleaned = 0
        memory_dir = self.workspace / 'memory'
        
        for md_file in memory_dir.glob('*.md'):
            if md_file.stat().st_size == 0:
                md_file.unlink()
                cleaned += 1
                print(f"🗑️  删除空文件：{md_file.name}")
        
        if cleaned > 0:
            print(f"✅ 清理 {cleaned} 个空文件")
        
        return cleaned
    
    def get_cleanup_stats(self):
        """获取清理统计"""
        stats = {
            'total_memories': 0,
            'old_memories': 0,
            'low_importance': 0,
            'empty_files': 0
        }
        
        cutoff_90 = datetime.now() - timedelta(days=90)
        cutoff_30 = datetime.now() - timedelta(days=30)
        
        # 统计 SQLite
        if self.db_path.exists():
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM memories")
            stats['total_memories'] += cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM memories
                WHERE created_at < ?
            """, (cutoff_90.isoformat(),))
            stats['old_memories'] += cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM memories
                WHERE importance < 3.0
            """)
            stats['low_importance'] += cursor.fetchone()[0]
            
            conn.close()
        
        # 统计向量缓存
        cache_file = self.vector_dir / "integrated_cache.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            if isinstance(cache, list):
                stats['total_memories'] += len(cache)
        
        # 统计空文件
        memory_dir = self.workspace / 'memory'
        for md_file in memory_dir.glob('*.md'):
            if md_file.stat().st_size == 0:
                stats['empty_files'] += 1
        
        return stats


if __name__ == '__main__':
    import sys
    
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    task = MemoryCleanupTask(workspace)
    
    if len(sys.argv) > 2:
        if sys.argv[2] == '--cleanup':
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 90
            importance = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
            task.cleanup_old_memories(days, importance)
        elif sys.argv[2] == '--empty':
            task.cleanup_empty_files()
        elif sys.argv[2] == '--stats':
            stats = task.get_cleanup_stats()
            print(f"📊 清理统计:")
            print(f"   总记忆数：{stats['total_memories']}")
            print(f"   90 天前：{stats['old_memories']}")
            print(f"   低重要性：<3.0 的有 {stats['low_importance']}")
            print(f"   空文件：{stats['empty_files']}")
    else:
        print("用法：python3 cleanup.py <workspace> [--cleanup <days> <importance>|--empty|--stats]")
