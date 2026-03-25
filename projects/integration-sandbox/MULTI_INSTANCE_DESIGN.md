# 多实例并行联调沙箱设计

_支持多个需求并行联调的实例化沙箱_

---

## 🎯 核心概念

### 沙箱实例（Sandbox Instance）

每个需求联调 = 一个独立的沙箱实例

```
需求 REQ-001 ──► 沙箱实例 Instance-001
    ├── Frontend Session（独立）
    ├── Backend Session（独立）
    └── Test Session（独立）

需求 REQ-002 ──► 沙箱实例 Instance-002（并行）
    ├── Frontend Session（独立）
    ├── Backend Session（独立）
    └── Test Session（独立）

需求 REQ-003 ──► 沙箱实例 Instance-003（并行）
    └── ...
```

**关键特性：**
- 每个实例完全隔离
- 实例之间互不干扰
- 可并行执行多个需求
- 独立的生命周期管理

---

## 🏗️ 实例化架构

### 实例管理器（Instance Manager）

```python
class SandboxInstanceManager:
    """
    沙箱实例管理器
    - 管理多个沙箱实例
    - 每个需求对应一个实例
    - 实例之间完全隔离
    """
    
    def __init__(self):
        self.instances = {}  # instance_id -> SandboxInstance
        self.requirement_map = {}  # requirement_id -> instance_id
    
    async def create_instance(self, requirement_id, config):
        """
        创建新的沙箱实例
        
        Args:
            requirement_id: 需求ID（如 REQ-001）
            config: 配置（前端代码、后端代码、需求描述）
        
        Returns:
            instance_id: 实例ID
        """
        instance_id = f"instance-{requirement_id}-{uuid.uuid4().hex[:8]}"
        
        # 创建实例
        instance = SandboxInstance(
            id=instance_id,
            requirement_id=requirement_id,
            config=config
        )
        
        # 启动实例
        await instance.start()
        
        # 记录映射
        self.instances[instance_id] = instance
        self.requirement_map[requirement_id] = instance_id
        
        return instance_id
    
    async def get_instance(self, instance_id):
        """获取实例"""
        return self.instances.get(instance_id)
    
    async def get_instance_by_requirement(self, requirement_id):
        """通过需求ID获取实例"""
        instance_id = self.requirement_map.get(requirement_id)
        if instance_id:
            return await self.get_instance(instance_id)
        return None
    
    async def list_instances(self, status=None):
        """
        列出所有实例
        
        Args:
            status: 过滤状态（running/stopped/error）
        """
        instances = list(self.instances.values())
        if status:
            instances = [i for i in instances if i.status == status]
        return instances
    
    async def destroy_instance(self, instance_id):
        """销毁实例"""
        instance = self.instances.get(instance_id)
        if instance:
            await instance.stop()
            del self.instances[instance_id]
            
            # 清理映射
            for req_id, inst_id in self.requirement_map.items():
                if inst_id == instance_id:
                    del self.requirement_map[req_id]
                    break
    
    async def run_integration(self, instance_id):
        """在指定实例中执行联调"""
        instance = await self.get_instance(instance_id)
        if not instance:
            raise Exception(f"Instance {instance_id} not found")
        
        return await instance.run_integration()
```

---

## 📦 沙箱实例（Sandbox Instance）

### 实例结构

