# -*- coding: utf-8 -*-
"""
领域专家求解器 - 专家级问题解答

核心功能:
1. 问题分类
2. 知识检索（复用 MemoryHub）
3. 方案检索（复用 SolutionReuse）
4. 质量排序
5. 专家级回答生成
6. 效果追踪（复用 EffectTracker）
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.domain_knowledge import DomainKnowledge
from domain.quality_scorer import KnowledgeQualityScorer


class DomainExpert:
    """领域专家求解器"""
    
    def __init__(self, 
                 domain: str,
                 enable_quality_scoring: bool = True,
                 enable_active_learning: bool = False):
        """
        初始化领域专家
        
        Args:
            domain: 领域名称
            enable_quality_scoring: 启用质量评分
            enable_active_learning: 启用主动学习
        """
        self.domain = domain
        self.enable_quality_scoring = enable_quality_scoring
        self.enable_active_learning = enable_active_learning
        
        # 初始化领域知识
        self.knowledge = DomainKnowledge(domain=domain)
        
        # 初始化质量评分器（可选）
        if enable_quality_scoring:
            self.scorer = KnowledgeQualityScorer()
        else:
            self.scorer = None
        
        # 初始化效果追踪器（复用现有）
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "self-evolution"))
            from effect_tracker import EffectTracker
            self.tracker = EffectTracker()
        except ImportError:
            self.tracker = None
        
        print(f"🎓 领域专家已初始化：{domain}")
        if enable_quality_scoring:
            print(f"   ✅ 质量评分已启用")
        if enable_active_learning:
            print(f"   ✅ 主动学习已启用")
    
    def solve(self, 
              problem: str, 
              problem_type: str = None,
              use_expert_knowledge: bool = True) -> str:
        """
        解决问题（专家模式）
        
        Args:
            problem: 问题描述
            problem_type: 问题类型（可选）
            use_expert_knowledge: 是否使用领域知识
        
        Returns:
            专家级回答
        """
        print(f"🔍 专家求解：{problem[:50]}...")
        
        # 1. 问题分类
        if not problem_type:
            problem_type = self._classify_problem(problem)
        
        # 2. 检索领域知识
        expert_knowledge = []
        if use_expert_knowledge:
            expert_knowledge = self.knowledge.search(
                query=problem,
                category=None,  # 搜索所有分类
                limit=10
            )
            print(f"   📚 找到 {len(expert_knowledge)} 条领域知识")
        
        # 3. 检索通用记忆（复用 MemoryHub）
        general_memories = []
        try:
            from libs.memory_hub import MemoryHub
            hub = MemoryHub(agent_name="default")
            general_memories = hub.search(
                query=problem,
                top_k=5,
                semantic=True
            )
            print(f"   💭 找到 {len(general_memories)} 条通用记忆")
        except Exception as e:
            print(f"   ⚠️  通用记忆检索失败：{e}")
        
        # 4. 检索历史方案（复用 SolutionReuse）
        historical_solutions = []
        if self.tracker:
            try:
                from solution_reuse import SolutionReuse
                reuse = SolutionReuse()
                similar = reuse.find_similar_problems(problem, threshold=0.6)
                historical_solutions = similar
                print(f"   📝 找到 {len(historical_solutions)} 个历史方案")
            except Exception as e:
                print(f"   ⚠️  历史方案检索失败：{e}")
        
        # 5. 质量排序（如果启用）
        if self.scorer and expert_knowledge:
            for item in expert_knowledge:
                item['quality_score'] = self.scorer.score(item)
            expert_knowledge.sort(key=lambda x: -x.get('quality_score', 0))
            print(f"   ⭐ 已按质量排序")
        
        # 6. 生成专家级回答
        answer = self._generate_expert_answer(
            problem=problem,
            problem_type=problem_type,
            expert_knowledge=expert_knowledge,
            general_memories=general_memories,
            historical_solutions=historical_solutions
        )
        
        # 7. 记录效果（如果启用）
        if self.tracker:
            self.tracker.record_solution(
                problem=problem,
                problem_type=problem_type,
                solution=answer,
                gene_used="expert_knowledge_synthesis"
            )
        
        return answer
    
    def _classify_problem(self, problem: str) -> str:
        """
        问题分类
        
        简单规则分类，可扩展为 LLM 分类
        """
        problem_lower = problem.lower()
        
        # Python 异步编程相关
        if any(kw in problem_lower for kw in ['async', 'await', 'asyncio', 'eventloop', 'coroutine']):
            return "how-to-async"
        
        # 性能相关
        if any(kw in problem_lower for kw in ['性能', '优化', '慢', '快', '效率']):
            return "performance"
        
        # 错误相关
        if any(kw in problem_lower for kw in ['错误', 'error', 'exception', 'bug']):
            return "debugging"
        
        # 概念相关
        if any(kw in problem_lower for kw in ['是什么', 'what', '定义', '概念']):
            return "concept"
        
        # 默认
        return "general"
    
    def _generate_expert_answer(self,
                               problem: str,
                               problem_type: str,
                               expert_knowledge: List[Dict],
                               general_memories: List[Dict],
                               historical_solutions: List[Dict]) -> str:
        """
        生成专家级回答
        
        综合领域知识、通用记忆、历史方案
        """
        answer_parts = []
        
        # 1. 领域知识优先
        if expert_knowledge:
            answer_parts.append("【领域知识】")
            for i, item in enumerate(expert_knowledge[:3], 1):
                title = item.get('title', '未知')
                content = item.get('content', '')[:200]
                quality = item.get('quality_score', 0.5)
                answer_parts.append(f"{i}. {title} (质量：{quality:.2f})")
                answer_parts.append(f"   {content}...")
        
        # 2. 通用记忆补充
        if general_memories:
            answer_parts.append("\n【相关记忆】")
            for i, mem in enumerate(general_memories[:2], 1):
                content = mem.get('content', '')[:150]
                answer_parts.append(f"{i}. {content}...")
        
        # 3. 历史方案参考
        if historical_solutions:
            answer_parts.append("\n【历史方案】")
            for i, sol in enumerate(historical_solutions[:2], 1):
                desc = sol.get('problem_description', '')[:100]
                success_rate = sol.get('success_rate', 0)
                answer_parts.append(f"{i}. {desc}... (成功率：{success_rate:.0%})")
        
        # 4. 综合建议
        answer_parts.append("\n【专家建议】")
        if expert_knowledge:
            best = expert_knowledge[0]
            answer_parts.append(f"基于 {len(expert_knowledge)} 条领域知识，建议：")
            answer_parts.append(best.get('content', '')[:500])
        else:
            answer_parts.append("基于现有信息，建议：")
            answer_parts.append("需要进一步分析具体问题场景。")
        
        return "\n".join(answer_parts)
    
    def add_knowledge(self,
                     content: str,
                     title: str,
                     category: str = "general",
                     tags: List[str] = None,
                     source: str = None) -> str:
        """
        添加领域知识
        
        Args:
            content: 知识内容
            title: 标题
            category: 分类
            tags: 标签
            source: 来源
        
        Returns:
            知识 ID
        """
        # 计算质量分（如果启用）
        quality_score = 0.5
        if self.scorer:
            quality_score = self.scorer.score({
                'content': content,
                'source': source,
                'created_at': None
            })
        
        knowledge_id = self.knowledge.add(
            content=content,
            title=title,
            category=category,
            tags=tags,
            quality_score=quality_score,
            source=source
        )
        
        print(f"✅ 已添加领域知识：{title} (质量：{quality_score:.2f})")
        return knowledge_id
    
    def get_stats(self) -> Dict:
        """获取专家统计"""
        stats = self.knowledge.get_stats()
        
        if self.tracker:
            # 添加效果追踪统计
            stats['solutions_recorded'] = "available"
        
        stats['quality_scoring'] = self.enable_quality_scoring
        stats['active_learning'] = self.enable_active_learning
        
        return stats
