#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整理自进化系统 v5.0 目录结构
清理冗余文件，归档历史版本
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# 配置
SELF_EVOLUTION_DIR = Path("/Users/dhr/.openclaw/workspace-ai-baby/skills/self-evolution")
ARCHIVE_DIR = SELF_EVOLUTION_DIR / "_archive"

# 核心文件（保留）
CORE_FILES = [
    # 核心模块
    "main.py",
    "memory_stream.py",
    "fractal_thinking.py",
    "nightly_cycle.py",
    "knowledge_base.py",
    "self_evolution_real.py",
    "install.py",
    
    # 配置文件
    "config.yaml.example",
    "skill.json",
    
    # 核心文档
    "ARCHITECTURE.md",
    "README_FINAL.md",
    "INSTALL.md",
    "SETUP.md",
    "INITIAL_SETUP.md",
]

# 辅助模块（保留）
HELPER_FILES = [
    "advanced_learning.py",
    "causal_reasoning_enhanced.py",
    "creative_learning_enhanced.py",
    "reinforcement_learning_enhanced.py",
    "specialist_agents.py",
    "sync_to_kb.py",
]

# 待清理的冗余文件
REDUNDANT_FILES = [
    # 旧版本/重复
    "fractal_thinking_v2.py",
    "auto_learning_demo.py",
    "auto_learning_rich.py",
    "self_learning_showcase.py",
    "quick_evolve.py",
    "scheduled_learning.py",
    "realtime_feedback.py",
    "daily_reflection.py",
    "knowledge_graph_expansion.py",
    "embedding.py",  # 已删除，复用 memory-search
    
    # 研究文档（可归档）
    "GITHUB_RESEARCH.md",
    "THINKING_FRAMEWORKS_RESEARCH.md",
    "INTELLIGENCE_REPORT.md",
    "MULTI_AGENT_DESIGN.md",
    "PATTERN_RECOGNITION_OPTIMIZATION.md",
    "DUPLEX_CHECK.md",
    "AUTO_RECORD_SUMMARY.md",
    "AUTOMATION_SETUP.md",
    "OLLAMA_SETUP.md",
    "FINAL_STATUS.md",
    "IMPROVEMENT_PLAN.md",  # 已有根目录版本
]

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    print(f"✅ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def create_archive_dir():
    """创建归档目录"""
    ARCHIVE_DIR.mkdir(exist_ok=True)
    print_success(f"创建归档目录：{ARCHIVE_DIR}")

def move_to_archive(files):
    """移动文件到归档目录"""
    moved = 0
    for filename in files:
        src = SELF_EVOLUTION_DIR / filename
        if src.exists():
            dst = ARCHIVE_DIR / filename
            shutil.move(str(src), str(dst))
            print_success(f"归档：{filename}")
            moved += 1
        else:
            print_info(f"跳过（不存在）：{filename}")
    return moved

def verify_core_files():
    """验证核心文件是否存在"""
    print_header("验证核心文件")
    
    missing = []
    for filename in CORE_FILES:
        if (SELF_EVOLUTION_DIR / filename).exists():
            print_success(f"{filename}")
        else:
            print_warning(f"缺失：{filename}")
            missing.append(filename)
    
    if missing:
        print_warning(f"\n缺失 {len(missing)} 个核心文件")
    else:
        print_success("所有核心文件完整")
    
    return missing

def show_directory_structure():
    """显示整理后的目录结构"""
    print_header("整理后的目录结构")
    
    core_files = [f for f in CORE_FILES if (SELF_EVOLUTION_DIR / f).exists()]
    helper_files = [f for f in HELPER_FILES if (SELF_EVOLUTION_DIR / f).exists()]
    
    print("\n📁 self-evolution/")
    print("   ├── 📄 核心模块")
    for f in sorted(core_files):
        if f.endswith('.py'):
            print(f"   │   ├── {f}")
    
    print("   │")
    print("   ├── 📄 辅助模块")
    for f in sorted(helper_files):
        print(f"   │   ├── {f}")
    
    print("   │")
    print("   ├── 📄 配置文件")
    print("   │   ├── config.yaml.example")
    print("   │   └── skill.json")
    print("   │")
    print("   ├── 📄 核心文档")
    for f in sorted([f for f in CORE_FILES if f.endswith('.md')]):
        print(f"   │   ├── {f}")
    
    print("   │")
    print(f"   └── 📂 _archive/ (归档的历史文件)")
    
    if ARCHIVE_DIR.exists():
        archive_count = len(list(ARCHIVE_DIR.iterdir()))
        print(f"       └── {archive_count} 个文件")

def main():
    print("\n🧹" + "=" * 58)
    print("  自进化系统 v5.0 - 目录结构整理")
    print("🧹" + "=" * 58)
    
    # 1. 验证核心文件
    missing = verify_core_files()
    
    # 2. 创建归档目录
    print_header("创建归档目录")
    create_archive_dir()
    
    # 3. 移动冗余文件到归档
    print_header("归档冗余文件")
    moved_count = move_to_archive(REDUNDANT_FILES)
    print_info(f"共归档 {moved_count} 个文件")
    
    # 4. 显示整理后的结构
    show_directory_structure()
    
    # 5. 总结
    print_header("整理完成")
    print("\n✅ 核心文件：", len([f for f in CORE_FILES if (SELF_EVOLUTION_DIR / f).exists()]))
    print("✅ 辅助文件：", len([f for f in HELPER_FILES if (SELF_EVOLUTION_DIR / f).exists()]))
    print("✅ 归档文件：", moved_count)
    print("\n💡 提示：归档文件保留在 _archive/ 目录，需要时可以恢复")
    print("")

if __name__ == "__main__":
    main()
