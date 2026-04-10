#!/usr/bin/env python3
"""
memory_indexer.py - 记忆索引器

扫描 markdown 文件，构建 SQLite FTS5 全文搜索索引 + Ollama 语义向量。

用法:
    python3 scripts/memory_indexer.py --full          # 全量重建
    python3 scripts/memory_indexer.py --incremental   # 增量更新
    python3 scripts/memory_indexer.py --full --embed   # 全量 + 语义向量
"""

import argparse
import json
import re
import sqlite3
import struct
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    import jieba
    jieba.setLogLevel(20)  # 抑制 jieba 调试日志
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False

from path_utils import resolve_workspace, resolve_data_dir

WORKSPACE = resolve_workspace()

sys.path.insert(0, str(WORKSPACE / "scripts"))
from lock_utils import file_lock, open_db
MEMORY_DIR = WORKSPACE / "memory"
INDEX_DIR = WORKSPACE / "data" / "index"
DB_PATH = INDEX_DIR / "memory_index.db"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "bge-m3"


def tokenize(text: str) -> str:
    """中文分词：用空格分隔，让 FTS5 能正确索引中文"""
    if HAS_JIEBA:
        return " ".join(jieba.cut_for_search(text))
    return text


def get_db_path() -> Path:
    """获取数据库路径"""
    return resolve_data_dir("index") / "memory_index.db"

