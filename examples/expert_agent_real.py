#!/usr/bin/env python3
"""
专家 Agent 感知系统 - 实际使用版本

这个版本直接集成到任务处理流程中
每次执行任务时自动：
1. 检索相关知识
2. 获取适用元规则
3. 基于知识执行
4. 记录反思

用法:
    cd /Users/dhr/.openclaw/workspace-demo51-agent
    PYTHONPATH=/Users/dhr/.openclaw/workspace/libs:$PYTHONPATH \
      python3 skills/expert_agent_real.py "你的任务描述"
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加 libs 路径
workspace = Path.cwd()
sys.path.insert(0, str(workspace / 'libs'))

from memory_hub import MemoryHub


class RealExpertAgent:
    """实际使用的专家 Agent"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.memory = MemoryHub(agent_name=agent_name)
    
    def execute_task(self, task_description):
        """
        执行任务（带感知）
        
        实际使用时，在这里调用你的真实任务处理逻辑
        """
        print(f"\n{'='*70}")
        print(f"🎯 任务：{task_description}")
        print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        # ========== 步骤 1: 任务前检索 ==========
        print("📚 步骤 1: 检索相关知识")
        print("-" * 70)
        
        memories = self.memory.search(task_description, top_k=5, semantic=True)
        
        if memories:
            print(f"✅ 检索到 {len(memories)} 条相关记忆\n")
            for i, m in enumerate(memories, 1):
                content = m.get('content', '')
                # 清理格式
                content = content.replace('===', '').replace('---', '').strip()
                if len(content) > 150:
                    content = content[:150] + '...'
                print(f"  [{i}] {content}\n")
        else:
            print("⚠️  没有找到相关记忆（这是新领域）\n")
        
        # ========== 步骤 2: 获取元规则 ==========
        print("📜 步骤 2: 获取适用元规则")
        print("-" * 70)
        
        rules = self.memory.search(
            "元规则 OR 原则 OR 最佳实践 OR 经验",
            top_k=5,
            memory_type='goal'
        )
        
        if rules:
            print(f"✅ 检索到 {len(rules)} 条元规则\n")
            for i, r in enumerate(rules, 1):
                content = r.get('content', '')
                if len(content) > 100:
                    content = content[:100] + '...'
                importance = r.get('importance', 5.0)
                print(f"  [{i}] [{importance:.1f}分] {content}\n")
        else:
            print("⚠️  没有找到元规则（需要运行分形思考提取）\n")
        
        # ========== 步骤 3: 执行任务 ==========
        print("🔧 步骤 3: 执行任务")
        print("-" * 70)
        
        # ⚠️  这里是关键！替换成你的实际任务处理逻辑
        # 示例：调用 Harness Agent、执行代码、调用 LLM 等
        
        # 模拟执行（实际使用时删除这段）
        result = self._simulate_task_execution(task_description, memories, rules)
        
        # 实际使用时替换成：
        # result = self.call_harness_agent(task_description, memories, rules)
        # 或
        # result = self.call_llm(task_description, memories, rules)
        # 或
        # result = self.run_code(task_description, memories, rules)
        
        print(f"✅ 任务完成\n")
        print(f"结果:\n{result}\n")
        
        # ========== 步骤 4: 任务后反思 ==========
        print("💭 步骤 4: 任务反思")
        print("-" * 70)
        
        self._reflect(task_description, result, memories, rules)
        
        print(f"\n{'='*70}")
        print("✅ 任务处理完成")
        print(f"{'='*70}\n")
        
        return result
    
    def _simulate_task_execution(self, task, memories, rules):
        """模拟任务执行（实际使用时删除）"""
        
        # 基于检索到的知识生成建议
        suggestions = []
        
        if memories:
            suggestions.append("基于历史经验：")
            for m in memories[:2]:
                content = m.get('content', '')
                if '学习点' in content:
                    # 提取学习点
                    start = content.find('学习点：')
                    if start >= 0:
                        learning = content[start+4:start+100]
                        suggestions.append(f"  - {learning}")
        
        if rules:
            suggestions.append("\n基于元规则：")
            for r in rules[:2]:
                content = r.get('content', '')
                suggestions.append(f"  - {content[:50]}")
        
        if not suggestions:
            suggestions.append("这是新任务，没有历史经验可供参考")
            suggestions.append("建议：完成任务后记录反思，积累知识")
        
        return "\n".join(suggestions)
    
    def _reflect(self, task, result, memories, rules):
        """任务后反思"""
        
        # 生成反思内容
        reflection = f"""
【任务反思】{datetime.now().strftime('%Y-%m-%d %H:%M')}

任务：{task}

使用的知识:
- 检索到 {len(memories)} 条相关记忆
- 检索到 {len(rules)} 条元规则

执行情况:
{result[:200] if len(result) > 200 else result}

学习点:
- 任务前检索帮助了解历史经验
- 元规则提供决策指导
- 需要持续积累领域知识

改进方向:
- 提取更多元规则（当前 {len(rules)} 条）
- 提高记忆密度（当前 {len(memories)} 条）
"""
        
        # 记录反思
        try:
            self.memory.add(
                content=reflection,
                memory_type='reflection',
                importance=7.0,
                tags=['reflection', 'task_completed', datetime.now().strftime('%Y-%m-%d')]
            )
            print("✅ 反思已记录到记忆系统")
        except Exception as e:
            print(f"⚠️  记录失败：{e}")
    
    def weekly_review(self):
        """周回顾"""
        print(f"\n{'='*70}")
        print("📊 周进化报告")
        print(f"{'='*70}\n")
        
        # 统计会话
        sessions = self.memory.session_storage.get_all_sessions()
        print(f"📈 记忆统计")
        print(f"  总会话数：{len(sessions)}")
        
        # 统计记忆
        total_memories = 0
        for session_id in sessions[:10]:
            memories = self.memory.session_storage.search_memories(
                session_id=session_id, top_k=100
            )
            total_memories += len(memories)
        
        print(f"  前 10 个会话的记忆数：{total_memories}")
        print(f"  平均每会话：{total_memories/max(len(sessions[:10]),1):.1f} 条")
        
        # 统计元规则
        rules = self.memory.search('元规则', top_k=100, memory_type='goal')
        print(f"\n📜 元规则")
        print(f"  总数：{len(rules)}")
        
        # 建议
        print(f"\n💡 改进建议")
        if len(sessions) < 10:
            print("  - 继续积累领域经验（当前会话数较少）")
        if len(rules) < 5:
            print("  - 加强分形思考，提取更多元规则")
            print("    运行：python3 skills/self-evolution/fractal_thinking.py")
        if total_memories/max(len(sessions[:10]),1) < 5:
            print("  - 提高记忆密度（当前平均每会话 < 5 条）")
        
        print(f"\n{'='*70}\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='专家 Agent 感知系统')
    parser.add_argument('task', nargs='?', default=None, help='任务描述')
    parser.add_argument('--agent', type=str, default='demo51-agent', help='Agent 名称')
    parser.add_argument('--weekly', action='store_true', help='运行周回顾')
    
    args = parser.parse_args()
    
    agent = RealExpertAgent(args.agent)
    
    if args.weekly:
        # 周回顾
        agent.weekly_review()
    elif args.task:
        # 执行任务
        agent.execute_task(args.task)
    else:
        # 演示模式
        print("💡 使用方式:")
        print("  1. 执行任务：python3 skills/expert_agent_real.py '任务描述'")
        print("  2. 周回顾：python3 skills/expert_agent_real.py --weekly")
        print("\n📋 示例:")
        print("  python3 skills/expert_agent_real.py '优化 Python 代码性能'")
        print("  python3 skills/expert_agent_real.py --weekly")


if __name__ == '__main__':
    main()
