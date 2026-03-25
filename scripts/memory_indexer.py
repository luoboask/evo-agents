#!/usr/bin/env python3
"""
memory_indexer.py - 记忆索引器

扫描 markdown 文件，构建 SQLite FTS5 全文搜索索引。
可选：使用 Ollama 生成语义向量。

用法:
    python3 scripts/memory_indexer.py --full          # 全量重建索引
    python3 scripts/memory_indexer.py --incremental   # 只索引变更文件
    python3 scripts/memory_indexer.py --full --embed   # 全量 + 语义向量
"""

import argparse
import json
import os
import re
import sqlite3
import struct
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"
INDEX_DIR = WORKSPACE / "data" / "index"
DB_PATH = INDEX_DIR / "memory_index.db"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


def init_db(conn: sqlite3.Connection):
    """初始化数据库表"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            line_start INTEGER NOT NULL,
            line_end INTEGER NOT NULL,
            content TEXT NOT NULL,
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

        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
            content,
            type,
            date,
            content='documents',
            content_rowid='id'
        );

        -- FTS 同步触发器
        CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
            INSERT INTO documents_fts(rowid, content, type, date)
            VALUES (new.id, new.content, new.type, new.date);
        END;

        CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, content, type, date)
            VALUES ('delete', old.id, old.content, old.type, old.date);
        END;

        CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, content, type, date)
            VALUES ('delete', old.id, old.content, old.type, old.date);
            INSERT INTO documents_fts(rowid, content, type, date)
            VALUES (new.id, new.content, new.type, new.date);
        END;
    """)


def detect_type(line: str) -> str:
    """从行内容检测记忆类型"""
    lower = line.lower()
    if any(k in line for k in ["## 📌 事件", "## 事件"]):
        return "event"
    if any(k in line for k in ["## 🔨 决定", "## 决定"]):
        return "decision"
    if any(k in line for k in ["## 📚 学习", "## 学习"]):
        return "learning"
    if any(k in line for k in ["## 💭 反思", "## 反思"]):
        return "reflection"
    if any(k in line for k in ["## ☐ 待办", "## 待办", "- [ ]", "- [x]"]):
        return "todo"
    if "✅" in line or "❌" in line:
        return "event"
    return "unknown"


def extract_date_from_path(filepath: Path) -> Optional[str]:
    """从文件名提取日期"""
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    if match:
        return match.group(1)
    match = re.search(r"(\d{4}-W\d{2})", filepath.name)
    if match:
        return match.group(1)
    match = re.search(r"(\d{4}-\d{2})", filepath.name)
    if match:
        return match.group(1)
    return None


def parse_md_chunks(filepath: Path) -> List[dict]:
    """将 markdown 文件拆分为段落块"""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    chunks = []
    current_chunk = []
    current_start = 1
    current_type = "unknown"
    file_date = extract_date_from_path(filepath)

    for i, line in enumerate(lines, 1):
        # 遇到新的 section 标题
        if line.startswith("## "):
            # 保存上一个 chunk
            if current_chunk:
                text = "\n".join(current_chunk).strip()
                if text and len(text) > 5:
                    chunks.append({
                        "content": text,
                        "line_start": current_start,
                        "line_end": i - 1,
                        "type": current_type,
                        "date": file_date,
                    })
            current_chunk = [line]
            current_start = i
            current_type = detect_type(line)
        elif line.startswith("# ") and not current_chunk:
            # 文件标题，跳过
            current_start = i + 1
        else:
            current_chunk.append(line)
            # 如果行本身有类型标记，更新
            line_type = detect_type(line)
            if line_type != "unknown":
                current_type = line_type

    # 最后一个 chunk
    if current_chunk:
        text = "\n".join(current_chunk).strip()
        if text and len(text) > 5:
            chunks.append({
                "content": text,
                "line_start": current_start,
                "line_end": len(lines),
                "type": current_type,
                "date": file_date,
            })

    return chunks


def get_embedding(text: str) -> Optional[bytes]:
    """使用 Ollama 生成嵌入向量，返回二进制格式"""
    try:
        result = subprocess.run(
            ["curl", "-s", OLLAMA_URL,
             "-H", "Content-Type: application/json",
             "-d", json.dumps({"model": EMBED_MODEL, "prompt": text[:500]})],
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
    """收集所有需要索引的 markdown 文件"""
    files = []

    # MEMORY.md
    memory_md = WORKSPACE / "MEMORY.md"
    if memory_md.exists():
        files.append(memory_md)

    # memory/ 下所有 .md（包括子目录）
    if MEMORY_DIR.exists():
        for md in sorted(MEMORY_DIR.rglob("*.md")):
            files.append(md)

    return files


def index_file(conn: sqlite3.Connection, filepath: Path, embed: bool = False) -> int:
    """索引单个文件，返回索引的块数"""
    rel_path = str(filepath.relative_to(WORKSPACE))
    mtime = filepath.stat().st_mtime

    # 删除旧索引
    old_ids = conn.execute(
        "SELECT id FROM documents WHERE path = ?", (rel_path,)
    ).fetchall()
    if old_ids:
        ids = [r[0] for r in old_ids]
        placeholders = ",".join("?" * len(ids))
        conn.execute(f"DELETE FROM embeddings WHERE doc_id IN ({placeholders})", ids)
        conn.execute(f"DELETE FROM documents WHERE id IN ({placeholders})", ids)

    # 解析并索引
    chunks = parse_md_chunks(filepath)
    count = 0
    for chunk in chunks:
        cursor = conn.execute(
            "INSERT INTO documents (path, line_start, line_end, content, type, date, mtime) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rel_path, chunk["line_start"], chunk["line_end"],
             chunk["content"], chunk["type"], chunk["date"], mtime)
        )
        count += 1

        if embed:
            vec = get_embedding(chunk["content"])
            if vec:
                conn.execute(
                    "INSERT INTO embeddings (doc_id, vector) VALUES (?, ?)",
                    (cursor.lastrowid, vec)
                )

    # 更新文件状态
    conn.execute(
        "INSERT OR REPLACE INTO file_state (path, mtime, indexed_at) VALUES (?, ?, ?)",
        (rel_path, mtime, datetime.now().isoformat())
    )

    return count


def run_index(full: bool = False, embed: bool = False):
    """执行索引"""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    init_db(conn)

    files = collect_md_files()
    total_chunks = 0
    indexed_files = 0
    skipped_files = 0

    for filepath in files:
        rel_path = str(filepath.relative_to(WORKSPACE))
        mtime = filepath.stat().st_mtime

        if not full:
            # 增量：检查 mtime
            row = conn.execute(
                "SELECT mtime FROM file_state WHERE path = ?", (rel_path,)
            ).fetchone()
            if row and row[0] >= mtime:
                skipped_files += 1
                continue

        chunks = index_file(conn, filepath, embed)
        total_chunks += chunks
        indexed_files += 1
        print(f"  📄 {rel_path}: {chunks} 块")

    conn.commit()

    # 统计
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
    parser = argparse.ArgumentParser(description="记忆索引器 - 构建 FTS5 搜索索引")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--full", action="store_true", help="全量重建索引")
    group.add_argument("--incremental", action="store_true", help="增量更新索引")
    parser.add_argument("--embed", action="store_true", help="生成语义向量（需要 Ollama）")
    args = parser.parse_args()

    # 默认增量
    full = args.full

    print(f"🔍 记忆索引器 ({'全量' if full else '增量'}模式)")
    print(f"{'  + 语义向量' if args.embed else ''}\n")
    run_index(full=full, embed=args.embed)


if __name__ == "__main__":
    main()
