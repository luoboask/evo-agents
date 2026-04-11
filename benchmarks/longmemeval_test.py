#!/usr/bin/env python3
"""
LongMemEval 风格基准测试

受 MemPalace 启发实现
测试 evo-agents 的记忆检索能力
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_hub import MemoryHub
from benchmarks.metrics import evaluate_retrieval, aggregate_metrics, print_report


def load_test_data(data_path: str) -> list:
    """
    加载测试数据
    
    数据格式：
    [
        {
            "id": "q001",
            "question": "用户喜欢吃什么？",
            "haystack": ["session_001.jsonl", "session_002.jsonl"],
            "ground_truth": ["session_001.jsonl"],
            "type": "preference"
        },
        ...
    ]
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_benchmark(questions: list, agent_name: str = "test-agent", limit: int = None) -> list:
    """
    运行基准测试
    
    Args:
        questions: 测试问题列表
        agent_name: Agent 名称
        limit: 限制测试问题数量（None 表示全部）
    
    Returns:
        所有问题的评估结果列表
    """
    if limit:
        questions = questions[:limit]
    
    print(f"📊 开始基准测试")
    print(f"   Agent: {agent_name}")
    print(f"   问题数：{len(questions)}")
    print()
    
    all_results = []
    
    for i, q in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] 测试问题 {q['id']}...")
        
        # 创建独立的记忆系统（每个问题独立测试）
        memory = MemoryHub(agent_name=agent_name)
        
        # 导入 haystack sessions
        for session_file in q['haystack']:
            try:
                # 读取会话文件
                session_path = Path(session_file)
                if not session_path.is_absolute():
                    # 相对于 workspace 目录
                    session_path = Path.cwd() / session_path
                
                if session_path.exists():
                    with open(session_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 使用 session_id 作为文件名
                    session_id = session_path.stem
                    
                    # 添加到记忆
                    memory.add_session(
                        content=content,
                        memory_type='observation',
                        tags=['haystack', 'benchmark'],
                        metadata={'source': session_file},
                        session_id=session_id
                    )
            except Exception as e:
                print(f"  ⚠️  导入失败 {session_file}: {e}")
        
        # 查询（直接使用 session_storage，因为 memory.search() 有问题）
        try:
            retrieved = memory.session_storage.search_memories(
                session_id='',  # 空表示搜索所有会话
                top_k=10
            )
            
            # 调试输出
            if len(retrieved) > 0:
                print(f"  检索到 {len(retrieved)} 条结果")
            
            # 提取检索结果的 ID（使用 session_id 作为来源）
            retrieved_ids = []
            for r in retrieved:
                source = r.get('session_id', '')
                if source:
                    # 转换为文件路径格式
                    retrieved_ids.append(f"memory/{source}.md")
            
            # 映射到索引
            all_sources = q['haystack']
            rankings = []
            for rid in retrieved_ids:
                if rid in all_sources:
                    rankings.append(all_sources.index(rid))
            
            # 正确答案
            correct_ids = set(all_sources.index(gt) for gt in q['ground_truth'] if gt in all_sources)
            
            # 评估
            if rankings and correct_ids:
                metrics = evaluate_retrieval(
                    rankings=rankings,
                    correct_ids=correct_ids,
                    corpus_ids=all_sources,
                    k_values=[5, 10]
                )
                
                # 添加问题类型
                metrics['question_id'] = q['id']
                metrics['question_type'] = q.get('type', 'unknown')
                
                all_results.append(metrics)
                
                # 打印简要结果
                status = "✅" if metrics['recall_any@5'] > 0.5 else "⚠️"
                print(f"  {status} Recall@5: {metrics['recall_any@5']:.1%}")
            else:
                print(f"  ❌ 无法评估（无检索结果或无正确答案）")
                
        except Exception as e:
            print(f"  ❌ 查询失败：{e}")
        
        # 清理记忆（为下一个问题准备）
        # 实际使用时可能需要更复杂的清理逻辑
    
    return all_results


def print_summary(all_results: list):
    """打印总结报告"""
    if not all_results:
        print("\n❌ 没有有效的测试结果")
        return
    
    # 总体统计
    avg_metrics = aggregate_metrics(all_results)
    
    print("\n" + "="*60)
    print("📊 基准测试总结")
    print("="*60)
    print_report(avg_metrics)
    
    # 按问题类型统计
    by_type = {}
    for result in all_results:
        qtype = result.get('question_type', 'unknown')
        if qtype not in by_type:
            by_type[qtype] = []
        by_type[qtype].append(result)
    
    print("\n按问题类型细分:")
    print("-"*60)
    
    for qtype, results in sorted(by_type.items()):
        avg = aggregate_metrics(results)
        print_report(avg, question_type=qtype)
    
    # 输出 JSONL
    output_file = f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in all_results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    print(f"\n💾 详细结果已保存到：{output_file}")


def main():
    parser = argparse.ArgumentParser(description='LongMemEval 风格基准测试')
    parser.add_argument('data_path', type=str, help='测试数据 JSON 文件路径')
    parser.add_argument('--agent', type=str, default='test-agent', help='Agent 名称')
    parser.add_argument('--limit', type=int, default=None, help='限制测试问题数量')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 检查数据文件
    data_path = Path(args.data_path)
    if not data_path.exists():
        print(f"❌ 数据文件不存在：{data_path}")
        print("\n示例数据格式:")
        print("""
[
    {
        "id": "q001",
        "question": "用户喜欢吃什么？",
        "haystack": ["memory/2026-04-01.md", "memory/2026-04-02.md"],
        "ground_truth": ["memory/2026-04-01.md"],
        "type": "preference"
    }
]
        """)
        return
    
    # 加载数据
    questions = load_test_data(str(data_path))
    
    # 运行测试
    all_results = run_benchmark(questions, args.agent, args.limit)
    
    # 打印总结
    print_summary(all_results)


if __name__ == '__main__':
    main()
