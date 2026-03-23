# -*- coding: utf-8 -*-
"""
数据模型定义
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional


class MemoryType(str, Enum):
    """记忆类型枚举"""
    OBSERVATION = 'observation'    # 观察记忆
    REFLECTION = 'reflection'      # 反思记忆
    KNOWLEDGE = 'knowledge'        # 知识记忆
    GOAL = 'goal'                  # 目标记忆


@dataclass
class Memory:
    """记忆数据模型"""
    id: Optional[int] = None
    content: str = ''
    memory_type: MemoryType = MemoryType.OBSERVATION
    importance: float = 5.0
    tags: List[str] = field(default_factory=list)
    embedding: List[float] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'memory_type': self.memory_type.value,
            'importance': self.importance,
            'tags': self.tags,
            'embedding': self.embedding,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory':
        """从字典创建"""
        return cls(
            id=data.get('id'),
            content=data.get('content', ''),
            memory_type=MemoryType(data.get('memory_type', 'observation')),
            importance=data.get('importance', 5.0),
            tags=data.get('tags', []),
            embedding=data.get('embedding', []),
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            last_accessed=datetime.fromisoformat(data['last_accessed']) if data.get('last_accessed') else None
        )


@dataclass
class Knowledge:
    """知识数据模型"""
    id: str = ''
    title: str = ''
    content: str = ''
    category: str = 'general'
    tags: List[str] = field(default_factory=list)
    is_public: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Knowledge':
        """从字典创建"""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            content=data.get('content', ''),
            category=data.get('category', 'general'),
            tags=data.get('tags', []),
            is_public=data.get('is_public', False),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
