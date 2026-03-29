#!/usr/bin/env python3
"""
RAG 集成测试 - 验证记忆搜索与 RAG 评估的集成
"""

import sys
import time
from pathlib import Path
from path_utils import resolve_workspace, resolve_data_dir

# 添加路径
SKILLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILLS_DIR))

# 导入记忆搜索
search_sqlite_path = SKILLS_DIR / "memory-search" / "search_sqlite.py"
import importlib.util
spec = importlib.util.spec_from_file_location("search_sqlite", search_sqlite_path)
search_sqlite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_sqlite)
SQLiteMemorySearch = search_sqlite.SQLiteMemorySearch


def test_basic_search():
    """测试基本搜索 + RAG 记录"""
    print("=" * 60)
    print("测试 1: 基本搜索 + RAG 记录")
    print("=" * 60)
    
    search = SQLiteMemorySearch()
    
    # 测试查询
    queries = [
        "RAG",
        "记忆系统",
        "用户偏好"
    ]
    
    for query in queries:
        print(f"\n🔍 查询：{query}")
        results = search.search(query, top_k=5, semantic=False, record_rag=True)
        print(f"   找到 {len(results)} 条结果")
        if results:
            print(f"   最高分：{results[0].get('score', 'N/A')}")
        time.sleep(0.2)
    
    print("\n✅ 测试完成")


def test_semantic_search():
    """测试语义搜索 + RAG 记录"""
    print("\n" + "=" * 60)
    print("测试 2: 向量语义搜索 + RAG 记录")
    print("=" * 60)
    
    search = SQLiteMemorySearch()
    
    queries = [
        "如何优化检索系统",
        "AI 助手学习"
    ]
    
    for query in queries:
        print(f"\n🔍 查询：{query}")
        results = search.search(query, top_k=5, semantic=True, record_rag=True)
        print(f"   找到 {len(results)} 条结果")
        if results:
            print(f"   最高相似度：{results[0].get('score', 'N/A')}")
        time.sleep(0.2)
    
    print("\n✅ 测试完成")


def test_no_record():
    """测试禁用 RAG 记录"""
    print("\n" + "=" * 60)
    print("测试 3: 禁用 RAG 记录")
    print("=" * 60)
    
    search = SQLiteMemorySearch()
    
    print("\n🔍 查询：test (record_rag=False)")
    results = search.search("test", top_k=5, record_rag=False)
    print(f"   找到 {len(results)} 条结果")
    print("   (此次查询不会被记录)")
    
    print("\n✅ 测试完成")


def show_stats():
    """显示 RAG 记录统计"""
    print("\n" + "=" * 60)
    print("RAG 记录统计")
    print("=" * 60)
    
    import subprocess
    result = subprocess.run(
        ["python3", "skills/rag/evaluate.py", "--report", "--days", "1"],
        capture_output=True, text=True
    )
    print(result.stdout)


if __name__ == "__main__":
    print("🧪 RAG 集成测试\n")
    
    test_basic_search()
    test_semantic_search()
    test_no_record()
    show_stats()
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成!")
    print("=" * 60)
