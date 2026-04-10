#!/usr/bin/env python3
"""
记忆管理器 - 统一的记忆压缩和管理系统

功能:
- 每日记忆压缩（保留 14 天）
- 周记忆压缩（保留 8 周）
- 月记忆压缩（保留 2 个月）
- 自动清理过期记忆
- 存储到共享记忆
- 分层搜索（月→周→日）

用法:
    python3 scripts/core/memory_manager.py --daily
    python3 scripts/core/memory_manager.py --weekly
    python3 scripts/core/memory_manager.py --monthly
    python3 scripts/core/memory_manager.py --all
    python3 scripts/core/memory_manager.py --search "关键词"
"""

import argparse
import json
import re
import shutil
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
WEEKLY_DIR = MEMORY_DIR / "weekly"
MONTHLY_DIR = MEMORY_DIR / "monthly"
ARCHIVE_DIR = MEMORY_DIR / "archive"

# 保留策略
DAILY_KEEP_DAYS = 14       # 每日记忆保留 14 天
WEEKLY_KEEP_WEEKS = 8      # 周记忆保留 8 周
MONTHLY_KEEP_MONTHS = 2    # 月记忆保留 2 个月

# 状态文件
STATE_FILE = MEMORY_DIR / ".memory_manager_state.json"


def load_state() -> dict:
    """加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'last_daily_compress': None,
        'last_weekly_compress': None,
        'last_monthly_compress': None,
        'total_compressions': 0
    }


def save_state(state: dict):
    """保存状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_content_hash(content: str) -> str:
    """计算内容哈希"""
    import hashlib
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def extract_sections(content: str) -> dict:
    """从 markdown 中提取各个部分"""
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_content)
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = "\n".join(current_content)
    
    return sections


def extract_key_lines(content: str) -> dict:
    """从 markdown 中提取关键行"""
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


def store_to_memory(content: str, memory_type: str, importance: float, tags: list):
    """存储到共享记忆"""
    try:
        hub = MemoryHub(agent_name='claude-code-agent')
        memory_id = hub.add(
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags
        )
        return memory_id
    except Exception as e:
        print(f"⚠️  存储失败：{e}")
        return None


def compress_daily():
    """每日记忆压缩"""
    print("📅 每日记忆压缩...")
    
    state = load_state()
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    
    # 检查今日记忆文件
    daily_file = MEMORY_DIR / f"{today_str}.md"
    if not daily_file.exists():
        print("  ⏭️  今日记忆文件不存在，跳过")
        return
    
    content = daily_file.read_text(encoding='utf-8')
    current_hash = get_content_hash(content)
    
    # 检查是否已压缩
    if state.get('last_daily_compress') == today_str and \
       state.get('last_daily_hash') == current_hash:
        print("  ⏭️  今日已压缩，跳过")
        return
    
    # 提取内容
    sections = extract_sections(content)
    extracted = extract_key_lines(content)
    
    # 生成压缩摘要
    summary_parts = [f"# {today_str} 记忆摘要"]
    summary_parts.append("")
    
    if extracted["events"]:
        summary_parts.append("## 📌 主要事件")
        for event in extracted["events"][:5]:
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
    memory_id = store_to_memory(
        content=summary,
        memory_type='observation',
        importance=8.0,
        tags=['daily-summary', today_str]
    )
    
    if memory_id:
        print(f"  ✅ 已压缩并存储 (ID: {memory_id})")
        
        # 更新状态
        state['last_daily_compress'] = today_str
        state['last_daily_hash'] = current_hash
        state['total_compressions'] = state.get('total_compressions', 0) + 1
        save_state(state)
    
    # 清理超过 14 天的每日记忆文件
    cleanup_old_files(MEMORY_DIR, "daily", DAILY_KEEP_DAYS)


