#!/usr/bin/env python3
"""
自动记录会话 - Auto Record Session
自动将对话记录到混合记忆系统
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from search import IntegratedHybridMemory


def auto_record_session(user_message: str, agent_response: str, 
                        importance: float = None, auto_eval: bool = True):
    """
    自动记录会话到记忆系统
    
    Args:
        user_message: 用户消息
        agent_response: Agent 回复
        importance: 重要性（1-10），自动评估如果为 None
        auto_eval: 是否自动评估重要性
    """
    memory = IntegratedHybridMemory()
    
    # 自动评估重要性
    if auto_eval and importance is None:
        importance = _evaluate_importance(user_message, agent_response)
    
    # 记录对话
    content = f"User: {user_message}\nAgent: {agent_response}"
    
    # 添加到工作记忆
    entry = memory.record_interaction(
        role='assistant',
        content=content,
        metadata={
            'type': 'dialogue',
            'user_message': user_message,
            'agent_response': agent_response,
            'importance': importance
        }
    )
    
    print(f"✅ 自动记录对话（重要性：{importance}/10）")
    return entry


def _evaluate_importance(user_message: str, agent_response: str) -> float:
    """
    自动评估对话重要性
    
    评分标准：
    - 包含关键词（决定、记住、重要）：+3
    - 技术性问题：+2
    - 长对话（>100 字符）：+1
    - 包含代码：+2
    - 基础问题：+1
    """
    score = 5.0  # 基础分
    
    # 关键词
    important_keywords = ['决定', '记住', '重要', '必须', '一定', 'critical', 'important', 'remember']
    if any(kw in user_message.lower() for kw in important_keywords):
        score += 3
    
    # 技术问题
    tech_keywords = ['代码', '函数', 'api', '数据库', 'sql', 'python', '配置', 'error', 'bug']
    if any(kw in user_message.lower() for kw in tech_keywords):
        score += 2
    
    # 长对话
    if len(user_message) > 100 or len(agent_response) > 200:
        score += 1
    
    # 包含代码
    if '```' in user_message or '```' in agent_response:
        score += 2
    
    # 限制在 1-10 范围
    return max(1.0, min(10.0, score))


def record_search_query(query: str, results_count: int, latency_ms: float):
    """
    记录搜索查询（用于 RAG 评估）
    
    Args:
        query: 搜索查询
        results_count: 返回结果数
        latency_ms: 延迟（毫秒）
    """
    from pathlib import Path
    import json
    from datetime import datetime
    
    data_dir = Path(__file__).parent.parent.parent / 'data' / 'rag'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = data_dir / 'search_log.jsonl'
    
    entry = {
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'results_count': results_count,
        'latency_ms': latency_ms
    }
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    # 测试
    print("测试自动记录功能...")
    
    entry = auto_record_session(
        user_message="如何配置 OpenClaw？",
        agent_response="配置 OpenClaw 需要以下步骤...",
        auto_eval=True
    )
    
    print(f"记录成功：{entry}")
