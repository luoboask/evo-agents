# evo-agents Workspace 安装指南

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🎯 概述

evo-agents 是一个完整的 OpenClaw Workspace 模板，包含：
- Agent 生命周期文件（AGENTS.md, SOUL.md, MEMORY.md, USER.md）
- 多个集成技能（self-evolution, rag, websearch, memory-search）
- 记忆管理系统（双向同步 + 语义搜索）
- 多 Agent 协作支持

---

## 🚀 安装方式

### 方式 1：一键安装（推荐）

```bash
# 安装默认名称 'my-agent'
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash

# 或指定自己的 agent 名称
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s your-agent-name
```

**示例：**
```bash
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s growth-assistant
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/init-agent.sh | bash -s demo-agent
```

**这将：**
1. 克隆模板到 `~/.openclaw/workspace-{agent-name}`
2. 创建目录结构
3. 注册 OpenClaw agent（`openclaw agents add`）
4. 运行快速测试

---

### 方式 2：手动安装

```bash
# 1. 克隆模板
git clone --depth 1 https://github.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent

# 2. 创建目录结构
cd ~/.openclaw/workspace-my-agent
mkdir -p memory/weekly memory/monthly memory/archive
mkdir -p data/index data/{agent-name}

# 3. 注册 OpenClaw agent
openclaw agents add my-agent --workspace "$(pwd)" --non-interactive

# 4. 测试
python3 scripts/session_recorder.py -t event -c 'Hello world'
python3 scripts/unified_search.py 'hello' --agent my-agent --semantic
```

---

## 📁 完整目录结构

```
workspace/
├── 📄 根目录文件
│   ├── AGENTS.md              # 会话行为规范 ⭐
│   ├── SOUL.md                # Agent 身份
│   ├── MEMORY.md              # 长期记忆
│   ├── USER.md                # 用户信息
│   ├── IDENTITY.md            # 身份标识
│   ├── TOOLS.md               # 工具配置
│   └── HEARTBEAT.md           # 心跳检查
│
├── 🔧 scripts/                # 共享脚本
│   ├── session_recorder.py        # 记录事件
│   ├── unified_search.py          # 统一搜索
│   ├── memory_indexer.py          # 构建索引
│   ├── memory_compressor.py       # 压缩沉淀
│   ├── memory_stats.py            # 系统统计
│   ├── health_check.py            # 健康检查
│   └── bridge/                    # 双向同步
│       ├── bridge_sync.py
│       ├── bridge_to_markdown.py
│       └── bridge_to_knowledge.py
│
├── 📚 libs/                   # 共享库
│   └── memory_hub/              # 记忆核心库
│
├── 🎯 skills/                 # 共享技能
│   ├── memory-search/           # 记忆搜索
│   ├── rag/                     # RAG 评估
│   ├── self-evolution/          # 自进化系统
│   └── websearch/               # 网页搜索
│
├── 📝 memory/                 # 记忆目录
│   ├── YYYY-MM-DD.md            # 每日记录
│   ├── weekly/                  # 周摘要
│   ├── monthly/                 # 月摘要
│   └── archive/                 # 归档
│
├── 💾 data/                   # 数据目录
│   ├── <agent-name>/            # Agent 数据
│   │   └── memory/              # SQLite 数据库
│   └── index/                   # 搜索索引
│
├── 🤖 agents/                 # 多 Agent 目录（可选）
│   └── <sub-agent-name>/        # 子 Agent
│       ├── AGENTS.md
│       ├── SOUL.md
│       ├── MEMORY.md
│       ├── config.yaml
│       ├── memory/
│       └── data/
│
├── 🌐 public/                 # 公共知识库
├── 📂 projects/               # Git 库管理
├── ⚙️ config/                 # 配置
│   └── agents.yaml              # 多 Agent 配置
└── 📖 docs/                   # 文档
    ├── ARCHITECTURE_GENERIC_CN.md
    ├── ARCHITECTURE_GENERIC_EN.md
    ├── PROJECT_STRUCTURE_GENERIC_CN.md
    └── PROJECT_STRUCTURE_GENERIC_EN.md
```

