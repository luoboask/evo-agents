# -*- coding: utf-8 -*-
"""
Programming Domain Plugin v2.0 - 编程开发领域插件

参考 Claude Code Tool.ts 规范设计
Reference: Claude Code Tool Interface Design

适用于：Web 开发、移动应用、后端服务、前端界面、数据库设计等
Language: Bilingual (English + 中文)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class ToolCharacteristic(Enum):
    """Tool characteristics / 工具特征"""
    CONCURRENCY_SAFE = "concurrency_safe"  # 可并发执行
    READ_ONLY = "read_only"  # 只读操作
    DESTRUCTIVE = "destructive"  # 破坏性操作
    REQUIRES_AUTH = "requires_auth"  # 需要认证


@dataclass
class ToolDefinition:
    """Tool definition following Claude Code pattern"""
    name: str
    description: str  # One-line capability phrase
    search_hint: str  # 3-10 words for keyword matching
    input_schema: Dict[str, Any]
    characteristics: List[ToolCharacteristic] = field(default_factory=list)
    
    def is_concurrency_safe(self) -> bool:
        return ToolCharacteristic.CONCURRENCY_SAFE in self.characteristics
    
    def is_read_only(self) -> bool:
        return ToolCharacteristic.READ_ONLY in self.characteristics
    
    def is_destructive(self) -> bool:
        return ToolCharacteristic.DESTRUCTIVE in self.characteristics


@dataclass
class ValidationResult:
    """Validation result"""
    result: bool
    message: str = ""
    error_code: int = 0


class ProgrammingPlugin:
    """
    Programming Domain Plugin v2.0
    
    Following Claude Code Tool.ts interface design:
    - Clear tool definitions with schemas
    - Validation before execution
    - Progress tracking
    - Concurrency safety checks
    """
    
    name = 'programming'
    display_name = 'Programming & Software Development'
    description = 'Complete software development with Claude Code-style tools'
    version = '2.0.0'
    languages = ['en', 'zh']
    
    def get_tools(self) -> List[ToolDefinition]:
        """Get all available tools"""
        return [
            ToolDefinition(
                name="create_project",
                description="Initialize new project with structure",
                search_hint="project initialization scaffolding",
                input_schema={
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "project_type": {
                            "type": "string",
                            "enum": ["web_app", "api_service", "mobile_app"]
                        },
                        "language": {
                            "type": "string",
                            "enum": ["typescript", "python", "go"]
                        }
                    },
                    "required": ["project_name", "project_type", "language"]
                },
                characteristics=[ToolCharacteristic.DESTRUCTIVE]
            ),
            
            ToolDefinition(
                name="implement_feature",
                description="Implement feature with tests",
                search_hint="feature implementation coding",
                input_schema={
                    "type": "object",
                    "properties": {
                        "feature_name": {"type": "string"},
                        "requirements": {"type": "array", "items": {"type": "string"}},
                        "acceptance_criteria": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["feature_name", "requirements"]
                },
                characteristics=[ToolCharacteristic.DESTRUCTIVE]
            ),
            
            ToolDefinition(
                name="run_tests",
                description="Execute test suite with coverage",
                search_hint="testing unit integration coverage",
                input_schema={
                    "type": "object",
                    "properties": {
                        "test_type": {
                            "type": "string",
                            "enum": ["unit", "integration", "e2e", "all"]
                        },
                        "coverage_threshold": {"type": "number", "default": 80}
                    },
                    "required": ["test_type"]
                },
                characteristics=[ToolCharacteristic.CONCURRENCY_SAFE, ToolCharacteristic.READ_ONLY]
            ),
            
            ToolDefinition(
                name="code_review",
                description="Review code for quality and security",
                search_hint="review lint security quality",
                input_schema={
                    "type": "object",
                    "properties": {
                        "files": {"type": "array", "items": {"type": "string"}},
                        "focus_areas": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["security", "performance", "style", "tests"]
                            }
                        }
                    },
                    "required": ["files"]
                },
                characteristics=[ToolCharacteristic.CONCURRENCY_SAFE, ToolCharacteristic.READ_ONLY]
            ),
            
            ToolDefinition(
                name="deploy",
                description="Deploy to staging or production",
                search_hint="deployment staging production release",
                input_schema={
                    "type": "object",
                    "properties": {
                        "environment": {
                            "type": "string",
                            "enum": ["staging", "production"]
                        },
                        "strategy": {
                            "type": "string",
                            "enum": ["blue-green", "canary", "rolling"]
                        }
                    },
                    "required": ["environment"]
                },
                characteristics=[ToolCharacteristic.DESTRUCTIVE, ToolCharacteristic.REQUIRES_AUTH]
            )
        ]
    
    def get_decomposition_template(self) -> str:
        """Task decomposition template"""
        return """
