#!/usr/bin/env python3
"""
批量生成记忆 embedding
用于加速语义搜索
"""

import sys
import sqlite3
import json
import urllib.request
import time
from pathlib import Path
from datetime import datetime

# 配置
AGENT_NAME = "ai-baby"
DB_PATH = Path(__file__).parent.parent / "data" / AGENT_NAME / "memory" / "memory_stream.db"
BATCH_SIZE = 20  # 每批处理数量
DELAY_MS = 100   # 请求间隔（避免 Ollama 过载）


def get_embedding(text: str) -> list:
    """获取 Ollama embedding"""
    try:
        payload = {
            "model": "nomic-embed-text",
            "prompt": text[:2000]  # 限制长度
        }
        req = urllib.request.Request(
            'http://localhost:11434/api/embeddings',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req, timeout=30)
        data = json.loads(response.read().decode())
        return data.get('embedding', [])
    except Exception as e:
        print(f"⚠️  Embedding 失败：{e}")
        return []


def main():
    if not DB_PATH.exists():
        print(f"❌ 数据库不存在：{DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 统计需要处理的记忆
    cur.execute('SELECT COUNT(*) FROM memories WHERE embedding = "[]" OR embedding IS NULL OR embedding = ""')
    total = cur.fetchone()[0]
    
    if total == 0:
        print("✅ 所有记忆已有 embedding")
        return
    
    print(f"📊 找到 {total} 条需要生成 embedding 的记忆")
    print(f"🚀 开始批量处理（每批 {BATCH_SIZE} 条）...")
    print()
    
    processed = 0
    failed = 0
    start_time = time.time()
    
    # 分批处理
    offset = 0
    while offset < total or processed + failed < offset:
        cur.execute('''
            SELECT id, content FROM memories 
            WHERE (embedding = "[]" OR embedding IS NULL OR embedding = "")
            LIMIT ? OFFSET ?
        ''', (BATCH_SIZE, offset))
        
        batch = cur.fetchall()
        if not batch:
            break
        
        print(f"📦 处理批次 {offset//BATCH_SIZE + 1}... ({len(batch)} 条)")
        
        for mem_id, content in batch:
            embedding = get_embedding(content)
            
            if embedding:
                cur.execute(
                    'UPDATE memories SET embedding = ? WHERE id = ?',
                    (json.dumps(embedding), mem_id)
                )
                processed += 1
                print(f"  ✅ #{mem_id}: {len(embedding)} 维")
            else:
                failed += 1
                print(f"  ❌ #{mem_id}: 失败")
            
            # 延迟避免过载
            time.sleep(DELAY_MS / 1000)
        
        conn.commit()
        offset += BATCH_SIZE
        
        # 显示进度
        elapsed = time.time() - start_time
        rate = (processed + failed) / elapsed if elapsed > 0 else 0
        print(f"   进度：{processed + failed}/{total} ({rate:.1f} 条/秒)\n")
    
    conn.close()
    
    # 总结
    elapsed = time.time() - start_time
    print("=" * 60)
    print("📊 批量生成完成")
    print(f"   成功：{processed} 条")
    print(f"   失败：{failed} 条")
    print(f"   耗时：{elapsed:.1f} 秒")
    print(f"   平均：{elapsed/(processed+failed):.2f} 秒/条")
    print("=" * 60)


if __name__ == '__main__':
    main()