---

## 🤖 多 Agent 配置（可选）

evo-agents 支持多 Agent 协作，可以创建多个专业子 Agent。

### 创建子 Agent

```bash
cd ~/.openclaw/workspace-my-agent

# 1. 创建子 Agent 目录
mkdir -p agents/analyst-agent/{memory,data}
mkdir -p agents/developer-agent/{memory,data}
mkdir -p agents/tester-agent/{memory,data}

# 2. 创建配置文件
cat > agents/analyst-agent/AGENTS.md << 'EOF'
# AGENTS.md - analyst-agent

**角色：** 需求分析师  
**职责：** 分析需求、设计方案

## 工作流程
1. 接收任务
2. 分析需求
3. 输出方案
EOF

cat > agents/analyst-agent/SOUL.md << 'EOF'
# SOUL.md - analyst-agent

**你是谁：** 需求分析师  
**emoji：** 🔍

## 个性
- 善于分析和拆解问题
- 注重细节和背景理解
EOF

cat > agents/analyst-agent/MEMORY.md << 'EOF'
# MEMORY.md - analyst-agent

## 长期记忆
_重要的人、事、偏好、决定_

## 用户
- 名称：待填写
- 时区：Asia/Shanghai
EOF

cat > agents/analyst-agent/config.yaml << 'EOF'
agent:
  name: analyst-agent
  role: analyst
  description: "需求分析师"
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory
EOF

# 3. 注册到 OpenClaw
openclaw agents add analyst-agent --workspace "$(pwd)/agents/analyst-agent" --non-interactive
openclaw agents add developer-agent --workspace "$(pwd)/agents/developer-agent" --non-interactive
openclaw agents add tester-agent --workspace "$(pwd)/agents/tester-agent" --non-interactive

# 4. 更新 config/agents.yaml
# 编辑 config/agents.yaml 添加子 Agent 配置
```

### 多 Agent 示例

```
my-agent (主协调) 🦞
├── analyst-agent (需求分析) 🔍
├── developer-agent (代码实现) 💻
└── tester-agent (质量测试) ✅
```

### 使用子 Agent

```bash
# 记录事件到子 Agent
python3 scripts/session_recorder.py -t event -c '内容' --agent analyst-agent

# 搜索子 Agent 记忆
python3 scripts/unified_search.py '关键词' --agent developer-agent --semantic

# 查看子 Agent 统计
python3 scripts/memory_stats.py --agent tester-agent
```

---

### 方式 3：一键创建多 Agent 体系（推荐）⭐

创建包含 3 个专业子 Agent 的完整多 Agent 体系：

