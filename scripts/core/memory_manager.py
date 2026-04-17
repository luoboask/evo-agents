#!/usr/bin/env python3
"""
记忆管理器 - 统一的记忆压缩和管理系统（整合版）

功能:
- 每日回顾（创建今日记忆 + 显示昨日摘要）
- 每日记忆压缩（保留 14 天）
- 周记忆压缩（保留 8 周）
- 月记忆压缩（保留 2 个月）
- MEMORY.md 文件压缩
- 自动清理过期记忆和空文件
- 系统统计
- 存储到共享记忆
- 分层搜索（月→周→日）

用法:
    python3 scripts/core/memory_manager.py --review         # 每日回顾
    python3 scripts/core/memory_manager.py --daily          # 每日增量压缩
    python3 scripts/core/memory_manager.py --weekly         # 周摘要
    python3 scripts/core/memory_manager.py --monthly        # 月摘要
    python3 scripts/core/memory_manager.py --compress       # MEMORY.md 压缩
    python3 scripts/core/memory_manager.py --cleanup        # 清理过期 + 空文件
    python3 scripts/core/memory_manager.py --stats          # 系统统计
    python3 scripts/core/memory_manager.py --search "关键词"  # 搜索记忆
    python3 scripts/core/memory_manager.py --all            # 全部执行
"""

import argparse
import json
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# 添加 libs 到路径
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

from memory_hub import MemoryHub
from path_utils import resolve_workspace

# 记忆限制常量
MEMORY_LIMIT = 2200  # MEMORY.md 字符限制
USER_LIMIT = 1375    # USER.md 字符限制

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


# ============================================================================
# 每日回顾
# ============================================================================

def get_yesterday_date():
    """获取昨天日期"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_today_date():
    """获取今天日期"""
    return datetime.now().strftime('%Y-%m-%d')


def read_memory_file(date_str):
    """读取记忆文件"""
    memory_file = MEMORY_DIR / f"{date_str}.md"
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def create_today_memory():
    """创建今日记忆文件"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    today = get_today_date()
    today_file = MEMORY_DIR / f"{today}.md"
    
    created = False
    if not today_file.exists():
        with open(today_file, 'w', encoding='utf-8') as f:
            f.write(f"# {today} - 会话记录\n\n## 会话\n\n")
        created = True
    
    return created, today


def get_yesterday_memory_summary():
    """获取昨日记忆摘要"""
    yesterday = get_yesterday_date()
    content = read_memory_file(yesterday)
    
    if not content:
        return None, yesterday
    
    # 提取关键内容（标题、列表项、待办事项）
    lines = content.split('\n')
    summary_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('#') or line.startswith('- ') or line.startswith('* '):
            summary_lines.append(line)
        elif '[x]' in line or '[ ]' in line:
            summary_lines.append(line)
    
    return '\n'.join(summary_lines[:50]), yesterday


def daily_review():
    """执行每日回顾"""
    output = []
    
    output.append("=" * 60)
    output.append("📅 每日回顾 - Daily Review")
    output.append("=" * 60)
    output.append("")
    
    # 创建今日记忆文件
    created, today = create_today_memory()
    
    if created:
        output.append(f"✅ 已创建今日记忆文件：memory/{today}.md")
    else:
        output.append(f"📄 今日记忆文件已存在：memory/{today}.md")
    output.append("")
    
    # 显示昨日记忆摘要
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
    output.append("💡 提示：你可以随时让我搜索记忆，例如:")
    output.append('   - "我们昨天做了什么？"')
    output.append('   - "搜索关于 websearch 的记忆"')
    output.append('   - "我有什么待办事项？"')
    output.append("=" * 60)
    
    result = '\n'.join(output)
    print(result)
    return result


# ============================================================================
# 状态管理
# ============================================================================

