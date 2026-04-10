#!/usr/bin/env python3
"""
Unified Memory Search - 统一记忆查询入口

整合 4 种查询方式：
1. shared_memory_search - 共享记忆（关键词）
2. session_memory_search - 会话记忆
3. semantic_search - 语义搜索（向量）
4. search_with_kg - 知识图谱

流程：
1. 并行执行 4 种查询
2. 合并和去重结果
3. 加权排序
4. 可选：调用大模型生成答案
"""

import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 添加 libs 到路径
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

# 导入 RAG 评估
from rag_eval.recorder import start_recording, finish_recording


class UnifiedMemorySearch:
    """统一记忆搜索"""
    
    def __init__(self, agent_name=None):
        self.agent_name = agent_name
        self.workspace_root = workspace_root
        
        # 加载 RAG 配置
        self.rag_config = self._load_rag_config()
        
        # 初始化查询模块
        from memory_hub import MemoryHub
        self.hub = MemoryHub(agent_name)
    
    def _load_rag_config(self):
        """加载 RAG 配置"""
        config_path = self.workspace_root / 'libs' / 'rag_eval' / 'config.json'
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {'current_config': {'top_k': 5}}
    
    def search_shared(self, query, top_k):
        """1. 共享记忆查询"""
        return self.hub.search(query, top_k=top_k)
    
    def search_session(self, query, top_k):
        """2. 会话记忆查询"""
        return self.hub.get_current_session_memories(top_k=top_k)
    
    def search_semantic(self, query, top_k, threshold=0.7):
        """3. 语义搜索"""
        # 简化实现：直接使用 memory_hub 的语义搜索
        # 实际应该调用 semantic_search.py 的逻辑
        return self.hub.search(query, top_k=top_k)  # 临时使用关键词搜索
    
    def search_kg(self, query, top_k):
        """4. 知识图谱搜索"""
        # 加载知识图谱
        kg_path = self.workspace_root / 'memory' / 'knowledge_graph.json'
        if not kg_path.exists():
            return []
        
        with open(kg_path) as f:
            kg = json.load(f)
        
        # 简单的实体匹配
        results = []
        for entity_id, entity in kg.get('entities', {}).items():
            if query.lower() in entity.get('name', '').lower():
                results.append({
                    'source': 'knowledge_graph',
                    'content': f"{entity['type']}: {entity['name']} (提及 {entity.get('mentions', 0)} 次)",
                    'score': 1.0,
                    'entity': entity
                })
        
        return results[:top_k]
    
    def search(self, 
               query: str,
               top_k: int = None,
               use_shared: bool = True,
               use_session: bool = True,
               use_semantic: bool = False,  # 语义搜索较慢，默认关闭
               use_kg: bool = True,
               merge_results: bool = True,
               record_eval: bool = True) -> List[Dict]:
        """
        统一搜索接口
        
        Args:
            query: 搜索关键词
            top_k: 返回数量（默认使用 RAG 配置）
            use_shared: 是否查询共享记忆
            use_session: 是否查询会话记忆
            use_semantic: 是否使用语义搜索
            use_kg: 是否查询知识图谱
            merge_results: 是否合并结果
            record_eval: 是否记录评估
        
        Returns:
            搜索结果列表
        """
        start_time = time.time()
        
        # 使用 RAG 配置的 top_k
        if top_k is None:
            top_k = self.rag_config.get('current_config', {}).get('top_k', 5)
        
        all_results = []
        
        # 1. 共享记忆查询
        if use_shared:
            try:
                results = self.search_shared(query, top_k=top_k)
                for r in results:
                    r['source'] = 'shared_memory'
                    r['weight'] = 1.0
                all_results.extend(results)
            except Exception as e:
                print(f"⚠️  共享记忆查询失败：{e}")
        
        # 2. 会话记忆查询
        if use_session:
            try:
                results = self.search_session(query, top_k=top_k)
                for r in results:
                    r['source'] = 'session_memory'
                    r['weight'] = 1.2  # 会话记忆权重稍高
                all_results.extend(results)
            except Exception as e:
                print(f"⚠️  会话记忆查询失败：{e}")
        
        # 3. 语义搜索（可选，较慢）
        if use_semantic:
            try:
                results = self.search_semantic(query, top_k=top_k)
                for r in results:
                    r['source'] = 'semantic'
                    r['weight'] = 1.5  # 语义搜索权重最高
                all_results.extend(results)
            except Exception as e:
                print(f"⚠️  语义搜索失败：{e}")
        
        # 4. 知识图谱查询
        if use_kg:
            try:
                results = self.search_kg(query, top_k=top_k)
                for r in results:
                    r['source'] = 'knowledge_graph'
                    r['weight'] = 1.3  # 知识图谱权重较高
                all_results.extend(results)
            except Exception as e:
                print(f"⚠️  知识图谱查询失败：{e}")
        
        # 合并和去重
        if merge_results:
            all_results = self._merge_results(all_results, top_k)
        
        # 记录评估
        if record_eval:
            finish_recording(
                retrieved_count=len(all_results),
                top_k=top_k,
                similarity_score=all_results[0].get('score', 0) if all_results else 0
            )
        
        return all_results
    
    def _merge_results(self, results: List[Dict], top_k: int) -> List[Dict]:
        """合并和去重结果"""
        # 按分数和权重排序
        results.sort(key=lambda x: x.get('score', 0) * x.get('weight', 1.0), reverse=True)
        
        # 去重（基于内容）
        seen = set()
        unique_results = []
        for r in results:
            content_hash = hash(r.get('content', '')[:100])
            if content_hash not in seen:
                seen.add(content_hash)
                unique_results.append(r)
        
        return unique_results[:top_k]
    
    def search_and_generate(self, 
                            query: str,
                            top_k: int = None,
                            model: str = 'qwen',
                            **kwargs) -> Dict:
        """
        搜索并生成答案
        
        Args:
            query: 用户问题
            top_k: 检索数量
            model: 使用的模型
        
        Returns:
            {
                'query': str,
                'retrieved': List[Dict],  # 检索结果
                'answer': str,            # 生成的答案
                'sources': List[str],     # 来源
                'latency_ms': float
            }
        """
        start_time = time.time()
        
        # 1. 检索相关记忆
        retrieved = self.search(query, top_k=top_k, **kwargs)
        
        # 2. 构建上下文
        context = self._build_context(retrieved)
        
        # 3. 调用大模型生成答案
        answer = self._generate_answer(query, context, model)
        
        # 4. 提取来源
        sources = list(set(r['source'] for r in retrieved))
        
        latency_ms = (time.time() - start_time) * 1000
        
        return {
            'query': query,
            'retrieved': retrieved,
            'answer': answer,
            'sources': sources,
            'latency_ms': latency_ms
        }
    
    def _build_context(self, results: List[Dict]) -> str:
        """构建上下文"""
        context_parts = []
        for i, r in enumerate(results, 1):
            source = r.get('source', 'unknown')
            content = r.get('content', '')[:500]
            context_parts.append(f"[{source}] {content}")
        
        return "\n\n".join(context_parts)
    
    def _generate_answer(self, query: str, context: str, model: str) -> str:
        """
        调用大模型生成答案
        
        简化实现：直接返回上下文
        实际应该调用 LLM API
        """
        if not context:
            return "没有找到相关信息。"
        
        # 简化实现：返回检索结果
        return f"根据记忆系统，找到以下相关信息：\n\n{context}"


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='统一记忆搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--top-k', '-k', type=int, default=None, help='返回数量')
    parser.add_argument('--no-session', action='store_true', help='不查询会话记忆')
    parser.add_argument('--no-shared', action='store_true', help='不查询共享记忆')
    parser.add_argument('--semantic', action='store_true', help='使用语义搜索')
    parser.add_argument('--no-kg', action='store_true', help='不查询知识图谱')
    parser.add_argument('--generate', '-g', action='store_true', help='生成答案')
    parser.add_argument('--agent', type=str, default=None, help='Agent 名称')
    
    args = parser.parse_args()
    
    # 确定 Agent 名称
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
    
    # 初始化搜索
    search = UnifiedMemorySearch(agent_name=agent_name)
    
    if args.generate:
        # 搜索并生成答案
        result = search.search_and_generate(
            args.query,
            top_k=args.top_k,
            use_shared=not args.no_shared,
            use_session=not args.no_session,
            use_semantic=args.semantic,
            use_kg=not args.no_kg
        )
        
        print(f"🔍 查询：{result['query']}")
        print(f"⏱️  延迟：{result['latency_ms']:.2f}ms")
        print(f"📚 来源：{', '.join(result['sources'])}")
        print(f"\n💡 答案:\n{result['answer']}")
        print(f"\n📊 检索到 {len(result['retrieved'])} 条结果")
    else:
        # 只搜索
        results = search.search(
            args.query,
            top_k=args.top_k,
            use_shared=not args.no_shared,
            use_session=not args.no_session,
            use_semantic=args.semantic,
            use_kg=not args.no_kg
        )
        
        print(f"🔍 查询：{args.query} (找到 {len(results)} 条)\n")
        
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['source']}] {r['content'][:100]}...")


if __name__ == '__main__':
    main()
