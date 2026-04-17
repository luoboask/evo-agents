# -*- coding: utf-8 -*-
"""
领域专家模块 - 可选插件

使用方式:
1. 通用模式（默认）- 无需导入此模块
2. 专家模式 - from scripts.domain import DomainExpert
3. 混合模式 - 运行时根据需求加载
"""

from .domain_knowledge import DomainKnowledge
from .expert_solver import DomainExpert
from .quality_scorer import KnowledgeQualityScorer

__version__ = "1.0.0"
__all__ = [
    "DomainKnowledge",
    "DomainExpert", 
    "KnowledgeQualityScorer"
]
