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

### 3. 使用记忆搜索

```bash
python3 skills/memory-search/search.py "你的查询"
```

### 4. 记录会话

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
