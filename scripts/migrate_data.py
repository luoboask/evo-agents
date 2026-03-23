#!/usr/bin/env python3
"""
数据迁移脚本
将旧数据库迁移到新的 Memory Hub 结构
"""

import shutil
from pathlib import Path
from datetime import datetime


def migrate_data():
    """迁移数据"""
    
    # 旧数据路径
    old_memory_path = Path.home() / '.openclaw' / 'workspace-ai-baby-config' / 'memory'
    old_logs_path = Path.home() / '.openclaw' / 'workspace-ai-baby-config' / 'logs'
    
    # 新数据路径
    new_data_path = Path('/Users/dhr/.openclaw/workspace-ai-baby/data/ai-baby')
    new_memory_path = new_data_path / 'memory'
    new_logs_path = new_data_path / 'logs'
    
    print("🔄 开始数据迁移...")
    print(f"   源目录：{old_memory_path}")
    print(f"   目标目录：{new_data_path}")
    print()
    
    # 创建新目录
    new_memory_path.mkdir(parents=True, exist_ok=True)
    new_logs_path.mkdir(parents=True, exist_ok=True)
    
    # 迁移记忆数据库
    if old_memory_path.exists():
        print("📦 迁移记忆数据库...")
        for db_file in old_memory_path.glob('*.db'):
            target = new_memory_path / db_file.name
            shutil.copy2(db_file, target)
            print(f"   ✅ {db_file.name} → {target}")
    else:
        print("   ⚠️  旧记忆数据库不存在")
    
    # 迁移 RAG 评估日志
    if old_logs_path.exists():
        print("\n📦 迁移 RAG 评估日志...")
        eval_log = old_logs_path / 'evaluations.jsonl'
        if eval_log.exists():
            target = new_logs_path / 'evaluations.jsonl'
            shutil.copy2(eval_log, target)
            print(f"   ✅ evaluations.jsonl → {target}")
        else:
            print("   ⚠️  evaluations.jsonl 不存在")
    else:
        print("\n   ⚠️  旧日志目录不存在")
    
    # 迁移学习记录
    old_learning_path = Path('/Users/dhr/.openclaw/workspace-ai-baby/memory/learning')
    new_learning_path = new_data_path / 'learning'
    if old_learning_path.exists():
        print("\n📦 迁移学习记录...")
        shutil.copytree(old_learning_path, new_learning_path, dirs_exist_ok=True)
        print(f"   ✅ learning/ → {new_learning_path}")
    else:
        print("\n   ⚠️  学习记录不存在")
    
    print("\n" + "=" * 60)
    print("✅ 数据迁移完成！")
    print("=" * 60)
    print("\n新数据位置:")
    print(f"   记忆数据库：{new_memory_path}/")
    print(f"   RAG 日志：{new_logs_path}/")
    if old_learning_path.exists():
        print(f"   学习记录：{new_learning_path}/")
    print("\n⚠️  注意:")
    print("   1. 旧数据已保留，未删除")
    print("   2. 请验证新数据可用后再删除旧数据")
    print("   3. 更新 OPENCLAW_AGENT 环境变量以使用新数据")


if __name__ == '__main__':
    migrate_data()
