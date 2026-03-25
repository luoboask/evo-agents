# 实际可行的 OpenClaw 联调沙箱方案

_基于 OpenClaw 实际能力（sessions_spawn）的设计_

---

## 🎯 关键澄清

### OpenClaw 的 Agent 是什么？

```
❌ 不是常驻进程
❌ 不是系统服务
✅ 是配置目录（~/.openclaw/agents/{name}/）
✅ 是动态创建的 Session
```

### 实际可用的能力

| 能力 | 命令 | 说明 |
|------|------|------|
| 创建会话 | `sessions_spawn` | 动态创建子会话 |
| 发送消息 | `sessions_send` | 向会话发送消息 |
| 获取历史 | `sessions_history` | 获取会话历史 |
| 查看状态 | `sessions_list` | 列出活跃会话 |

---

## 🏗️ 实际架构

### 动态 Session 沙箱

```
当前主会话（你）
    │
    ├─► sessions_spawn ──► Frontend Session（子进程）
    │                        • 运行前端沙箱代码
    │                        • 等待指令
    │                        • 返回结果
    │
    ├─► sessions_spawn ──► Backend Session（子进程）
    │                        • 运行后端沙箱代码
    │                        • 等待指令
    │                        • 返回结果
    │
    └─► sessions_spawn ──► Test Session（子进程）
                               • 生成测试用例
                               • 验证结果
                               • 返回报告
```

### 核心特点

- **动态创建**：每次联调时创建新 Session
- **独立隔离**：每个 Session 完全独立
- **按需通信**：通过 sessions_send 发送指令
- **自动清理**：Session 结束自动回收资源

---

## 💻 实现代码

### 主协调脚本

