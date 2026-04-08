# 存储限制配置更新

## 📅 更新时间
**2026-04-08 21:21 GMT+8**

---

## 📊 更新内容

### 修改前
| 限制项 | 旧值 |
|--------|------|
| **单条消息长度** | 500 字符 |
| **每会话记忆数** | 50 条 |
| **总容量** | ~25K 字符/会话 |

### 修改后
| 限制项 | 新值 | 提升 |
|--------|------|------|
| **单条消息长度** | **4000 字符** | 8x ⬆️ |
| **每会话记忆数** | **100 条** | 2x ⬆️ |
| **总容量** | **~400K 字符/会话** | 16x ⬆️ |

---

## 📝 详细说明

### 1. 单条消息长度：500 → 4000 字符

**文件**: `scripts/core/scan_sessions.py`

**修改**:
```python
# 修改前
content=f"[{role.upper()}] {content[:500]}",  # 限制长度

# 修改后
content=f"[{role.upper()}] {content[:4000]}",  # 4000 字符（约 2000 汉字）
```

**原因**:
- 500 字符太短，无法保存完整对话
- 4000 字符可以保存：
  - 完整的长消息
  - 代码片段
  - 详细说明
  - 多轮对话上下文

---

### 2. 每会话记忆数：50 → 100 条

**文件**: `libs/memory_hub/session_storage.py`

**修改**:
```python
# 修改前
MAX_SESSION_MEMORIES = 50  # 每个会话最多保留 50 条

# 修改后
MAX_SESSION_MEMORIES = 100  # 每个会话最多保留 100 条（增加容量）
```

**原因**:
- 50 条对于长会话不够用
- 100 条可以保存更长的对话历史
- 仍然保持自动清理机制
- 避免无限增长

---

## 📈 容量对比

### 实际例子

**场景**: 保存一次完整的编程讨论会话

**修改前 (500 字符 × 50 条)**:
```
会话 1: "帮我写个函数..." (500 字符被截断，丢失后续内容)
会话 2: "好的，这是代码..." (500 字符被截断，代码不完整)
...
第 50 条后：最早的消息被删除
```

**修改后 (4000 字符 × 100 条)**:
```
会话 1: "帮我写个函数，需要支持以下功能：
1. 参数验证
2. 错误处理
3. 日志记录
4. 性能优化
... [完整内容，4000 字符]

会话 2: "好的，这是完整的实现：
```python
def my_function(param1, param2):
    # 参数验证
    if not param1:
        raise ValueError(...)
    
    # 错误处理
    try:
        # 主要逻辑
        ...
    except Exception as e:
        logger.error(...)
        raise
    
    return result
```
... [完整代码和说明，4000 字符]

... [保存 100 条完整对话]
```

---

## 🎯 适用场景

### 适合保存的内容

✅ **现在可以完整保存**:
- 长消息（1000-3000 字符）
- 代码片段（含注释和说明）
- 详细的技术讨论
- 多轮对话上下文
- 会议记录
- 项目规划文档
- 学习笔记

❌ **仍然不适合**:
- 完整文件（>10K 字符）
- 大型代码文件
- 完整书籍章节
- 视频/音频内容

---

## ⚙️ 性能影响

### 数据库大小估算

**修改前**:
```
50 条 × 500 字符 = 25,000 字符/会话
10 个会话 ≈ 250K 字符 ≈ 0.25MB
```

**修改后**:
```
100 条 × 4000 字符 = 400,000 字符/会话
10 个会话 ≈ 4,000K 字符 ≈ 4MB
```

**影响**:
- ✅ 数据库增大 16 倍（但仍然很小）
- ✅ 搜索性能影响可忽略（有索引）
- ✅ 内存占用增加约 4MB/10 会话

---

## 🔧 自定义配置

### 如果需要更大的限制

```python
# scripts/core/scan_sessions.py
# 修改为 8000 字符（约 4000 汉字）
content=f"[{role.upper()}] {content[:8000]}",

# libs/memory_hub/session_storage.py
# 修改为 200 条
MAX_SESSION_MEMORIES = 200
```

### 如果需要无限制

```python
# scripts/core/scan_sessions.py
# 不限制长度（但不推荐）
content=f"[{role.upper()}] {content}",

# libs/memory_hub/session_storage.py
# 增加到很大的数
MAX_SESSION_MEMORIES = 1000
```

---

## 📋 修改的文件

| 文件 | 修改内容 | 位置 |
|------|---------|------|
| `scripts/core/scan_sessions.py` | 500 → 4000 字符 | 第 195 行 |
| `libs/memory_hub/session_storage.py` | 50 → 100 条 | 第 28 行 |

---

## ✅ 验证

```bash
# 验证配置
cd ~/.openclaw/workspace-claude-code-agent
python3 -c "
from libs.memory_hub.session_storage import SessionMemoryStorage
print(f'每会话记忆数：{SessionMemoryStorage.MAX_SESSION_MEMORIES} 条')
"

# 输出:
# 每会话记忆数：100 条
```

---

## 📚 相关文档

- [会话扫描使用指南](./SESSION_SCAN_CRON.md)
- [Session Memories 读取指南](./SESSION_MEMORIES_READ_GUIDE.md)
- [Memory Hub API 文档](../libs/memory_hub/README_SESSION_MEMORY.md)

---

**更新完成！** 🎉

现在可以保存更完整的对话内容了！
