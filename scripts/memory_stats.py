#!/usr/bin/env python3
"""
memory_stats.py - 记忆系统统计

显示当前记忆系统的完整状态。

用法:
    python3 scripts/memory_stats.py
"""

import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"
WEEKLY_DIR = MEMORY_DIR / "weekly"
MONTHLY_DIR = MEMORY_DIR / "monthly"
ARCHIVE_DIR = MEMORY_DIR / "archive"
DB_PATH = WORKSPACE / "data" / "index" / "memory_index.db"
MEMORY_MD = WORKSPACE / "MEMORY.md"


def count_files(directory: Path, pattern: str = "*.md") -> int:
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))


def count_entries_in_file(filepath: Path) -> dict:
    """统计文件中各类型的条目数"""
    counts = {"event": 0, "decision": 0, "learning": 0, "reflection": 0, "todo": 0, "other": 0}
    if not filepath.exists():
        return counts

    current_type = "other"
    content = filepath.read_text(encoding="utf-8")
    for line in content.split("\n"):
        if "事件" in line and line.startswith("##"):
            current_type = "event"
        elif "决定" in line and line.startswith("##"):
            current_type = "decision"
        elif "学习" in line and line.startswith("##"):
            current_type = "learning"
        elif "反思" in line and line.startswith("##"):
            current_type = "reflection"
        elif "待办" in line and line.startswith("##"):
            current_type = "todo"
        elif line.startswith("## "):
            current_type = "other"
        elif line.strip().startswith("- "):
            counts[current_type] += 1

    return counts


def get_index_stats() -> dict:
    """获取索引统计"""
    stats = {
        "exists": DB_PATH.exists(),
        "size": 0,
        "total_docs": 0,
        "total_embeddings": 0,
        "files_indexed": 0,
        "last_indexed": None,
    }

    if not DB_PATH.exists():
        return stats

    stats["size"] = DB_PATH.stat().st_size

    conn = sqlite3.connect(str(DB_PATH))
    try:
        stats["total_docs"] = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        stats["total_embeddings"] = conn.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
        stats["files_indexed"] = conn.execute("SELECT COUNT(*) FROM file_state").fetchone()[0]
        row = conn.execute("SELECT MAX(indexed_at) FROM file_state").fetchone()
        if row and row[0]:
            stats["last_indexed"] = row[0]
    except Exception:
        pass
    finally:
        conn.close()

    return stats


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def main():
    print("=" * 55)
    print("📊 记忆系统统计")
    print("=" * 55)

    # MEMORY.md
    if MEMORY_MD.exists():
        size = MEMORY_MD.stat().st_size
        lines = len(MEMORY_MD.read_text(encoding="utf-8").split("\n"))
        print(f"\n📝 MEMORY.md (长期记忆)")
        print(f"   大小: {format_size(size)}")
        print(f"   行数: {lines}")
    else:
        print(f"\n📝 MEMORY.md: 不存在")

    # Daily files
    daily_files = sorted(MEMORY_DIR.glob("????-??-??.md"))
    print(f"\n📅 每日记录")
    print(f"   文件数: {len(daily_files)}")
    if daily_files:
        first = daily_files[0].stem
        last = daily_files[-1].stem
        print(f"   范围: {first} ~ {last}")

        # 统计各类型条目
        total_counts = {"event": 0, "decision": 0, "learning": 0,
                        "reflection": 0, "todo": 0, "other": 0}
        for f in daily_files:
            counts = count_entries_in_file(f)
            for k, v in counts.items():
                total_counts[k] += v

        total = sum(total_counts.values())
        print(f"   总条目: {total}")
        for type_name, count in total_counts.items():
            if count > 0:
                label = {"event": "事件", "decision": "决定", "learning": "学习",
                         "reflection": "反思", "todo": "待办", "other": "其他"}
                print(f"     {label.get(type_name, type_name)}: {count}")

    # Weekly
    weekly_count = count_files(WEEKLY_DIR)
    print(f"\n📅 周摘要: {weekly_count} 份")

    # Monthly
    monthly_count = count_files(MONTHLY_DIR)
    print(f"📅 月摘要: {monthly_count} 份")

    # Archive
    archive_count = count_files(ARCHIVE_DIR)
    print(f"📦 归档: {archive_count} 份")

    # Index
    idx = get_index_stats()
    print(f"\n🔍 搜索索引")
    if idx["exists"]:
        print(f"   状态: ✅ 已建立")
        print(f"   大小: {format_size(idx['size'])}")
        print(f"   文档块数: {idx['total_docs']}")
        print(f"   向量数: {idx['total_embeddings']}")
        print(f"   已索引文件: {idx['files_indexed']}")
        if idx["last_indexed"]:
            print(f"   最后索引: {idx['last_indexed']}")
    else:
        print(f"   状态: ❌ 未建立")
        print(f"   运行 python3 scripts/memory_indexer.py --full 来建立索引")

    print(f"\n{'=' * 55}")


if __name__ == "__main__":
    main()