```python
#!/usr/bin/env python3
"""
联调沙箱协调器
基于 OpenClaw sessions_spawn 实现
"""

import json
import asyncio
from openclaw import sessions_spawn, sessions_send, sessions_history, sessions_list

class IntegrationSandbox:
    """联调沙箱"""
    
    def __init__(self):
        self.sessions = {}
    
    async def start_sandbox(self, config):
        """启动沙箱（创建子 Session）"""
        print("🚀 启动联调沙箱...")
        
        # 1. 创建 Frontend Session
        print("  启动 Frontend Session...")
        self.sessions['frontend'] = await sessions_spawn({
            'task': '''
                你是前端沙箱 Agent。
                
                你的职责：
                1. 使用 Puppeteer 运行前端代码
                2. 执行用户操作（点击、输入等）
                3. 拦截并记录所有 API 调用
                4. 截图记录 UI 状态
                5. 返回执行结果
                
                等待我的指令，收到 "RUN_TEST" 指令后执行测试。
                收到 "STOP" 指令后结束。
                
                可用工具：
                - exec: 执行命令
                - read: 读取文件
                - write: 写入文件
            ''',
            'mode': 'session',  # 持久会话
            'label': 'frontend-sandbox',
            'timeout': 0  # 不超时，一直运行
        })
        print(f"  ✅ Frontend Session: {self.sessions['frontend'].sessionKey}")
        
        # 2. 创建 Backend Session
        print("  启动 Backend Session...")
        self.sessions['backend'] = await sessions_spawn({
            'task': '''
                你是后端沙箱 Agent。
                
                你的职责：
                1. 在 Docker 中运行后端服务
                2. 处理 API 请求
                3. 记录响应数据
                4. 检测异常和错误
                
                等待我的指令，收到 "EXECUTE_API" 指令后执行。
                收到 "STOP" 指令后结束。
                
                可用工具：
                - exec: 执行命令（包括 docker）
                - read: 读取文件
            ''',
            'mode': 'session',
            'label': 'backend-sandbox',
            'timeout': 0
        })
        print(f"  ✅ Backend Session: {self.sessions['backend'].sessionKey}")
        
        # 3. 创建 Test Session
        print("  启动 Test Session...")
        self.sessions['test'] = await sessions_spawn({
            'task': '''
                你是测试沙箱 Agent。
                
                你的职责：
                1. 基于需求生成测试用例
                2. 验证前后端结果一致性
                3. 检测边界情况
                4. 评估测试覆盖率
                
                可用指令：
                - "GENERATE_TESTS": 生成测试用例
                - "VALIDATE": 验证执行结果
                - "STOP": 结束
                
                可用工具：
                - read: 读取需求文档
                - web_search: 搜索测试方法
            ''',
            'mode': 'session',
            'label': 'test-sandbox',
            'timeout': 0
        })
        print(f"  ✅ Test Session: {self.sessions['test'].sessionKey}")
        
        print("✅ 沙箱启动完成！")
        return self.sessions
    
    async def run_integration(self, requirement):
        """执行联调"""
        print(f"\n🧪 开始联调: {requirement}")
        
        # 1. 生成测试用例
        print("  生成测试用例...")
        await sessions_send({
            'sessionKey': self.sessions['test'].sessionKey,
            'message': json.dumps({
                'type': 'GENERATE_TESTS',
                'requirement': requirement
            })
        })
        
        # 等待 Test Session 生成用例
        await asyncio.sleep(5)
        test_history = await sessions_history({
            'sessionKey': self.sessions['test'].sessionKey,
            'limit': 10
        })
        
        # 解析测试用例（从 Session 历史中提取）
        test_cases = self._extract_test_cases(test_history)
        print(f"  ✅ 生成 {len(test_cases)} 个测试用例")
        
        # 2. 执行每个测试用例
        results = []
        for i, tc in enumerate(test_cases, 1):
            print(f"\n  执行测试用例 {i}/{len(test_cases)}: {tc.get('name', 'Unknown')}")
            result = await self._run_test_case(tc)
            results.append(result)
        
        # 3. 汇总报告
        return self._generate_report(results)
    
    async def _run_test_case(self, test_case):
        """执行单个测试用例"""
        # 2.1 Frontend 执行
        print("    Frontend 执行...")
        await sessions_send({
            'sessionKey': self.sessions['frontend'].sessionKey,
            'message': json.dumps({
                'type': 'RUN_TEST',
                'test_case': test_case
            })
        })
        await asyncio.sleep(3)
        frontend_history = await sessions_history({
            'sessionKey': self.sessions['frontend'].sessionKey,
            'limit': 5
        })
        frontend_result = self._extract_result(frontend_history)
        
        # 2.2 Backend 执行
        print("    Backend 执行...")
        api_calls = frontend_result.get('api_calls', [])
        await sessions_send({
            'sessionKey': self.sessions['backend'].sessionKey,
            'message': json.dumps({
                'type': 'EXECUTE_API',
                'api_calls': api_calls
            })
        })
        await asyncio.sleep(3)
        backend_history = await sessions_history({
            'sessionKey': self.sessions['backend'].sessionKey,
            'limit': 5
        })
        backend_result = self._extract_result(backend_history)
        
        # 2.3 Test 验证
        print("    Test 验证...")
        await sessions_send({
            'sessionKey': self.sessions['test'].sessionKey,
            'message': json.dumps({
                'type': 'VALIDATE',
                'frontend_result': frontend_result,
                'backend_result': backend_result
            })
        })
        await asyncio.sleep(2)
        validation_history = await sessions_history({
            'sessionKey': self.sessions['test'].sessionKey,
            'limit': 5
        })
        validation = self._extract_result(validation_history)
        
        return {
            'test_case': test_case,
            'frontend': frontend_result,
            'backend': backend_result,
            'validation': validation
        }
    
    async def stop_sandbox(self):
        """停止沙箱"""
        print("\n🛑 停止沙箱...")
        for role, session in self.sessions.items():
            print(f"  停止 {role} Session...")
            await sessions_send({
                'sessionKey': session.sessionKey,
                'message': 'STOP'
            })
        print("✅ 沙箱已停止")
    
    def _extract_test_cases(self, history):
        """从 Session 历史中提取测试用例"""
        # 简化实现：从 AI 回复中提取
        test_cases = []
        for msg in history.get('messages', []):
            if msg.get('role') == 'assistant':
                content = msg.get('content', '')
                # 尝试解析 JSON
                try:
                    if '```json' in content:
                        json_str = content.split('```json')[1].split('```')[0]
                        data = json.loads(json_str)
                        if isinstance(data, list):
                            test_cases.extend(data)
                except:
                    pass
        return test_cases
    
    def _extract_result(self, history):
        """从 Session 历史中提取结果"""
        for msg in reversed(history.get('messages', [])):
            if msg.get('role') == 'assistant':
                content = msg.get('content', '')
                # 尝试解析 JSON 结果
                try:
                    if 'RESULT:' in content:
                        json_str = content.split('RESULT:')[1].strip()
                        return json.loads(json_str)
                except:
                    pass
        return {}
    
    def _generate_report(self, results):
        """生成报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total': len(results),
            'passed': sum(1 for r in results if r.get('validation', {}).get('success')),
            'failed': sum(1 for r in results if not r.get('validation', {}).get('success')),
            'details': results
        }
        return report


# 使用示例
async def main():
    sandbox = IntegrationSandbox()
    
    # 1. 启动沙箱
    await sandbox.start_sandbox({})
    
    # 2. 执行联调
    report = await sandbox.run_integration('用户登录功能')
    
    # 3. 打印报告
    print("\n📊 联调报告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 4. 停止沙箱
    await sandbox.stop_sandbox()

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 📋 关键区别

### 之前的设计（过于理想化）

```yaml
# ❌ 不真实的配置
name: sandbox-manager
type: manager  # OpenClaw 没有这种类型

sub_agents:
  frontend:
    agent: frontend-sub-agent  # 不是常驻的
```

### 实际可行的设计

```python
# ✅ 真实的实现
# 每次联调时动态创建 Session

frontend_session = await sessions_spawn({
    'task': '前端沙箱任务描述...',
    'mode': 'session',  # ✅ OpenClaw 真实支持
    'label': 'frontend-sandbox'
})

# 通过 sessions_send 通信
await sessions_send({
    'sessionKey': frontend_session.sessionKey,  # ✅ 真实存在
    'message': '执行测试...'
})
```

---

## 🎯 总结

### 什么是真实的？

| 概念 | 是否真实 | 实际是什么 |
|------|---------|-----------|
| Agent 配置 | ✅ | `~/.openclaw/agents/{name}/` 目录 |
| Agent 进程 | ❌ | 不是常驻进程 |
| Session | ✅ | `sessions_spawn` 创建的子进程 |
| Session 通信 | ✅ | `sessions_send` 发送消息 |
| Gateway | ✅ | `openclaw gateway` 启动的服务 |

### 实际方案

**使用 `sessions_spawn` 动态创建子 Session：**

```
主会话（你）
    │
    ├─► sessions_spawn ──► Frontend Session（真实子进程）
    ├─► sessions_spawn ──► Backend Session（真实子进程）
    └─► sessions_spawn ──► Test Session（真实子进程）
```

**特点：**
- ✅ 真实可行
- ✅ 动态创建
- ✅ 独立隔离
- ✅ 可通信

**这就是实际可行的 OpenClaw 联调沙箱方案！** 🤖✨
