#!/usr/bin/env python3
"""
解决方案复用器 - 优先复用历史方案，避免重复思考

核心功能:
- 语义级问题匹配
- 选择最佳历史方案
- 自动记录使用效果
"""

import sys
import math
import urllib.request
import json
from pathlib import Path
from typing import Optional, Tuple, List

sys.path.insert(0, str(Path(__file__).parent))

from effect_tracker import EffectTracker

# 使用本地 embedding_cache（不是 libs/memory_hub 的）
_embedding_cache_path = str(Path(__file__).parent)
if _embedding_cache_path not in sys.path:
    sys.path.insert(0, _embedding_cache_path)

# 强制使用本地模块
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "local_embedding_cache",
    Path(__file__).parent / "embedding_cache.py"
)
_local_cache_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_local_cache_module)
get_cached_embedding = _local_cache_module.get_cached_embedding


def get_embedding(text: str) -> List[float]:
    """获取 Ollama embedding (带缓存)"""
    return get_cached_embedding(text)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算余弦相似度"""
    if not a or not b:
        return 0.0
    
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


class SolutionReuse:
    """解决方案复用器"""
    
    def __init__(self, agent_name: str = "default"):
        self.tracker = EffectTracker(agent_name=agent_name)
    
    def find_similar_problems(self, 
                             problem: str, 
                             threshold: float = 0.7) -> List[dict]:
        """查找类似问题 (语义级)"""
        # 获取问题的 embedding
        problem_embedding = get_embedding(problem)
        
        if not problem_embedding:
            return []
        
        # 从数据库获取所有方案
        import sqlite3
        conn = sqlite3.connect(self.tracker.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, problem_description, problem_type FROM solutions')
        rows = cursor.fetchall()
        conn.close()
        
        # 计算语义相似度
        similar = []
        for row in rows:
            solution_id, desc, problem_type = row
            desc_embedding = get_embedding(desc)
            
            if desc_embedding:
                similarity = cosine_similarity(problem_embedding, desc_embedding)
                
                if similarity >= threshold:
                    similar.append({
                        'id': solution_id,
                        'problem_type': problem_type,
                        'similarity': similarity
                    })
        
        # 按相似度排序
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similar
    
    def get_best_solution(self, problem: str) -> Optional[dict]:
        """获取最佳解决方案"""
        similar = self.find_similar_problems(problem, threshold=0.7)
        
        if not similar:
            return None
        
        # 选择成功率最高的
        best = None
        best_score = 0
        
        for s in similar:
            # 获取详细统计
            import sqlite3
            conn = sqlite3.connect(self.tracker.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT success_count, failure_count FROM solutions 
                WHERE id = ?
            ''', (s['id'],))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                success_count, failure_count = row
                # 计算成功率 (平滑处理)
                score = success_count / (success_count + failure_count + 1)
                
                # 综合相似度和成功率
                combined_score = s['similarity'] * 0.4 + score * 0.6
                
                if combined_score > best_score:
                    best_score = combined_score
                    best = s
        
        # 只有成功率足够高才复用
        if best and best_score >= 0.6:
            # 获取完整方案
            import sqlite3
            conn = sqlite3.connect(self.tracker.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM solutions WHERE id = ?', (best['id'],))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                print(f"✅ 找到历史方案：{best['problem_type']} " +
                      f"(相似度 {best['similarity']:.1%}, " +
                      f"成功率 {best_score:.1%})")
                return self.tracker._row_to_dict(row)
        
        return None
    
    def solve_with_reuse(self, 
                        problem: str, 
                        problem_type: str,
                        solve_func) -> Tuple[str, str]:
        """
        解决问题 (优先复用)
        
        Args:
            problem: 问题描述
            problem_type: 问题类型
            solve_func: 解决函数 (当无历史方案时调用)
        
        Returns:
            (solution, source) - source 为 'reused' 或 'new'
        """
        # 1. 尝试复用历史方案
        solution_record = self.get_best_solution(problem)
        
        if solution_record:
            # 标记为已使用 (成功)
            self.tracker.mark_used(problem, success=True, context='reused')
            return solution_record['solution'], 'reused'
        
        # 2. 无历史记录，重新思考
        solution = solve_func(problem)
        
        # 记录新方案
        self.tracker.record_solution(problem, problem_type, solution)
        
        return solution, 'new'


# 集成示例
if __name__ == '__main__':
    reuse = SolutionReuse()
    
    # 示例：解决问题
    def my_solver(problem):
        # 这里调用分形思考
        from fractal_thinking import run_fractal_thinking
        return run_fractal_thinking(problem)
    
    problem = "API 调用频繁超时"
    solution, source = reuse.solve_with_reuse(
        problem=problem,
        problem_type="API 性能",
        solve_func=my_solver
    )
    
    print(f"解决方案来源：{source}")
    print(f"方案：{solution[:200]}...")
