# -*- coding: utf-8 -*-
"""
分形思考增强的方案复用 - Pattern 层识别指导方案复用

功能:
1. 使用 Pattern 层识别问题类型
2. 根据模式分类优先复用方案
3. 提升方案匹配准确度
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from solution_reuse import SolutionReuse
from fractal_thinking import FractalThinkingEngine


class FractalSolutionReuse:
    """分形思考增强的方案复用器"""
    
    def __init__(self):
        self.reuse = SolutionReuse()
        self.fractal = FractalThinkingEngine()
        print(f"🧠 分形方案复用器已初始化")
    
    def solve_with_pattern(self, 
                          problem: str, 
                          problem_type: str = None,
                          use_pattern_priority: bool = True) -> Tuple[str, str]:
        """
        解决问题（使用分形思考增强）
        
        Args:
            problem: 问题描述
            problem_type: 问题类型
            use_pattern_priority: 是否使用模式优先级
        
        Returns:
            (solution, source) - source 为 'reused' 或 'new'
        """
        # 1. 先进行分形思考，识别问题模式
        pattern_info = self._analyze_pattern(problem)
        
        # 2. 根据模式优先级复用方案
        if use_pattern_priority and pattern_info:
            solution, source = self._reuse_by_pattern(
                problem=problem,
                problem_type=problem_type,
                pattern=pattern_info
            )
        else:
            # 降级到普通复用
            solution, source = self.reuse.solve_with_reuse(
                problem=problem,
                problem_type=problem_type,
                solve_func=lambda p: self._generate_solution(p)
            )
        
        # 3. 记录分形思考结果
        if source == 'reused' and pattern_info:
            self._record_pattern_usage(problem, pattern_info)
        
        return solution, source
    
    def _analyze_pattern(self, problem: str) -> Optional[Dict]:
        """
        分析问题的 Pattern 层（简化版：直接分类）
        
        Args:
            problem: 问题描述
        
        Returns:
            Pattern 信息字典
        """
        try:
            # 直接分类问题模式
            pattern_type = self._classify_pattern(problem)
            
            return {
                'level_name': 'Pattern',
                'description': f'问题模式：{pattern_type}',
                'pattern_type': pattern_type
            }
        except Exception as e:
            print(f"⚠️  分形分析失败：{e}")
        
        return None
    
    def _classify_pattern(self, pattern_description: str) -> str:
        """
        分类模式类型
        
        Args:
            pattern_description: 模式描述
        
        Returns:
            模式类型标签
        """
        desc_lower = pattern_description.lower()
        
        # 简单规则分类（可以扩展为 LLM 分类）
        if any(kw in desc_lower for kw in ['重复', 'recurring', 'again', 'repeat']):
            return 'recurring_issue'
        
        if any(kw in desc_lower for kw in ['性能', 'performance', 'slow', '快', '慢']):
            return 'performance_issue'
        
        if any(kw in desc_lower for kw in ['错误', 'error', 'bug', '异常', 'exception']):
            return 'bug_fix'
        
        if any(kw in desc_lower for kw in ['功能', 'feature', '新增', 'add']):
            return 'feature_request'
        
        return 'general'
    
    def _reuse_by_pattern(self, 
                         problem: str, 
                         problem_type: str,
                         pattern: Dict) -> Tuple[str, str]:
        """
        根据模式优先级复用方案
        
        Args:
            problem: 问题描述
            problem_type: 问题类型
            pattern: Pattern 信息
        
        Returns:
            (solution, source)
        """
        pattern_type = pattern.get('pattern_type', 'general')
        print(f"   🧩 问题模式：{pattern_type}")
        
        # 1. 优先复用同模式的方案
        similar_problems = self.reuse.find_similar_problems(
            problem=problem,
            threshold=0.6  # 降低阈值，找到更多候选
        )
        
        # 2. 按模式匹配度排序
        if similar_problems:
            # 给同模式方案加分
            for prob in similar_problems:
                prob_pattern = prob.get('metadata', {}).get('pattern_type', 'general')
                if prob_pattern == pattern_type:
                    prob['pattern_match_bonus'] = 0.3  # 同模式加分
                else:
                    prob['pattern_match_bonus'] = 0.0
            
            # 重新排序（原始相似度 + 模式加分）
            similar_problems.sort(
                key=lambda x: x.get('similarity', 0) + x.get('pattern_match_bonus', 0),
                reverse=True
            )
            
            # 3. 使用最佳匹配
            best_match = similar_problems[0]
            solution_id = best_match.get('id')
            
            # 获取方案
            solution = self._get_solution(solution_id)
            
            if solution:
                print(f"   ✅ 复用方案（模式匹配 + 语义相似）")
                return solution, 'reused'
        
        # 4. 降级：生成新方案
        print(f"   🆕 无匹配方案，生成新方案")
        new_solution = self._generate_solution(problem)
        return new_solution, 'new'
    
    def _get_solution(self, solution_id: int) -> Optional[str]:
        """获取方案内容"""
        # 简化：从 effect_tracker 获取
        try:
            import sqlite3
            conn = sqlite3.connect(self.reuse.tracker.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT solution FROM solutions WHERE id = ?',
                (solution_id,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0]
        except Exception as e:
            print(f"⚠️  获取方案失败：{e}")
        
        return None
    
    def _generate_solution(self, problem: str) -> str:
        """生成新方案"""
        # 简化：返回占位符
        return f"新方案：{problem}"
    
    def _record_pattern_usage(self, problem: str, pattern: Dict):
        """记录模式使用情况"""
        # 可以在这里记录模式使用统计，用于优化
        pass


# 快捷函数
def solve_with_pattern(problem: str, **kwargs):
    """快捷使用分形方案复用"""
    reuse = FractalSolutionReuse()
    return reuse.solve_with_pattern(problem, **kwargs)
