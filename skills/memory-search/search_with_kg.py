#!/usr/bin/env python3
"""
search_with_kg.py - 集成知识图谱的语义搜索（带评估记录）

使用 knowledge_graph 共享库进行实体识别和关系扩展。
"""

import sys, time
from pathlib import Path

# 添加 libs 到路径
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

# 导入 rag_eval (libs 下的通用库)
try:
    from rag_eval.recorder import finish_recording
except ImportError:
    def finish_recording(*args, **kwargs):
        pass  # 无 rag_eval 时静默跳过

# knowledge_graph 已移除（跨 skill 依赖）
KnowledgeGraph = None


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
    
    def search(self, query, top_k=10, record_eval=True):
        """搜索记忆（结合知识图谱），自动记录评估数据"""
        # 简单实现：关键词匹配 + 实体匹配
        results = []
        for memory in self.memories:
            if query.lower() in memory['content'].lower():
                results.append({'memory': memory, 'score': 1.0})
        
        if record_eval:
            finish_recording(
                retrieved_count=len(results),
                top_k=top_k
            )
        
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