def init_db(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            line_start INTEGER NOT NULL,
            line_end INTEGER NOT NULL,
            content TEXT NOT NULL,
            content_tokenized TEXT DEFAULT '',
            type TEXT DEFAULT 'unknown',
            date TEXT,
            mtime REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS file_state (
            path TEXT PRIMARY KEY,
            mtime REAL NOT NULL,
            indexed_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS embeddings (
            doc_id INTEGER PRIMARY KEY,
            vector BLOB NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        );
    """)
    # 检查 FTS 表是否存在，不存在则创建
    existing = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='documents_fts'"
    ).fetchone()
    if not existing:
        conn.executescript("""
            CREATE VIRTUAL TABLE documents_fts USING fts5(
                content_tokenized, type, date,
                content='documents', content_rowid='id'
            );
            CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
                INSERT INTO documents_fts(rowid, content_tokenized, type, date)
                VALUES (new.id, new.content_tokenized, new.type, new.date);
            END;
            CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
                INSERT INTO documents_fts(documents_fts, rowid, content_tokenized, type, date)
                VALUES ('delete', old.id, old.content_tokenized, old.type, old.date);
            END;
        """)


def detect_type(line: str) -> str:
    if any(k in line for k in ["事件", "观察"]):
        return "event"
    if "决定" in line:
        return "decision"
    if any(k in line for k in ["学习", "知识"]):
        return "learning"
    if "反思" in line:
        return "reflection"
    if any(k in line for k in ["待办", "目标", "- [ ]", "- [x]"]):
        return "todo"
    return "unknown"


def extract_date_from_path(filepath: Path) -> Optional[str]:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    return match.group(1) if match else None


def parse_md_chunks(filepath: Path) -> List[dict]:
    """将 markdown 拆分为细粒度块：每个列表项独立成块，提升语义搜索精度"""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    chunks = []
    current_type = "unknown"
    current_section = ""
    file_date = extract_date_from_path(filepath)

    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            current_type = detect_type(line)
            current_section = line.strip()
            continue
        if line.startswith("# "):
            continue

        stripped = line.strip()
        # 列表项：每条独立成块
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            # 去掉时间前缀和 checkbox
            item_clean = re.sub(r'^\[\d{2}:\d{2}\]\s*', '', item)
            item_clean = re.sub(r'^\[[ x]\]\s*', '', item_clean)
            if item_clean and len(item_clean) > 3:
                chunks.append({
                    "content": item_clean,
                    "line_start": i,
                    "line_end": i,
                    "type": current_type,
                    "date": file_date,
                })
        # 非列表的有内容段落（标题、描述等）
        elif stripped and len(stripped) > 10 and not stripped.startswith("**"):
            chunks.append({
                "content": stripped,
                "line_start": i,
                "line_end": i,
                "type": current_type,
                "date": file_date,
            })

    return chunks




def hybrid_search(query, top_k=10):
    """混合搜索（关键词 + 语义）"""
    import numpy as np
    
    if not DB_PATH.exists():
        return []
    
    # 1. 关键词搜索
    keyword_results = keyword_search(query, top_k=top_k * 2)
    
    # 2. 语义搜索
    semantic_results = []
    query_embedding = get_embedding(query)
    if query_embedding:
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT doc_id, vector FROM embeddings")
            for row in cursor.fetchall():
                # 正确读取 BLOB 向量
                try:
                    vector_bytes = bytes(row['vector'])
                    doc_embedding = np.frombuffer(vector_bytes, dtype=np.float32)
                except Exception as e:
                    print(f"Vector read error: {e}")
                    continue
                
                # 计算余弦相似度
                query_vec = np.array(query_embedding, dtype=np.float32)
                similarity = float(np.dot(query_vec, doc_embedding) / 
                                 (np.linalg.norm(query_vec) * np.linalg.norm(doc_embedding)))
                
                # 获取文档内容
                cursor.execute("SELECT id, content, path, type FROM documents WHERE id = ?", (row['doc_id'],))
                doc_row = cursor.fetchone()
                if doc_row:
                    semantic_results.append({
                        'id': doc_row['id'],
                        'content': doc_row['content'][:500],
                        'source': doc_row['path'],
                        'type': doc_row['type'],
                        'score': similarity,
                        'search_type': 'semantic'
                    })
            
            conn.close()
            semantic_results.sort(key=lambda x: x['score'], reverse=True)
            semantic_results = semantic_results[:top_k * 2]
        except Exception as e:
            print(f"Semantic search error: {e}")
    
    # 3. 合并结果
    merged = {}
    for r in keyword_results + semantic_results:
        doc_id = r['id']
        if doc_id not in merged:
            merged[doc_id] = r
        else:
            if r['search_type'] == 'keyword':
                merged[doc_id]['keyword_score'] = r.get('score', 0)
            else:
                merged[doc_id]['semantic_score'] = r.get('score', 0)
    
    # 4. 加权排序
    final_results = []
    for doc_id, r in merged.items():
        keyword_score = r.get('keyword_score', 0)
        semantic_score = r.get('semantic_score', 0)
        
        if r['search_type'] == 'keyword' and keyword_score > 0:
            keyword_score = min(keyword_score / 10.0, 1.0)
        
        combined_score = 0.6 * keyword_score + 0.4 * semantic_score
        r['combined_score'] = combined_score
        final_results.append(r)
    
    final_results.sort(key=lambda x: x['combined_score'], reverse=True)
    return final_results[:top_k]

def get_embedding(text: str, prefix: str = "search_document: ") -> Optional[bytes]:
    """使用 Ollama 生成嵌入向量，加 nomic 推荐的 task prefix"""
    try:
        result = subprocess.run(
            ["curl", "-s", OLLAMA_URL,
             "-H", "Content-Type: application/json",
             "-d", json.dumps({"model": EMBED_MODEL, "prompt": prefix + text[:500]})],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "embedding" in data:
                vec = data["embedding"]
                return struct.pack(f"{len(vec)}f", *vec)
    except Exception:
        pass
    return None


def collect_md_files() -> List[Path]:
    files = []
    memory_md = WORKSPACE / "MEMORY.md"
    if memory_md.exists():
        files.append(memory_md)
    if MEMORY_DIR.exists():
        for md in sorted(MEMORY_DIR.rglob("*.md")):
            files.append(md)
    return files


def index_file(conn: sqlite3.Connection, filepath: Path, embed: bool = False) -> int:
    rel_path = str(filepath.relative_to(WORKSPACE))
    mtime = filepath.stat().st_mtime

    old_ids = conn.execute("SELECT id FROM documents WHERE path = ?", (rel_path,)).fetchall()
    if old_ids:
        ids = [r[0] for r in old_ids]
        ph = ",".join("?" * len(ids))
        conn.execute(f"DELETE FROM embeddings WHERE doc_id IN ({ph})", ids)
        conn.execute(f"DELETE FROM documents WHERE id IN ({ph})", ids)

    chunks = parse_md_chunks(filepath)
    count = 0
    for chunk in chunks:
        tokenized = tokenize(chunk["content"])
        cursor = conn.execute(
            "INSERT INTO documents (path, line_start, line_end, content, content_tokenized, type, date, mtime) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (rel_path, chunk["line_start"], chunk["line_end"],
             chunk["content"], tokenized, chunk["type"], chunk["date"], mtime)
        )
        count += 1
        if embed:
            vec = get_embedding(chunk["content"])
            if vec:
                conn.execute("INSERT INTO embeddings (doc_id, vector) VALUES (?, ?)",
                             (cursor.lastrowid, vec))

    conn.execute(
        "INSERT OR REPLACE INTO file_state (path, mtime, indexed_at) VALUES (?, ?, ?)",
        (rel_path, mtime, datetime.now().isoformat())
    )
    return count


def run_index(full: bool = False, embed: bool = False):
    """执行索引（带全局锁）"""
    with file_lock("memory_indexer"):
        _run_index_inner(full, embed)


def _run_index_inner(full: bool = False, embed: bool = False):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    conn = open_db(DB_PATH)
    init_db(conn)

    files = collect_md_files()
    total_chunks = 0
    indexed_files = 0
    skipped_files = 0

    for filepath in files:
        rel_path = str(filepath.relative_to(WORKSPACE))
        mtime = filepath.stat().st_mtime
        if not full:
            row = conn.execute("SELECT mtime FROM file_state WHERE path = ?", (rel_path,)).fetchone()
            if row and row[0] >= mtime:
                skipped_files += 1
                continue

        chunks = index_file(conn, filepath, embed)
        total_chunks += chunks
        indexed_files += 1
        print(f"  📄 {rel_path}: {chunks} 块" + (" 🧠" if embed else ""))

    conn.commit()
    total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    total_embeds = conn.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
    conn.close()

    print(f"\n{'=' * 50}")
    print(f"📊 索引完成")
    print(f"{'=' * 50}")
    print(f"  扫描文件: {len(files)}")
    print(f"  索引文件: {indexed_files}")
    print(f"  跳过文件: {skipped_files}")
    print(f"  新增块数: {total_chunks}")
    print(f"  总文档数: {total_docs}")
    print(f"  向量数量: {total_embeds}")
    print(f"  数据库: {DB_PATH}")
    print(f"{'=' * 50}")


def main():
    parser = argparse.ArgumentParser(description="记忆索引器")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--full", action="store_true", help="全量重建")
    group.add_argument("--incremental", action="store_true", help="增量更新")
    parser.add_argument("--embed", action="store_true", help="生成语义向量（需要 Ollama）")
    parser.add_argument("--memory-db", action="store_true", help="索引 memory_stream.db")
    args = parser.parse_args()

    full = args.full
    print(f"🔍 记忆索引器 ({'全量' if full else '增量'})")
    if args.embed:
        print("  + 语义向量 (Ollama)")
    print()
    run_index(full=full, embed=args.embed)



def index_memory_stream_db(embed: bool = False):
    """索引 memory_stream.db 中的记忆"""
    import numpy as np
    
    print("🔨 索引 memory_stream.db...")
    print("")
    
    memory_db_path = WORKSPACE / 'data' / 'claude-code-agent' / 'memory' / 'memory_stream.db'
    if not memory_db_path.exists():
        print(f"❌ memory_stream.db 不存在：{memory_db_path}")
        return
    
    conn = open_db(DB_PATH)
    cursor = conn.cursor()
    mem_conn = sqlite3.connect(str(memory_db_path))
    mem_conn.row_factory = sqlite3.Row
    mem_cursor = mem_conn.cursor()
    
    print("📄 加载共享记忆...")
    mem_cursor.execute("SELECT id, content, memory_type FROM memories")
    memories = mem_cursor.fetchall()
    print(f"   找到 {len(memories)} 条共享记忆")
    
    count = 0
    for mem in memories:
        content_text = mem['content'][:500]
        doc_type = mem['memory_type'] or 'memory'
        
        cursor.execute("""
            INSERT OR REPLACE INTO documents 
            (path, line_start, line_end, content, content_tokenized, type, date, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"memory_stream:memories:{mem['id']}",
            0, 0, content_text, tokenize(content_text), doc_type, None, datetime.now().timestamp()
        ))
        
        doc_id = cursor.lastrowid
        count += 1
        
        if embed:
            vec = get_embedding(content_text)
            if vec and isinstance(vec, bytes):
                vector_bytes = vec
            elif vec and isinstance(vec, list):
                vector_bytes = np.array(vec, dtype=np.float32).tobytes()
            else:
                vector_bytes = None
            
            if vector_bytes:
                cursor.execute("INSERT OR REPLACE INTO embeddings (doc_id, vector) VALUES (?, ?)",
                             (doc_id, vector_bytes))
        
        if count % 50 == 0:
            print(f"   已索引 {count}/{len(memories)}...")
    
    print(f"   ✅ 共享记忆：{count} 条")
    
    print("\n📄 加载会话记忆...")
    mem_cursor.execute("SELECT id, session_id, content, memory_type FROM session_memories")
    session_memories = mem_cursor.fetchall()
    print(f"   找到 {len(session_memories)} 条会话记忆")
    
    session_count = 0
    for mem in session_memories:
        content_text = mem['content'][:500]
        doc_type = mem['memory_type'] or 'session'
        session_id = mem['session_id'][:8]
        
        cursor.execute("""
            INSERT OR REPLACE INTO documents 
            (path, line_start, line_end, content, content_tokenized, type, date, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"memory_stream:sessions:{mem['id']}",
            0, 0, content_text, tokenize(content_text), doc_type, session_id, datetime.now().timestamp()
        ))
        
        doc_id = cursor.lastrowid
        session_count += 1
        
        if embed:
            vec = get_embedding(content_text)
            if vec and isinstance(vec, bytes):
                vector_bytes = vec
            elif vec and isinstance(vec, list):
                vector_bytes = np.array(vec, dtype=np.float32).tobytes()
            else:
                vector_bytes = None
            
            if vector_bytes:
                cursor.execute("INSERT OR REPLACE INTO embeddings (doc_id, vector) VALUES (?, ?)",
                             (doc_id, vector_bytes))
        
        if session_count % 100 == 0:
            print(f"   已索引 {session_count}/{len(session_memories)}...")
    
    print(f"   ✅ 会话记忆：{session_count} 条")
    
    conn.commit()
    conn.close()
    mem_conn.close()
    
    print("")
    print(f"✅ 完成：共索引 {count + session_count} 条记忆")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--memory-db":
        embed = "--embed" in sys.argv
        index_memory_stream_db(embed=embed)
    else:
        main()


def keyword_search(query, top_k=10):
    """关键词搜索（FTS5）"""
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 分词
    query_tokenized = tokenize(query)
    
    # FTS5 搜索
    cursor.execute("""
        SELECT d.id, d.content, d.path, d.line_start, d.type,
               bm25(documents_fts) as score
        FROM documents_fts
        JOIN documents d ON d.id = documents_fts.rowid
        WHERE documents_fts MATCH ?
        ORDER BY score
        LIMIT ?
    """, (query_tokenized, top_k))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row['id'],
            'content': row['content'][:500],
            'source': row['path'],
            'type': row['type'],
            'score': -row['score'],  # bm25 分数越低越好，取反
            'search_type': 'keyword'
        })
    
    conn.close()
    return results


def keyword_search(query, top_k=10):
    """关键词搜索（FTS5）"""
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 分词
    query_tokenized = tokenize(query)
    
    # FTS5 搜索
    try:
        cursor.execute("""
            SELECT d.id, d.content, d.path, d.line_start, d.type,
                   bm25(documents_fts) as score
            FROM documents_fts
            JOIN documents d ON d.id = documents_fts.rowid
            WHERE documents_fts MATCH ?
            ORDER BY score
            LIMIT ?
        """, (query_tokenized, top_k))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'content': row['content'][:500],
                'source': row['path'],
                'type': row['type'],
                'score': -row['score'] if row['score'] else 0,
                'search_type': 'keyword'
            })
        
        conn.close()
        return results
    except Exception as e:
        print(f"Keyword search error: {e}")
        conn.close()
        return []

