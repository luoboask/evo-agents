#!/usr/bin/env python3
"""
unified_search.py - 统一搜索

同时搜索 markdown 文件和 SQLite 知识系统，合并结果。

用法:
    python3 scripts/unified_search.py '关键词'
    python3 scripts/unified_search.py '记忆系统' --limit 5
    python3 scripts/unified_search.py '改造' --source all
    python3 scripts/unified_search.py '知识' --source knowledge  # 只搜 SQLite
    python3 scripts/unified_search.py '知识' --source markdown   # 只搜文件
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import List, Dict

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"


def search_markdown(query: str, limit: int = 10) -> List[Dict]:
    """搜索 markdown 文件（grep 方式）"""
    results = []
    search_paths = []

    # MEMORY.md
    memory_md = WORKSPACE / "MEMORY.md"
    if memory_md.exists():
        search_paths.append(memory_md)

    # memory/ 下所有 md
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
                    start = max(0, i - 3)
                    end = min(len(lines), i + 2)
                    context = "\n".join(lines[start:end]).strip()
                    results.append({
                        "source": "markdown",
                        "path": rel_path,
                        "line": i,
                        "content": context[:200],
                    })
                    if len(results) >= limit:
                        return results
        except Exception:
            continue
    return results


def search_knowledge(query: str, agent_name: str = "demo-agent",
                     limit: int = 10) -> List[Dict]:
    """搜索 SQLite 知识系统"""
    db_path = WORKSPACE / "data" / agent_name / "memory" / "memory_stream.db"
    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        # 用 LIKE 做模糊搜索
        rows = conn.execute("""
            SELECT id, content, memory_type, importance, created_at
            FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        """, (f"%{query}%", limit)).fetchall()

        results = []
        for row in rows:
            results.append({
                "source": "knowledge",
                "id": row["id"],
                "content": row["content"][:200],
                "type": row["memory_type"],
                "importance": row["importance"],
                "date": str(row["created_at"])[:10],
            })
        return results
    except Exception:
        return []
    finally:
        conn.close()


def format_results(md_results: List[Dict], kb_results: List[Dict]) -> str:
    lines = []

    if md_results:
        lines.append(f"📂 Markdown 结果 ({len(md_results)} 条)")
        lines.append("-" * 40)
        for i, r in enumerate(md_results, 1):
            lines.append(f"  [{i}] {r['path']}:{r['line']}")
            content = r["content"].replace("\n", "\n      ")
            lines.append(f"      {content}")
            lines.append("")

    if kb_results:
        lines.append(f"🧠 知识系统结果 ({len(kb_results)} 条)")
        lines.append("-" * 40)
        for i, r in enumerate(kb_results, 1):
            meta = f"[{r['type']}] ★{r['importance']}"
            if r.get("date"):
                meta += f" ({r['date']})"
            lines.append(f"  [{i}] {meta}")
            lines.append(f"      {r['content']}")
            lines.append("")

    if not md_results and not kb_results:
        lines.append("没有找到匹配结果。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="统一记忆搜索")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--limit", "-n", type=int, default=10)
    parser.add_argument("--source", choices=["all", "markdown", "knowledge"],
                        default="all", help="搜索范围")
    parser.add_argument("--agent", default="demo-agent")
    args = parser.parse_args()

    print(f"🔍 搜索: \"{args.query}\" (范围: {args.source})\n")

    md_results = []
    kb_results = []

    if args.source in ("all", "markdown"):
        md_results = search_markdown(args.query, args.limit)

    if args.source in ("all", "knowledge"):
        kb_results = search_knowledge(args.query, args.agent, args.limit)

    total = len(md_results) + len(kb_results)
    print(f"找到 {total} 条结果:\n")
    print(format_results(md_results, kb_results))


if __name__ == "__main__":
    main()
