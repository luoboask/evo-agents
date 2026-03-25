#!/usr/bin/env python3
"""
session_recorder.py - 会话记录器

将对话事件写入 memory/YYYY-MM-DD.md，按类型分组。
这是记忆系统的入口：所有记忆先落地为 markdown。

用法:
    python3 scripts/session_recorder.py --type event --content '记忆系统改造完成'
    python3 scripts/session_recorder.py --type decision --content '采用统一记忆架构'
    python3 scripts/session_recorder.py --type learning --content '数据源必须统一'
    python3 scripts/session_recorder.py --type reflection --content '今天效率很高'
    python3 scripts/session_recorder.py --type todo --content '测试记忆压缩功能'
"""

import argparse
import os
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"

# 类型映射：英文 -> 中文标题 + emoji
TYPE_MAP = {
    "event":      ("事件", "📌"),
    "decision":   ("决定", "🔨"),
    "learning":   ("学习", "📚"),
    "reflection": ("反思", "💭"),
    "todo":       ("待办", "☐"),
}

VALID_TYPES = list(TYPE_MAP.keys())


def get_today_file() -> Path:
    """获取今天的记忆文件路径"""
    today = datetime.now().strftime("%Y-%m-%d")
    return MEMORY_DIR / f"{today}.md"


def ensure_daily_file(filepath: Path) -> str:
    """确保每日文件存在，返回现有内容"""
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")

    today = datetime.now()
    header = f"# {today.strftime('%Y-%m-%d')} - 会话记录\n\n"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(header, encoding="utf-8")
    return header


def find_section(content: str, section_title: str) -> int:
    """查找 section 在内容中的结束位置（下一个 ## 之前或文件末尾）"""
    pattern = rf"^## {re.escape(section_title)}"
    lines = content.split("\n")

    section_start = -1
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            section_start = i
            break

    if section_start == -1:
        return -1  # section 不存在

    # 找下一个 ## 或文件末尾
    for i in range(section_start + 1, len(lines)):
        if lines[i].startswith("## "):
            return i  # 插入点在下一个 section 之前
    return len(lines)  # 文件末尾


def append_to_section(content: str, section_title: str, emoji: str, entry: str) -> str:
    """将条目追加到指定 section，如果 section 不存在则创建"""
    lines = content.split("\n")
    insert_pos = find_section(content, section_title)

    timestamp = datetime.now().strftime("%H:%M")
    new_line = f"- [{timestamp}] {entry}"

    if insert_pos == -1:
        # Section 不存在，在文件末尾创建
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(f"## {emoji} {section_title}")
        lines.append("")
        lines.append(new_line)
        lines.append("")
    else:
        # 在 section 末尾插入（下一个 section 之前）
        # 跳过空行
        while insert_pos > 0 and not lines[insert_pos - 1].strip():
            insert_pos -= 1
        lines.insert(insert_pos, new_line)

    return "\n".join(lines)


def record(entry_type: str, content: str, date: str = None) -> str:
    """记录一条记忆"""
    if entry_type not in VALID_TYPES:
        raise ValueError(f"无效类型: {entry_type}，可选: {VALID_TYPES}")

    if date:
        filepath = MEMORY_DIR / f"{date}.md"
    else:
        filepath = get_today_file()

    section_title, emoji = TYPE_MAP[entry_type]

    file_content = ensure_daily_file(filepath)

    # 检查是否重复（同一天同一内容）
    if content in file_content:
        return f"⏭️  跳过（已存在）: {content[:50]}..."

    updated = append_to_section(file_content, section_title, emoji, content)
    filepath.write_text(updated, encoding="utf-8")

    return f"✅ 已记录 [{entry_type}]: {content[:80]}"


def main():
    parser = argparse.ArgumentParser(description="会话记录器 - 将事件写入每日记忆文件")
    parser.add_argument("--type", "-t", required=True, choices=VALID_TYPES,
                        help="记忆类型")
    parser.add_argument("--content", "-c", required=True,
                        help="记忆内容")
    parser.add_argument("--date", "-d", default=None,
                        help="指定日期 (YYYY-MM-DD)，默认今天")
    args = parser.parse_args()

    result = record(args.type, args.content, args.date)
    print(result)


if __name__ == "__main__":
    main()