```bash
# 创建并执行安装脚本
cat > /tmp/setup-multi-agent.sh << 'SCRIPT'
#!/bin/bash
set -e

WORKSPACE="$1"
if [ -z "$WORKSPACE" ]; then
    echo "用法：./setup-multi-agent.sh <workspace-path>"
    exit 1
fi

cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     创建多 Agent 体系                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 创建子 Agent 目录
for agent in analyst-agent developer-agent tester-agent; do
    echo "📁 创建 $agent..."
    mkdir -p "agents/$agent/{memory,data}"
    
    # 创建 AGENTS.md
    cat > "agents/$agent/AGENTS.md" << EOF
# AGENTS.md - $agent

**角色：** ${agent%-agent}
**职责：** 专业任务处理

## 工作流程
1. 接收任务
2. 处理任务
3. 输出结果
EOF

    # 创建 SOUL.md
    case $agent in
        analyst-agent)
            emoji="🔍"
            desc="需求分析师"
            ;;
        developer-agent)
            emoji="💻"
            desc="代码开发者"
            ;;
        tester-agent)
            emoji="✅"
            desc="质量测试员"
            ;;
    esac
    
    cat > "agents/$agent/SOUL.md" << EOF
# SOUL.md - $agent

**你是谁：** $desc
**emoji：** $emoji

## 个性
- 专业、认真、负责
- 善于思考和解决问题
EOF

    # 创建 MEMORY.md
    cat > "agents/$agent/MEMORY.md" << EOF
# MEMORY.md - $agent

## 长期记忆
_重要的人、事、偏好、决定_

## 用户
- 名称：待填写
- 时区：Asia/Shanghai
EOF

    # 创建 config.yaml
    cat > "agents/$agent/config.yaml" << EOF
agent:
  name: $agent
  role: ${agent%-agent}
  description: "$desc"
  data_path: agents/$agent/data
  memory_path: agents/$agent/memory
EOF

    echo "   ✅ $agent 创建完成"
done

# 更新 config/agents.yaml
AGENT_NAME=$(basename "$WORKSPACE" | sed 's/workspace-//')
cat > config/agents.yaml << EOF
# Multi-Agent Configuration

# Main agent
$AGENT_NAME:
  name: $AGENT_NAME
  role: coordinator
  data_path: data/$AGENT_NAME
  memory_path: memory

# Sub-agents
analyst-agent:
  name: analyst-agent
  role: analyst
  data_path: agents/analyst-agent/data
  memory_path: agents/analyst-agent/memory

developer-agent:
  name: developer-agent
  role: developer
  data_path: agents/developer-agent/data
  memory_path: agents/developer-agent/memory

tester-agent:
  name: tester-agent
  role: tester
  data_path: agents/tester-agent/data
  memory_path: agents/tester-agent/memory
EOF

# 注册子 Agent 到 OpenClaw
echo ""
echo "📝 注册 OpenClaw 子 Agent..."
for agent in analyst-agent developer-agent tester-agent; do
    openclaw agents add "$agent" --workspace "$WORKSPACE/agents/$agent" --non-interactive 2>/dev/null && \
        echo "   ✅ $agent 已注册到 OpenClaw" || \
        echo "   ⚠️  $agent 可能已存在"
done

echo ""
echo "✅ 多 Agent 体系创建完成！"
echo ""
echo "📊 Agent 列表:"
echo "   • $AGENT_NAME (主协调)"
echo "   • analyst-agent (需求分析 🔍) - OpenClaw 已注册"
echo "   • developer-agent (代码实现 💻) - OpenClaw 已注册"
echo "   • tester-agent (质量测试 ✅) - OpenClaw 已注册"
echo ""
echo "🎯 使用示例:"
echo "   # 使用 OpenClaw 直接调用子 Agent"
echo "   openclaw agent --agent analyst-agent --message '分析这个需求...'"
echo "   openclaw agent --agent developer-agent --message '实现这个功能...'"
echo ""
echo "   # 或使用脚本"
echo "   python3 scripts/session_recorder.py -t event -c '内容' --agent analyst-agent"
echo "   python3 scripts/unified_search.py '关键词' --agent developer-agent --semantic"
SCRIPT

chmod +x /tmp/setup-multi-agent.sh
bash /tmp/setup-multi-agent.sh "$(pwd)"
```

---

## ❌ 不适用于 SubAgent/Skill

本仓库是**完整的 Workspace 模板**，包含：
- Agent 生命周期文件（AGENTS.md, SOUL.md, MEMORY.md, USER.md）
- 多个集成技能（self-evolution, rag, websearch）
- 完整的运行时目录结构

**对于 SubAgent 或仅 Skill 安装**，使用轻量级 skill 仓库：

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/luoboask/unified-memory-skill.git unified-memory
```

查看 [unified-memory-skill](https://github.com/luoboask/unified-memory-skill) 了解 SubAgent/Skill 用法。

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| **双向桥接** | Markdown ↔ SQLite 自动同步，数据一致 |
| **语义搜索** | 自然语言查询，bge-m3 理解语义（本地 Ollama，无需 API key） |
| **FTS5 中文** | jieba 分词，精确中文关键词匹配 |
| **智能评分** | 自动重要性（决策 8+，学习 6+，事件 5+） |
| **自动压缩** | 日→周→月→长期，防止数据膨胀 |
| **并发安全** | fcntl 锁 + SQLite WAL，多会话无数据丢失 |

---

## 🛠️ 快速开始

### 最小安装（零依赖）

只需 Python 3.10+，开箱即用。

```bash
# 记录事件
python3 scripts/session_recorder.py -t event -c '今天完成了重要工作'

