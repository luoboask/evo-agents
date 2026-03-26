# 功能激活指南

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🎯 概述

安装 evo-agents 后，默认已启用基础功能。本指南教你如何手动激活高级功能：

1. **语义搜索模型** - Ollama + 嵌入模型（可选模型）
2. **知识库** - Knowledge Base（知识管理系统）
3. **自进化系统** - 自动学习和进化
4. **RAG 评估** - 检索增强生成评估
5. **定时任务** - 自动执行任务

**新增功能：**
- ✅ 可选择激活哪些功能
- ✅ 语义搜索支持多种模型选择
- ✅ 交互式向导，简单易懂

---

## 📋 前置检查

```bash
# 检查 workspace
cd ~/.openclaw/workspace-my-agent

# 检查基本结构
ls -la scripts/ libs/ skills/
```

---

## 1️⃣ 激活语义搜索模型

### 步骤 1：安装 Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
```bash
# 下载 https://ollama.com/download/windows
```

---

### 步骤 2：启动 Ollama 服务

```bash
# 后台启动
ollama serve

# 或系统服务启动
# macOS: brew services start ollama
# Linux: systemctl start ollama
```

---

### 步骤 3：下载嵌入模型

**根据语言选择模型：**

| 模型 | 大小 | 语言 | 推荐场景 |
|------|------|------|---------|
| **bge-m3** | 1.2GB | 中文最佳 | 中文内容、多语言混合 |
| **nomic-embed-text** | 274MB | 英文最佳 | 英文内容、快速搜索 |
| **mxbai-embed-large** | 670MB | 多语言 | 多语言混合场景 |
| **all-minilm** | 46MB | 英文 | 快速测试、低配置 |

**中文用户推荐：**
```bash
# bge-m3 - 中文最佳，支持多语言
ollama pull bge-m3
```

**英文用户推荐：**
```bash
# nomic-embed-text - 英文最佳，轻量快速
ollama pull nomic-embed-text

# 或 all-minilm - 最小最快（适合测试）
ollama pull all-minilm
```

**多语言用户推荐：**
```bash
# mxbai-embed-large - 多语言支持好
ollama pull mxbai-embed-large
```

**全部下载（自动选择）：**
```bash
# 下载所有常用模型
ollama pull bge-m3
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

---

### 步骤 4：验证安装

```bash
# 检查模型
ollama list

# 应该看到：
# NAME                ID              SIZE      MODIFIED
# bge-m3:latest       790764642607    1.2 GB    now
# nomic-embed-text    0a109f422b47    274 MB    now
```

---

### 步骤 5：测试语义搜索

```bash
# 记录测试记忆
python3 scripts/session_recorder.py -t event -c '测试语义搜索' --agent my-agent

# 语义搜索测试
python3 scripts/unified_search.py '测试' --agent my-agent --semantic

# 查看统计
python3 scripts/memory_stats.py --agent my-agent
```

**预期输出：**
```
🦙 Ollama: ✅ 运行中 (3 模型)
   嵌入模型：✅ bge-m3:latest
🔍 搜索索引
   向量数：6 ✅
```

---

## 2️⃣ 激活知识库系统

### 步骤 1：检查 memory_hub

```bash
cd ~/.openclaw/workspace-my-agent

# 检查 memory_hub 是否存在
ls -la libs/memory_hub/
```

---

### 步骤 2：初始化知识库

```bash
python3 << 'EOF'
from libs.memory_hub import MemoryHub

# 初始化
hub = MemoryHub('my-agent')

# 添加基础知识
hub.knowledge.add(
    title='我的项目介绍',
    content='这是我的个人项目，专注于...',
    category='projects',
    tags=['项目', '介绍']
)

hub.knowledge.add(
    title='工作流程',
    content='我的标准工作流程是...',
    category='workflow',
    tags=['流程', '工作']
)

print('✅ 知识库已激活')
print(f'📊 分类：{len(hub.knowledge.list_categories())} 个')
EOF
```

---

### 步骤 3：验证知识库

```bash
python3 << 'EOF'
from libs.memory_hub import MemoryHub

hub = MemoryHub('my-agent')

# 搜索知识
results = hub.knowledge.search('项目')
print('🔍 搜索结果:')
for r in results[:3]:
    print(f'  - {r.get("title", "Unknown")}')

# 查看分类
print(f'\n📊 分类：{hub.knowledge.list_categories()}')
EOF
```

---

### 步骤 4：使用 RAG 评估

```bash
# 记录一次检索
python3 skills/rag/evaluate.py \
  --record \
  --query "测试查询" \
  --retrieved 5 \
  --latency 100 \
  --feedback positive \
  --agent my-agent

# 生成报告
python3 skills/rag/evaluate.py --report --days 7 --agent my-agent
```

---

## 3️⃣ 激活自进化系统

### 步骤 1：检查自进化系统

```bash
cd skills/self-evolution

# 检查文件
ls -la main.py memory_stream.py fractal_thinking.py nightly_cycle.py
```

---

### 步骤 2：初始化自进化系统

```bash
cd skills/self-evolution

# 查看状态
python3 main.py status

# 初始化记忆流
python3 << 'EOF'
from memory_stream import MemoryStream

ms = MemoryStream()

