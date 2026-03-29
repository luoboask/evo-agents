#!/usr/bin/env python3
"""
分形思考引擎 - 参考 TinkerClaw
https://github.com/globalcaos/tinkerclaw

核心思想：从问题求解到元规则编码的 4 层自动分析

Level 0 - Solve: 解决问题
Level 1 - Pattern: 识别模式（为什么这个问题存在？）
Level 2 - Correction: 修正规则（什么规则导致了问题？）
Level 3 - Meta-Rule: 编码元规则（如何防止类似问题？）

所有层级自动执行，无需人工干预。
"""

import json
import sqlite3
import math
import sys
from datetime import datetime
from pathlib import Path
from path_utils import resolve_workspace, resolve_data_dir
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).parent))

from memory_stream import MemoryStream
from self_evolution_real import RealSelfEvolution

# 使用 Ollama API 直接获取 embedding
import urllib.request
import json as json_lib

def get_embedding(text):
    """获取 Ollama embedding"""
    try:
        payload = {
            "model": "nomic-embed-text",
            "prompt": text
        }
        req = urllib.request.Request(
            'http://localhost:11434/api/embeddings',
            data=json_lib.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req, timeout=10)
        data = json_lib.loads(response.read().decode())
        return data.get('embedding', [])
    except Exception as e:
        print(f"⚠️  Embedding 失败：{e}")
        return []

def cosine_similarity(a, b):
    """计算余弦相似度"""
    if not a or not b:
        return 0.0
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


@dataclass
class FractalAnalysis:
    """分形分析结果"""
    level: int  # 0-3
    level_name: str
    description: str
    input_data: str
    output_data: str
    timestamp: str
    metadata: Dict = None
    
    def to_dict(self):
        return asdict(self)