# 搜索（自动选择最佳方法）
python3 scripts/unified_search.py '重要工作' --agent my-agent
```

### 推荐增强（可选）

**1. FTS5 中文分词（推荐）**

```bash
pip3 install jieba  # 或 pip3 install --user --break-system-packages jieba
python3 scripts/memory_indexer.py --full
```

**2. 语义搜索（推荐，中文效果好）**

```bash
# 安装 Ollama
brew install ollama  # macOS
# 或访问 https://ollama.com/download

# 启动并下载模型
ollama serve
ollama pull bge-m3  # 1.2GB，中文效果好
# 或 ollama pull nomic-embed-text  # 274MB，英文效果好

# 构建语义索引
python3 scripts/memory_indexer.py --full --embed

# 语义搜索
python3 scripts/unified_search.py '我昨天做了什么' --semantic
```

---

## 💬 会话中的记忆流

**AGENTS.md 包含完整的规范**，每次会话自动遵循：

### 会话开始：搜索记忆

当用户提到之前的事情 → 先搜索，再回答：
```bash
python3 scripts/unified_search.py '相关关键词' --agent my-agent --semantic
```

### 会话中：实时记录

发现重要信息 → 立即记录：
```bash
python3 scripts/session_recorder.py -t decision -c '用户决定使用 X 方案' --sync
python3 scripts/session_recorder.py -t learning -c '学习了 Y 知识点' --sync
python3 scripts/session_recorder.py -t event -c '发生了 Z 事件' --sync
```

### 会话结束：同步

如果记录了内容 → 自动同步（`--sync` 后台运行）

---

## 🔧 常用命令

| 命令 | 说明 |
|------|------|
| `session_recorder.py -t event -c '...'` | 记录事件 |
| `session_recorder.py -t decision -c '...' --sync` | 记录决策并自动同步 |
| `unified_search.py '关键词'` | 关键词搜索 |
| `unified_search.py '问题' --semantic` | 语义搜索 |
| `bridge_sync.py --agent my-agent` | 双向同步 |
| `memory_indexer.py --incremental --embed` | 增量索引 + 向量 |
| `memory_compressor.py --weekly` | 生成周摘要 |
| `memory_stats.py --agent my-agent` | 系统统计 |
| `health_check.py --agent my-agent` | 健康检查 |

---

## ⏰ 定时任务（推荐）

```bash
# 每天凌晨 3 点：增量索引
openclaw cron add --name "daily-index" --cron "0 3 * * *" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_indexer.py --incremental --embed"

# 每 6 小时：双向同步
openclaw cron add --name "bridge-sync" --every "6h" \
  --system-event "cd /path/to/workspace && python3 scripts/bridge/bridge_sync.py --agent my-agent"

# 周一凌晨 4 点：周摘要
openclaw cron add --name "weekly-compress" --cron "0 4 * * 1" \
  --system-event "cd /path/to/workspace && python3 scripts/memory_compressor.py --weekly"
```

---

## 🔄 优雅降级

| 依赖 | 已安装 | 未安装 |
|------|--------|--------|
| **jieba** | FTS5 中文分词 | 降级到 grep（慢但可用） |
| **Ollama + 模型** | 语义搜索（自然语言） | 降级到 FTS5 或 grep |
| **都没有** | grep + SQLite LIKE | 核心功能完全可用 |

**最小安装零依赖** — 只需 Python 3.10+。

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

## 📚 文档

- `README.md` / `README.zh-CN.md` — 项目说明
- `workspace-setup.md` — 本文档（完整安装指南）
- `AGENTS.md` — 会话记忆流规范
- `docs/ARCHITECTURE_GENERIC_CN.md` — 架构设计
- `docs/PROJECT_STRUCTURE_GENERIC_CN.md` — 目录结构

---

## 📄 许可证

MIT
