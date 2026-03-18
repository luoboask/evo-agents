#!/usr/bin/env python3
"""
SQLite 记忆搜索 - 直接查询 ai-baby_memory_stream.db
支持关键词匹配和简单语义搜索
"""

import argparse
import sqlite3
import json
from pathlib import Path
from datetime import datetime


class SQLiteMemorySearch:
    """SQLite 记忆搜索"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path("/Users/dhr/.openclaw/workspace-ai-baby/memory/ai-baby_memory_stream.db")
        self.db_path = Path(db_path)
    
    def search(self, query, top_k=10, memory_type=None):
        """
        搜索记忆
        
        Args:
            query: 查询关键词
            top_k: 返回数量
            memory_type: 过滤类型 (observation/goal/reflection/etc)
        """
        if not self.db_path.exists():
            return []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 基础查询
        if memory_type:
            cur.execute('''
                SELECT id, content, memory_type, importance, tags, created_at, last_accessed
                FROM memories
                WHERE content LIKE ? OR tags LIKE ?
                AND memory_type = ?
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', memory_type, top_k))
        else:
            cur.execute('''
                SELECT id, content, memory_type, importance, tags, created_at, last_accessed
                FROM memories
                WHERE content LIKE ? OR tags LIKE ?
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', top_k))
        
        results = [dict(row) for row in cur.fetchall()]
        
        # 更新 last_accessed
        if results:
            cur.execute('''
                UPDATE memories
                SET last_accessed = ?
                WHERE id IN ({})
            '''.format(','.join('?' * len(results))),
            [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + [r['id'] for r in results])
            conn.commit()
        
        conn.close()
        return results
    
    def add(self, content, memory_type='observation', importance=5.0, tags=None):
        """添加记忆"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        tags_json = json.dumps(tags or [])
        cur.execute('''
            INSERT INTO memories (content, memory_type, importance, tags, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (content, memory_type, importance, tags_json, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        conn.close()
        return cur.lastrowid
    
    def list_all(self, limit=20):
        """列出所有记忆"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute('''
            SELECT id, content, memory_type, importance, tags, created_at
            FROM memories
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        results = [dict(row) for row in cur.fetchall()]
        conn.close()
        return results
    
    def stats(self):
        """统计信息"""
        if not self.db_path.exists():
            return {"error": "Database not found"}
        
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
            "total": total,
            "by_type": by_type,
            "avg_importance": round(avg_importance, 2),
            "db_path": str(self.db_path)
        }


# ═══════════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='SQLite 记忆搜索')
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--add', '-a', help='添加记忆')
    parser.add_argument('--type', '-t', default='observation', help='记忆类型 (observation/goal/reflection)')
    parser.add_argument('--importance', '-i', type=float, default=5.0, help='重要性 (1-10)')
    parser.add_argument('--tags', help='标签 (逗号分隔)')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有记忆')
    parser.add_argument('--stats', '-s', action='store_true', help='统计信息')
    parser.add_argument('--limit', '-n', type=int, default=10, help='返回数量')
    
    args = parser.parse_args()
    search = SQLiteMemorySearch()
    
    # 添加记忆
    if args.add:
        tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
        mem_id = search.add(args.add, args.type, args.importance, tags)
        print(f"✅ 已添加记忆 #{mem_id}")
        return
    
    # 统计
    if args.stats:
        stats = search.stats()
        print("📊 记忆统计:")
        print(f"  数据库：{stats.get('db_path', 'N/A')}")
        print(f"  总数：{stats.get('total', 0)}")
        print(f"  平均重要性：{stats.get('avg_importance', 0)}")
        print(f"  按类型：{stats.get('by_type', {})}")
        return
    
    # 列出所有
    if args.list:
        memories = search.list_all(args.limit)
        print(f"📝 最近 {len(memories)} 条记忆:\n")
        for m in memories:
            tags = json.loads(m.get('tags', '[]'))
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"  [{m['id']}] {m['content']}")
            print(f"      类型：{m['memory_type']} | 重要性：{m['importance']} | {m['created_at']}{tag_str}")
            print()
        return
    
    # 搜索
    if args.query:
        results = search.search(args.query, args.limit)
        print(f"🔍 搜索：{args.query}\n")
        if not results:
            print("  未找到相关记忆")
        else:
            for r in results:
                tags = json.loads(r.get('tags', '[]'))
                tag_str = f" [{', '.join(tags)}]" if tags else ""
                print(f"  [{r['id']}] {r['content']}")
                print(f"      类型：{r['memory_type']} | 重要性：{r['importance']} | {r['created_at']}{tag_str}")
                print()
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == '__main__':
    main()
