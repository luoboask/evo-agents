# Sandbox Manager Agent 设计

_统一管理 Frontend/Backend/Test 三个子 Agent 的沙箱管理器_

---

## 🎯 核心概念

**沙箱管理 Agent（Sandbox Manager）** = 一个特殊的 Agent，专门负责：
- 管理多个子 Agent（Frontend/Backend/Test）
- 协调子 Agent 之间的通信
- 监控子 Agent 健康状态
- 汇总执行结果
- 与用户（Main Agent）交互

```
┌─────────────────────────────────────────────────────────────┐
│                     OpenClaw Gateway                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Sandbox Manager Agent（沙箱管理器）          │   │
│  │                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │ Frontend    │  │   Backend   │  │    Test     │ │   │
│  │  │ Sub-Agent   │  │   Sub-Agent │  │   Sub-Agent │ │   │
│  │  │             │  │             │  │             │ │   │
│  │  │ • 独立进程   │  │ • 独立进程   │  │ • 独立进程   │ │   │
│  │  │ • 专属技能   │  │ • 专属技能   │  │ • 专属技能   │ │   │
│  │  │ • 向 Manager │  │ • 向 Manager │  │ • 向 Manager │ │   │
│  │  │   汇报      │  │   汇报      │  │   汇报      │ │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │   │
│  │         │                │                │        │   │
│  │         └────────────────┼────────────────┘        │   │
│  │                          │                         │   │
│  │                    ┌─────┴─────┐                   │   │
│  │                    │  内部协调  │                   │   │
│  │                    │  • 任务分配 │                   │   │
│  │                    │  • 结果汇总 │                   │   │
│  │                    │  • 状态监控 │                   │   │
│  │                    └─────┬─────┘                   │   │
│  │                          │                         │   │
│  └──────────────────────────┼─────────────────────────┘   │
│                             │                             │
│  ┌──────────────────────────┼─────────────────────────┐   │
│  │                     Main Agent（你）                │   │
│  │                                                     │   │
│  │  • 全局决策                                          │   │
│  │  • 用户交互                                          │   │
│  │  • 向 Sandbox Manager 发送指令                        │   │
│  └──────────────────────────┴─────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ 架构设计

### Sandbox Manager 职责

```python
class SandboxManagerAgent:
    """
    沙箱管理 Agent
    - 管理多个子 Agent
    - 协调子 Agent 执行
    - 监控子 Agent 健康
    - 汇总执行结果
    """
    
    def __init__(self):
        self.sub_agents = {
            'frontend': None,  # Frontend Sub-Agent
            'backend': None,   # Backend Sub-Agent
            'test': None,      # Test Sub-Agent
        }
        self.status = {}     # 子 Agent 状态
        self.results = []    # 执行结果
    
    # ═══════════════════════════════════════════════════════════
    # 1. 子 Agent 生命周期管理
    # ═══════════════════════════════════════════════════════════
    
    async def start_sub_agents(self, config):
        """启动所有子 Agent"""
        tasks = []
        
        # 启动 Frontend Sub-Agent
        tasks.append(self._start_frontend_agent(config.get('frontend')))
        
        # 启动 Backend Sub-Agent
        tasks.append(self._start_backend_agent(config.get('backend')))
        
        # 启动 Test Sub-Agent
        tasks.append(self._start_test_agent(config.get('test')))
        
        # 并行启动
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 检查启动结果
        for role, result in zip(['frontend', 'backend', 'test'], results):
            if isinstance(result, Exception):
                self.status[role] = {'state': 'ERROR', 'error': str(result)}
            else:
                self.sub_agents[role] = result
                self.status[role] = {'state': 'RUNNING', 'pid': result.pid}
        
        return self.status
    
    async def stop_sub_agents(self):
        """停止所有子 Agent"""
        for role, agent in self.sub_agents.items():
            if agent:
                await agent.stop()
                self.status[role] = {'state': 'STOPPED'}
    
    async def restart_sub_agent(self, role):
        """重启指定子 Agent"""
        if role in self.sub_agents:
            await self.sub_agents[role].stop()
            await asyncio.sleep(2)
            
            if role == 'frontend':
                self.sub_agents[role] = await self._start_frontend_agent()
            elif role == 'backend':
                self.sub_agents[role] = await self._start_backend_agent()
            elif role == 'test':
                self.sub_agents[role] = await self._start_test_agent()
    
    # ═══════════════════════════════════════════════════════════
    # 2. 任务协调与分配
    # ═══════════════════════════════════════════════════════════
    
    async def run_integration(self, requirement):
        """
        执行联调任务
        
        流程：
        1. 向 Test Sub-Agent 请求生成测试用例
        2. 并行分发测试用例给 Frontend/Backend
        3. 收集执行结果
        4. 验证结果一致性
        5. 返回汇总结果
        """
        self.results = []
        
        # Phase 1: 生成测试用例
        test_cases = await self._dispatch_to_test_agent({
            'type': 'GENERATE_TESTS',
            'requirement': requirement
        })
        
        # Phase 2: 并行执行测试
        for test_case in test_cases:
            result = await self._run_test_case(test_case)
            self.results.append(result)
        
        # Phase 3: 汇总结果
        return self._aggregate_results()
    
    async def _run_test_case(self, test_case):
        """执行单个测试用例"""
        # 1. Frontend Sub-Agent 执行
        frontend_result = await self._dispatch_to_frontend_agent({
            'type': 'RUN_TEST',
            'test_case': test_case
        })
        
        # 2. 提取 API 调用
        api_calls = frontend_result.get('api_calls', [])
        
        # 3. Backend Sub-Agent 执行
        backend_result = await self._dispatch_to_backend_agent({
            'type': 'EXECUTE_APIS',
            'api_calls': api_calls
        })
        
        # 4. Test Sub-Agent 验证
        validation = await self._dispatch_to_test_agent({
            'type': 'VALIDATE',
            'frontend_result': frontend_result,
            'backend_result': backend_result
        })
        
        return {
            'test_case': test_case,
            'frontend': frontend_result,
            'backend': backend_result,
            'validation': validation
        }
    
    # ═══════════════════════════════════════════════════════════
    # 3. 子 Agent 通信封装
    # ═══════════════════════════════════════════════════════════
    
    async def _dispatch_to_frontend_agent(self, message):
        """分发任务给 Frontend Sub-Agent"""
        agent = self.sub_agents.get('frontend')
        if not agent:
            raise Exception('Frontend Sub-Agent not running')
        
        return await agent.send_message(message)
    
    async def _dispatch_to_backend_agent(self, message):
        """分发任务给 Backend Sub-Agent"""
        agent = self.sub_agents.get('backend')
        if not agent:
            raise Exception('Backend Sub-Agent not running')
        
        return await agent.send_message(message)
    
    async def _dispatch_to_test_agent(self, message):
        """分发任务给 Test Sub-Agent"""
        agent = self.sub_agents.get('test')
        if not agent:
            raise Exception('Test Sub-Agent not running')
        
        return await agent.send_message(message)
    
    # ═══════════════════════════════════════════════════════════
    # 4. 健康监控
    # ═══════════════════════════════════════════════════════════
    
    async def health_check(self):
        """检查所有子 Agent 健康状态"""
        health = {}
        
        for role, agent in self.sub_agents.items():
            if agent:
                try:
                    # 发送心跳检测
                    response = await agent.send_message({'type': 'HEALTH_CHECK'})
                    health[role] = {
                        'status': 'HEALTHY',
                        'response_time': response.get('time', 0)
                    }
                except Exception as e:
                    health[role] = {
                        'status': 'UNHEALTHY',
                        'error': str(e)
                    }
            else:
                health[role] = {
                    'status': 'NOT_RUNNING'
                }
        
        return health
    
    async def monitor_loop(self):
        """持续监控循环"""
        while True:
            health = await self.health_check()
            
            # 检查是否有不健康 Agent
            for role, status in health.items():
                if status['status'] != 'HEALTHY':
                    # 自动重启
                    await self.restart_sub_agent(role)
            
            await asyncio.sleep(30)  # 每30秒检查一次
    
    # ═══════════════════════════════════════════════════════════
    # 5. 结果汇总与报告
    # ═══════════════════════════════════════════════════════════
    
    def _aggregate_results(self):
        """汇总所有测试结果"""
        summary = {
            'total': len(self.results),
            'passed': 0,
            'failed': 0,
            'bugs': [],
            'fixes': []
        }
        
        for result in self.results:
            validation = result.get('validation', {})
            
            if validation.get('success'):
                summary['passed'] += 1
            else:
                summary['failed'] += 1
                
            # 收集 Bug
            bugs = validation.get('bugs', [])
            summary['bugs'].extend(bugs)
            
            # 收集修复
            fixes = validation.get('fixes', [])
            summary['fixes'].extend(fixes)
        
        return summary
    
    def generate_report(self):
        """生成联调报告"""
        summary = self._aggregate_results()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': summary,
            'details': self.results,
            'health': self.status
        }
        
        return report
