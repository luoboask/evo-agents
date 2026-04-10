# knowledge-graph - 知识图谱构建器安装指南

**从记忆中提取实体和关系，构建结构化知识网络。**

> 🔗 实体识别 | 🔗 关系抽取 | 🔗 图谱可视化

---

## ⚡ 一键安装（推荐）

技能已预装，只需验证和测试：

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/libs/knowledge-graph

# 2. 测试运行
python3 -c "from builder import KnowledgeGraph; print('✅ 模块加载成功')"

# 3. 测试构建
python3 builder.py --test 2>/dev/null || python3 -c "
from builder import KnowledgeGraph
kg = KnowledgeGraph()
print('✅ 知识图谱初始化成功')
print(f'实体数：{len(kg.entities)}')
"
```

**就这么简单！** 技能已预装，无需额外依赖。

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 5MB 磁盘空间

### 可选

- ⭕ graphviz（用于图谱可视化）
  ```bash
  brew install graphviz
  pip3 install graphviz
  ```

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/libs/knowledge-graph/

# 应该看到：
# builder.py
```

### Step 2: 检查 Python 依赖

```bash
# Python 版本
python3 --version  # 需要 3.9+

# SQLite3
python3 -c "import sqlite3; print('SQLite3:', sqlite3.version)"

# 测试模块导入
python3 -c "from builder import KnowledgeGraph; print('✅ KnowledgeGraph 加载成功')"
```

### Step 3: 测试运行

```bash
cd ~/.openclaw/workspace/libs/knowledge-graph

# 测试知识图谱构建
python3 -c "
from builder import KnowledgeGraph
kg = KnowledgeGraph()

# 添加测试实体
kg.add_entity('person', 'Alice', {'age': 30})
kg.add_entity('person', 'Bob', {'age': 25})
kg.add_relation('Alice', 'knows', 'Bob', confidence=0.9)

# 保存
kg.save()

print('✅ 测试成功')
print(f'实体数：{len(kg.entities)}')
print(f'关系数：{len(kg.relations)}')
"
```

---

## 🔧 配置说明

### 数据路径配置

编辑 `builder.py` 中的数据路径（如需要）：

```python
# 默认配置
self.workspace = Path("/Users/dhr/.openclaw/workspace")
self.memory_dir = self.workspace / "memory"
self.graph_file = self.memory_dir / "knowledge_graph.json"
```

### 实体类型

支持的实体类型：

| 类型 | 说明 | 示例 |
|------|------|------|
| `person` | 人物 | Alice, Bob |
| `concept` | 概念 | Python, AI |
| `skill` | 技能 | websearch, memory-search |
| `project` | 项目 | OpenClaw |
| `event` | 事件 | 技能创建 |
| `custom` | 自定义 | 任意类型 |

### 关系类型

支持的关系类型：

| 关系 | 说明 | 示例 |
|------|------|------|
| `knows` | 认识 | Alice knows Bob |
| `related_to` | 相关 | Python related_to AI |
| `used_for` | 用于 | Python used_for web_development |
| `created` | 创建 | Alice created Project |
| `custom` | 自定义 | 任意关系 |

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/libs/knowledge-graph/
├── builder.py              # 知识图谱构建器
└── INSTALL.md              # 本文件

数据文件（自动创建）：
~/.openclaw/workspace/memory/
└── knowledge_graph.json    # 知识图谱数据
```

---

## 🎯 使用方法

### Python 调用

```python
from builder import KnowledgeGraph

# 初始化
kg = KnowledgeGraph()

# 添加实体
kg.add_entity("person", "Alice", {"age": 30, "role": "developer"})
kg.add_entity("skill", "websearch", {"type": "search"})
kg.add_entity("project", "OpenClaw", {"status": "active"})

# 添加关系
kg.add_relation("Alice", "created", "websearch", confidence=0.95)
kg.add_relation("websearch", "part_of", "OpenClaw", confidence=0.9)

