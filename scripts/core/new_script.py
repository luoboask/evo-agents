#!/usr/bin/env python3
"""
new_script.py - 生成新脚本模板

用法:
    python3 scripts/core/new_script.py my_feature

生成:
    scripts/my_feature.py (带完整模板)
"""
import sys
from pathlib import Path

TEMPLATE = '''#!/usr/bin/env python3
"""
{script_name}.py - {{description}}

用法:
    python3 scripts/{script_name}.py [options]
    
示例:
    python3 scripts/{script_name}.py --agent demo-agent
    EVO_WORKSPACE=/tmp/test python3 scripts/{script_name}.py
"""
import argparse
import sys
from pathlib import Path

# 统一路径解析（优先级：env > config > derive）
from path_utils import resolve_workspace, resolve_agent_memory, resolve_data_dir

WORKSPACE = resolve_workspace()


def main():
    parser = argparse.ArgumentParser(
        description="{{description}}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 scripts/{script_name}.py --agent demo-agent
    python3 scripts/{script_name}.py --workspace /tmp/my-workspace
        """
    )
    parser.add_argument("--agent", help="Agent 名称")
    parser.add_argument("--workspace", help="自定义 Workspace 路径（覆盖环境变量）")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--dry-run", "-n", action="store_true", help="空运行（不实际修改）")
    args = parser.parse_args()
    
    # 支持 --workspace 覆盖
    if args.workspace:
        global WORKSPACE
        WORKSPACE = Path(args.workspace)
    
    # 获取各目录路径
    memory_dir = resolve_agent_memory(args.agent)
    data_dir = resolve_data_dir()
    
    if args.verbose:
        print(f"Workspace: {{WORKSPACE}}")
        print(f"Memory Dir: {{memory_dir}}")
        print(f"Data Dir: {{data_dir}}")
    
    # TODO: 实现业务逻辑
    print("✅ 脚本已就绪，请实现业务逻辑")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

def main():
    if len(sys.argv) < 2:
        print("用法：python3 new_script.py <script_name>")
        print("")
        print("示例:")
        print("   python3 new_script.py my_feature")
        print("   python3 new_script.py data_export")
        sys.exit(1)
    
    script_name = sys.argv[1]
    
    # 获取 workspace 根目录
    workspace = Path(__file__).resolve().parent.parent.parent
    
    # 默认输出到 scripts/ 根目录
    output = workspace / "scripts" / f"{script_name}.py"
    
    # 如果 scripts/core/ 下已存在，提示放到 scripts/user/
    core_script = workspace / "scripts" / "core" / f"{script_name}.py"
    if core_script.exists():
        print(f"⚠️  核心脚本已存在：{core_script}")
        print(f"💡 建议将自定义脚本放在 scripts/user/{script_name}.py")
        output = workspace / "scripts" / "user" / f"{script_name}.py"
        output.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入模板
    output.write_text(TEMPLATE.format(script_name=script_name))
    output.chmod(0o755)
    
    print(f"✅ 创建：{output}")
    print("")
    print("📝 下一步:")
    print(f"   1. 编辑 {output}")
    print("   2. 替换 {{description}} 为实际描述")
    print("   3. 实现 main() 函数中的业务逻辑")
    print("")
    print("🧪 测试:")
    print(f"   python3 {output} --help")
    print(f"   python3 {output} --agent demo-agent --verbose")


if __name__ == "__main__":
    main()
