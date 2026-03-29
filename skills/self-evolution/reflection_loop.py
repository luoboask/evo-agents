#!/usr/bin/env python3
"""
反思循环模块 - 借鉴 LangGraph
多轮反思直到收敛
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ReflectionLoop:
    """反思循环（多轮反思直到收敛）"""
    
    def __init__(self, max_rounds: int = 3, convergence_threshold: float = 0.1):
        self.max_rounds = max_rounds  # 最大反思轮数
        self.convergence_threshold = convergence_threshold  # 收敛阈值（改进<10% 则停止）
        self.workspace = Path.cwd()
    
    def reflect(self, memories: List[Dict]) -> List[Dict]:
        """
        单轮反思
        
        Args:
            memories: 记忆列表
            
        Returns:
            反思后的改进建议
        """
        improvements = []
        
        # 分析记忆模式
        patterns = self._analyze_patterns(memories)
        
        # 生成改进建议
        for pattern in patterns:
            if pattern['frequency'] >= 3:  # 出现 3 次以上的模式
                improvements.append({
                    'type': 'pattern',
                    'description': f"发现模式：{pattern['description']}",
                    'suggestion': f"建议：{pattern['suggestion']}",
                    'confidence': pattern['frequency'] / len(memories)
                })
        
        return improvements
    
    def _analyze_patterns(self, memories: List[Dict]) -> List[Dict]:
        """分析记忆中的模式"""
        patterns = []
        
        # 简单实现：统计关键词频率
        keywords = {}
        for memory in memories:
            content = memory.get('content', '').lower()
            words = content.split()
            for word in words:
                if len(word) > 2:  # 忽略短词
                    keywords[word] = keywords.get(word, 0) + 1
        
        # 提取高频词作为模式
        for word, freq in keywords.items():
            if freq >= 3:
                patterns.append({
                    'description': f"频繁提及 '{word}' ({freq}次)",
                    'suggestion': f"可能需要更多关注'{word}'相关内容",
                    'frequency': freq
                })
        
        return patterns
    
    def run_loop(self, memories: List[Dict]) -> Tuple[List[Dict], int]:
        """
        运行反思循环
        
        Args:
            memories: 记忆列表
            
        Returns:
            (改进建议列表，实际反思轮数)
        """
        all_improvements = []
        prev_improvement_score = 0
        
        for round in range(self.max_rounds):
            print(f"  🔄 第 {round + 1}/{self.max_rounds} 轮反思...")
            
            # 单轮反思
            improvements = self.reflect(memories)
            
            # 计算改进分数
            improvement_score = sum(i['confidence'] for i in improvements)
            
            print(f"     发现 {len(improvements)} 条改进建议 (分数：{improvement_score:.2f})")
            
            # 检查收敛
            if improvement_score - prev_improvement_score < self.convergence_threshold:
                print(f"     ✅ 已收敛（改进 < {self.convergence_threshold}）")
                break
            
            prev_improvement_score = improvement_score
            all_improvements.extend(improvements)
        
        return all_improvements, round + 1
    
    def apply_improvements(self, improvements: List[Dict], memory_system) -> int:
        """
        应用改进建议到记忆系统
        
        Args:
            improvements: 改进建议列表
            memory_system: 记忆系统实例
            
        Returns:
            应用的改进数量
        """
        count = 0
        
        for imp in improvements:
            if imp['confidence'] >= 0.5:  # 只应用高置信度建议
                # 将改进建议记录为学习
                memory_system.record_interaction(
                    role='assistant',
                    content=f"反思发现：{imp['description']}\n建议：{imp['suggestion']}",
                    metadata={
                        'type': 'reflection_improvement',
                        'confidence': imp['confidence']
                    }
                )
                count += 1
                print(f"     ✅ 应用改进：{imp['description'][:50]}...")
        
        return count


if __name__ == '__main__':
    # 测试
    loop = ReflectionLoop(max_rounds=3)
    
    # 模拟记忆
    memories = [
        {'content': '如何配置 OpenClaw', 'type': 'question'},
        {'content': 'OpenClaw 配置教程', 'type': 'tutorial'},
        {'content': '配置 OpenClaw 的步骤', 'type': 'guide'},
        {'content': '今天天气真好', 'type': 'chat'},
        {'content': 'OpenClaw 配置问题', 'type': 'question'},
    ]
    
    print("反思循环测试:")
    improvements, rounds = loop.run_loop(memories)
    print(f"\n结果：{len(improvements)} 条改进建议，经过 {rounds} 轮反思")