```python
class SandboxInstance:
    """
    单个沙箱实例
    - 对应一个需求联调
    - 包含 Frontend/Backend/Test 三个 Session
    - 完全隔离，独立运行
    """
    
    def __init__(self, id, requirement_id, config):
        self.id = id
        self.requirement_id = requirement_id
        self.config = config
        
        self.status = 'CREATED'  # CREATED/RUNNING/STOPPED/ERROR
        self.sessions = {
            'frontend': None,
            'backend': None,
            'test': None
        }
        self.results = []
        self.created_at = datetime.now()
        self.started_at = None
        self.stopped_at = None
    
    async def start(self):
        """启动实例（创建所有 Session）"""
        print(f"🚀 启动沙箱实例: {self.id}")
        self.status = 'STARTING'
        
        try:
            # 1. 创建 Frontend Session
            print(f"  [{self.id}] 创建 Frontend Session...")
            self.sessions['frontend'] = await self._create_frontend_session()
            
            # 2. 创建 Backend Session
            print(f"  [{self.id}] 创建 Backend Session...")
            self.sessions['backend'] = await self._create_backend_session()
            
            # 3. 创建 Test Session
            print(f"  [{self.id}] 创建 Test Session...")
            self.sessions['test'] = await self._create_test_session()
            
            self.status = 'RUNNING'
            self.started_at = datetime.now()
            print(f"✅ 实例 {self.id} 启动完成")
            
        except Exception as e:
            self.status = 'ERROR'
            print(f"❌ 实例 {self.id} 启动失败: {e}")
            raise
    
    async def _create_frontend_session(self):
        """创建 Frontend Session"""
        return await sessions_spawn({
            'task': f'''
                你是前端沙箱 Agent（实例: {self.id}）。
                
                需求ID: {self.requirement_id}
                前端代码: {self.config.get('frontend_code')}
                
                你的职责：
                1. 运行前端代码
                2. 执行测试操作
                3. 拦截 API 调用
                4. 返回结果
                
                注意：你只属于实例 {self.id}，不要与其他实例混淆。
            ''',
            'mode': 'session',
            'label': f'frontend-{self.id}',
            'timeout': 0
        })
    
    async def _create_backend_session(self):
        """创建 Backend Session"""
        # 为每个实例分配独立端口
        port = self._allocate_port()
        
        return await sessions_spawn({
            'task': f'''
                你是后端沙箱 Agent（实例: {self.id}）。
                
                需求ID: {self.requirement_id}
                后端代码: {self.config.get('backend_code')}
                服务端口: {port}
                
                你的职责：
                1. 在端口 {port} 启动服务
                2. 处理 API 请求
                3. 记录响应
                4. 返回结果
                
                注意：你只属于实例 {self.id}，使用独立端口 {port}。
            ''',
            'mode': 'session',
            'label': f'backend-{self.id}',
            'timeout': 0
        })
    
    async def _create_test_session(self):
        """创建 Test Session"""
        return await sessions_spawn({
            'task': f'''
                你是测试沙箱 Agent（实例: {self.id}）。
                
                需求ID: {self.requirement_id}
                需求描述: {self.config.get('requirement_desc')}
                
                你的职责：
                1. 生成测试用例
                2. 验证结果
                3. 检测 Bug
                4. 返回报告
                
                注意：你只属于实例 {self.id}。
            ''',
            'mode': 'session',
            'label': f'test-{self.id}',
            'timeout': 0
        })
    
    async def run_integration(self):
        """在实例中执行联调"""
        print(f"\n🧪 实例 {self.id} 开始联调")
        
        # 1. 生成测试用例
        test_cases = await self._generate_test_cases()
        
        # 2. 执行每个用例
        results = []
        for tc in test_cases:
            result = await self._run_test_case(tc)
            results.append(result)
        
        # 3. 汇总
        self.results = results
        return self._generate_report()
    
    async def _generate_test_cases(self):
        """生成测试用例"""
        await sessions_send({
            'sessionKey': self.sessions['test'].sessionKey,
            'message': json.dumps({
                'type': 'GENERATE_TESTS',
                'requirement': self.config.get('requirement_desc')
            })
        })
        
        await asyncio.sleep(5)
        
        # 获取结果
        history = await sessions_history({
            'sessionKey': self.sessions['test'].sessionKey,
            'limit': 10
        })
        
        return self._extract_test_cases(history)
    
    async def _run_test_case(self, test_case):
        """执行单个测试用例"""
        # Frontend 执行
        await sessions_send({
            'sessionKey': self.sessions['frontend'].sessionKey,
            'message': json.dumps({
                'type': 'RUN_TEST',
                'test_case': test_case
            })
        })
        await asyncio.sleep(3)
        frontend_result = await self._get_result('frontend')
        
        # Backend 执行
        await sessions_send({
            'sessionKey': self.sessions['backend'].sessionKey,
            'message': json.dumps({
                'type': 'EXECUTE_API',
                'api_calls': frontend_result.get('api_calls', [])
            })
        })
        await asyncio.sleep(3)
        backend_result = await self._get_result('backend')
        
        # Test 验证
        await sessions_send({
            'sessionKey': self.sessions['test'].sessionKey,
            'message': json.dumps({
                'type': 'VALIDATE',
                'frontend': frontend_result,
                'backend': backend_result
            })
        })
        await asyncio.sleep(2)
        validation = await self._get_result('test')
        
        return {
            'test_case': test_case,
            'frontend': frontend_result,
            'backend': backend_result,
            'validation': validation
        }
    
    async def stop(self):
        """停止实例"""
        print(f"🛑 停止实例: {self.id}")
        
        for role, session in self.sessions.items():
            if session:
                print(f"  停止 {role} Session...")
                await sessions_send({
                    'sessionKey': session.sessionKey,
                    'message': 'STOP'
                })
        
        self.status = 'STOPPED'
        self.stopped_at = datetime.now()
        print(f"✅ 实例 {self.id} 已停止")
    
    def _allocate_port(self):
        """为实例分配独立端口"""
        # 基于实例ID生成唯一端口
        # 例如：instance-001 -> 8001, instance-002 -> 8002
        import hashlib
        hash_val = int(hashlib.md5(self.id.encode()).hexdigest(), 16)
        return 8000 + (hash_val % 1000)
    
    def _generate_report(self):
        """生成报告"""
        passed = sum(1 for r in self.results if r.get('validation', {}).get('success'))
        failed = len(self.results) - passed
        
        return {
            'instance_id': self.id,
            'requirement_id': self.requirement_id,
            'status': self.status,
            'summary': {
                'total': len(self.results),
                'passed': passed,
                'failed': failed
            },
            'results': self.results,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'duration': (datetime.now() - self.started_at).total_seconds() if self.started_at else 0
        }
```