```

---

## 📋 OpenClaw 配置

### Sandbox Manager Agent 配置

```yaml
# agents/sandbox-manager/config.yaml
name: sandbox-manager
description: "沙箱管理 Agent，统一管理 Frontend/Backend/Test 三个子 Agent"
type: manager  # 特殊类型：管理器

# 管理的子 Agent
sub_agents:
  frontend:
    agent: frontend-sub-agent
    required: true
    auto_start: true
    
  backend:
    agent: backend-sub-agent
    required: true
    auto_start: true
    
  test:
    agent: test-sub-agent
    required: false
    auto_start: true

# 协调配置
coordinator:
  # 任务分配策略
  strategy: parallel  # parallel/sequential/priority
  
  # 超时配置
  timeout:
    frontend: 60s
    backend: 30s
    test: 120s
  
  # 重试配置
  retry:
    max_attempts: 3
    backoff: exponential

# 健康监控
health_check:
  enabled: true
  interval: 30s
  auto_restart: true

# 权限
permissions:
  - agent:manage  # 管理其他 Agent
  - agent:spawn   # 启动子 Agent
  - agent:stop    # 停止子 Agent
  - agent:message # 向子 Agent 发送消息

# 心跳
heartbeat:
  enabled: true
  interval: 30s
```

### Frontend Sub-Agent 配置

```yaml
# agents/frontend-sub-agent/config.yaml
name: frontend-sub-agent
description: "前端子 Agent，受 Sandbox Manager 管理"
type: subordinate  # 从属类型