# 添加初始记忆
ms.add_memory(
    content='自进化系统初始化完成',
    memory_type='observation',
    importance=5.0,
    tags=['初始化', '系统']
)

print('✅ 自进化系统已激活')
print(f'📊 记忆数：{len(ms.get_memories(limit=100))}')
EOF
```

---

### 步骤 3：配置定时任务

```bash
# 每天凌晨 2 点执行夜间循环
openclaw cron add --name "nightly-cycle" --cron "0 2 * * *" \
  --system-event "cd ~/.openclaw/workspace-my-agent/skills/self-evolution && python3 main.py nightly"

# 每周日凌晨 3 点执行分形思考
openclaw cron add --name "fractal-thinking" --cron "0 3 * * 0" \
  --system-event "cd ~/.openclaw/workspace-my-agent/skills/self-evolution && python3 main.py fractal --limit 50"

# 查看 cron 任务
openclaw cron list
```

---

### 步骤 4：测试自进化

```bash
cd skills/self-evolution

# 记录进化事件
python3 main.py evolve -t KNOWLEDGE_GAINED -c "学习了新功能激活方法"

# 查看状态
python3 main.py status
```

---

## 4️⃣ 完整激活脚本

创建 `scripts/activate-features.sh`：

```bash
#!/bin/bash
# activate-features.sh - 一键激活所有高级功能

set -e

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     激活高级功能                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 1. 检查 Ollama
echo "1️⃣  检查 Ollama..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama 已安装"
    ollama list | grep -E "bge-m3|nomic-embed" && echo "   ✅ 嵌入模型已下载" || echo "   ⚠️  需要下载模型：ollama pull bge-m3"
else
    echo "   ❌ Ollama 未安装"
    echo "   安装：brew install ollama (macOS)"
fi

echo ""

# 2. 激活知识库
echo "2️⃣  激活知识库..."
python3 << 'EOF'
from libs.memory_hub import MemoryHub
hub = MemoryHub('my-agent')
try:
    hub.knowledge.add(
        title='功能激活',
        content='已激活所有高级功能',
        category='system',
        tags=['激活', '功能']
    )
    print('   ✅ 知识库已激活')
except Exception as e:
    print(f'   ⚠️  知识库激活失败：{e}')
EOF

echo ""

# 3. 测试语义搜索
echo "3️⃣  测试语义搜索..."
python3 scripts/unified_search.py '测试' --agent my-agent --semantic --limit 1 2>&1 | head -5 && echo "   ✅ 语义搜索正常" || echo "   ⚠️  语义搜索异常"

echo ""

# 4. 检查自进化
echo "4️⃣  检查自进化系统..."
cd skills/self-evolution && python3 main.py status 2>&1 | grep -E "✅|❌" | head -3 && echo "   ✅ 自进化系统正常" || echo "   ⚠️  自进化系统需要初始化"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     ✅ 功能激活完成！                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
```

---

### 使用激活脚本

```bash
cd ~/.openclaw/workspace-my-agent
chmod +x scripts/activate-features.sh
./scripts/activate-features.sh
```

---

## 📊 功能对比

| 功能 | 默认 | 激活后 |
|------|------|--------|
| **基础记忆** | ✅ | ✅ |
| **关键词搜索** | ✅ | ✅ |
| **语义搜索** | ❌ | ✅ (Ollama + bge-m3) |
| **知识库** | ❌ | ✅ (Knowledge Base) |
| **RAG 评估** | ❌ | ✅ (skills/rag/) |
| **自进化** | ❌ | ✅ (skills/self-evolution/) |
| **分形思考** | ❌ | ✅ (每周自动执行) |
| **夜间循环** | ❌ | ✅ (每天自动执行) |

---

## 🎯 推荐配置

### 最小配置（快速启动）

```bash
# 只需安装 Ollama + 下载模型
brew install ollama
ollama pull bge-m3
```

### 标准配置（推荐）

```bash
# 1. 安装 Ollama
brew install ollama

# 2. 下载模型
ollama pull bge-m3

# 3. 激活知识库
python3 scripts/activate-features.sh

# 4. 配置 cron
openclaw cron add --name "nightly" --cron "0 2 * * *" \
  --system-event "cd skills/self-evolution && python3 main.py nightly"
```

### 完整配置（高级用户）

```bash
# 1. 安装 Ollama
brew install ollama

# 2. 下载多个模型
ollama pull bge-m3
ollama pull nomic-embed-text

# 3. 运行激活脚本
python3 scripts/activate-features.sh

# 4. 配置所有 cron 任务
openclaw cron add --name "nightly" --cron "0 2 * * *" \
  --system-event "cd skills/self-evolution && python3 main.py nightly"

openclaw cron add --name "fractal" --cron "0 3 * * 0" \
  --system-event "cd skills/self-evolution && python3 main.py fractal --limit 50"

openclaw cron add --name "index" --cron "0 3 * * *" \
  --system-event "python3 scripts/memory_indexer.py --incremental --embed"
```

---

## 🔗 相关文档

- `workspace-setup.md` - 完整安装指南
- `skills/memory-search/SKILL.md` - 记忆搜索技能
- `skills/rag/README.md` - RAG 评估文档
- `skills/self-evolution/README_FINAL.md` - 自进化系统文档

---

**最后更新：** 2026-03-26  
**维护者：** growth-agents team
