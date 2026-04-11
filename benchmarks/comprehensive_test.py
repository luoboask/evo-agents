#!/usr/bin/env python3
"""
综合基准测试 - 测试所有记忆类型

覆盖范围:
1. 会话记忆 (Session Memories)
2. 共享记忆 (Shared Memory / MEMORY.md)
3. 知识图谱 (Knowledge Graph)
4. 每日记忆 (Daily Memories - YYYY-MM-DD.md)
5. 进化事件 (Evolution Events)

用法:
    cd /Users/dhr/.openclaw/workspace-demo51-agent
    PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
      python3 /Users/dhr/cursor/evo-agents/benchmarks/comprehensive_test.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加 libs 路径
workspace = Path.cwd()
sys.path.insert(0, str(workspace / 'libs'))

from memory_hub import MemoryHub


def test_session_memories(agent_name: str):
    """测试 1: 会话记忆"""
    print("\n" + "="*60)
    print("📊 测试 1: 会话记忆 (Session Memories)")
    print("="*60)
    
    memory = MemoryHub(agent_name=agent_name)
    
    # 获取所有会话
    sessions = memory.session_storage.get_all_sessions()
    
    # 统计
    total_memories = 0
    for session_id in sessions[:10]:
        memories = memory.session_storage.search_memories(session_id=session_id, top_k=100)
        total_memories += len(memories)
    
    print(f"✅ 会话数：{len(sessions)}")
    print(f"✅ 前 10 个会话的记忆数：{total_memories}")
    print(f"✅ 平均每会话：{total_memories/max(len(sessions[:10]),1):.1f} 条")
    
    return {
        'type': 'session_memories',
        'total_sessions': len(sessions),
        'sample_memories': total_memories,
        'avg_per_session': round(total_memories/max(len(sessions[:10]),1), 1)
    }


def test_shared_memory(agent_name: str):
    """测试 2: 共享记忆 (MEMORY.md)"""
    print("\n" + "="*60)
    print("📊 测试 2: 共享记忆 (Shared Memory)")
    print("="*60)
    
    memory_md = workspace / 'MEMORY.md'
    
    if memory_md.exists():
        content = memory_md.read_text(encoding='utf-8')
        lines = content.split('\n')
        chars = len(content)
        
        # 统计章节
        sections = [l for l in lines if l.startswith('## ')]
        
        print(f"✅ MEMORY.md 存在")
        print(f"✅ 行数：{len(lines)}")
        print(f"✅ 字符数：{chars}")
        print(f"✅ 章节数：{len(sections)}")
        
        return {
            'type': 'shared_memory',
            'exists': True,
            'lines': len(lines),
            'characters': chars,
            'sections': len(sections)
        }
    else:
        print(f"❌ MEMORY.md 不存在")
        return {
            'type': 'shared_memory',
            'exists': False
        }


def test_daily_memories(agent_name: str):
    """测试 3: 每日记忆文件"""
    print("\n" + "="*60)
    print("📊 测试 3: 每日记忆 (Daily Memories)")
    print("="*60)
    
    memory_dir = workspace / 'memory'
    
    if not memory_dir.exists():
        print(f"❌ memory 目录不存在")
        return {
            'type': 'daily_memories',
            'exists': False
        }
    
    # 统计 MD 文件
    md_files = list(memory_dir.glob('*.md'))
    total_chars = sum(f.stat().st_size for f in md_files)
    
    # 按月份分组
    by_month = {}
    for f in md_files:
        month = f.stem[:7]  # YYYY-MM
        by_month[month] = by_month.get(month, 0) + 1
    
    print(f"✅ memory 目录存在")
    print(f"✅ 记忆文件数：{len(md_files)}")
    print(f"✅ 总字符数：{total_chars:,}")
    print(f"✅ 月份数：{len(by_month)}")
    
    if by_month:
        latest_month = max(by_month.keys())
        print(f"✅ 最新月份：{latest_month} ({by_month[latest_month]} 个文件)")
    
    return {
        'type': 'daily_memories',
        'exists': True,
        'file_count': len(md_files),
        'total_characters': total_chars,
        'months_covered': len(by_month),
        'latest_month': max(by_month.keys()) if by_month else None
    }


def test_knowledge_graph(agent_name: str):
    """测试 4: 知识图谱"""
    print("\n" + "="*60)
    print("📊 测试 4: 知识图谱 (Knowledge Graph)")
    print("="*60)
    
    kg_file = workspace / 'memory' / 'knowledge_graph.json'
    
    if kg_file.exists():
        with open(kg_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        entities = data.get('entities', {})
        relations = data.get('relations', [])
        
        print(f"✅ knowledge_graph.json 存在")
        print(f"✅ 实体数：{len(entities)}")
        print(f"✅ 关系数：{len(relations)}")
        
        # 实体类型统计
        entity_types = {}
        for key, entity in entities.items():
            if isinstance(entity, dict):
                etype = entity.get('type', 'unknown')
            elif isinstance(entity, list) and len(entity) > 0:
                etype = entity[0] if isinstance(entity[0], str) else 'unknown'
            else:
                etype = 'unknown'
            entity_types[etype] = entity_types.get(etype, 0) + 1
        
        if entity_types:
            print(f"✅ 实体类型分布:")
            for etype, count in sorted(entity_types.items(), key=lambda x: -x[1])[:5]:
                print(f"   - {etype}: {count}")
        
        return {
            'type': 'knowledge_graph',
            'exists': True,
            'entities': len(entities),
            'relations': len(relations),
            'entity_types': entity_types
        }
    else:
        print(f"❌ knowledge_graph.json 不存在")
        return {
            'type': 'knowledge_graph',
            'exists': False
        }


def test_evolution_events(agent_name: str):
    """测试 5: 进化事件"""
    print("\n" + "="*60)
    print("📊 测试 5: 进化事件 (Evolution Events)")
    print("="*60)
    
    evolution_dir = workspace / 'data' / agent_name / 'evolution_events'
    
    if evolution_dir.exists():
        event_files = list(evolution_dir.glob('*.json'))
        
        print(f"✅ evolution_events 目录存在")
        print(f"✅ 事件文件数：{len(event_files)}")
        
        # 读取最新事件
        if event_files:
            latest = max(event_files, key=lambda f: f.stat().st_mtime)
            with open(latest, 'r', encoding='utf-8') as f:
                event = json.load(f)
            
            event_type = event.get('event_type', 'unknown')
            print(f"✅ 最新事件类型：{event_type}")
            print(f"✅ 最新事件：{latest.name}")
        
        return {
            'type': 'evolution_events',
            'exists': True,
            'event_count': len(event_files),
            'latest_event_type': event_type if event_files else None
        }
    else:
        print(f"❌ evolution_events 目录不存在")
        return {
            'type': 'evolution_events',
            'exists': False
        }


def run_comprehensive_test(agent_name: str = 'demo51-agent'):
    """运行完整测试套件"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║  evo-agents 综合基准测试                                ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"\n📦 Agent: {agent_name}")
    print(f"📁 Workspace: {workspace}")
    print(f"🕒 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # 运行所有测试
    results.append(test_session_memories(agent_name))
    results.append(test_shared_memory(agent_name))
    results.append(test_daily_memories(agent_name))
    results.append(test_knowledge_graph(agent_name))
    results.append(test_evolution_events(agent_name))
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    
    summary = {}
    for r in results:
        summary[r['type']] = r.get('exists', r.get('total_sessions', 0))
    
    print(f"\n记忆系统覆盖:")
    for test_type, exists in summary.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {test_type}")
    
    # 输出 JSON 报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'agent': agent_name,
        'workspace': str(workspace),
        'results': results
    }
    
    # 保存报告
    report_file = workspace / 'benchmarks' / f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 详细报告已保存到：{report_file}")
    
    return report


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='综合基准测试')
    parser.add_argument('--agent', type=str, default='demo51-agent', help='Agent 名称')
    
    args = parser.parse_args()
    
    run_comprehensive_test(args.agent)
