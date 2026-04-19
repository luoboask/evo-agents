# -*- coding: utf-8 -*-
"""
知识图谱搜索增强器 - 使用图谱关系增强搜索

功能:
1. 搜索时扩展相关概念
2. 按图谱关系排序
3. 发现隐藏关联
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Set, Optional

sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))

from memory_hub import MemoryHub


class KnowledgeGraphSearchEnhancer:
    """知识图谱搜索增强器"""
    
    def __init__(self, agent_name: str = "default"):
        self.agent_name = agent_name
        self.hub = MemoryHub(agent_name=agent_name)
        self.kg_data = self._load_knowledge_graph()
        
        print(f"🕸️ 知识图谱搜索增强器已初始化")
        print(f"   Agent: {agent_name}")
        print(f"   图谱实体：{len(self.kg_data.get('entities', []))}")
    
    def _load_knowledge_graph(self) -> Dict:
        """加载知识图谱数据"""
        kg_path = Path(f"data/{self.agent_name}/knowledge/private/knowledge_graph.json")
        
        if kg_path.exists():
            try:
                with open(kg_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  加载知识图谱失败：{e}")
        
        # 返回空图谱
        return {'entities': [], 'relations': []}
    
    def enhance_search(self, 
                      query: str, 
                      original_results: List[Dict],
                      top_k: int = 5) -> List[Dict]:
        """
        增强搜索结果
        
        流程:
        1. 从 query 提取实体
        2. 查找图谱中的相关概念
        3. 扩展搜索词
        4. 重新搜索并合并结果
        5. 按图谱关联度排序
        
        Args:
            query: 原始搜索词
            original_results: 原始搜索结果
            top_k: 返回数量
        
        Returns:
            增强后的搜索结果
        """
        # 1. 提取 query 中的实体
        entities = self._extract_entities(query)
        
        if not entities:
            # 无实体，返回原始结果
            return original_results[:top_k]
        
        # 2. 查找相关概念
        related_concepts = self._find_related_concepts(entities)
        
        if not related_concepts:
            # 无相关概念，返回原始结果
            return original_results[:top_k]
        
        # 3. 扩展搜索词
        expanded_queries = [query] + related_concepts
        
        # 4. 重新搜索
        all_results = []
        seen_ids = set()
        
        for exp_query in expanded_queries:
            results = self.hub.search(query=exp_query, top_k=top_k)
            
            for r in results:
                if r.get('id') not in seen_ids:
                    # 添加图谱关联度分数
                    r['kg_relevance'] = self._calculate_kg_relevance(r, entities)
                    all_results.append(r)
                    seen_ids.add(r.get('id'))
        
        # 5. 按图谱关联度排序
        all_results.sort(key=lambda x: x.get('kg_relevance', 0), reverse=True)
        
        return all_results[:top_k]
    
    def _extract_entities(self, text: str) -> List[str]:
        """从文本中提取实体（简化版）"""
        # 简单规则：提取名词性词汇
        # 可以扩展为 NER 或 LLM 提取
        
        # 常见技术实体
        tech_entities = [
            'Python', 'JavaScript', 'SQL', 'Redis', 'Docker', 'K8s',
            'FastAPI', 'React', 'Vue', 'TensorFlow', 'PyTorch',
            '异步', '缓存', '连接池', '索引', '事务', '锁',
            'RESTful', 'WebSocket', 'GraphQL', 'Microservice'
        ]
        
        entities = []
        text_lower = text.lower()
        
        for entity in tech_entities:
            if entity.lower() in text_lower:
                entities.append(entity)
        
        return entities
    
    def _find_related_concepts(self, entities: List[str]) -> List[str]:
        """查找图谱中的相关概念"""
        related = []
        
        # 从图谱中查找关系
        for relation in self.kg_data.get('relations', []):
            source = relation.get('source', '')
            target = relation.get('target', '')
            rel_type = relation.get('type', '')
            
            # 如果实体在关系中
            for entity in entities:
                if entity.lower() in source.lower():
                    related.append(target)
                elif entity.lower() in target.lower():
                    related.append(source)
        
        # 去重
        return list(set(related))[:5]  # 最多 5 个相关概念
    
    def _calculate_kg_relevance(self, result: Dict, entities: List[str]) -> float:
        """
        计算结果与图谱实体的关联度
        
        Args:
            result: 搜索结果
            entities: query 中的实体
        
        Returns:
            关联度分数 (0.0-1.0)
        """
        score = 0.0
        content = result.get('content', '') + ' ' + result.get('title', '')
        content_lower = content.lower()
        
        # 实体匹配
        for entity in entities:
            if entity.lower() in content_lower:
                score += 0.3
        
        # 相关概念匹配
        related = self._find_related_concepts(entities)
        for concept in related:
            if concept.lower() in content_lower:
                score += 0.2
        
        # 图谱中有明确关系
        for relation in self.kg_data.get('relations', []):
            if any(e.lower() in relation.get('source', '').lower() for e in entities):
                score += 0.1
            if any(e.lower() in relation.get('target', '').lower() for e in entities):
                score += 0.1
        
        return min(1.0, score)


# 快捷函数
def enhance_search(query: str, results: List[Dict], agent_name: str = "default"):
    """快捷增强搜索"""
    enhancer = KnowledgeGraphSearchEnhancer(agent_name=agent_name)
    return enhancer.enhance_search(query, results)
