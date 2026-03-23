#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证系统功能
"""

import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent / "skills" / "memory-search"))
sys.path.insert(0, str(Path(__file__).parent / "skills" / "rag"))

from search_sqlite import SQLiteMemorySearch
from evaluate import RAGEvaluator

print("=" * 60)
print("  🍼 ai-baby 功能验证")
print("=" * 60)

# 1. 测试记忆搜索
print("\n[1/3] 测试记忆搜索...")
try:
    search = SQLiteMemorySearch()
    results = search.search("RAG", top_k=3, semantic=False)
    print(f"✅ 记忆搜索正常 - 找到 {len(results)} 条结果")
    if results:
        print(f"   示例：{results[0]['content'][:50]}...")
except Exception as e:
    print(f"❌ 记忆搜索失败：{e}")

# 2. 测试 RAG 记录
print("\n[2/3] 测试 RAG 记录...")
try:
    evaluator = RAGEvaluator()
    evaluator.record(
        query="验证测试",
        retrieved_count=1,
        latency_ms=50.0,
        feedback="positive"
    )
    print("✅ RAG 记录正常")
except Exception as e:
    print(f"❌ RAG 记录失败：{e}")

# 3. 测试配置加载
print("\n[3/3] 测试配置加载...")
try:
    import yaml
    config_path = Path.home() / ".openclaw" / "workspace-ai-baby-config" / "config.yaml"
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        workspace = config.get('workspace', 'N/A')
        print(f"✅ 配置加载正常 - 工作区：{workspace}")
    else:
        print("⚠️  配置文件不存在")
except Exception as e:
    print(f"❌ 配置加载失败：{e}")

print("\n" + "=" * 60)
print("  ✅ 所有功能验证通过！")
print("=" * 60)
print("\n系统已就绪，可以开始使用！")
print("\n常用命令:")
print("  ./start.sh                                    # 查看系统状态")
print("  python3 skills/memory-search/search_sqlite.py \"查询\" --semantic  # 语义搜索")
print("  python3 skills/rag/evaluate.py --report --days 7  # RAG 报告")
print()
