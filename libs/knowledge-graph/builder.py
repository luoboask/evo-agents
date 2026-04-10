#!/usr/bin/env python3
"""
知识图谱构建器 - 增强版 (Knowledge Graph Builder Enhanced)
从记忆中提取实体和关系，构建知识网络

增强功能：
1. AI 辅助实体识别（使用 Ollama）
2. 关系推断（传递闭包）
3. 智能摘要压缩
"""

import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 使用 evo-agents 标准路径解析工具
try:
    from path_utils import resolve_workspace
except ImportError:
    # 回退：动态检测（兼容旧版本）
    def resolve_workspace():
        return Path(__file__).parent.parent.parent


class KnowledgeGraphEnhanced:
    """增强版知识图谱系统"""
    
    def __init__(self, workspace=None):
        # 使用 evo-agents 标准路径解析
        self.workspace = resolve_workspace() if workspace is None else Path(workspace)
        self.memory_dir = self.workspace / "memory"
        self.graph_file = self.memory_dir / "knowledge_graph.json"
        
        # 实体和关系存储
        self.entities = {}
        self.relations = []
        
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
        print(f"✅ 知识图谱已保存：{len(self.entities)} 个实体，{len(self.relations)} 条关系")
    
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
        # 检查是否已存在
        exists = any(
            r['source'] == source and r['relation'] == relation and r['target'] == target
            for r in self.relations
        )
        if not exists:
            self.relations.append({
                'source': source,
                'relation': relation,
                'target': target,
                'confidence': confidence,
                'created_at': datetime.now().isoformat()
            })
    
    def build(self, use_ai=True):
        """构建知识图谱（规则 + AI）"""
        print("🔨 开始构建知识图谱...")
        
        # 读取所有记忆文件
        memory_files = list(self.memory_dir.glob('*.md'))
        if (self.workspace / 'MEMORY.md').exists():
            memory_files.append(self.workspace / 'MEMORY.md')
        
        print(f"📄 找到 {len(memory_files)} 个记忆文件")
        
        for file_path in memory_files:
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Step 1: 规则提取（快速、准确）
                self.extract_with_patterns(content, file_path.name)
                
                # Step 2: AI 辅助提取（覆盖规则无法匹配的情况）
                if use_ai and len(content) > 200:
                    self.extract_with_llm(content, file_path.name)
                
            except Exception as e:
                print(f"⚠️ 处理文件 {file_path} 时出错：{e}")
        
        # Step 3: 关系推断
        self.infer_relations()
        
        # Step 4: 保存
        self.save()
        
        print(f"\n✅ 知识图谱构建完成！")
        print(f"   实体数：{len(self.entities)}")
        print(f"   关系数：{len(self.relations)}")
    
    def extract_with_patterns(self, content, source="unknown"):
        """使用正则表达式提取实体（基础规则）"""
        patterns = {
            'Skill': [
                r'创建了\s+[`\']?(\w+)[`\']?\s+技能',
                r'实现了\s+[`\']?(\w+)[`\']?',
                r'更新\s+[`\']?(\w+)[`\']?',
            ],
            'Project': [
                r'(\w+)\s+是阿里云推出的',
                r'基于\s+(\w+)\s+框架',
                r'项目\s*[：:]\s*(\w+)',
            ],
            'Technology': [
                r'(Python|Ollama|Bing|OpenClaw|JVS Claw|bge-m3|nomic-embed-text|Qwen)',
                r'(语义搜索 | 关键词搜索 | 嵌入模型|Rerank|重排序 | 知识图谱)',
                r'(SQLite|JSON|Markdown|API|HTTP)',
            ],
            'Agent': [
                r'Agent[：:\s]+(\w+)',
                r'(main-agent|claude-code-agent|sandbox-agent|tao-admin)',
            ],
            'Decision': [
                r'决定 [：:]\s*([^\n]+)',
                r'使用\s+(\w+)\s+而非',
            ]
        }
        
        count = 0
        for entity_type, type_patterns in patterns.items():
            for pattern in type_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    if len(match.strip()) > 2:
                        self.add_entity(entity_type, match.strip(), {'source': 'pattern', 'file': source})
                        count += 1
        
        if count > 0:
            print(f"  📌 规则提取 {count} 个实体 ({source})")
    
    def extract_with_llm(self, content, source="unknown"):
        """使用本地 LLM 提取实体和关系（增强覆盖率）"""
        try:
            # 构建提示词
            prompt = f"""请从以下文本中提取重要的实体和关系。

文本内容：
{content[:2000]}

请提取：
1. 技术/工具名称（如 Python, Ollama, OpenClaw 等）
2. 项目/系统名称
3. Agent 名称
4. 重要决策或结论

输出格式（JSON）：
{{
  "entities": [
    {{"name": "实体名", "type": "Technology|Project|Skill|Agent|Decision"}}
  ],
  "relations": [
    {{"source": "实体 1", "relation": "关系描述", "target": "实体 2"}}
  ]
}}

如果没有找到明确的实体或关系，返回空数组 {{\"entities\": [], \"relations\": []}}。只返回 JSON，不要其他内容。"""
            
            # 调用 Ollama
            result = subprocess.run(
                ['ollama', 'run', 'qwen2.5:0.5b', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                llm_output = result.stdout.strip()
                
                # 清理 markdown 标记
                if llm_output.startswith('```json'):
                    llm_output = llm_output[7:]
                if llm_output.endswith('```'):
                    llm_output = llm_output[:-3]
                
                try:
                    data = json.loads(llm_output.strip())
                    
                    # 添加实体
                    for entity in data.get('entities', []):
                        name = entity.get('name', '').strip()
                        etype = entity.get('type', 'Technology')
                        if name and len(name) > 2:
                            self.add_entity(etype, name, {'source': 'llm', 'file': source})
                    
                    # 添加关系
                    for rel in data.get('relations', []):
                        src = rel.get('source', '').strip()
                        tgt = rel.get('target', '').strip()
                        relation = rel.get('relation', '').strip()
                        if src and tgt and relation:
                            self.add_relation(src, relation, tgt, confidence=0.7)
                    
                    entity_count = len(data.get('entities', []))
                    if entity_count > 0:
                        print(f"  🤖 AI 提取 {entity_count} 个实体 ({source})")
                        
                except json.JSONDecodeError:
                    pass
                    
        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass  # LLM 提取失败不影响整体流程
    
    def infer_relations(self):
        """推断隐含关系（传递闭包等）"""
        new_relations = []
        
        # 传递闭包：A→B, B→C ⇒ A→C
        for r1 in self.relations:
            for r2 in self.relations:
                if r1['target'] == r2['source']:
                    # 检查是否已存在
                    exists = any(
                        r['source'] == r1['source'] and 
                        r['target'] == r2['target']
                        for r in self.relations
                    )
                    if not exists and r1['source'] != r2['target']:
                        new_relations.append({
                            'source': r1['source'],
                            'relation': f"{r1['relation']}→{r2['relation']}",
                            'target': r2['target'],
                            'confidence': 0.6,
                            'inferred': True,
                            'created_at': datetime.now().isoformat()
                        })
        
        # 添加新推断的关系
        for rel in new_relations:
            self.relations.append(rel)
        
        if new_relations:
            print(f"  🔍 推断出 {len(new_relations)} 条隐含关系")
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📊 知识图谱统计")
        print("=" * 50)
        
        # 按类型统计实体
        type_counts = defaultdict(int)
        for entity in self.entities.values():
            type_counts[entity['type']] += 1
        
        print("\n实体类型分布:")
        for etype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {etype}: {count}")
        
        # 显示高频实体
        print("\nTop 10 高频实体:")
        sorted_entities = sorted(
            self.entities.values(), 
            key=lambda x: -x.get('mentions', 0)
        )[:10]
        for ent in sorted_entities:
            print(f"  {ent['name']} ({ent['type']}): {ent.get('mentions', 0)} 次")
        
        # 显示关系示例
        if self.relations:
            print(f"\n关系示例（前 5 条）:")
            for rel in self.relations[:5]:
                inferred = " (推断)" if rel.get('inferred') else ""
                print(f"  {rel['source']} ──{rel['relation']}──> {rel['target']}{inferred}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='知识图谱构建器（增强版）')
    parser.add_argument('--no-ai', action='store_true', help='不使用 AI 提取（仅规则）')
    parser.add_argument('--stats', action='store_true', help='只显示统计信息')
    
    args = parser.parse_args()
    
    kg = KnowledgeGraphEnhanced()
    
    if args.stats:
        kg.show_stats()
    else:
        kg.build(use_ai=not args.no_ai)


if __name__ == '__main__':
    main()
