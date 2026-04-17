#!/usr/bin/env python3
"""
分形思考引擎 v2 - 优化版

优化方向：
1. 更准确的模式检测（分析根本原因、时间分布、文件聚集）
2. 更有用的元规则（具体、可操作、带条件）
3. 更智能的关联检索（语义 + 上下文）
4. 更主动的提醒（临界点警告、定期回顾）
"""

import json
import sqlite3
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import sys

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))

from memory_stream import MemoryStream
from self_evolution_real import RealSelfEvolution
from embedding_utils import get_embedding, cosine_similarity


@dataclass
class FractalAnalysis:
    """分形分析结果"""
    level: int
    level_name: str
    description: str
    input_data: str
    output_data: str
    timestamp: str
    confidence: float = 1.0  # 置信度
    metadata: Dict = None
    
    def to_dict(self):
        return asdict(self)


class FractalThinkingEngineV2:
    """分形思考引擎 v2 - 优化版"""
    
    def __init__(self):
        self.memory_stream = MemoryStream()
        self.evolution = RealSelfEvolution()
        
        # 模式识别规则（优化版 - 代码 + 通用领域）
        self.pattern_rules = {
            # ===== 代码领域 =====
            'recurring_bug': {
                'seed_phrases': ['修复 Bug', '错误修复', '问题解决', '缺陷修复',
                    'BUG_FIX', '修复了', 'bug', 'fix', 'error'],
                'threshold': 2,
                'pattern_description': '重复出现的 Bug',
                'severity': 'high',
                'domain': 'code',
                'analysis': {
                    'check_root_cause': True,
                    'check_time_distribution': True,
                    'check_file_cluster': True
                }
            },
            'feature_bloat': {
                'seed_phrases': ['新增功能', '功能实现', '添加', 'FEATURE',
                    'new feature', 'added', 'implement'],
                'threshold': 3,
                'pattern_description': '功能快速增加，可能需要重构',
                'severity': 'medium',
                'domain': 'code',
                'analysis': {
                    'check_complexity': True,
                    'check_code_duplication': True
                }
            },
            'code_improvement': {
                'seed_phrases': ['优化', '改进', '重构', 'CODE_IMPROVED',
                    'optimize', 'improve', 'refactor', 'enhance'],
                'threshold': 2,
                'pattern_description': '持续代码改进，技术债务累积',
                'severity': 'medium',
                'domain': 'code',
                'analysis': {
                    'check_before_after': True,
                    'check_impact_scope': True
                }
            },
            
            # ===== 学习领域 =====
            'learning_gap': {
                'seed_phrases': ['学习', '理解', '知识获取', 'KNOWLEDGE',
                    'learned', 'understand', 'study', '调研'],
                'threshold': 3,
                'pattern_description': '知识获取频繁，可能存在知识空白',
                'severity': 'low',
                'domain': 'learning',
                'analysis': {
                    'check_topic_cluster': True,
                    'check_practice_gap': True
                }
            },
            'learning_abandon': {
                'seed_phrases': ['放弃', '没坚持', '半途而废', '停止学习',
                    'gave up', 'quit', 'stopped learning'],
                'threshold': 2,
                'pattern_description': '学习半途而废',
                'severity': 'medium',
                'domain': 'learning',
                'analysis': {
                    'check_reason': True,
                    'check_duration': True
                }
            },
            
            # ===== 工作领域 =====
            'work_delay': {
                'seed_phrases': ['迟到', '拖延', '延期', '耽误',
                    'late', 'delay', 'postpone', 'procrastinate'],
                'threshold': 2,
                'pattern_description': '工作或会议拖延',
                'severity': 'medium',
                'domain': 'work',
                'analysis': {
                    'check_root_cause': True,
                    'check_time_distribution': True
                }
            },
            'work_overload': {
                'seed_phrases': ['加班', '太忙', '工作量大', '压力大',
                    'overtime', 'overwhelmed', 'too busy', 'stress'],
                'threshold': 3,
                'pattern_description': '工作负荷过重',
                'severity': 'high',
                'domain': 'work',
                'analysis': {
                    'check_source': True,
                    'check_frequency': True
                }
            },
            
            # ===== 生活领域 =====
            'bad_habit': {
                'seed_phrases': ['熬夜', '坏习惯', '不健康', '沉迷',
                    'stay up late', 'bad habit', 'unhealthy', 'addicted'],
                'threshold': 3,
                'pattern_description': '不良生活习惯',
                'severity': 'high',
                'domain': 'life',
                'analysis': {
                    'check_trigger': True,
                    'check_frequency': True
                }
            },
            'good_habit': {
                'seed_phrases': ['坚持', '习惯', '每天', '养成',
                    'persist', 'habit', 'daily', 'formed'],
                'threshold': 5,
                'pattern_description': '好习惯形成期',
                'severity': 'low',
                'domain': 'life',
                'analysis': {
                    'check_streak': True,
                    'check_benefit': True
                }
            },
            
            # ===== 通用领域 =====
            'system_evolution': {
                'seed_phrases': ['进化', '自进化', '系统改进', 'EVOLUTION',
                    'evolution', 'self-improvement', 'automated'],
                'threshold': 3,
                'pattern_description': '系统自进化活跃期',
                'severity': 'low',
                'domain': 'general',
                'analysis': {
                    'check_evolution_velocity': True,
                    'check_auto_improvement': True
                }
            }
        }
        
        # 元规则模板（更具体、可操作 - 跨领域）
        self.meta_rule_templates = {
            # ===== 代码领域 =====
            'SECURITY': [
                "所有{input_type}必须先{validation}才能用于{operation}",
                "禁止将{input_type}直接用于{dangerous_operation}",
                "{operation}必须使用{safe_method}代替{unsafe_method}"
            ],
            'COMPLEXITY': [
                "函数复杂度超过{threshold}必须拆分为多个小函数",
                "单个文件不超过{max_lines}行，超过必须拆分",
                "嵌套超过{max_depth}层必须重构为扁平结构"
            ],
            'REUSE': [
                "相同逻辑出现{count}次以上必须提取为公共模块",
                "优先复用现有模块而不是新建文件",
                "删除代码前必须确认没有引用"
            ],
            'TESTING': [
                "核心功能必须有单元测试覆盖",
                "Bug 修复后必须添加回归测试",
                "边界情况必须单独测试"
            ],
            
            # ===== 学习领域 =====
            'LEARNING_METHOD': [
                "学习新技术必须边学边做项目，不能只看不练",
                "每天学习时间不超过{max_hours}小时，避免 burnout",
                "学完一个概念后必须{practice_method}来巩固"
            ],
            'LEARNING_PERSISTENCE': [
                "放弃前必须至少坚持{min_days}天",
                "遇到困难时先尝试{attempt_count}次再求助",
                "每周必须复习{review_times}次防止遗忘"
            ],
            
            # ===== 工作领域 =====
            'TIME_MANAGEMENT': [
                "所有会议前必须预留{buffer_minutes}分钟缓冲时间",
                "重要任务必须在{deadline_hours}小时前开始准备",
                "每天必须预留{focus_hours}小时深度工作时间"
            ],
            'WORK_LOAD': [
                "连续加班不超过{max_overtime_days}天必须休息",
                "工作量超过{max_tasks}个任务时必须重新排优先级",
                "感到压力过大时必须立即{stress_relief_method}"
            ],
            
            # ===== 生活领域 =====
            'HEALTH_HABIT': [
                "每天必须保证{sleep_hours}小时睡眠",
                "睡前{no_screen_minutes}分钟不使用电子设备",
                "每周必须运动{exercise_times}次"
            ],
            'HABIT_FORMATION': [
                "新习惯必须连续坚持{min_streak_days}天才能算养成",
                "习惯中断后必须在{restart_days}天内重新开始",
                "习惯养成期间必须每天记录进展"
            ],
            
            # ===== 通用领域 =====
            'PROBLEM_SOLVING': [
                "问题出现{occurrence_count}次以上必须找根本原因",
                "解决问题后必须记录经验教训",
                "类似问题必须建立检查清单防止再犯"
            ],
            'DECISION_MAKING': [
                "重要决定必须考虑至少{option_count}个选项",
                "情绪激动时不做重要决定",
                "决定后必须设定{review_days}天后回顾效果"
            ]
        }
    
    def analyze_event(self, event: Dict) -> List[FractalAnalysis]:
        """对单个进化事件进行分形分析（优化版）"""
        analyses = []
        
        # Level 0: 记录问题本身
        level0 = self._analyze_level_0(event)
        analyses.append(level0)
        
        # Level 1: 识别模式（增强版）
        level1 = self._analyze_level_1_enhanced(event, analyses)
        analyses.append(level1)
        
        # Level 2: 修正规则（增强版）
        level2 = self._analyze_level_2_enhanced(event, analyses)
        analyses.append(level2)
        
        # Level 3: 编码元规则（增强版 - 更具体）
        level3 = self._analyze_level_3_enhanced(event, analyses)
        analyses.append(level3)
        
        return analyses
    
    def _analyze_level_0(self, event: Dict) -> FractalAnalysis:
        """Level 0 - Solve: 解决问题"""
        description = event.get('description', '')
        event_type = event.get('event_type', '')
        
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
        
        return FractalAnalysis(
            level=0,
            level_name='Solve',
            description=f"问题：{problem}\n解决：{solution}",
            input_data=description,
            output_data=solution,
            timestamp=datetime.now().isoformat(),
            confidence=1.0,
            metadata={'event_type': event_type, 'problem': problem, 'solution': solution}
        )
    
    def _analyze_level_1_enhanced(self, event: Dict, prev_analyses: List) -> FractalAnalysis:
        """Level 1 - Pattern: 识别模式（增强版）"""
        events = self.evolution.get_evolution_history(limit=50)
        current_type = event.get('event_type', '')
        current_desc = event.get('description', '')
        
        patterns = []
        pattern_details = []
        
        for pattern_name, rule in self.pattern_rules.items():
            # 语义相似度匹配
            matches = self._find_semantic_matches(
                events=events,
                seed_phrases=rule['seed_phrases'],
                min_similarity=0.35
            )
            
            if len(matches) >= rule['threshold']:
                # 增强分析
                analysis_result = self._analyze_pattern_details(matches, rule)
                
                patterns.append({
                    'name': rule['pattern_description'],
                    'count': len(matches),
                    'strength': analysis_result['strength'],
                    'severity': rule.get('severity', 'medium'),
                    'root_cause': analysis_result.get('root_cause', '未知'),
                    'time_distribution': analysis_result.get('time_distribution', '均匀'),
                    'file_cluster': analysis_result.get('file_cluster', [])
                })
                
                pattern_details.append(
                    f"{rule['pattern_description']} ({len(matches)}次，"
                    f"强度{analysis_result['strength']:.2f}, "
                    f"原因：{analysis_result.get('root_cause', '未知')})"
                )
        
        if patterns:
            sorted_patterns = sorted(patterns, key=lambda x: -x['strength'])
            pattern_desc = f"检测到 {len(patterns)} 个模式：\n" + "\n".join([
                f"  - {p['name']} ({p['count']}次，强度{p['strength']:.2f}, "
                f"原因：{p.get('root_cause', '未知')})"
                for p in sorted_patterns
            ])
            insight = f"这不是孤立事件，而是{len(patterns)}个模式之一"
        else:
            pattern_desc = f"事件类型 '{current_type}' 出现较少，继续观察"
            insight = "可能是孤立事件，继续观察"
        
        return FractalAnalysis(
            level=1,
            level_name='Pattern',
            description=pattern_desc,
            input_data=current_desc,
            output_data=insight,
            timestamp=datetime.now().isoformat(),
            confidence=0.9 if patterns else 0.5,
            metadata={'patterns_detected': patterns, 'pattern_details': pattern_details}
        )
    
    def _analyze_pattern_details(self, matches: List, rule: Dict) -> Dict:
        """分析模式细节（根本原因、时间分布、文件聚集）"""
        analysis = {'strength': 0.0}
        
        # 计算强度
        strength = self._calculate_pattern_strength(matches, rule)
        analysis['strength'] = strength
        
        # 分析根本原因
        if rule['analysis'].get('check_root_cause'):
            root_causes = []
            for match in matches:
                event = match['event']
                lesson = event.get('lesson_learned', '')
                if lesson:
                    root_causes.append(lesson)
            
            if root_causes:
                # 找出最常见的根本原因
                from collections import Counter
                cause_counts = Counter(root_causes)
                most_common = cause_counts.most_common(1)[0][0]
                analysis['root_cause'] = most_common[:50] + "..." if len(most_common) > 50 else most_common
        
        # 分析时间分布
        if rule['analysis'].get('check_time_distribution'):
            times = []
            for match in matches:
                timestamp = match['event'].get('timestamp', '')
                if timestamp:
                    try:
                        times.append(datetime.fromisoformat(timestamp))
                    except:
                        pass
            
            if len(times) >= 2:
                time_span = (max(times) - min(times)).days
                if time_span <= 1:
                    analysis['time_distribution'] = '集中爆发（需要立即关注）'
                elif time_span <= 7:
                    analysis['time_distribution'] = '近期频繁（需要关注）'
                else:
                    analysis['time_distribution'] = '分散出现（持续问题）'
        
        # 分析文件聚集
        if rule['analysis'].get('check_file_cluster'):
            file_clusters = []
            for match in matches:
                event = match['event']
                files = event.get('files_changed', [])
                if files:
                    for f in files:
                        file_clusters.append(f.split('/')[-1])
            
            if file_clusters:
                from collections import Counter
                cluster_counts = Counter(file_clusters)
                hotspots = [f for f, c in cluster_counts.most_common(3) if c >= 2]
                if hotspots:
                    analysis['file_cluster'] = hotspots
        
        return analysis
    
    def _analyze_level_2_enhanced(self, event: Dict, prev_analyses: List) -> FractalAnalysis:
        """Level 2 - Correction: 修正规则（增强版）"""
        level1 = prev_analyses[1] if len(prev_analyses) > 1 else None
        patterns = level1.metadata.get('patterns_detected', []) if level1 else []
        
        rule_defects = []
        corrections = []
        
        for pattern in patterns:
            pattern_name = pattern.get('name', '')
            root_cause = pattern.get('root_cause', '')
            
            if 'Bug' in pattern_name:
                rule_defects.append(f"Bug 重复出现 → {root_cause or '测试覆盖不足或代码审查缺失'}")
                corrections.append("建立自动化测试 + 代码审查流程")
            
            if '功能快速增加' in pattern_name:
                rule_defects.append("功能快速增加 → 缺乏架构规划")
                corrections.append("定期重构 + 架构文档化")
            
            if '知识获取频繁' in pattern_name:
                rule_defects.append("频繁学习新知识 → 知识体系不完整")
                corrections.append("建立知识图谱 + 系统化学习路径")
        
        if not rule_defects:
            event_type = event.get('event_type', '')
            if 'BUG' in event_type:
                rule_defects.append("单个 Bug → 可能是边界情况未考虑")
                corrections.append("增加边界测试用例")
            elif 'FEATURE' in event_type:
                rule_defects.append("新功能 → 可能是新需求")
                corrections.append("保持当前开发节奏")
        
        defect_desc = f"规则缺陷：{rule_defects[0] if rule_defects else '无明显缺陷'}"
        correction_desc = f"修正建议：{corrections[0] if corrections else '保持当前实践'}"
        
        return FractalAnalysis(
            level=2,
            level_name='Correction',
            description=f"{defect_desc}\n{correction_desc}",
            input_data=level1.description if level1 else '',
            output_data=correction_desc if corrections else '',
            timestamp=datetime.now().isoformat(),
            confidence=0.85,
            metadata={'rule_defects': rule_defects, 'corrections': corrections}
        )
    
    def _analyze_level_3_enhanced(self, event: Dict, prev_analyses: List) -> FractalAnalysis:
        """Level 3 - Meta-Rule: 编码元规则（增强版 - 跨领域通用）"""
        level2 = prev_analyses[2] if len(prev_analyses) > 2 else None
        defects = level2.metadata.get('rule_defects', []) if level2 else []
        corrections = level2.metadata.get('corrections', []) if level2 else []
        
        # 获取事件领域
        event_type = event.get('event_type', '')
        domain = self._detect_domain(event_type, event.get('description', ''))
        
        meta_rules = []
        
        # 根据领域和缺陷类型生成具体元规则
        for defect in defects:
            # 代码领域
            if domain == 'code':
                if '测试覆盖' in defect or 'Bug 重复' in defect:
                    meta_rules.append(
                        "核心功能必须有单元测试覆盖，Bug 修复后必须添加回归测试"
                    )
                
                if '架构规划' in defect or '功能快速' in defect:
                    meta_rules.append(
                        "函数复杂度超过 10 必须拆分为多个小函数，单个文件不超过 500 行"
                    )
                
                if '输入验证' in defect or 'SQL' in defect:
                    meta_rules.append(
                        "所有用户输入必须先验证才能用于数据库查询，SQL 必须使用参数化查询"
                    )
            
            # 学习领域
            elif domain == 'learning':
                if '半途而废' in defect or '放弃' in defect:
                    meta_rules.append(
                        "学习新技术必须边学边做项目，放弃前必须至少坚持 7 天"
                    )
                
                if '知识体系' in defect or '知识获取' in defect:
                    meta_rules.append(
                        "每天学习时间不超过 4 小时，学完一个概念后必须实践巩固"
                    )
            
            # 工作领域
            elif domain == 'work':
                if '拖延' in defect or '迟到' in defect:
                    meta_rules.append(
                        "所有会议前必须预留 15 分钟缓冲时间，重要任务必须提前 24 小时准备"
                    )
                
                if '工作负荷' in defect or '加班' in defect:
                    meta_rules.append(
                        "连续加班不超过 3 天必须休息，工作量超过 5 个任务时必须重新排优先级"
                    )
            
            # 生活领域
            elif domain == 'life':
                if '熬夜' in defect or '坏习惯' in defect:
                    meta_rules.append(
                        "每天必须保证 7 小时睡眠，睡前 30 分钟不使用电子设备"
                    )
                
                if '习惯' in defect or '坚持' in defect:
                    meta_rules.append(
                        "新习惯必须连续坚持 21 天才能算养成，中断后必须在 3 天内重新开始"
                    )
            
            # 通用领域
            else:
                if '问题' in defect:
                    meta_rules.append(
                        "问题出现 3 次以上必须找根本原因，解决后必须记录经验教训"
                    )
        
        # 如果没有特定规则，使用通用规则
        if not meta_rules:
            meta_rules.append(
                "当修正错误时，限制应该与风险成比例，而非全面禁止"
            )
        
        meta_rule_text = '\n'.join(meta_rules)
        
        return FractalAnalysis(
            level=3,
            level_name='Meta-Rule',
            description=meta_rule_text,
            input_data=level2.description if level2 else '',
            output_data=meta_rules[0] if meta_rules else '',
            timestamp=datetime.now().isoformat(),
            confidence=0.9,
            metadata={
                'meta_rules': meta_rules,
                'source_defects': defects,
                'domain': domain
            }
        )
    
    def _detect_domain(self, event_type: str, description: str) -> str:
        """检测事件所属领域"""
        text = f"{event_type} {description}".lower()
        
        # 代码领域
        if any(kw in text for kw in ['bug', 'code', 'feature', 'function', 'api', '代码', '功能', '接口']):
            return 'code'
        
        # 学习领域
        if any(kw in text for kw in ['learn', 'study', '学习', '理解', '知识']):
            return 'learning'
        
        # 工作领域
        if any(kw in text for kw in ['work', 'meeting', 'late', '加班', '会议', '迟到', '工作']):
            return 'work'
        
        # 生活领域
        if any(kw in text for kw in ['sleep', 'habit', 'exercise', '熬夜', '习惯', '运动', '健康']):
            return 'life'
        
        # 默认通用
        return 'general'
    
    def _find_semantic_matches(self, events: List[Dict], seed_phrases: List[str], 
                                min_similarity: float = 0.35) -> List[Dict]:
        """基于语义相似度查找匹配事件"""
        matches = []
        
        for event in events:
            text = f"{event.get('event_type', '')} {event.get('description', '')}"
            
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
        """计算两个文本的语义相似度（使用 Ollama embedding）"""
        try:
            vec1 = get_embedding(text1)
            vec2 = get_embedding(text2)
            
            if not vec1 or not vec2:
                return self._simple_string_similarity(text1, text2)
            
            return cosine_similarity(vec1, vec2)
        except:
            return self._simple_string_similarity(text1, text2)
    
    def _simple_string_similarity(self, text1: str, text2: str) -> float:
        """降级方案：简单字符串相似度（Jaccard）"""
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        if not set1 or not set2:
            return 0.0
        return len(set1 & set2) / len(set1 | set2)
    
    def _calculate_pattern_strength(self, matches: List[Dict], rule: Dict) -> float:
        """计算模式强度（0-1）"""
        if not matches:
            return 0.0
        
        # 频率分数
        frequency_score = min(1.0, len(matches) / rule['threshold'])
        
        # 平均相似度
        avg_similarity = sum(m['similarity'] for m in matches) / len(matches)
        
        # 近因性分数
        now = datetime.now()
        recency_scores = []
        for m in matches:
            event_time = m['event'].get('timestamp', '')
            if event_time:
                try:
                    event_dt = datetime.fromisoformat(event_time)
                    hours_ago = (now - event_dt).total_seconds() / 3600
                    recency = math.exp(-hours_ago / 48)
                    recency_scores.append(recency)
                except:
                    recency_scores.append(0.5)
        
        avg_recency = sum(recency_scores) / len(recency_scores) if recency_scores else 0.5
        
        # 综合强度
        strength = (
            frequency_score * 0.4 +
            avg_similarity * 0.3 +
            avg_recency * 0.3
        )
        
        return min(1.0, max(0.0, strength))
    
    def process_events(self, limit: int = 10) -> Dict:
        """处理最近的进化事件，进行分形分析"""
        print("=" * 70)
        print("🧠 分形思考引擎 v2 - 优化版")
        print("=" * 70)
        
        events = self.evolution.get_evolution_history(limit=limit)
        
        print(f"\n📊 分析 {len(events)} 个进化事件...")
        print("=" * 70)
        
        all_analyses = []
        pattern_summary = {}
        meta_rules_found = []
        
        for i, event in enumerate(events, 1):
            print(f"\n事件 {i}/{len(events)}: {event.get('event_type', 'UNKNOWN')}")
            print(f"   {event.get('description', '')[:60]}...")
            
            analyses = self.analyze_event(event)
            all_analyses.extend(analyses)
            
            # 收集模式
            level1 = analyses[1] if len(analyses) > 1 else None
            if level1:
                patterns = level1.metadata.get('patterns_detected', [])
                for p in patterns:
                    pname = p.get('name', 'Unknown')
                    pattern_summary[pname] = pattern_summary.get(pname, 0) + 1
            
            # 收集元规则
            level3 = analyses[3] if len(analyses) > 3 else None
            if level3:
                rules = level3.metadata.get('meta_rules', [])
                meta_rules_found.extend(rules)
            
            # 存入记忆流
            for analysis in analyses:
                self.memory_stream.add_memory(
                    content=analysis.description,
                    memory_type='reflection',
                    tags=[f'Fractal_L{analysis.level}', analysis.level_name],
                    importance=8.0 if analysis.level >= 2 else 6.0,
                    metadata=analysis.to_dict()
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
            for i, rule in enumerate(unique_rules[:5], 1):
                print(f"   {i}. {rule}")
        
        return {
            'total_analyses': len(all_analyses),
            'by_level': {level: len([a for a in all_analyses if a.level == level]) for level in range(4)},
            'patterns': pattern_summary,
            'meta_rules': list(set(meta_rules_found))
        }


# 使用示例
if __name__ == '__main__':
    engine = FractalThinkingEngineV2()
    results = engine.process_events(limit=10)
    
    print("\n" + "=" * 70)
    print("✅ 分形分析完成（优化版）")
    print("=" * 70)
