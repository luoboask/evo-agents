#!/usr/bin/env python3
"""
每日记忆压缩 - 将昨日记忆压缩并追加到 MEMORY.md

用法:
    python3 scripts/core/daily_memory_compress.py
    python3 scripts/core/daily_memory_compress.py --date 2026-04-09
"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 添加 libs 到路径
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

from path_utils import resolve_workspace

WORKSPACE = resolve_workspace()
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = MEMORY_DIR / "MEMORY.md"


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


def compress_daily(target_date: datetime = None):
    """压缩指定日期的记忆并追加到 MEMORY.md"""
    if target_date is None:
        target_date = datetime.now() - timedelta(days=1)
    
    date_str = target_date.strftime("%Y-%m-%d")
    daily_file = MEMORY_DIR / f"{date_str}.md"
    
    if not daily_file.exists():
        print(f"⏭️  {date_str}.md 不存在，跳过")
        return
    
    print(f"📅 压缩 {date_str} 的记忆...")
    
    content = daily_file.read_text(encoding="utf-8")
    extracted = extract_key_lines(content)
    
    # 如果没有关键内容，跳过
    has_content = any([extracted["events"], extracted["decisions"], extracted["learnings"]])
    
    if not has_content:
        print(f"  ⏭️  无关键内容，跳过")
        return
    
    # 生成摘要条目
    summary_entry = f"- **{date_str}**: "
    parts = []
    
    if extracted["events"]:
        parts.append(f"{len(extracted['events'])} 个事件")
    if extracted["decisions"]:
        parts.append(f"{len(extracted['decisions'])} 个决定")
    if extracted["learnings"]:
        parts.append(f"{len(extracted['learnings'])} 个学习")
    
    summary_entry += ", ".join(parts)
    
    # 追加到 MEMORY.md 的"重要事件"部分
    if MEMORY_MD.exists():
        memory_content = MEMORY_MD.read_text(encoding="utf-8")
        
        # 检查是否已存在该日期的条目
        if date_str in memory_content:
            print(f"  ⏭️  {date_str} 已存在于 MEMORY.md，跳过")
            return
        
        # 找到"## 重要事件"部分，在其后插入
        lines = memory_content.split("\n")
        insert_idx = None
        
        for i, line in enumerate(lines):
            if line.startswith("## 重要事件"):
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("## ") and j > i + 1:
                        insert_idx = j
                        break
                if insert_idx is None:
                    insert_idx = i + 2
                break
        
        if insert_idx:
            lines.insert(insert_idx, summary_entry)
            MEMORY_MD.write_text("\n".join(lines), encoding="utf-8")
            print(f"  ✅ {date_str} 摘要已追加到 MEMORY.md")
        else:
            with open(MEMORY_MD, 'a', encoding='utf-8') as f:
                f.write(f"\n{summary_entry}\n")
            print(f"  ✅ {date_str} 摘要已追加到 MEMORY.md")
    else:
        with open(MEMORY_MD, 'w', encoding='utf-8') as f:
            f.write(f"# MEMORY.md - 长期记忆\n\n## 重要事件\n{summary_entry}\n")
        print(f"  ✅ MEMORY.md 已创建，{date_str} 摘要已添加")


def main():
    parser = argparse.ArgumentParser(description="每日记忆压缩")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，默认为昨天")
    args = parser.parse_args()
    
    target = None
    if args.date:
        target = datetime.strptime(args.date, "%Y-%m-%d")
    
    compress_daily(target)


if __name__ == "__main__":
    main()
