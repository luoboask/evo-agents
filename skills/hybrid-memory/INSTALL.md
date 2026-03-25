# hybrid-memory - 混合记忆系统安装指南

**三层混合记忆系统：工作记忆 + 向量记忆 + 图谱记忆**

> 🧠 L1 工作记忆（当前会话）| 📚 L2 向量记忆（语义检索）| 🔗 L3 图谱记忆（结构化关系）

---

## ⚡ 一键安装（推荐）

技能已预装，只需验证和测试：

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/hybrid-memory

# 2. 测试运行
python3 hybrid_memory.py

# 3. 查看帮助
python3 hybrid_memory.py --help 2>/dev/null || python3 -c "from hybrid_memory import HybridMemory; print('✅ 模块加载成功')"
```

**就这么简单！** 技能已预装，无需额外依赖。

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 10MB 磁盘空间

### 可选（推荐）

- ⭕ Ollama（用于向量嵌入）
  ```bash
  brew install ollama
  ollama pull nomic-embed-text
  ```

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/hybrid-memory/

# 应该看到：
# hybrid_memory.py, integrated_memory.py
```

### Step 2: 检查 Python 依赖

```bash
# Python 版本
python3 --version  # 需要 3.9+

# SQLite3
python3 -c "import sqlite3; print('SQLite3:', sqlite3.version)"

# 测试模块导入
python3 -c "from hybrid_memory import HybridMemory; print('✅ HybridMemory 加载成功')"
python3 -c "from integrated_memory import IntegratedMemory; print('✅ IntegratedMemory 加载成功')"
```

### Step 3: 测试运行

```bash
cd ~/.openclaw/workspace/skills/hybrid-memory

# 测试混合记忆系统
python3 -c "
from hybrid_memory import HybridMemory
mem = HybridMemory()
print('✅ 混合记忆系统初始化成功')
print(f'工作记忆容量：{mem.working_memory.maxlen}')
"
```

---

## 🔧 配置说明

### 三层记忆架构

```python
# L1: 工作记忆 (当前会话，最近 20 条)
self.working_memory = deque(maxlen=20)

# L2: 向量记忆 (使用 Ollama 生成嵌入)
self.vector_cache = {}  # 简单的内存缓存
self.vector_dir = workspace / "memory" / "vector_db"

# L3: 知识图谱 (结构化关系)
self.kg_file = workspace / "memory" / "knowledge_graph.json"
```

### Ollama 配置（可选）

编辑 `hybrid_memory.py` 中的 Ollama 配置：

```python
# Ollama 配置
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
```

### 工作记忆容量

```python
# 修改工作记忆容量（默认 20 条）
self.working_memory = deque(maxlen=50)  # 增加到 50 条
```

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/skills/hybrid-memory/
├── hybrid_memory.py        # 混合记忆主模块
├── integrated_memory.py    # 集成记忆模块
└── INSTALL.md              # 本文件

数据目录（自动创建）：
~/.openclaw/workspace/memory/
├── vector_db/              # 向量数据库
├── knowledge_graph.json    # 知识图谱
├── memory_stream.db        # 记忆流
└── knowledge_base.db       # 知识库
```

---

## 🎯 使用方法

### Python 调用

```python
from hybrid_memory import HybridMemory

# 初始化
mem = HybridMemory()

# 添加到工作记忆
mem.add_to_working("今天学习了 Python", {"type": "learning"})

# 添加到向量记忆
mem.add_to_vector("Python 是一种编程语言", {"tags": ["programming", "python"]})

# 添加到知识图谱
mem.add_entity("concept", "Python", {"type": "programming_language"})
mem.add_relation("Python", "used_for", "web_development")

# 搜索
results = mem.search("Python", limit=5)
```

### 三层记忆说明

| 层级 | 名称 | 用途 | 容量 |
|------|------|------|------|
| L1 | 工作记忆 | 当前会话上下文 | 20 条 |
| L2 | 向量记忆 | 语义搜索和检索 | 无限制 |
| L3 | 图谱记忆 | 结构化知识关系 | 无限制 |

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 测试模块导入
cd ~/.openclaw/workspace/skills/hybrid-memory
python3 -c "from hybrid_memory import HybridMemory; print('✅ 加载成功')"

# 2. 测试初始化
python3 -c "
from hybrid_memory import HybridMemory
mem = HybridMemory()
print('✅ 初始化成功')
print(f'工作记忆：{len(mem.working_memory)} 条')
print(f'知识图谱：{len(mem.knowledge_graph.get(\"entities\", {}))} 个实体')
"

# 3. 检查数据目录
ls -la ~/.openclaw/workspace/memory/
```

---

## ❓ 常见问题

### Q: 导入模块失败

**A:** 检查 Python 路径：

```bash
cd ~/.openclaw/workspace/skills/hybrid-memory
python3 -c "import sys; print(sys.path)"
```

### Q: Ollama 连接失败

**A:** 检查 Ollama 是否运行：

```bash
# 检查状态
ollama list

# 启动服务
ollama serve
```

或禁用 Ollama 使用降级方案（TF-IDF）。

### Q: 知识图谱文件不存在

**A:** 首次运行时会自动创建：

```bash
python3 -c "
from hybrid_memory import HybridMemory
mem = HybridMemory()
mem.save_kg()  # 保存知识图谱
"
```

### Q: 如何备份记忆数据？

**A:** 备份 memory 目录：

```bash
cp -r ~/.openclaw/workspace/memory /path/to/backup/memory-$(date +%Y%m%d)
```

### Q: hybrid-memory 和 memory-search 有什么区别？

**A:** 

| 功能 | hybrid-memory | memory-search |
|------|---------------|---------------|
| 记忆架构 | 三层混合 | 文件 + 数据库 |
| 主要用途 | 记忆存储和管理 | 记忆搜索和检索 |
| 向量支持 | ✅ | ✅ (需要 Ollama) |
| 知识图谱 | ✅ | ❌ |
| 工作记忆 | ✅ | ❌ |

**建议：** 两者配合使用，hybrid-memory 负责存储，memory-search 负责检索。

### Q: 如何卸载技能？

**A:** 删除技能目录（数据保留）：

```bash
rm -rf ~/.openclaw/workspace/skills/hybrid-memory
```

---

## 📚 相关技能

| 技能 | 说明 |
|------|------|
| **hybrid-memory** | 混合记忆存储 |
| **memory-search** | 记忆搜索检索 |
| **knowledge-graph** | 知识图谱构建 |

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **INSTALL.md** | 本文件 - 安装指南 |
| **hybrid_memory.py** | 主模块（内嵌文档） |
| **integrated_memory.py** | 集成模块（内嵌文档） |

---

## 🆘 获取帮助

遇到问题？

1. 运行测试命令验证安装
2. 检查 Python 模块导入
3. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建独立安装文档
- **2026-03-16**: hybrid-memory 技能创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
