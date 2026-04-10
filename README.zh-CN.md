# evo-agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**🌐 语言:** [English](README.md) | [简体中文](README.zh-CN.md)

---

## ⚡ 快速开始

### 一行安装

```bash
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s my-agent
```

**完成！** 几秒钟内拥有功能完整的 Agent 工作区。

---

## 🎯 什么是 evo-agents?

**生产级 OpenClaw Agent 模板**，包含：

- 📦 **预配置技能** - 记忆搜索、RAG、自进化
- 🔒 **数据隔离** - 每个 Agent 独立工作区
- 🛠️ **开箱即用** - 安装、激活、清理脚本
- 🧠 **Harness Agent** - 8 个领域插件处理复杂任务
- 📚 **高级记忆** - 分层压缩（日→周→月）

---

## ✨ 核心特性

### 1. 多 Agent 架构

```
evo-agents/
├── agents/          # 隔离的 Agent
├── skills/          # 共享技能
├── memory/          # 记忆文件
└── libs/            # 共享库
```

### 2. Harness Agent 插件

**8 个领域插件:** 编程 | 电商 | 数据分析 | DevOps | 营销 | 内容创作 | 自媒体

```bash
/harness-agent "开发博客系统" --domain programming
```

### 3. 高级记忆系统

| 层级 | 保留时间 | 压缩时间 |
|------|---------|---------|
| **每日** | 14 天 | 每天 09:30 |
| **每周** | 8 周 | 周日 03:00 |
| **每月** | 2 个月 | 1 号 04:00 |

**搜索:** 月→周→日→全量

---

## 📚 文档

- **[快速开始](docs/QUICKSTART.md)** - 5 分钟指南
- **[常见问题](docs/FAQ.md)** - 常见问题解答
- **[技能指南](docs/SKILLS_GUIDE.md)** - 技能使用说明

---

## 🔧 脚本

```bash
# 安装
./install.sh my-agent

# 激活功能
./scripts/core/activate-features.sh

# 记忆管理
python3 scripts/core/memory_manager.py --all
```

---

## 📊 状态

- ✅ 记忆管理器（日/周/月）
- ✅ 分层搜索
- ✅ 增量压缩
- ✅ 自动清理

---

**许可:** MIT | **创建:** 2026-04 | **最后更新:** 2026-04-10
