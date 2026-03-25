# Workspace Setup

统一记忆系统的安装和配置指南。

## 快速开始（最小安装）

只需要 Python 3.10+ 和标准库，不需要任何额外依赖。

```bash
export WORKSPACE="/path/to/your/workspace"
export AGENT="your-agent-name"

cd "$WORKSPACE"

# 创建目录结构
mkdir -p memory/weekly memory/monthly memory/archive data/index scripts/bridge

# 测试基本功能
python3 scripts/session_recorder.py -t event -c '系统初始化完成'
python3 scripts/unified_search.py '初始化' --agent "$AGENT"
python3 scripts/memory_stats.py --agent "$AGENT"
python3 scripts/health_check.py --agent "$AGENT"
```

这就够了。关键词搜索（grep）开箱即用，不需要任何额外安装。

## 可选功能

### 1. FTS5 全文搜索（推荐）

需要 jieba 中文分词库。安装后搜索速度和准确度显著提升。

```bash
# 安装 jieba
pip3 install jieba
# 如果报 externally-managed-environment 错误：
pip3 install --user --break-system-packages jieba

# 验证
python3 -c "import jieba; print('jieba OK')"

# 建立 FTS5 索引
python3 scripts/memory_indexer.py --full
```

**不安装 jieba 会怎样？**
- FTS5 索引仍然可以建立（用空格分词），但中文搜索精度较低
- 系统自动 fallback 到 grep 搜索，功能不受影响

### 2. 语义搜索（可选，中文效果好）

需要 Ollama + 嵌入模型。安装后支持自然语言提问（如"昨天做了什么决定"）。

```bash
# 安装 Ollama（macOS）
brew install ollama
# 或访问 https://ollama.com/download

# 启动 Ollama
ollama serve

# 下载嵌入模型（推荐 bge-m3，中文效果好）
ollama pull bge-m3
# 或用更小的 nomic-embed-text（274MB vs 1.2GB）
# ollama pull nomic-embed-text

# 建立语义索引
python3 scripts/memory_indexer.py --full --embed

# 测试语义搜索
python3 scripts/unified_search.py '自然语言提问' --semantic
```

**不安装 Ollama 会怎样？**
- `--semantic` 参数会提示不可用，自动退回 FTS5 或 grep
- 其他所有功能正常工作
- 索引命令的 `--embed` 参数会被忽略

**切换嵌入模型：**
修改 `scripts/memory_indexer.py` 和 `scripts/unified_search.py` 中的 `EMBED_MODEL` 变量：
```python
EMBED_MODEL = "bge-m3"           # 推荐，中文好，1.2GB
# EMBED_MODEL = "nomic-embed-text"  # 更小，英文好，274MB
```

### 3. 模型内存需求

| 模型 | 磁盘 | 运行内存 | 中文 | 英文 |
|------|------|---------|------|------|
| bge-m3 | 1.2 GB | ~1.5 GB | ✅ 好 | ✅ 好 |
| nomic-embed-text | 274 MB | ~350 MB | ⚠️ 一般 | ✅ 好 |

## 功能降级矩阵

| 依赖 | 安装了 | 没安装 |
|------|--------|--------|
| **jieba** | FTS5 中文分词搜索 | 退回 grep（能用但慢） |
| **Ollama + 模型** | 语义搜索（自然语言） | 退回 FTS5 或 grep |
| **两者都没有** | grep 文件搜索 + SQLite LIKE | 基本功能完整可用 |

## 脚本说明

### 核心脚本

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `scripts/session_recorder.py` | 记录事件到 daily markdown | 无 |
| `scripts/unified_search.py` | 统一搜索 | 可选 jieba + Ollama |
| `scripts/memory_indexer.py` | 建立搜索索引 | 可选 jieba + Ollama |
| `scripts/memory_compressor.py` | 日→周→月压缩 | 无 |
| `scripts/memory_stats.py` | 系统统计 | 无 |
| `scripts/health_check.py` | 健康检查 + 自动修复 | 无 |
| `scripts/lock_utils.py` | 并发锁工具 | 无 |

### 桥接脚本（双系统互通）

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `scripts/bridge/bridge_sync.py` | 一键双向同步 | 无 |
| `scripts/bridge/bridge_to_markdown.py` | SQLite → markdown | 无 |
| `scripts/bridge/bridge_to_knowledge.py` | markdown → SQLite | 无 |

## 目录结构

```
workspace/
├── MEMORY.md                    # 长期核心记忆
├── memory/
│   ├── YYYY-MM-DD.md            # 每日记录
│   ├── weekly/YYYY-WXX.md       # 周摘要
│   ├── monthly/YYYY-MM.md       # 月摘要
│   └── archive/                 # 归档的旧日志
├── data/
│   ├── <agent>/memory/
│   │   └── memory_stream.db     # 知识系统 SQLite
│   └── index/
│       └── memory_index.db      # FTS5 + 向量索引
├── scripts/
│   ├── session_recorder.py
│   ├── unified_search.py
│   ├── memory_indexer.py
│   ├── memory_compressor.py
│   ├── memory_stats.py
│   ├── health_check.py
│   ├── lock_utils.py
│   └── bridge/
│       ├── bridge_sync.py
│       ├── bridge_to_markdown.py
│       └── bridge_to_knowledge.py
├── libs/memory_hub/             # 知识记忆核心库（原有）
└── skills/                      # 技能模块（原有）
```

## 推荐的 cron 定时任务

通过 OpenClaw cron 配置：

```bash
# 每天凌晨：增量索引（如果有 Ollama 则含向量）
openclaw cron add --name "daily-index" --cron "0 3 * * *" --tz "Asia/Shanghai" \
  --system-event "cd $WORKSPACE && python3 scripts/memory_indexer.py --incremental --embed 2>&1"

# 每 6 小时：双向同步
openclaw cron add --name "bridge-sync" --every "6h" \
  --system-event "cd $WORKSPACE && python3 scripts/bridge/bridge_sync.py --agent $AGENT 2>&1"

# 每周一：周摘要压缩
openclaw cron add --name "weekly-compress" --cron "0 4 * * 1" --tz "Asia/Shanghai" \
  --system-event "cd $WORKSPACE && python3 scripts/memory_compressor.py --weekly 2>&1"

# 每月 1 号：月摘要 + 归档
openclaw cron add --name "monthly-compress" --cron "0 5 1 * *" --tz "Asia/Shanghai" \
  --system-event "cd $WORKSPACE && python3 scripts/memory_compressor.py --monthly --archive 2>&1"
```

## 验证安装

```bash
cd "$WORKSPACE"

# 1. 基本功能
python3 scripts/session_recorder.py -t event -c '安装验证'
python3 scripts/memory_stats.py --agent "$AGENT"
python3 scripts/health_check.py --agent "$AGENT"

# 2. 搜索（自动选择最佳可用方式）
python3 scripts/unified_search.py '验证' --agent "$AGENT"

# 3. 语义搜索（如果安装了 Ollama）
python3 scripts/unified_search.py '安装是否成功' --semantic

# 4. 双向同步
python3 scripts/bridge/bridge_sync.py --agent "$AGENT"
```

全部通过即安装成功。
