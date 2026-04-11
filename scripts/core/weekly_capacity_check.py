#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每周记忆容量检查

用法:
  python3 scripts/weekly_capacity_check.py
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加 workspace 到路径
workspace_path = Path.home() / '.openclaw' / 'workspace'
sys.path.insert(0, str(workspace_path))
sys.path.insert(0, str(workspace_path / 'skills' / 'self-evolution'))

from capacity_manager import CapacityManager


def main():
    """每周容量检查"""
    print("=" * 70)
    print("📅 每周记忆容量检查")
    print(f"日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    manager = CapacityManager(workspace_root=workspace_path)
    result = manager.check_capacity(verbose=True)
    
    # 如果需要行动，给出建议
    if result['action_required']:
        print("\n" + "=" * 70)
        print("🔧 建议操作:")
        print("=" * 70)
        
        if result['status'] == 'critical':
            print("\n🚨 紧急：立即压缩记忆")
            print("   命令：cd /Users/dhr/.openclaw/workspace/skills/self-evolution")
            print("         python3 main.py capacity-compress --exec")
        elif result['status'] == 'warning':
            print("\n⚠️  建议：考虑压缩记忆")
            print("   命令：cd /Users/dhr/.openclaw/workspace/skills/self-evolution")
            print("         python3 main.py capacity-compress")
        
        print("\n📊 查看详细报告:")
        print("   命令：cd /Users/dhr/.openclaw/workspace/skills/self-evolution")
        print("         python3 main.py capacity-check")
    else:
        print("\n✅ 记忆容量健康，无需操作")
    
    # 记录到日志
    log_file = workspace_path / 'logs' / 'weekly_capacity_check.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{datetime.now().isoformat()}] Weekly Check\n")
        f.write(f"  Status: {result['status']}\n")
        f.write(f"  MEMORY: {result['memory']['percentage']}% ({result['memory']['current']}/{MEMORY_LIMIT})\n")
        f.write(f"  USER: {result['user']['percentage']}% ({result['user']['current']}/{USER_LIMIT})\n")
        
        if result['suggestions']:
            for suggestion in result['suggestions']:
                f.write(f"  {suggestion}\n")


if __name__ == '__main__':
    # 导入常量
    from libs.memory_hub.hub import MEMORY_LIMIT, USER_LIMIT
    main()
