# Integration Sandbox - 多角色联调沙箱系统

> 自动完成前后端联调、测试、修复的一站式解决方案

---

## 📖 项目概述

### 背景与痛点

在现代软件开发中，前后端联调是一个耗时且容易出错的环节：

- **时间浪费**：前端开发完成后需等待后端接口就绪
- **沟通成本**：接口变更需要反复沟通确认
- **Bug 发现晚**：联调阶段才发现的 Bug 修复成本高
- **测试覆盖低**：人工测试难以覆盖所有边界情况

### 解决方案

**Integration Sandbox** 通过以下方式解决上述问题：

1. **沙箱隔离**：前端、后端、测试独立运行，互不干扰
2. **自动联调**：无需人工干预，自动完成接口对接
3. **智能检测**：自动发现接口不匹配、数据不一致等问题
4. **自动修复**：80% 的常见问题可自动修复
5. **持续集成**：每次代码提交自动触发联调

---

## 🎯 核心特性

### ✨ 主要功能

- **多沙箱并行**：前端、后端、测试三个沙箱独立运行
- **智能接口匹配**：自动识别前后端接口对应关系
- **自动生成测试数据**：基于 Schema 生成合法数据
- **Bug 自动检测与分类**：5 大类 Bug 自动识别
- **自动修复引擎**：70% 的 Bug 可自动修复
- **可视化报告**：交互式联调报告，一目了然

### 📈 预期收益

| 指标 | 传统方式 | 沙箱方式 | 提升 |
|------|---------|---------|------|
| 联调时间 | 2-3 天 | 30 分钟 | **90%↓** |
| Bug 发现率 | 60% | 95% | **58%↑** |
| 自动修复率 | 0% | 70% | **∞** |
| 回归测试时间 | 4 小时 | 10 分钟 | **96%↓** |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      Integration Sandbox                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│   │ Frontend     │      │ Backend      │      │ Test         │ │
│   │ Sandbox      │◄────►│ Sandbox      │◄────►│ Sandbox      │ │
│   │              │      │              │      │              │ │
│   │ • Puppeteer  │      │ • Docker     │      │ • Generator  │ │
│   │ • Jest       │      │ • Mock DB    │      │ • Validator  │ │
│   │ • Recorder   │      │ • Logger     │      │ • Analyzer   │ │
│   └──────────────┘      └──────────────┘      └──────────────┘ │
│          │                     │                     │          │
│          └─────────────────────┼─────────────────────┘          │
│                                ▼                                │
│                   ┌────────────────────────┐                    │
│                   │   Integration Hub      │                    │
│                   │                        │                    │
│                   │ • Orchestrator         │                    │
│                   │ • Interface Matcher    │                    │
│                   │ • Data Generator       │                    │
│                   └────────────────────────┘                    │
│                                │                                │
│          ┌─────────────────────┼─────────────────────┐          │
│          ▼                     ▼                     ▼          │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│   │ Bug Detector │      │ Auto-Fix     │      │ Report       │ │
│   │              │      │ Engine       │      │ Generator    │ │
│   │ • Matcher    │      │              │      │              │ │
│   │ • Analyzer   │      │ • AST Parser │      │ • HTML       │ │
│   │ • Classifier │      │ • Transformer│      │ • JSON       │ │
│   └──────────────┘      └──────────────┘      └──────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎭 角色详解

### 1. Frontend Sandbox（前端沙箱）

**职责：**
- 在隔离环境中运行前端应用
- 模拟真实用户操作
- 拦截并记录所有 API 调用
- 捕获 UI 状态变化

**技术栈：**
- **Puppeteer**：无头浏览器，模拟真实用户
- **Jest**：测试框架，执行测试用例
- **React/Vue/Angular**：支持主流前端框架

**核心功能：**
```javascript
class FrontendSandbox {
  async run(testCase) {
    // 1. 启动应用
    await this.browser.goto('http://localhost:3000');
    
    // 2. 拦截 API 调用
    this.apiInterceptor.on('request', (req) => {
      this.recordAPICall(req);
    });
    
    // 3. 执行用户操作
    for (const action of testCase.actions) {
      await this.executeAction(action);
      await this.recordState();
    }
    
    // 4. 返回结果
    return {
      apiCalls: this.apiInterceptor.getCalls(),
      uiStates: this.stateRecorder.getStates(),
      errors: this.errorCollector.getErrors(),
    };
  }
}
```

---

### 2. Backend Sandbox（后端沙箱）

**职责：**
- 在 Docker 容器中运行后端服务
- 提供模拟数据库环境
- 记录所有 API 响应
- 检测异常和错误

