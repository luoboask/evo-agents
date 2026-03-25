#!/usr/bin/env python3
"""
session_recorder.py - 会话记录器

将对话事件写入 memory/YYYY-MM-DD.md，按类型分组。
这是 OpenClaw 侧的记忆入口。

用法:
    python3 scripts/session_recorder.py --type event --content '记忆系统改造完成'
    python3 scripts/session_recorder.py --type decision --content '采用统一记忆架构'
    python3 scripts/session_recorder.py --type learning --content '数据源必须统一'
    python3 scripts/session_recorder.py --type reflection --content '今天效率很高'
    python3 scripts/session_recorder.py --type todo --content '测试记忆压缩功能'
"""

import argparse
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"

TYPE_MAP = {
    "event":      ("📌 事件",),
    "decision":   ("🔨 决定",),
    "learning":   ("📚 学习",),
    "reflection": ("💭 反思",),
    "todo":       ("☐ 待办",),
}

VALID_TYPES = list(TYPE_MAP.keys())


def get_today_file() -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    return MEMORY_DIR / f"{today}.md"


def ensure_daily_file(filepath: Path) -> str:
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    # 从文件名提取日期，而不是用当前时间
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filepath.name)
    date_str = match.group(1) if match else datetime.now().strftime("%Y-%m-%d")
    header = f"# {date_str} - 会话记录\n\n"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(header, encoding="utf-8")
    return header


def append_to_section(content: str, section_title: str, entry: str) -> str:
    lines = content.split("\n")
    pattern = rf"^## {re.escape(section_title)}"

    # 找 section
    section_start = -1
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            section_start = i
            break

    timestamp = datetime.now().strftime("%H:%M")
    new_line = f"- [{timestamp}] {entry}"

    if section_start == -1:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(f"## {section_title}")
        lines.append("")
        lines.append(new_line)
        lines.append("")
    else:
        # 找 section 末尾
        insert_pos = len(lines)
        for i in range(section_start + 1, len(lines)):
            if lines[i].startswith("## "):
                insert_pos = i
                break
        while insert_pos > 0 and not lines[insert_pos - 1].strip():
            insert_pos -= 1
        lines.insert(insert_pos, new_line)

    return "\n".join(lines)


def record(entry_type: str, content: str, date: str = None, sync: bool = False) -> str:
    if entry_type not in VALID_TYPES:
        raise ValueError(f"无效类型: {entry_type}，可选: {VALID_TYPES}")

    filepath = MEMORY_DIR / f"{date}.md" if date else get_today_file()
    section_title = TYPE_MAP[entry_type][0]
    file_content = ensure_daily_file(filepath)

    if content in file_content:
        return f"⏭️  跳过（已存在）: {content[:50]}..."

    updated = append_to_section(file_content, section_title, content)
    filepath.write_text(updated, encoding="utf-8")

    result = f"✅ 已记录 [{entry_type}]: {content[:80]}"

    # 自动触发同步
    if sync:
        import subprocess
        # 双向同步
        bridge = WORKSPACE / "scripts" / "bridge" / "bridge_sync.py"
        if bridge.exists():
            try:
                subprocess.run(
                    ["python3", str(bridge), "--agent", "demo-agent", "--days", "1"],
                    capture_output=True, timeout=30, cwd=str(WORKSPACE)
                )
            except Exception:
                pass
        # 增量索引更新
        indexer = WORKSPACE / "scripts" / "memory_indexer.py"
        if indexer.exists():
            try:
                subprocess.run(
                    ["python3", str(indexer), "--incremental", "--embed"],
                    capture_output=True, timeout=60, cwd=str(WORKSPACE)
                )
                result += " (+ 已同步+索引)"
            except Exception:
                result += " (+ 已同步)"

    return result


def batch_record(entries: list, sync: bool = False) -> str:
    """批量记录多条记忆
    entries: [{"type": "event", "content": "..."}, ...]
    """
    results = []
    for entry in entries:
        r = record(entry["type"], entry["content"], entry.get("date"), sync=False)
        results.append(r)

    if sync:
        import subprocess
        bridge = WORKSPACE / "scripts" / "bridge" / "bridge_sync.py"
        if bridge.exists():
            try:
                subprocess.run(
                    ["python3", str(bridge), "--agent", "demo-agent", "--days", "1"],
                    capture_output=True, timeout=30, cwd=str(WORKSPACE)
                )
                results.append("🔄 已同步")
            except Exception:
                results.append("⚠️ 同步失败")

    return "\n".join(results)


def main():
    parser = argparse.ArgumentParser(description="会话记录器")
    parser.add_argument("--type", "-t", choices=VALID_TYPES,
                        help="记忆类型（单条模式）")
    parser.add_argument("--content", "-c",
                        help="记忆内容（单条模式）")
    parser.add_argument("--batch", "-b",
                        help='批量模式，JSON 格式: \'[{"type":"event","content":"xxx"},...]\'')
    parser.add_argument("--date", "-d", default=None)
    parser.add_argument("--sync", "-s", action="store_true",
                        help="记录后自动触发双向同步")
    args = parser.parse_args()

    if args.batch:
        import json
        entries = json.loads(args.batch)
        print(batch_record(entries, args.sync))
    elif args.type and args.content:
        print(record(args.type, args.content, args.date, args.sync))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
