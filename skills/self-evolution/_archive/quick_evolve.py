#!/usr/bin/env python3
"""
快速记录进化事件 - 自动草拟，用户确认

用法：
  python3 quick_evolve.py "实现了用户登录功能"
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))
from self_evolution_real import RealSelfEvolution


def auto_detect_type(description: str) -> str:
    """自动检测事件类型"""
    desc_lower = description.lower()
    
    if any(kw in desc_lower for kw in ['bug', '修复', '错误', '问题', 'fix']):
        return 'BUG_FIX'
    elif any(kw in desc_lower for kw in ['优化', '重构', '改进', 'improve', 'refactor']):
        return 'CODE_IMPROVED'
    elif any(kw in desc_lower for kw in ['学习', '理解', '研究', 'learn', 'study']):
        return 'KNOWLEDGE_GAINED'
    elif any(kw in desc_lower for kw in ['功能', '实现', '添加', 'feature', 'add']):
        return 'FEATURE_ADDED'
    else:
        return 'FEATURE_ADDED'  # 默认


def suggest_lesson(description: str, event_type: str) -> str:
    """建议经验教训（基于关键词）"""
    suggestions = {
        'BUG_FIX': [
            "需要增加边界检查",
            "应该添加单元测试覆盖此场景",
            "输入验证很重要"
        ],
        'FEATURE_ADDED': [
            "设计时考虑了扩展性",
            "使用了 XX 设计模式",
            "性能优化点：XX"
        ],
        'CODE_IMPROVED': [
            "提取了公共逻辑，减少重复",
            "使用了更好的数据结构",
            "代码可读性提升"
        ],
        'KNOWLEDGE_GAINED': [
            "核心概念是 XX",
            "可以应用到 XX 场景",
            "与之前的 XX 知识相关联"
        ]
    }
    
    return suggestions.get(event_type, ["记录具体收获"])[0]


def quick_evolve(description: str, auto_files: list = None):
    """快速记录进化事件"""
    print("=" * 70)
    print("⚡ 快速记录进化事件")
    print("=" * 70)
    
    # 自动检测类型
    event_type = auto_detect_type(description)
    print(f"\n📋 自动检测类型：{event_type}")
    
    # 建议经验教训
    suggested_lesson = suggest_lesson(description, event_type)
    print(f"💡 建议经验教训：{suggested_lesson}")
    
    # 自动检测文件（如果有 git）
    if auto_files is None:
        auto_files = detect_changed_files()
        if auto_files:
            print(f"📁 检测到修改的文件：{', '.join(auto_files[:5])}")
    
    # 显示草拟内容
    print("\n" + "=" * 70)
    print("📝 草拟内容:")
    print("=" * 70)
    print(f"类型：{event_type}")
    print(f"描述：{description}")
    print(f"经验：{suggested_lesson}")
    print(f"文件：{', '.join(auto_files) if auto_files else '无'}")
    
    # 用户确认
    print("\n" + "=" * 70)
    print("确认操作:")
    print("  [Enter] 使用建议保存")
    print("  [e] 编辑经验教训")
    print("  [q] 取消")
    print("=" * 70)
    
    choice = input("你的选择：").strip().lower()
    
    if choice == 'q':
        print("❌ 已取消")
        return
    
    if choice == 'e':
        lesson = input("输入经验教训：").strip()
    else:
        lesson = suggested_lesson
    
    # 保存
    evolution = RealSelfEvolution()
    event = evolution.record_evolution(
        event_type=event_type,
        description=description,
        lesson_learned=lesson,
        files_changed=auto_files
    )
    
    print(f"\n✅ 已保存！事件 ID: {event.get('id', 'N/A')}")
    print("=" * 70)


def detect_changed_files() -> list:
    """检测最近修改的文件（git）"""
    import subprocess
    try:
        # 获取最近修改的 5 个文件
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            files = result.stdout.strip().split('\n')
            return [f for f in files if f][:5]
    except:
        pass
    return []


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python3 quick_evolve.py \"描述你的工作\"")
        print("\n示例:")
        print('  python3 quick_evolve.py "实现了用户登录功能"')
        print('  python3 quick_evolve.py "修复了空指针 Bug"')
        sys.exit(1)
    
    description = ' '.join(sys.argv[1:])
    quick_evolve(description)
