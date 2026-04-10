#!/usr/bin/env python3
"""
每日 MEMORY.md 压缩 - 压缩 MEMORY.md 内容，保持简洁

功能:
- 读取 MEMORY.md
- 压缩"重要事件"部分（保留最近 7 天）
- 合并重复内容
- 保持文件简洁

用法:
    python3 scripts/core/daily_memory_compress.py
"""

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


def compress_memory_md():
    """压缩 MEMORY.md，保持简洁"""
    if not MEMORY_MD.exists():
        print("⏭️  MEMORY.md 不存在，跳过")
        return
    
    print("📅 压缩 MEMORY.md...")
    
    content = MEMORY_MD.read_text(encoding="utf-8")
    lines = content.split("\n")
    
    # 找到"## 重要事件"部分
    in_events_section = False
    events_start = -1
    events_end = -1
    
    for i, line in enumerate(lines):
        if line.startswith("## 重要事件"):
            in_events_section = True
            events_start = i
        elif in_events_section and line.startswith("## "):
            events_end = i
            break
    
    if events_start == -1:
        print("  ⏭️  未找到重要事件部分，跳过")
        return
    
    # 提取事件条目
    event_lines = []
    cutoff_date = datetime.now() - timedelta(days=7)  # 保留最近 7 天
    
    for i in range(events_start + 1, events_end if events_end > 0 else len(lines)):
        line = lines[i]
        # 跳过子条目（以"  - "开头的）
        if line.strip().startswith("- **"):
            # 提取日期（支持多种格式）
            match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
            if match:
                event_date = datetime.strptime(match.group(1), "%Y-%m-%d")
                if event_date >= cutoff_date:
                    event_lines.append((event_date, line))
    
    # 按日期排序（最新的在前）
    event_lines.sort(key=lambda x: x[0], reverse=True)
    
    # 生成新的事件部分
    new_events = ["## 重要事件", ""]
    
    # 添加汇总行
    if event_lines:
        total_events = sum(
            int(re.search(r'(\d+) 个事件', line[1]).group(1) or 0) 
            for line in event_lines 
            if re.search(r'(\d+) 个事件', line[1])
        )
        total_decisions = sum(
            int(re.search(r'(\d+) 个决定', line[1]).group(1) or 0) 
            for line in event_lines 
            if re.search(r'(\d+) 个决定', line[1])
        )
        total_learnings = sum(
            int(re.search(r'(\d+) 个学习', line[1]).group(1) or 0) 
            for line in event_lines 
            if re.search(r'(\d+) 个学习', line[1])
        )
        
        # 添加每日条目（最多 7 天）
        for event_date, line in event_lines[:7]:
            # 简化格式，只保留日期和摘要
            new_events.append(f"- **{event_date.strftime('%m-%d')}**: {line.split('**: ')[-1] if '**: ' in line else line[2:]}")
    
    # 替换旧的事件部分
    if events_end > 0:
        new_lines = lines[:events_start] + new_events + lines[events_end:]
    else:
        new_lines = lines[:events_start] + new_events
    
    # 写回文件
    MEMORY_MD.write_text("\n".join(new_lines), encoding="utf-8")
    
    print(f"  ✅ MEMORY.md 已压缩（保留最近 7 天，共 {len(event_lines)} 条）")


def main():
    compress_memory_md()


if __name__ == "__main__":
    main()
