#!/usr/bin/env python3
"""
Sandbox Agent - 可管理的联调沙箱 Agent（集成自进化能力）
基于 OpenClaw 的 sessions_spawn 实现
"""

import json
import asyncio
import uuid
from datetime import datetime
from pathlib import Path

# 导入自进化集成
import sys
EVOLUTION_PATH = Path(__file__).parent.parent.parent / 'skills' / 'self-evolution-5.0'
sys.path.insert(0, str(EVOLUTION_PATH))
MEMORY_SEARCH_PATH = Path(__file__).parent.parent.parent / 'skills' / 'memory-search'
sys.path.insert(0, str(MEMORY_SEARCH_PATH))
from evolution_integration import SandboxEvolutionIntegration


class SandboxAgent:
    """
    沙箱 Agent
    - 管理多个沙箱实例
    - 每个实例包含 Frontend/Backend/Test 三个 Session
    - 支持并行执行多个需求联调
    - 自动记录进化事件和学习经验
    """
    
    def __init__(self, workspace_dir=None):
        self.workspace = Path(workspace_dir) if workspace_dir else Path.home() / '.sandbox-agent'
        self.workspace.mkdir(exist_ok=True)
        
        self.instances = {}  # instance_id -> SandboxInstance
        self.active_sessions = {}  # 追踪活跃的 OpenClaw sessions
        
        # 自进化集成
        self.evolution = SandboxEvolutionIntegration()
        
        print(f"🚀 Sandbox Agent 初始化完成")
        print(f"   工作目录: {self.workspace}")
    
    # ═══════════════════════════════════════════════════════════
    # 1. 实例管理
    # ═══════════════════════════════════════════════════════════
    
    async def create_instance(self, requirement_id, config):
        """
        创建新的沙箱实例
        
        Args:
            requirement_id: 需求ID，如 "REQ-001"
            config: {
                'frontend_code': './frontend/login',
                'backend_code': './backend/login', 
                'requirement_desc': '用户登录功能'
            }
        
        Returns:
            instance_id: 实例ID
        """
        instance_id = f"sandbox-{requirement_id}-{uuid.uuid4().hex[:8]}"
        
        print(f"\n🚀 创建沙箱实例: {instance_id}")
        print(f"   需求: {requirement_id}")
        
        # 创建实例目录
        instance_dir = self.workspace / instance_id
        instance_dir.mkdir(exist_ok=True)
        
        # 保存配置
        config_file = instance_dir / 'config.json'
        with open(config_file, 'w') as f:
            json.dump({
                'instance_id': instance_id,
                'requirement_id': requirement_id,
                'config': config,
                'created_at': datetime.now().isoformat(),
                'status': 'CREATED'
            }, f, indent=2)
        
        # 创建实例对象
        instance = {
            'id': instance_id,
            'requirement_id': requirement_id,
            'config': config,
            'dir': instance_dir,
            'status': 'CREATED',
            'sessions': {},
            'port': self._allocate_port(instance_id),
            'created_at': datetime.now()
        }
        
        self.instances[instance_id] = instance
        
        print(f"✅ 实例创建成功: {instance_id}")
        print(f"   端口: {instance['port']}")
        print(f"   目录: {instance_dir}")
        
        
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
        
        return instance_id
    
    async def start_instance(self, instance_id):
        """启动沙箱实例（创建所有 Session）"""
        instance = self.instances.get(instance_id)
        if not instance:
            raise Exception(f"实例 {instance_id} 不存在")
        
        if instance['status'] == 'RUNNING':
            print(f"⚠️ 实例 {instance_id} 已在运行")
            return instance_id
        
        print(f"\n▶️  启动实例: {instance_id}")
        instance['status'] = 'STARTING'
        
        try:
            # 1. 创建 Frontend Session
            print(f"   启动 Frontend Session...")
            frontend_session = await self._spawn_frontend_session(instance)
            instance['sessions']['frontend'] = frontend_session
            self.active_sessions[f"{instance_id}-frontend"] = frontend_session
            
            # 2. 创建 Backend Session
            print(f"   启动 Backend Session...")
            backend_session = await self._spawn_backend_session(instance)
            instance['sessions']['backend'] = backend_session
            self.active_sessions[f"{instance_id}-backend"] = backend_session
            
            # 3. 创建 Test Session
            print(f"   启动 Test Session...")
            test_session = await self._spawn_test_session(instance)
            instance['sessions']['test'] = test_session
            self.active_sessions[f"{instance_id}-test"] = test_session
            
            instance['status'] = 'RUNNING'
            instance['started_at'] = datetime.now()
            
            print(f"✅ 实例启动成功: {instance_id}")
            
        except Exception as e:
            instance['status'] = 'ERROR'
            instance['error'] = str(e)
            print(f"❌ 实例启动失败: {e}")
            raise
        
        return instance_id
    
    async def stop_instance(self, instance_id):
        """停止沙箱实例"""
        instance = self.instances.get(instance_id)
        if not instance:
            print(f"⚠️ 实例 {instance_id} 不存在")
            return
        
        if instance['status'] != 'RUNNING':
            print(f"⚠️ 实例 {instance_id} 未在运行")
            return
        
        print(f"\n⏹️  停止实例: {instance_id}")
        
        # 停止所有 Session
        for role, session in instance['sessions'].items():
            if session:
                print(f"   停止 {role} Session...")
                try:
                    # 发送停止指令
                    await self._send_to_session(session, {'type': 'STOP'})
                    # 从活跃列表移除
                    session_key = f"{instance_id}-{role}"
                    if session_key in self.active_sessions:
                        del self.active_sessions[session_key]
                except Exception as e:
                    print(f"   警告: 停止 {role} 失败: {e}")
        
        instance['sessions'] = {}
        instance['status'] = 'STOPPED'
        instance['stopped_at'] = datetime.now()
        
        print(f"✅ 实例已停止: {instance_id}")
    
    async def destroy_instance(self, instance_id):
        """销毁实例（停止并删除）"""
        await self.stop_instance(instance_id)
        
        instance = self.instances.get(instance_id)
        if instance:
            # 删除目录
            import shutil
            if instance['dir'].exists():
                shutil.rmtree(instance['dir'])
            
            # 从列表移除
            del self.instances[instance_id]
            
            print(f"🗑️  实例已销毁: {instance_id}")
    
    def list_instances(self, status=None):
        """列出所有实例"""
        instances = list(self.instances.values())
        if status:
            instances = [i for i in instances if i['status'] == status]
        return instances
    
    def get_instance(self, instance_id):
        """获取实例信息"""
        return self.instances.get(instance_id)
    
    # ═══════════════════════════════════════════════════════════
    # 2. Session 管理
    # ═══════════════════════════════════════════════════════════
    
    async def _spawn_frontend_session(self, instance):
        """创建 Frontend Session"""
        # 这里应该调用 OpenClaw 的 sessions_spawn
        # 简化实现：返回模拟的 session 对象
        
        config = instance['config']
        
        session_config = {
            'task': f'''
                你是前端沙箱 Session（实例: {instance['id']}）。
                
                需求ID: {instance['requirement_id']}
                前端代码: {config.get('frontend_code', '未指定')}
                
                职责：
                1. 读取并运行前端代码
                2. 拦截所有 API 调用
                3. 记录 UI 状态变化
                4. 执行测试操作
                
                可用指令：
                - "RUN_TEST": 执行测试用例
                - "GET_APIS": 获取拦截的 API 调用
                - "STOP": 停止运行
                
                回复格式：
                - 执行结果用 JSON 格式
                - 包含 api_calls, ui_states, errors
            ''',
            'mode': 'session',
            'label': f"frontend-{instance['id']}",
            'timeout': 0
        }
        
        # 实际应该调用：
        # return await sessions_spawn(session_config)
        
        # 模拟返回
        return {
            'sessionKey': f"frontend-{instance['id']}",
            'config': session_config
        }
    
    async def _spawn_backend_session(self, instance):
        """创建 Backend Session"""
        config = instance['config']
        port = instance['port']
        
        session_config = {
            'task': f'''
                你是后端沙箱 Session（实例: {instance['id']}）。
                
                需求ID: {instance['requirement_id']}
                后端代码: {config.get('backend_code', '未指定')}
                服务端口: {port}
                
                职责：
                1. 在端口 {port} 启动后端服务
                2. 处理 API 请求
                3. 记录响应数据
                4. 检测异常
                
                可用指令：
                - "START_SERVICE": 启动服务
                - "EXECUTE_API": 执行 API 调用
                - "GET_LOGS": 获取日志
                - "STOP": 停止服务
                
                回复格式：
                - 执行结果用 JSON 格式
                - 包含 responses, errors, logs
            ''',
            'mode': 'session',
            'label': f"backend-{instance['id']}",
            'timeout': 0
        }
        
        return {
            'sessionKey': f"backend-{instance['id']}",
            'config': session_config
        }
    
    async def _spawn_test_session(self, instance):
        """创建 Test Session"""
        config = instance['config']
        
        session_config = {
            'task': f'''
                你是测试沙箱 Session（实例: {instance['id']}）。
                
                需求ID: {instance['requirement_id']}
                需求描述: {config.get('requirement_desc', '未指定')}
                
                职责：
                1. 基于需求生成测试用例
                2. 验证前后端结果一致性
                3. 检测边界情况
                4. 生成测试报告
                
                可用指令：
                - "GENERATE_TESTS": 生成测试用例
                - "VALIDATE": 验证执行结果
                - "GET_REPORT": 获取测试报告
                - "STOP": 停止
                
                回复格式：
                - 测试用例用 JSON 数组
                - 验证结果包含 success, bugs, fixes
            ''',
            'mode': 'session',
            'label': f"test-{instance['id']}",
            'timeout': 0
        }
        
        return {
            'sessionKey': f"test-{instance['id']}",
            'config': session_config
        }
    
    async def _send_to_session(self, session, message):
        """向 Session 发送消息"""
        # 实际应该调用：
        # return await sessions_send({
        #     'sessionKey': session['sessionKey'],
        #     'message': json.dumps(message)
        # })
        
        # 模拟实现
        print(f"   [发送到 {session['sessionKey']}]: {message.get('type', 'UNKNOWN')}")
        return {'status': 'sent'}
    
    # ═══════════════════════════════════════════════════════════
    # 3. 联调执行
    # ═══════════════════════════════════════════════════════════
    
    async def run_integration(self, instance_id):
        """在实例中执行联调"""
        instance = self.instances.get(instance_id)
        if not instance:
            raise Exception(f"实例 {instance_id} 不存在")
        
        if instance['status'] != 'RUNNING':
            raise Exception(f"实例 {instance_id} 未运行，请先调用 start_instance()")
        
        print(f"\n🧪 开始联调: {instance_id}")
        print(f"   需求: {instance['requirement_id']}")
        
        results = []
        
        try:
            # 1. 生成测试用例
            print("\n  [1/3] 生成测试用例...")
            test_cases = await self._generate_test_cases(instance)
            print(f"      ✅ 生成 {len(test_cases)} 个测试用例")
            
            # 2. 执行每个测试用例
            print("\n  [2/3] 执行测试用例...")
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n      用例 {i}/{len(test_cases)}: {test_case.get('name', 'Unknown')}")
                result = await self._run_test_case(instance, test_case)
                results.append(result)
            
            # 3. 生成报告
            print("\n  [3/3] 生成报告...")
            report = self._generate_report(instance, results)
            
            # 保存报告
            report_file = instance['dir'] / 'report.json'
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"      ✅ 报告已保存: {report_file}")
            
            
            # 从联调报告学习
            if hasattr(self, 'evolution'):
                self.evolution.learn_from_integration_report(instance_id, report)
            
            return report
            
        except Exception as e:
            print(f"\n❌ 联调失败: {e}")
            raise
    
    async def _generate_test_cases(self, instance):
        """生成测试用例"""
        test_session = instance['sessions'].get('test')
        if not test_session:
            raise Exception("Test Session 未启动")
        
        # 发送生成指令
        await self._send_to_session(test_session, {
            'type': 'GENERATE_TESTS',
            'requirement': instance['config'].get('requirement_desc', '')
        })
        
        # 等待生成（实际应该轮询或回调）
        await asyncio.sleep(2)
        
        # 模拟返回测试用例
        return [
            {'id': 1, 'name': '正常流程测试', 'priority': 'high'},
            {'id': 2, 'name': '边界值测试', 'priority': 'medium'},
            {'id': 3, 'name': '异常流程测试', 'priority': 'medium'}
        ]
    
    async def _run_test_case(self, instance, test_case):
        """执行单个测试用例"""
        frontend = instance['sessions']['frontend']
        backend = instance['sessions']['backend']
        test = instance['sessions']['test']
        
        # Frontend 执行
        print(f"        Frontend 执行...")
        await self._send_to_session(frontend, {
            'type': 'RUN_TEST',
            'test_case': test_case
        })
        await asyncio.sleep(1)
        frontend_result = {'api_calls': ['/api/login'], 'success': True}
        
        # Backend 执行
        print(f"        Backend 执行...")
        await self._send_to_session(backend, {
            'type': 'EXECUTE_API',
            'api_calls': frontend_result['api_calls']
        })
        await asyncio.sleep(1)
        backend_result = {'responses': [{'status': 200}], 'success': True}
        
        # Test 验证
        print(f"        Test 验证...")
        await self._send_to_session(test, {
            'type': 'VALIDATE',
            'frontend': frontend_result,
            'backend': backend_result
        })
        await asyncio.sleep(1)
        validation = {'success': True, 'bugs': []}
        
        return {
            'test_case': test_case,
            'frontend': frontend_result,
            'backend': backend_result,
            'validation': validation
        }
    
    def _generate_report(self, instance, results):
        """生成报告"""
        passed = sum(1 for r in results if r['validation'].get('success'))
        failed = len(results) - passed
        
        duration = 0
        if instance.get('started_at'):
            duration = (datetime.now() - instance['started_at']).total_seconds()
        
        return {
            'instance_id': instance['id'],
            'requirement_id': instance['requirement_id'],
            'status': 'COMPLETED',
            'summary': {
                'total': len(results),
                'passed': passed,
                'failed': failed,
                'duration': round(duration, 2)
            },
            'results': results,
            'created_at': instance['created_at'].isoformat(),
            'completed_at': datetime.now().isoformat()
        }
    
    # ═══════════════════════════════════════════════════════════
    # 4. 工具方法
    # ═══════════════════════════════════════════════════════════
    
    def _allocate_port(self, instance_id):
        """为实例分配端口"""
        import hashlib
        hash_val = int(hashlib.md5(instance_id.encode()).hexdigest(), 16)
        return 8000 + (hash_val % 1000)
    
    def get_status(self):
        """获取Agent 状态"""
        return {
            'workspace': str(self.workspace),
            'total_instances': len(self.instances),
            'active_instances': len([i for i in self.instances.values() if i['status'] == 'RUNNING']),
            'instances': [
                {
                    'id': i['id'],
                    'requirement_id': i['requirement_id'],
                    'status': i['status'],
                    'port': i.get('port'),
                    'created_at': i['created_at'].isoformat()
                }
                for i in self.instances.values()
            ]
        }


