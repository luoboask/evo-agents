# OpenClaw 技能包 - 安装指南

**5 分钟快速安装，从零开始你的智能助手之旅。**

> 本技能包包含：**memory-search**（混合记忆系统）和 **websearch**（智能网页搜索）。

---

## ⚡ 一键安装（推荐）

技能已预装在当前 workspace，无需额外安装！

```bash
# 验证安装
cd /Users/dhr/.openclaw/workspace

# 检查技能文件
ls -la skills/memory-search/
ls -la skills/websearch/
```

**如果技能未安装，手动复制：**

```bash
# 技能已在正确位置，跳过此步
# 如需从其他位置复制：
cp -r /path/to/skills/memory-search ~/.openclaw/workspace/skills/
cp -r /path/to/skills/websearch ~/.openclaw/workspace/skills/
```

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 5MB 磁盘空间

### 可选（推荐）

- ⭕ Ollama（用于 memory-search 的语义搜索）
  - macOS: `brew install ollama`
  - 然后：`ollama pull nomic-embed-text`

---

## 🔧 技能说明

### 1. memory-search - 混合记忆系统

**功能：**
- 🧠 三层记忆架构（工作记忆 + 向量记忆 + 知识图谱）
- 🔍 语义搜索（需要 Ollama）
- 📅 每日回顾自动化
- 📝 自动记录会话上下文

**文件结构：**
```
skills/memory-search/
├── SKILL.md           # 技能定义
├── search.py          # 关键词搜索
├── semantic_search.py # 语义搜索（需要 Ollama）
├── daily_review.py    # 每日回顾
├── auto_record.py     # 自动记录
└── startup.py         # 启动检查
```

**用法：**
```bash
# 关键词搜索
python3 skills/memory-search/search.py "关键词"

# 语义搜索（需要 Ollama）
python3 skills/memory-search/semantic_search.py "自然语言查询"

# 每日回顾
python3 skills/memory-search/daily_review.py
```

---

### 2. websearch - 智能网页搜索

**功能：**
- 🌐 基于 Bing 的网页搜索
- 🔑 无需 API key
- 📄 自动提取网页内容
- 🔄 智能引擎选择

**文件结构：**
```
skills/websearch/
├── SKILL.md    # 技能定义
├── search.py   # 主搜索脚本
└── search.sh   # Shell 快捷方式
```

**用法：**
```bash
# 搜索网页
python3 skills/websearch/search.py "查询内容"

# 或使用 Shell 脚本
./skills/websearch/search.sh "查询内容"
```

---

## ✅ 安装验证

```bash
# 1. 检查 Python 版本
python3 --version

# 2. 检查 SQLite3
python3 -c "import sqlite3; print('SQLite3:', sqlite3.version)"

# 3. 测试 memory-search
python3 skills/memory-search/search.py "测试"

# 4. 测试 websearch
python3 skills/websearch/search.py "测试搜索"

# 5. （可选）测试 Ollama 连接
ollama list 2>/dev/null || echo "Ollama 未安装（可选）"
```

---

## 📁 目录结构

```
~/.openclaw/workspace/
├── skills/
│   ├── memory-search/      # 混合记忆系统
│   │   ├── SKILL.md
│   │   ├── search.py
│   │   ├── semantic_search.py
│   │   └── daily_review.py
│   │
│   └── websearch/          # 网页搜索
│       ├── SKILL.md
│       └── search.py
│
├── memory/                  # 记忆数据（自动创建）
│   ├── YYYY-MM-DD.md       # 每日记忆
│   ├── MEMORY.md           # 长期记忆
│   └── vector_db/          # 向量数据库（可选）
│
├── AGENTS.md               # Agent 配置
├── SOUL.md                 # 人格定义
├── USER.md                 # 用户信息
└── HEARTBEAT.md            # 心跳任务
```

---

## ⚙️ 配置说明

### memory-search 配置

**Ollama 配置（可选，用于语义搜索）：**

```bash
# 安装 Ollama
brew install ollama

# 拉取嵌入模型
ollama pull nomic-embed-text

# 启动 Ollama 服务
ollama serve
```

**编辑 `skills/memory-search/semantic_search.py` 配置：**
```python
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
```

### websearch 配置

无需配置，开箱即用。搜索参数在 `skills/websearch/search.py` 中定义。

---

## 🎯 快速开始

### 1. 创建今日记忆文件

```bash
python3 skills/memory-search/daily_review.py
```

### 2. 搜索记忆

```bash
# 关键词搜索
python3 skills/memory-search/search.py "websearch"

# 语义搜索（需要 Ollama）
python3 skills/memory-search/semantic_search.py "我们安装了什么技能"
```

### 3. 搜索网页

```bash
python3 skills/websearch/search.py "OpenClaw 文档"
```

---

## ❓ 常见问题

### Q: 安装时提示 "Permission denied"

**A:** 检查文件权限：

```bash
chmod +x skills/memory-search/*.py
chmod +x skills/websearch/*.py
```

### Q: 语义搜索失败

**A:** 确保 Ollama 已安装并运行：

```bash
# 检查 Ollama 状态
ollama list

# 如果没有模型，拉取一个
ollama pull nomic-embed-text

# 启动服务
ollama serve
```

或者使用关键词搜索（不需要 Ollama）：
```bash
python3 skills/memory-search/search.py "关键词"
```

### Q: websearch 搜索失败

**A:** 检查网络连接：

```bash
curl -I https://www.bing.com
```

### Q: 如何备份记忆数据？

**A:** 备份 memory 目录：

```bash
# 备份到外部存储
cp -r ~/.openclaw/workspace/memory /path/to/backup/
cp ~/.openclaw/workspace/MEMORY.md /path/to/backup/
```

### Q: 如何卸载技能？

**A:** 删除技能目录（数据保留）：

```bash
# 删除技能代码
rm -rf ~/.openclaw/workspace/skills/memory-search
rm -rf ~/.openclaw/workspace/skills/websearch

# 数据文件（memory/ 目录）不会被删除
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **SKILL.md** | 每个技能的详细定义和用法 |
| **AGENTS.md** | Agent 配置和日常流程 |
| **SOUL.md** | Agent 人格和行为准则 |
| **HEARTBEAT.md** | 心跳任务配置 |
| **MEMORY.md** | 长期记忆文件 |

---

## 🆘 获取帮助

遇到问题？

1. 查看技能的 `SKILL.md` 文件
2. 检查 Python 错误输出
3. 在 OpenClaw 社区提问：https://discord.com/invite/clawd
4. 查看文档：https://docs.openclaw.ai

---

## 📝 更新日志

- **2026-03-21**: 创建综合安装指南
- **2026-03-17**: websearch 技能创建
- **2026-03-16**: memory-search 技能创建

---

**最后更新：** 2026-03-21  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace
