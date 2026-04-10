#!/usr/bin/env python3
"""
build_relationships.py - 自动推断并构建实体间关系

基于以下规则推断关系：
1. 共现关系：在同一文件中频繁出现的实体可能有关系
2. 类型关系：Agent 使用 Technology，Project 使用 Technology
3. 层级关系：子项目属于父项目
4. 语义关系：基于实体名称的语义相似度
"""

import json
from pathlib import Path
from collections import defaultdict
import re

def load_knowledge_graph():
    """加载知识图谱"""
    # 尝试多个可能的位置
    possible_paths = [
        Path(__file__).parent.parent.parent / 'memory' / 'knowledge_graph.json',
        Path(__file__).parent.parent / 'memory' / 'knowledge_graph.json',
        Path('/Users/dhr/.openclaw/workspace/memory/knowledge_graph.json')
    ]
    
    for kg_file in possible_paths:
        if kg_file.exists():
            with open(kg_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    raise FileNotFoundError(f"Knowledge graph not found in {possible_paths}")

def save_knowledge_graph(data):
    """保存知识图谱"""
    kg_file = Path('/Users/dhr/.openclaw/workspace/memory/knowledge_graph.json')
    with open(kg_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def infer_relationships(entities):
    """推断实体间关系"""
    relationships = []
    entity_list = list(entities.values())
    
    print("🔍 开始推断关系...")
    print()
    
    # ========== 规则 1: Agent 使用 Technology ==========
    print("📌 规则 1: Agent 使用 Technology")
    agents = [e for e in entity_list if e.get('type') == 'Agent']
    technologies = [e for e in entity_list if e.get('type') == 'Technology']
    
    # 从记忆文件中分析共现关系
    memory_dir = Path('/Users/dhr/.openclaw/workspace/memory')
    co_occurrence = defaultdict(lambda: defaultdict(int))
    
    for md_file in memory_dir.glob('*.md'):
        if md_file.name.startswith('2026-'):
            content = md_file.read_text(encoding='utf-8')
            
            # 找出该文件中提到的所有实体
            file_entities = []
            for entity in entity_list:
                entity_name = entity.get('name', '')
                if entity_name and entity_name in content:
                    file_entities.append(entity)
            
            # 统计 Agent 和 Technology 的共现
            file_agents = [e for e in file_entities if e.get('type') == 'Agent']
            file_techs = [e for e in file_entities if e.get('type') == 'Technology']
            
            for agent in file_agents:
                for tech in file_techs:
                    agent_name = agent.get('name', '')
                    tech_name = tech.get('name', '')
                    co_occurrence[agent_name][tech_name] += 1
    
    # 创建关系（共现次数 >= 2）
    count = 0
    for agent_name, techs in co_occurrence.items():
        for tech_name, freq in techs.items():
            if freq >= 2:
                relationships.append({
                    'from': agent_name,
                    'to': tech_name,
                    'type': 'USES',
                    'weight': freq,
                    'evidence': f'共现于{freq}个文件'
                })
                count += 1
    
    print(f"   ✅ 发现 {count} 条 USES 关系")
    print()
    
    # ========== 规则 2: Project 使用 Technology ==========
    print("📌 规则 2: Project 使用 Technology")
    projects = [e for e in entity_list if e.get('type') == 'Project']
    
    co_occurrence_proj = defaultdict(lambda: defaultdict(int))
    
    for md_file in memory_dir.glob('*.md'):
        if md_file.name.startswith('2026-'):
            content = md_file.read_text(encoding='utf-8')
            
            file_projects = []
            file_techs = []
            
            for entity in entity_list:
                entity_name = entity.get('name', '')
                if entity_name and entity_name in content:
                    etype = entity.get('type', '')
                    if etype == 'Project':
                        file_projects.append(entity)
                    elif etype == 'Technology':
                        file_techs.append(entity)
            
            for proj in file_projects:
                for tech in file_techs:
                    proj_name = proj.get('name', '')
                    tech_name = tech.get('name', '')
                    co_occurrence_proj[proj_name][tech_name] += 1
    
    count = 0
    for proj_name, techs in co_occurrence_proj.items():
        for tech_name, freq in techs.items():
            if freq >= 2:
                relationships.append({
                    'from': proj_name,
                    'to': tech_name,
                    'type': 'USES',
                    'weight': freq,
                    'evidence': f'共现于{freq}个文件'
                })
                count += 1
    
    print(f"   ✅ 发现 {count} 条 Project USES Technology 关系")
    print()
    
    # ========== 规则 3: Agent 属于 Project ==========
    print("📌 规则 3: Agent 属于 Project")
    
    # 基于命名模式推断
    for agent in agents:
        agent_name = agent.get('name', '')
        
        # 查找包含 Agent 名称的 Project
        for proj in projects:
            proj_name = proj.get('name', '')
            
            # 如果 Project 名称包含 Agent 名称或反之
            if agent_name.lower() in proj_name.lower() or proj_name.lower() in agent_name.lower():
                relationships.append({
                    'from': agent_name,
                    'to': proj_name,
                    'type': 'BELONGS_TO',
                    'weight': 5,
                    'evidence': '命名模式匹配'
                })
                print(f"   • {agent_name} BELONGS_TO {proj_name}")
    
    print()
    
    # ========== 规则 4: Technology 相关关系 ==========
    print("📌 规则 4: Technology 相关关系")
    
    # 语义相关的 Technology
    tech_groups = {
        '搜索技术': ['关键词搜索', '语义搜索', 'Bing'],
        '嵌入模型': ['nomic-embed-text', 'bge-m3', '嵌入模型'],
        '数据格式': ['JSON', 'Markdown', 'SQLite'],
    }
    
    count = 0
    for group_name, techs in tech_groups.items():
        for i, tech1 in enumerate(techs):
            for tech2 in techs[i+1:]:
                # 检查这两个技术是否都存在
                if any(e.get('name') == tech1 for e in technologies) and \
                   any(e.get('name') == tech2 for e in technologies):
                    relationships.append({
                        'from': tech1,
                        'to': tech2,
                        'type': 'RELATED_TO',
                        'weight': 3,
                        'evidence': f'同属{group_name}',
                        'group': group_name
                    })
                    count += 1
    
    print(f"   ✅ 发现 {count} 条 RELATED_TO 关系")
    print()
    
    # ========== 规则 5: Skill 增强 Project ==========
    print("📌 规则 5: Skill 增强 Project")
    skills = [e for e in entity_list if e.get('type') == 'Skill']
    
    for skill in skills:
        skill_name = skill.get('name', '')
        for proj in projects:
            proj_name = proj.get('name', '')
            # 假设所有 Skill 都用于所有 Project（简化处理）
            relationships.append({
                'from': skill_name,
                'to': proj_name,
                'type': 'ENHANCES',
                'weight': 2,
                'evidence': '技能增强项目'
            })
    
    print(f"   ✅ 发现 {len(skills) * len(projects)} 条 ENHANCES 关系")
    print()
    
    return relationships

def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║     构建实体关系                                        ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # 加载知识图谱
    data = load_knowledge_graph()
    entities = data.get('entities', {})
    existing_rels = data.get('relationships', [])
    
    print(f"📊 当前状态:")
    print(f"   • 实体数：{len(entities)}")
    print(f"   • 现有关系：{len(existing_rels)}")
    print()
    
    # 推断新关系
    new_relationships = infer_relationships(entities)
    
    # 合并关系（去重）
    all_relationships = existing_rels.copy() if isinstance(existing_rels, list) else []
    
    # 去重
    seen = set()
    unique_rels = []
    for rel in new_relationships:
        key = (rel['from'], rel['to'], rel['type'])
        if key not in seen:
            seen.add(key)
            unique_rels.append(rel)
    
    all_relationships.extend(unique_rels)
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print(f"✅ 关系构建完成!")
    print(f"   • 新增关系：{len(unique_rels)}条")
    print(f"   • 总关系数：{len(all_relationships)}条")
    print()
    
    # 保存
    data['relationships'] = all_relationships
    save_knowledge_graph(data)
    
    print(f"💾 已保存到 memory/knowledge_graph.json")
    print()
    
    # 展示部分关系
    print("🔗 关系示例 (Top 20):")
    print("-" * 60)
    sorted_rels = sorted(all_relationships, key=lambda x: x.get('weight', 0), reverse=True)[:20]
    for i, rel in enumerate(sorted_rels, 1):
        from_e = rel.get('from', 'unknown')
        to_e = rel.get('to', 'unknown')
        rel_type = rel.get('type', 'unknown')
        weight = rel.get('weight', 0)
        print(f"   {i:2}. {from_e:25} --[{rel_type:12}]--> {to_e:25} (权重：{weight})")
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == '__main__':
    main()
