#!/usr/bin/env python3
"""
事件同步脚本
从每日记忆文件提取事件，同步到 SQLite 记忆流数据库
"""

import re
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


# 运行时配置（由 main 注入）
WORKSPACE = Path.cwd()
MEMORY_DIR = WORKSPACE / 'memory'
DB_PATH = WORKSPACE / 'data' / 'demo-agent' / 'memory' / 'memory_stream.db'
OLLAMA_URL = 'http://localhost:11434/api/embeddings'


def get_embedding(text: str) -> List[float]:
    """使用 Ollama 生成嵌入向量"""
    try:
        result = subprocess.run(
            ["curl", "-s", OLLAMA_URL,
             "-H", "Content-Type: application/json",
             "-d", json.dumps({"model": "nomic-embed-text", "prompt": text[:500]})],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("embedding", [])
    except Exception as e:
        print(f"  ⚠️ 嵌入生成失败：{e}")
    return []


def parse_daily_file(filepath: Path) -> List[Dict]:
    """
    解析每日记忆文件，提取结构化事件
    
    识别模式：
    - ## 标题 (章节)
    - **Trigger:** 触发器
    - **Actions Taken:** 行动
    - **Learned & Recorded:** 学习内容
    - **Lesson:** 教训/洞察
    - **Result:** 结果
    - **Insights:** 洞察
    """
    if not filepath.exists():
        print(f"  ⚠️ 文件不存在：{filepath}")
        return []
    
    content = filepath.read_text(encoding='utf-8')
    events = []
    
    # 按章节分割
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    
    for section in sections[1:]:  # 跳过第一个空章节
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        title = lines[0].strip()
        body = '\n'.join(lines[1:])
        
        # 提取关键信息
        trigger_match = re.search(r'\*\*Trigger:\*\*\s*(.+)', body)
        actions_match = re.search(r'\*\*Actions Taken:\*\*\n(.+?)(?=\n\*\*|\n\n|$)', body, re.DOTALL)
        lesson_match = re.search(r'\*\*Lesson:\*\*\s*(.+)', body)
        result_match = re.search(r'\*\*Result:\*\*\s*(.+)', body)
        insights_match = re.search(r'\*\*Insights?:\*\*\s*(.+)', body, re.DOTALL)
        learned_match = re.search(r'\*\*Learned & Recorded:\*\*\n(.+?)(?=\n\*\*|\n\n|$)', body, re.DOTALL)
        
        # 确定事件类型
        if 'Learned' in title or '学习' in title:
            event_type = 'learning'
        elif 'Evolution' in title or '进化' in title:
            event_type = 'evolution'
        elif 'Reflection' in title or '反思' in title:
            event_type = 'reflection'
        elif 'Insight' in title or '洞察' in title:
            event_type = 'insight'
        elif 'Onboarding' in title or 'Onboarding' in title:
            event_type = 'milestone'
        else:
            event_type = 'observation'
        
        # 构建事件记录
        event = {
            'title': title,
            'type': event_type,
            'date': filepath.stem,  # YYYY-MM-DD
            'trigger': trigger_match.group(1).strip() if trigger_match else None,
            'actions': actions_match.group(1).strip() if actions_match else None,
            'lesson': lesson_match.group(1).strip() if lesson_match else None,
            'result': result_match.group(1).strip() if result_match else None,
            'insights': insights_match.group(1).strip() if insights_match else None,
            'learned': learned_match.group(1).strip() if learned_match else None,
            'raw_body': body.strip()
        }
        
        events.append(event)
    
    return events


def memory_exists(db_path: Path, content: str) -> bool:
    """检查记忆是否已存在（基于内容相似度）"""
    if not db_path.exists():
        return False
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 检查完全匹配
    cur.execute('SELECT id FROM memories WHERE content = ?', (content,))
    if cur.fetchone():
        conn.close()
        return True
    
    # 检查包含关系（避免重复记录）
    cur.execute('SELECT id, content FROM memories WHERE memory_type = ?', ('learning',))
    existing = cur.fetchall()
    
    for existing_id, existing_content in existing:
        # 如果新内容包含已有内容，或已有内容包含新内容，视为重复
        if content in existing_content or existing_content in content:
            conn.close()
            return True
    
    conn.close()
    return False


def sync_event(db_path: Path, event: Dict) -> Tuple[int, bool]:
    """
    同步单个事件到数据库
    
    Returns:
        (memory_id, is_new) - 记忆 ID 和是否为新记录
    """
    # 构建记忆内容
    content_parts = []
    
    if event.get('title'):
        content_parts.append(f"【{event['title']}】")
    
    if event.get('learned'):
        content_parts.append(event['learned'])
    elif event.get('result'):
        content_parts.append(event['result'])
    elif event.get('actions'):
        content_parts.append(event['actions'])
    elif event.get('insights'):
        content_parts.append(event['insights'])
    
    if event.get('lesson'):
        content_parts.append(f"教训：{event['lesson']}")
    
    content = ' | '.join(content_parts)
    
    # 去重检查
    if memory_exists(db_path, content):
        print(f"  ⏭️  跳过（已存在）: {event['title'][:40]}...")
        return None, False
    
    # 确定记忆类型
    type_mapping = {
        'learning': 'observation',
        'evolution': 'reflection',
        'reflection': 'reflection',
        'insight': 'reflection',
        'milestone': 'goal',
        'observation': 'observation'
    }
    memory_type = type_mapping.get(event['type'], 'observation')
    
    # 计算重要性
    importance = 5.0
    if event['type'] in ['evolution', 'reflection']:
        importance += 2.0
    if event.get('lesson'):
        importance += 1.0
    if event.get('learned'):
        importance += 1.5
    
    # 提取标签
    tags = [event['type'], event['date']]
    if event.get('title'):
        # 从标题提取关键词
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,}|[A-Za-z]{3,}', event['title'])
        tags.extend(keywords[:3])
    
    # 生成嵌入
    print(f"  🧠 生成嵌入向量...")
    embedding = get_embedding(content)
    
    # 构建元数据
    metadata = {
        'event_type': event['type'],
        'trigger': event.get('trigger'),
        'source_file': f"{event['date']}.md",
        'title': event['title']
    }
    
    # 插入数据库
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO memories (content, memory_type, importance, tags, embedding, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        content,
        memory_type,
        importance,
        json.dumps(tags, ensure_ascii=False),
        json.dumps(embedding, ensure_ascii=False) if embedding else '[]',
        json.dumps(metadata, ensure_ascii=False),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    
    memory_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    print(f"  ✅ 已同步：{event['title'][:50]}... (ID: {memory_id}, 重要性：{importance})")
    return memory_id, True


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description="同步 daily memory 到 agent 数据库")
    parser.add_argument("--workspace", required=True, help="Workspace 路径")
    parser.add_argument("--agent", default="demo-agent", help="Agent 名称")
    parser.add_argument("--date", help="指定日期 YYYY-MM-DD")
    args = parser.parse_args()

    global WORKSPACE, MEMORY_DIR, DB_PATH
    WORKSPACE = Path(args.workspace).expanduser().resolve()
    MEMORY_DIR = WORKSPACE / 'memory'
    DB_PATH = WORKSPACE / 'data' / args.agent / 'memory' / 'memory_stream.db'

    print("=" * 60)
    print(f"🤖 事件同步 (agent={args.agent})")
    print("=" * 60)
    
    # 确定要同步的文件
    if args.date:
        date_str = args.date
        daily_file = MEMORY_DIR / f"{date_str}.md"
        files_to_sync = [daily_file]
    else:
        # 同步今天和昨天
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        files_to_sync = [
            MEMORY_DIR / f"{today}.md",
            MEMORY_DIR / f"{yesterday}.md"
        ]
    
    # 确保数据库存在
    if not DB_PATH.exists():
        print(f"  ⚠️ 数据库不存在，创建中...")
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                memory_type TEXT DEFAULT 'observation',
                importance REAL DEFAULT 5.0,
                tags TEXT DEFAULT '[]',
                last_accessed TEXT,
                embedding BLOB,
                metadata TEXT DEFAULT '{}'
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reflection_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id_1 INTEGER,
                memory_id_2 INTEGER,
                link_type TEXT,
                strength REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    total_events = 0
    new_events = 0
    skipped_events = 0
    
    for daily_file in files_to_sync:
        if not daily_file.exists():
            print(f"\n⏭️  跳过（文件不存在）: {daily_file.name}")
            continue
        
        print(f"\n📄 解析：{daily_file.name}")
        events = parse_daily_file(daily_file)
        
        if not events:
            print(f"  ⚠️ 未找到可同步的事件")
            continue
        
        print(f"  找到 {len(events)} 个事件")
        
        for event in events:
            total_events += 1
            memory_id, is_new = sync_event(DB_PATH, event)
            if is_new:
                new_events += 1
            else:
                skipped_events += 1
    
    # 统计
    print("\n" + "=" * 60)
    print("📊 同步完成")
    print("=" * 60)
    print(f"  处理文件：{len(files_to_sync)}")
    print(f"  总事件数：{total_events}")
    print(f"  新增记忆：{new_events}")
    print(f"  跳过重复：{skipped_events}")
    
    # 数据库统计
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM memories')
        total = cur.fetchone()[0]
        cur.execute('SELECT memory_type, COUNT(*) FROM memories GROUP BY memory_type')
        by_type = dict(cur.fetchall())
        conn.close()
        
        print(f"\n  数据库状态:")
        print(f"    总记忆数：{total}")
        print(f"    按类型：{by_type}")
    
    print("=" * 60)
    
    return 0 if new_events > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
