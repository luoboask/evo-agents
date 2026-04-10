#!/usr/bin/env python3
"""
每日 MEMORY.md 压缩 - 将 MEMORY.md 内容压缩并存储到共享记忆

功能:
- 读取 MEMORY.md
- 提取关键内容（用户信息、重要事件、技能、决定等）
- 压缩为结构化摘要
- 存储到共享记忆（memories 表）

用法:
    python3 scripts/core/daily_memory_compress.py
"""

import re
from datetime import datetime
from pathlib import Path
import sys

# 添加 libs 到路径
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

from memory_hub import MemoryHub
from path_utils import resolve_workspace

WORKSPACE = resolve_workspace()
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = MEMORY_DIR / "MEMORY.md"


def extract_sections(content: str) -> dict:
    """从 MEMORY.md 中提取各个部分"""
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            # 保存上一个 section
            if current_section:
                sections[current_section] = "\n".join(current_content)
            
            # 开始新 section
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # 保存最后一个 section
    if current_section:
        sections[current_section] = "\n".join(current_content)
    
    return sections


def compress_memory_md():
    """压缩 MEMORY.md 并存储到共享记忆"""
    if not MEMORY_MD.exists():
        print("⏭️  MEMORY.md 不存在，跳过")
        return
    
    print("📅 压缩 MEMORY.md 到共享记忆...")
    
    # 读取 MEMORY.md
    content = MEMORY_MD.read_text(encoding="utf-8")
    sections = extract_sections(content)
    
    # 生成压缩摘要
    summary_parts = ["# MEMORY.md 压缩摘要"]
    summary_parts.append(f"_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_" )
    summary_parts.append("")
    
    # 用户信息
    if "用户" in sections:
        summary_parts.append("## 👤 用户信息")
        summary_parts.append(sections["用户"].strip())
        summary_parts.append("")
    
    # 重要事件（最近 7 天）
    if "重要事件" in sections:
        events = sections["重要事件"].strip()
        event_lines = [line for line in events.split("\n") if line.strip().startswith("- **")]
        
        # 只保留最近 7 天的事件
        cutoff_date = datetime.now() - timedelta(days=7)
        recent_events = []
        
        for line in event_lines:
            match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
            if match:
                event_date = datetime.strptime(match.group(1), "%Y-%m-%d")
                if event_date >= cutoff_date:
                    recent_events.append(line)
        
        if recent_events:
            summary_parts.append("## 📅 最近事件（7 天内）")
            for event in recent_events[:10]:  # 最多 10 条
                summary_parts.append(event)
            summary_parts.append("")
    
    # 技能
    if "技能" in sections:
        summary_parts.append("## 🛠️ 技能")
        summary_parts.append(sections["技能"].strip())
        summary_parts.append("")
    
    # 决定
    if "决定" in sections:
        summary_parts.append("## 🔨 重要决定")
        summary_parts.append(sections["决定"].strip())
        summary_parts.append("")
    
    # 项目
    if "项目" in sections:
        summary_parts.append("## 📦 项目")
        # 只保留项目名称和关键信息
        projects = sections["项目"].strip()
        for line in projects.split("\n")[:20]:  # 最多 20 行
            summary_parts.append(line)
        summary_parts.append("")
    
    summary = "\n".join(summary_parts)
    
    # 存储到共享记忆
    try:
        hub = MemoryHub(agent_name='claude-code-agent')
        memory_id = hub.add(
            content=summary,
            memory_type='observation',
            importance=9.0,  # 高重要性
            tags=['memory-md', 'compressed', 'daily-summary']
        )
        print(f"✅ MEMORY.md 摘要已存储到共享记忆 (ID: {memory_id})")
        print(f"   内容长度：{len(summary)} 字符")
    except Exception as e:
        print(f"⚠️  存储失败：{e}")


# 需要导入 timedelta
from datetime import timedelta


def main():
    compress_memory_md()


if __name__ == "__main__":
    main()