---

## 🚀 使用示例

### 场景：并行联调多个需求

```python
async def main():
    # 创建实例管理器
    manager = SandboxInstanceManager()
    
    # 需求1: 用户登录
    print("=" * 60)
    print("创建实例: 用户登录功能")
    instance1 = await manager.create_instance(
        requirement_id='REQ-001',
        config={
            'frontend_code': './frontend/login',
            'backend_code': './backend/login',
            'requirement_desc': '用户登录功能，支持手机号/密码登录'
        }
    )
    print(f"实例ID: {instance1}")
    
    # 需求2: 商品列表（并行）
    print("=" * 60)
    print("创建实例: 商品列表功能（并行）")
    instance2 = await manager.create_instance(
        requirement_id='REQ-002',
        config={
            'frontend_code': './frontend/products',
            'backend_code': './backend/products',
            'requirement_desc': '商品列表展示，支持分页和筛选'
        }
    )
    print(f"实例ID: {instance2}")
    
    # 需求3: 购物车（并行）
    print("=" * 60)
    print("创建实例: 购物车功能（并行）")
    instance3 = await manager.create_instance(
        requirement_id='REQ-003',
        config={
            'frontend_code': './frontend/cart',
            'backend_code': './backend/cart',
            'requirement_desc': '购物车功能，支持增删改查'
        }
    )
    print(f"实例ID: {instance3}")
    
    # 并行执行所有实例的联调
    print("\n" + "=" * 60)
    print("并行执行所有联调...")
    
    tasks = [
        manager.run_integration(instance1),
        manager.run_integration(instance2),
        manager.run_integration(instance3)
    ]
    
    results = await asyncio.gather(*tasks)
    
    # 打印所有报告
    for i, result in enumerate(results, 1):
        print(f"\n📊 实例 {i} 报告:")
        print(f"  需求: {result['requirement_id']}")
        print(f"  状态: {result['status']}")
        print(f"  通过: {result['summary']['passed']}/{result['summary']['total']}")
        print(f"  耗时: {result['duration']:.1f}s")
    
    # 列出所有运行中的实例
    print("\n" + "=" * 60)
    print("运行中的实例:")
    running = await manager.list_instances(status='RUNNING')
    for inst in running:
        print(f"  - {inst.id}: {inst.requirement_id}")
    
    # 清理：销毁所有实例
    print("\n" + "=" * 60)
    print("清理：销毁所有实例")
    await manager.destroy_instance(instance1)
    await manager.destroy_instance(instance2)
    await manager.destroy_instance(instance3)
    print("✅ 清理完成")

# 运行
asyncio.run(main())
```

---

## 📊 输出示例

