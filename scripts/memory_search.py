#!/usr/bin/env python3
"""
memory_search.py - 统一记忆搜索

整合 FTS5 全文搜索 + Ollama 语义搜索 + grep 文件搜索。

用法:
    python3 scripts/memory_search.py '记忆系统'
    python3 scripts/memory_search.py '改造' --limit 5
    python3 scripts/memory_search.py 'unified memory' --semantic
    python3 scripts/memory_search.py '决定' --type decision
"""

import argparse
import json
import math
import os
import re
import sqlite3
import struct
import subprocess
from pathlib import Path
from typing import List, Optional

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"
DB_PATH = WORKSPACE / "data" / "index" / "memory_index.db"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


def search_fts(query: str, limit: int = 10, type_filter: str = None) -> List[dict]:
    """FTS5 全文搜索"""
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    try:
        # FTS5 查询
        sql = """
            SELECT d.path, d.line_start, d.line_end, d.content, d.type, d.date,
                   rank
            FROM documents_fts
            JOIN documents d ON d.id = documents_fts.rowid
            WHERE documents_fts MATCH ?
        """
        params = [query]

        if type_filter:
            sql += " AND d.type = ?"
            params.append(type_filter)

        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        results = []
        for row in rows:
            results.append({
                "source": "fts5",
                "path": row["path"],
                "line_start": row["line_start"],
                "line_end": row["line_end"],
                "content": row["content"][:200],
                "type": row["type"],
                "date": row["date"],
                "score": abs(row["rank"]),
            })
        return results
    except Exception as e:
        # FTS 查询失败时返回空（可能是查询语法问题）
        return []
    finally:
        conn.close()


def get_embedding(text: str) -> Optional[List[float]]:
    """使用 Ollama 生成嵌入向量"""
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
                return data["embedding"]
    except Exception:
        pass
    return None


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search_semantic(query: str, limit: int = 10, type_filter: str = None) -> List[dict]:
    """语义搜索（需要 Ollama + 已建索引的向量）"""
    if not DB_PATH.exists():
        return []

    query_vec = get_embedding(query)
    if not query_vec:
        print("  ⚠️  无法生成查询向量（Ollama 不可用），退回 FTS 搜索")
        return search_fts(query, limit, type_filter)

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    try:
        sql = """
            SELECT d.id, d.path, d.line_start, d.line_end, d.content, d.type, d.date,
                   e.vector
            FROM embeddings e
            JOIN documents d ON d.id = e.doc_id
        """
        if type_filter:
            sql += f" WHERE d.type = '{type_filter}'"

        rows = conn.execute(sql).fetchall()

        scored = []
        for row in rows:
            vec_bytes = row["vector"]
            dim = len(vec_bytes) // 4
            doc_vec = list(struct.unpack(f"{dim}f", vec_bytes))
            sim = cosine_similarity(query_vec, doc_vec)
            scored.append((sim, row))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        for sim, row in scored[:limit]:
            results.append({
                "source": "semantic",
                "path": row["path"],
                "line_start": row["line_start"],
                "line_end": row["line_end"],
                "content": row["content"][:200],
                "type": row["type"],
                "date": row["date"],
                "score": round(sim, 4),
            })
        return results
    finally:
        conn.close()


def search_grep(query: str, limit: int = 10) -> List[dict]:
    """Grep 文件搜索（fallback，无需索引）"""
    results = []

    # 搜索所有 md 文件
    search_paths = [WORKSPACE / "MEMORY.md"]
    if MEMORY_DIR.exists():
        search_paths.extend(sorted(MEMORY_DIR.rglob("*.md")))

    for filepath in search_paths:
        if not filepath.exists():
            continue
        try:
            lines = filepath.read_text(encoding="utf-8").split("\n")
            rel_path = str(filepath.relative_to(WORKSPACE))

            for i, line in enumerate(lines, 1):
                if query.lower() in line.lower():
                    # 提取上下文（前后各 2 行）
                    start = max(0, i - 3)
                    end = min(len(lines), i + 2)
                    context = "\n".join(lines[start:end]).strip()

                    results.append({
                        "source": "grep",
                        "path": rel_path,
                        "line_start": i,
                        "line_end": i,
                        "content": context[:200],
                        "type": "unknown",
                        "date": None,
                        "score": 1.0,
                    })

                    if len(results) >= limit:
                        return results
        except Exception:
            continue

    return results


def format_results(results: List[dict]) -> str:
    """格式化搜索结果"""
    if not results:
        return "没有找到匹配结果。"

    lines = []
    for i, r in enumerate(results, 1):
        header = f"[{i}] {r['path']}:{r['line_start']}"
        if r["date"]:
            header += f" ({r['date']})"
        if r["type"] != "unknown":
            header += f" [{r['type']}]"
        header += f" (score: {r['score']:.2f})"

        content = r["content"].replace("\n", "\n    ")
        lines.append(f"{header}")
        lines.append(f"    {content}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="统一记忆搜索")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--semantic", action="store_true",
                        help="使用语义搜索（需要 Ollama）")
    parser.add_argument("--limit", "-n", type=int, default=10,
                        help="最大结果数（默认 10）")
    parser.add_argument("--type", "-t", choices=[
        "event", "decision", "learning", "reflection", "todo", "unknown"
    ], help="按类型过滤")
    parser.add_argument("--grep", action="store_true",
                        help="使用 grep 搜索（无需索引）")
    args = parser.parse_args()

    print(f"🔍 搜索: \"{args.query}\"\n")

    results = []

    if args.grep:
        print("📂 文件搜索 (grep)...")
        results = search_grep(args.query, args.limit)
    elif args.semantic:
        print("🧠 语义搜索...")
        results = search_semantic(args.query, args.limit, args.type)
    else:
        # 默认：先 FTS，不够则 grep 补充
        print("📖 全文搜索 (FTS5)...")
        results = search_fts(args.query, args.limit, args.type)
        if not results:
            print("  FTS 无结果，退回 grep...")
            results = search_grep(args.query, args.limit)

    print(f"\n找到 {len(results)} 条结果:\n")
    print(format_results(results))


if __name__ == "__main__":
    main()
