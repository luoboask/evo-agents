# evo-agents

[English](./README.md) | [简体中文](./README.zh-CN.md)

**OpenClaw 多 Agent Workspace 模板**

---

## 🦞 一键安装（推荐）⭐

**用 OpenClaw 自然语言安装：**

```bash
openclaw agent --message "Read https://raw.githubusercontent.com/luoboask/evo-agents/master/workspace-setup.md and help me install"
```

**或者手动安装：**

```bash
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent
./scripts/activate-features.sh
```

---

## 🚀 快速使用

### 创建多 Agent

```bash
./scripts/setup-multi-agent.sh analyst developer tester
```

### 新增单个 Agent

```bash
./scripts/add-agent.sh designer "UI 设计师" 🎨
```

### 激活高级功能

```bash
./scripts/activate-features.sh
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [workspace-setup.md](workspace-setup.md) | ⭐ 完整安装指南 |
| [FEATURE_ACTIVATION_GUIDE.md](FEATURE_ACTIVATION_GUIDE.md) | 功能激活指南 |

---

**GitHub:** https://github.com/luoboask/evo-agents
