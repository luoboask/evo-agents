#!/usr/bin/env python3
"""
集成混合记忆系统 - Integrated Hybrid Memory
完全替换现有 memory_search，提供三层混合检索
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 添加 libs 到路径
from collections import deque


# 缓存配置
MAX_CACHE_SIZE = 10000  # 最多 10000 条记录
MAX_CACHE_MB = 100      # 最多 100MB

class IntegratedHybridMemory:
    """
    集成混合记忆系统
    - 自动记录每次重要交互
    - 三层检索：工作记忆 + 向量记忆 + 知识图谱
    - 智能重要性评估
    """
    
    def __init__(self):
        self.workspace = Path(__file__).parent.parent.parent
        self.memory_dir = self.workspace / "memory"
        
        # 三层记忆
        self.working_memory = deque(maxlen=50)  # 增加到50条
        self.vector_cache = {}
        
        # 知识图谱
        self.kg_file = self.memory_dir / "knowledge_graph.json"
        self.knowledge_graph = self._load_kg()
        
        # Phase 4: 统一索引
        from unified_index import UnifiedMemoryIndex
        self.unified_index = UnifiedMemoryIndex(self.workspace)
        
        # 加载今日工作记忆
        self._load_today_working_memory()
    
    # ═══════════════════════════════════════════════════════════════
    # 核心：自动记录和检索
    # ═══════════════════════════════════════════════════════════════
    
    def record_interaction(self, role, content, metadata=None):
        """
        记录交互到记忆系统
        
        Args:
            role: 'user' 或 'assistant'
            content: 内容
            metadata: 额外信息
        """
        # 评估重要性
        importance = self._assess_importance(content, role)
        
        # 构建记忆条目
        entry = {
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        }
        
        # L1: 工作记忆（所有交互）
        self.working_memory.append(entry)
        self._save_working_memory()
        
        # L2: 向量记忆（中等到重要）
        if importance in ["medium", "high", "critical"]:
            self._add_to_vector(entry)
        
        # L3: 知识图谱（关键信息）
        if importance == "critical":
            self._extract_to_kg(entry)
        
        return entry
    
    def _assess_importance(self, content, role):
        """智能评估重要性"""
        content_lower = content.lower()
        
        # Critical: 规则、决策、重要事实
        critical_patterns = [
            "规则", "必须", "禁止", "决定", "重要", "密码", "密钥",
            "rule", "must", "never", "decision", "important", "password"
        ]
        for pattern in critical_patterns:
            if pattern in content_lower:
                return "critical"
        
        # High: 偏好、习惯、技能
        high_patterns = [
            "喜欢", "偏好", "习惯", "技能", "创建", "完成",
            "like", "prefer", "habit", "skill", "created", "completed"
        ]
        for pattern in high_patterns:
            if pattern in content_lower:
                return "high"
        
        # Medium: 一般信息
        if len(content) > 50 or role == "assistant":
            return "medium"
        
        # Low: 简短对话
        return "low"
    
    def search(self, query, context="medium", top_k=5):
        """
        混合检索记忆
        
        Args:
            query: 查询内容
            context: small/medium/large
            top_k: 返回数量
        """
        results = []
        
        # L1: 工作记忆（总是搜索）
        working_results = self._search_working(query, top_k)
        results.extend([{**r, "layer": "working"} for r in working_results])
        
        # L2: 向量记忆
        if context in ["medium", "large"]:
            vector_results = self._search_vector(query, top_k)
            results.extend(vector_results)
        
        # L3: 知识图谱
        if context == "large":
            kg_results = self._search_kg(query, top_k)
            results.extend(kg_results)
        
        # 去重和排序
        seen = set()
        unique_results = []
        for r in results:
            key = r.get("content", "")[:100]
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        # 按分数排序
        unique_results.sort(key=lambda x: -x.get("score", 0))
        return unique_results[:top_k]
    
    # ═══════════════════════════════════════════════════════════════
    # L1: 工作记忆实现
    # ═══════════════════════════════════════════════════════════════
    
    def _load_today_working_memory(self):
        """加载今天的工作记忆"""
        today = datetime.now().strftime('%Y-%m-%d')
        working_file = self.memory_dir / f"working_memory_{today}.jsonl"
        
        if working_file.exists():
            with open(working_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.working_memory.append(json.loads(line))
    
    def _save_working_memory(self):
        """保存工作记忆"""
        today = datetime.now().strftime('%Y-%m-%d')
        working_file = self.memory_dir / f"working_memory_{today}.jsonl"
        
        with open(working_file, 'w') as f:
            for entry in self.working_memory:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def _search_working(self, query, top_k=5):
        """搜索工作记忆"""
        results = []
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        for entry in reversed(self.working_memory):
            content = entry.get("content", "").lower()
            content_words = set(content.split())
            
            # 计算重叠度
            overlap = len(query_words & content_words)
            if overlap > 0:
                score = overlap / len(query_words)
                results.append({
                    **entry,
                    "score": score
                })
        
        results.sort(key=lambda x: -x["score"])
        return results[:top_k]
    
    # ═══════════════════════════════════════════════════════════════
    # L2: 向量记忆实现（使用 Ollama）
    # ═══════════════════════════════════════════════════════════════
    
    def _get_embedding(self, text):
        """使用 Ollama 生成嵌入"""
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/embeddings",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps({"model": "nomic-embed-text", "prompt": text[:500]})],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("embedding", [])
        except Exception as e:
            print(f"Embedding error: {e}", file=sys.stderr)
        return []
    
    def _cosine_similarity(self, a, b):
        """计算余弦相似度"""
        if not a or not b:
            return 0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot / (norm_a * norm_b)
    
    def _add_to_vector(self, entry):
        """添加到向量记忆"""
        content = entry.get("content", "")
        embedding = self._get_embedding(content)
        
        if embedding:
            doc_id = f"vec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.vector_cache)}"
            self.vector_cache[doc_id] = {
                "entry": entry,
                "embedding": embedding
            }
        
    def _search_vector(self, query, top_k=5):
        """搜索向量记忆"""
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return []
                
        results = []
        for doc_id, doc in self.vector_cache.items():
            similarity = self._cosine_similarity(query_embedding, doc["embedding"])
            if similarity > 0.6:  # 阈值
                results.append({
                    **doc["entry"],
                    "score": similarity,
                    "layer": "vector"
                })
        
        results.sort(key=lambda x: -x["score"])
        return results[:top_k]
    


    def _index_existing_memories(self):
        """索引已有记忆文件（Phase 2: 使用统一索引）"""
        if hasattr(self, 'unified_index'):
            count = self.unified_index.index_all()
            if count > 0:
                print(f"✅ 统一索引 {count} 条记忆")
        else:
            # 回退到旧方法
            indexed_files = set()
            for entry in self.vector_cache:
                if isinstance(entry, dict) and 'metadata' in entry:
                    indexed_files.add(entry['metadata'].get('source', ''))
            
            count = 0
            for md_file in self.memory_dir.glob('*.md'):
                if str(md_file) not in indexed_files:
                    try:
                        content = md_file.read_text(encoding='utf-8')
                        for line in content.split('\n'):
                            if line.startswith('- [') and ']' in line:
                                start = line.find(']') + 1
                                if start > 0 and line[start:].strip():
                                    entry = {
                                        'content': line[start:].strip(),
                                        'metadata': {'source': str(md_file), 'type': 'file'}
                                    }
                                    self._add_to_vector(entry)
                                    count += 1
                    except Exception as e:
                        pass
            
            if count > 0:
                        print(f"✅ 自动索引 {count} 条已有记忆")
    
    # ═══════════════════════════════════════════════════════════════
    # L3: 知识图谱实现
    # ═══════════════════════════════════════════════════════════════
    
    def _load_kg(self):
        """加载知识图谱"""
        if self.kg_file.exists():
            with open(self.kg_file, 'r') as f:
                return json.load(f)
        return {"entities": {}, "relations": []}
    
    def _extract_to_kg(self, entry):
        """提取关键信息到知识图谱（简化版）"""
        content = entry.get("content", "")
        # 这里可以添加实体提取逻辑
        pass
    
    def _search_kg(self, query, top_k=5):
        """搜索知识图谱"""
        results = []
        query_lower = query.lower()
        
        for entity_id, entity in self.knowledge_graph.get("entities", {}).items():
            name = entity.get("name", "").lower()
            if query_lower in name or name in query_lower:
                results.append({
                    "content": entity.get("name"),
                    "type": entity.get("type"),
                    "score": 0.9,
                    "layer": "knowledge_graph"
                })
        
        results.sort(key=lambda x: -x["score"])
        return results[:top_k]
    
    # ═══════════════════════════════════════════════════════════════
    # 统计和导出
    # ═══════════════════════════════════════════════════════════════
    
    def get_stats(self):
        """获取统计信息"""
        return {
            "working_memory": len(self.working_memory),
            "vector_memory": len(self.vector_cache),
            "kg_entities": len(self.knowledge_graph.get("entities", {})),
            "kg_relations": len(self.knowledge_graph.get("relations", []))
        }
    
    def print_summary(self):
        """打印记忆摘要"""
        stats = self.get_stats()
        
        print("\n" + "=" * 60)
        print("🧠 混合记忆系统状态")
        print("=" * 60)
        print(f"\nL1 - 工作记忆: {stats['working_memory']} 条")
        print(f"L2 - 向量记忆: {stats['vector_memory']} 条")
        print(f"L3 - 知识图谱: {stats['kg_entities']} 实体, {stats['kg_relations']} 关系")
        print("\n" + "=" * 60)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='集成混合记忆系统')
    parser.add_argument('query', nargs='?', help='搜索查询')
    parser.add_argument('--record', type=str, help='记录内容')
    parser.add_argument('--role', default='user', help='角色 (user/assistant)')
    parser.add_argument('--context', default='medium', help='上下文大小 (small/medium/large)')
    parser.add_argument('--stats', action='store_true', help='显示统计')
    
    args = parser.parse_args()
    
    memory = IntegratedHybridMemory()
    
    if args.stats:
        memory.print_summary()
    elif args.record:
        entry = memory.record_interaction(args.role, args.record)
        print(f"✅ 已记录 ({entry['importance']}): {args.record[:50]}...")
    elif args.query:
        print(f"🔍 搜索: {args.query}\n")
        results = memory.search(args.query, context=args.context)
        
        if not results:
            print("未找到相关记忆")
        else:
            for i, r in enumerate(results, 1):
                content = r.get("content", "N/A")
                layer = r.get("layer", "unknown")
                score = r.get("score", 0)
                role = r.get("role", "")
                print(f"{i}. [{layer}] [{role}] {content[:60]}...")
                print(f"   相关度: {score:.2f}")
                print()
    else:
        memory.print_summary()


if __name__ == '__main__':
    main()
