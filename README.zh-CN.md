# test-agents - OpenClaw 多 Agent Workspace

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

**给 OpenClaw Agent 真正的记忆和多 Agent 协作能力。**

[English](./README.md) | [简体中文](./README.zh-CN.md)

---

## 🎯 特性

| 特性 | 说明 |
|------|------|
| **多 Agent 架构** | 主 Agent + 专业子 Agent（分析师/开发者/测试员） |
| **数据隔离** | 每个 Agent 独立 memory/ 和 data/ |
| **共享资源** | scripts/libs/skills 所有 Agent 共用 |
| **双向同步** | Markdown ↔ SQLite 自动一致 |
| **语义搜索** | Ollama + bge-m3，理解中文语义 |
| **并发安全** | fcntl 锁 + SQLite WAL 模式 |

---

## 🚀 快速开始

### 方式 1：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-test-agents
cd ~/.openclaw/workspace-test-agents

# 2. 安装依赖（可选）
pip3 install --user jieba  # 中文分词

# 3. 创建目录
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/test-agents

# 4. 注册 OpenClaw agent
openclaw agents add test-agents --workspace "$(pwd)" --non-interactive

# 5. 运行测试
./test-multi-agent.sh
```

### 方式 2：从零创建

```bash
# 1. 创建目录
mkdir -p ~/.openclaw/workspace-test-agents
cd ~/.openclaw/workspace-test-agents

# 2. 注册 OpenClaw agent
openclaw agents add test-agents --workspace "$(pwd)" --non-interactive

# 3. 创建核心文件
cat > AGENTS.md << 'EOF'
# AGENTS.md - test-agents

## 会话流程
1. 会话开始：搜索记忆
2. 会话中：实时记录
3. 会话结束：同步
EOF

# 4. 创建目录
mkdir -p memory agents scripts skills libs
```

---

## 🤖 多 Agent 架构

```
test-agents (主协调) 🦞
├── analyst-agent (需求分析) 🔍
├── developer-agent (代码实现) 💻
└── tester-agent (质量测试) ✅
```

### Agent 列表

| Agent | 角色 | 路径 |
|-------|------|------|
| **test-agents** | coordinator | `memory/` + `data/test-agents/` |
| **analyst-agent** | analyst | `agents/analyst-agent/` |
| **developer-agent** | developer | `agents/developer-agent/` |
| **tester-agent** | tester | `agents/tester-agent/` |

---

## 🎯 使用方式

### 记录事件

```bash
cd ~/.openclaw/workspace-test-agents

# 记录到子 Agent
python3 scripts/session_recorder.py -t event -c '分析完成' --agent analyst-agent

# 记录到主 Agent
python3 scripts/session_recorder.py -t decision -c '采用方案 A' --agent test-agents --sync
```

### 搜索记忆

```bash
# 搜索子 Agent
python3 scripts/unified_search.py '需求分析' --agent analyst-agent --semantic

# 搜索主 Agent
python3 scripts/unified_search.py '昨天的决定' --agent test-agents --semantic
```

### 查看统计

```bash
python3 scripts/memory_stats.py --agent developer-agent
```

---

## 📁 目录结构

```
workspace/
├── 📄 根目录文件
│   ├── AGENTS.md           # 会话规范 ⭐
│   ├── SOUL.md             # Agent 身份
│   ├── MEMORY.md           # 长期记忆
│   ├── USER.md             # 用户信息
│   └── ...
│
├── 🤖 agents/              # ⭐ 子 Agent 数据隔离
│   ├── analyst-agent/
│   │   ├── AGENTS.md
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   ├── config.yaml
│   │   ├── memory/         # 🔒 独立记忆
│   │   └── data/           # 🔒 独立数据库
│   ├── developer-agent/
│   └── tester-agent/
│
├── 🔧 scripts/             # ⭐ 共享脚本
│   ├── session_recorder.py     # 支持 --agent
│   ├── unified_search.py       # 支持 --agent
│   ├── memory_indexer.py
│   └── ...
│
├── 📚 libs/                  # ⭐ 共享库
│   └── memory_hub/
│
├── 🎯 skills/                # ⭐ 共享技能
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
│
├── 📝 memory/                # 主 Agent 记忆
├── 💾 data/                  # 主 Agent 数据
├── 🌐 public/                # 公共知识库
├── ⚙️ config/                # 配置
└── 📂 projects/              # Git 库管理
```

---

## 🔄 多 Agent 协作流程

```
1️⃣  analyst-agent    需求分析
    ↓
