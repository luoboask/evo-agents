#!/usr/bin/env python3
"""Session Memory Search - 会话记忆搜索（带评估记录）"""
import sys, argparse, time
from pathlib import Path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))
from memory_hub import MemoryHub
from rag_eval.recorder import finish_recording

class SessionMemorySearch:
    def __init__(self, agent_name=None):
        self.hub = MemoryHub(agent_name)
    
    def search_current(self, top_k=15, record_eval=True):
        """搜索当前会话记忆，自动记录评估数据"""
        results = self.hub.get_current_session_memories(top_k=top_k)
        
        if record_eval:
            finish_recording(
                retrieved_count=len(results),
                top_k=top_k
            )
        
        return results
    
    def search_session(self, session_id, top_k=50, record_eval=True):
        """搜索指定会话，自动记录评估数据"""
        if len(session_id) < 36:
            sessions = self.hub.get_all_sessions()
            matched = [s for s in sessions if s.startswith(session_id)]
            if matched:
                session_id = matched[0]
            else:
                return None, []
        
        memories = self.hub.get_session_memories(session_id=session_id, top_k=top_k)
        
        if record_eval:
            finish_recording(
                retrieved_count=len(memories),
                top_k=top_k
            )
        
        return session_id, memories
    
    def list_sessions(self):
        sessions = self.hub.get_all_sessions()
        return [(s, self.hub.get_session_stats(s).get('total', 0)) for s in sessions]

def main():
    parser = argparse.ArgumentParser(description='会话记忆搜索')
    parser.add_argument('--limit', '-n', type=int, default=15)
    parser.add_argument('--session', '-s', type=str)
    parser.add_argument('--list', '-l', action='store_true')
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
    
    search = SessionMemorySearch(agent_name=agent_name)
    if args.list:
        sessions = search.list_sessions()
        print(f"📋 会话 ({len(sessions)} 个)")
        for sid, cnt in sorted(sessions, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {sid[:8]}... : {cnt} 条")
        return
    if args.stats:
        sessions = search.list_sessions()
        total = sum(c for _, c in sessions)
        print(f"📊 会话：{len(sessions)} 个 | 记忆：{total} 条")
        return
    if args.session:
        sid, memories = search.search_session(args.session, top_k=args.limit)
        if sid:
            print(f"📋 会话 {sid[:8]}... ({len(memories)} 条)")
            for m in memories:
                print(f"  ID {m['id']:4} | {m['content'][:60]}...")
        return
    memories = search.search_current(top_k=args.limit)
    print(f"📌 当前会话 ({len(memories)} 条)")
    for m in memories:
        print(f"  ID {m['id']:4} | {m['content'][:60]}...")

if __name__ == '__main__':
    main()
