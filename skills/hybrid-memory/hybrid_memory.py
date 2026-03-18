#!/usr/bin/env python3
"""
混合记忆系统 - Hybrid Memory System
结合向量数据库 + 知识图谱 + 分层摘要的优势
"""

import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
import subprocess


class HybridMemory:
    """
    三层混合记忆系统
    - L1: 工作记忆 (当前会话)
    - L2: 向量记忆 (语义检索)
    - L3: 图谱记忆 (结构化关系)
    """
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace-ai-baby")
        self.memory_dir = self.workspace / "memory"
        self.vector_dir = self.memory_dir / "vector_db"
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        
        # L1: 工作记忆 (当前会话，最近20条)
        self.working_memory = deque(maxlen=20)
        
        # L2: 向量记忆 (使用 Ollama 生成嵌入)
        self.vector_cache = {}  # 简单的内存缓存
        self._load_vector_cache()
        
        # L3: 知识图谱 (已有)
        self.kg_file = self.memory_dir / "knowledge_graph.json"
        self.knowledge_graph = self._load_kg()
    
    # ═══════════════════════════════════════════════════════════════
    # L1: 工作记忆 (Working Memory)
    # ═══════════════════════════════════════════════════════════════
    
    def add_to_working(self, content, metadata=None):
        """添加到工作记忆"""
        entry = {
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        self.working_memory.append(entry)
    
    def search_working(self, query, top_k=5):
        """搜索工作记忆 (简单关键词匹配)"""
        results = []
        query_lower = query.lower()
        
        for entry in reversed(self.working_memory):
            content = entry["content"].lower()
            # 简单相关性评分
            score = 0
            for word in query_lower.split():
                if word in content:
                    score += 1
            
            if score > 0:
                results.append({
                    **entry,
                    "score": score,
                    "layer": "working"
                })
        
        # 按分数排序
        results.sort(key=lambda x: -x["score"])
        return results[:top_k]
    
    # ═══════════════════════════════════════════════════════════════
    # L2: 向量记忆 (Vector Memory) - 使用 Ollama
    # ═══════════════════════════════════════════════════════════════
    
    def _get_embedding(self, text):
        """使用 Ollama 生成嵌入"""
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/embeddings",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps({"model": "nomic-embed-text", "prompt": text})],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("embedding", [])
        except:
            pass
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
    
    def add_to_vector(self, content, metadata=None):
        """添加到向量记忆"""
        embedding = self._get_embedding(content)
        if embedding:
            doc_id = f"vec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.vector_cache)}"
            self.vector_cache[doc_id] = {
                "content": content,
                "embedding": embedding,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }
            self._save_vector_cache()
            return doc_id
        return None
    
    def search_vector(self, query, top_k=5):
        """语义搜索向量记忆"""
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return []
        
        results = []
        for doc_id, doc in self.vector_cache.items():
            similarity = self._cosine_similarity(query_embedding, doc["embedding"])
            if similarity > 0.5:  # 阈值
                results.append({
                    "id": doc_id,
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "score": similarity,
                    "layer": "vector"
                })
        
        results.sort(key=lambda x: -x["score"])
        return results[:top_k]
    
    def _load_vector_cache(self):
        """加载向量缓存"""
        cache_file = self.vector_dir / "cache.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                self.vector_cache = json.load(f)
    
    def _save_vector_cache(self):
        """保存向量缓存"""
        cache_file = self.vector_dir / "cache.json"
        with open(cache_file, 'w') as f:
            json.dump(self.vector_cache, f, ensure_ascii=False, indent=2)
    
    # ═══════════════════════════════════════════════════════════════
    # L3: 知识图谱 (Knowledge Graph)
    # ═══════════════════════════════════════════════════════════════
    
    def _load_kg(self):
        """加载知识图谱"""
        if self.kg_file.exists():
            with open(self.kg_file, 'r') as f:
                return json.load(f)
        return {"entities": {}, "relations": []}
    
    def search_kg(self, query, top_k=5):
        """搜索知识图谱"""
        results = []
        query_lower = query.lower()
        
        # 搜索实体
        for entity_id, entity in self.knowledge_graph.get("entities", {}).items():
            name = entity.get("name", "").lower()
            if query_lower in name or name in query_lower:
                results.append({
                    "id": entity_id,
                    "name": entity["name"],
                    "type": entity["type"],
                    "score": 0.9,
                    "layer": "knowledge_graph"
                })
        
        # 搜索关系
        for rel in self.knowledge_graph.get("relations", []):
            if query_lower in rel.get("reason", "").lower():
                results.append({
                    "relation": rel["relation"],
                    "source": rel["source"],
                    "target": rel["target"],
                    "score": 0.7,
                    "layer": "knowledge_graph"
                })
        
        results.sort(key=lambda x: -x["score"])
        return results[:top_k]
    
    # ═══════════════════════════════════════════════════════════════
    # 混合检索 (Hybrid Search)
    # ═══════════════════════════════════════════════════════════════
    
    def remember(self, content, importance="medium", metadata=None):
        """
        记忆内容到合适的层级
        
        importance: low/medium/high/critical
        """
        # 总是添加到工作记忆
        self.add_to_working(content, metadata)
        
        # 中等到重要内容添加到向量记忆
        if importance in ["medium", "high", "critical"]:
            self.add_to_vector(content, metadata)
        
        # 关键内容同时更新知识图谱（简化版）
        if importance == "critical":
            # 这里可以添加实体提取逻辑
            pass
    
    def recall(self, query, context="medium"):
        """
        混合检索记忆
        
        context: small/medium/large
        """
        all_results = []
        
        # L1: 工作记忆 (总是搜索)
        working_results = self.search_working(query, top_k=5)
        all_results.extend(working_results)
        
        # L2: 向量记忆 (medium 和 large)
        if context in ["medium", "large"]:
            vector_results = self.search_vector(query, top_k=5)
            all_results.extend(vector_results)
        
        # L3: 知识图谱 (large)
        if context == "large":
            kg_results = self.search_kg(query, top_k=3)
            all_results.extend(kg_results)
        
        # 去重和排序
        seen = set()
        unique_results = []
        for r in all_results:
            key = r.get("content", r.get("name", str(r)))
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        unique_results.sort(key=lambda x: -x.get("score", 0))
        return unique_results[:10]
    
    def get_stats(self):
        """获取记忆统计"""
        return {
            "working_memory": len(self.working_memory),
            "vector_memory": len(self.vector_cache),
            "knowledge_graph_entities": len(self.knowledge_graph.get("entities", {})),
            "knowledge_graph_relations": len(self.knowledge_graph.get("relations", []))
        }


def main():
    """测试混合记忆"""
    print("🧠 混合记忆系统测试")
    print("=" * 60)
    
    memory = HybridMemory()
    
    # 添加测试记忆
    print("\n💾 添加记忆...")
    memory.remember("用户喜欢简洁的回答", importance="high", metadata={"type": "preference"})
    memory.remember("用户要求删除操作必须授权", importance="critical", metadata={"type": "rule"})
    memory.remember("今天创建了 websearch 技能", importance="medium", metadata={"type": "event"})
    memory.remember("用户名叫 openclaw-tui", importance="high", metadata={"type": "user_info"})
    
    # 测试检索
    print("\n🔍 测试检索...")
    
    queries = [
        "用户偏好什么？",
        "删除操作规则",
        "今天做了什么",
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        results = memory.recall(query, context="medium")
        for i, r in enumerate(results[:3], 1):
            content = r.get("content", r.get("name", "N/A"))
            layer = r.get("layer", "unknown")
            score = r.get("score", 0)
            print(f"  {i}. [{layer}] {content[:50]}... (score: {score:.2f})")
    
    # 统计
    print("\n📊 记忆统计:")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    print("\n✅ 测试完成!")


if __name__ == '__main__':
    main()
