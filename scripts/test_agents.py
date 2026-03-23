#!/usr/bin/env python3
"""
测试多 Agent 配置
"""

import os
import sys
from pathlib import Path

# 添加 workspace 根目录到路径以支持 libs 导入
WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

# 使用标准导入 (memory_hub 现在是合法的 Python 包名)
try:
    from libs.memory_hub import MemoryHub
except ImportError as e:
    print(f"❌ 导入 Memory Hub 失败：{e}")
    sys.exit(1)


def test_agent(agent_name: str):
    """测试 Agent"""
    print(f"\n{'='*60}")
    print(f"🤖 测试 Agent: {agent_name}")
    print(f"{'='*60}")
    
    # 设置环境变量
    os.environ['OPENCLAW_AGENT'] = agent_name
    
    # 创建 Memory Hub
    hub = MemoryHub(agent_name)
    
    # 测试添加记忆
    print("\n📝 测试添加记忆...")
    mem_id = hub.add(
        content=f"{agent_name} 的测试记忆",
        memory_type='observation',
        importance=5.0,
        tags=['test', agent_name]
    )
    print(f"   ✅ 添加记忆 #{mem_id}")
    
    # 测试搜索记忆
    print("\n🔍 测试搜索记忆...")
    results = hub.search(agent_name, top_k=5)
    print(f"   ✅ 找到 {len(results)} 条记忆")
    for r in results:
        print(f"      - {r['content']}")
    
    # 测试统计
    print("\n📊 测试统计...")
    stats = hub.stats()
    print(f"   ✅ 总记忆数：{stats['total']}")
    print(f"   ✅ 按类型：{stats['by_type']}")
    
    # 测试知识
    print("\n📚 测试知识管理...")
    if hub.knowledge:
        print(f"   ✅ 知识接口可用")
        print(f"   ✅ 公共知识路径：{hub.knowledge.public_path}")
        print(f"   ✅ 私有知识路径：{hub.knowledge.private_path}")
    
    # 测试评估
    print("\n📈 测试评估...")
    if hub.evaluation:
        print(f"   ✅ 评估接口可用")
        eval_id = hub.evaluation.record(
            query=f"{agent_name} 测试",
            retrieved_count=len(results),
            latency_ms=50.0,
            feedback="positive"
        )
        print(f"   ✅ 记录评估 #{eval_id}")
    
    print(f"\n✅ {agent_name} 测试完成！")


def main():
    """测试所有 Agent"""
    agents = ['ai-baby', 'baby1', 'baby2', 'baby3']
    
    print("🚀 开始多 Agent 测试...")
    
    for agent in agents:
        test_agent(agent)
    
    print("\n" + "="*60)
    print("✅ 所有 Agent 测试完成！")
    print("="*60)
    
    # 验证数据隔离
    print("\n📊 验证数据隔离...")
    for agent in agents:
        data_path = Path('/Users/dhr/.openclaw/workspace-ai-baby/data') / agent
        memory_path = data_path / 'memory'
        
        if memory_path.exists():
            db_files = list(memory_path.glob('*.db'))
            print(f"   ✅ {agent}: {len(db_files)} 个数据库文件")
        else:
            print(f"   ⚠️  {agent}: 数据目录不存在")


if __name__ == '__main__':
    main()
