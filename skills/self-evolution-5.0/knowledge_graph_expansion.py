#!/usr/bin/env python3
"""
知识图谱自动扩展系统 - Knowledge Graph Auto-Expansion
实现：自动实体提取、关系发现、知识融合
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class EntityExtractor:
    """实体提取器"""
    
    def __init__(self):
        # 实体类型模式
        self.entity_patterns = {
            'technology': [
                r'\b(Python|JavaScript|AI|ML|Deep Learning|Neural Network)\b',
                r'\b(OpenClaw|Agent|Skill|Module|System)\b'
            ],
            'concept': [
                r'\b(learning|evolution|optimization|reasoning|creativity)\b',
                r'\b(knowledge|memory|intelligence|awareness)\b'
            ],
            'person': [
                r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'
            ],
            'organization': [
                r'\b(GitHub|OpenAI|Anthropic|Google|Microsoft)\b'
            ]
        }
        
        self.extracted_entities = []
    
    def extract_from_text(self, text: str) -> List[dict]:
        """从文本中提取实体"""
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity = {
                        'id': f"{entity_type}_{match.lower().replace(' ', '_')}",
                        'name': match,
                        'type': entity_type,
                        'confidence': 0.8,
                        'source': text[:100]
                    }
                    entities.append(entity)
                    self.extracted_entities.append(entity)
        
        return entities
    
    def get_extraction_statistics(self) -> dict:
        """提取统计"""
        by_type = defaultdict(int)
        for entity in self.extracted_entities:
            by_type[entity['type']] += 1
        
        return {
            'total_entities': len(self.extracted_entities),
            'by_type': dict(by_type)
        }


class RelationDiscoverer:
    """关系发现器"""
    
    def __init__(self):
        # 关系模式
        self.relation_patterns = {
            'uses': [
                r'(\w+) uses (\w+)',
                r'(\w+) 使用 (\w+)'
            ],
            'part_of': [
                r'(\w+) is part of (\w+)',
                r'(\w+) 是 (\w+) 的一部分'
            ],
            'improves': [
                r'(\w+) improves (\w+)',
                r'(\w+) 提升 (\w+)'
            ],
            'depends_on': [
                r'(\w+) depends on (\w+)',
                r'(\w+) 依赖 (\w+)'
            ]
        }
        
        self.discovered_relations = []
    
    def discover_from_text(self, text: str, entities: List[dict]) -> List[dict]:
        """从文本中发现关系"""
        relations = []
        
        for relation_type, patterns in self.relation_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        entity1, entity2 = match
                        relations.append({
                            'id': f"{relation_type}_{len(self.discovered_relations)}",
                            'type': relation_type,
                            'from': entity1.lower(),
                            'to': entity2.lower(),
                            'confidence': 0.7,
                            'source': text[:100]
                        })
                        self.discovered_relations.append(relations[-1])
        
        return relations
    
    def get_discovery_statistics(self) -> dict:
        """发现统计"""
        by_type = defaultdict(int)
        for relation in self.discovered_relations:
            by_type[relation['type']] += 1
        
        return {
            'total_relations': len(self.discovered_relations),
            'by_type': dict(by_type)
        }


class KnowledgeFusion:
    """知识融合器"""
    
    def __init__(self):
        self.fusion_history = []
    
    def fuse_entities(self, entities1: List[dict], entities2: List[dict]) -> List[dict]:
        """融合两个实体列表"""
        fused = []
        entity_map = {}
        
        # 建立映射
        for entity in entities1:
            key = f"{entity['type']}_{entity['name'].lower()}"
            entity_map[key] = entity
        
        # 融合
        for entity in entities2:
            key = f"{entity['type']}_{entity['name'].lower()}"
            if key in entity_map:
                # 合并
                existing = entity_map[key]
                merged = {
                    **existing,
                    'confidence': max(existing.get('confidence', 0), entity.get('confidence', 0)),
                    'sources': [existing.get('source', ''), entity.get('source', '')]
                }
                fused.append(merged)
            else:
                fused.append(entity)
        
        self.fusion_history.append({
            'timestamp': datetime.now().isoformat(),
            'input_count': len(entities1) + len(entities2),
            'output_count': len(fused)
        })
        
        return fused
    
    def get_fusion_statistics(self) -> dict:
        """融合统计"""
        return {
            'total_fusions': len(self.fusion_history),
            'entities_merged': sum(
                f['input_count'] - f['output_count'] 
                for f in self.fusion_history
            )
        }


class KnowledgeGraphExpander:
    """知识图谱扩展器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        self.entity_extractor = EntityExtractor()
        self.relation_discoverer = RelationDiscoverer()
        self.knowledge_fusion = KnowledgeFusion()
        
        # 知识图谱
        self.knowledge_graph = {
            'entities': {},
            'relations': [],
            'last_updated': None
        }
        
        self._load_knowledge_graph()
    
    def _load_knowledge_graph(self):
        """加载知识图谱"""
        kg_file = self.learning_dir / 'knowledge_graph_expanded.json'
        if kg_file.exists():
            with open(kg_file, 'r') as f:
                self.knowledge_graph = json.load(f)
    
    def _save_knowledge_graph(self):
        """保存知识图谱"""
        self.knowledge_graph['last_updated'] = datetime.now().isoformat()
        kg_file = self.learning_dir / 'knowledge_graph_expanded.json'
        with open(kg_file, 'w') as f:
            json.dump(self.knowledge_graph, f, indent=2, ensure_ascii=False)
    
    def expand_from_text(self, text: str) -> dict:
        """从文本扩展知识图谱"""
        print(f"📚 从文本扩展知识图谱...")
        
        expansion = {
            'timestamp': datetime.now().isoformat(),
            'text_length': len(text),
            'new_entities': 0,
            'new_relations': 0,
            'fused_entities': 0
        }
        
        # 1. 提取实体
        entities = self.entity_extractor.extract_from_text(text)
        expansion['new_entities'] = len(entities)
        
        # 2. 发现关系
        relations = self.relation_discoverer.discover_from_text(text, entities)
        expansion['new_relations'] = len(relations)
        
        # 3. 融合知识
        existing_entities = list(self.knowledge_graph['entities'].values())
        fused = self.knowledge_fusion.fuse_entities(existing_entities, entities)
        expansion['fused_entities'] = len(existing_entities) + len(entities) - len(fused)
        
        # 4. 更新知识图谱
        for entity in fused:
            self.knowledge_graph['entities'][entity['id']] = entity
        
        self.knowledge_graph['relations'].extend(relations)
        
        # 5. 保存
        self._save_knowledge_graph()
        
        print(f"   ✅ 提取 {expansion['new_entities']} 个实体")
        print(f"   ✅ 发现 {expansion['new_relations']} 个关系")
        print(f"   ✅ 融合 {expansion['fused_entities']} 个实体")
        
        return expansion
    
    def expand_from_learning(self) -> dict:
        """从学习记录扩展"""
        print(f"📚 从学习记录扩展知识图谱...")
        
        expansion = {
            'timestamp': datetime.now().isoformat(),
            'sources_processed': 0,
            'entities_added': 0,
            'relations_added': 0
        }
        
        # 读取学习文件
        learning_files = list(self.learning_dir.glob('*.jsonl'))
        
        for file in learning_files:
            if file.name.startswith('scheduled_learning_'):
                with open(file, 'r') as f:
                    for line in f:
                        if line.strip():
                            record = json.loads(line)
                            text = json.dumps(record)
                            result = self.expand_from_text(text)
                            expansion['sources_processed'] += 1
                            expansion['entities_added'] += result['new_entities']
                            expansion['relations_added'] += result['new_relations']
        
        print(f"   ✅ 处理 {expansion['sources_processed']} 个学习文件")
        
        return expansion
    
    def query_entities(self, entity_type: str = None) -> List[dict]:
        """查询实体"""
        entities = list(self.knowledge_graph['entities'].values())
        
        if entity_type:
            entities = [e for e in entities if e.get('type') == entity_type]
        
        return entities
    
    def query_relations(self, relation_type: str = None) -> List[dict]:
        """查询关系"""
        relations = self.knowledge_graph['relations']
        
        if relation_type:
            relations = [r for r in relations if r.get('type') == relation_type]
        
        return relations
    
    def get_graph_statistics(self) -> dict:
        """获取图谱统计"""
        entity_types = defaultdict(int)
        for entity in self.knowledge_graph['entities'].values():
            entity_types[entity.get('type', 'unknown')] += 1
        
        relation_types = defaultdict(int)
        for relation in self.knowledge_graph['relations']:
            relation_types[relation.get('type', 'unknown')] += 1
        
        return {
            'total_entities': len(self.knowledge_graph['entities']),
            'total_relations': len(self.knowledge_graph['relations']),
            'entity_types': dict(entity_types),
            'relation_types': dict(relation_types),
            'last_updated': self.knowledge_graph.get('last_updated'),
            'extraction_stats': self.entity_extractor.get_extraction_statistics(),
            'discovery_stats': self.relation_discoverer.get_discovery_statistics(),
            'fusion_stats': self.knowledge_fusion.get_fusion_statistics()
        }


