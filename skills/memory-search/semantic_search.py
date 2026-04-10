#!/usr/bin/env python3
"""
语义搜索 - 使用 memory_indexer.py 创建的 SQLite 索引

用法:
    python3 skills/memory-search/semantic_search.py "关键词" --top-k 5
"""

import argparse
import json
import sqlite3
import sys
import numpy as np
from pathlib import Path

workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

from path_utils import resolve_workspace

WORKSPACE = resolve_workspace()
INDEX_DB = WORKSPACE / 'data' / 'index' / 'memory_index.db'
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "bge-m3"


def get_embedding(text, model=EMBED_MODEL):
    """从 Ollama 获取向量嵌入"""
    import urllib.request
    
    data = json.dumps({
        "model": model,
        "prompt": text
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{OLLAMA_URL}",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('embedding', [])
    except Exception as e:
        print(f"⚠️  Embedding 失败：{e}", file=sys.stderr)
        return []


def cosine_similarity(a, b):
    """计算余弦相似度"""
    # 如果 b 是 bytes，转换为 numpy 数组
    if isinstance(b, bytes):
        b = np.frombuffer(b, dtype=np.float32)
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def semantic_search(query, top_k=5):
    """语义搜索"""
    if not INDEX_DB.exists():
        print(f"❌ 索引不存在：{INDEX_DB}")
        print("   请先运行：python3 scripts/core/memory_indexer.py --full --embed")
        return []
    
    # 获取查询向量
    print("🔢 生成查询向量...")
    query_embedding = get_embedding(query)
    if not query_embedding:
        print("❌ 无法生成查询向量")
        return []
    
    # 从 SQLite 加载所有向量并计算相似度
    conn = sqlite3.connect(str(INDEX_DB))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 使用 embeddings 表
    cursor.execute("""
        SELECT d.id, d.content, e.vector 
        FROM documents d
        JOIN embeddings e ON d.id = e.doc_id
        WHERE e.vector IS NOT NULL
    """)
    rows = cursor.fetchall()
    conn.close()
    
    # 计算相似度
    results = []
    for row in rows:
        # vector 是 bytes 格式（numpy float32 数组）
        similarity = cosine_similarity(query_embedding, row['vector'])
        results.append({
            'id': row['id'],
            'content': row['content'][:200],
            'similarity': similarity
        })
    
    # 排序并返回 top_k
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]


def main():
    parser = argparse.ArgumentParser(description="语义搜索")
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--top-k', '-k', type=int, default=5, help='返回数量')
    args = parser.parse_args()
    
    print(f"🔍 语义搜索：{args.query}\n")
    
    results = semantic_search(args.query, top_k=args.top_k)
    
    if not results:
        print("   ⏭️  无结果")
        return
    
    print(f"✅ 找到 {len(results)} 条结果:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [相似度：{r['similarity']:.3f}] {r['content']}...")
        print()


if __name__ == "__main__":
    main()
