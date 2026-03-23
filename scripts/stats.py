#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆&知识系统调用统计

显示：
- 记忆总数和类型分布
- 知识管理统计
- RAG 评估记录
- 最近调用记录
"""

import json
import sys
from pathlib import Path

# 添加 workspace 根目录到路径
WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from libs.memory_hub import MemoryHub


def print_stats(agent_name='ai-baby', days=7):
    """打印统计信息"""
    hub = MemoryHub(agent_name)
    
    print("=" * 70)
    print(f"📊 {agent_name} - 记忆&知识系统调用统计")
    print("=" * 70)
    
    # 1. 记忆统计
    stats = hub.stats()
    print(f"\n📈 记忆总数：{stats.get('total', 0)}")
    print(f"   按类型分布:")
    for mtype, count in stats.get('by_type', {}).items():
        print(f"      - {mtype}: {count} 条")
    
    # 2. 知识统计
    print(f"\n📚 知识管理:")
    public_dir = Path('public')
    if public_dir.exists():
        knowledge_files = list(public_dir.glob('**/*.json'))
        print(f"   公共知识文件：{len(knowledge_files)} 个")
        for kf in knowledge_files[:5]:
            print(f"      - {kf.relative_to(public_dir)}")
    
    # 3. RAG 评估统计
    print(f"\n📉 RAG 评估记录 (过去{days}天):")
    evals_path = hub.evaluation.evaluations_path
    if evals_path.exists():
        with open(evals_path, 'r') as f:
            evals = [line for line in f.readlines()]
        print(f"   总记录数：{len(evals)} 条")
        
        # 分析反馈
        feedback = {'positive': 0, 'neutral': 0, 'negative': 0}
        zero_results = 0
        for e in evals:
            data = json.loads(e)
            fb = data.get('feedback', 'neutral')
            feedback[fb] = feedback.get(fb, 0) + 1
            if data.get('retrieved_count', 0) == 0:
                zero_results += 1
        
        print(f"   用户反馈:")
        pos = feedback.get('positive', 0)
        print(f"      - 正面：{pos} ({pos/len(evals)*100:.1f}%)")
        print(f"      - 中性：{feedback.get('neutral', 0)}")
        print(f"      - 负面：{feedback.get('negative', 0)}")
        print(f"   零结果查询：{zero_results} 条 ({zero_results/len(evals)*100:.1f}%)")
    else:
        print(f"   无评估记录")
    
    # 4. 最近调用
    print(f"\n🕐 最近评估记录 (Top 5):")
    if evals_path.exists():
        with open(evals_path, 'r') as f:
            lines = f.readlines()
        for line in lines[-5:]:
            data = json.loads(line)
            print(f"   - {data['timestamp'][:19]}: {data['query'][:30]} (检索：{data['retrieved_count']}条)")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='记忆&知识系统调用统计')
    parser.add_argument('--agent', default='ai-baby', help='Agent 名称')
    parser.add_argument('--days', type=int, default=7, help='统计天数')
    
    args = parser.parse_args()
    print_stats(args.agent, args.days)
