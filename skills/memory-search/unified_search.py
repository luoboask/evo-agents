#!/usr/bin/env python3
"""
统一记忆搜索 - Unified Memory Search

整合 4 种查询方式：
1. 会话记忆搜索
2. 语义搜索
3. 共享记忆搜索（分层）
4. 知识图谱搜索
"""

import sys
import argparse
from pathlib import Path

workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

from memory_hub import MemoryHub


class UnifiedMemorySearch:
    """统一记忆搜索"""
    
    def __init__(self, agent_name='claude-code-agent'):
        self.agent_name = agent_name
        self.hub = MemoryHub(agent_name)
    
    def search_session(self, query='', top_k=5):
        """搜索会话记忆"""
        return self.hub.get_current_session_memories(top_k=top_k)
    
    def search_shared(self, query, top_k=5, hierarchical=True):
        """搜索共享记忆（分层）"""
        return self.hub.search(query, top_k=top_k, hierarchical=hierarchical)
    
    def search_semantic(self, query, top_k=5):
        """语义搜索"""
        return self.hub.search(query, top_k=top_k, semantic=True)
    
    def search_kg(self, query, top_k=5):
        """知识图谱搜索"""
        return []  # TODO: 实现知识图谱搜索
    
    def search(self, query, top_k=10, use_session=True, use_semantic=False, 
               use_shared=True, use_kg=False, hierarchical=True):
        """统一搜索"""
        all_results = []
        search_modes = []
        
        # 1. 会话记忆查询（最近的对话上下文，最相关）
        if use_session:
            results = self.search_session(query, top_k=top_k)
            for r in results:
                r['source'] = 'session_memory'
                r['weight'] = 1.5
            all_results.extend(results)
            search_modes.append('session')
        
        # 2. 语义搜索（基于共享记忆的向量搜索）
        if use_semantic:
            results = self.search_semantic(query, top_k=top_k)
            for r in results:
                r['source'] = 'semantic'
                r['weight'] = 1.4
            all_results.extend(results)
            search_modes.append('semantic')
        
        # 3. 共享记忆查询（分层搜索：月→周→日→全量）
        if use_shared:
            results = self.search_shared(query, top_k=top_k, hierarchical=hierarchical)
            for r in results:
                r['source'] = 'shared_memory'
                r['weight'] = 1.2
            all_results.extend(results)
            search_modes.append('shared')
        
        # 4. 知识图谱查询（实体关系增强）
        if use_kg:
            results = self.search_kg(query, top_k=top_k)
            for r in results:
                r['source'] = 'knowledge_graph'
                r['weight'] = 1.3
            all_results.extend(results)
            search_modes.append('kg')
        
        # 合并去重
        seen = set()
        unique = []
        for r in sorted(all_results, key=lambda x: x.get('weight', 0), reverse=True):
            key = r.get('content', '')[:100]
            if key not in seen:
                seen.add(key)
                unique.append(r)
        
        # 输出搜索模式
        if len(search_modes) > 1:
            print(f"✅ 搜索顺序：{' → '.join(search_modes)}")
        
        return unique[:top_k]


def main():
    parser = argparse.ArgumentParser(description='统一记忆搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--top-k', '-k', type=int, default=10)
    parser.add_argument('--agent', type=str, default='claude-code-agent')
    parser.add_argument('--no-session', action='store_true')
    parser.add_argument('--no-shared', action='store_true')
    parser.add_argument('--semantic', action='store_true')
    parser.add_argument('--kg', action='store_true')
    args = parser.parse_args()
    
    search = UnifiedMemorySearch(agent_name=args.agent)
    results = search.search(
        args.query,
        top_k=args.top_k,
        use_session=not args.no_session,
        use_shared=not args.no_shared,
        use_semantic=args.semantic,
        use_kg=args.kg
    )
    
    print(f"\n🔍 搜索：{args.query} (找到 {len(results)} 条)\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['source']}] {r['content'][:100]}...")


if __name__ == '__main__':
    main()
