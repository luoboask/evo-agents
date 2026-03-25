# Sandbox Agent

> 可管理的联调沙箱 Agent，支持多实例并行执行

---

## 🎯 功能特性

- ✅ **实例化管理** - 每个需求一个独立沙箱实例
- ✅ **多实例并行** - 支持同时运行多个实例
- ✅ **完全隔离** - 每个实例独立端口、独立资源
- ✅ **自动协调** - Frontend/Backend/Test 三个 Session 自动协调
- ✅ **生命周期管理** - 创建、启动、停止、销毁完整生命周期
- ✅ **报告生成** - 自动生成联调报告

---

## 🚀 快速开始

### 安装

```bash
# 复制到 OpenClaw agents 目录
cp -r sandbox-agent ~/.openclaw/agents/

# 安装依赖
pip install -r requirements.txt
```

### 使用

```python
from agent import SandboxAgent
import asyncio

async def main():
    # 创建 Agent
    agent = SandboxAgent()
    
    # 创建实例
    instance_id = await agent.create_instance(
        requirement_id='REQ-001',
        config={
            'frontend_code': './frontend/login',
            'backend_code': './backend/login',
            'requirement_desc': '用户登录功能'
        }
    )
    
    # 启动实例
    await agent.start_instance(instance_id)
    
    # 执行联调
    report = await agent.run_integration(instance_id)
    
    # 打印结果
    print(f"通过: {report['summary']['passed']}/{report['summary']['total']}")
    
    # 停止实例
    await agent.stop_instance(instance_id)
    
    # 销毁实例
    await agent.destroy_instance(instance_id)

asyncio.run(main())
```

---

## 📁 项目结构

```
sandbox-agent/
├── agent.py          # 主 Agent 代码
├── config.yaml       # 配置文件
├── requirements.txt  # 依赖
└── README.md         # 说明文档
```

---

## 🎭 架构

```
SandboxAgent
├── create_instance()      # 创建实例
├── start_instance()       # 启动实例
├── stop_instance()        # 停止实例
├── destroy_instance()     # 销毁实例
├── run_integration()      # 执行联调
└── get_status()           # 获取状态

Instance
├── Frontend Session
├── Backend Session
└── Test Session
```

---

## 📊 状态管理

| 状态 | 说明 |
|------|------|
| CREATED | 已创建，未启动 |
| STARTING | 正在启动 |
| RUNNING | 运行中 |
| STOPPED | 已停止 |
| ERROR | 发生错误 |
| DESTROYED | 已销毁 |

---

## 🔧 配置

编辑 `config.yaml`：

```yaml
# 端口范围
instance:
  port_range:
    start: 8000
    end: 9000

# 最大实例数
resources:
  max_instances: 10
```

---

## 📈 性能

- 单实例启动时间: ~5s
- 联调执行时间: 取决于需求复杂度
- 支持并行实例数: 10+（取决于系统资源）

---

## 📝 License

MIT
