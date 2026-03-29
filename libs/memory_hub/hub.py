# -*- coding: utf-8 -*-
"""
Memory Hub - 记忆中心
统一管理所有记忆相关操作
"""

from pathlib import Path
from path_utils import resolve_workspace
from typing import List, Dict, Optional

try:
    from .storage import StorageManager
    from .knowledge import KnowledgeInterface
    from .evaluation import EvaluationInterface
except ImportError:
    from storage import StorageManager
    from knowledge import KnowledgeInterface
    from evaluation import EvaluationInterface


class MemoryHub:
    """记忆中心 - 统一管理所有记忆相关操作"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.workspace_root = resolve_workspace()
        
        # 数据路径
        self.data_path = self.workspace_root / 'data' / agent_name
        self.memory_path = self.data_path / 'memory'
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # 初始化子模块
        self.storage = StorageManager(self.memory_path)
        self.knowledge = KnowledgeInterface(self)
        self.evaluation = EvaluationInterface(self)
    
    # ───────────────────────────────────────────────────────
    # 记忆 CRUD 操作
    # ───────────────────────────────────────────────────────
    
    def add(self, 
            content: str, 
            memory_type: str = 'observation',
            importance: float = 5.0,
            tags: List[str] = None,
            metadata: Dict = None) -> int:
        """添加记忆"""
        return self.storage.add_memory(
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags,
            metadata=metadata
        )
    
    def search(self, 
               query: str, 
               top_k: int = 5,
               memory_type: Optional[str] = None,
               semantic: bool = False) -> List[Dict]:
        """搜索记忆"""
        return self.storage.search_memories(
            query=query,
            top_k=top_k,
            memory_type=memory_type,
            semantic=semantic
        )
    
    def get(self, memory_id: int) -> Optional[Dict]:
        """获取单条记忆"""
        return self.storage.get_memory(memory_id)
    
    def delete(self, memory_id: int) -> bool:
        """删除记忆"""
        return self.storage.delete_memory(memory_id)
    
    def update(self, memory_id: int, **kwargs) -> bool:
        """更新记忆"""
        return self.storage.update_memory(memory_id, **kwargs)
    
    def stats(self) -> Dict:
        """获取统计信息"""
        return self.storage.get_stats()
    
    # ───────────────────────────────────────────────────────
    # 评估接口（委托给 evaluation 模块）
    # ───────────────────────────────────────────────────────
    
    def record_evaluation(self, **kwargs):
        """记录检索评估"""
        return self.evaluation.record(**kwargs)
    
    def generate_evaluation_report(self, days: int = 7):
        """生成评估报告"""
        return self.evaluation.generate_report(days)
    
    def analyze_evaluations(self, min_samples: int = 10):
        """分析评估数据"""
        return self.evaluation.analyze(min_samples)
    
    # ───────────────────────────────────────────────────────
    # 进化记录接口
    # ───────────────────────────────────────────────────────
    
    def record_evolution(self,
                        event_type: str,
                        content: str,
                        metadata: Dict = None) -> int:
        """记录进化事件"""
        return self.add(
            content=content,
            memory_type='reflection',
            importance=8.0,
            metadata={
                'type': 'evolution',
                'event_type': event_type,
                **(metadata or {})
            }
        )
