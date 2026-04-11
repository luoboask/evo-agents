#!/usr/bin/env python3
"""Shared Memory Search - 共享记忆搜索（带评估记录）"""
import sys, argparse, time
from pathlib import Path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))
from memory_hub import MemoryHub
from rag_eval.recorder import finish_recording

class SharedMemorySearch:
    def __init__(self, agent_name=None):
        self.hub = MemoryHub(agent_name)
    
    def search(self, query, top_k=10, record_eval=True):
        """搜索共享记忆，自动记录评估数据"""
        start_time = time.time()
        results = self.hub.search(query, top_k=top_k)
        
        if record_eval:
            finish_recording(
                retrieved_count=len(results),
                similarity_score=results[0].get('score') if results else None,
                top_k=top_k
            )
        
        return results
    
    def stats(self):
        return self.hub.stats()

def main():
    parser = argparse.ArgumentParser(description='共享记忆搜索')
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--limit', '-n', type=int, default=10)
    parser.add_argument('--stats', action='store_true')
    parser.add_argument('--agent', type=str, default=None)
    args = parser.parse_args()
    
    agent_name = args.agent
    if not agent_name:
        config_file = workspace_root / '.install-config'
        if config_file.exists():
            for line in config_file.read_text().splitlines():
                if line.startswith('agent_name='):
                    agent_name = line.split('=')[1].strip()
                    break
    if not agent_name:
        print("❌ 请指定 --agent 参数")
        return
    
    search = SharedMemorySearch(agent_name=agent_name)
    if args.stats:
        stats = search.stats()
        print(f"📊 共享记忆：{stats.get('total', 0)} 条")
        return
    if args.query:
        results = search.search(args.query, top_k=args.limit)
        print(f"🔍 搜索：{args.query} ({len(results)} 条)")
        for r in results:
            print(f"  ID {r['id']:4} | {r['content'][:60]}...")

if __name__ == '__main__':
    main()
