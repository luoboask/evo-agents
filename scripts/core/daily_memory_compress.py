#!/usr/bin/env python3
"""
每日记忆压缩 - 将昨日记忆压缩并存储到共享记忆

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

from memory_hub import MemoryHub
from path_utils import resolve_workspace

WORKSPACE = resolve_workspace()
MEMORY_DIR = WORKSPACE / "memory"


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
    """压缩指定日期的记忆并存储到共享记忆"""
    if target_date is None:
        # 默认为昨天
        target_date = datetime.now() - timedelta(days=1)
    
    date_str = target_date.strftime("%Y-%m-%d")
    daily_file = MEMORY_DIR / f"{date_str}.md"
    
    if not daily_file.exists():
        print(f"⏭️  {date_str}.md 不存在，跳过")
        return
    
    print(f"📅 压缩 {date_str} 的记忆...")
    
    content = daily_file.read_text(encoding="utf-8")
    extracted = extract_key_lines(content)
    
    # 生成摘要
    summary_parts = [f"# {date_str} 记忆摘要"]
    summary_parts.append("")
    
    if extracted["events"]:
        summary_parts.append("## 📌 主要事件")
        for event in extracted["events"][:5]:  # 最多 5 条
            summary_parts.append(f"- {event}")
        summary_parts.append("")
    
    if extracted["decisions"]:
        summary_parts.append("## 🔨 重要决定")
        for decision in extracted["decisions"][:3]:
            summary_parts.append(f"- {decision}")
        summary_parts.append("")
    
    if extracted["learnings"]:
        summary_parts.append("## 📚 学习收获")
        for learning in extracted["learnings"][:3]:
            summary_parts.append(f"- {learning}")
        summary_parts.append("")
    
    summary = "\n".join(summary_parts)
    
    # 存储到共享记忆
    try:
        hub = MemoryHub(agent_name='claude-code-agent')
        memory_id = hub.add(
            content=summary,
            memory_type='observation',
            importance=7.0,
            tags=['daily-summary', 'compressed', date_str]
        )
        print(f"✅ {date_str} 摘要已存储到共享记忆 (ID: {memory_id})")
    except Exception as e:
        print(f"⚠️  存储失败：{e}")


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