def load_state() -> dict:
    """加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'last_daily_compress': None,
        'last_weekly_compress': None,
        'last_monthly_compress': None,
        'last_cleanup': None,
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


# ============================================================================
# 内容提取工具
# ============================================================================

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
        hub = MemoryHub(agent_name='ai-baby')
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


# ============================================================================
# 记忆压缩功能
# ============================================================================

def compress_daily():
    """每日增量记忆压缩"""
    print("📅 每日增量记忆压缩...")
    
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
    
    # 检查内容是否变化
    if state.get('last_daily_hash') == current_hash:
        print("  ⏭️  今日内容无变化，跳过")
        return
    
    # 提取新增内容（对比昨日）
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    yesterday_file = MEMORY_DIR / f"{yesterday_str}.md"
    
    yesterday_content = ""
    if yesterday_file.exists():
        yesterday_content = yesterday_file.read_text(encoding='utf-8')
    
    # 提取今日内容
    extracted = extract_key_lines(content)
    yesterday_extracted = extract_key_lines(yesterday_content) if yesterday_content else {"events": [], "decisions": [], "learnings": []}
    
    # 计算增量（今日 - 昨日）
    new_events = [e for e in extracted["events"] if e not in yesterday_extracted["events"]]
    new_decisions = [d for d in extracted["decisions"] if d not in yesterday_extracted["decisions"]]
    new_learnings = [l for l in extracted["learnings"] if l not in yesterday_extracted["learnings"]]
    
    # 如果没有增量，跳过
    if not new_events and not new_decisions and not new_learnings:
        print("  ⏭️  无新增内容，跳过")
        state['last_daily_compress'] = today_str
        state['last_daily_hash'] = current_hash
        save_state(state)
        return
    
    # 生成增量摘要
    summary_parts = [f"# {today_str} 增量摘要"]
    summary_parts.append("")
    
    if new_events:
        summary_parts.append("## 📌 新增事件")
        for event in new_events[:5]:
            summary_parts.append(f"- {event}")
        summary_parts.append("")
    
    if new_decisions:
        summary_parts.append("## 🔨 新增决定")
        for decision in new_decisions[:3]:
            summary_parts.append(f"- {decision}")
        summary_parts.append("")
    
    if new_learnings:
        summary_parts.append("## 📚 新增学习")
        for learning in new_learnings[:3]:
            summary_parts.append(f"- {learning}")
        summary_parts.append("")
    
    summary = "\n".join(summary_parts)
    
    # 存储到共享记忆
    memory_id = store_to_memory(
        content=summary,
        memory_type='observation',
        importance=8.0,
        tags=['daily-summary', 'incremental', today_str]
    )
    
    if memory_id:
        print(f"  ✅ 增量摘要已存储 (ID: {memory_id})")
        print(f"     新增：{len(new_events)} 事件，{len(new_decisions)} 决定，{len(new_learnings)} 学习")
        
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
    
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    weekly_file.write_text(summary, encoding='utf-8')
    
    memory_id = store_to_memory(
        content=summary,
        memory_type='observation',
        importance=7.0,
        tags=['weekly-summary', f'{year}-W{week_num:02d}']
    )
    
    if memory_id:
        print(f"  ✅ 周摘要已保存 (ID: {memory_id}, 文件：{weekly_file.name})")
    
    cleanup_old_files(WEEKLY_DIR, "weekly", WEEKLY_KEEP_WEEKS * 7)


def compress_monthly():
    """月记忆压缩"""
    print("📅 月记忆压缩...")
    
    today = datetime.now()
    if today.month == 1:
        last_month = 12
        last_year = today.year - 1
    else:
        last_month = today.month - 1
        last_year = today.year
    
    monthly_file = MONTHLY_DIR / f"{last_year}-{last_month:02d}.md"
    
    monthly_weeks = []
    
    if WEEKLY_DIR.exists():
        for wf in WEEKLY_DIR.glob("*.md"):
            import re
            match = re.search(r"(\d{4})-W(\d{2})", wf.name)
            if match:
                week_year = int(match.group(1))
                week_num = int(match.group(2))
                
                jan1 = datetime(week_year, 1, 1)
                first_monday = jan1 + timedelta(days=(7 - jan1.weekday()) % 7)
                week_monday = first_monday + timedelta(weeks=week_num - 1)
                
                if week_monday.year == last_year and week_monday.month == last_month:
                    monthly_weeks.append((wf.name, wf.read_text(encoding='utf-8')))
    
    if not monthly_weeks:
        print("  ⏭️  上月无周摘要，跳过")
        return
    
    summary_parts = [f"# {last_year}-{last_month:02d} 月摘要"]
    summary_parts.append("")
    summary_parts.append(f"_包含 {len(monthly_weeks)} 周的摘要_")
    summary_parts.append("")
    
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
    
    MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    monthly_file.write_text(summary, encoding='utf-8')
    
    memory_id = store_to_memory(
        content=summary,
        memory_type='observation',
        importance=6.0,
        tags=['monthly-summary', f'{last_year}-{last_month:02d}']
    )
    
    if memory_id:
        print(f"  ✅ 月摘要已保存 (ID: {memory_id}, 文件：{monthly_file.name})")
    
    cleanup_old_files(MONTHLY_DIR, "monthly", MONTHLY_KEEP_MONTHS * 30)


# ============================================================================
# MEMORY.md 压缩功能（从 compress_memory.py 整合）
# ============================================================================

def analyze_memory_file(workspace_root: Path) -> dict:
    """分析 MEMORY.md 内容结构"""
    memory_file = workspace_root / 'MEMORY.md'
    if not memory_file.exists():
        return {'error': 'MEMORY.md not found'}
    
    content = memory_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    sections = []
    current_section = {'name': 'Header', 'start': 0, 'lines': 0, 'chars': 0}
    
    for i, line in enumerate(lines):
        if line.startswith('## '):
            if current_section['lines'] > 0:
                sections.append(current_section)
            current_section = {
                'name': line.replace('## ', '').strip(),
                'start': i,
                'lines': 1,
                'chars': len(line)
            }
        else:
            current_section['lines'] += 1
            current_section['chars'] += len(line) + 1
    
    if current_section['lines'] > 0:
        sections.append(current_section)
    
    return {
        'total_lines': len(lines),
        'total_chars': len(content),
        'sections': sections,
        'limit': MEMORY_LIMIT,
        'over_by': len(content) - MEMORY_LIMIT
    }


def compress_memory_file(workspace_root: Path, dry_run: bool = False) -> str:
    """压缩 MEMORY.md"""
    memory_file = workspace_root / 'MEMORY.md'
    if not memory_file.exists():
        return "❌ MEMORY.md not found"
    
    content = memory_file.read_text(encoding='utf-8')
    compressed = content
    
    # 1. 移除多余空行（保留最多 2 个连续空行）
    compressed = re.sub(r'\n{3,}', '\n\n', compressed)
    
    # 2. 移除行首行尾空白
    lines = compressed.split('\n')
    lines = [line.rstrip() for line in lines]
    compressed = '\n'.join(lines)
    
    reduction = len(content) - len(compressed)
    reduction_pct = reduction / len(content) * 100 if content else 0
    
    result = f"""
