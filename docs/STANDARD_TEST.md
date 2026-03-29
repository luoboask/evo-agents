# 标准测试流程

## 测试脚本

```bash
cd /Users/dhr/.openclaw/workspace-<agent-name>
bash run_standard_test.sh
```

## 测试项目（固定 30 项）

### 1. 安装验证 (7 项)
- Workspace 存在
- scripts/core 存在
- skills/memory-search 存在
- skills/rag 存在
- skills/self-evolution 存在
- skills/web-knowledge 存在
- libs/memory_hub 存在

### 2. 路径系统 (1 项)
- path_utils 正常工作

### 3. 核心功能 (7 项)
- 会话记录
- 记忆索引
- 索引数据库
- 记忆搜索
- 双向同步
- 健康检查
- 自检功能

### 4. 子 Agent (6 项)
- 创建子 agent
- 子 agent 目录
- skills 符号链接
- OpenClaw 注册
- 子 agent 运行
- 子 agent 数据

### 5. 激活功能 (1 项)
- 激活所有功能

### 6. 维护工具 (3 项)
- reinstall.sh
- uninstall-agent.sh
- uninstall-workspace.sh

### 7. 文档 (2 项)
- README.md
- TEST_REGRESSION_CHECKLIST.md

### 8. 数据隔离 (3 项)
- 主 agent 数据
- 子 agent 数据
- 无硬编码

**总计：30 项（固定）**

