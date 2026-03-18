#!/usr/bin/env python3
"""
Daily review - automatically run at first conversation of the day.
Reviews yesterday's memory and session history.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_yesterday_date():
    """Get yesterday's date in YYYY-MM-DD format."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_today_date():
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime('%Y-%m-%d')


def read_memory_file(date_str):
    """Read a memory file for a specific date."""
    workspace = Path("/Users/dhr/.openclaw/workspace-ai-baby")
    memory_file = workspace / "memory" / f"{date_str}.md"
    
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def create_today_memory():
    """Create memory file for today if it doesn't exist."""
    workspace = Path("/Users/dhr/.openclaw/workspace-ai-baby")
    memory_dir = workspace / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    today = get_today_date()
    today_file = memory_dir / f"{today}.md"
    
    created = False
    if not today_file.exists():
        with open(today_file, 'w', encoding='utf-8') as f:
            f.write(f"# {today} - 会话记录\n\n## 会话\n\n")
        created = True
    
    return created, today


def get_yesterday_memory_summary():
    """Get a summary of yesterday's memory file."""
    yesterday = get_yesterday_date()
    content = read_memory_file(yesterday)
    
    if not content:
        return None, yesterday
    
    # Extract key sections
    lines = content.split('\n')
    summary_lines = []
    
    for line in lines:
        line = line.strip()
        # Include headers and list items
        if line.startswith('#') or line.startswith('- ') or line.startswith('* '):
            summary_lines.append(line)
        # Include important markers
        elif '[x]' in line or '[ ]' in line:
            summary_lines.append(line)
    
    return '\n'.join(summary_lines[:50]), yesterday


def check_first_session_today():
    """Check if this is the first session today by looking at today's memory file."""
    today = get_today_date()
    workspace = Path("/Users/dhr/.openclaw/workspace-ai-baby")
    memory_file = workspace / "memory" / f"{today}.md"
    
    if not memory_file.exists():
        return True
    
    # Check if file has content beyond the header
    content = read_memory_file(today)
    if content:
        # Count non-empty lines after header
        lines = content.split('\n')
        content_lines = [l for l in lines if l.strip() and not l.startswith('#')]
        return len(content_lines) < 3  # Less than 3 content lines = first session
    
    return True


def generate_daily_review():
    """Generate the daily review report."""
    output = []
    
    output.append("=" * 60)
    output.append("📅 每日回顾 - Daily Review")
    output.append("=" * 60)
    output.append("")
    
    # Create today's file
    created, today = create_today_memory()
    
    if created:
        output.append(f"✅ 已创建今日记忆文件: memory/{today}.md")
    else:
        output.append(f"📄 今日记忆文件已存在: memory/{today}.md")
    output.append("")
    
    # Review yesterday's memory
    summary, yesterday = get_yesterday_memory_summary()
    
    if summary:
        output.append(f"📅 昨天 ({yesterday}) 的记忆摘要:")
        output.append("-" * 40)
        output.append(summary)
        output.append("-" * 40)
    else:
        output.append(f"ℹ️  昨天 ({yesterday}) 没有记忆记录")
    
    output.append("")
    output.append("=" * 60)
    output.append("💡 提示: 你可以随时让我搜索记忆，例如:")
    output.append('   - "我们昨天做了什么?"')
    output.append('   - "搜索关于 websearch 的记忆"')
    output.append('   - "我有什么待办事项?"')
    output.append("=" * 60)
    
    return '\n'.join(output)


def main():
    """Main entry point."""
    review = generate_daily_review()
    print(review)
    return review


if __name__ == '__main__':
    main()
