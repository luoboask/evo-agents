# -*- coding: utf-8 -*-
"""
Self-Evolution - 自进化系统核心库

功能:
- 效果追踪 (effect_tracker)
- 方案复用 (solution_reuse)
- Embedding 缓存 (embedding_cache)
- 自动策略 (auto_strategy)
- Gene 进化 (gene_evolution)
- 元学习 (meta_learning)
- 主动学习 (active_learning_trigger)
"""

from .effect_tracker import EffectTracker
from .solution_reuse import SolutionReuse
from .embedding_cache import EmbeddingCache, get_cached_embedding
from .self_evolution_real import RealSelfEvolution

__all__ = [
    'EffectTracker',
    'SolutionReuse',
    'EmbeddingCache',
    'get_cached_embedding',
    'RealSelfEvolution',
]
