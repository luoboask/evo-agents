#!/usr/bin/env python3
"""
简化版基准测试 - 直接测试记忆检索

用于快速验证记忆系统是否正常工作

用法:
    cd /Users/dhr/.openclaw/workspace-demo51-agent
    PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
      python3 benchmarks/simple_test.py
"""

import sys
from pathlib import Path

# 添加 libs 路径
workspace = Path.cwd()
sys.path.insert(0, str(workspace / 'libs'))

from memory_hub import MemoryHub


def test_basic_search(agent_name='demo51-agent'):
    """测试基本搜索功能"""
    print("📊 测试基本搜索功能")
    print("="*60)
    print(f"Agent: {agent_name}")
    print(f"Workspace: {workspace}")
    print()
    
    # 初始化
    memory = MemoryHub(agent_name=agent_name)
    
    # 获取所有会话
    sessions = memory.session_storage.get_all_sessions()
    print(f"✅ 找到 {len(sessions)} 个会话")
    if sessions:
        print(f"   示例：{sessions[:3]}")
    print()
    
    # 测试 1：检索特定会话
    print("测试 1: 检索特定会话的记忆")
    if sessions:
        session_id = sessions[0]
        memories = memory.session_storage.search_memories(session_id=session_id, top_k=5)
        print(f"  ✅ 会话 {session_id[:8]}...: {len(memories)} 条记忆")
        if memories:
            print(f"     内容预览：{memories[0].get('content', '')[:50]}...")
    print()
    
    # 测试 2：统计信息
    print("测试 2: 统计信息")
    total_memories = 0
    for session_id in sessions[:10]:  # 只统计前 10 个
        memories = memory.session_storage.search_memories(session_id=session_id, top_k=100)
        total_memories += len(memories)
    
    print(f"  总会话数：{len(sessions)}")
    print(f"  前 10 个会话的总记忆数：{total_memories}")
    print(f"  平均每会话：{total_memories/max(len(sessions[:10]),1):.1f} 条")
    print()
    
    # 测试 3：搜索特定内容
    print("测试 3: 搜索包含 'OpenClaw' 的会话")
    found_count = 0
    for session_id in sessions[:10]:
        memories = memory.session_storage.search_memories(session_id=session_id, top_k=10)
        for m in memories:
            if 'OpenClaw' in m.get('content', ''):
                found_count += 1
                print(f"  ✅ {session_id[:8]}...: 找到 OpenClaw 相关内容")
                break
    
    print(f"总计：在 {found_count}/10 个会话中找到 OpenClaw")
    print()
    
    print("="*60)
    print("✅ 基本搜索测试完成")
    
    return {
        'total_sessions': len(sessions),
        'total_memories': total_memories,
        'search_hits': found_count
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='简化版基准测试')
    parser.add_argument('--agent', type=str, default='demo51-agent', help='Agent 名称')
    
    args = parser.parse_args()
    
    results = test_basic_search(args.agent)
    
    # 输出 JSON 结果
    print(f"\n📊 JSON 结果:")
    import json
    print(json.dumps(results, indent=2))
