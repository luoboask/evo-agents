# -*- coding: utf-8 -*-
"""
质量评分插件 - 为 MemoryHub 添加知识质量评估能力
"""

from typing import Dict, List
from . import Plugin


class QualityScorerPlugin(Plugin):
    """质量评分插件"""
    
    def __init__(self, hub, config: Dict):
        super().__init__(hub, config)
        self.name = "quality_scoring"
        self.scorer = None
    
    def initialize(self):
        """初始化评分器"""
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
            
            from domain.quality_scorer import KnowledgeQualityScorer
            self.scorer = KnowledgeQualityScorer()
            print(f"✅ 质量评分已激活")
        except Exception as e:
            print(f"⚠️  质量评分初始化失败：{e}")
    
    def score(self, knowledge: Dict) -> float:
        """
        评分知识质量
        
        Args:
            knowledge: 知识字典
        
        Returns:
            质量分 (0.0-1.0)
        """
        if not self.scorer:
            self.initialize()
        
        if self.scorer:
            return self.scorer.score(knowledge)
        else:
            return 0.5
    
    def score_batch(self, knowledge_list: List[Dict]) -> List[Dict]:
        """
        批量评分
        
        Args:
            knowledge_list: 知识列表
        
        Returns:
            带评分的知识列表（已排序）
        """
        if not self.scorer:
            self.initialize()
        
        if self.scorer:
            return self.scorer.score_batch(knowledge_list)
        else:
            return knowledge_list
    
    def get_breakdown(self, knowledge: Dict) -> Dict:
        """
        获取评分明细
        
        Args:
            knowledge: 知识字典
        
        Returns:
            各维度评分明细
        """
        if not self.scorer:
            self.initialize()
        
        if self.scorer:
            return self.scorer.get_score_breakdown(knowledge)
        else:
            return {"error": "scorer not initialized"}
    
    def cleanup(self):
        """清理"""
        self.scorer = None