# 上级 Agent
parent: sandbox-manager

skills:
  - puppeteer-test
  - react-dev
  - api-interceptor
  - screenshot

permissions:
  - read: ./frontend-code
  - exec: npm, node
  - network: localhost:3000-3999

heartbeat:
  enabled: true
  interval: 30s
  report_to: sandbox-manager
```

### Backend Sub-Agent 配置

```yaml
# agents/backend-sub-agent/config.yaml
name: backend-sub-agent
description: "后端子 Agent，受 Sandbox Manager 管理"
type: subordinate

parent: sandbox-manager

skills:
  - docker-runner
  - api-server
  - mock-database
  - request-logger

permissions:
  - read: ./backend-code
  - exec: docker, python, node
  - network: localhost:8000-8999
  - docker: true

heartbeat:
  enabled: true
  interval: 30s
  report_to: sandbox-manager
```

### Test Sub-Agent 配置

```yaml
# agents/test-sub-agent/config.yaml
name: test-sub-agent
description: "测试子 Agent，受 Sandbox Manager 管理"
type: subordinate

parent: sandbox-manager

skills:
  - test-generator
  - property-testing
  - coverage-analyzer
  - bug-detector

permissions:
  - read: ./requirements
  - exec: python
  - network: all

heartbeat:
  enabled: true
  interval: 30s
  report_to: sandbox-manager
```

---

## 🔄 工作流程

### 1. 启动流程

```
Main Agent
    │
    ▼ 发送指令
Sandbox Manager Agent
    │
    ├─► 启动 Frontend Sub-Agent
    ├─► 启动 Backend Sub-Agent
    └─► 启动 Test Sub-Agent
    │
    ▼ 汇报状态
Main Agent ◄── 所有 Sub-Agent 就绪
```

### 2. 执行流程

```
Main Agent
    │
    ▼ 发送 "执行联调 REQ-001"
