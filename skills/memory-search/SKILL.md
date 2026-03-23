---
name: memory_search
description: 记忆搜索技能，支持关键词和语义搜索
homepage: https://github.com/ai-baby/workspace-ai-baby
metadata:
  emoji: "🧠"
  category: memory
  version: "1.0.0"
  updated_at: "2026-03-23"
---

# 记忆搜索技能

记忆搜索技能提供记忆存储、检索和管理功能。

## 功能

- **关键词搜索** - 快速查找相关记忆
- **语义搜索** - 使用 Ollama 向量搜索（需要本地 Ollama 服务）
- **记忆管理** - 添加、删除、修改记忆
- **统计分析** - 查看记忆数量、类型分布等

## 可用工具

### search(query, top_k=5, semantic=false)

搜索记忆库。

**参数：**
- `query` (string, required): 搜索关键词
- `top_k` (integer, default=5): 返回结果数量
- `semantic` (boolean, default=false): 是否使用语义搜索

**示例：**
```
search(query="RAG 优化", top_k=5, semantic=true)
```

### add(content, type="observation", importance=5.0, tags=[])

添加新记忆。

**参数：**
- `content` (string, required): 记忆内容
- `type` (string, default="observation"): 记忆类型 (observation/reflection/knowledge/goal)
- `importance` (float, default=5.0): 重要性 (1-10)
- `tags` (array, default=[]): 标签列表

**示例：**
```
add(content="今天学习了 RAG 评估系统", type="knowledge", importance=8.0, tags=["RAG", "学习"])
```

### delete(memory_id)

删除记忆。

**参数：**
- `memory_id` (integer, required): 记忆 ID

**示例：**
```
delete(memory_id=123)
```

### stats()

获取记忆统计信息。

**返回：**
- total: 总记忆数
- by_type: 按类型分布
- avg_importance: 平均重要性

**示例：**
```
stats()
```

## 数据存储

记忆数据存储在：
```
~/.openclaw/workspace-ai-baby-config/memory/
├── memory_stream.db      # 记忆流数据库
├── knowledge_base.db     # 知识库
└── vector_db/            # 向量数据库（语义搜索）
```

## 依赖

- **SQLite3** - 数据库（必需）
- **Ollama** - 语义搜索（可选，需要 nomic-embed-text 模型）

## 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "memory-search": {
        "enabled": true,
        "env": {
          "OLLAMA_URL": "http://localhost:11434",
          "EMBEDDING_MODEL": "nomic-embed-text"
        }
      }
    }
  }
}
```

## 使用场景

1. **日常回顾** - 搜索特定日期的记忆
2. **知识检索** - 查找相关知识点
3. **模式识别** - 分析重复出现的主题
4. **统计分析** - 了解记忆分布

## 注意事项

- 语义搜索需要本地 Ollama 服务
- 建议定期备份记忆数据库
- 敏感信息不要存储在记忆中
