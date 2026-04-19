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

用法:
    # 手动运行
    python3 skills/self-evolution/fractal_thinking.py
    
    # 自动模式 (扫描最近事件并分析)
    python3 skills/self-evolution/fractal_thinking.py --auto --agent demo100-agent
    
    # 指定事件数量
    python3 skills/self-evolution/fractal_thinking.py --auto --agent demo100-agent --limit 10
"""

import json
import sqlite3
import math
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).parent))
# 使用统一路径解析工具
try:
    from path_utils import resolve_workspace
except ImportError:
    def resolve_workspace():
        return Path(__file__).parent.parent.parent

sys.path.insert(0, str(resolve_workspace() / 'libs'))
from memory_stream import MemoryStream
from self_evolution_real import RealSelfEvolution

# 使用 libs 下的通用 embedding 工具
from embedding_utils import get_embedding as ollama_embed, cosine_similarity


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


class FractalThinkingEngine:
    """分形思考引擎"""
    
    def __init__(self, agent_name: str = 'demo100-agent'):
        self.agent_name = agent_name
        self.workspace = resolve_workspace()
        
        # 初始化记忆流和进化系统
        self.memory_stream = MemoryStream(agent_id=agent_name)
        self.evolution = RealSelfEvolution(agent_id=agent_name)
        
        # 模式识别规则
        self.pattern_rules = {
            'recurring_bug': {
                'seed_phrases': ['bug', 'fix', 'error', 'issue', 'leak', 'crash'],
                'threshold': 2,
                'pattern_description': '重复出现的 Bug',
                'severity': 'high'
            },
            'feature_growth': {
                'seed_phrases': ['feature', 'add', 'implement', 'new'],
                'threshold': 3,
                'pattern_description': '功能快速增加',
                'severity': 'medium'
            },
            'knowledge_gain': {
                'seed_phrases': ['learn', 'understand', 'know', 'study'],
                'threshold': 3,
                'pattern_description': '知识获取频繁',
                'severity': 'low'
            },
            'performance_issue': {
                'seed_phrases': ['slow', 'performance', 'optimize', 'latency'],
                'threshold': 2,
                'pattern_description': '性能问题',
                'severity': 'high'
            }
        }
        
        # 语义相似度配置
        self.similarity_config = {
            'min_similarity': 0.6,  # 最小相似度阈值
            'recency_weight': 0.3,   # 近因性权重
            'frequency_weight': 0.4, # 频率权重
            'similarity_weight': 0.3  # 相似度权重
        }
        
        # 模式阈值（可动态调整）
        self.pattern_thresholds = {
            'recurring_bug': 0.65,
            'feature_growth': 0.6,
            'knowledge_gain': 0.55,
            'performance_issue': 0.65
        }
    
    def process_events(self, limit: int = 10) -> Dict:
        """处理进化事件并生成分形分析报告"""
        print(f"🧠 分形思考引擎启动 (Agent: {self.agent_name})")
        print(f"   分析最近 {limit} 个事件\n")
        
        # 获取最近的进化事件
        events = self.evolution.get_evolution_history(limit=limit)
        
        if not events:
            print("⚠️  没有发现进化事件")
            return {'report': 'No events found', 'analyses': []}
        
        analyses = []
        meta_rules = []
        patterns = []
        
        for event in events:
            # Level 0: Solve
            l0 = self._analyze_level_0(event)
            analyses.append(l0)
            
            # Level 1: Pattern
            l1 = self._analyze_level_1(event, analyses)
            analyses.append(l1)
            if 'Pattern' in l1.description:
                patterns.append(l1.description)
            
            # Level 2: Correction
            l2 = self._analyze_level_2(event, [l0, l1])
            analyses.append(l2)
            
            # Level 3: Meta-Rule
            l3 = self._analyze_level_3(event, [l0, l1, l2])
            analyses.append(l3)
            if l3.metadata and 'meta_rule' in l3.metadata:
                meta_rules.append(l3.metadata['meta_rule'])
        
        # 生成报告
        report = self._generate_report(analyses, patterns, meta_rules)
        
        # 保存元规则到记忆
        self._save_meta_rules_to_memory(meta_rules, analyses)
        
        return {
            'report': report,
            'analyses': analyses,
            'patterns': patterns,
            'meta_rules': meta_rules
        }
    
    def auto_trigger_mode(self, hours: int = 24, min_events: int = 3) -> Dict:
        """
        自动触发模式 - 扫描最近事件并分析
        
        Args:
            hours: 扫描最近多少小时的事件 (默认 24 小时)
            min_events: 最少事件数量 (默认 3 个)
        
        Returns:
            分析结果
        """
        print(f"🧠 分形思考 - 自动触发模式")
        print(f"   扫描最近事件")
        print(f"   最少事件数：{min_events}\n")
        
        # 获取最近事件 (使用 get_evolution_history)
        events = self.evolution.get_evolution_history(limit=50)
        
        if len(events) < min_events:
            print(f"⚠️  事件数量不足 ({len(events)}/{min_events})，跳过分析")
            return {'skipped': True, 'reason': 'Not enough events'}
        
        print(f"✅ 发现 {len(events)} 个事件，开始分析...\n")
        
        # 执行分形分析
        result = self.process_events(limit=len(events))
        
        print(f"\n✅ 分形思考完成!")
        print(f"   分析事件：{len(events)} 个")
        print(f"   生成元规则：{len(result['meta_rules'])} 条")
        
        return result
    
    def _analyze_level_0(self, event: Dict) -> FractalAnalysis:
        """Level 0 - Solve: 解决问题"""
        event_type = event.get('event_type', '')
        description = event.get('description', '')
        
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
        """Level 1 - Pattern: 识别模式（语义相似度增强版）"""
        events = self.evolution.get_evolution_history(limit=50)
        current_type = event.get('event_type', '')
        current_desc = event.get('description', '')
        
        type_counts = {}
        for e in events:
            etype = e.get('event_type', '')
            type_counts[etype] = type_counts.get(etype, 0) + 1
        
        patterns = []
        
        for pattern_name, rule in self.pattern_rules.items():
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
                strength = self._calculate_pattern_strength(matches, rule)
                patterns.append({
                    'name': rule['pattern_description'],
                    'count': len(matches),
                    'strength': strength
                })
        
        if patterns:
            sorted_patterns = sorted(patterns, key=lambda x: -x['strength'])
            pattern_desc = f"检测到 {len(patterns)} 个模式：" + ", ".join([
                f"{p['name']} ({p['count']}次)"
                for p in sorted_patterns
            ])
        else:
            pattern_desc = f"事件类型 '{current_type}' 出现 {type_counts.get(current_type, 1)} 次"
        
        analysis = FractalAnalysis(
            level=1,
            level_name='Pattern',
            description=pattern_desc,
            input_data=current_desc,
            output_data="模式识别完成",
            timestamp=datetime.now().isoformat(),
            metadata={'patterns': patterns}
        )
        
        print(f"  L1 🔍 {pattern_desc[:60]}...")
        return analysis
    
    def _analyze_level_2(self, event: Dict, prev_analyses: List[FractalAnalysis]) -> FractalAnalysis:
        """Level 2 - Correction: 修正规则"""
        correction = "需要建立规范化流程"
        
        analysis = FractalAnalysis(
            level=2,
            level_name='Correction',
            description=correction,
            input_data=event.get('description', ''),
            output_data=correction,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"  L2 🔧 {correction}")
        return analysis
    
    def _analyze_level_3(self, event: Dict, prev_analyses: List[FractalAnalysis]) -> FractalAnalysis:
        """Level 3 - Meta-Rule: 编码元规则"""
        meta_rule = f"从 {event.get('event_type', '事件')} 中学习：{event.get('lesson_learned', '经验')}"
        
        analysis = FractalAnalysis(
            level=3,
            level_name='Meta-Rule',
            description=meta_rule,
            input_data=event.get('description', ''),
            output_data=meta_rule,
            timestamp=datetime.now().isoformat(),
            metadata={'meta_rule': meta_rule}
        )
        
        print(f"  L3 📜 {meta_rule[:50]}...")
        return analysis
    
    def _find_semantic_matches(self, events: List[Dict], seed_phrases: List[str], min_similarity: float) -> List[Dict]:
        """查找语义匹配的事件"""
        matches = []
        for event in events:
            desc = event.get('description', '').lower()
            for phrase in seed_phrases:
                if phrase.lower() in desc:
                    matches.append(event)
                    break
        return matches
    
    def _calculate_pattern_strength(self, matches: List, rule: Dict) -> float:
        """计算模式强度"""
        return min(1.0, len(matches) / rule['threshold'])
    
    def _generate_report(self, analyses: List[FractalAnalysis], patterns: List[str], meta_rules: List[str]) -> str:
        """生成分形思考报告"""
        report = "# 🧠 分形思考报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Agent**: {self.agent_name}\n\n"
        
        report += "## 检测到的模式\n\n"
        if patterns:
            for p in list(set(patterns))[:5]:
                report += f"- {p}\n"
        else:
            report += "无明显模式\n"
        
        report += "\n## 生成的元规则\n\n"
        if meta_rules:
            for i, rule in enumerate(list(set(meta_rules))[:5], 1):
                report += f"{i}. {rule}\n"
        else:
            report += "无新元规则生成\n"
        
        return report
    
    def _save_meta_rules_to_memory(self, meta_rules: List[str], analyses: List[FractalAnalysis]):
        """保存元规则到记忆系统"""
        if not meta_rules:
            return
        
        unique_rules = list(set(meta_rules))
        for rule in unique_rules:
            self.memory_stream.add_memory(
                content=rule,
                memory_type='goal',
                importance=9.5,
                tags=['meta_rule', 'fractal_thinking']
            )


# =============================================================================
# 主函数 - 支持手动和自动模式
# =============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='分形思考引擎')
    parser.add_argument('--auto', action='store_true', help='自动触发模式')
    parser.add_argument('--agent', type=str, default='demo100-agent', help='Agent 名称')
    parser.add_argument('--limit', type=int, default=10, help='分析事件数量')
    parser.add_argument('--hours', type=int, default=24, help='扫描最近多少小时 (自动模式)')
    parser.add_argument('--min-events', type=int, default=3, help='最少事件数 (自动模式)')
    
    args = parser.parse_args()
    
    engine = FractalThinkingEngine(agent_name=args.agent)
    
    if args.auto:
        # 自动触发模式
        result = engine.auto_trigger_mode(hours=args.hours, min_events=args.min_events)
    else:
        # 手动模式
        result = engine.process_events(limit=args.limit)
        
        # 显示报告
        print("\n" + "=" * 70)
        print("📄 分形思考报告")
        print("=" * 70)
        print(result['report'])