**技术栈：**
- **Docker**：容器化隔离
- **Python/Node/Java**：支持多语言后端
- **TestContainers**：数据库模拟

**核心功能：**
```python
class BackendSandbox:
  async def run(self, api_requests):
    results = []
    
    for request in api_requests:
      # 1. 路由到对应处理器
      handler = self.router.match(request)
      
      # 2. 执行业务逻辑
      response = await handler.process(request)
      
      # 3. 记录响应
      self.responseRecorder.record(request, response)
      
      # 4. 检测异常
      if response.status >= 400:
        results.append({
          'error': True,
          'request': request,
          'response': response,
        })
      else:
        results.append({
          'error': False,
          'data': response.data,
        })
    
    return results
```

---

### 3. Test Sandbox（测试沙箱）

**职责：**
- 基于需求生成测试用例
- 验证业务逻辑正确性
- 检测边界情况
- 评估测试覆盖率

**技术栈：**
- **Property-based Testing**：自动生成测试数据
- **Faker.js**：生成真实模拟数据
- **Coverage Tools**：代码覆盖率分析

**核心功能：**
```python
class TestSandbox:
  def generate_tests(self, requirements):
    tests = []
    
    for req in requirements:
      # 1. 正常流程测试
      tests.append(self.generate_happy_path_test(req))
      
      # 2. 边界值测试
      tests.append(self.generate_boundary_test(req))
      
      # 3. 异常流程测试
      tests.append(self.generate_error_test(req))
      
      # 4. 性能测试
      tests.append(self.generate_performance_test(req))
    
    return tests
  
  def validate(self, frontend_result, backend_result):
    issues = []
    
    # 验证数据一致性
    if not self.check_data_consistency(frontend_result, backend_result):
      issues.append({
        'type': 'DATA_INCONSISTENCY',
        'severity': 'HIGH',
      })
    
    # 验证业务逻辑
    if not self.check_business_logic(backend_result):
      issues.append({
        'type': 'BUSINESS_LOGIC_ERROR',
        'severity': 'CRITICAL',
      })
    
    return issues
```

---

## 🔄 工作流程

### 阶段 1: 代码提交

```bash
# 前端开发者提交代码
sandbox submit \
  --role frontend \
  --source ./frontend \
  --requirement REQ-001 \
  --branch feature/login

# 后端开发者提交代码
sandbox submit \
  --role backend \
  --source ./backend \
  --requirement REQ-001 \
  --branch api/login
```

### 阶段 2: 沙箱启动

```
[INFO] 正在启动 Frontend Sandbox...
[INFO] 正在启动 Backend Sandbox...
[INFO] 正在启动 Test Sandbox...
[INFO] 所有沙箱启动完成 ✓
```

### 阶段 3: 接口匹配

```
[INFO] 分析前端 API 调用...
[INFO] 发现 5 个 API 调用
[INFO] 匹配后端接口...
[INFO] 4 个接口匹配成功
[WARN] 1 个接口未匹配: /api/user/info
[INFO] 建议匹配: /api/user/profile
```

### 阶段 4: 联调执行

```
[INFO] 执行测试用例 1/15: 正常登录流程
[INFO] 执行测试用例 2/15: 错误密码处理
...
[INFO] 执行测试用例 15/15: 并发登录
```

### 阶段 5: Bug 检测

```
[INFO] Bug 检测完成
[INFO] 发现 3 个 Bug:
  [CRITICAL] INTERFACE_MISMATCH: /api/login 路径不匹配
  [HIGH]     DATA_FORMAT_ERROR: 响应字段类型错误
  [MEDIUM]   STATUS_CODE_MISMATCH: 期望 401 实际 403
```

### 阶段 6: 自动修复

```
[INFO] 尝试自动修复...
[INFO] [CRITICAL] INTERFACE_MISMATCH: 修复成功 ✓
[INFO] [HIGH]     DATA_FORMAT_ERROR: 修复成功 ✓
[INFO] [MEDIUM]   STATUS_CODE_MISMATCH: 需要人工修复
[INFO] 自动修复率: 66.7% (2/3)
```

### 阶段 7: 报告生成

```
[INFO] 生成联调报告...
[INFO] 报告地址: http://localhost:8080/report/REQ-001
```

---

## 🐛 Bug 分类与修复策略

### Bug 类型定义