```
============================================================
创建实例: 用户登录功能
  启动沙箱实例: instance-REQ-001-a1b2c3d4
    [instance-REQ-001-a1b2c3d4] 创建 Frontend Session...
    [instance-REQ-001-a1b2c3d4] 创建 Backend Session...
    [instance-REQ-001-a1b2c3d4] 创建 Test Session...
  ✅ 实例 instance-REQ-001-a1b2c3d4 启动完成
实例ID: instance-REQ-001-a1b2c3d4

============================================================
创建实例: 商品列表功能（并行）
  启动沙箱实例: instance-REQ-002-e5f6g7h8
    [instance-REQ-002-e5f6g7h8] 创建 Frontend Session...
    [instance-REQ-002-e5f6g7h8] 创建 Backend Session...
    [instance-REQ-002-e5f6g7h8] 创建 Test Session...
  ✅ 实例 instance-REQ-002-e5f6g7h8 启动完成
实例ID: instance-REQ-002-e5f6g7h8

============================================================
创建实例: 购物车功能（并行）
  ...

============================================================
并行执行所有联调...

🧪 实例 instance-REQ-001-a1b2c3d4 开始联调
  生成测试用例...
  ✅ 生成 5 个测试用例
  执行测试用例 1/5: 正常登录
    Frontend 执行...
    Backend 执行...
    Test 验证...
  执行测试用例 2/5: 错误密码...
  ...

🧪 实例 instance-REQ-002-e5f6g7h8 开始联调
  ...

🧪 实例 instance-REQ-003-i9j0k1l2 开始联调
  ...

📊 实例 1 报告:
  需求: REQ-001
  状态: RUNNING
  通过: 5/5
  耗时: 45.2s

📊 实例 2 报告:
  需求: REQ-002
  状态: RUNNING
  通过: 8/8
  耗时: 38.7s

📊 实例 3 报告:
  需求: REQ-003
  状态: RUNNING
  通过: 6/7
  耗时: 52.1s

============================================================
运行中的实例:
  - instance-REQ-001-a1b2c3d4: REQ-001
  - instance-REQ-002-e5f6g7h8: REQ-002
  - instance-REQ-003-i9j0k1l2: REQ-003

============================================================
清理：销毁所有实例
  停止实例: instance-REQ-001-a1b2c3d4
  ...
✅ 清理完成
```

---

## 🎯 关键特性

### 1. 完全隔离

```
Instance-001              Instance-002
├─ Frontend (port 8001)   ├─ Frontend (port 8002)
├─ Backend (port 8001)    ├─ Backend (port 8002)
└─ Test                   └─ Test

✅ 独立端口
✅ 独立 Session
✅ 独立资源
✅ 互不干扰
```

### 2. 并行执行

```python
# 三个实例同时执行
tasks = [
    instance1.run_integration(),  # 在后台运行
    instance2.run_integration(),  # 在后台运行
    instance3.run_integration()   # 在后台运行
]

results = await asyncio.gather(*tasks)  # 等待全部完成
```

### 3. 独立生命周期

```python
# 实例1 正在运行
instance1 = await manager.create_instance('REQ-001', config1)

# 实例2 稍后创建（实例1 仍在运行）
instance2 = await manager.create_instance('REQ-002', config2)

# 可以单独停止某个实例
await manager.destroy_instance(instance1)  # 实例2 继续运行
```

### 4. 资源管理

```python
# 自动分配资源
- 独立端口（8001, 8002, 8003...）
- 独立进程（Session）
- 独立内存空间
- 自动回收（销毁时）
```

---

## 💡 对比：单实例 vs 多实例

| 特性 | 单实例 | 多实例（本方案） |
|------|--------|----------------|
| 并行需求 | ❌ 串行 | ✅ 并行 |
| 资源隔离 | ❌ 共享 | ✅ 独立 |
| 故障隔离 | ❌ 影响全部 | ✅ 只影响单个 |
| 扩展性 | ❌ 有限 | ✅ 无限（理论上） |
| 管理复杂度 | 低 | 中（有管理器） |
| 适用场景 | 简单项目 | 复杂/多需求项目 |

---

## 🚀 下一步实现

1. **实现 SandboxInstanceManager**
2. **实现 SandboxInstance 类**
3. **添加端口分配器**
4. **实现实例监控**
5. **开发 Web 管理界面**

---

**这就是支持多实例并行的联调沙箱设计——每个需求一个独立沙箱，完全隔离，互不干扰！** 🤖✨
