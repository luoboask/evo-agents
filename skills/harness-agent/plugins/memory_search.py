#!/usr/bin/env python3
"""
Memory Search Plugin - 记忆搜索插件

用于 Harness Agent 在对话中自动查询记忆系统。
"""

import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'memory-search'))

from unified_search import UnifiedMemorySearch


class MemorySearchPlugin:
    """记忆搜索插件"""
    
    def __init__(self, agent_name='claude-code-agent'):
        self.agent_name = agent_name
        self.search = UnifiedMemorySearch(agent_name)
        self.name = 'memory_search'
        self.description = '从记忆系统中检索相关信息'
    
    def search_memory(self, query, top_k=None, generate=False):
        """
        查询记忆
        
        Args:
            query: 搜索关键词
            top_k: 返回数量
            generate: 是否生成答案
        
        Returns:
            搜索结果或生成的答案
        """
        if generate:
            return self.search.search_and_generate(query, top_k=top_k)
        return self.search.search(query, top_k=top_k)
    
    def get_context(self, query, top_k=5):
        """
        获取上下文（用于对话）
        
        Args:
            query: 当前对话内容
            top_k: 返回数量
        
        Returns:
            格式化的上下文字符串
        """
        results = self.search.search(query, top_k=top_k)
        
        if not results:
            return ""
        
        context_parts = []
        for i, r in enumerate(results, 1):
            source = r.get('source', 'unknown')
            content = r.get('content', '')[:300]
            context_parts.append(f"[{source}] {content}")
        
        return "\n\n".join(context_parts)
    
    def should_search(self, user_message):
        """
        判断是否需要查询记忆
        
        Args:
            user_message: 用户消息
        
        Returns:
            bool
        """
        # 触发关键词
        trigger_keywords = [
            '之前', '以前', '历史', '记得', '说过', '问过',
            '配置', '怎么', '如何', '什么', '哪里',
            '项目', '系统', '任务'
        ]
        
        # 检查是否包含触发词
        return any(keyword in user_message.lower() for keyword in trigger_keywords)


# 使用示例
if __name__ == '__main__':
    plugin = MemorySearchPlugin()
    
    # 示例 1：直接搜索
    results = plugin.search_memory("记忆系统")
    print(f"找到 {len(results)} 条结果")
    
    # 示例 2：获取上下文
    context = plugin.get_context("如何配置？")
    print(f"上下文:\n{context}")
    
    # 示例 3：生成答案
    result = plugin.search_memory("如何配置定时任务？", generate=True)
    print(f"答案:\n{result['answer']}")