def compress_weekly():
    """周记忆压缩"""
    print("📅 周记忆压缩...")
    
    today = datetime.now()
    # 计算本周一
    last_monday = today - timedelta(days=today.weekday())
    last_sunday = last_monday + timedelta(days=6)
    week_num = last_monday.isocalendar()[1]
    year = last_monday.year
    
    weekly_file = WEEKLY_DIR / f"{year}-W{week_num:02d}.md"
    
    # 收集本周的每日记忆
    daily_files = []
    current = last_monday
    while current <= last_sunday:
        date_str = current.strftime("%Y-%m-%d")
        daily_file = MEMORY_DIR / f"{date_str}.md"
        if daily_file.exists():
            daily_files.append((date_str, daily_file.read_text(encoding='utf-8')))
        current += timedelta(days=1)
    
    if not daily_files:
        print("  ⏭️  本周无每日记忆，跳过")
        return
    
    # 生成周摘要
    summary_parts = [f"# {year}-W{week_num:02d} 周摘要 ({last_monday.strftime('%m-%d')} ~ {last_sunday.strftime('%m-%d')})"]
    summary_parts.append("")
    
    all_events = []
    all_decisions = []
    all_learnings = []
    
    for date_str, content in daily_files:
        extracted = extract_key_lines(content)
        all_events.extend([(date_str, e) for e in extracted["events"]])
        all_decisions.extend([(date_str, d) for d in extracted["decisions"]])
        all_learnings.extend([(date_str, l) for l in extracted["learnings"]])
    
    if all_events:
        summary_parts.append("## 📌 本周事件")
        for date_str, event in all_events[:10]:
            summary_parts.append(f"- [{date_str}] {event}")
        summary_parts.append("")
    
    if all_decisions:
        summary_parts.append("## 🔨 本周决定")
        for date_str, decision in all_decisions[:5]:
            summary_parts.append(f"- [{date_str}] {decision}")
        summary_parts.append("")
    
    if all_learnings:
        summary_parts.append("## 📚 本周学习")
        for date_str, learning in all_learnings[:5]:
            summary_parts.append(f"- [{date_str}] {learning}")
        summary_parts.append("")
    
    summary = "\n".join(summary_parts)
    
    # 保存周摘要文件
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    weekly_file.write_text(summary, encoding='utf-8')
    
    # 存储到共享记忆
    memory_id = store_to_memory(
        content=summary,
        memory_type='observation',
        importance=7.0,
        tags=['weekly-summary', f'{year}-W{week_num:02d}']
    )
    
    if memory_id:
        print(f"  ✅ 周摘要已保存 (ID: {memory_id}, 文件：{weekly_file.name})")
    
    # 清理超过 8 周的周摘要
    cleanup_old_files(WEEKLY_DIR, "weekly", WEEKLY_KEEP_WEEKS * 7)


def compress_monthly():
    """月记忆压缩"""
    print("📅 月记忆压缩...")
    
    today = datetime.now()
    # 计算上月
    if today.month == 1:
        last_month = 12
        last_year = today.year - 1
    else:
        last_month = today.month - 1
        last_year = today.year
    
    monthly_file = MONTHLY_DIR / f"{last_year}-{last_month:02d}.md"
    
    # 收集上月的周摘要
    weekly_files = sorted(WEEKLY_DIR.glob(f"{last_year}-W*.md"))
    monthly_weeks = []
    
    for wf in weekly_files:
        # 简单判断是否属于该月
        content = wf.read_text(encoding='utf-8')
        if f"{last_year}-{last_month:02d}" in wf.name or \
           f"{last_month:02d}" in content.split("\n")[0]:
            monthly_weeks.append((wf.name, content))
    
    if not monthly_weeks:
        print("  ⏭️  上月无周摘要，跳过")
        return
    
    # 生成月摘要
    summary_parts = [f"# {last_year}-{last_month:02d} 月摘要"]
    summary_parts.append("")
    summary_parts.append(f"_包含 {len(monthly_weeks)} 周的摘要_")
    summary_parts.append("")
    
    # 汇总关键内容
    all_events = []
    all_decisions = []
    all_learnings = []
    
    for week_name, content in monthly_weeks:
        sections = extract_sections(content)
        if "本周事件" in sections:
            for line in sections["本周事件"].split("\n"):
                if line.strip().startswith("- "):
                    all_events.append((week_name, line.strip()[2:]))
        if "本周决定" in sections:
            for line in sections["本周决定"].split("\n"):
                if line.strip().startswith("- "):
                    all_decisions.append((week_name, line.strip()[2:]))
        if "本周学习" in sections:
            for line in sections["本周学习"].split("\n"):
                if line.strip().startswith("- "):
                    all_learnings.append((week_name, line.strip()[2:]))
    
    if all_events:
        summary_parts.append("## 📌 本月事件")
        for week, event in all_events[:15]:
            summary_parts.append(f"- [{week}] {event}")
        summary_parts.append("")
    
    if all_decisions:
        summary_parts.append("## 🔨 本月决定")
        for week, decision in all_decisions[:8]:
            summary_parts.append(f"- [{week}] {decision}")
        summary_parts.append("")
    
    if all_learnings:
        summary_parts.append("## 📚 本月学习")
        for week, learning in all_learnings[:8]:
            summary_parts.append(f"- [{week}] {learning}")
        summary_parts.append("")
    
    summary = "\n".join(summary_parts)
    
    # 保存月摘要文件
    MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    monthly_file.write_text(summary, encoding='utf-8')
    
    # 存储到共享记忆
    memory_id = store_to_memory(
        content=summary,
        memory_type='observation',
        importance=6.0,
        tags=['monthly-summary', f'{last_year}-{last_month:02d}']
    )
    
    if memory_id:
        print(f"  ✅ 月摘要已保存 (ID: {memory_id}, 文件：{monthly_file.name})")
    
    # 清理超过 2 个月的月摘要
    cleanup_old_files(MONTHLY_DIR, "monthly", MONTHLY_KEEP_MONTHS * 30)


