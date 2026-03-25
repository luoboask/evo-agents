# OpenClaw 技能包

**智能助手的核心能力集合**

> 🧠 记忆系统 | 🔍 搜索工具 | 🌐 浏览器自动化 | 🤖 自进化系统 | 📊 监控仪表板

---

## 📦 技能列表

### 核心技能

| 技能 | 说明 | 文档 |
|------|------|------|
| **memory-search** | 三层记忆架构，支持关键词和语义搜索 | [INSTALL.md](memory-search/INSTALL.md) |
| **websearch** | 基于 Bing 的网页搜索，无需 API key | [INSTALL.md](websearch/INSTALL.md) |
| **hybrid-memory** | 混合记忆系统（工作 + 向量 + 图谱） | [INSTALL.md](hybrid-memory/INSTALL.md) |
| **knowledge-graph** | 知识图谱构建器 | [INSTALL.md](knowledge-graph/INSTALL.md) |

### 自进化系统

| 技能 | 说明 | 文档 |
|------|------|------|
| **self-evolution-5.0** | 完整自进化系统（记忆流、分形思考、夜间循环） | [INSTALL.md](self-evolution-5.0/INSTALL.md) |
| **self-reflection** | 自我反思系统（交互记录、教训提取） | [INSTALL.md](self-reflection/INSTALL.md) |
| **sandbox-evolution** | 沙箱进化（为 sandbox-agent 提供学习能力） | [INSTALL.md](sandbox-evolution/INSTALL.md) |
| **evolution-workbench** | 进化监控仪表板（实时展示系统状态） | [INSTALL.md](evolution-workbench/INSTALL.md) |

### 浏览器工具

| 技能 | 说明 | 文档 |
|------|------|------|
| **browser-debug** | 浏览器调试（Puppeteer，完整功能） | [INSTALL.md](browser-debug/INSTALL.md) |
| **browser-test** | 浏览器测试（Puppeteer，简化版） | [INSTALL.md](browser-test/INSTALL.md) |

---

## ⚡ 快速开始

### 安装验证

```bash
cd ~/.openclaw/workspace/skills

# 查看所有技能
ls -la

# 运行启动检查
python3 memory-search/startup.py
```

### 快速测试

```bash
# 搜索记忆
python3 memory-search/search.py "websearch"

# 搜索网页
python3 websearch/search.py "OpenClaw 文档"

# 每日回顾
python3 memory-search/daily_review.py

# 自进化系统状态
python3 self-evolution-5.0/main.py status

# 进化仪表板
python3 evolution-workbench/dashboard.py --once

# 浏览器测试
node browser-test/test.js http://example.com
```

---

## 📚 技能文档

### memory-search（混合记忆系统）

| 文档 | 说明 |
|------|------|
| [INSTALL.md](memory-search/INSTALL.md) | 安装和配置指南 |
| [SKILL.md](memory-search/SKILL.md) | 技能定义 |

**功能：**
- 🧠 三层记忆架构（工作记忆 + 向量记忆 + 知识图谱）
- 🔍 关键词搜索 + 语义搜索（需要 Ollama）
- 📅 每日回顾自动化
- 📝 自动记录会话上下文

**常用命令：**
```bash
# 关键词搜索
python3 memory-search/search.py "关键词"

# 语义搜索（需要 Ollama）
python3 memory-search/semantic_search.py "自然语言查询"

# 每日回顾
python3 memory-search/daily_review.py
```

---

### websearch（智能网页搜索）

| 文档 | 说明 |
|------|------|
| [INSTALL.md](websearch/INSTALL.md) | 安装和使用指南 |
| [SKILL.md](websearch/SKILL.md) | 技能定义 |

**功能：**
- 🌐 基于 Bing 的网页搜索
- 🔑 无需 API key
- 📄 自动提取网页内容
- 🔄 智能引擎选择

**常用命令：**
```bash
# 基本搜索
python3 websearch/search.py "查询内容"

# 指定结果数量
python3 websearch/search.py "AI 新闻" --count 5

# 最近一周的内容
python3 websearch/search.py "科技新闻" --freshness week
```

---

## 🔧 系统要求

### 必需

- ✅ Python 3.9+
- ✅ SQLite3
- ✅ Node.js 16+（browser-debug, browser-test）
- ✅ 网络连接（websearch, browser-*）
- ✅ 约 300MB 磁盘空间（所有技能）

### 可选（推荐）

- ⭕ Ollama（用于语义搜索和 Embedding）
  ```bash
  brew install ollama
  ollama pull nomic-embed-text
  ```

- ⭕ Chrome/Chromium（browser-* 技能会自动下载）

---

## 📁 目录结构

