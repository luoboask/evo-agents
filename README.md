# evo-agents

[English](./README.md) | [简体中文](./README.zh-CN.md)

Reusable self-evolving agent workspace with explicit runtime context (`--workspace`, `--agent`), strict per-agent data isolation, and shared capability layers.

---

## 🦞 OpenClaw One-Click Install (Recommended) ⭐

**如果你有 OpenClaw，可以用自然语言一键安装：**

```bash
openclaw agent --message "Read https://raw.githubusercontent.com/luoboask/evo-agents/master/workspace-setup.md and help me install a workspace named demo-agent"
```

**OpenClaw 会：**
1. 读取 `workspace-setup.md` 安装指南
2. 克隆模板到 `~/.openclaw/workspace-demo-agent`
3. 创建目录结构
4. 注册 `demo-agent` 到 OpenClaw
5. 配置多 Agent 系统（可选）
6. 运行测试

---

## 🚀 Quick Start

### Option 1: Manual Install

```bash
# 1. Clone template
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent
cd ~/.openclaw/workspace-my-agent

# 2. Create directory structure
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/my-agent

# 3. Register OpenClaw agent
openclaw agents add my-agent --workspace "$(pwd)" --non-interactive

# 4. Test
python3 scripts/session_recorder.py -t event -c 'Hello world'
python3 scripts/unified_search.py 'hello' --agent my-agent --semantic
```

---

## 🔧 Feature Activation

After installation, activate advanced features interactively:

```bash
./scripts/activate-features.sh
```

**Available Features:**
1. 🔮 Semantic Search (Ollama + Embedding Models)
2. 📚 Knowledge Base System
3. 🧬 Self-Evolution System
4. 📊 RAG Evaluation
5. ⏰ Scheduled Tasks (Cron)
6. ✅ Activate All
7. ❌ Skip

**Embedding Models:**
- bge-m3 (1.2GB, 🇨🇳 Chinese)
- nomic-embed-text (274MB, 🇺🇸 English)
- mxbai-embed-large (670MB, 🌍 Multi-language)
- all-minilm (46MB, 🇺🇸 English, Fast)

**Documentation:**
- `FEATURE_ACTIVATION_GUIDE.md` - Full activation guide
- `workspace-setup.md` - Complete installation playbook

---

## 🤖 Multi-Agent Scripts

### setup-multi-agent.sh - Create Multiple Agents

```bash
./scripts/setup-multi-agent.sh designer writer ops
# Creates: designer-agent, writer-agent, ops-agent
```

### add-agent.sh - Add Single Agent

```bash
./scripts/add-agent.sh designer UI/UX 设计师 🎨
# Creates: designer-agent (UI/UX 设计师 🎨)
```

---

## 📁 Directory Structure

```
evo-agents/
├── 📄 Root Files
│   ├── README.md
│   ├── README.zh-CN.md
│   ├── workspace-setup.md
│   └── FEATURE_ACTIVATION_GUIDE.md
│
├── 🔧 scripts/
│   ├── activate-features.sh
│   ├── setup-multi-agent.sh
│   ├── add-agent.sh
│   └── ...
│
├── 📚 libs/
│   └── memory_hub/
│
├── 🎯 skills/
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📂 agents/
│   └── .gitkeep
│
└── 📖 docs/
    ├── ARCHITECTURE_GENERIC_EN.md
    └── PROJECT_STRUCTURE_GENERIC_EN.md
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `workspace-setup.md` | ⭐ Complete installation guide |
| `FEATURE_ACTIVATION_GUIDE.md` | Feature activation guide |
| `README.md` | Quick start (English) |
| `README.zh-CN.md` | Quick start (Chinese) |
| `docs/ARCHITECTURE_GENERIC_EN.md` | Architecture design |
| `docs/PROJECT_STRUCTURE_GENERIC_EN.md` | Directory structure |

---

**Last Updated:** 2026-03-26