def cleanup_old_files(directory: Path, file_type: str, keep_days: int):
    """清理过期文件"""
    if not directory.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    removed = 0
    
    for file in directory.glob("*.md"):
        # 从文件名提取日期
        match = re.search(r'(\d{4}-\d{2}-\d{2})', file.name)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if file_date < cutoff_date:
                # 移动到归档目录
                archive_subdir = ARCHIVE_DIR / file_type / file_date.strftime("%Y/%m")
                archive_subdir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file), str(archive_subdir / file.name))
                removed += 1
    
    if removed > 0:
        print(f"  🗑️  清理 {removed} 个过期{file_type}文件 (> {keep_days}天)")


def search_memory(query: str, top_k: int = 10):
    """分层搜索：月→周→日"""
    print(f"🔍 搜索：{query}")
    print("")
    
    hub = MemoryHub(agent_name='claude-code-agent')
    
    # 1. 先搜月记忆
    print("📅 搜索月记忆...")
    monthly_results = hub.search(f"{query} monthly-summary", top_k=2)
    if monthly_results:
        print(f"  ✅ 找到 {len(monthly_results)} 条月记忆")
        for r in monthly_results[:1]:
            print(f"    - {r['content'][:100]}...")
    else:
        print("  ⏭️  无月记忆")
    
    # 2. 再搜周记忆
    print("\n📅 搜索周记忆...")
    weekly_results = hub.search(f"{query} weekly-summary", top_k=3)
    if weekly_results:
        print(f"  ✅ 找到 {len(weekly_results)} 条周记忆")
        for r in weekly_results[:2]:
            print(f"    - {r['content'][:100]}...")
    else:
        print("  ⏭️  无周记忆")
    
    # 3. 最后搜日记忆
    print("\n📅 搜索日记忆...")
    daily_results = hub.search(f"{query} daily-summary", top_k=5)
    if daily_results:
        print(f"  ✅ 找到 {len(daily_results)} 条日记忆")
        for r in daily_results[:3]:
            print(f"    - {r['content'][:100]}...")
    else:
        print("  ⏭️  无日记忆")
    
    # 4. 如果都没找到，全量搜索
    if not monthly_results and not weekly_results and not daily_results:
        print("\n🔍 全量搜索日记忆...")
        all_results = hub.search(query, top_k=top_k)
        if all_results:
            print(f"  ✅ 找到 {len(all_results)} 条记忆")
            for r in all_results[:5]:
                print(f"    - [{r.get('tags', ['unknown'])[0]}] {r['content'][:100]}...")
        else:
            print("  ⏭️  未找到相关记忆")
    
    print("")


def main():
    parser = argparse.ArgumentParser(description="记忆管理器")
    parser.add_argument("--daily", action="store_true", help="每日压缩")
    parser.add_argument("--weekly", action="store_true", help="周压缩")
    parser.add_argument("--monthly", action="store_true", help="月压缩")
    parser.add_argument("--all", action="store_true", help="全部压缩")
    parser.add_argument("--search", type=str, help="搜索记忆")
    parser.add_argument("--top-k", type=int, default=10, help="搜索结果数量")
    args = parser.parse_args()
    
    if not any([args.daily, args.weekly, args.monthly, args.all, args.search]):
        parser.print_help()
        return
    
    print("🗄️  记忆管理器\n")
    
    if args.search:
        search_memory(args.search, args.top_k)
    else:
        if args.daily or args.all:
            compress_daily()
        if args.weekly or args.all:
            compress_weekly()
        if args.monthly or args.all:
            compress_monthly()
    
    print("\n✅ 完成")


if __name__ == "__main__":
    main()
