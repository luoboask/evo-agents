# -*- coding: utf-8 -*-
"""
MemoryHub 插件系统 - 可选功能扩展

使用方式:
1. 通用模式 - 无需加载插件
2. 专家模式 - hub.plugins.load_plugin("expert_mode", config)
"""

from typing import Dict, Optional


class PluginManager:
    """插件管理器"""
    
    def __init__(self, hub):
        """
        初始化插件管理器
        
        Args:
            hub: MemoryHub 实例
        """
        self.hub = hub
        self.plugins = {}
        self.loaded = False
    
    def load_plugin(self, name: str, config: Dict = None):
        """
        加载插件
        
        Args:
            name: 插件名称
            config: 插件配置
        
        Returns:
            插件实例
        """
        if name == "expert_mode":
            from .expert_mode import ExpertModePlugin
            plugin = ExpertModePlugin(self.hub, config or {})
            self.plugins[name] = plugin
            print(f"✅ 已加载插件：{name}")
            return plugin
        
        elif name == "quality_scoring":
            from .quality_scorer import QualityScorerPlugin
            plugin = QualityScorerPlugin(self.hub, config or {})
            self.plugins[name] = plugin
            print(f"✅ 已加载插件：{name}")
            return plugin
        
        else:
            print(f"⚠️  未知插件：{name}")
            return None
    
    def get_plugin(self, name: str):
        """获取插件"""
        return self.plugins.get(name)
    
    def unload_plugin(self, name: str):
        """卸载插件"""
        if name in self.plugins:
            del self.plugins[name]
            print(f"✅ 已卸载插件：{name}")


# 插件基类
class Plugin:
    """插件基类"""
    
    def __init__(self, hub, config: Dict):
        self.hub = hub
        self.config = config
        self.name = "base_plugin"
    
    def initialize(self):
        """初始化插件"""
        pass
    
    def cleanup(self):
        """清理插件"""
        pass
