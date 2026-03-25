#!/usr/bin/env python3
"""
知识图谱构建器 - Knowledge Graph Builder
从记忆中提取实体和关系，构建知识网络
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class KnowledgeGraph:
    """知识图谱系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.memory_dir = self.workspace / "memory"
        self.graph_file = self.memory_dir / "knowledge_graph.json"
        
        # 实体和关系存储
        self.entities = {}  # id -> {type, name, properties}
        self.relations = []  # (source, relation, target, confidence)
        
        # 加载已有图谱
        self.load()
    
    def load(self):
        """加载已有知识图谱"""
        if self.graph_file.exists():
            with open(self.graph_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.entities = data.get('entities', {})
                self.relations = data.get('relations', [])
    
    def save(self):
        """保存知识图谱"""
        data = {
            'entities': self.entities,
            'relations': self.relations,
            'updated_at': datetime.now().isoformat()
        }
        with open(self.graph_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_entity(self, entity_type, name, properties=None):
        """添加实体"""
        entity_id = f"{entity_type}:{name.lower().replace(' ', '_')}"
        
        if entity_id not in self.entities:
            self.entities[entity_id] = {
                'type': entity_type,
                'name': name,
                'properties': properties or {},
                'created_at': datetime.now().isoformat(),
                'mentions': 1
            }
        else:
            self.entities[entity_id]['mentions'] += 1
            if properties:
                self.entities[entity_id]['properties'].update(properties)
        
        return entity_id
    
    def add_relation(self, source, relation, target, confidence=1.0):
        """添加关系"""
        self.relations.append({
            'source': source,
            'relation': relation,
            'target': target,
            'confidence': confidence,
            'created_at': datetime.now().isoformat()
        })
    
    def extract_from_memory(self):
        """从记忆文件中提取知识"""
        # 定义实体模式
        patterns = {
            'Skill': [
                r'创建了\s+[`\']?(\w+)[`\']?\s+技能',
                r'实现了\s+[`\']?(\w+)[`\']?',
            ],
            'Project': [
                r'(\w+)\s+是阿里云推出的',
                r'基于\s+(\w+)\s+框架',
            ],
            'Technology': [
                r'(Python|Ollama|Bing|OpenClaw|JVS Claw)',
                r'(语义搜索|关键词搜索|嵌入模型)',
            ],
            'Person': [
                r'用户\s*[:：]\s*(\w+)',
            ],
            'Decision': [
                r'决定[：:]\s*(.+)',
                r'使用\s+(\w+)\s+而非',
            ]
        }
        
        # 读取所有记忆文件
        memory_files = list(self.memory_dir.glob('*.md'))
        memory_files.append(self.workspace / 'MEMORY.md')
        
        for file_path in memory_files:
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取实体
                for entity_type, type_patterns in patterns.items():
                    for pattern in type_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            if isinstance(match, tuple):
                                match = match[0]
                            if len(match) > 2:  # 忽略太短的匹配
                                self.add_entity(entity_type, match.strip())
                
                # 提取关系（简化版）
                # "X 基于 Y" -> (X, based_on, Y)
                based_on_matches = re.findall(r'(\w+)\s+基于\s+(\w+)', content)
                for x, y in based_on_matches:
                    x_id = self.add_entity('Technology', x)
                    y_id = self.add_entity('Technology', y)
                    self.add_relation(x_id, 'based_on', y_id)
                
                # "创建了 X" -> (User, created, X)
                created_matches = re.findall(r'创建了\s+[`\']?(\w+)[`\']?', content)
                for x in created_matches:
                    x_id = self.add_entity('Skill', x)
                    self.add_relation('Person:user', 'created', x_id)
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        self.save()
    
    def query(self, entity_name=None, entity_type=None, relation=None):
        """查询知识图谱"""
        results = []
        
        # 查找实体
        matching_entities = []
        for entity_id, entity in self.entities.items():
            match = True
            if entity_name and entity_name.lower() not in entity['name'].lower():
                match = False
            if entity_type and entity['type'] != entity_type:
                match = False
            if match:
                matching_entities.append(entity_id)
        
        # 查找关系
        for rel in self.relations:
            if rel['source'] in matching_entities or rel['target'] in matching_entities:
                if relation is None or rel['relation'] == relation:
                    results.append({
                        'source': self.entities.get(rel['source'], {}).get('name', rel['source']),
                        'relation': rel['relation'],
                        'target': self.entities.get(rel['target'], {}).get('name', rel['target']),
                        'confidence': rel['confidence']
                    })
        
        return results
    
    def get_stats(self):
        """获取统计信息"""
        type_counts = defaultdict(int)
        for entity in self.entities.values():
            type_counts[entity['type']] += 1
        
        return {
            'total_entities': len(self.entities),
            'total_relations': len(self.relations),
            'entity_types': dict(type_counts),
            'relation_types': list(set(r['relation'] for r in self.relations))
        }
    
    def print_graph(self):
        """打印知识图谱摘要"""
        stats = self.get_stats()
        
        print("=" * 60)
        print("🕸️  知识图谱摘要")
        print("=" * 60)
        print()
        print(f"实体总数: {stats['total_entities']}")
        print(f"关系总数: {stats['total_relations']}")
        print()
        print("实体类型分布:")
        for entity_type, count in sorted(stats['entity_types'].items(), key=lambda x: -x[1]):
            print(f"  - {entity_type}: {count}")
        print()
        
        if stats['relation_types']:
            print("关系类型:")
            for rel_type in stats['relation_types']:
                print(f"  - {rel_type}")
            print()
        
        # 显示一些示例实体
        print("示例实体:")
        for i, (entity_id, entity) in enumerate(list(self.entities.items())[:5]):
            print(f"  - [{entity['type']}] {entity['name']} (提及 {entity['mentions']} 次)")
        print()
        print("=" * 60)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='知识图谱构建器')
    parser.add_argument('--build', action='store_true', help='从记忆构建图谱')
    parser.add_argument('--query', type=str, help='查询实体')
    parser.add_argument('--stats', action='store_true', help='显示统计')
    
    args = parser.parse_args()
    
    kg = KnowledgeGraph()
    
    if args.build:
        print("正在从记忆文件中提取知识...")
        kg.extract_from_memory()
        print("✅ 知识图谱已更新")
        kg.print_graph()
    elif args.query:
        results = kg.query(entity_name=args.query)
        if results:
            print(f"\n🔍 查询 '{args.query}' 的结果:")
            for r in results:
                print(f"  {r['source']} --[{r['relation']}]--> {r['target']}")
        else:
            print(f"未找到与 '{args.query}' 相关的信息")
    elif args.stats:
        kg.print_graph()
    else:
        kg.print_graph()


if __name__ == '__main__':
    main()
