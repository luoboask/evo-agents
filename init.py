#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自进化系统 v5.0 初始化脚本
初始化数据库和配置文件
"""

import os
import sys
from pathlib import Path

# 配置
WORKSPACE = Path("/Users/dhr/.openclaw/workspace-ai-baby")
MEMORY_DIR = WORKSPACE / "memory"
SKILLS_DIR = WORKSPACE / "skills"
SELF_EVOLUTION_DIR = SKILLS_DIR / "self-evolution"

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def init_directories():
    """创建必要的目录"""
    print_header("初始化目录")
    
    dirs_to_create = [
        MEMORY_DIR,
        MEMORY_DIR / "vector_db",
        MEMORY_DIR / "vector_db" / "ai-baby",
        MEMORY_DIR / "learning",
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        print_success(f"目录：{dir_path}")
    
    print_info("目录初始化完成")

def init_self_evolution():
    """初始化自进化系统"""
    print_header("初始化自进化系统 v5.0")
    
    # 运行安装脚本
    install_script = SELF_EVOLUTION_DIR / "install.py"
    if install_script.exists():
        print_info(f"运行安装脚本：{install_script}")
        os.system(f"cd {SELF_EVOLUTION_DIR} && python3 install.py")
        print_success("自进化系统初始化完成")
    else:
        print_error("安装脚本不存在")

def verify_databases():
    """验证数据库"""
    print_header("验证数据库")
    
    databases = [
        MEMORY_DIR / "ai-baby_memory_stream.db",
        MEMORY_DIR / "ai-baby_knowledge_base.db",
        SKILLS_DIR / "rag" / "logs" / "evaluations.jsonl",
    ]
    
    all_exist = True
    for db_path in databases:
        if db_path.exists():
            print_success(f"{db_path.name}")
        else:
            print_error(f"{db_path.name} (不存在)")
            all_exist = False
    
    if all_exist:
        print_info("所有数据库已就绪")
    else:
        print_info("部分数据库需要创建")

def show_status():
    """显示系统状态"""
    print_header("系统状态")
    
    # 记忆统计
    print("\n📊 记忆流:")
    os.system(f"cd {SKILLS_DIR}/memory-search && python3 search_sqlite.py --stats 2>/dev/null | head -10")
    
    # RAG 统计
    print("\n📊 RAG 评估:")
    rag_log = SKILLS_DIR / "rag" / "logs" / "evaluations.jsonl"
    if rag_log.exists():
        with open(rag_log, 'r') as f:
            count = sum(1 for _ in f)
        print(f"   总记录数：{count}")
        if count >= 10:
            print("   ✅ 可以进行自动调优")
        else:
            print(f"   ⏳ 需要积累更多数据 (当前：{count}/10)")
    else:
        print("   未激活")
    
    # 自进化系统
    print("\n📊 自进化系统:")
    os.system(f"cd {SELF_EVOLUTION_DIR} && python3 main.py status 2>&1 | grep -E '记忆 | 进化 | 知识库' | head -5")

def main():
    print("\n" + "🍼" * 30)
    print("  ai-baby 自进化系统 v5.1 - 初始化")
    print("🍼" * 30)
    
    # 1. 创建目录
    init_directories()
    
    # 2. 初始化自进化系统
    init_self_evolution()
    
    # 3. 验证数据库
    verify_databases()
    
    # 4. 显示状态
    show_status()
    
    print_header("初始化完成")
    print("\n✅ 系统已就绪！")
    print("\n下一步:")
    print("  1. 运行 ./start.sh 查看系统状态")
    print("  2. 正常使用，积累 RAG 数据")
    print("  3. 数据达到 10+ 条后运行自动调优")
    print("")

if __name__ == "__main__":
    main()
