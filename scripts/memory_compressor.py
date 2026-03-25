#!/usr/bin/env python3
"""
memory_compressor.py - 记忆压缩器

将日记忆压缩为周摘要、月摘要，并沉淀到 MEMORY.md。
不依赖 LLM，纯规则提取。

用法:
    python3 scripts/memory_compressor.py --weekly     # 生成上周摘要
    python3 scripts/memory_compressor.py --monthly    # 生成上月摘要
    python3 scripts/memory_compressor.py --archive    # 归档已压缩的 daily 文件
    python3 scripts/memory_compressor.py --all        # 全部执行
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
MEMORY_MD = WORKSPACE / "MEMORY.md"


def get_daily_files(start_date: datetime, end_date: datetime) -> List[Tuple[str, Path]]:
    """获取日期范围内的 daily 文件"""
    files = []
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        filepath = MEMORY_DIR / f"{date_str}.md"
        if filepath.exists():
            files.append((date_str, filepath))
        current += timedelta(days=1)
    return files


def extract_key_content(content: str) -> dict:
    """从 markdown 内容中提取关键信息"""
    result = {
        "headings": [],
        "decisions": [],
        "events": [],
        "learnings": [],
        "todos_done": [],
        "todos_open": [],
        "reflections": [],
        "highlights": [],
    }

    current_section = None
    for line in content.split("\n"):
        stripped = line.strip()

        # Section 标题
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            result["headings"].append(heading)
            if "决定" in heading:
                current_section = "decisions"
            elif "事件" in heading:
                current_section = "events"
            elif "学习" in heading:
                current_section = "learnings"
            elif "反思" in heading:
                current_section = "reflections"
            elif "待办" in heading:
                current_section = "todos"
            else:
                current_section = "events"  # 默认归到事件
            continue

        # 列表项
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            # 完成的 todo
            if stripped.startswith("- [x]") or "✅" in stripped:
                result["todos_done"].append(item)
                if current_section and current_section in result:
                    result[current_section].append(item)
            # 未完成的 todo
            elif stripped.startswith("- [ ]"):
                result["todos_open"].append(item)
            # 失败/重要标记
            elif "❌" in stripped:
                result["highlights"].append(item)
                if current_section and current_section in result:
                    result[current_section].append(item)
            # 普通列表项
            elif current_section and current_section in result:
                result[current_section].append(item)

    return result


def generate_weekly(target_date: datetime = None) -> str:
    """生成周摘要"""
    if target_date is None:
        # 默认是上周
        today = datetime.now()
        # 上周一
        last_monday = today - timedelta(days=today.weekday() + 7)
    else:
        last_monday = target_date - timedelta(days=target_date.weekday())

    last_sunday = last_monday + timedelta(days=6)
    week_num = last_monday.isocalendar()[1]
    year = last_monday.year

    files = get_daily_files(last_monday, last_sunday)
    if not files:
        print(f"  ⏭️  没有找到 W{week_num:02d} 的 daily 文件")
        return ""

    filename = f"{year}-W{week_num:02d}.md"
    output_path = WEEKLY_DIR / filename

    if output_path.exists():
        print(f"  ⏭️  {filename} 已存在")
        return str(output_path)

    # 收集关键内容
    all_content = {
        "events": [],
        "decisions": [],
        "learnings": [],
        "todos_done": [],
        "todos_open": [],
        "reflections": [],
        "highlights": [],
    }

    dates_covered = []
    for date_str, filepath in files:
        dates_covered.append(date_str)
        content = filepath.read_text(encoding="utf-8")
        extracted = extract_key_content(content)

        for key in all_content:
            if key in extracted:
                all_content[key].extend(extracted[key])

    # 生成摘要
    lines = [
        f"# 周摘要 {year}-W{week_num:02d}",
        f"",
        f"**日期范围**: {last_monday.strftime('%Y-%m-%d')} ~ {last_sunday.strftime('%Y-%m-%d')}",
        f"**记录天数**: {len(dates_covered)}",
        f"",
    ]

    if all_content["events"]:
        lines.append("## 📌 关键事件")
        lines.append("")
        for item in all_content["events"][:20]:  # 限制数量
            lines.append(f"- {item}")
        lines.append("")

    if all_content["decisions"]:
        lines.append("## 🔨 决定")
        lines.append("")
        for item in all_content["decisions"]:
            lines.append(f"- {item}")
        lines.append("")

    if all_content["learnings"]:
        lines.append("## 📚 学习")
        lines.append("")
        for item in all_content["learnings"]:
            lines.append(f"- {item}")
        lines.append("")

    if all_content["todos_done"]:
        lines.append("## ✅ 完成")
        lines.append("")
        for item in all_content["todos_done"][:15]:
            lines.append(f"- {item}")
        lines.append("")

    if all_content["todos_open"]:
        lines.append("## ☐ 待办（未完成）")
        lines.append("")
        for item in all_content["todos_open"]:
            lines.append(f"- {item}")
        lines.append("")

    if all_content["reflections"]:
        lines.append("## 💭 反思")
        lines.append("")
        for item in all_content["reflections"]:
            lines.append(f"- {item}")
        lines.append("")

    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ 生成: {filename} ({len(dates_covered)} 天, {sum(len(v) for v in all_content.values())} 条)")
    return str(output_path)


def generate_monthly(target_date: datetime = None) -> str:
    """生成月摘要"""
    if target_date is None:
        # 默认上月
        today = datetime.now()
        first_of_month = today.replace(day=1)
        last_month_end = first_of_month - timedelta(days=1)
        year = last_month_end.year
        month = last_month_end.month
    else:
        year = target_date.year
        month = target_date.month

    filename = f"{year}-{month:02d}.md"
    output_path = MONTHLY_DIR / filename

    if output_path.exists():
        print(f"  ⏭️  {filename} 已存在")
        return str(output_path)

    # 收集该月的 weekly 文件
    weekly_files = sorted(WEEKLY_DIR.glob(f"{year}-W*.md"))
    relevant_weeklies = []
    for wf in weekly_files:
        content = wf.read_text(encoding="utf-8")
        # 检查日期范围是否在目标月份
        match = re.search(r"\*\*日期范围\*\*:\s*(\d{4}-\d{2})-\d{2}", content)
        if match and match.group(1) == f"{year}-{month:02d}":
            relevant_weeklies.append(wf)

    # 也直接扫描该月的 daily 文件
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(days=1)

    daily_files = get_daily_files(start, end)

    if not daily_files and not relevant_weeklies:
        print(f"  ⏭️  {year}-{month:02d} 没有数据")
        return ""

    # 从 daily 文件提取
    all_content = {
        "events": [], "decisions": [], "learnings": [],
        "todos_done": [], "todos_open": [], "reflections": [],
    }

    for date_str, filepath in daily_files:
        content = filepath.read_text(encoding="utf-8")
        extracted = extract_key_content(content)
        for key in all_content:
            if key in extracted:
                all_content[key].extend(extracted[key])

    lines = [
        f"# 月度摘要 {year}-{month:02d}",
        f"",
        f"**记录天数**: {len(daily_files)}",
        f"**周报数量**: {len(relevant_weeklies)}",
        f"",
    ]

    if all_content["decisions"]:
        lines.append("## 🔨 关键决定")
        lines.append("")
        for item in all_content["decisions"]:
            lines.append(f"- {item}")
        lines.append("")

    if all_content["events"]:
        lines.append("## 📌 重要事件")
        lines.append("")
        # 月度去重，只保留最重要的
        seen = set()
        for item in all_content["events"]:
            short = item[:50]
            if short not in seen:
                seen.add(short)
                lines.append(f"- {item}")
        lines.append("")

    if all_content["learnings"]:
        lines.append("## 📚 学习总结")
        lines.append("")
        for item in all_content["learnings"]:
            lines.append(f"- {item}")
        lines.append("")

    if all_content["reflections"]:
        lines.append("## 💭 反思")
        lines.append("")
        for item in all_content["reflections"]:
            lines.append(f"- {item}")
        lines.append("")

    MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ 生成: {filename} ({len(daily_files)} 天)")
    return str(output_path)


def archive_old_dailies(keep_days: int = 14):
    """将超过 keep_days 天的 daily 文件移到 archive/"""
    cutoff = datetime.now() - timedelta(days=keep_days)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    archived = 0
    for md_file in sorted(MEMORY_DIR.glob("????-??-??.md")):
        match = re.match(r"(\d{4}-\d{2}-\d{2})", md_file.name)
        if not match:
            continue
        file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
        if file_date < cutoff:
            dest = ARCHIVE_DIR / md_file.name
            shutil.move(str(md_file), str(dest))
            archived += 1
            print(f"  📦 归档: {md_file.name}")

    if archived:
        print(f"  共归档 {archived} 个文件")
    else:
        print(f"  没有需要归档的文件（保留最近 {keep_days} 天）")


def main():
    parser = argparse.ArgumentParser(description="记忆压缩器 - 日→周→月→长期")
    parser.add_argument("--weekly", action="store_true", help="生成周摘要")
    parser.add_argument("--monthly", action="store_true", help="生成月摘要")
    parser.add_argument("--archive", action="store_true", help="归档旧的 daily 文件")
    parser.add_argument("--all", action="store_true", help="执行全部操作")
    parser.add_argument("--keep-days", type=int, default=14,
                        help="归档时保留最近多少天（默认 14）")
    args = parser.parse_args()

    if not any([args.weekly, args.monthly, args.archive, args.all]):
        parser.print_help()
        return

    print("🗜️  记忆压缩器\n")

    if args.weekly or args.all:
        print("📅 生成周摘要...")
        generate_weekly()
        print()

    if args.monthly or args.all:
        print("📅 生成月摘要...")
        generate_monthly()
        print()

    if args.archive or args.all:
        print("📦 归档旧文件...")
        archive_old_dailies(args.keep_days)
        print()

    print("✅ 完成")


if __name__ == "__main__":
    main()