Sandbox Manager Agent
    │
    ├─► 向 Test Sub-Agent 请求生成用例
    │   └─► 返回 15 个测试用例
    │
    ├─► 循环执行每个用例
    │   ├─► 向 Frontend Sub-Agent 发送 "执行用例"
    │   │   └─► 返回 API 调用列表
    │   │
    │   ├─► 向 Backend Sub-Agent 发送 "执行 API"
    │   │   └─► 返回响应结果
    │   │
    │   └─► 向 Test Sub-Agent 发送 "验证结果"
    │       └─► 返回验证结果
    │
    ├─► 汇总所有结果
    │
    ▼ 返回完整报告
Main Agent
```

### 3. 监控流程

```
Sandbox Manager Agent (后台线程)
    │
    ├─► 每 30 秒检查 Sub-Agent 健康
    │   ├─► Frontend Sub-Agent: HEALTHY
    │   ├─► Backend Sub-Agent: UNHEALTHY
    │   │   └─► 自动重启 Backend Sub-Agent
    │   └─► Test Sub-Agent: HEALTHY
    │
    ▼ 继续监控
```

---

## 💡 关键优势

### 1. 层级管理

```
Main Agent (全局决策)
    └── Sandbox Manager (协调管理)
            ├── Frontend Sub-Agent (执行)
            ├── Backend Sub-Agent (执行)
            └── Test Sub-Agent (执行)

优势：
- 职责清晰
- 易于扩展（新增 Sub-Agent 容易）
- 故障隔离（单个 Sub-Agent 失败不影响其他）
```

### 2. 统一入口

```
Main Agent 只需与 Sandbox Manager 通信
- 无需直接管理多个 Sub-Agent
- 简化通信逻辑
- 统一接口
```

### 3. 自动恢复

```
Sandbox Manager 自动监控
- 检测 Sub-Agent 健康
- 自动重启失败 Agent
- 保证高可用
```

### 4. 灵活配置

```
通过 YAML 配置即可调整
- Sub-Agent 数量
- 启动顺序
- 超时时间
- 重试策略
```

---

## 🚀 使用方式

### 启动沙箱

```bash
# 1. 启动 Sandbox Manager（自动启动所有 Sub-Agent）
openclaw agent start sandbox-manager

# 2. 检查状态
openclaw agent status sandbox-manager
# Output:
# sandbox-manager: RUNNING
#   ├─ frontend-sub-agent: RUNNING
#   ├─ backend-sub-agent: RUNNING
#   └─ test-sub-agent: RUNNING
```

### 执行联调

```bash
# Main Agent 向 Sandbox Manager 发送指令
openclaw agent send sandbox-manager --message "{
  type: 'RUN_INTEGRATION',
  requirement: 'REQ-001',
  frontend_code: './frontend',
  backend_code: './backend'
}"

# Sandbox Manager 自动协调 Sub-Agent 执行
# 返回结果
```

### 查看报告

```bash
# 获取报告
openclaw agent send sandbox-manager --message "{
  type: 'GET_REPORT'
}"

# 或通过 Web 界面
open http://localhost:8080/sandbox-manager/report
```

---

## 📊 对比：直接管理 vs Sandbox Manager

| 维度 | 直接管理 | Sandbox Manager | 优势 |
|------|---------|----------------|------|
| 复杂度 | 高（管理多个） | 低（管理一个） | Manager |
| 扩展性 | 差（新增需改代码） | 好（配置即可） | Manager |
| 故障隔离 | 差（一个失败全失败） | 好（自动重启） | Manager |
| 代码复用 | 低 | 高（通用管理逻辑） | Manager |
| 监控难度 | 高 | 低（统一监控） | Manager |
| 配置灵活性 | 低 | 高（YAML配置） | Manager |

---

## 🎯 下一步实现

1. **创建 Sandbox Manager Agent 代码**
2. **实现 Sub-Agent 注册机制**
3. **开发任务分发逻辑**
4. **实现健康监控循环**
5. **创建 Web 管理界面**

---

**这就是 Sandbox Manager Agent 设计——一个专门管理其他 Agent 的"超级 Agent"！** 🤖✨
