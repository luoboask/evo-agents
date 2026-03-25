#!/usr/bin/env python3
"""
应用自进化集成到 sandbox-agent

这个脚本会：
1. 修改 agent.py 导入 evolution_integration
2. 在关键位置添加进化事件记录
3. 在联调完成后添加学习调用
"""

import sys
from pathlib import Path

# 读取 agent.py
agent_file = Path(__file__).parent / 'agent.py'
with open(agent_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 70)
print("🔧 应用自进化集成到 sandbox-agent")
print("=" * 70)

# 1. 添加导入
print("\n1. 添加导入...")
import_code = '''
# 导入自进化集成
import sys
EVOLUTION_PATH = Path(__file__).parent.parent.parent / 'skills' / 'self-evolution-5.0'
sys.path.insert(0, str(EVOLUTION_PATH))
MEMORY_SEARCH_PATH = Path(__file__).parent.parent.parent / 'skills' / 'memory-search'
sys.path.insert(0, str(MEMORY_SEARCH_PATH))
from evolution_integration import SandboxEvolutionIntegration
'''

# 在 import 部分添加
if 'from evolution_integration import' not in content:
    content = content.replace(
        'from pathlib import Path\n',
        'from pathlib import Path\n' + import_code
    )
    print("   ✅ 已添加导入")
else:
    print("   ⚠️ 导入已存在")

# 2. 修改类文档字符串
print("\n2. 更新类文档...")
content = content.replace(
    'Sandbox Agent - 可管理的联调沙箱 Agent',
    'Sandbox Agent - 可管理的联调沙箱 Agent（集成自进化能力）'
)
content = content.replace(
    '- 支持并行执行多个需求联调',
    '- 支持并行执行多个需求联调\n    - 自动记录进化事件和学习经验'
)
print("   ✅ 已更新文档")

# 3. 添加自进化初始化
print("\n3. 添加自进化初始化...")
init_addition = '''
        # 自进化集成
        self.evolution = SandboxEvolutionIntegration()
        
'''
content = content.replace(
    'print(f"🚀 Sandbox Agent 初始化完成")\n        print(f"   工作目录：{self.workspace}")',
    'print(f"🚀 Sandbox Agent 初始化完成（集成自进化能力）")\n        print(f"   工作目录：{self.workspace}")\n        print(f"   自进化：已启用")'
)
content = content.replace(
    'self.active_sessions = {}  # 追踪活跃的 OpenClaw sessions\n        \n        print',
    'self.active_sessions = {}  # 追踪活跃的 OpenClaw sessions\n        \n        # 自进化集成\n        self.evolution = SandboxEvolutionIntegration()\n        \n        print'
)
print("   ✅ 已添加初始化")

# 4. 在 create_instance 中添加事件记录
print("\n4. 添加 create_instance 事件记录...")
create_addition = '''
        # 记录沙箱创建事件
        if hasattr(self, 'evolution'):
            self.evolution.record_sandbox_event(
                event_type='SANDBOX_CREATED',
                instance_id=instance_id,
                details={
                    'requirement_id': requirement_id,
                    'description': f'创建{requirement_id}沙箱',
                    'config': config
                }
            )
        
'''
# 在 return instance_id 前添加
content = content.replace(
    'return instance_id\n    \n    async def start_instance',
    create_addition + '        return instance_id\n    \n    async def start_instance'
)
print("   ✅ 已添加 create_instance 事件记录")

# 5. 在 run_integration 完成后添加学习
print("\n5. 添加 run_integration 学习调用...")
learn_addition = '''
            # 从联调报告学习
            if hasattr(self, 'evolution'):
                self.evolution.learn_from_integration_report(instance_id, report)
            
'''
content = content.replace(
    'return report\n            \n        except Exception as e:',
    learn_addition + '            return report\n            \n        except Exception as e:'
)
print("   ✅ 已添加学习调用")

# 6. 保存修改
print("\n6. 保存修改...")
with open(agent_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("   ✅ 已保存到 agent.py")

# 7. 创建测试脚本
print("\n7. 创建测试脚本...")
test_code = '''#!/usr/bin/env python3
"""
测试 sandbox-agent 的自进化集成
"""

import asyncio
import sys
from pathlib import Path

# 添加路径
EVOLUTION_PATH = Path(__file__).parent.parent.parent / 'skills' / 'self-evolution-5.0'
sys.path.insert(0, str(EVOLUTION_PATH))
MEMORY_SEARCH_PATH = Path(__file__).parent.parent.parent / 'skills' / 'memory-search'
sys.path.insert(0, str(MEMORY_SEARCH_PATH))

from agent import SandboxAgent


async def main():
    """测试主函数"""
    print("=" * 70)
    print("🧪 Sandbox Agent 自进化集成测试")
    print("=" * 70)
    
    # 创建 Agent
    print("\\n1. 创建 Sandbox Agent")
    agent = SandboxAgent()
    
    # 创建实例
    print("\\n2. 创建沙箱实例")
    instance_id = await agent.create_instance(
        requirement_id='REQ-TEST-001',
        config={
            'frontend_code': './frontend/test',
            'backend_code': './backend/test',
            'requirement_desc': '测试功能'
        }
    )
    
    # 获取统计
    print("\\n3. 获取进化统计")
    stats = agent.evolution.get_evolution_stats()
    print(f"   记忆总数：{stats['memory_stream']['total_memories']}")
    print(f"   进化事件：{stats['evolution_events']['total_events']}")
    
    # 生成报告
    print("\\n4. 生成学习报告")
    report = agent.evolution.generate_learning_report(days=1)
    print(f"   时期：{report['period']}")
    print(f"   洞察：{report['insights']}")
    
    print("\\n" + "=" * 70)
    print("✅ 测试完成！")
    print("=" * 70)


if __name__ == '__main__':
    asyncio.run(main())
'''

test_file = Path(__file__).parent / 'test_evolution.py'
with open(test_file, 'w', encoding='utf-8') as f:
    f.write(test_code)
print("   ✅ 已创建 test_evolution.py")

print("\n" + "=" * 70)
print("✅ 自进化集成应用完成！")
print("=" * 70)
print("\n📝 修改内容:")
print("   1. ✅ 添加 evolution_integration 导入")
print("   2. ✅ 添加 SandboxEvolutionIntegration 初始化")
print("   3. ✅ 在 create_instance 中添加事件记录")
print("   4. ✅ 在 run_integration 中添加学习调用")
print("   5. ✅ 创建测试脚本 test_evolution.py")
print("\n🚀 下一步:")
print("   python3 test_evolution.py")
print("=" * 70)
