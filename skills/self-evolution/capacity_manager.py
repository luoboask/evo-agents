#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆容量管理 - 集成到自进化系统

功能:
- 自动检查记忆容量
- 超限警告
- 建议压缩
- 自动触发压缩
"""

import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 添加 workspace 到路径
workspace_path = Path.home() / '.openclaw' / 'workspace'
sys.path.insert(0, str(workspace_path))

try:
    from libs.memory_hub.hub import MemoryHub, MEMORY_LIMIT, USER_LIMIT
except ImportError:
    from memory_hub.hub import MemoryHub, MEMORY_LIMIT, USER_LIMIT


class CapacityManager:
    """记忆容量管理器"""
    
    def __init__(self, agent_name: str = 'main', workspace_root: Path = None):
        """
        初始化容量管理器
        
        Args:
            agent_name: Agent 名称
            workspace_root: Workspace 路径
        """
        self.workspace_root = workspace_root or Path.home() / '.openclaw' / 'workspace'
        self.hub = MemoryHub(agent_name=agent_name, workspace_root=self.workspace_root)
        
        # 警告阈值
        self.WARNING_THRESHOLD = 80.0  # 80% 时警告
        self.CRITICAL_THRESHOLD = 95.0  # 95% 时严重警告
        
        # 日志路径
        self.log_file = self.workspace_root / 'logs' / 'capacity_check.log'
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def check_capacity(self, verbose: bool = True) -> Dict:
        """
        检查记忆容量
        
        Args:
            verbose: 是否打印详细信息
            
        Returns:
            dict: 检查结果
        """
        memory_usage = self.hub.get_memory_usage()
        user_usage = self.hub.get_user_usage()
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'memory': memory_usage,
            'user': user_usage,
            'status': 'ok',
            'action_required': False,
            'suggestions': []
        }
        
        # 检查 MEMORY.md
        if memory_usage['percentage'] >= self.CRITICAL_THRESHOLD:
            result['status'] = 'critical'
            result['action_required'] = True
            result['suggestions'].append(
                f"🚨 MEMORY.md 使用率超过 {self.CRITICAL_THRESHOLD}% ({memory_usage['percentage']}%)，"
                f"需要立即压缩！"
            )
        elif memory_usage['percentage'] >= self.WARNING_THRESHOLD:
            result['status'] = 'warning'
            result['action_required'] = True
            result['suggestions'].append(
                f"⚠️  MEMORY.md 使用率超过 {self.WARNING_THRESHOLD}% ({memory_usage['percentage']}%)，"
                f"建议压缩。"
            )
        
        # 检查 USER.md
        if user_usage['percentage'] >= self.CRITICAL_THRESHOLD:
            result['status'] = 'critical' if result['status'] == 'ok' else result['status']
            result['action_required'] = True
            result['suggestions'].append(
                f"🚨 USER.md 使用率超过 {self.CRITICAL_THRESHOLD}% ({user_usage['percentage']}%)，"
                f"需要压缩！"
            )
        elif user_usage['percentage'] >= self.WARNING_THRESHOLD:
            result['status'] = 'warning' if result['status'] == 'ok' else result['status']
            result['action_required'] = True
            result['suggestions'].append(
                f"⚠️  USER.md 使用率超过 {self.WARNING_THRESHOLD}% ({user_usage['percentage']}%)，"
                f"建议压缩。"
            )
        
        # 打印结果
        if verbose:
            self._print_report(result)
        
        # 记录日志
        self._log_result(result)
        
        return result
    
    def _print_report(self, result: Dict):
        """打印容量报告"""
        print("=" * 70)
        print("📊 记忆容量检查")
        print("=" * 70)
        
        memory = result['memory']
        user = result['user']
        
        # MEMORY.md 状态
        status_icon = "✅" if memory['percentage'] < self.WARNING_THRESHOLD else "⚠️"
        print(f"\n{status_icon} MEMORY.md: {memory['percentage']}% — {memory['current']:,}/{MEMORY_LIMIT:,} chars")
        print(f"   可用空间：{memory['available']:,} chars")
        
        # USER.md 状态
        status_icon = "✅" if user['percentage'] < self.WARNING_THRESHOLD else "⚠️"
        print(f"\n{status_icon} USER.md: {user['percentage']}% — {user['current']:,}/{USER_LIMIT:,} chars")
        print(f"   可用空间：{user['available']:,} chars")
        
        # 建议
        if result['suggestions']:
            print("\n💡 建议:")
            for suggestion in result['suggestions']:
                print(f"   {suggestion}")
            
            if result['action_required']:
                print("\n🔧 运行压缩:")
                print(f"   python3 scripts/compress_memory.py")
        
        # 状态
        print(f"\n📈 总体状态：{result['status'].upper()}")
        print("=" * 70)
    
    def _log_result(self, result: Dict):
        """记录日志"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{result['timestamp']}] Status: {result['status']}\n")
            f.write(f"  MEMORY: {result['memory']['percentage']}% ({result['memory']['current']}/{MEMORY_LIMIT})\n")
            f.write(f"  USER: {result['user']['percentage']}% ({result['user']['current']}/{USER_LIMIT})\n")
            
            if result['suggestions']:
                for suggestion in result['suggestions']:
                    f.write(f"  {suggestion}\n")
    
    def auto_compress(self, dry_run: bool = True) -> Dict:
        """
        自动压缩记忆
        
        Args:
            dry_run: 是否仅预览
            
        Returns:
            dict: 压缩结果
        """
        import subprocess
        
        result = {
            'success': False,
            'message': '',
            'dry_run': dry_run
        }
        
        try:
            # 运行压缩脚本
            cmd = [
                sys.executable,
                str(self.workspace_root / 'scripts' / 'compress_memory.py')
            ]
            
            if dry_run:
                cmd.append('--dry-run')
            
            output = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.workspace_root)
            )
            
            result['output'] = output.stdout
            result['success'] = output.returncode == 0
            
            if not dry_run and result['success']:
                # 检查压缩后的状态
                new_usage = self.hub.get_memory_usage()
                result['new_usage'] = new_usage
                result['message'] = f"压缩完成！新使用率：{new_usage['percentage']}%"
            else:
                result['message'] = "预览完成" if dry_run else "压缩失败"
        
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            result['message'] = f"压缩出错：{e}"
        
        return result
    
    def before_add_check(self, content: str) -> Dict:
        """
        添加记忆前的容量检查
        
        Args:
            content: 要添加的记忆内容
            
        Returns:
            dict: 检查结果
        """
        check = self.hub.check_memory_capacity(content)
        
        result = {
            'can_add': check['new_would_fit'],
            'current': check['current'],
            'limit': check['limit'],
            'new_length': len(content),
            'would_exceed': not check['new_would_fit'],
            'message': ''
        }
        
        if not result['can_add']:
            result['message'] = (
                f"⚠️  添加此记忆 ({result['new_length']} chars) 后会超出限制 "
                f"({check['usage']} → 超出 {result['new_length'] - self.hub.get_memory_usage()['available']} chars)"
            )
        
        return result


