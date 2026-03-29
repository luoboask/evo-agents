#!/usr/bin/env python3
"""
Daily startup routine - check memory and review yesterday.
Run at the beginning of first session each day.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 添加 libs 到路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "libs"))
from path_utils import resolve_workspace, resolve_data_dir


def get_yesterday_date():
    """Get yesterday's date in YYYY-MM-DD format."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_today_date():
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime('%Y-%m-%d')


def read_memory_file(date_str):
    """Read a memory file for a specific date."""
    workspace = Path(__file__).parent.parent.parent
    memory_file = workspace / "memory" / f"{date_str}.md"
    
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def create_today_memory():
    """Create memory file for today if it doesn't exist."""
    workspace = Path(__file__).parent.parent.parent
    memory_dir = workspace / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    today = get_today_date()
    today_file = memory_dir / f"{today}.md"
    
    if not today_file.exists():
        with open(today_file, 'w', encoding='utf-8') as f:
            f.write(f"# {today} - 会话记录\n\n## 会话\n\n")
        return True
    return False


def get_yesterday_summary():
    """Get a summary of yesterday's activities."""
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
    
    return '\n'.join(summary_lines[:30]), yesterday  # Limit output


def main():
    print("=" * 50)
    print("📅 Daily Memory Check")
    print("=" * 50)
    print()
    
    # Create today's file
    created = create_today_memory()
    today = get_today_date()
    
    if created:
        print(f"✅ Created memory file for today: memory/{today}.md")
    else:
        print(f"📄 Today's memory file exists: memory/{today}.md")
    print()
    
    # Review yesterday
    summary, yesterday_date = get_yesterday_summary()
    
    if summary:
        print(f"📅 Yesterday ({yesterday_date}) Summary:")
        print("-" * 40)
        print(summary)
        print("-" * 40)
    else:
        print(f"ℹ️  No memory file for yesterday ({yesterday_date})")
    
    print()
    print("=" * 50)
    print("Ready for today's session!")
    print("=" * 50)


if __name__ == '__main__':
    main()
