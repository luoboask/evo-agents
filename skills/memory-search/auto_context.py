#!/usr/bin/env python3
"""
Auto Context - 自动上下文增强

在 OpenClaw 原始记忆中查找，如果没找到，自动从 memory-search 查询。

使用场景：
- OpenClaw 对话中自动增强上下文
- 在回复用户前自动检索相关记忆
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

# 添加路径
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))
sys.path.insert(0, str(Path(__file__).parent))

from unified_search import UnifiedMemorySearch


class AutoContext:
    """自动上下文增强"""
    
    def __init__(self, agent_name='claude-code-agent'):
        self.agent_name = agent_name
        self.search = UnifiedMemorySearch(agent_name)
        
        # 触发查询的关键词
        self.trigger_keywords = [
            '之前', '以前', '历史', '记得', '说过', '问过',
            '配置', '怎么', '如何', '什么', '哪里',
            '项目', '系统', '任务', '部署', '安装',
            '为什么', '怎么办', '何时', '什么时候'
        ]
    
    def should_enhance(self, user_message: str) -> bool:
        """
        判断是否需要增强上下文
        
        Args:
            user_message: 用户消息
        
        Returns:
            bool
        """
        # 检查是否包含触发词
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in self.trigger_keywords)
    
    def get_context(self, 
                    user_message: str,
                    top_k: int = 5,
                    force: bool = False) -> str:
        """
        获取增强上下文
        
        流程:
        1. 检查是否需要增强（或强制增强）
        2. 从 memory-search 查询相关记忆
        3. 返回格式化的上下文
        
        Args:
            user_message: 用户消息
            top_k: 返回数量
            force: 是否强制查询（忽略触发词检查）
        
        Returns:
            格式化的上下文字符串
        """
        # 检查是否需要增强
        if not force and not self.should_enhance(user_message):
            return ""
        
        # 查询记忆
        results = self.search.search(user_message, top_k=top_k)
        
        if not results:
            return ""
        
        # 构建上下文
        context_parts = []
        for i, r in enumerate(results, 1):
            source = r.get('source', 'unknown')
            content = r.get('content', '')[:300]
            context_parts.append(f"[{source}] {content}")
        
        if not context_parts:
            return ""
        
        context = "\n\n".join(context_parts)
        return f"相关记忆:\n{context}"
    
    def enhance_prompt(self, 
                       user_message: str,
                       original_prompt: str = "",
                       top_k: int = 5) -> str:
        """
        增强系统提示
        
        Args:
            user_message: 用户消息
            original_prompt: 原始系统提示
            top_k: 返回数量
        
        Returns:
            增强后的系统提示
        """
        # 获取上下文
        context = self.get_context(user_message, top_k=top_k)
        
        if not context:
            return original_prompt
        
        # 构建增强提示
        if original_prompt:
            enhanced = f"{original_prompt}\n\n{context}"
        else:
            enhanced = context
        
        return enhanced


# 全局实例（方便在 OpenClaw 中使用）
_auto_context = None

def get_auto_context(agent_name='claude-code-agent') -> AutoContext:
    """获取 AutoContext 实例"""
    global _auto_context
    if _auto_context is None or _auto_context.agent_name != agent_name:
        _auto_context = AutoContext(agent_name)
    return _auto_context


def auto_enhance_context(user_message: str, 
                         original_prompt: str = "",
                         agent_name: str = 'claude-code-agent') -> str:
    """
    自动增强上下文（便捷函数）
    
    用法:
    enhanced_prompt = auto_enhance_context(user_message, system_prompt)
    
    Args:
        user_message: 用户消息
        original_prompt: 原始系统提示
        agent_name: Agent 名称
    
    Returns:
        增强后的系统提示
    """
    auto = get_auto_context(agent_name)
    return auto.enhance_prompt(user_message, original_prompt)


if __name__ == '__main__':
    # 测试
    auto = AutoContext()
    
    test_messages = [
        "如何配置定时任务？",
        "我之前说过什么？",
        "今天天气不错",
        "记忆系统怎么工作的？"
    ]
    
    for msg in test_messages:
        should = auto.should_enhance(msg)
        context = auto.get_context(msg)
        
        print(f"消息：{msg}")
        print(f"需要增强：{'✅' if should else '❌'}")
        if context:
            print(f"上下文:\n{context[:200]}...")
        print("-" * 60)
