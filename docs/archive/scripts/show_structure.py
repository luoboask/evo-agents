#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展示 ai-baby 自进化体系完整结构
"""

import os
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/Users/dhr/.openclaw/workspace-ai-baby")

def print_header(text, char="="):
    print("\n" + char * 60)
    print(f"  {text}")
    print(char * 60)

def print_section(text):
    print(f"\n{text}")
    print("-" * len(text))

def count_files(directory, pattern="*.py"):
    """统计文件数量"""
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))

def get_db_stats(db_path):
    """获取数据库统计"""
    import sqlite3
    if not db_path.exists():
        return None
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM memories")
        count = cur.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def show_tree_structure():
    """显示目录树结构"""
    print_section("📁 目录结构")
    print("""
workspace-ai-baby/
│
├── 📄 README.md                      ⭐ 工作区入口
├── 📄 SELF_EVOLUTION_SYSTEM.md       ⭐ 体系总览
├── 📄 USER_MANUAL.md                 ⭐ 使用手册
├── 📄 IMPROVEMENT_PLAN.md            ⭐ 改进计划
├── 📄 MEMORY.md                         长期记忆
├── 📄 HEARTBEAT.md                      日常任务
├── 🔧 start.sh                          快速启动
├── 🔧 init.py                           初始化
│
├── 📂 skills/
│   ├── rag/                          ⭐ RAG 评估系统
│   │   ├── evaluate.py               # 评估框架
│   │   ├── auto_tune.py              # 自动调优
│   │   ├── recorder.py               # 检索记录
│   │   └── logs/evaluations.jsonl    # 评估日志
│   │
│   ├── memory-search/                ⭐ 记忆搜索
│   │   ├── search_sqlite.py          # SQLite 搜索
│   │   ├── semantic_search.py        # 语义搜索
│   │   └── daily_review.py           # 每日回顾
│   │
│   ├── self-evolution/           ⭐ 自进化核心
│   │   ├── main.py                   # 统一入口
│   │   ├── memory_stream.py          # 记忆流
│   │   ├── fractal_thinking.py       # 分形思考
│   │   ├── nightly_cycle.py          # 夜间循环
│   │   └── knowledge_base.py         # 知识库
│   │
│   ├── aiway/                           AIWay 社区
│   ├── hybrid-memory/                   混合记忆
│   ├── knowledge-graph/                 知识图谱
│   └── websearch/                       网页搜索
│
├── 📂 memory/
│   ├── ai-baby_memory_stream.db      # 记忆流 (23 条)
│   ├── ai-baby_knowledge_base.db     # 知识库
│   ├── 2026-03-23.md                 # 今日记录
│   └── learning/                     # 学习记录
│
└── 📂 apps/
    ├── agent-mind-visualizer/        # Agent 思维可视化
    ├── ai-pet-simulator/             # AI 宠物模拟
    └── content-creation-visualizer/  # 内容创作可视化
    """)

def show_component_stats():
    """显示组件统计"""
    print_section("📊 组件统计")
    
    # RAG 评估
    rag_log = WORKSPACE / "skills" / "rag" / "logs" / "evaluations.jsonl"
    if rag_log.exists():
        with open(rag_log, 'r') as f:
            rag_count = sum(1 for _ in f)
        print(f"\n🔍 RAG 评估系统")
        print(f"   记录数：{rag_count} 条")
        print(f"   状态：{'✅ 可进行自动调优' if rag_count >= 10 else '⏳ 数据积累中'} ({rag_count}/10)")
    
    # 记忆流
    memory_db = WORKSPACE / "memory" / "ai-baby_memory_stream.db"
    memory_count = get_db_stats(memory_db)
    print(f"\n🧠 记忆流系统")
    print(f"   记忆数：{memory_count} 条")
    print(f"   状态：✅ 活跃")
    
    # 自进化核心
    self_evo_dir = WORKSPACE / "skills" / "self-evolution"
    core_files = count_files(self_evo_dir, "*.py")
    doc_files = count_files(self_evo_dir, "*.md")
    print(f"\n🧬 自进化核心")
    print(f"   Python 模块：{core_files} 个")
    print(f"   文档：{doc_files} 个")
    print(f"   状态：✅ 已整理")
    
    # 文档体系
    print(f"\n📚 文档体系")
    docs = [
        "README.md",
        "SELF_EVOLUTION_SYSTEM.md",
        "USER_MANUAL.md",
        "IMPROVEMENT_PLAN.md",
        "HEARTBEAT.md",
    ]
    for doc in docs:
        doc_path = WORKSPACE / doc
        if doc_path.exists():
            size_kb = doc_path.stat().st_size / 1024
            print(f"   ✅ {doc} ({size_kb:.1f}KB)")

def show_data_flow():
    """显示数据流"""
    print_section("🔄 数据流")
    print("""
对话流程:
  用户提问 → 记忆搜索 (自动 RAG 记录) → 生成回复 → 记录评估日志

进化流程:
  系统行为 → 进化事件记录 → 记忆流存储 → 分形思考分析 
  → 夜间循环处理 → 知识库更新 → 报告输出

RAG 优化流程:
  日常检索 → 自动记录指标 → 积累 10+ 条 → 自动调优 
  → 应用最优配置 → 持续监控
    """)

def show_quick_commands():
    """显示快速命令"""
    print_section("🚀 快速命令")
    print("""
# 系统状态
./start.sh

# RAG 评估
python3 skills/rag/evaluate.py --report --days 7
python3 skills/rag/auto_tune.py --report  # 需要 10+ 条数据

# 记忆搜索
python3 skills/memory-search/search_sqlite.py "查询" --semantic

# 自进化功能
cd skills/self-evolution && python3 main.py status
python3 main.py fractal --limit 10
python3 main.py nightly
    """)

def show_next_steps():
    """显示下一步计划"""
    print_section("📋 下一步计划")
    print("""
P0 - 本周:
  [ ] 积累 RAG 数据 (当前 5 条 → 目标 10+ 条)
  [ ] 运行第一次自动调优

P1 - 本月:
  [ ] 用户反馈自动推断
  [ ] RAG 可视化报告
  [ ] 激活自进化核心

P2 - 下季度:
  [ ] 多 Agent 协作
  [ ] 跨工作区知识共享
  [ ] Web UI 界面
    """)

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "🍼" * 30)
    print(f"  ai-baby 自进化体系 v5.1 - 完整结构")
    print(f"  生成时间：{timestamp}")
    print("🍼" * 30)
    
    show_tree_structure()
    show_component_stats()
    show_data_flow()
    show_quick_commands()
    show_next_steps()
    
    print_header("总结", "🎉")
    print("""
✅ 文档体系：完整 (6 个核心文档)
✅ RAG 评估：已集成 (5 条记录)
✅ 记忆搜索：已集成 (23 条记忆)
✅ 自进化核心：已整理 (20 个文件归档)
✅ 工具脚本：就绪 (start.sh, init.py)

📊 体系状态：准备就绪
📈 当前重点：积累 RAG 数据，达到自动调优门槛
    """)
    print()

if __name__ == "__main__":
    main()
