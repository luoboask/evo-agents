# -*- coding: utf-8 -*-
"""
Memory Hub - 记忆中心 v2.0
支持 Agent 隔离 + 会话隔离（独立表）

架构:
- shared_memories 表 - 共享记忆（所有会话可见）
- session_memories 表 - 会话记忆（独立表，每会话最多 50 条）
"""

from pathlib import Path
from path_utils import resolve_workspace
from typing import List, Dict, Optional

try:
    from .storage import StorageManager
    from .knowledge import KnowledgeInterface
    from .evaluation import EvaluationInterface
    from .session_manager import SessionManager
    from .session_storage import SessionMemoryStorage
except ImportError:
    from storage import StorageManager
    from knowledge import KnowledgeInterface
    from evaluation import EvaluationInterface
    from session_manager import SessionManager
    from session_storage import SessionMemoryStorage


class MemoryHub:
    """记忆中心 - 统一管理所有记忆相关操作
    
    支持两种隔离级别:
    1. Agent 隔离 - 不同 Agent 有独立的数据目录
    2. 会话隔离 - 会话记忆独立表存储（每会话最多 50 条）
    """
    
    def __init__(self, agent_name: str, session_id: str = None, workspace_root: Path = None):
        """
        初始化 MemoryHub
        
        Args:
            agent_name: Agent 名称（用于数据隔离）
            session_id: 会话 ID（可选，用于会话隔离）
            workspace_root: Workspace 路径（可选，默认自动查找）
        """
        self.agent_name = agent_name
        self.session_id = session_id
        self.workspace_root = workspace_root or resolve_workspace()
        
        # 数据路径
        self.data_path = self.workspace_root / 'data' / agent_name
        self.memory_path = self.data_path / 'memory'
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # 初始化子模块
        # shared_storage: 共享记忆（旧表，无 session_id 限制）
        self.shared_storage = StorageManager(self.memory_path)
        # session_storage: 会话记忆（新表，每会话最多 50 条）
        self.session_storage = SessionMemoryStorage(self.memory_path)
        self.session_manager = SessionManager(self.memory_path)
        self.knowledge = KnowledgeInterface(self)
        self.evaluation = EvaluationInterface(self)
    
    # ───────────────────────────────────────────────────────
    # 共享记忆操作（原始接口，无 session_id）
    # ───────────────────────────────────────────────────────
    
    def add(self, 
            content: str, 
            memory_type: str = 'observation',
            importance: float = 5.0,
            tags: List[str] = None,
            metadata: Dict = None) -> int:
        """添加共享记忆（原始接口）"""
        return self.shared_storage.add_memory(
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
        """搜索共享记忆（原始接口）"""
        return self.shared_storage.search_memories(
            query=query,
            top_k=top_k,
            memory_type=memory_type,
            semantic=semantic
        )
    
    # ───────────────────────────────────────────────────────
    # 会话记忆操作（独立表，每会话最多 50 条）
    # ───────────────────────────────────────────────────────
    
    def add_session(self,
                    content: str,
                    memory_type: str = 'observation',
                    importance: float = 5.0,
                    tags: List[str] = None,
                    metadata: Dict = None,
                    session_id: str = None) -> int:
        """
        添加会话记忆（自动清理超出 50 条的旧记录）
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性
            tags: 标签列表
            metadata: 元数据
            session_id: 会话 ID（None 表示使用当前会话）
        """
        effective_session_id = session_id or self.session_id
        if not effective_session_id:
            raise ValueError("必须指定 session_id 或先设置当前会话")
        
        return self.session_storage.add_memory(
            session_id=effective_session_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags,
            metadata=metadata
        )
    
    def search_session(self,
                       query: str,
                       top_k: int = 5,
                       memory_type: Optional[str] = None,
                       session_id: str = None,
                       semantic: bool = False) -> List[Dict]:
        """
        搜索会话记忆
        
        Args:
            query: 搜索查询
            top_k: 返回数量
            memory_type: 记忆类型过滤
            session_id: 会话 ID（None 表示使用当前会话）
            semantic: 是否使用语义搜索
        """
        effective_session_id = session_id or self.session_id
        if not effective_session_id:
            raise ValueError("必须指定 session_id 或先设置当前会话")
        
        return self.session_storage.search_memories(
            session_id=effective_session_id,
            top_k=top_k,
            memory_type=memory_type,
            semantic=semantic
        )
    
    def get_session_stats(self, session_id: str = None) -> Dict:
        """获取会话统计"""
        effective_session_id = session_id or self.session_id
        if not effective_session_id:
            return {'error': 'No session ID provided'}
        
        return self.session_storage.get_stats(effective_session_id)
    
    # ───────────────────────────────────────────────────────
    # 委托接口（共享记忆 - 原始接口）
    # ───────────────────────────────────────────────────────
    
    def get(self, memory_id: int) -> Optional[Dict]:
        """获取单条记忆（共享记忆）"""
        return self.shared_storage.get_memory(memory_id)
    
    def delete(self, memory_id: int) -> bool:
        """删除记忆（共享记忆）"""
        return self.shared_storage.delete_memory(memory_id)
    
    def update(self, memory_id: int, **kwargs) -> bool:
        """更新记忆（共享记忆）"""
        return self.shared_storage.update_memory(memory_id, **kwargs)
    
    def stats(self) -> Dict:
        """获取统计信息（共享记忆）"""
        return self.shared_storage.get_stats()
    
    # ───────────────────────────────────────────────────────
    # 会话管理接口
    # ───────────────────────────────────────────────────────
    
    def create_session(self,
                       session_name: str = None,
                       metadata: Dict = None) -> str:
        """创建新会话"""
        session_id = self.session_manager.create_session(session_name, metadata)
        self.session_id = session_id
        return session_id
    
    def switch_session(self, session_id: str):
        """切换到指定会话"""
        self.session_id = session_id
        self.session_manager.update_session_activity(session_id)
    
    def close_session(self, session_id: str = None):
        """关闭当前会话"""
        sid = session_id or self.session_id
        if sid:
            self.session_manager.close_session(sid)
            self.session_id = None
    
    def get_current_session(self) -> Optional[Dict]:
        """获取当前会话信息"""
        if self.session_id:
            return self.session_manager.get_session(self.session_id)
        return None
    
    def list_sessions(self,
                      active_only: bool = True,
                      limit: int = 50) -> List[Dict]:
        """列出会话"""
        return self.session_manager.list_sessions(active_only, limit)
    
    def clear_session_memories(self, session_id: str) -> int:
        """清空会话的所有记忆"""
        return self.session_storage.clear_session(session_id)
    
    # ───────────────────────────────────────────────────────
    # 评估和进化接口
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
    
    def record_evolution(self,
                        event_type: str,
                        content: str,
                        metadata: Dict = None) -> int:
        """记录进化事件（添加到共享记忆）"""
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