def cmd_check(args):
    """容量检查命令"""
    manager = CapacityManager()
    result = manager.check_capacity(verbose=True)
    
    if result['action_required']:
        sys.exit(1)  # 需要行动时返回非零退出码
    sys.exit(0)


def cmd_auto_compress(args):
    """自动压缩命令"""
    manager = CapacityManager()
    
    # 先检查
    check_result = manager.check_capacity(verbose=False)
    
    if check_result['status'] == 'ok':
        print("✅ 记忆容量充足，无需压缩")
        sys.exit(0)
    
    print(f"⚠️  检测到容量问题：{check_result['status']}")
    
    # 执行压缩
    if args.dry_run:
        print("\n🔍 预览压缩效果...\n")
    else:
        print("\n🔄 开始压缩...\n")
    
    result = manager.auto_compress(dry_run=args.dry_run)
    
    print(result['output'])
    
    if result['success'] and not args.dry_run:
        print(f"\n✅ {result['message']}")
    else:
        print(f"\n⚠️  {result['message']}")


def cmd_before_add(args):
    """添加前检查命令"""
    manager = CapacityManager()
    result = manager.before_add_check(args.content)
    
    print(f"📊 容量检查:")
    print(f"   当前：{result['current']:,} chars")
    print(f"   限制：{result['limit']:,} chars")
    print(f"   新内容：{result['new_length']:,} chars")
    
    if result['can_add']:
        print(f"\n✅ 可以添加")
        sys.exit(0)
    else:
        print(f"\n❌ {result['message']}")
        print(f"\n💡 建议先运行：python3 main.py capacity-check")
        sys.exit(1)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='记忆容量管理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 capacity_manager.py check              # 容量检查
  python3 capacity_manager.py auto-compress      # 自动压缩（预览）
  python3 capacity_manager.py auto-compress --exec  # 执行压缩
  python3 capacity_manager.py before-add "内容"   # 添加前检查
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # check 命令
    check_parser = subparsers.add_parser('check', help='容量检查')
    check_parser.set_defaults(func=cmd_check)
    
    # auto-compress 命令
    compress_parser = subparsers.add_parser('auto-compress', help='自动压缩')
    compress_parser.add_argument('--dry-run', action='store_true', default=True, help='预览模式')
    compress_parser.add_argument('--exec', action='store_true', dest='execute', help='执行压缩')
    compress_parser.set_defaults(func=cmd_auto_compress)
    
    # before-add 命令
    before_add_parser = subparsers.add_parser('before-add', help='添加前检查')
    before_add_parser.add_argument('content', type=str, help='要添加的内容')
    before_add_parser.set_defaults(func=cmd_before_add)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()
