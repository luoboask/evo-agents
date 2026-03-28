#!/usr/bin/env python3
"""
自动记录会话 - Auto Record Session
自动将对话记录到混合记忆系统
"""

import sys
import json
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from search import IntegratedHybridMemory


def record_session():
    """记录当前会话"""
    memory = IntegratedHybridMemory()
    
    # 读取标准输入
    content = sys.stdin.read().strip()
    
    if not content:
        print("No content to record")
        return
    
    # 解析 JSON 输入
    try:
        data = json.loads(content)
        role = data.get("role", "user")
        text = data.get("content", "")
        metadata = data.get("metadata", {})
    except:
        # 纯文本输入
        role = "user"
        text = content
        metadata = {}
    
    # 记录
    entry = memory.record_interaction(role, text, metadata)
    
    print(f"✅ Recorded ({entry['importance']}): {text[:50]}...")
    
    # 显示统计
    stats = memory.get_stats()
    print(f"📊 Memory: {stats['working_memory']} working, {stats['vector_memory']} vector")


if __name__ == '__main__':
    record_session()
