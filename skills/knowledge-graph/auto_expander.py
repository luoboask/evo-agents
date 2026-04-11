#!/usr/bin/env python3
"""
知识图谱自动扩展器 - 从对话中自动提取实体和关系

功能:
- 从对话中提取实体（人名、项目、技术等）
- 识别实体间关系
- 自动更新知识图谱
- 支持批量处理

用法:
    python3 skills/knowledge-graph/auto_expander.py --agent demo51-agent
"""

import sys
import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))


class KnowledgeGraphAutoExpander:
    """知识图谱自动扩展器"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.db_path = Path(f'data/{agent_name}/memory/memory_stream.db')
        self.kg_path = Path(f'data/{agent_name}/knowledge/private/knowledge_graph.json')
        
        # 实体类型模式
        self.entity_patterns = {
            'technology': [
                r'Python', r'JavaScript', r'SQL', r'Redis', r'Docker', r'K8s',
                r'FastAPI', r'React', r'Vue', r'TensorFlow', r'PyTorch'
            ],
            'project': [
                r'电商平台', r'用户系统', r'支付系统', r'日志系统', r'监控系统'
            ],
            'concept': [
                r'异步', r'缓存', r'连接池', r'索引', r'事务', r'锁',
                r'RESTful', r'WebSocket', r'GraphQL', r'Microservice'
            ],
            'person': [
                r'[A-Z][a-z]+',  # 英文名
            ],
            'tool': [
                r'Git', r'Jenkins', r'Prometheus', r'Grafana', r'ELK',
                r'VSCode', r'PyCharm'
            ]
        }
        
        # 关系模式
        self.relation_patterns = {
            'uses': [r'使用', r'采用', r'基于'],
            'contains': [r'包含', r'包括', r'有'],
            'optimizes': [r'优化', r'提升', r'改善'],
            'depends_on': [r'依赖', r'需要', r'要求'],
            'conflicts_with': [r'冲突', r'不兼容', r'问题']
        }
    
    def extract_entities(self, text: str) -> List[Dict]:
        """从文本中提取实体"""
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    entity_name = match.group()
                    entities.append({
                        'type': entity_type,
                        'name': entity_name,
                        'source': text[:100],
                        'confidence': 0.8
                    })
        
        # 去重
        seen = set()
        unique = []
        for e in entities:
            key = f"{e['type']}:{e['name']}"
            if key not in seen:
                seen.add(key)
                unique.append(e)
        
        return unique
    
    def extract_relations(self, text: str, entities: List[Dict]) -> List[Dict]:
        """从文本中提取关系"""
        relations = []
        
        for rel_type, patterns in self.relation_patterns.items():
            for pattern in patterns:
                # 简单匹配：实体 1 + 关系 + 实体 2
                for p in patterns:
                    regex = f"({p})"
                    matches = re.finditer(regex, text)
                    for match in matches:
                        # 查找前后的实体
                        start = max(0, match.start() - 20)
                        end = min(len(text), match.end() + 20)
                        context = text[start:end]
                        
                        # 简单提取（可以改进）
                        for e1 in entities:
                            for e2 in entities:
                                if e1['name'] != e2['name']:
                                    if e1['name'] in context and e2['name'] in context:
                                        relations.append({
                                            'source': e1['name'],
                                            'relation': rel_type,
                                            'target': e2['name'],
                                            'confidence': 0.7
                                        })
        
        return relations
    
    def expand(self, limit=50) -> Dict:
        """从记忆中提取并扩展知识图谱"""
        print(f"🧠 从记忆中提取知识...")
        print("=" * 70)
        
        # 读取记忆
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT content FROM session_memories
        ORDER BY id DESC
        LIMIT ?
        ''', (limit,))
        
        memories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # 加载现有知识图谱
        kg = self._load_kg()
        
        # 提取实体和关系
        new_entities = 0
        new_relations = 0
        
        for memory in memories:
            entities = self.extract_entities(memory)
            relations = self.extract_relations(memory, entities)
            
            # 添加到知识图谱
            for entity in entities:
                key = f"{entity['type']}:{entity['name']}"
                if key not in kg['entities']:
                    kg['entities'][key] = entity
                    new_entities += 1
                    print(f"  ✅ 新实体：[{entity['type']}] {entity['name']}")
            
            for relation in relations:
                rel_key = f"{relation['source']}:{relation['relation']}:{relation['target']}"
                if not any(r.get('source') == relation['source'] and 
                          r.get('relation') == relation['relation'] and 
                          r.get('target') == relation['target'] 
                          for r in kg['relations']):
                    kg['relations'].append(relation)
                    new_relations += 1
                    print(f"  ✅ 新关系：{relation['source']} -[{relation['relation']}]-> {relation['target']}")
        
        # 保存
        self._save_kg(kg)
        
        print(f"\n📊 扩展结果:")
        print(f"  总实体数：{len(kg['entities'])} (+{new_entities})")
        print(f"  总关系数：{len(kg['relations'])} (+{new_relations})")
        
        return {
            'new_entities': new_entities,
            'new_relations': new_relations,
            'total_entities': len(kg['entities']),
            'total_relations': len(kg['relations'])
        }
    
    def _load_kg(self) -> Dict:
        """加载知识图谱"""
        if self.kg_path.exists():
            with open(self.kg_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 创建新的
            self.kg_path.parent.mkdir(parents=True, exist_ok=True)
            return {'entities': {}, 'relations': [], 'updated_at': datetime.now().isoformat()}
    
    def _save_kg(self, kg: Dict):
        """保存知识图谱"""
        kg['updated_at'] = datetime.now().isoformat()
        
        with open(self.kg_path, 'w', encoding='utf-8') as f:
            json.dump(kg, f, ensure_ascii=False, indent=2)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='知识图谱自动扩展器')
    parser.add_argument('--agent', type=str, default='demo51-agent', help='Agent 名称')
    parser.add_argument('--limit', type=int, default=50, help='处理的记忆数量')
    
    args = parser.parse_args()
    
    expander = KnowledgeGraphAutoExpander(args.agent)
    result = expander.expand(args.limit)
    
    print(f"\n✅ 知识图谱扩展完成！")


if __name__ == '__main__':
    main()
