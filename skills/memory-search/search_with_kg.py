#!/usr/bin/env python3
"""
search_with_kg.py - 集成知识图谱的语义搜索

增强功能:
1. 实体识别：识别查询中的实体
2. 关系扩展：通过关系网络找到相关实体
3. 加权排序：结合文本相似度和关系权重
4. 可解释性：显示为什么返回这些结果
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

def load_knowledge_graph():
    """加载知识图谱"""
    kg_file = Path('/Users/dhr/.openclaw/workspace/memory/knowledge_graph.json')
    if kg_file.exists():
        with open(kg_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_memories():
    """加载记忆文件"""
    memory_dir = Path('/Users/dhr/.openclaw/workspace/memory')
    memories = []
    
    for md_file in memory_dir.glob('*.md'):
        if md_file.name.startswith('2026-'):
            content = md_file.read_text(encoding='utf-8')
            memories.append({
                'file': md_file.name,
                'content': content,
                'date': md_file.stem
            })
    
    # 也加载 MEMORY.md
    memory_md = memory_dir.parent / 'MEMORY.md'
    if memory_md.exists():
        memories.append({
            'file': 'MEMORY.md',
            'content': memory_md.read_text(encoding='utf-8'),
            'date': 'long-term'
        })
    
    return memories

def extract_entities_from_query(query, entities):
    """从查询中提取实体"""
    found_entities = []
    
    for entity_id, entity_data in entities.items():
        entity_name = entity_data.get('name', '')
        if entity_name and entity_name in query:
            found_entities.append({
                'id': entity_id,
                'name': entity_name,
                'type': entity_data.get('type', 'unknown'),
                'mentions': entity_data.get('mentions', 0)
            })
    
    return found_entities

def find_related_entities(entity_ids, relationships, max_depth=2):
    """通过关系网络找到相关实体"""
    related = set()
    
    # 建立索引
    rel_from = {}
    rel_to = {}
    for rel in relationships:
        from_e = rel.get('from', '')
        to_e = rel.get('to', '')
        rel_type = rel.get('type', '')
        weight = rel.get('weight', 1)
        
        if from_e not in rel_from:
            rel_from[from_e] = []
        rel_from[from_e].append((to_e, rel_type, weight))
        
        if to_e not in rel_to:
            rel_to[to_e] = []
        rel_to[to_e].append((from_e, rel_type, weight))
    
    # BFS 查找相关实体
    queue = [(e, 0) for e in entity_ids]
    visited = set(entity_ids)
    
    while queue:
        current, depth = queue.pop(0)
        
        if depth >= max_depth:
            continue
        
        # 查找从当前实体出发的关系
        if current in rel_from:
            for target, rel_type, weight in rel_from[current]:
                if target not in visited:
                    visited.add(target)
                    related.add((target, rel_type, weight, depth + 1))
                    queue.append((target, depth + 1))
        
        # 查找指向当前实体的关系
        if current in rel_to:
            for target, rel_type, weight in rel_to[current]:
                if target not in visited:
                    visited.add(target)
                    related.add((target, rel_type, weight, depth + 1))
                    queue.append((target, depth + 1))
    
    return related

def search_with_kg(query, top_k=5):
    """集成知识图谱的搜索"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║     语义搜索（增强版 - 集成知识图谱）                    ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # 加载数据
    print("📂 加载数据...")
    kg = load_knowledge_graph()
    memories = load_memories()
    
    if not kg:
        print("   ❌ 知识图谱不存在")
        return
    
    entities = kg.get('entities', {})
    relationships = kg.get('relationships', [])
    
    print(f"   ✅ 加载 {len(entities)}个实体，{len(relationships)}条关系")
    print(f"   ✅ 加载 {len(memories)}个记忆文件")
    print()
    
    # Step 1: 实体识别
    print(f"🔍 查询：\"{query}\"")
    print()
    print("Step 1: 实体识别")
    query_entities = extract_entities_from_query(query, entities)
    
    if query_entities:
        print(f"   ✅ 识别到 {len(query_entities)}个实体:")
        for e in query_entities:
            print(f"      • [{e['type']}] {e['name']} (提及：{e['mentions']}次)")
    else:
        print("   ⚠️  未识别到明确实体，使用纯文本搜索")
    print()
    
    # Step 2: 关系扩展
    print("Step 2: 关系扩展")
    if query_entities:
        entity_ids = [e['id'] for e in query_entities]
        related = find_related_entities(entity_ids, relationships)
        
        if related:
            print(f"   ✅ 找到 {len(related)}个相关实体:")
            for target, rel_type, weight, depth in sorted(related, key=lambda x: x[2], reverse=True)[:10]:
                print(f"      • {target} --[{rel_type}]--> (权重:{weight}, 深度:{depth})")
        else:
            print("   ⚠️  未找到相关实体")
    else:
        related = set()
        print("   ⚠️  跳过（无初始实体）")
    print()
    
    # Step 3: 搜索记忆
    print("Step 3: 搜索记忆")
    results = []
    
    query_lower = query.lower()
    query_entity_names = set(e['name'].lower() for e in query_entities)
    related_entity_names = set(r[0].lower() for r in related)
    
    for memory in memories:
        content = memory['content']
        file = memory['file']
        
        # 基础文本相似度
        text_score = content.lower().count(query_lower)
        
        # 实体匹配加分
        entity_score = 0
        for e in query_entities:
            if e['name'] in content:
                entity_score += e['mentions']
        
        # 相关实体加分
        related_score = 0
        for target, rel_type, weight, depth in related:
            if target in content:
                related_score += weight * (1.0 / depth)
        
        # 综合得分
        total_score = text_score * 1.0 + entity_score * 0.5 + related_score * 0.3
        
        if total_score > 0:
            results.append({
                'file': file,
                'score': total_score,
                'text_matches': text_score,
                'entity_matches': entity_score,
                'related_matches': related_score,
                'preview': content[:200].replace('\n', ' ') + '...'
            })
    
    # 排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"   ✅ 找到 {len(results)}个相关记忆")
    print()
    
    # Step 4: 展示结果
    print("Step 4: 搜索结果 (Top {top_k})".format(top_k=top_k))
    print("-" * 60)
    
    for i, result in enumerate(results[:top_k], 1):
        print(f"\n   {i}. {result['file']}")
        print(f"      综合得分：{result['score']:.2f}")
        print(f"      - 文本匹配：{result['text_matches']}")
        print(f"      - 实体匹配：{result['entity_matches']}")
        print(f"      - 相关实体：{result['related_matches']:.1f}")
        print(f"      预览：{result['preview']}")
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    if results:
        print("💡 洞察:")
        best = results[0]
        print(f"   • 最相关的记忆：{best['file']}")
        print(f"   • 主要匹配方式：{'实体匹配' if best['entity_matches'] > best['text_matches'] else '文本匹配'}")
        
        if query_entities:
            print(f"   • 识别到的实体：{', '.join(e['name'] for e in query_entities)}")
        
        if related:
            print(f"   • 扩展的相关实体：{len(related)}个")
    else:
        print("💡 未找到相关记忆，尝试其他关键词")
    
    print()
    print("✅ 搜索完成!")
    
    return results

if __name__ == '__main__':
    # 测试查询
    test_queries = [
        "Harness Agent",
        "OpenClaw Python",
        "语义搜索 Ollama",
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70 + "\n")
        search_with_kg(query, top_k=3)
        print()
