#!/usr/bin/env python3
"""
Test script for Programming Plugin integration with Harness Agent
编程插件集成测试脚本
"""

import sys
sys.path.insert(0, 'plugins')

from programming import load_plugin


def test_basic_usage():
    """测试基本使用"""
    print("=" * 70)
    print("🧪 测试 1: 基本使用")
    print("=" * 70)
    
    plugin = load_plugin()
    
    # 获取工具列表
    tools = plugin.get_tools()
    print(f"\n可用工具数量：{len(tools)}")
    
    for tool in tools:
        safe_icon = "✅" if tool['safe'] else "⚠️"
        print(f"  {safe_icon} {tool['name']}: {tool['desc']}")
    
    print("\n✅ 测试通过!")


def test_validation():
    """测试验证功能"""
    print("\n" + "=" * 70)
    print("🧪 测试 2: 输入验证")
    print("=" * 70)
    
    plugin = load_plugin()
    
    test_cases = [
        {
            "name": "缺少必需参数",
            "tool": "create_project",
            "params": {"project_name": "my-app"},
            "expected_valid": False
        },
        {
            "name": "参数完整",
            "tool": "create_project",
            "params": {
                "project_name": "my-app",
                "project_type": "web_app",
                "language": "typescript"
            },
            "expected_valid": True
        },
        {
            "name": "部署缺少环境",
            "tool": "deploy",
            "params": {"strategy": "blue-green"},
            "expected_valid": False
        }
    ]
    
    passed = 0
    failed = 0
    
    for case in test_cases:
        is_valid, error = plugin.validate_input(case['tool'], case['params'])
        
        if is_valid == case['expected_valid']:
            print(f"  ✅ {case['name']}: 通过")
            passed += 1
        else:
            print(f"  ❌ {case['name']}: 失败")
            print(f"     期望：{case['expected_valid']}, 实际：{is_valid}")
            if error:
                print(f"     错误：{error}")
            failed += 1
    
    print(f"\n结果：{passed} 通过，{failed} 失败")
    if failed == 0:
        print("✅ 所有验证测试通过!")


def test_tech_stack():
    """测试技术栈推荐"""
    print("\n" + "=" * 70)
    print("🧪 测试 3: 技术栈推荐")
    print("=" * 70)
    
    plugin = load_plugin()
    
    project_types = ['web_app', 'api_service', 'mobile_app']
    
    for ptype in project_types:
        print(f"\n{ptype}:")
        stack = plugin.get_tech_stack(ptype)
        for key, value in stack.items():
            print(f"  • {key}: {value}")
    
    print("\n✅ 技术栈推荐正常!")


def test_harness_integration():
    """模拟 Harness Agent 集成"""
    print("\n" + "=" * 70)
    print("🧪 测试 4: Harness Agent 集成模拟")
    print("=" * 70)
    
    plugin = load_plugin()
    
    # 模拟 Harness Agent 调用
    print("\n场景：开发一个博客系统")
    print("-" * 70)
    
    # Step 1: 获取任务模板
    print("\n1️⃣ 任务分解:")
    print(plugin.get_task_template())
    
    # Step 2: 获取推荐技术栈
    print("\n2️⃣ 技术栈推荐:")
    stack = plugin.get_tech_stack('web_app')
    for key, value in stack.items():
        print(f"   {key}: {value}")
    
    # Step 3: 规划工具使用
    print("\n3️⃣ 工具使用规划:")
    tools = plugin.get_tools()
    
    # 安全工具可以并发
    safe_tools = [t for t in tools if t['safe']]
    unsafe_tools = [t for t in tools if not t['safe']]
    
    print(f"   可并发工具 ({len(safe_tools)}个):")
    for tool in safe_tools:
        print(f"     ✅ {tool['name']}")
    
    print(f"   需串行工具 ({len(unsafe_tools)}个):")
    for tool in unsafe_tools:
        print(f"     ⚠️ {tool['name']}")
    
    # Step 4: 验收标准
    print("\n4️⃣ 验收标准:")
    for criterion in plugin.get_acceptance_criteria():
        print(f"   {criterion}")
    
    # Step 5: 最佳实践提醒
    print("\n5️⃣ 最佳实践:")
    for practice in plugin.get_best_practices()[:3]:  # 只显示前 3 个
        print(f"   {practice}")
    
    print("\n✅ Harness 集成模拟完成!")


def main():
    """运行所有测试"""
    print("\n" + "🚀" * 35)
    print("Programming Plugin Integration Tests")
    print("编程插件集成测试")
    print("🚀" * 35 + "\n")
    
    try:
        test_basic_usage()
        test_validation()
        test_tech_stack()
        test_harness_integration()
        
        print("\n" + "=" * 70)
        print("🎉 所有测试完成!")
        print("=" * 70)
        print("\n下一步:")
        print("  1. 在真实 Harness 任务中使用插件")
        print("  2. 创建更多领域插件 (电商、数据分析等)")
        print("  3. 推送到 GitHub")
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
