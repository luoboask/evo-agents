#!/usr/bin/env python3
"""
进化控制中心 - Evolution Control Center
自我进化系统的统一入口
"""

import sys
import subprocess
from pathlib import Path


class EvolutionControl:
    """进化控制中心"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.reflection_dir = self.workspace / "skills" / "self-reflection"
    
    def run_full_check(self):
        """运行完整的自我检查"""
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 15 + "🧬 自我进化控制中心" + " " * 32 + "║")
        print("╚" + "=" * 68 + "╝")
        print()
        
        # 1. 健康检查
        print("📊 步骤 1/4: 系统健康检查...")
        print("-" * 70)
        self._run_script("predictive_maintenance.py", ["--check"])
        print()
        
        # 2. 反思报告
        print("📊 步骤 2/4: 生成反思报告...")
        print("-" * 70)
        self._run_script("reflection.py", ["--report"])
        print()
        
        # 3. 改进建议
        print("📊 步骤 3/4: 生成改进计划...")
        print("-" * 70)
        self._run_script("improvement_generator.py", ["--generate"])
        print()
        
        # 4. 知识图谱
        print("📊 步骤 4/4: 更新知识图谱...")
        print("-" * 70)
        self._run_script("../knowledge-graph/builder.py", ["--build"])
        print()
        
        # 总结
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 20 + "✅ 自我检查完成!" + " " * 29 + "║")
        print("╚" + "=" * 68 + "╝")
        print()
        print("📋 下一步行动:")
        print("   1. 查看上面的改进建议")
        print("   2. 实施高优先级的改进")
        print("   3. 运行测试验证改进效果")
        print("   4. 记录改进到记忆系统")
        print()
    
    def _run_script(self, script_name, args):
        """运行子脚本"""
        script_path = self.reflection_dir / script_name
        if not script_path.exists():
            # 尝试其他路径
            script_path = self.workspace / "skills" / script_name.replace("../", "")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)] + args,
                capture_output=False,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            print(f"❌ 运行 {script_name} 失败: {e}")
            return False
    
    def auto_evolve(self):
        """自动执行进化"""
        print("🚀 启动自动进化模式...")
        print()
        print("这将自动:")
        print("  1. 分析系统健康")
        print("  2. 识别改进机会")
        print("  3. 生成改进代码")
        print("  4. 测试验证")
        print()
        print("⚠️  注意: 自动进化可能会修改文件，请确保已备份")
        print()
        
        response = input("是否继续? (yes/no): ")
        if response.lower() != 'yes':
            print("已取消")
            return
        
        # 这里可以实现自动改进逻辑
        print("\n🤖 自动进化功能开发中...")
        print("   目前请手动实施改进建议")
    
    def show_menu(self):
        """显示菜单"""
        print("\n" + "=" * 70)
        print("🧬 自我进化控制中心")
        print("=" * 70)
        print()
        print("可用命令:")
        print()
        print("  1. full-check     - 运行完整的自我检查")
        print("  2. health         - 系统健康检查")
        print("  3. reflect        - 生成反思报告")
        print("  4. improve        - 生成改进计划")
        print("  5. knowledge      - 更新知识图谱")
        print("  6. auto-evolve    - 自动进化模式")
        print("  7. help           - 显示帮助")
        print("  8. quit           - 退出")
        print()


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='进化控制中心')
    parser.add_argument('command', nargs='?', help='命令')
    parser.add_argument('--menu', action='store_true', help='显示菜单')
    
    args = parser.parse_args()
    
    control = EvolutionControl()
    
    if args.menu:
        control.show_menu()
    elif args.command == 'full-check':
        control.run_full_check()
    elif args.command == 'health':
        control._run_script("predictive_maintenance.py", ["--check"])
    elif args.command == 'reflect':
        control._run_script("reflection.py", ["--report"])
    elif args.command == 'improve':
        control._run_script("improvement_generator.py", ["--generate"])
    elif args.command == 'knowledge':
        control._run_script("../knowledge-graph/builder.py", ["--build"])
    elif args.command == 'auto-evolve':
        control.auto_evolve()
    elif args.command == 'help':
        control.show_menu()
    else:
        # 默认运行完整检查
        control.run_full_check()


if __name__ == '__main__':
    main()
