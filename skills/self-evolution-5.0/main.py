#!/usr/bin/env python3
"""
自进化系统统一入口

整合所有功能模块，提供命令行界面
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))


def cmd_status(args):
    """显示系统状态"""
    print("=" * 70)
    print("🚀 自进化系统 v5.0 - 状态")
    print("=" * 70)
    print(f"\n📅 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查数据库
    from pathlib import Path
    db_files = [
        'memory/memory_stream.db',
        'memory/knowledge_base.db',
        'skills/evolution-workbench/evolution.db'
    ]
    
    print("\n📊 数据库状态:")
    for db in db_files:
        full_path = Path('/Users/dhr/.openclaw/workspace-ai-baby') / db
        if full_path.exists():
            size_mb = full_path.stat().st_size / 1024 / 1024
            print(f"   ✅ {db} ({size_mb:.2f}MB)")
        else:
            print(f"   ❌ {db} (不存在)")
    
    # 显示统计
    try:
        from memory_stream import MemoryStream
        ms = MemoryStream()
        stats = ms.get_stats()
        print(f"\n🧠 记忆流:")
        print(f"   总记忆：{stats['total_memories']}条")
        print(f"   最近 24h: {stats['recent_24h']}条")
    except Exception as e:
        print(f"   ⚠️ 无法获取记忆流统计：{e}")
    
    try:
        from self_evolution_real import RealSelfEvolution
        evolution = RealSelfEvolution()
        summary = evolution.get_summary()
        print(f"\n📈 进化事件:")
        print(f"   总事件：{summary['total_events']}次")
        print(f"   类型数：{len(summary['by_type'])}种")
    except Exception as e:
        print(f"   ⚠️ 无法获取进化统计：{e}")
    
    print("\n" + "=" * 70)


def cmd_fractal(args):
    """运行分形思考引擎"""
    from fractal_thinking import FractalThinkingEngine
    
    print("=" * 70)
    print("🧠 分形思考引擎")
    print("=" * 70)
    
    engine = FractalThinkingEngine()
    results = engine.process_events(limit=args.limit)
    
    if args.verbose:
        print("\n📄 完整报告:")
        print(results['report'])


def cmd_nightly(args):
    """运行夜间进化循环"""
    from nightly_cycle import NightlyEvolutionCycle
    
    print("=" * 70)
    print("🌙 夜间进化循环")
    print("=" * 70)
    
    cycle = NightlyEvolutionCycle()
    results = cycle.run_full_cycle()
    
    print(f"\n✅ 循环完成")


def cmd_memory(args):
    """管理记忆流"""
    from memory_stream import MemoryStream
    
    ms = MemoryStream()
    
    if args.action == 'add':
        memory_id = ms.add_memory(
            content=args.content,
            memory_type=args.type or 'observation',
            importance=args.importance or 5.0,
            tags=args.tags.split(',') if args.tags else []
        )
        print(f"✅ 记忆已添加 (ID: {memory_id})")
    
    elif args.action == 'list':
        memories = ms.get_memories(
            memory_type=args.type,
            limit=args.limit
        )
        print(f"\n📝 记忆列表 ({len(memories)}条):")
        for mem in memories:
            print(f"   [{mem.memory_type}] {mem.content[:60]}... (重要性：{mem.importance})")
    
    elif args.action == 'stats':
        stats = ms.get_stats()
        print(f"\n📊 记忆统计:")
        print(f"   总记忆：{stats['total_memories']}")
        print(f"   最近 24h: {stats['recent_24h']}")
        for mtype, data in stats['by_type'].items():
            print(f"   - {mtype}: {data['count']}条 (平均重要性：{data['avg_importance']:.1f})")


def cmd_embedding(args):
    """测试 Embedding 模块"""
    from embedding import EmbeddingModel
    
    print("=" * 70)
    print("🧠 Embedding 模块测试")
    print("=" * 70)
    
    model = EmbeddingModel()
    print(f"\nOllama 可用：{'✅ 是' if model.ollama_available else '⚠️  否 (降级到本地算法)'}")
    
    if args.text1 and args.text2:
        sim = model.similarity(args.text1, args.text2)
        print(f"\n🔍 相似度：'{args.text1}' vs '{args.text2}' = {sim:.3f}")
    else:
        # 默认测试
        test_pairs = [
            ("修复 Bug", "修复了错误"),
            ("优化代码", "代码改进"),
        ]
        print("\n🔍 相似度测试:")
        for text1, text2 in test_pairs:
            sim = model.similarity(text1, text2)
            print(f"   '{text1}' vs '{text2}': {sim:.3f}")


def cmd_evolve(args):
    """记录进化事件"""
    from self_evolution_real import RealSelfEvolution
    
    evolution = RealSelfEvolution()
    
    event = evolution.record_evolution(
        event_type=args.type,
        description=args.description,
        lesson_learned=args.lesson or '',
        files_changed=args.files.split(',') if args.files else []
    )
    
    print(f"✅ 进化事件已记录 (ID: {event.get('id', 'N/A')})")


def check_ollama():
    """检查并自动启动 Ollama"""
    import subprocess
    import time
    
    # 检查是否运行
    try:
        result = subprocess.run(['pgrep', '-x', 'ollama'], capture_output=True)
        if result.returncode == 0:
            print("✅ Ollama 服务：运行中")
            return True
    except:
        pass
    
    # 尝试启动
    print("⚠️  Ollama 服务：未运行，自动启动中...")
    subprocess.Popen(['nohup', 'ollama', 'serve'], 
                     stdout=open('/tmp/ollama.log', 'w'),
                     stderr=subprocess.STDOUT)
    
    # 等待启动
    for i in range(10):
        time.sleep(1)
        try:
            import urllib.request
            urllib.request.urlopen('http://localhost:11434/api/tags', timeout=2)
            print("✅ Ollama 已启动")
            return True
        except:
            continue
    
    print("❌ Ollama 启动失败，请手动运行：ollama serve")
    return False


def main():
    # 自动检查 Ollama
    check_ollama()
    
    parser = argparse.ArgumentParser(
        description='自进化系统 v5.0 - 统一入口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 main.py status                    # 显示系统状态
  python3 main.py fractal --limit 10        # 运行分形思考
  python3 main.py nightly                   # 运行夜间循环
  python3 main.py memory list --limit 20    # 列出记忆
  python3 main.py embedding "修复 Bug" "修复错误"  # 测试相似度
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # status 命令
    status_parser = subparsers.add_parser('status', help='显示系统状态')
    status_parser.set_defaults(func=cmd_status)
    
    # fractal 命令
    fractal_parser = subparsers.add_parser('fractal', help='运行分形思考引擎')
    fractal_parser.add_argument('--limit', type=int, default=10, help='分析事件数量')
    fractal_parser.add_argument('--verbose', '-v', action='store_true', help='显示完整报告')
    fractal_parser.set_defaults(func=cmd_fractal)
    
    # nightly 命令
    nightly_parser = subparsers.add_parser('nightly', help='运行夜间进化循环')
    nightly_parser.set_defaults(func=cmd_nightly)
    
    # memory 命令
    memory_parser = subparsers.add_parser('memory', help='管理记忆流')
    memory_parser.add_argument('action', choices=['add', 'list', 'stats'], help='操作类型')
    memory_parser.add_argument('--content', type=str, help='记忆内容 (add 操作)')
    memory_parser.add_argument('--type', type=str, help='记忆类型 (observation/reflection/goal)')
    memory_parser.add_argument('--importance', type=float, default=5.0, help='重要性 1-10')
    memory_parser.add_argument('--tags', type=str, help='标签 (逗号分隔)')
    memory_parser.add_argument('--limit', type=int, default=20, help='返回数量')
    memory_parser.set_defaults(func=cmd_memory)
    
    # embedding 命令
    embedding_parser = subparsers.add_parser('embedding', help='测试 Embedding 模块')
    embedding_parser.add_argument('text1', nargs='?', type=str, help='文本 1')
    embedding_parser.add_argument('text2', nargs='?', type=str, help='文本 2')
    embedding_parser.set_defaults(func=cmd_embedding)
    
    # evolve 命令
    evolve_parser = subparsers.add_parser('evolve', help='记录进化事件')
    evolve_parser.add_argument('--type', type=str, required=True, help='事件类型')
    evolve_parser.add_argument('--description', type=str, required=True, help='事件描述')
    evolve_parser.add_argument('--lesson', type=str, help='经验教训')
    evolve_parser.add_argument('--files', type=str, help='修改的文件 (逗号分隔)')
    evolve_parser.set_defaults(func=cmd_evolve)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()
