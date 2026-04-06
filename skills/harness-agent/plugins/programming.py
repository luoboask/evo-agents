# -*- coding: utf-8 -*-
"""
Programming Domain Plugin - 编程开发领域插件

简洁版设计，参考 Claude Code 理念但保持易用性
Simple design inspired by Claude Code but keeping it simple
"""

from typing import List, Dict


class ProgrammingPlugin:
    """编程开发领域插件 - 简洁版"""
    
    name = 'programming'
    description = 'Software development - Web/Mobile/Backend/Frontend'
    version = '2.0.0'
    
    def get_task_template(self) -> str:
        """任务分解模板"""
        return """
## 软件开发任务分解

1. **需求分析** - 用户故事、验收标准
2. **技术选型** - 技术栈、架构设计  
3. **开发实现** - 编码、单元测试
4. **代码审查** - Lint、安全检查
5. **测试验证** - 集成测试、E2E 测试
6. **部署上线** - 部署、监控
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """验收标准"""
        return [
            "✅ 代码编译/构建无错误",
            "✅ 测试覆盖率 >80%",
            "✅ Lint 检查通过",
            "✅ 无高危安全漏洞",
            "✅ API 文档完整",
            "✅ 性能达标 (响应<200ms)"
        ]
    
    def get_tools(self) -> List[Dict]:
        """
        可用工具列表
        
        每个工具包含:
        - name: 工具名称
        - desc: 简单描述
        - params: 关键参数
        - safe: 是否可并发/只读
        """
        return [
            {
                "name": "create_project",
                "desc": "创建新项目",
                "params": ["project_name", "project_type", "language"],
                "safe": False  # 会创建文件，不可并发
            },
            {
                "name": "implement_feature", 
                "desc": "实现功能",
                "params": ["feature_name", "requirements"],
                "safe": False  # 会修改代码
            },
            {
                "name": "run_tests",
                "desc": "运行测试",
                "params": ["test_type", "coverage_threshold"],
                "safe": True  # 只读，可并发
            },
            {
                "name": "code_review",
                "desc": "代码审查",
                "params": ["files", "focus_areas"],
                "safe": True  # 只读，可并发
            },
            {
                "name": "deploy",
                "desc": "部署应用",
                "params": ["environment", "strategy"],
                "safe": False  # 破坏性操作
            }
        ]
    
    def get_tech_stack(self, project_type: str) -> Dict:
        """推荐技术栈"""
        stacks = {
            'web_app': {
                'frontend': 'React + TypeScript',
                'backend': 'Node.js + FastAPI',
                'database': 'PostgreSQL',
                'deployment': 'Docker + GitHub Actions'
            },
            'api_service': {
                'runtime': 'Python + FastAPI',
                'database': 'PostgreSQL + Redis',
                'docs': 'OpenAPI/Swagger'
            },
            'mobile_app': {
                'framework': 'React Native + Expo',
                'state': 'Zustand/Redux'
            }
        }
        return stacks.get(project_type, stacks['web_app'])
    
    def get_best_practices(self) -> List[str]:
        """最佳实践"""
        return [
            "📝 代码自文档化，命名清晰",
            "🧪 测试驱动开发 (TDD)",
            "🔒 安全第一：验证输入，清理输出",
            "♻️ DRY 原则：不要重复自己",
            "⚡ 先测量再优化性能"
        ]
    
    def validate_input(self, tool_name: str, params: Dict) -> tuple:
        """
        简单验证输入
        
        Returns:
            (is_valid: bool, error_message: str)
        """
        required_params = {
            'create_project': ['project_name', 'project_type'],
            'implement_feature': ['feature_name', 'requirements'],
            'deploy': ['environment']
        }
        
        if tool_name not in required_params:
            return True, ""
        
        missing = [p for p in required_params[tool_name] if p not in params]
        if missing:
            return False, f"缺少必需参数：{', '.join(missing)}"
        
        return True, ""


def load_plugin():
    """加载插件"""
    return ProgrammingPlugin()


if __name__ == '__main__':
    plugin = ProgrammingPlugin()
    
    print("=" * 60)
    print(f"插件：{plugin.name}")
    print(f"版本：{plugin.version}")
    print("=" * 60)
    
    print("\n🛠️ 可用工具:")
    for tool in plugin.get_tools():
        safe_icon = "✅" if tool['safe'] else "⚠️"
        print(f"  {safe_icon} {tool['name']} - {tool['desc']}")
        print(f"      参数：{', '.join(tool['params'])}")
    
    print("\n✅ 验收标准:")
    for criterion in plugin.get_acceptance_criteria():
        print(f"  {criterion}")
    
    print("\n💡 最佳实践:")
    for practice in plugin.get_best_practices():
        print(f"  {practice}")
    
    print("\n🏗️ 技术栈推荐 (Web App):")
    stack = plugin.get_tech_stack('web_app')
    for key, value in stack.items():
        print(f"  {key}: {value}")