# 使用示例
if __name__ == '__main__':
    expander = KnowledgeGraphExpander()
    
    print("=" * 70)
    print("📚 知识图谱自动扩展演示")
    print("=" * 70)
    print()
    
    # 1. 从文本扩展
    print("1️⃣ 从文本扩展")
    print("-" * 70)
    text = """
    OpenClaw uses Python for implementation. 
    AI improves learning efficiency. 
    Machine Learning is part of Artificial Intelligence.
    Agent 依赖 Skill 来执行任务。
    """
    result = expander.expand_from_text(text)
    print()
    
    # 2. 从学习记录扩展
    print("2️⃣ 从学习记录扩展")
    print("-" * 70)
    result = expander.expand_from_learning()
    print()
    
    # 3. 查询实体
    print("3️⃣ 查询实体")
    print("-" * 70)
    entities = expander.query_entities('technology')
    print(f"   技术类实体：{len(entities)} 个")
    for entity in entities[:5]:
        print(f"     - {entity['name']}")
    print()
    
    # 4. 统计
    print("📊 图谱统计:")
    stats = expander.get_graph_statistics()
    print(f"   总实体数：{stats['total_entities']}")
    print(f"   总关系数：{stats['total_relations']}")
    print(f"   实体类型：{stats['entity_types']}")
    print(f"   关系类型：{stats['relation_types']}")