📊 压缩结果:
   原始：{len(content):,} chars
   压缩后：{len(compressed):,} chars
   减少：{reduction:,} chars ({reduction_pct:.1f}%)
   仍超出：{max(0, len(compressed) - MEMORY_LIMIT):,} chars
"""
    
    if not dry_run and reduction > 0:
        backup = memory_file.parent / f'MEMORY.md.backup.{datetime.now().strftime("%Y%m%d%H%M%S")}'
        shutil.copy(str(memory_file), str(backup))
        memory_file.write_text(compressed, encoding='utf-8')
        result += f"\n✅ 已保存到 {memory_file}"
        result += f"\n💾 备份在 {backup}"
    elif dry_run:
        result += "\n⚠️  预览模式，使用 --execute 执行实际压缩"
    
    return result


# ============================================================================
# 清理功能
# ============================================================================

def cleanup_old_files(directory: Path, file_type: str, keep_days: int):
    """清理过期文件"""
    if not directory.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    removed = 0
    
    for file in directory.glob("*.md"):
        match = re.search(r'(\d{4}-\d{2}-\d{2})', file.name)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if file_date < cutoff_date:
                archive_subdir = ARCHIVE_DIR / file_type / file_date.strftime("%Y/%m")
                archive_subdir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file), str(archive_subdir / file.name))
                removed += 1
    
    if removed > 0:
        print(f"  🗑️  清理 {removed} 个过期{file_type}文件 (> {keep_days}天)")


def cleanup_empty_files():
    """清理空文件"""
    print("🧹 清理空文件...")
    
    removed = 0
    for dir_path in [MEMORY_DIR, WEEKLY_DIR, MONTHLY_DIR]:
        if not dir_path.exists():
            continue
        for file in dir_path.glob("*.md"):
            if file.stat().st_size == 0:
                file.unlink()
                removed += 1
    
    if removed > 0:
        print(f"  ✅ 清理 {removed} 个空文件")
    else:
        print("  ⏭️  无空文件")


def run_cleanup():
    """执行完整清理"""
    print("🧹 执行系统清理...\n")
    
    # 清理过期文件
    print("1. 清理过期每日记忆文件...")
    cleanup_old_files(MEMORY_DIR, "daily", DAILY_KEEP_DAYS)
    
    print("\n2. 清理过期周摘要文件...")
    cleanup_old_files(WEEKLY_DIR, "weekly", WEEKLY_KEEP_WEEKS * 7)
    
    print("\n3. 清理过期月摘要文件...")
    cleanup_old_files(MONTHLY_DIR, "monthly", MONTHLY_KEEP_MONTHS * 30)
    
    print("\n4. 清理空文件...")
    cleanup_empty_files()
    
    # 更新状态
    state = load_state()
    state['last_cleanup'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state(state)
    
    print("\n✅ 清理完成")


# ============================================================================
# 统计功能
# ============================================================================

def show_stats():
    """显示系统统计"""
    print("📊 记忆系统统计\n")
    
    # 文件统计
    print("1. 文件统计:")
    daily_count = len(list(MEMORY_DIR.glob("*.md"))) if MEMORY_DIR.exists() else 0
    weekly_count = len(list(WEEKLY_DIR.glob("*.md"))) if WEEKLY_DIR.exists() else 0
    monthly_count = len(list(MONTHLY_DIR.glob("*.md"))) if MONTHLY_DIR.exists() else 0
    print(f"   每日记忆文件：{daily_count}")
    print(f"   周摘要文件：{weekly_count}")
    print(f"   月摘要文件：{monthly_count}")
    
    # MEMORY.md 状态
    print("\n2. MEMORY.md 状态:")
    memory_file = WORKSPACE / 'MEMORY.md'
    if memory_file.exists():
        content = memory_file.read_text(encoding='utf-8')
        chars = len(content)
        pct = chars / MEMORY_LIMIT * 100
        status = "✅" if chars <= MEMORY_LIMIT else "⚠️"
        print(f"   {status} 字符数：{chars:,} / {MEMORY_LIMIT:,} ({pct:.1f}%)")
    else:
        print("   ❌ 文件不存在")
    
    # 状态信息
    print("\n3. 最后执行时间:")
    state = load_state()
    print(f"   每日压缩：{state.get('last_daily_compress', '从未')}")
    print(f"   每周压缩：{state.get('last_weekly_compress', '从未')}")
    print(f"   每月压缩：{state.get('last_monthly_compress', '从未')}")
    print(f"   系统清理：{state.get('last_cleanup', '从未')}")
    print(f"   总压缩次数：{state.get('total_compressions', 0)}")
    
    # 共享记忆统计
    print("\n4. 共享记忆:")
    try:
        hub = MemoryHub(agent_name='ai-baby')
        stats = hub.stats()
        print(f"   总记忆数：{stats.get('total', 0)}")
        print(f"   向量数：{stats.get('vectors', 0)}")
    except Exception as e:
        print(f"   ⚠️  无法获取统计：{e}")
    
    print("")


# ============================================================================
# 搜索功能
# ============================================================================

def search_memory(query: str, top_k: int = 10):
    """分层搜索：月→周→日"""
    print(f"🔍 搜索：{query}\n")
    
    hub = MemoryHub(agent_name='ai-baby')
    
    print("📅 搜索月记忆...")
    monthly_results = hub.search(f"{query} monthly-summary", top_k=2)
    if monthly_results:
        print(f"  ✅ 找到 {len(monthly_results)} 条月记忆")
        for r in monthly_results[:1]:
            print(f"    - {r['content'][:100]}...")
    else:
        print("  ⏭️  无月记忆")
    
    print("\n📅 搜索周记忆...")
    weekly_results = hub.search(f"{query} weekly-summary", top_k=3)
    if weekly_results:
        print(f"  ✅ 找到 {len(weekly_results)} 条周记忆")
        for r in weekly_results[:2]:
            print(f"    - {r['content'][:100]}...")
    else:
        print("  ⏭️  无周记忆")
    
    print("\n📅 搜索日记忆...")
    daily_results = hub.search(f"{query} daily-summary", top_k=5)
    if daily_results:
        print(f"  ✅ 找到 {len(daily_results)} 条日记忆")
        for r in daily_results[:3]:
            print(f"    - {r['content'][:100]}...")
    else:
        print("  ⏭️  无日记忆")
    
    if not monthly_results and not weekly_results and not daily_results:
        print("\n🔍 全量搜索...")
        all_results = hub.search(query, top_k=top_k)
        if all_results:
            print(f"  ✅ 找到 {len(all_results)} 条记忆")
            for r in all_results[:5]:
                print(f"    - [{r.get('tags', ['unknown'])[0]}] {r['content'][:100]}...")
        else:
            print("  ⏭️  未找到相关记忆")
    
    print("")


# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="记忆管理器 - 统一的记忆压缩和管理系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/core/memory_manager.py --review         # 每日回顾
  python3 scripts/core/memory_manager.py --daily          # 每日增量压缩
  python3 scripts/core/memory_manager.py --weekly         # 周摘要
  python3 scripts/core/memory_manager.py --monthly        # 月摘要
  python3 scripts/core/memory_manager.py --compress       # MEMORY.md 压缩
  python3 scripts/core/memory_manager.py --cleanup        # 清理过期 + 空文件
  python3 scripts/core/memory_manager.py --stats          # 系统统计
  python3 scripts/core/memory_manager.py --search "关键词"  # 搜索记忆
  python3 scripts/core/memory_manager.py --all            # 全部执行
        """
    )
    
    parser.add_argument("--review", action="store_true", help="每日回顾（创建今日记忆 + 显示昨日摘要）")
    parser.add_argument("--daily", action="store_true", help="每日增量压缩")
    parser.add_argument("--weekly", action="store_true", help="周摘要")
    parser.add_argument("--monthly", action="store_true", help="月摘要")
    parser.add_argument("--compress", action="store_true", help="MEMORY.md 压缩")
    parser.add_argument("--cleanup", action="store_true", help="清理过期 + 空文件")
    parser.add_argument("--stats", action="store_true", help="系统统计")
    parser.add_argument("--search", type=str, help="搜索记忆")
    parser.add_argument("--top-k", type=int, default=10, help="搜索结果数量")
    parser.add_argument("--dry-run", action="store_true", help="预览模式（不实际修改）")
    parser.add_argument("--execute", action="store_true", help="执行实际压缩（与 --compress 配合）")
    parser.add_argument("--all", action="store_true", help="全部执行")
    
    args = parser.parse_args()
    
    if not any([args.review, args.daily, args.weekly, args.monthly, args.compress, args.cleanup, args.stats, args.search, args.all]):
        parser.print_help()
        return
    
    print("🗄️  记忆管理器\n")
    
    if args.review:
        daily_review()
    elif args.search:
        search_memory(args.search, args.top_k)
    elif args.stats:
        show_stats()
    elif args.compress:
        print("📝 MEMORY.md 压缩...\n")
        analysis = analyze_memory_file(WORKSPACE)
        if 'error' in analysis:
            print(f"❌ {analysis['error']}")
            return
        print(f"   总字符数：{analysis['total_chars']:,}")
        print(f"   限制：{MEMORY_LIMIT:,}")
        print(f"   超出：{analysis['over_by']:,} chars")
        print(f"   章节数：{len(analysis['sections'])}")
        print("")
        result = compress_memory_file(WORKSPACE, dry_run=not args.execute)
        print(result)
    elif args.cleanup:
        run_cleanup()
    else:
        if args.daily or args.all:
            compress_daily()
        if args.weekly or args.all:
            compress_weekly()
        if args.monthly or args.all:
            compress_monthly()
        if args.cleanup or args.all:
            run_cleanup()
    
    print("\n✅ 完成")


if __name__ == "__main__":
    main()
