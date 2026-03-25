#!/usr/bin/env python3
"""
memory_compressor.py - 记忆压缩器

日记忆 → 周摘要 → 月摘要，并归档旧文件。
不依赖 LLM，纯规则提取关键内容。

用法:
    python3 scripts/memory_compressor.py --weekly      # 生成上周摘要
    python3 scripts/memory_compressor.py --monthly     # 生成上月摘要
    python3 scripts/memory_compressor.py --archive     # 归档已压缩的 daily
    python3 scripts/memory_compressor.py --all         # 全部执行
    python3 scripts/memory_compressor.py --weekly --target-date 2026-03-17  # 指定日期所在周
"""

import argparse
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"
WEEKLY_DIR = MEMORY_DIR / "weekly"
MONTHLY_DIR = MEMORY_DIR / "monthly"
ARCHIVE_DIR = MEMORY_DIR / "archive"


def get_daily_files(start_date: datetime, end_date: datetime) -> List[Tuple[str, Path]]:
    files = []
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        filepath = MEMORY_DIR / f"{date_str}.md"
        if filepath.exists():
            files.append((date_str, filepath))
        current += timedelta(days=1)
    return files


def extract_key_lines(content: str) -> dict:
    """从 markdown 中提取关键行，按类型分组"""
    result = {
        "events": [], "decisions": [], "learnings": [],
        "reflections": [], "todos_done": [], "todos_open": [],
    }
    current_section = "events"

    for line in content.split("\n"):
        s = line.strip()
        if s.startswith("## "):
            heading = s[3:]
            if any(k in heading for k in ["事件", "观察"]):
                current_section = "events"
            elif "决定" in heading:
                current_section = "decisions"
            elif any(k in heading for k in ["学习", "知识"]):
                current_section = "learnings"
            elif "反思" in heading:
                current_section = "reflections"
            elif "待办" in heading:
                current_section = "todos_open"
            continue

        if s.startswith("- "):
            item = s[2:].strip()
            # 去掉时间前缀 [HH:MM]
            item = re.sub(r'^\[\d{2}:\d{2}\]\s*', '', item)
            if not item or len(item) < 3:
                continue

            if s.startswith("- [x]") or "✅" in s:
                result["todos_done"].append(item)
            elif s.startswith("- [ ]"):
                result["todos_open"].append(item)
            elif current_section in result:
                result[current_section].append(item)

    return result


def generate_weekly(target_date: datetime = None) -> str:
    if target_date is None:
        today = datetime.now()
        last_monday = today - timedelta(days=today.weekday() + 7)
    else:
        last_monday = target_date - timedelta(days=target_date.weekday())

    last_sunday = last_monday + timedelta(days=6)
    week_num = last_monday.isocalendar()[1]
    year = last_monday.year

    files = get_daily_files(last_monday, last_sunday)
    if not files:
        print(f"  ⏭️  W{week_num:02d} 没有 daily 文件")
        return ""

    filename = f"{year}-W{week_num:02d}.md"
    output_path = WEEKLY_DIR / filename

    if output_path.exists():
        print(f"  ⏭️  {filename} 已存在")
        return str(output_path)

    # 收集
    all_items = {
        "events": [], "decisions": [], "learnings": [],
        "reflections": [], "todos_done": [], "todos_open": [],
    }
    dates = []
    for date_str, filepath in files:
        dates.append(date_str)
        content = filepath.read_text(encoding="utf-8")
        extracted = extract_key_lines(content)
        for key in all_items:
            all_items[key].extend(extracted[key])

    # 去重
    for key in all_items:
        all_items[key] = list(dict.fromkeys(all_items[key]))

    # 生成
    lines = [
        f"# 周摘要 {year}-W{week_num:02d}",
        f"",
        f"**日期**: {last_monday.strftime('%Y-%m-%d')} ~ {last_sunday.strftime('%Y-%m-%d')}",
        f"**记录天数**: {len(dates)}",
        f"",
    ]

    sections = [
        ("decisions", "🔨 关键决定"),
        ("events", "📌 事件"),
        ("learnings", "📚 学习"),
        ("reflections", "💭 反思"),
        ("todos_done", "✅ 完成"),
        ("todos_open", "☐ 未完成"),
    ]
    for key, title in sections:
        items = all_items[key]
        if items:
            lines.append(f"## {title}")
            lines.append("")
            for item in items[:20]:
                lines.append(f"- {item}")
            lines.append("")

    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    total = sum(len(v) for v in all_items.values())
    print(f"  ✅ {filename} ({len(dates)} 天, {total} 条)")
    return str(output_path)


