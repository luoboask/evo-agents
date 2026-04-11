#!/usr/bin/env python3
"""
OpenClaw 集成 - 在 OpenClaw 对话中自动查询记忆

这个模块会在 OpenClaw 处理用户消息前，自动检查是否需要查询记忆系统。

使用方法:
在 OpenClaw 的会话处理流程中调用:

```python
from memory_search.openclaw_integration import enhance_openclaw_context

# 在 OpenClaw 处理前
enhanced_context = enhance_openclaw_context(user_message, original_context)
```
"""

import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from auto_context import AutoContext, get_auto_context


def enhance_openclaw_context(user_message: str,
                             original_context: str = "",
                             agent_name: str = None,
                             top_k: int = 5) -> str:
    """
    增强 OpenClaw 上下文
    
    流程:
    1. 检查用户消息是否需要查询记忆
    2. 如果需要，从 memory-search 查询
    3. 将查询结果添加到上下文中
    
    Args:
        user_message: 用户消息
        original_context: OpenClaw 原始上下文
        agent_name: Agent 名称（自动检测）
        top_k: 查询数量
    
    Returns:
        增强后的上下文
    """
    # 自动检测 Agent 名称
    if not agent_name:
        # 从环境变量或配置文件读取
        config_file = Path(__file__).parent.parent.parent / '.install-config'
        if config_file.exists():
            for line in config_file.read_text().splitlines():
                if line.startswith('agent_name='):
                    agent_name = line.split('=')[1].strip()
                    break
        
        if not agent_name:
            agent_name = 'claude-code-agent'
    
    # 获取自动上下文增强器
    auto = get_auto_context(agent_name)
    
    # 增强上下文
    enhanced = auto.enhance_prompt(user_message, original_context, top_k=top_k)
    
    return enhanced


def before_respond_hook(user_message: str,
                        context: dict,
                        agent_name: str = None) -> dict:
    """
    OpenClaw 回复前钩子
    
    在 OpenClaw 回复用户前调用，自动增强上下文。
    
    用法:
    在 OpenClaw 配置中:
    ```python
    hooks = {
        'before_respond': before_respond_hook
    }
    ```
    
    Args:
        user_message: 用户消息
        context: OpenClaw 上下文（包含 system_prompt 等）
        agent_name: Agent 名称
    
    Returns:
        增强后的上下文
    """
    original_prompt = context.get('system_prompt', '')
    
    # 增强上下文
    enhanced_prompt = enhance_openclaw_context(
        user_message,
        original_prompt,
        agent_name
    )
    
    # 更新上下文
    context['system_prompt'] = enhanced_prompt
    
    return context


# 使用示例
if __name__ == '__main__':
    # 模拟 OpenClaw 上下文
    test_context = {
        'system_prompt': '你是一个有帮助的助手。',
        'session_id': 'test-123',
        'agent_name': 'claude-code-agent'
    }
    
    test_messages = [
        "如何配置定时任务？",
        "我之前说过什么？",
        "今天天气不错"
    ]
    
    print("测试 OpenClaw 集成:\n")
    
    for msg in test_messages:
        print(f"用户：{msg}")
        
        # 调用钩子
        enhanced_context = before_respond_hook(msg, test_context.copy())
        
        # 显示增强后的提示
        if enhanced_context['system_prompt'] != test_context['system_prompt']:
            print(f"✅ 上下文已增强")
            print(f"增强后:\n{enhanced_context['system_prompt'][:300]}...")
        else:
            print(f"❌ 无需增强")
        
        print("-" * 60)
