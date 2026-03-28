# evo-agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.13-green.svg)](https://github.com/openclaw/openclaw)

**🌐 语言:** [English](README.md) | [简体中文](README.zh-CN.md)

**🤖 OpenClaw 多 Agent Workspace 模板**

可复用的自进化 Agent workspace，具有严格的数据隔离、共享能力层和生产级工具链。

---

## ⚡ 快速开始

**一行命令安装：**

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

**就这么简单！** 几秒钟内拥有一个功能完整的 Agent workspace。

---

## 🎯 什么是 evo-agents？

evo-agents 是一个**生产级模板**，用于创建隔离的 OpenClaw Agent，具有：

- 📦 **预配置技能** - 记忆搜索、RAG、自进化、网络知识
- 🔒 **数据隔离** - 每个 Agent 有自己的 workspace、记忆和配置
- 🛠️ **即用脚本** - 安装、激活、清理、卸载
- 📚 **完整文档** - 安装、使用、迁移指南
- 🧪 **测试流程** - 备份、恢复、多 Agent 设置

---

## ✨ 特性

| 特性 | 描述 |
|------|------|
| 🔍 **语义搜索** | Ollama 驱动的向量搜索 + Embedding 缓存 |
| 📚 **知识库** | SQLite + Markdown 双重存储 + 自动同步 |
| 🧬 **自进化** | 分形思考 + 夜间反思循环 |
| 📊 **RAG 评估** | 自动评估 + 自动调优 |
| 🌐 **网络知识** | 多引擎搜索 + 网页爬取 |
| 🤖 **多 Agent** | 创建和管理多个隔离的 Agent |

---

## 📦 安装

### 新安装

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

### 更新现有

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent
```

### 交互模式

```bash
curl -sO https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh
bash install.sh my-agent
```

### 强制安装

```bash
curl -fsSL https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent --force
```

---

## 🚀 使用

### 1. 激活功能

安装后，激活高级功能：

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/activate-features.sh
```

### 2. 创建子 Agent

```bash
./scripts/core/add-agent.sh assistant "我的助手" 🤖
./scripts/core/setup-multi-agent.sh researcher writer editor
```

### 3. 卸载 Agent

**卸载整个 workspace：**

```bash
# 交互式（推荐）
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-workspace.sh

# 或指定 agent 名称
./scripts/core/uninstall-workspace.sh my-agent
```

**卸载流程：**
1. ⚠️  要求确认（输入 agent 名称）
2. 📝  从 OpenClaw 注销（`openclaw agents delete --force`）
3. 🗑️  删除 workspace 目录
4. 💾  可选备份

**卸载子 Agent：**

```bash
cd ~/.openclaw/workspace-my-agent
./scripts/core/uninstall-agent.sh assistant-agent
```

**⚠️  警告：**
- 先备份：`cp -r ~/.openclaw/workspace-my-agent /tmp/backup`
- 卸载是永久的（workspace 移到回收站，OpenClaw 配置被删除）
- workspace 内的子 Agent 不会自动卸载

### 4. 自检与自动修复

**检查工作区健康状态：**

```bash
cd ~/.openclaw/workspace-my-agent
python3 scripts/core/self_check.py
```

**自动修复问题：**

```bash
# 预览修复
python3 scripts/core/self_check.py --dry-run

# 执行修复
python3 scripts/core/self_check.py --fix
```

**检查项目：**
- ✅ 目录结构完整性
- ✅ 关键文件存在性
- ✅ 运行时数据（不应该存在的目录）
- ✅ Git 配置
- ✅ OpenClaw 注册状态
- ✅ 路径系统功能
- ✅ 技能完整性
- ✅ 数据库健康

**可自动修复：**
- 🔧 创建缺失目录（自动添加 .gitkeep）
- 🔧 删除异常目录（scripts/data, scripts/memory）
- 🔧 清理 data/ 目录
- 🔧 重建索引数据库

---

### 5. 使用记忆搜索

```bash
python3 skills/memory-search/search.py "你的查询"
```

### 5. 记录会话

```bash
python3 scripts/core/session_recorder.py -t event -c "你的内容" --agent my-agent
```

---

## 📁 项目结构

```
~/.openclaw/workspace-my-agent/
├── scripts/           # 共享脚本
│   └── core/          # 核心工具
├── skills/            # 技能 (4 个通用 + 自定义)
│   ├── memory-search/ # 语义搜索
│   ├── rag/           # RAG 评估
│   ├── self-evolution/# 自进化
│   └── web-knowledge/ # 网络搜索 + 爬取
├── memory/            # 每日记忆文件
├── data/              # Agent 特定数据
└── docs/              # 文档
```

---

## 📖 文档

| 文档 | 描述 |
|------|------|
| **[安装指南](workspace-setup.md)** | 完整安装指南 |
| **[迁移](docs/MIGRATION.md)** | 从旧版本更新 |
| **[功能](FEATURE_ACTIVATION_GUIDE.md)** | 激活高级功能 |
| **[结构](docs/STRUCTURE_RULES.md)** | 项目结构规则 |
| **[Workspace](docs/WORKSPACE_RULES.md)** | Workspace 使用规则 |
| **[Agent](docs/AGENT_INSTRUCTIONS.md)** | Agent 指令 |
| **[FAQ](docs/FAQ.md)** | 常见问题 |
| **[性能](docs/PERFORMANCE_OPTIMIZATION_PLAN.md)** | 性能优化方案 |

---

## 🤝 贡献

欢迎贡献！详情请查看 [贡献指南](CONTRIBUTING.md)。

### 快速开始

1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 运行测试
5. 提交 Pull Request

### 行为准则

请在贡献前阅读 [行为准则](CODE_OF_CONDUCT.md)。

---

## 🐛 问题

发现 Bug 或有功能建议？

- 🐛 [报告 Bug](https://github.com/luoboask/evo-agents/issues/new?template=bug_report.md)
- 💡 [功能建议](https://github.com/luoboask/evo-agents/issues/new?template=feature_request.md)
- ❓ [提问](https://github.com/luoboask/evo-agents/discussions)

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - Agent 框架
- [Ollama](https://ollama.com/) - 本地 LLM 和 Embedding
- [SQLite](https://www.sqlite.org/) - 轻量级数据库

---

## 📬 联系方式

- 🌐 网站：https://github.com/luoboask/evo-agents
- 📧 邮箱：[Your email]
- 💬 Discord: [Your Discord]

---

**Made with ❤️ by the evo-agents team**
