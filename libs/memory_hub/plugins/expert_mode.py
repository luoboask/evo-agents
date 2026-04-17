# -*- coding: utf-8 -*-
"""
专家模式插件 - 为 MemoryHub 添加领域专家能力
"""

from typing import Dict, Optional
from . import Plugin


class ExpertModePlugin(Plugin):
    """专家模式插件"""
    
    def __init__(self, hub, config: Dict):
        super().__init__(hub, config)
        self.name = "expert_mode"
        self.domain = config.get('domain', 'General')
        self.expert = None
    
    def initialize(self):
        """初始化专家模式"""
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
            
            from domain.expert_solver import DomainExpert
            self.expert = DomainExpert(
                domain=self.domain,
                enable_quality_scoring=self.config.get('enable_quality_scoring', True),
                enable_active_learning=self.config.get('enable_active_learning', False)
            )
            print(f"🎓 专家模式已激活：{self.domain}")
        except Exception as e:
            print(f"⚠️  专家模式初始化失败：{e}")
    
    def solve(self, problem: str, problem_type: str = None) -> str:
        """
        使用专家能力解决问题
        
        Args:
            problem: 问题描述
            problem_type: 问题类型
        
        Returns:
            专家级回答
        """
        if not self.expert:
            self.initialize()
        
        if self.expert:
            return self.expert.solve(problem, problem_type)
        else:
            # 降级到通用模式
            return self.hub.search(problem, top_k=5)
    
    def add_knowledge(self,
                     content: str,
                     title: str,
                     category: str = "general",
                     tags: list = None,
                     source: str = None) -> str:
        """
        添加领域知识
        
        Args:
            content: 知识内容
            title: 标题
            category: 分类
            tags: 标签
            source: 来源
        
        Returns:
            知识 ID
        """
        if not self.expert:
            self.initialize()
        
        if self.expert:
            return self.expert.add_knowledge(
                content=content,
                title=title,
                category=category,
                tags=tags,
                source=source
            )
        else:
            # 降级到通用知识管理
            return self.hub.knowledge.add(
                content=content,
                title=title,
                category=category,
                tags=tags
            )
    
    def get_stats(self) -> Dict:
        """获取专家统计"""
        if self.expert:
            return self.expert.get_stats()
        else:
            return {"status": "not_initialized"}
    
    def cleanup(self):
        """清理"""
        self.expert = None