def generate_monthly(target_date: datetime = None) -> str:
    if target_date is None:
        today = datetime.now()
        first = today.replace(day=1)
        last_month_end = first - timedelta(days=1)
        year, month = last_month_end.year, last_month_end.month
    else:
        year, month = target_date.year, target_date.month

    filename = f"{year}-{month:02d}.md"
    output_path = MONTHLY_DIR / filename
    if output_path.exists():
        print(f"  ⏭️  {filename} 已存在")
        return str(output_path)

    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(days=1)

    daily_files = get_daily_files(start, end)
    if not daily_files:
        print(f"  ⏭️  {year}-{month:02d} 没有数据")
        return ""

    all_items = {
        "events": [], "decisions": [], "learnings": [],
        "reflections": [], "todos_done": [], "todos_open": [],
    }
    for _, filepath in daily_files:
        content = filepath.read_text(encoding="utf-8")
        extracted = extract_key_lines(content)
        for key in all_items:
            all_items[key].extend(extracted[key])

    for key in all_items:
        all_items[key] = list(dict.fromkeys(all_items[key]))

    lines = [
        f"# 月度摘要 {year}-{month:02d}",
        f"",
        f"**记录天数**: {len(daily_files)}",
        f"",
    ]
    sections = [
        ("decisions", "🔨 关键决定"),
        ("events", "📌 重要事件"),
        ("learnings", "📚 学习总结"),
        ("reflections", "💭 反思"),
    ]
    for key, title in sections:
        items = all_items[key]
        if items:
            lines.append(f"## {title}")
            lines.append("")
            for item in items[:30]:
                lines.append(f"- {item}")
            lines.append("")

    MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ {filename} ({len(daily_files)} 天)")
    return str(output_path)


def archive_old_dailies(keep_days: int = 14):
    cutoff = datetime.now() - timedelta(days=keep_days)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archived = 0
    for md_file in sorted(MEMORY_DIR.glob("????-??-??.md")):
        match = re.match(r"(\d{4}-\d{2}-\d{2})", md_file.name)
        if not match:
            continue
        file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
        if file_date < cutoff:
            shutil.move(str(md_file), str(ARCHIVE_DIR / md_file.name))
            archived += 1
            print(f"  📦 {md_file.name}")
    print(f"  共归档 {archived} 个" if archived else f"  无需归档（保留最近 {keep_days} 天）")


def main():
    parser = argparse.ArgumentParser(description="记忆压缩器")
    parser.add_argument("--weekly", action="store_true")
    parser.add_argument("--monthly", action="store_true")
    parser.add_argument("--archive", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--keep-days", type=int, default=14)
    parser.add_argument("--target-date", help="指定日期 (YYYY-MM-DD)")
    args = parser.parse_args()

    if not any([args.weekly, args.monthly, args.archive, args.all]):
        parser.print_help()
        return

    target = datetime.strptime(args.target_date, "%Y-%m-%d") if args.target_date else None

    print("🗜️  记忆压缩器\n")
    if args.weekly or args.all:
        print("📅 周摘要...")
        generate_weekly(target)
        print()
    if args.monthly or args.all:
        print("📅 月摘要...")
        generate_monthly(target)
        print()
    if args.archive or args.all:
        print("📦 归档...")
        archive_old_dailies(args.keep_days)
        print()
    print("✅ 完成")


if __name__ == "__main__":
    main()
