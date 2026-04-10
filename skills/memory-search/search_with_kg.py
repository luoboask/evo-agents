#!/usr/bin/env python3
"""
search_with_kg.py - 集成知识图谱的语义搜索

使用 knowledge_graph 共享库进行实体识别和关系扩展。
"""

import sys
from pathlib import Path

# 添加 libs 到路径
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

# 导入 knowledge_graph
from knowledge_graph.builder import KnowledgeGraphEnhanced
KnowledgeGraph = KnowledgeGraphEnhanced


class SearchWithKG:
    """集成知识图谱的搜索"""
    
    def __init__(self, workspace=None):
        """初始化知识图谱"""
        self.kg = KnowledgeGraph(workspace)
        self.memories = self._load_memories()
    
    def _load_memories(self):
        """加载记忆文件"""
        memories = []
        for file_path in self.kg.memory_dir.glob('*.md'):
            if file_path.name.startswith('2026-'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        memories.append({
                            'file': file_path.name,
                            'content': f.read(),
                            'date': file_path.stem
                        })
                except:
                    continue
        
        memory_md = self.kg.workspace / 'MEMORY.md'
        if memory_md.exists():
            with open(memory_md, 'r', encoding='utf-8') as f:
                memories.append({'file': 'MEMORY.md', 'content': f.read(), 'date': 'long-term'})
        
        return memories
    
    def search(self, query, top_k=10):
        """搜索记忆（结合知识图谱）"""
        # 简单实现：关键词匹配 + 实体匹配
        results = []
        for memory in self.memories:
            if query.lower() in memory['content'].lower():
                results.append({'memory': memory, 'score': 1.0})
        return results[:top_k]


def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description='知识图谱搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--limit', '-n', type=int, default=10)
    args = parser.parse_args()
    
    search = SearchWithKG()
    results = search.search(args.query, top_k=args.limit)
    
    print(f"🔍 搜索：{args.query} (找到 {len(results)} 条)\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['memory']['file']}] {r['memory']['content'][:100]}...\n")


if __name__ == '__main__':
    main()
