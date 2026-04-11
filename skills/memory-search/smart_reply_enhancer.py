#!/usr/bin/env python3
"""
智能回复增强器 - 让 Agent 变聪明

在每次回复前自动检索记忆和元规则，并在回复中引用

用法:
    from smart_reply_enhancer import SmartReplyEnhancer
    
    enhancer = SmartReplyEnhancer('demo51-agent')
    enhanced = enhancer.enhance_response(user_message, original_response)
    print(enhanced)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))

from memory_hub import MemoryHub
from datetime import datetime


class SmartReplyEnhancer:
    """智能回复增强器"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.memory = MemoryHub(agent_name=agent_name)
    
    def enhance_response(self, user_message: str, original_response: str) -> str:
        """
        增强回复：自动检索记忆和元规则，并在回复中引用
        
        Args:
            user_message: 用户消息
            original_response: 原始回复（LLM 生成的）
        
        Returns:
            增强后的回复
        """
        # 1. 检索相关记忆
        memories = self.memory.search(user_message, top_k=3, semantic=True)
        
        # 2. 检索元规则
        rules = self.memory.search(
            "元规则 OR 原则 OR 经验 OR 最佳实践",
            top_k=3,
            memory_type='goal'
        )
        
        # 3. 如果没有检索到，返回原始回复
        if not memories and not rules:
            return original_response
        
        # 4. 构建增强回复
        enhanced = original_response
        
        # 添加历史经验
        if memories:
            enhanced += "\n\n📚 **根据历史经验：**\n"
            for i, m in enumerate(memories, 1):
                # 处理不同格式
                if isinstance(m, dict):
                    content = m.get('content', '')
                    timestamp = m.get('metadata', {}).get('timestamp', '')
                else:
                    content = str(m)
                    timestamp = ''
                
                # 清理格式
                content = content.replace('===', '').replace('---', '').strip()
                if len(content) > 100:
                    content = content[:100] + '...'
                
                # 添加时间戳
                if timestamp:
                    date = timestamp[:10]
                    enhanced += f"\n{i}. ({date}) {content}"
                else:
                    enhanced += f"\n{i}. {content}"
        
        # 添加元规则
        if rules:
            enhanced += "\n\n📜 **根据元规则：**\n"
            for i, r in enumerate(rules, 1):
                if isinstance(r, dict):
                    content = r.get('content', '')
                else:
                    content = str(r)
                
                if len(content) > 100:
                    content = content[:100] + '...'
                enhanced += f"\n{i}. {content}"
        
        return enhanced
    
    def should_enhance(self, user_message: str) -> bool:
        """判断是否需要增强回复"""
        
        # 触发关键词
        trigger_keywords = [
            '怎么', '如何', '什么', '哪里', '为什么',  # 疑问词
            '之前', '以前', '记得', '历史',  # 历史相关
            '配置', '使用', '优化', '解决',  # 技术相关
            '项目', '任务', '功能', 'Bug'  # 工作相关
        ]
        
        for keyword in trigger_keywords:
            if keyword in user_message:
                return True
        
        return False


# =============================================================================
# 使用示例
# =============================================================================

if __name__ == '__main__':
    enhancer = SmartReplyEnhancer('demo51-agent')
    
    # 模拟对话
    user_message = "如何优化 Python 代码性能？"
    original_response = "可以使用异步编程和缓存来提升性能。"
    
    # 判断是否需要增强
    if enhancer.should_enhance(user_message):
        enhanced = enhancer.enhance_response(user_message, original_response)
        print("📤 用户：", user_message)
        print("\n📥 Agent:")
        print(enhanced)
    else:
        print("⚠️  不需要增强")
        print(original_response)
