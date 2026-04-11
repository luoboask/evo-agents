#!/usr/bin/env python3
"""
专家 Agent 感知系统 - 实现示例

这个脚本展示了如何让 Agent 感知和使用自进化成果

用法:
    cd /Users/dhr/.openclaw/workspace-demo51-agent
    PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
      python3 /Users/dhr/cursor/evo-agents/examples/expert_agent_demo.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加 libs 路径
workspace = Path.cwd()
sys.path.insert(0, str(workspace / 'libs'))

from memory_hub import MemoryHub


class SimpleExpertAgent:
    """简化版专家 Agent - 展示感知机制"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.memory = MemoryHub(agent_name=agent_name)
    
    def search_memories(self, query, top_k=5):
        """搜索相关记忆"""
        return self.memory.search(query, top_k=top_k, semantic=True)
    
    def get_meta_rules(self):
        """获取元规则"""
        return self.memory.search(
            "元规则 OR 原则 OR 最佳实践",
            top_k=5,
            memory_type='goal'
        )
    
    def handle_task(self, task_description):
        """处理任务（带感知）"""
        print(f"\n{'='*60}")
        print(f"🎯 任务：{task_description}")
        print(f"{'='*60}")
        
        # 1. 任务前检索
        print("\n📚 步骤 1: 检索相关知识")
        memories = self.search_memories(task_description, top_k=5)
        
        if memories:
            print(f"  ✅ 找到 {len(memories)} 条相关记忆")
            for i, m in enumerate(memories[:3], 1):
                content = m.get('content', '')
                if len(content) > 80:
                    content = content[:80] + '...'
                print(f"    {i}. {content}")
        else:
            print("  ⚠️  没有找到相关记忆")
        
        # 2. 获取元规则
        print("\n📜 步骤 2: 获取适用元规则")
        rules = self.get_meta_rules()
        
        if rules:
            print(f"  ✅ 找到 {len(rules)} 条元规则")
            for i, r in enumerate(rules[:3], 1):
                content = r.get('content', '')
                if len(content) > 80:
                    content = content[:80] + '...'
                print(f"    {i}. {content}")
        else:
            print("  ⚠️  没有找到元规则")
        
        # 3. 执行任务（模拟）
        print("\n🔧 步骤 3: 执行任务")
        result = self.execute_task(task_description, memories, rules)
        print(f"  结果：{result}")
        
        # 4. 任务后反思
        print("\n💭 步骤 4: 任务反思")
        self.reflect(task_description, result)
        
        print(f"\n{'='*60}")
        print("✅ 任务完成")
        print(f"{'='*60}\n")
        
        return result
    
    def execute_task(self, task, memories, rules):
        """执行任务（模拟）"""
        # 实际应用中这里会调用 LLM 或执行代码
        # 基于检索到的记忆和元规则来决策
        
        # 模拟执行
        return "任务已完成，基于检索到的知识和元规则"
    
    def reflect(self, task, result):
        """任务后反思"""
        # 记录这次任务的经验
        reflection = f"""
任务：{task}
结果：{result}
时间：{datetime.now().isoformat()}

学习点：
- 任务前检索帮助决策
- 元规则提供指导
- 需要持续积累领域知识
"""
        
        # 添加到记忆（使用 add 方法）
        try:
            self.memory.add(
                content=reflection,
                memory_type='reflection',
                importance=7.0,
                tags=['reflection', 'task_completed']
            )
            print("  ✅ 反思已记录")
        except Exception as e:
            print(f"  ⚠️  记录失败：{e}")
        
        print("  ✅ 反思已记录")
    
    def weekly_review(self):
        """周回顾"""
        print(f"\n{'='*60}")
        print("📊 周进化报告")
        print(f"{'='*60}")
        
        # 统计记忆
        sessions = self.memory.session_storage.get_all_sessions()
        print(f"\n📈 记忆统计")
        print(f"  总会话数：{len(sessions)}")
        
        # 统计记忆类型
        total_memories = 0
        for session_id in sessions[:10]:
            memories = self.memory.session_storage.search_memories(
                session_id=session_id, top_k=100
            )
            total_memories += len(memories)
        
        print(f"  前 10 个会话的记忆数：{total_memories}")
        print(f"  平均每会话：{total_memories/max(len(sessions[:10]),1):.1f} 条")
        
        # 获取元规则
        rules = self.get_meta_rules()
        print(f"\n📜 元规则")
        print(f"  总数：{len(rules)}")
        
        # 建议
        print(f"\n💡 改进建议")
        if len(sessions) < 10:
            print("  - 继续积累领域经验（当前会话数较少）")
        if len(rules) < 5:
            print("  - 加强分形思考，提取更多元规则")
        if total_memories/max(len(sessions[:10]),1) < 5:
            print("  - 提高记忆密度（当前平均每会话 < 5 条）")
        
        print(f"\n{'='*60}\n")


def demo():
    """演示专家 Agent 感知系统"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║  专家 Agent 感知系统演示                                  ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 Agent
    agent = SimpleExpertAgent('demo51-agent')
    
    # 演示 1: 处理任务
    print("演示 1: 处理任务（带感知）")
    agent.handle_task("优化 Python 代码性能")
    
    # 演示 2: 周回顾
    print("演示 2: 周回顾")
    agent.weekly_review()


if __name__ == '__main__':
    demo()
