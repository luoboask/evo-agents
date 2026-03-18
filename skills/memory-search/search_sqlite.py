#!/usr/bin/env python3
"""
SQLite 记忆搜索 - 直接查询 ai-baby_memory_stream.db
支持关键词匹配 + Ollama 向量语义搜索
"""

import argparse
import sqlite3
import json
import subprocess
from pathlib import Path
from datetime import datetime


def get_embedding(text):
    """使用 Ollama 生成嵌入向量"""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/embeddings",
             "-H", "Content-Type: application/json",
             "-d", json.dumps({"model": "nomic-embed-text", "prompt": text[:500]})],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("embedding", [])
    except Exception as e:
        pass
    return []


def cosine_similarity(a, b):
    """计算余弦相似度"""
    if not a or not b:
        return 0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


class SQLiteMemorySearch:
    """SQLite 记忆搜索"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path("/Users/dhr/.openclaw/workspace-ai-baby/memory/ai-baby_memory_stream.db")
        self.db_path = Path(db_path)
    
    def search(self, query, top_k=10, memory_type=None, semantic=False):
        """
        搜索记忆
        
        Args:
            query: 查询关键词
            top_k: 返回数量
            memory_type: 过滤类型 (observation/goal/reflection/etc)
            semantic: 是否使用向量语义搜索 (需要 Ollama)
        """
        if not self.db_path.exists():
            return []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 获取所有记忆
        if memory_type:
            cur.execute('''
                SELECT id, content, memory_type, importance, tags, created_at, last_accessed, embedding
                FROM memories
                WHERE memory_type = ?
                ORDER BY created_at DESC
            ''', (memory_type,))
        else:
            cur.execute('''
                SELECT id, content, memory_type, importance, tags, created_at, last_accessed, embedding
                FROM memories
                ORDER BY created_at DESC
            ''')
        
        all_memories = [dict(row) for row in cur.fetchall()]
        
        if semantic:
            # 向量语义搜索
            query_embedding = get_embedding(query)
            if query_embedding:
                results = []
                for m in all_memories:
                    embedding = json.loads(m.get('embedding') or '[]')
                    if embedding:
                        similarity = cosine_similarity(query_embedding, embedding)
                        if similarity > 0.5:  # 阈值
                            m['score'] = similarity
                            results.append(m)
                
                # 按相似度排序
                results.sort(key=lambda x: -x['score'])
                final_results = results[:top_k]
                
                # 更新访问时间
                if final_results:
                    cur.execute('''
                        UPDATE memories
                        SET last_accessed = ?
                        WHERE id IN ({})
                    '''.format(','.join('?' * len(final_results))),
                    [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + [r['id'] for r in final_results])
                    conn.commit()
                
                conn.close()
                return final_results
        
        # 关键词匹配 (fallback)
        keyword_results = []
        query_lower = query.lower()
        for m in all_memories:
            if query_lower in m['content'].lower() or query_lower in m.get('tags', '').lower():
                m['score'] = 1.0
                keyword_results.append(m)
        
        keyword_results.sort(key=lambda x: -x['importance'])
        final_results = keyword_results[:top_k]
        
        # 更新访问时间
        if final_results:
            cur.execute('''
                UPDATE memories
                SET last_accessed = ?
                WHERE id IN ({})
            '''.format(','.join('?' * len(final_results))),
            [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + [r['id'] for r in final_results])
            conn.commit()
        
        conn.close()
        return final_results
    
    def add(self, content, memory_type='observation', importance=5.0, tags=None, with_embedding=False, details=None, source_url=None):
        """添加记忆
        
        Args:
            content: 记忆摘要
            memory_type: 类型 (observation/goal/reflection/knowledge)
            importance: 重要性 (1-10)
            tags: 标签列表
            with_embedding: 是否生成向量嵌入
            details: 详细知识内容 (字典或字符串)
            source_url: 来源 URL
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        tags_json = json.dumps(tags or [])
        embedding_json = '[]'
        
        # 构建元数据（包含知识详情）
        metadata = {
            'details': details,
            'source_url': source_url,
            'content_length': len(content)
        }
        metadata_json = json.dumps(metadata, ensure_ascii=False)
        
        # 生成向量嵌入 (可选)
        if with_embedding:
            embedding = get_embedding(content + (details if isinstance(details, str) else json.dumps(details)))
            if embedding:
                embedding_json = json.dumps(embedding)
        
        cur.execute('''
            INSERT INTO memories (content, memory_type, importance, tags, embedding, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (content, memory_type, importance, tags_json, embedding_json, metadata_json, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
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
    parser.add_argument('--semantic', action='store_true', help='使用向量语义搜索 (需要 Ollama)')
    parser.add_argument('--with-embedding', action='store_true', help='添加时生成向量嵌入')
    parser.add_argument('--details', '-d', help='知识详情 (长文本或 JSON)')
    parser.add_argument('--source', help='来源 URL')
    
    args = parser.parse_args()
    search = SQLiteMemorySearch()
    
    # 添加记忆
    if args.add:
        tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
        
        # 解析详情 (支持 JSON 或普通文本)
        details = None
        if args.details:
            try:
                details = json.loads(args.details)
            except:
                details = args.details
        
        mem_id = search.add(args.add, args.type, args.importance, tags, 
                           with_embedding=args.with_embedding, 
                           details=details, 
                           source_url=args.source)
        
        if args.with_embedding:
            print(f"✅ 已添加记忆 #{mem_id} (带向量嵌入)")
        else:
            print(f"✅ 已添加记忆 #{mem_id}")
        
        if args.details:
            detail_len = len(args.details)
            print(f"   详情：{detail_len} 字符")
        if args.source:
            print(f"   来源：{args.source}")
        
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
            metadata = json.loads(m.get('metadata') or '{}')
            has_details = 'details' in metadata and metadata['details']
            source = metadata.get('source_url')
            
            print(f"  [{m['id']}] {m['content']}")
            print(f"      类型：{m['memory_type']} | 重要性：{m['importance']} | {m['created_at']}{tag_str}")
            if has_details:
                details_preview = str(metadata['details'])[:100] + "..." if len(str(metadata['details'])) > 100 else metadata['details']
                print(f"      详情：{details_preview}")
            if source:
                print(f"      来源：{source}")
            print()
        return
    
    # 搜索
    if args.query:
        results = search.search(args.query, args.limit, semantic=args.semantic)
        mode = " (向量语义)" if args.semantic else ""
        print(f"🔍 搜索：{args.query}{mode}\n")
        if not results:
            print("  未找到相关记忆")
        else:
            for r in results:
                tags = json.loads(r.get('tags', '[]'))
                tag_str = f" [{', '.join(tags)}]" if tags else ""
                metadata = json.loads(r.get('metadata') or '{}')
                has_details = 'details' in metadata and metadata['details']
                source = metadata.get('source_url')
                
                print(f"  [{r['id']}] {r['content']}")
                print(f"      类型：{r['memory_type']} | 重要性：{r['importance']} | {r['created_at']}{tag_str}")
                if has_details:
                    details_preview = str(metadata['details'])[:200] + "..." if len(str(metadata['details'])) > 200 else metadata['details']
                    print(f"      详情：{details_preview}")
                if source:
                    print(f"      来源：{source}")
                print()
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == '__main__':
    main()