2️⃣  developer-agent  方案实现
    ↓
3️⃣  tester-agent     质量测试
    ↓
4️⃣  test-agents      总结沉淀
```

---

## 📊 测试

```bash
# 运行完整测试
./test-multi-agent.sh

# 测试结果
╔════════════════════════════════════════════════════════╗
║     test-agents 多 Agent 完整测试                       ║
╚════════════════════════════════════════════════════════╝

总测试数：26
✅ 通过：26
❌ 失败：0
成功率：100%

🎉 所有测试通过！多 Agent 架构运行正常！
```

---

## 📚 文档

| 文档 | 用途 |
|------|------|
| `docs/ARCHITECTURE_GENERIC_CN.md` | 架构说明（中文） |
| `docs/ARCHITECTURE_GENERIC_EN.md` | Architecture (English) |
| `docs/PROJECT_STRUCTURE_GENERIC_CN.md` | 目录结构（中文） |
| `docs/PROJECT_STRUCTURE_GENERIC_EN.md` | Project Structure (English) |
| `TEST_REPORT_MULTI_AGENT.md` | 测试报告 |

---

## ⚙️ 配置

### config/agents.yaml

```yaml
test-agents:
  name: test-agents
  role: coordinator
  data_path: data/test-agents
  memory_path: memory

analyst-agent:
  name: analyst-agent
  role: analyst
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory

developer-agent:
  name: developer-agent
  role: developer
  
tester-agent:
  name: tester-agent
  role: tester
```

---

## 🔧 依赖

### 必需
- Python 3.10+
- OpenClaw

### 可选
- **jieba** - 中文分词（FTS5 搜索）
- **Ollama** - 语义搜索（bge-m3 模型）

```bash
# 安装 jieba
pip3 install --user jieba

# 安装 Ollama
brew install ollama  # macOS
ollama pull bge-m3   # 中文语义模型
```

---

## 🎯 核心原则

1. **共享代码 + 隔离数据** - scripts/libs/skills 共享，memory/data 隔离
2. **参数化设计** - 所有脚本支持 `--agent` 参数
3. **扁平结构** - projects/ 不分类，直接放
4. **OpenClaw 边界** - `~/.openclaw/agents/` 由 OpenClaw 管理

---

## 📋 Git 库管理

```bash
# 克隆到 projects/
git clone https://github.com/xxx/lib.git projects/

# 查看
ls -1 projects/

# 删除
rm -rf projects/old-lib/
```

**原则：** 扁平结构，不分类，手动清理。

---

## ✅ 测试验证

| 测试项 | 结果 |
|--------|------|
| 环境检查 | ✅ 8/8 |
| 记录事件 | ✅ 4/4 |
| 数据隔离 | ✅ 4/4 |
| 搜索功能 | ✅ 4/4 |
| 统计功能 | ✅ 4/4 |
| 深度验证 | ✅ 2/2 |
| **总计** | **✅ 26/26 (100%)** |

---

## 📝 更新日志

### v1.0 (2026-03-26)
- ✅ 多 Agent 架构实施
- ✅ 3 个子 Agent（analyst/developer/tester）
- ✅ 自动化测试（26 测试 100% 通过）
- ✅ 文档整理（删除 23 个临时文档）
- ✅ 脚本清理（删除 4 个过时脚本）

---

## 🤝 贡献

1. Fork 项目
2. 创建特性分支
3. 提交 PR
4. 通过测试

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🔗 链接

- **GitHub:** https://github.com/luoboask/evo-agents
- **OpenClaw:** https://github.com/openclaw/openclaw
- **文档:** https://docs.openclaw.ai

---

**最后更新：** 2026-03-26  
**维护者：** test-agents 🦞