```
~/.openclaw/workspace/skills/
├── README.md              # 本文件 - 技能包总览
├── INSTALL.md             # 综合安装指南
│
├── memory-search/         # 混合记忆系统
│   ├── INSTALL.md
│   ├── SKILL.md
│   ├── search.py
│   ├── semantic_search.py
│   ├── daily_review.py
│   └── startup.py
│
├── websearch/             # 网页搜索
│   ├── INSTALL.md
│   ├── SKILL.md
│   └── search.py
│
├── hybrid-memory/         # 混合记忆存储
│   ├── INSTALL.md
│   ├── hybrid_memory.py
│   └── integrated_memory.py
│
├── knowledge-graph/       # 知识图谱
│   ├── INSTALL.md
│   └── builder.py
│
├── self-evolution-5.0/    # 自进化系统
│   ├── INSTALL.md
│   ├── main.py
│   ├── install.py
│   └── (40+ 文件)
│
├── self-reflection/       # 自我反思
│   ├── INSTALL.md
│   ├── reflection.py
│   └── (7 个模块)
│
├── sandbox-evolution/     # 沙箱进化
│   ├── INSTALL.md
│   ├── evolution.py
│   └── (5 个文件)
│
├── evolution-workbench/   # 进化仪表板
│   ├── INSTALL.md
│   ├── dashboard.py
│   └── (HTML 模板)
│
├── browser-debug/         # 浏览器调试
│   ├── INSTALL.md
│   ├── debug.js
│   └── (Node.js 项目)
│
└── browser-test/          # 浏览器测试
    ├── INSTALL.md
    ├── test.js
    └── (Node.js 项目)
```

---

## 🎯 典型使用场景

### 场景 1：研究一个新主题

```bash
# 1. 搜索网页获取最新信息
python3 websearch/search.py "OpenClaw 技能开发"

# 2. 将重要信息记录到记忆
# （在 OpenClaw 会话中自动记录）

# 3. 后续可以通过记忆搜索快速回顾
python3 memory-search/search.py "OpenClaw 技能"
```

### 场景 2：每日回顾

```bash
# 每天早上运行每日回顾
python3 memory-search/daily_review.py

# 查看昨天的活动和今天的计划
```

### 场景 3：查找之前的对话内容

```bash
# 关键词搜索
python3 memory-search/search.py "websearch 安装"

# 语义搜索（更自然）
python3 memory-search/semantic_search.py "我们怎么安装网页搜索的"
```

### 场景 4：系统自我进化

```bash
# 1. 查看系统状态
python3 self-evolution-5.0/main.py status

# 2. 运行分形思考
python3 self-evolution-5.0/main.py fractal --limit 5

# 3. 记录进化事件
python3 self-evolution-5.0/main.py evolve --type KNOWLEDGE_GAINED --content "学习了新技能"

# 4. 查看进化仪表板
python3 evolution-workbench/dashboard.py --watch
```

### 场景 5：网页调试

```bash
# 1. 打开页面并调试
node browser-debug/debug.js open http://localhost:3000

# 2. 查看控制台日志
node browser-debug/debug.js logs http://localhost:3000

# 3. 截图
node browser-debug/debug.js screenshot http://localhost:3000
```

---

## ⚙️ 配置说明

### memory-search 配置

**Ollama 配置（可选）：**

```bash
# 安装 Ollama
brew install ollama

# 拉取嵌入模型
ollama pull nomic-embed-text

# 验证安装
ollama list
```

### websearch 配置

无需配置，开箱即用。

---

## ❓ 常见问题

### Q: 技能在哪里？

**A:** 默认位置：`~/.openclaw/workspace/skills/`

### Q: 语义搜索不工作

**A:** 检查 Ollama 是否安装并运行：

```bash
ollama list
ollama serve  # 如未运行
```

或使用关键词搜索（不需要 Ollama）：
```bash
python3 memory-search/search.py "关键词"
```

### Q: 网页搜索返回空结果

**A:** 检查网络连接：

```bash
curl -I https://www.bing.com
```

### Q: 浏览器技能无法启动

**A:** 检查 Node.js 和 Puppeteer：

```bash
node --version
cd browser-debug && npm install
```

### Q: 自进化系统数据库不存在

**A:** 运行安装脚本：

```bash
cd self-evolution-5.0 && python3 install.py
```

### Q: 如何备份所有数据？

**A:** 备份 memory 目录：

```bash
cp -r ~/.openclaw/workspace/memory /path/to/backup/memory-$(date +%Y%m%d)
```

### Q: 如何添加新技能？

**A:** 参考 OpenClaw 文档：https://docs.openclaw.ai

---

## 🆘 获取帮助

- 📖 **OpenClaw 文档**: https://docs.openclaw.ai
- 💬 **Discord 社区**: https://discord.com/invite/clawd
- 🐛 **GitHub Issues**: https://github.com/openclaw/openclaw

---

## 📝 更新日志

- **2026-03-22**: 为所有 10 个技能创建 INSTALL.md 文档
  - memory-search, websearch, hybrid-memory, knowledge-graph
  - self-evolution-5.0, self-reflection, sandbox-evolution, evolution-workbench
  - browser-debug, browser-test
- **2026-03-17**: websearch 技能创建
- **2026-03-16**: memory-search 技能创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**维护者：** OpenClaw Assistant