class FractalThinkingEngine:
    """
    分形思考引擎
    
    自动从进化事件中提取：
    - Level 0: 问题本身
    - Level 1: 问题背后的模式
    - Level 2: 导致模式的规则缺陷
    - Level 3: 防止缺陷的元规则
    """
    
    def __init__(self):
        self.memory_stream = MemoryStream()
        self.evolution = RealSelfEvolution()
        
        # 分形层级定义
        self.levels = {
            0: {
                'name': 'Solve',
                'description': '解决问题',
                'question': '问题是什么？如何解决的？'
            },
            1: {
                'name': 'Pattern',
                'description': '识别模式',
                'question': '为什么这个问题存在？是孤立事件还是重复模式？'
            },
            2: {
                'name': 'Correction',
                'description': '修正规则',
                'question': '什么规则/限制导致了这个问题？如何修正？'
            },
            3: {
                'name': 'Meta-Rule',
                'description': '编码元规则',
                'question': '如何设计元规则防止类似问题再次发生？'
            }
        }
        
        # 模式识别规则 - 语义相似度版本
        self.pattern_rules = {
            'recurring_bug': {
                'seed_phrases': [
                    '修复 Bug', '错误修复', '问题解决', '缺陷修复',
                    'BUG_FIX', '修复了', 'bug', 'fix', 'error'
                ],
                'threshold': 2,
                'pattern_description': '重复出现的 Bug',
                'severity': 'high'
            },
            'feature_bloat': {
                'seed_phrases': [
                    '新增功能', '功能实现', '添加', 'FEATURE',
                    'new feature', 'added', 'implement'
                ],
                'threshold': 3,
                'pattern_description': '功能快速增加，可能需要重构',
                'severity': 'medium'
            },
            'learning_gap': {
                'seed_phrases': [
                    '学习', '理解', '知识获取', 'KNOWLEDGE',
                    'learned', 'understand', 'study', '调研'
                ],
                'threshold': 3,
                'pattern_description': '知识获取频繁，可能存在知识空白',
                'severity': 'low'
            },
            'code_improvement': {
                'seed_phrases': [
                    '优化', '改进', '重构', 'CODE_IMPROVED',
                    'optimize', 'improve', 'refactor', 'enhance'
                ],
                'threshold': 2,
                'pattern_description': '持续代码改进，技术债务累积',
                'severity': 'medium'
            },
            'system_evolution': {
                'seed_phrases': [
                    '进化', '自进化', '系统改进', 'EVOLUTION',
                    'evolution', 'self-improvement', 'automated'
                ],
                'threshold': 3,
                'pattern_description': '系统自进化活跃期',
                'severity': 'low'
            }
        }
        
        # 语义相似度配置
        self.similarity_config = {
            'use_semantic': True,      # 启用语义相似度
            'min_similarity': 0.35,    # 最小相似度阈值（降低以匹配更多）
            'weight_recency': 0.3,     # 近因性权重
            'weight_frequency': 0.4,   # 频率权重
            'weight_similarity': 0.3   # 相似度权重
        }
        
        # 各模式的相似度阈值（可单独调整）
        self.pattern_thresholds = {
            'recurring_bug': 0.35,      # Bug 相关较容易识别
            'feature_bloat': 0.30,      # 功能相关阈值稍低
            'learning_gap': 0.30,       # 学习相关
            'code_improvement': 0.35,   # 代码改进
            'system_evolution': 0.30    # 系统进化
        }
    
    def analyze_event(self, event: Dict) -> List[FractalAnalysis]:
        """
        对单个进化事件进行分形分析
        
        Returns:
            4 层分析结果列表
        """
        analyses = []
        
        # Level 0: 记录问题本身
        level0 = self._analyze_level_0(event)
        analyses.append(level0)
        
        # Level 1: 识别模式
        level1 = self._analyze_level_1(event, analyses)
        analyses.append(level1)
        
        # Level 2: 修正规则
        level2 = self._analyze_level_2(event, analyses)
        analyses.append(level2)
        
        # Level 3: 编码元规则
        level3 = self._analyze_level_3(event, analyses)
        analyses.append(level3)
        
        return analyses
    
    def _analyze_level_0(self, event: Dict) -> FractalAnalysis:
        """
        Level 0 - Solve: 解决问题
        
        输入：进化事件
        输出：问题描述和解决方案
        """
        description = event.get('description', '')
        event_type = event.get('event_type', '')
        
        # 提取问题和解决
        if 'BUG' in event_type:
            problem = f"Bug: {description}"
            solution = event.get('lesson_learned', '已修复')
        elif 'FEATURE' in event_type:
            problem = f"需求：{description}"
            solution = "功能已实现"
        elif 'IMPROVED' in event_type:
            problem = f"改进点：{description}"
            solution = "代码已优化"
        else:
            problem = description
            solution = event.get('lesson_learned', '已完成')
        
        analysis = FractalAnalysis(
            level=0,
            level_name='Solve',
            description=f"问题：{problem}\n解决：{solution}",
            input_data=description,
            output_data=solution,
            timestamp=datetime.now().isoformat(),
            metadata={
                'event_type': event_type,
                'problem': problem,
                'solution': solution
            }
        )
        
        print(f"  L0 🎯 {problem[:50]}... → {solution[:30]}...")
        return analysis
    
    def _analyze_level_1(self, event: Dict, prev_analyses: List[FractalAnalysis]) -> FractalAnalysis:
        """
        Level 1 - Pattern: 识别模式（语义相似度增强版）
        
        输入：Level 0 分析 + 历史事件
        输出：模式识别结果
        
        优化：
        1. 语义相似度替代关键词匹配
        2. 考虑近因性、频率、相似度三个维度
        3. 动态阈值调整
        """
        # 获取历史事件进行模式匹配
        events = self.evolution.get_evolution_history(limit=50)
        current_type = event.get('event_type', '')
        current_desc = event.get('description', '')
        
        # 统计同类型事件
        type_counts = {}
        for e in events:
            etype = e.get('event_type', '')
            type_counts[etype] = type_counts.get(etype, 0) + 1
        
        # 使用语义相似度检测模式
        patterns = []
        pattern_details = []
        
        for pattern_name, rule in self.pattern_rules.items():
            # 使用针对该模式的阈值
            pattern_threshold = self.pattern_thresholds.get(
                pattern_name, 
                self.similarity_config['min_similarity']
            )
            
            matches = self._find_semantic_matches(
                events=events,
                seed_phrases=rule['seed_phrases'],
                min_similarity=pattern_threshold
            )
            
            if len(matches) >= rule['threshold']:
                # 计算模式强度（0-1）
                strength = self._calculate_pattern_strength(matches, rule)
                patterns.append({
                    'name': rule['pattern_description'],
                    'count': len(matches),
                    'strength': strength,
                    'severity': rule.get('severity', 'medium')
                })
                pattern_details.append(f"{rule['pattern_description']} ({len(matches)}次，强度{strength:.2f})")
        
        # 生成模式分析
        if patterns:
            sorted_patterns = sorted(patterns, key=lambda x: -x['strength'])
            pattern_desc = f"检测到 {len(patterns)} 个模式：\n" + "\n".join([
                f"  - {p['name']} ({p['count']}次，强度{p['strength']:.2f})"
                for p in sorted_patterns
            ])
            insight = f"这不是孤立事件，而是{len(patterns)}个模式之一，最强模式强度{sorted_patterns[0]['strength']:.2f}"
        else:
            pattern_desc = f"事件类型 '{current_type}' 出现 {type_counts.get(current_type, 1)} 次"
            insight = "可能是孤立事件，继续观察"
        
        analysis = FractalAnalysis(
            level=1,
            level_name='Pattern',
            description=pattern_desc,
            input_data=event.get('description', ''),
            output_data=insight,
            timestamp=datetime.now().isoformat(),
            metadata={
                'patterns_detected': patterns,
                'type_frequency': type_counts.get(current_type, 1)
            }
        )
        
        print(f"  L1 🔍 检测到 {len(patterns)} 个模式...")
        return analysis
    
    def _find_semantic_matches(self, events: List[Dict], seed_phrases: List[str], 
                                min_similarity: float = None) -> List[Dict]:
        """
        基于语义相似度查找匹配事件
        
        Args:
            events: 事件列表
            seed_phrases: 种子短语列表
            min_similarity: 最小相似度（如果为 None，使用默认配置）
        """
        if min_similarity is None:
            min_similarity = self.similarity_config['min_similarity']
        """
        基于语义相似度查找匹配事件
        
        算法：
        1. 将 seed phrases 转换为语义向量（简化版：使用字符 n-gram 相似度）
        2. 计算每个事件与 seed phrases 的最大相似度
        3. 返回超过阈值的事件
        
        TODO: 可以集成 Ollama/本地 embedding 模型获得更好的语义理解
        """
        matches = []
        
        for event in events:
            text = f"{event.get('event_type', '')} {event.get('description', '')}"
            
            # 计算与所有 seed phrases 的最大相似度
            max_sim = 0.0
            for seed in seed_phrases:
                sim = self._calculate_text_similarity(text, seed)
                max_sim = max(max_sim, sim)
            
            if max_sim >= min_similarity:
                matches.append({
                    'event': event,
                    'similarity': max_sim,
                    'text': text
                })
        
        return matches
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度（使用 Ollama nomic-embed-text）
        
        直接使用 Ollama embedding + 余弦相似度
        """
        vec1 = get_embedding(text1)
        vec2 = get_embedding(text2)
        
        # 余弦相似度
        return cosine_similarity(vec1, vec2)
    
    def _calculate_pattern_strength(self, matches: List[Dict], rule: Dict) -> float:
        """
        计算模式强度（0-1）
        
        考虑因素：
        - 匹配数量（频率）
        - 平均相似度
        - 近因性（最近的事件权重更高）
        """
        if not matches:
            return 0.0
        
        # 1. 频率分数（归一化到 0-1）
        frequency_score = min(1.0, len(matches) / rule['threshold'])
        
        # 2. 平均相似度
        avg_similarity = sum(m['similarity'] for m in matches) / len(matches)
        
        # 3. 近因性分数（越近的事件权重越高）
        now = datetime.now()
        recency_scores = []
        for m in matches:
            event_time = m['event'].get('timestamp', '')
            if event_time:
                try:
                    event_dt = datetime.fromisoformat(event_time)
                    hours_ago = (now - event_dt).total_seconds() / 3600
                    recency = math.exp(-hours_ago / 48)  # 48 小时半衰期
                    recency_scores.append(recency)
                except:
                    recency_scores.append(0.5)
        
        avg_recency = sum(recency_scores) / len(recency_scores) if recency_scores else 0.5
        
        # 综合强度分数
        strength = (
            frequency_score * self.similarity_config['weight_frequency'] +
            avg_similarity * self.similarity_config['weight_similarity'] +
            avg_recency * self.similarity_config['weight_recency']
        )
        
        return min(1.0, max(0.0, strength))
    
    def _analyze_level_2(self, event: Dict, prev_analyses: List[FractalAnalysis]) -> FractalAnalysis:
        """
        Level 2 - Correction: 修正规则
        
        输入：Level 1 模式分析
        输出：规则缺陷识别和修正建议
        """
        level1 = prev_analyses[1] if len(prev_analyses) > 1 else None
        patterns = level1.metadata.get('patterns_detected', []) if level1 else []
        
        # 根据模式推断规则缺陷
        rule_defects = []
        corrections = []
        
        if '重复出现的 Bug' in patterns:
            rule_defects.append("Bug 重复出现 → 测试覆盖不足或代码审查缺失")
            corrections.append("建立自动化测试 + 代码审查流程")
        
        if '功能快速增加' in patterns:
            rule_defects.append("功能快速增加 → 缺乏架构规划")
            corrections.append("定期重构 + 架构文档化")
        
        if '知识获取频繁' in patterns:
            rule_defects.append("频繁学习新知识 → 知识体系不完整")
            corrections.append("建立知识图谱 + 系统化学习路径")
        
        if '持续代码改进' in patterns:
            rule_defects.append("持续改进 → 初期设计考虑不周")
            corrections.append("设计阶段增加评审 + 原型验证")
        
        # 如果没有检测到模式，从事件本身推断
        if not rule_defects:
            event_type = event.get('event_type', '')
            if 'BUG' in event_type:
                rule_defects.append("单个 Bug → 可能是边界情况未考虑")
                corrections.append("增加边界测试用例")
            elif 'FEATURE' in event_type:
                rule_defects.append("新功能 → 可能是新需求")
                corrections.append("保持当前开发节奏")
        
        # 生成规则修正分析
        if rule_defects:
            defect_desc = f"规则缺陷：{rule_defects[0]}"
            correction_desc = f"修正建议：{corrections[0]}"
        else:
            defect_desc = "未检测到明显规则缺陷"
            correction_desc = "保持当前实践"
        
        analysis = FractalAnalysis(
            level=2,
            level_name='Correction',
            description=f"{defect_desc}\n{correction_desc}",
            input_data=level1.description if level1 else '',
            output_data=correction_desc,
            timestamp=datetime.now().isoformat(),
            metadata={
                'rule_defects': rule_defects,
                'corrections': corrections
            }
        )
        
        print(f"  L2 🔧 {defect_desc[:50]}... → {corrections[0] if corrections else '保持'}...")
        return analysis
    
    def _analyze_level_3(self, event: Dict, prev_analyses: List[FractalAnalysis]) -> FractalAnalysis:
        """
        Level 3 - Meta-Rule: 编码元规则
        
        输入：Level 2 规则修正
        输出：元规则（防止类似问题的原则）
        """
        level2 = prev_analyses[2] if len(prev_analyses) > 2 else None
        defects = level2.metadata.get('rule_defects', []) if level2 else []
        corrections = level2.metadata.get('corrections', []) if level2 else []
        
        # 从规则修正生成元规则
        meta_rules = []
        
        if defects and corrections:
            # 提取通用原则
            if '测试覆盖' in str(defects):
                meta_rules.append("元规则：任何代码变更必须伴随测试更新")
            if '代码审查' in str(defects):
                meta_rules.append("元规则：重要变更需要同行评审")
            if '架构规划' in str(defects):
                meta_rules.append("元规则：功能开发前先设计架构")
            if '知识体系' in str(defects):
                meta_rules.append("元规则：学习新知识时更新知识图谱")
            if '边界情况' in str(defects):
                meta_rules.append("元规则：实现功能时先考虑边界情况")
        
        # 默认元规则（如果没有特定规则）
        if not meta_rules:
            meta_rules.append("元规则：当修正错误时，限制应该与风险成比例，而非全面禁止")
        
        # 生成元规则分析
        meta_rule_text = '\n'.join(meta_rules)
        
        analysis = FractalAnalysis(
            level=3,
            level_name='Meta-Rule',
            description=meta_rule_text,
            input_data=level2.description if level2 else '',
            output_data=meta_rules[0],
            timestamp=datetime.now().isoformat(),
            metadata={
                'meta_rules': meta_rules,
                'source_defects': defects,
                'source_corrections': corrections
            }
        )
        
        print(f"  L3 📜 {meta_rules[0][:60]}...")
        return analysis
    
    def process_events(self, limit: int = 10) -> Dict:
        """
        处理最近的进化事件，进行分形分析
        
        Returns:
            分析结果统计
        """
        print("=" * 70)
        print("🧠 分形思考引擎")
        print("=" * 70)
        
        # 获取最近的进化事件
        events = self.evolution.get_evolution_history(limit=limit)
        
        print(f"\n📊 分析 {len(events)} 个进化事件...")
        print("=" * 70)
        
        all_analyses = []
        pattern_summary = {}
        meta_rules_found = []
        
        for i, event in enumerate(events, 1):
            print(f"\n事件 {i}/{len(events)}: {event.get('event_type', 'UNKNOWN')}")
            print(f"   {event.get('description', '')[:60]}...")
            
            # 进行分形分析
            analyses = self.analyze_event(event)
            all_analyses.extend(analyses)
            
            # 收集模式
            level1 = analyses[1] if len(analyses) > 1 else None
            if level1:
                patterns = level1.metadata.get('patterns_detected', [])
                for p in patterns:
                    # p 现在是 dict，使用 pattern name 作为键
                    if isinstance(p, dict):
                        pname = p.get('name', 'Unknown')
                        pattern_summary[pname] = pattern_summary.get(pname, 0) + 1
                    else:
                        pattern_summary[p] = pattern_summary.get(p, 0) + 1
            
            # 收集元规则
            level3 = analyses[3] if len(analyses) > 3 else None
            if level3:
                rules = level3.metadata.get('meta_rules', [])
                meta_rules_found.extend(rules)
            
            # 将分析存入记忆流
            for analysis in analyses:
                # 将 metadata 内容合并到 content 中
                content = analysis.description
                if analysis.metadata:
                    if 'meta_rules' in analysis.metadata:
                        content += f" [元规则：{', '.join(analysis.metadata['meta_rules'])}]"
                
                self.memory_stream.add_memory(
                    content=content,
                    memory_type='reflection',
                    tags=[f'Fractal_L{analysis.level}', analysis.level_name],
                    importance=8.0 if analysis.level >= 2 else 6.0
                )
        
        # 生成总结
        print("\n" + "=" * 70)
        print("📊 分形分析总结")
        print("=" * 70)
        
        print(f"\n总分析数：{len(all_analyses)}")
        for level in range(4):
            count = len([a for a in all_analyses if a.level == level])
            print(f"   Level {level} ({self.levels[level]['name']}): {count}个")
        
        if pattern_summary:
            print(f"\n检测到的模式:")
            for pattern, count in sorted(pattern_summary.items(), key=lambda x: -x[1]):
                print(f"   - {pattern}: {count}次")
        
        if meta_rules_found:
            print(f"\n生成的元规则:")
            unique_rules = list(set(meta_rules_found))
            for i, rule in enumerate(unique_rules[:5], 1):  # 只显示前 5 个
                print(f"   {i}. {rule}")
        
        # 生成综合报告
        report = self._generate_fractal_report(all_analyses, pattern_summary, meta_rules_found)
        
        return {
            'total_analyses': len(all_analyses),
            'by_level': {level: len([a for a in all_analyses if a.level == level]) for level in range(4)},
            'patterns': pattern_summary,
            'meta_rules': list(set(meta_rules_found)),
            'report': report
        }
    
    def _generate_fractal_report(self, analyses: List[FractalAnalysis],
                                  patterns: Dict, meta_rules: List[str]) -> str:
        """生成分形思考报告"""
        report = f"# 分形思考报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "## 执行摘要\n\n"
        report += f"- 分析事件数：{len(set(a.input_data for a in analyses))}\n"
        report += f"- 总分析数：{len(analyses)}\n"
        report += f"- 检测模式：{len(patterns)}个\n"
        report += f"- 生成元规则：{len(set(meta_rules))}个\n\n"
        
        report += "## 检测到的模式\n\n"
        if patterns:
            for pattern, count in sorted(patterns.items(), key=lambda x: -x[1]):
                report += f"- **{pattern}**: {count}次\n"
        else:
            report += "未检测到明显模式\n"
        
        report += "\n## 生成的元规则\n\n"
        if meta_rules:
            for i, rule in enumerate(list(set(meta_rules))[:5], 1):
                report += f"{i}. {rule}\n"
        else:
            report += "无新元规则生成\n"
        
        report += "\n## 建议行动\n\n"
        if patterns:
            report += "基于检测到的模式，建议:\n"
            if '重复出现的 Bug' in patterns:
                report += "- 🔴 优先：建立自动化测试流程\n"
            if '功能快速增加' in patterns:
                report += "- 🟡 中期：进行架构重构\n"
            if '知识获取频繁' in patterns:
                report += "- 🟢 长期：建立系统化学习路径\n"
        
        return report
    
    def get_fractal_insights(self, query: str = None, limit: int = 5) -> List[Dict]:
        """
        检索分形思考的洞察
        
        Args:
            query: 可选的查询关键词
            limit: 返回数量限制
        
        Returns:
            洞察列表
        """
        # 从记忆流检索分形相关的反思
        if query:
            results = self.memory_stream.retrieve_by_relevance(query, limit=limit * 2)
        else:
            results = [
                (mem, 1.0) for mem in 
                self.memory_stream.get_memories(memory_type='reflection', limit=limit * 2)
                if 'Fractal' in str(mem.tags)
            ]
        
        insights = []
        for mem, score in results[:limit]:
            if 'Fractal' in str(mem.tags):
                insights.append({
                    'content': mem.content,
                    'level': mem.tags[0] if mem.tags else 'Unknown',
                    'importance': mem.importance,
                    'timestamp': mem.created_at
                })
        
        return insights


# 使用示例
if __name__ == '__main__':
    engine = FractalThinkingEngine()
    
    # 处理最近 5 个事件
    results = engine.process_events(limit=5)
    
    # 显示报告
    print("\n" + "=" * 70)
    print("📄 分形思考报告")
    print("=" * 70)
    print(results['report'])
    
    # 检索洞察
    print("\n" + "=" * 70)
    print("💡 分形洞察检索")
    print("=" * 70)
    insights = engine.get_fractal_insights(limit=3)
    for i, insight in enumerate(insights, 1):
        print(f"\n{i}. [{insight['level']}] 重要性：{insight['importance']}")
        print(f"   {insight['content'][:100]}...")