# ═══════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════

async def main():
    """使用示例"""
    
    # 创建沙箱 Agent
    agent = SandboxAgent()
    
    print("\n" + "=" * 60)
    print("Sandbox Agent 演示")
    print("=" * 60)
    
    # 1. 创建实例
    print("\n1. 创建沙箱实例")
    instance_id = await agent.create_instance(
        requirement_id='REQ-001',
        config={
            'frontend_code': './frontend/login',
            'backend_code': './backend/login',
            'requirement_desc': '用户登录功能，支持手机号/密码登录'
        }
    )
    
    # 2. 启动实例
    print("\n2. 启动实例")
    await agent.start_instance(instance_id)
    
    # 3. 执行联调
    print("\n3. 执行联调")
    report = await agent.run_integration(instance_id)
    
    # 4. 打印报告
    print("\n4. 联调报告")
    print(f"   实例ID: {report['instance_id']}")
    print(f"   需求: {report['requirement_id']}")
    print(f"   状态: {report['status']}")
    print(f"   通过: {report['summary']['passed']}/{report['summary']['total']}")
    print(f"   耗时: {report['summary']['duration']}s")
    
    # 5. 查看状态
    print("\n5. Agent 状态")
    status = agent.get_status()
    print(f"   工作目录: {status['workspace']}")
    print(f"   实例总数: {status['total_instances']}")
    print(f"   运行中: {status['active_instances']}")
    
    # 6. 停止实例
    print("\n6. 停止实例")
    await agent.stop_instance(instance_id)
    
    # 7. 销毁实例
    print("\n7. 销毁实例")
    await agent.destroy_instance(instance_id)
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
