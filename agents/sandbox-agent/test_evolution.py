#!/usr/bin/env python3
"""
测试 sandbox-agent 的自进化集成
"""

import asyncio
import sys
from pathlib import Path

# 添加路径
EVOLUTION_PATH = Path(__file__).parent.parent.parent / 'skills' / 'self-evolution-5.0'
sys.path.insert(0, str(EVOLUTION_PATH))
MEMORY_SEARCH_PATH = Path(__file__).parent.parent.parent / 'skills' / 'memory-search'
sys.path.insert(0, str(MEMORY_SEARCH_PATH))

from agent import SandboxAgent


async def main():
    """测试主函数"""
    print("=" * 70)
    print("🧪 Sandbox Agent 自进化集成测试")
    print("=" * 70)
    
    # 创建 Agent
    print("\n1. 创建 Sandbox Agent")
    agent = SandboxAgent()
    
    # 创建实例
    print("\n2. 创建沙箱实例")
    instance_id = await agent.create_instance(
        requirement_id='REQ-TEST-001',
        config={
            'frontend_code': './frontend/test',
            'backend_code': './backend/test',
            'requirement_desc': '测试功能'
        }
    )
    
    # 获取统计
    print("\n3. 获取进化统计")
    stats = agent.evolution.get_evolution_stats()
    print(f"   记忆总数：{stats['memory_stream']['total_memories']}")
    print(f"   进化事件：{stats['evolution_events']['total_events']}")
    
    # 生成报告
    print("\n4. 生成学习报告")
    report = agent.evolution.generate_learning_report(days=1)
    print(f"   时期：{report['period']}")
    print(f"   洞察：{report['insights']}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成！")
    print("=" * 70)


if __name__ == '__main__':
    asyncio.run(main())
