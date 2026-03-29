# evo-agents 核心测试清单

**版本：** v1.1.0  
**更新日期：** 2026-03-29  
**测试范围：** 核心功能回归

---

## 📋 测试维度（精简版）

1. [安装流程](#1-安装流程) - 8 项
2. [目录结构](#2-目录结构) - 6 项
3. [路径系统](#3-路径系统) - 4 项
4. [核心功能](#4-核心功能) - 15 项
5. [子 Agent](#5-子 agent) - 8 项
6. [数据隔离](#6-数据隔离) - 6 项
7. [维护工具](#7-维护工具) - 6 项
8. [文档完整性](#8-文档完整性) - 4 项

**总计：57 个核心测试点**

---

## 1. 安装流程

### 1.1 新安装
- [ ] 1.1.1 Gitee 源安装成功（国内）
- [ ] 1.1.2 GitHub 源安装成功（海外）
- [ ] 1.1.3 workspace 创建成功
- [ ] 1.1.4 OpenClaw 注册成功
- [ ] 1.1.5 .install-config 创建

### 1.2 清理验证
- [ ] 1.2.1 删除 .github/ 目录
- [ ] 1.2.2 删除 CONTRIBUTING.md 等
- [ ] 1.2.3 保留 libs/memory_hub

---

## 2. 目录结构

### 2.1 必需目录
- [ ] 2.1.1 scripts/core/ 存在
- [ ] 2.1.2 skills/ 存在（4 个通用技能）
- [ ] 2.1.3 libs/memory_hub/ 存在
- [ ] 2.1.4 memory/ 存在
- [ ] 2.1.5 data/ 存在
- [ ] 2.1.6 docs/ 存在（仅用户文档）

---

## 3. 路径系统

### 3.1 path_utils
- [ ] 3.1.1 resolve_workspace() 正确
- [ ] 3.1.2 resolve_agent_memory() 正确
- [ ] 3.1.3 resolve_data_dir() 正确
- [ ] 3.1.4 支持环境变量覆盖

---

## 4. 核心功能

### 4.1 会话记录
- [ ] 4.1.1 记录事件（event）
- [ ] 4.1.2 记录决定（decision）
- [ ] 4.1.3 记录学习（learning）
- [ ] 4.1.4 支持 --agent 参数

### 4.2 记忆索引
- [ ] 4.2.1 全量索引（--full）
- [ ] 4.2.2 增量索引（--incremental）
- [ ] 4.2.3 SQLite 数据库创建

### 4.3 记忆搜索
- [ ] 4.3.1 关键词搜索
- [ ] 4.3.2 语义搜索（需要 Ollama）
- [ ] 4.3.3 统一搜索（unified_search.py）

### 4.4 双向同步
- [ ] 4.4.1 Markdown → SQLite
- [ ] 4.4.2 SQLite → Markdown
- [ ] 4.4.3 不重复同步

### 4.5 自检功能
- [ ] 4.5.1 25 项完整性检查
- [ ] 4.5.2 自动修复可修复问题
- [ ] 4.5.3 JSON 报告生成

---

## 5. 子 Agent

### 5.1 创建子 Agent
- [ ] 5.1.1 add-agent.sh 执行成功
- [ ] 5.1.2 agents/<agent>/ 目录创建
- [ ] 5.1.3 skills/ 符号链接创建
- [ ] 5.1.4 OpenClaw 注册成功

### 5.2 子 Agent 运行
- [ ] 5.2.1 从子 agent 目录运行父脚本
- [ ] 5.2.2 路径解析正确
- [ ] 5.2.3 技能共享正常
- [ ] 5.2.4 数据目录自动创建

---

## 6. 数据隔离

### 6.1 多 Agent 数据
- [ ] 6.1.1 主 agent 数据在 data/<main>/
- [ ] 6.1.2 子 agent 数据在 data/<sub>/
- [ ] 6.1.3 数据不会交叉污染

### 6.2 硬编码清理
- [ ] 6.2.1 没有 ai-baby 硬编码
- [ ] 6.2.2 没有 demo-agent 硬编码
- [ ] 6.2.3 没有 /Users/dhr 硬编码

### 6.3 运行时数据
- [ ] 6.3.1 data/ 只有当前 agent 数据
- [ ] 6.3.2 .gitkeep 保持目录结构
- [ ] 6.3.3 没有历史测试数据残留

---

## 7. 维护工具

### 7.1 重装/修复
- [ ] 7.1.1 reinstall.sh 可用
- [ ] 7.1.2 自动备份
- [ ] 7.1.3 自动修复硬编码

### 7.2 卸载
- [ ] 7.2.1 uninstall-agent.sh 可用
- [ ] 7.2.2 uninstall-workspace.sh 可用
- [ ] 7.2.3 从 OpenClaw 注销

### 7.3 自检
- [ ] 7.3.1 self-check.py 可用
- [ ] 7.3.2 --fix 参数修复
- [ ] 7.3.3 --report 参数生成 JSON

---

## 8. 文档完整性

### 8.1 用户文档
- [ ] 8.1.1 README.md 存在
- [ ] 8.1.2 QUICKSTART.md 存在
- [ ] 8.1.3 FAQ.md 存在
- [ ] 8.1.4 SELF_CHECK.md 存在
- [ ] 8.1.5 UNINSTALL.md 存在
- [ ] 8.1.6 AGENT_INSTRUCTIONS.md 存在
- [ ] 8.1.7 WORKSPACE_RULES.md 存在
- [ ] 8.1.8 INDEX.md 存在

### 8.2 架构文档
- [ ] 8.2.1 ARCHITECTURE_GENERIC_CN.md 存在
- [ ] 8.2.2 ARCHITECTURE_GENERIC_EN.md 存在
- [ ] 8.2.3 PERFORMANCE_OPTIMIZATION_PLAN.md 存在

### 8.3 文档内容
- [ ] 8.3.1 没有硬编码路径
- [ ] 8.3.2 示例使用通用路径

---

## 📊 测试执行记录

### 执行信息
- **执行日期：** _________
- **执行者：** _________
- **Workspace:** _________
- **版本：** v1.1.0

### 测试结果

| 维度 | 测试项数 | 通过 | 失败 | 通过率 |
|------|---------|------|------|--------|
| 1. 安装流程 | 8 | | | |
| 2. 目录结构 | 6 | | | |
| 3. 路径系统 | 4 | | | |
| 4. 核心功能 | 15 | | | |
| 5. 子 Agent | 8 | | | |
| 6. 数据隔离 | 6 | | | |
| 7. 维护工具 | 6 | | | |
| 8. 文档完整性 | 4 | | | |
| **总计** | **57** | | | |

### 通过标准

- **关键测试（1-4 维度）：** 100% 通过
- **重要测试（5-7 维度）：** 95% 通过
- **文档测试（第 8 维度）：** 100% 通过

**总体通过率要求：** ≥98%

---

## ✅ 快速测试脚本

```bash
# 1. 安装测试
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s test-agent

# 2. 目录检查
cd ~/.openclaw/workspace-test-agent
find . -maxdepth 2 -type d | grep -v ".git" | sort

# 3. 路径测试
python3 -c "from scripts.core.path_utils import resolve_workspace; print(resolve_workspace())"

# 4. 核心功能
python3 scripts/core/session_recorder.py -t event -c "测试"
python3 scripts/core/memory_indexer.py --full
python3 scripts/core/unified_search.py "测试"
python3 scripts/core/self-check.py

# 5. 子 Agent
bash scripts/core/add-agent.sh sub-test "Sub Test" 🤖
cd agents/sub-test && python3 ../../scripts/core/session_recorder.py -t event -c "子 agent 测试" --agent sub-test

# 6. 数据隔离
ls -la data/
grep -rn "ai-baby" skills/ --include="*.py" --include="*.json" | wc -l

# 7. 维护工具
bash scripts/core/reinstall.sh
bash scripts/core/uninstall-agent.sh sub-test

# 8. 文档检查
ls docs/*.md
```

---

**最后更新：** 2026-03-29  
**维护者：** evo-agents team