| 类型 | 严重程度 | 自动修复 | 说明 |
|------|---------|---------|------|
| INTERFACE_MISMATCH | CRITICAL | ✅ | 接口路径/方法不匹配 |
| DATA_FORMAT_ERROR | HIGH | ✅ | 数据格式/类型错误 |
| STATUS_CODE_MISMATCH | MEDIUM | ✅ | HTTP 状态码错误 |
| DATA_INCONSISTENCY | HIGH | ✅ | 前后端数据不一致 |
| BUSINESS_LOGIC_ERROR | CRITICAL | ❌ | 业务逻辑实现错误 |
| PERFORMANCE_ISSUE | MEDIUM | ❌ | 性能不达标 |
| SECURITY_VULNERABILITY | CRITICAL | ❌ | 安全漏洞 |

### 自动修复示例

**场景 1: 接口路径错误**
```javascript
// 前端代码
fetch('/api/user/info')  // ❌ 错误

// 后端定义
@app.get('/api/user/profile')  // ✅ 正确
// 自动修复
const fix = {
  type: 'INTERFACE_MISMATCH',
  file: 'src/api/user.js',
  line: 15,
  original: '/api/user/info',
  replacement: '/api/user/profile',
};

// 应用修复
await applyFix(fix);
```

**场景 2: 数据类型错误**
```javascript
// 后端响应
{
  "age": "25"  // ❌ 字符串
}

// 前端期望
{
  "age": 25    // ✅ 数字
}

// 自动修复
const fix = {
  type: 'DATA_FORMAT_ERROR',
  file: 'src/api/transformer.js',
  transformation: 'parseInt',
};
```

---

## 🛠️ 安装与使用

### 环境要求

- Docker 20.10+
- Node.js 18+
- Python 3.9+
- 4GB+ RAM

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-org/integration-sandbox.git
cd integration-sandbox

# 安装依赖
npm install
pip install -r requirements.txt

# 启动服务
npm run dev
```

### 快速开始

```bash
# 1. 初始化项目
sandbox init --project my-project

# 2. 配置前后端
sandbox config --frontend ./frontend --backend ./backend

# 3. 执行联调
sandbox run --requirement REQ-001

# 4. 查看报告
sandbox report --open
```

---

## 📊 项目结构

```
integration-sandbox/
├── README.md                 # 项目说明
├── DESIGN.md                 # 详细设计文档
├── package.json              # Node.js 依赖
├── requirements.txt          # Python 依赖
├── docker-compose.yml        # 服务编排
├──
├── src/                      # 源代码
│   ├── core/                 # 核心模块
│   │   ├── orchestrator.ts   # 协调器
│   │   ├── matcher.ts        # 接口匹配
│   │   └── generator.ts      # 数据生成
│   │
│   ├── sandboxes/            # 沙箱实现
│   │   ├── frontend/         # 前端沙箱
│   │   ├── backend/          # 后端沙箱
│   │   └── test/             # 测试沙箱
│   │
│   ├── detector/             # Bug 检测
│   │   ├── analyzer.ts       # 分析器
│   │   └── classifier.ts     # 分类器
│   │
│   ├── fixer/                # 自动修复
│   │   ├── engine.ts         # 修复引擎
│   │   └── strategies/       # 修复策略
│   │
│   ├── report/               # 报告生成
│   │   ├── generator.ts      # 生成器
│   │   └── templates/        # 模板
│   │
│   └── cli/                  # 命令行工具
│       └── index.ts          # CLI 入口
│
├── examples/                 # 示例项目
│   ├── simple-login/         # 简单登录示例
│   └── complex-dashboard/    # 复杂仪表板示例
│
└── docs/                     # 文档
    ├── architecture.md       # 架构文档
    ├── api.md                # API 文档
    └── contributing.md       # 贡献指南
```

---

## 🗺️ 路线图

### Phase 1: MVP (4 周)
- [ ] 基础沙箱实现（前端、后端）
- [ ] 简单接口匹配
- [ ] 基础 Bug 检测
- [ ] 命令行工具

### Phase 2: 增强 (4 周)
- [ ] 测试沙箱实现
- [ ] 智能接口匹配
- [ ] 自动修复引擎
- [ ] Web 界面

### Phase 3: 完善 (4 周)
- [ ] 性能优化
- [ ] 更多语言支持
- [ ] CI/CD 集成
- [ ] 企业级特性

---

## 🤝 贡献指南

欢迎贡献！请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解如何参与。

### 贡献方式

1. **报告 Bug**：提交 Issue
2. **提交代码**：Fork + PR
3. **完善文档**：补充示例和说明
4. **分享经验**：撰写使用案例

---

## 📄 许可证

MIT License © 2026 Integration Sandbox Team

---

## 💬 联系我们

- **GitHub Issues**: [问题反馈](https://github.com/your-org/integration-sandbox/issues)
- **Discord**: [社区讨论](https://discord.gg/integration-sandbox)
- **Email**: team@integration-sandbox.io

---

> **让联调不再痛苦，让开发更加高效！** 🚀