## Software Development Task Decomposition

### 1. Requirements Analysis
- User stories and acceptance criteria
- Functional and non-functional requirements
- Technical constraints and dependencies

### 2. Architecture Design
- Technology stack selection
- System architecture (monolith/microservices)
- API design and data models

### 3. Implementation Plan
- Break down into small, testable units
- Define interfaces between components
- Identify risks and mitigation strategies

### 4. Development
- Implement with tests (TDD when possible)
- Follow coding standards and best practices
- Continuous integration and code review

### 5. Testing & QA
- Unit tests (>80% coverage)
- Integration tests
- E2E tests for critical paths

### 6. Deployment
- Staging deployment and validation
- Production deployment with rollback plan
- Monitoring and alerting setup
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """Acceptance criteria checklist"""
        return [
            "✅ Code builds without errors",
            "✅ All tests pass (>80% coverage)",
            "✅ Code follows style guide (lint passes)",
            "✅ Security scan clean (no high severity issues)",
            "✅ API documentation complete",
            "✅ Performance benchmarks met (<200ms response)",
            "✅ Error handling and logging implemented",
            "✅ Deployment tested in staging"
        ]
    
    def validate_tool_input(self, tool_name: str, input_data: Dict) -> ValidationResult:
        """
        Validate tool input before execution
        
        Following Claude Code pattern: validate before execute
        """
        tools = {tool.name: tool for tool in self.get_tools()}
        
        if tool_name not in tools:
            return ValidationResult(
                result=False,
                message=f"Unknown tool: {tool_name}",
                error_code=1
            )
        
        tool = tools[tool_name]
        schema = tool.input_schema
        
        # Simple validation (can be enhanced with jsonschema library)
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in input_data:
                return ValidationResult(
                    result=False,
                    message=f"Missing required field: {field}",
                    error_code=2
                )
        
        return ValidationResult(result=True)
    
    def get_tech_stack_recommendations(self, project_type: str) -> Dict[str, Any]:
        """Get recommended technology stack"""
        stacks = {
            'web_app': {
                'name': 'Full-Stack Web Application',
                'frontend': 'React + TypeScript + Vite',
                'backend': 'Node.js + Fastify/NestJS',
                'database': 'PostgreSQL + Prisma',
                'deployment': 'Docker + GitHub Actions'
            },
            'api_service': {
                'name': 'RESTful/GraphQL API Service',
                'runtime': 'Python + FastAPI',
                'database': 'PostgreSQL + Redis',
                'documentation': 'OpenAPI/Swagger',
                'deployment': 'Docker + Kubernetes'
            },
            'mobile_app': {
                'name': 'Cross-Platform Mobile Application',
                'framework': 'React Native + Expo',
                'state_management': 'Zustand/Redux',
                'testing': 'Detox + Jest'
            }
        }
        
        return stacks.get(project_type, stacks['web_app'])
    
    def get_best_practices(self) -> List[str]:
        """Best practices following industry standards"""
        return [
            "📝 Write self-documenting code with clear naming",
            "🧪 Test-Driven Development (TDD) when possible",
            "🔒 Security first: validate inputs, sanitize outputs",
            "📊 Use meaningful logging (INFO/WARN/ERROR levels)",
            "♻️ Follow DRY principle (Don't Repeat Yourself)",
            "🏗️ Apply SOLID principles for maintainability",
            "⚡ Optimize for performance but measure first",
            "🔐 Use environment variables for configuration"
        ]


def load_plugin():
    """Load plugin instance"""
    return ProgrammingPlugin()


if __name__ == '__main__':
    # Demo usage
    plugin = ProgrammingPlugin()
    
    print("=" * 70)
    print(f"Plugin: {plugin.name}")
    print(f"Version: {plugin.version}")
    print("=" * 70)
    
    print("\n🛠️ Available Tools:")
    for tool in plugin.get_tools():
        print(f"\n  • {tool.name}")
        print(f"    Description: {tool.description}")
        print(f"    Search Hint: {tool.search_hint}")
        print(f"    Characteristics:")
        if tool.is_concurrency_safe():
            print("      ✓ Concurrency Safe")
        if tool.is_read_only():
            print("      ✓ Read Only")
        if tool.is_destructive():
            print("      ⚠ Destructive")
    
    print("\n✅ Acceptance Criteria:")
    for criterion in plugin.get_acceptance_criteria():
        print(f"  {criterion}")
    
    print("\n💡 Best Practices:")
    for practice in plugin.get_best_practices():
        print(f"  {practice}")
