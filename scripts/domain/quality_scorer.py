# -*- coding: utf-8 -*-
"""
知识质量评分器 - 多维度评估知识价值

评分维度:
1. 来源权威性 (20%) - 网站/来源的可信度
2. 内容完整性 (25%) - 内容覆盖度
3. 时效性 (20%) - 发布时间
4. 用户反馈 (20%) - 成功率/满意度
5. 引用次数 (15%) - 被引用频率
"""

import re
from datetime import datetime
from typing import Dict, List


class KnowledgeQualityScorer:
    """知识质量评分器"""
    
    def __init__(self):
        # 权威网站列表（示例）
        self.authoritative_domains = {
            'high': [
                'github.com', 'stackoverflow.com', 'medium.com',
                'wikipedia.org', 'docs.python.org', 'realpython.com',
                'gov.cn', 'edu.cn', 'acm.org', 'ieee.org'
            ],
            'medium': [
                'zhihu.com', 'csdn.net', 'juejin.cn', 'segmentfault.com',
                'blog.csdn.net', 'cnblogs.com'
            ]
        }
        
        # 评分权重
        self.weights = {
            'authority': 0.20,    # 来源权威性
            'completeness': 0.25, # 内容完整性
            'timeliness': 0.20,   # 时效性
            'feedback': 0.20,     # 用户反馈
            'citation': 0.15      # 引用次数
        }
    
    def score(self, knowledge: Dict) -> float:
        """
        计算知识质量分
        
        Args:
            knowledge: 知识字典（包含 content, source, created_at 等）
        
        Returns:
            质量分 (0.0-1.0)
        """
        scores = {}
        
        # 1. 来源权威性
        scores['authority'] = self._score_authority(knowledge.get('source', ''))
        
        # 2. 内容完整性
        scores['completeness'] = self._score_completeness(knowledge.get('content', ''))
        
        # 3. 时效性
        scores['timeliness'] = self._score_timeliness(knowledge.get('created_at'))
        
        # 4. 用户反馈
        scores['feedback'] = self._score_feedback(knowledge)
        
        # 5. 引用次数
        scores['citation'] = self._score_citation(knowledge.get('citation_count', 0))
        
        # 加权平均
        total_score = sum(
            scores[dim] * self.weights[dim]
            for dim in self.weights
        )
        
        return round(total_score, 3)
    
    def _score_authority(self, source: str) -> float:
        """
        评分来源权威性
        
        Args:
            source: 来源 URL 或描述
        
        Returns:
            权威性分数 (0.0-1.0)
        """
        if not source:
            return 0.5  # 未知来源，中等分数
        
        source_lower = source.lower()
        
        # 高权威网站
        for domain in self.authoritative_domains['high']:
            if domain in source_lower:
                return 0.9
        
        # 中等权威网站
        for domain in self.authoritative_domains['medium']:
            if domain in source_lower:
                return 0.7
        
        # 其他网站
        if 'http' in source_lower or 'www' in source_lower:
            return 0.5
        
        # 非网络来源（书籍、文档等）
        if any(kw in source_lower for kw in ['book', 'doc', 'paper', '官方']):
            return 0.8
        
        return 0.5
    
    def _score_completeness(self, content: str) -> float:
        """
        评分内容完整性
        
        Args:
            content: 知识内容
        
        Returns:
            完整性分数 (0.0-1.0)
        """
        if not content:
            return 0.0
        
        content_len = len(content)
        
        # 基于长度评分
        if content_len < 100:
            return 0.3
        elif content_len < 300:
            return 0.5
        elif content_len < 1000:
            return 0.7
        elif content_len < 3000:
            return 0.85
        else:
            return 0.9
    
    def _score_timeliness(self, created_at: str = None) -> float:
        """
        评分时效性
        
        Args:
            created_at: 创建时间（ISO 格式）
        
        Returns:
            时效性分数 (0.0-1.0)
        """
        if not created_at:
            return 0.5  # 未知时间，中等分数
        
        try:
            # 解析时间
            if 'T' in created_at:
                created = datetime.fromisoformat(created_at)
            else:
                created = datetime.strptime(created_at, '%Y-%m-%d')
            
            # 计算天数差
            days_old = (datetime.now() - created).days
            
            # 越新分数越高
            if days_old <= 30:
                return 1.0
            elif days_old <= 90:
                return 0.9
            elif days_old <= 180:
                return 0.8
            elif days_old <= 365:
                return 0.7
            elif days_old <= 730:
                return 0.6
            else:
                return 0.5
        
        except Exception:
            return 0.5
    
    def _score_feedback(self, knowledge: Dict) -> float:
        """
        评分用户反馈
        
        Args:
            knowledge: 知识字典
        
        Returns:
            反馈分数 (0.0-1.0)
        """
        # 如果有成功率数据
        if 'success_rate' in knowledge:
            return knowledge['success_rate']
        
        if 'success_count' in knowledge and 'failure_count' in knowledge:
            success = knowledge['success_count']
            failure = knowledge['failure_count']
            total = success + failure
            
            if total > 0:
                return success / total
        
        # 如果有用户评分
        if 'user_rating' in knowledge:
            return knowledge['user_rating'] / 5.0  # 假设 5 分制
        
        # 默认中等分数
        return 0.5
    
    def _score_citation(self, citation_count: int) -> float:
        """
        评分引用次数
        
        Args:
            citation_count: 被引用次数
        
        Returns:
            引用分数 (0.0-1.0)
        """
        if citation_count <= 0:
            return 0.5  # 无引用，中等分数
        elif citation_count <= 5:
            return 0.6
        elif citation_count <= 10:
            return 0.7
        elif citation_count <= 20:
            return 0.8
        elif citation_count <= 50:
            return 0.9
        else:
            return 1.0
    
    def score_batch(self, knowledge_list: List[Dict]) -> List[Dict]:
        """
        批量评分
        
        Args:
            knowledge_list: 知识列表
        
        Returns:
            带评分的知识列表
        """
        for knowledge in knowledge_list:
            knowledge['quality_score'] = self.score(knowledge)
        
        # 按质量分排序
        knowledge_list.sort(key=lambda x: -x.get('quality_score', 0))
        
        return knowledge_list
    
    def get_score_breakdown(self, knowledge: Dict) -> Dict:
        """
        获取评分明细
        
        Args:
            knowledge: 知识字典
        
        Returns:
            各维度评分明细
        """
        breakdown = {
            'authority': self._score_authority(knowledge.get('source', '')),
            'completeness': self._score_completeness(knowledge.get('content', '')),
            'timeliness': self._score_timeliness(knowledge.get('created_at')),
            'feedback': self._score_feedback(knowledge),
            'citation': self._score_citation(knowledge.get('citation_count', 0)),
            'weights': self.weights,
            'total': self.score(knowledge)
        }
        
        return breakdown
