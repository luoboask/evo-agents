# -*- coding: utf-8 -*-
"""
Memory Hub - 记忆中心
统一管理所有记忆相关操作
"""

import sys
import json
from pathlib import Path
from path_utils import resolve_workspace
from typing import List, Dict, Optional

try:
    from .storage import StorageManager
    from .knowledge import KnowledgeInterface
    from .evaluation import EvaluationInterface
    from .session_storage import SessionMemoryStorage
except ImportError:
    from storage import StorageManager
    from knowledge import KnowledgeInterface
    from evaluation import EvaluationInterface
    from session_storage import SessionMemoryStorage


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
        self.session_storage = SessionMemoryStorage(self.memory_path)
        self.knowledge = KnowledgeInterface(self)
        self.evaluation = EvaluationInterface(self)
        
        # RAG 配置（自动调优参数）
        self.rag_config = self._load_rag_config()
    
    def _load_rag_config(self) -> Dict:
        """加载 RAG 调优配置"""
        # 尝试从 libs/rag_eval 读取配置
        rag_config_path = self.workspace_root / 'libs' / 'rag_eval' / 'config.json'
        if rag_config_path.exists():
            try:
                with open(rag_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认配置
        return {
            'current_config': {
                'top_k': 5,
                'similarity_threshold': 0.7,
                'chunk_size': 512
            }
        }
    
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
               semantic: bool = False,
               hierarchical: bool = True,
               session_id: Optional[str] = None) -> List[Dict]:
        """
        搜索记忆（支持会话隔离）
        
        Args:
            query: 搜索关键词
            top_k: 返回数量
            memory_type: 记忆类型过滤
            semantic: 是否使用语义搜索
            hierarchical: 是否使用分层搜索（月→周→日）
            session_id: 会话 ID（用于过滤私有记忆）
        
        Returns:
            记忆列表（已过滤私有记忆）
        """
        if hierarchical:
            results = self._hierarchical_search(query, top_k, memory_type, semantic)
        else:
            results = self.storage.search_memories(
                query=query,
                top_k=top_k,
                memory_type=memory_type,
                semantic=semantic
            )
        
        # 过滤私有记忆（会话隔离）- 在 hierarchical search 后也要过滤
        print(f"DEBUG: session_id={session_id}, results={len(results)}", file=sys.stderr)
        if session_id:
            # 有会话上下文：返回公共记忆 + 本会话私有记忆
            filtered = []
            for m in results:
                metadata = m.get('metadata', '{}')
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}
                
                is_private = metadata.get('is_private', False)
                original_session_id = metadata.get('original_session_id')
                
                if not is_private or original_session_id == session_id:
                    filtered.append(m)
        else:
            # 无会话上下文：只返回公共记忆
            filtered = []
            for m in results:
                metadata = m.get('metadata', '{}')
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}
                
                print(f"DEBUG: content={m.get('content')}", file=sys.stderr)
                print(f"DEBUG: raw metadata={m.get('metadata')}", file=sys.stderr)
                print(f"DEBUG: parsed metadata={metadata}", file=sys.stderr)
                print(f"DEBUG: is_private={metadata.get('is_private', False)}", file=sys.stderr)
                if not metadata.get('is_private', False):
                    filtered.append(m)
                    print(f"DEBUG: Added to filtered", file=sys.stderr)
                else:
                    print(f"DEBUG: Skipped (private)", file=sys.stderr)
        
        print(f"DEBUG: filtered={len(filtered)}", file=sys.stderr)
        return filtered[:top_k]
    
    def _hierarchical_search(self, query: str, top_k: int, 
                            memory_type: Optional[str], 
                            semantic: bool) -> List[Dict]:
        """分层搜索：月→周→日"""
        all_results = []
        seen_ids = set()
        
        # 1. 先搜月记忆（monthly-summary）
        monthly = self.storage.search_memories(
            query=f"{query} monthly-summary",
            top_k=2,
            memory_type=memory_type,
            semantic=semantic
        )
        for r in monthly:
            if r['id'] not in seen_ids:
                all_results.append(r)
                seen_ids.add(r['id'])
        
        # 2. 再搜周记忆（weekly-summary）
        weekly = self.storage.search_memories(
            query=f"{query} weekly-summary",
            top_k=3,
            memory_type=memory_type,
            semantic=semantic
        )
        for r in weekly:
            if r['id'] not in seen_ids and len(all_results) < top_k:
                all_results.append(r)
                seen_ids.add(r['id'])
        
        # 3. 最后搜日记忆（daily-summary）
        daily = self.storage.search_memories(
            query=f"{query} daily-summary",
            top_k=5,
            memory_type=memory_type,
            semantic=semantic
        )
        for r in daily:
            if r['id'] not in seen_ids and len(all_results) < top_k:
                all_results.append(r)
                seen_ids.add(r['id'])
        
        # 4. 如果结果不足，全量搜索补充
        if len(all_results) < top_k:
            remaining = top_k - len(all_results)
            all = self.storage.search_memories(
                query=query,
                top_k=remaining,
                memory_type=memory_type,
                semantic=semantic
            )
            for r in all:
                if r['id'] not in seen_ids:
                    all_results.append(r)
                    seen_ids.add(r['id'])
        
        return all_results
    
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
    
    # ───────────────────────────────────────────────────────
    # 会话记忆接口
    # ───────────────────────────────────────────────────────
    
    def get_session_memories(self,
                              session_id: str,
                              top_k: int = None,
                              memory_type: Optional[str] = None,
                              include_all: bool = False) -> List[Dict]:
        """获取指定会话的记忆（top_k=None 时使用 RAG 配置）"""
        if top_k is None:
            top_k = self.rag_config.get('current_config', {}).get('top_k', 50)
        
        return self.session_storage.search_memories(
            session_id=session_id,
            top_k=top_k,
            memory_type=memory_type,
            include_all=include_all
        )
    
    def get_current_session_memories(self,
                                      top_k: int = None,
                                      memory_type: Optional[str] = None,
                                      include_all: bool = False) -> List[Dict]:
        """获取当前会话的记忆（自动获取最新会话，top_k=None 时使用 RAG 配置）"""
        if top_k is None:
            top_k = self.rag_config.get('current_config', {}).get('top_k', 15)
        
        sessions = self.session_storage.get_all_sessions()
        if not sessions:
            return []
        
        latest_session = sessions[0]
        return self.session_storage.search_memories(
            session_id=latest_session,
            top_k=top_k,
            memory_type=memory_type,
            include_all=include_all
        )
    
    def get_all_sessions(self) -> List[str]:
        """获取所有有记忆的会话 ID"""
        return self.session_storage.get_all_sessions()
    
    def get_session_stats(self, session_id: str) -> Dict:
        """获取会话统计"""
        return self.session_storage.get_stats(session_id)
