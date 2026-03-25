# memory-search - 混合记忆系统安装指南

**5 分钟快速安装，从零开始你的智能记忆系统。**

> 三层记忆架构：工作记忆 + 向量记忆 + 知识图谱

---

## ⚡ 一键安装（推荐）

技能已预装，只需验证和初始化：

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/memory-search

# 2. 运行启动检查
python3 startup.py

# 3. 创建今日记忆文件
python3 daily_review.py
```

**就这么简单！** 启动脚本会自动：
- ✅ 检查 Python 和 SQLite3
- ✅ 验证 memory 目录
- ✅ 初始化数据库（如需要）
- ✅ 创建今日记忆文件

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 5MB 磁盘空间

### 可选（强烈推荐）

- ⭕ Ollama（用于语义搜索）
  - macOS: `brew install ollama`
  - 然后：`ollama pull nomic-embed-text`

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/memory-search/

# 应该看到：
# SKILL.md, search.py, semantic_search.py, daily_review.py, auto_record.py
```

### Step 2: 检查系统依赖

```bash
# Python 版本
python3 --version  # 需要 3.9+

# SQLite3
python3 -c "import sqlite3; print('SQLite3:', sqlite3.version)"

# Ollama（可选）
ollama list 2>/dev/null || echo "Ollama 未安装（可选）"
```

### Step 3: 运行启动检查

```bash
cd ~/.openclaw/workspace/skills/memory-search
python3 startup.py
```

**输出示例：**
```
========================================
🧠 memory-search 启动检查
========================================

✅ Python 3.11.0 已安装
✅ SQLite3 已安装
✅ memory 目录存在
✅ 数据库初始化完成

========================================
🎉 启动检查完成！
========================================
```

### Step 4: 创建今日记忆文件

```bash
python3 daily_review.py
```

**输出示例：**
```
============================================================
📅 每日回顾 - Daily Review
============================================================

✅ 已创建今日记忆文件：memory/2026-03-22.md

📅 昨天 (2026-03-21) 的记忆摘要：
----------------------------------------
[昨日的记忆内容]
```

---

## 🔧 Ollama 配置（可选但推荐）

### 为什么需要 Ollama？

| 功能 | 无 Ollama | 有 Ollama |
|------|-----------|-----------|
| 关键词搜索 | ✅ 支持 | ✅ 支持 |
| 语义搜索 | ❌ 不支持 | ✅ 支持 |
| 相似度匹配 | TF-IDF | 向量嵌入 |
| 自然语言查询 | ❌ 不支持 | ✅ 支持 |

### 安装 Ollama

```bash
# macOS
brew install ollama

# 拉取嵌入模型
ollama pull nomic-embed-text

# 启动服务（通常自动启动）
ollama serve
```

### 验证 Ollama 连接

```bash
# 检查模型
ollama list

# 测试嵌入
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "测试文本"
}'
```

### 配置语义搜索

编辑 `semantic_search.py`（如需要）：

```python
# 默认配置通常无需修改
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
```

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/
├── skills/
│   └── memory-search/      # 技能代码
│       ├── SKILL.md        # 技能定义
│       ├── INSTALL.md      # 本文件
│       ├── search.py       # 关键词搜索
│       ├── semantic_search.py  # 语义搜索
│       ├── daily_review.py # 每日回顾
│       ├── auto_record.py  # 自动记录
│       └── startup.py      # 启动检查
│
└── memory/                  # 记忆数据目录
    ├── YYYY-MM-DD.md       # 每日记忆文件
    ├── MEMORY.md           # 长期记忆
    ├── knowledge_base.db   # 知识库数据库
    ├── memory_stream.db    # 记忆流数据库
    ├── ai-baby_*.db        # AI Baby 专用数据库
    └── vector_db/          # 向量数据库（Ollama）
```

**重要：** 代码和数据是分离的。升级技能时，数据不会丢失。

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 关键词搜索
python3 search.py "测试"

# 2. 语义搜索（需要 Ollama）
python3 semantic_search.py "我们昨天做了什么"

# 3. 每日回顾
python3 daily_review.py

# 4. 查看记忆文件
ls -la ../memory/*.md
```

---

## 🎯 常用命令

```bash
# 关键词搜索
python3 search.py "关键词"

# 语义搜索（自然语言）
python3 semantic_search.py "我们安装了什么技能"

# 每日回顾（创建今日文件 + 显示昨日摘要）
python3 daily_review.py

# 搜索特定数量结果
python3 search.py "关键词" --limit 10

# 查看记忆文件列表
ls -la ../memory/
```

---

## ❓ 常见问题

### Q: 安装时提示 "Permission denied"

**A:** 检查文件权限：

```bash
chmod +x ~/.openclaw/workspace/skills/memory-search/*.py
chmod 755 ~/.openclaw/workspace/memory
```

### Q: 语义搜索失败，提示连接错误

**A:** 检查 Ollama 是否运行：

```bash
# 检查状态
ollama list

# 如果没有模型，拉取一个
ollama pull nomic-embed-text

# 启动服务
ollama serve
```

或者使用关键词搜索（不需要 Ollama）：
```bash
python3 search.py "关键词"
```

### Q: 记忆文件在哪里？

**A:** 默认位置：

```bash
ls -la ~/.openclaw/workspace/memory/
cat ~/.openclaw/workspace/memory/2026-03-22.md
```

### Q: 如何备份记忆数据？

**A:** 备份 memory 目录：

```bash
# 备份到外部存储
cp -r ~/.openclaw/workspace/memory /path/to/backup/memory-$(date +%Y%m%d)
```

### Q: 如何卸载技能？

**A:** 删除技能目录（数据保留）：

```bash
# 删除技能代码
rm -rf ~/.openclaw/workspace/skills/memory-search

# 数据文件（memory/ 目录）不会被删除，手动删除需谨慎
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **SKILL.md** | 技能定义和用法详解 |
| **INSTALL.md** | 本文件 - 安装指南 |
| **search.py** | 关键词搜索脚本（内嵌帮助） |
| **semantic_search.py** | 语义搜索脚本（内嵌帮助） |
| **daily_review.py** | 每日回顾脚本（内嵌帮助） |

---

## 🆘 获取帮助

遇到问题？

1. 运行 `python3 startup.py` 检查系统状态
2. 查看技能的 `SKILL.md` 文件
3. 检查 Python 错误输出
4. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-21**: 创建独立安装文档
- **2026-03-19**: 添加 Ollama 语义搜索支持
- **2026-03-16**: 初始版本创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
