# Memory Search - 统一记忆查询技能

> **功能**: 从记忆系统中检索相关信息，支持 4 种查询方式  
> **用途**: 回答基于记忆的问题、查找历史记录、检索上下文  
> **状态**: ✅ Production Ready  

---

## 🚀 使用方法

### 在对话中自动使用

当用户问到与历史、记忆、上下文相关的问题时，自动调用：

```python
from unified_search import UnifiedMemorySearch

search = UnifiedMemorySearch(agent_name='claude-code-agent')

# 搜索记忆
results = search.search("用户之前问过什么？")

# 搜索并生成答案
result = search.search_and_generate("如何配置定时任务？")
print(result['answer'])
```

### 命令行使用

```bash
# 基本查询
python3 skills/memory-search/unified_search.py "关键词" --agent claude-code-agent

# 搜索并生成答案
python3 skills/memory-search/unified_search.py "如何配置定时任务" --generate --agent claude-code-agent

# 指定查询来源
python3 skills/memory-search/unified_search.py "关键词" --no-session --agent claude-code-agent
```

---

## 🔧 集成到对话流程

### 方式 1：在 SOUL.md 中添加规则

在 `SOUL.md` 或 `AGENTS.md` 中添加：

```markdown
## 记忆查询

当用户问到以下类型的问题时，先查询记忆系统：

- "我之前说过什么？"
- "我们之前讨论过什么？"
- "如何配置 XXX？"（可能之前讨论过）
- "XXX 是什么？"（可能之前解释过）

查询方法:
```python
from skills.memory_search.unified_search import UnifiedMemorySearch
search = UnifiedMemorySearch(agent_name='claude-code-agent')
results = search.search(query)
```
```

### 方式 2：创建 Harness Agent 插件

```python
# skills/harness-agent/plugins/memory_search.py

from memory_search.unified_search import UnifiedMemorySearch

class MemorySearchPlugin:
    def __init__(self, agent_name):
        self.search = UnifiedMemorySearch(agent_name)
    
    def search_memory(self, query, generate=False):
        """查询记忆"""
        if generate:
            return self.search.search_and_generate(query)
        return self.search.search(query)
```

### 方式 3：在对话前自动查询

```python
# 在回复用户前
def respond_to_user(user_message):
    # 1. 先查询相关记忆
    search = UnifiedMemorySearch(agent_name='claude-code-agent')
    context = search.search(user_message, top_k=5)
    
    # 2. 构建带上下文的回复
    context_text = build_context(context)
    
    # 3. 调用 LLM 生成回复
    response = llm.generate(user_message, context=context_text)
    
    return response
```

---

## 📊 查询配置

### 默认配置

```json
{
  "top_k": 5,
  "use_shared": true,
  "use_session": true,
  "use_semantic": false,
  "use_kg": true
}
```

### 自定义配置

```python
search.search(
    query="关键词",
    top_k=10,              # 返回数量
    use_shared=True,       # 查询共享记忆
    use_session=True,      # 查询会话记忆
    use_semantic=False,    # 语义搜索（较慢）
    use_kg=True,           # 知识图谱
    record_eval=True       # 记录评估
)
```

---

## 🎯 使用场景

| 场景 | 推荐配置 |
|------|---------|
| 快速查询 | `use_semantic=False` |
| 深度检索 | `use_semantic=True` |
| 只查历史对话 | `use_shared=False, use_session=True` |
| 只查知识 | `use_shared=True, use_session=False, use_kg=True` |
| 生成答案 | `--generate` |

---

## 📝 示例

### 示例 1：查询用户偏好

```python
search = UnifiedMemorySearch(agent_name='claude-code-agent')
results = search.search("用户喜欢什么编程语言？")

# 结果可能包含:
# - 共享记忆中的用户偏好记录
# - 会话记忆中之前的对话
# - 知识图谱中的实体关系
```

### 示例 2：查找项目信息

```python
result = search.search_and_generate("source-deploy 项目是什么？")
print(result['answer'])
print(result['sources'])  # ['shared_memory', 'knowledge_graph']
```

### 示例 3：检索上下文

```python
# 在对话开始时自动检索
context = search.search(user_message, top_k=5)
# 将 context 作为系统提示的一部分
```

---

## 🔗 相关文件

- `unified_search.py` - 统一查询入口
- `shared_memory_search.py` - 共享记忆查询
- `session_memory_search.py` - 会话记忆查询
- `semantic_search.py` - 语义搜索
- `search_with_kg.py` - 知识图谱搜索

---

**最后更新**: 2026-04-10  
**版本**: v2.0 (Unified Search)