# 保存
kg.save()

# 查询实体
entity = kg.get_entity("skill:websearch")
print(entity)

# 查询关系
relations = kg.get_relations("Alice")
print(relations)

# 搜索实体
results = kg.search_entities("web")
print(results)
```

### 从记忆自动构建

```python
from builder import KnowledgeGraph

kg = KnowledgeGraph()

# 从记忆文件提取实体和关系
kg.extract_from_memory()

# 保存图谱
kg.save()
```

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 测试模块导入
cd ~/.openclaw/workspace/libs/knowledge-graph
python3 -c "from builder import KnowledgeGraph; print('✅ 加载成功')"

# 2. 测试基本操作
python3 -c "
from builder import KnowledgeGraph
kg = KnowledgeGraph()
kg.add_entity('test', 'TestEntity', {})
kg.save()
print('✅ 基本操作成功')
"

# 3. 检查数据文件
ls -la ~/.openclaw/workspace/memory/knowledge_graph.json
cat ~/.openclaw/workspace/memory/knowledge_graph.json | python3 -m json.tool | head -20
```

---

## 📊 知识图谱示例

```json
{
  "entities": {
    "person:alice": {
      "type": "person",
      "name": "Alice",
      "properties": {"age": 30, "role": "developer"}
    },
    "skill:websearch": {
      "type": "skill",
      "name": "websearch",
      "properties": {"type": "search"}
    }
  },
  "relations": [
    {
      "source": "person:alice",
      "relation": "created",
      "target": "skill:websearch",
      "confidence": 0.95
    }
  ],
  "updated_at": "2026-03-22T01:57:00"
}
```

---

## ❓ 常见问题

### Q: 导入模块失败

**A:** 检查 Python 路径：

```bash
cd ~/.openclaw/workspace/libs/knowledge-graph
python3 -c "import sys; print(sys.path)"
```

### Q: 知识图谱文件不存在

**A:** 首次运行时会自动创建：

```bash
python3 -c "
from builder import KnowledgeGraph
kg = KnowledgeGraph()
kg.save()  # 保存空图谱
"
```

### Q: 如何可视化知识图谱？

**A:** 使用 graphviz 或在线工具：

```bash
# 安装 graphviz
brew install graphviz
pip3 install graphviz

# 导出为 DOT 格式（需要添加导出功能）
```

或使用在线 JSON 查看器查看 `knowledge_graph.json`。

### Q: 如何备份知识图谱？

**A:** 备份数据文件：

```bash
cp ~/.openclaw/workspace/memory/knowledge_graph.json \
   /path/to/backup/knowledge_graph-$(date +%Y%m%d).json
```

### Q: knowledge-graph 和 hybrid-memory 有什么区别？

**A:** 

| 功能 | knowledge-graph | hybrid-memory |
|------|-----------------|---------------|
| 主要用途 | 知识图谱构建 | 混合记忆存储 |
| 数据结构 | 实体 + 关系 | 三层记忆 |
| 查询方式 | 图查询 | 语义搜索 |
| 可视化 | ✅ (需 graphviz) | ❌ |

**建议：** 两者配合使用，knowledge-graph 负责结构化知识，hybrid-memory 负责记忆存储。

### Q: 如何卸载技能？

**A:** 删除技能目录（数据保留）：

```bash
rm -rf ~/.openclaw/workspace/libs/knowledge-graph
```

---

## 📚 相关技能

| 技能 | 说明 |
|------|------|
| **knowledge-graph** | 知识图谱构建 |
| **hybrid-memory** | 混合记忆系统 |
| **memory-search** | 记忆搜索检索 |

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **INSTALL.md** | 本文件 - 安装指南 |
| **builder.py** | 构建器模块（内嵌文档） |

---

## 🆘 获取帮助

遇到问题？

1. 运行测试命令验证安装
2. 检查 Python 模块导入
3. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建独立安装文档
- **2026-03-16**: knowledge-graph 技能创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
