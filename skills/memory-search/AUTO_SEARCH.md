# memory-search 技能 - 自动增强版

**每次回复前自动检索相关记忆**

---

## 🔧 修改 SKILL.md

将以下内容添加到 `skills/memory-search/SKILL.md`：

```markdown
## 🤖 自动触发规则

**在以下情况自动检索记忆：**

1. **用户问到历史相关问题**
   - "我之前说过什么？"
   - "我们之前讨论过什么？"
   - "还记得 XXX 吗？"
   - "之前那个 XXX 怎么弄的？"

2. **用户问到配置/使用问题**（可能之前讨论过）
   - "如何配置 XXX？"
   - "XXX 怎么用？"
   - "XXX 是什么？"

3. **用户提到项目/任务**
   - "XXX 项目进行到哪了？"
   - "XXX 任务完成没？"

**检索方法：**

```python
from skills.memory_search.unified_search import UnifiedMemorySearch

search = UnifiedMemorySearch(agent_name='demo51-agent')
results = search.search(user_message)

# 如果有相关记忆，在回复中引用
if results:
    context = "\n".join([r['content'][:200] for r in results[:3]])
    # 基于 context 回复用户
    response = f"根据之前的记录，{context}...\n我的建议是..."
```

**注意事项：**

- ✅ **按需查询**：不是每次对话都查询
- ✅ **引用来源**：回复时说明"根据记忆..."
- ✅ **避免重复**：如果记忆中有答案，不要重复解释
```

---

## 🚀 自动检索实现

### 修改 `skills/memory-search/search.py`

```python
#!/usr/bin/env python3
"""
记忆搜索 - 自动增强版

在回复前自动检索相关记忆
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))

from memory_hub import MemoryHub


class AutoMemorySearch:
    """自动记忆检索"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.memory = MemoryHub(agent_name=agent_name)
    
    def should_search(self, user_message):
        """判断是否需要检索记忆"""
        
        # 关键词触发
        trigger_keywords = [
            '之前', '以前', '上次', '记得', '历史',
            '配置', '怎么', '如何', '什么', '哪里',
            '项目', '任务', '进行', '完成'
        ]
        
        for keyword in trigger_keywords:
            if keyword in user_message:
                return True
        
        return False
    
    def search_and_respond(self, user_message, original_response):
        """
        检索记忆并增强回复
        
        Args:
            user_message: 用户消息
            original_response: 原始回复（没有检索记忆）
        
        Returns:
            增强后的回复
        """
        
        # 判断是否需要检索
        if not self.should_search(user_message):
            return original_response
        
        # 检索记忆
        memories = self.memory.search(user_message, top_k=3, semantic=True)
        
        if not memories:
            return original_response
        
        # 构建增强回复
        enhanced = original_response + "\n\n📚 **根据历史记录：**\n"
        
        for i, m in enumerate(memories, 1):
            content = m.get('content', '')
            timestamp = m.get('metadata', {}).get('timestamp', '')
            
            # 清理格式
            content = content.replace('===', '').replace('---', '').strip()
            if len(content) > 150:
                content = content[:150] + '...'
            
            enhanced += f"\n{i}. {content}"
            if timestamp:
                enhanced += f" ({timestamp[:10]})"
        
        return enhanced


# 使用示例
if __name__ == '__main__':
    searcher = AutoMemorySearch()
    
    # 模拟用户消息和原始回复
    user_message = "之前那个 Python 优化怎么弄的？"
    original_response = "可以使用异步编程和缓存来提升性能。"
    
    # 增强回复
    enhanced = searcher.search_and_respond(user_message, original_response)
    print(enhanced)
```

---

## 📋 Cron 配置（后台自动进化）

```bash
cd /Users/dhr/.openclaw/workspace-demo51-agent

# 每小时自动分形思考
openclaw cron add --cron "0 * * * *" \
  --agent demo51-agent \
  --message "python3 skills/self-evolution/fractal_thinking.py --limit 20 --auto" \
  --name "auto-fractal" \
  --no-deliver --session isolated

# 每天自动记忆整合
openclaw cron add --cron "0 2 * * *" \
  --agent demo51-agent \
  --message "python3 skills/self-evolution/nightly_cycle.py" \
  --name "auto-consolidation" \
  --no-deliver --session isolated
```

---

## ✅ 使用效果

### 用户视角（无感知）

```
用户：之前那个 Python 优化怎么弄的？

Agent: 可以使用异步编程和缓存来提升性能。

📚 **根据历史记录：**

1. 任务：优化 Python 代码性能
   结果：任务已完成
   学习点：任务前检索帮助决策 (2026-04-11)

2. 会话记录 (压缩版，50 条消息)
   [ASSISTANT] 使用 async/await 处理 I/O 密集型任务... (2026-04-11)
```

### 系统视角（自动发生）

```
用户消息
  ↓
AutoMemorySearch.should_search() → True
  ↓
memory.search() → 找到 3 条记忆
  ↓
增强回复（引用历史）
  ↓
返回给用户
  ↓
（用户无感知）
```

---

## 🎯 集成到现有流程

### 方法 1: 修改 Harness Agent

在 `skills/harness-agent/SKILL.md` 中添加：

```markdown
## 🧠 记忆集成

**每次回复前：**

1. 调用 `AutoMemorySearch` 检索相关记忆
2. 如果有记忆，在回复中引用
3. 回复后自动记录反思
```

### 方法 2: 修改 OpenClaw 配置

在 `AGENTS.md` 中添加：

```markdown
## 🧠 记忆查询规则

**当用户问到以下类型的问题时，先查询记忆系统：**

1. 历史相关问题
2. 配置/使用问题
3. 项目/任务相关

**查询方法：**

```python
from skills.memory_search.search import AutoMemorySearch
search = AutoMemorySearch()
enhanced_response = search.search_and_respond(user_message, response)
```
```

---

**这就是无感知进化！** 🎓

用户正常使用，系统自动检索、自动记录、自动进化。
