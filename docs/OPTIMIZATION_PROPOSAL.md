# 记忆系统优化建议

**创建日期:** 2026-03-30  
**优先级:** 高  
**影响范围:** skills/memory-search/

---

## 📋 问题背景

根据实际使用发现以下问题：

1. **知识库索引为空** - 新安装 agent 后，已有记忆文件不会被自动索引
2. **向量缓存无限增长** - `integrated_cache.json` 会越来越大，没有清理机制
3. **双索引不同步** - 向量索引和 SQLite 索引独立运行，数据不一致

---

## 🔍 问题分析

### 1. 索引构建机制

**当前逻辑:**
```python
# search.py
def record_interaction(self, role, content, metadata=None):
    # 只记录新交互
    entry = {...}
    self.working_memory.append(entry)
    self._add_to_vector(entry)  # 只索引新记录
```

**问题:**
- ❌ 已有记忆文件不会被索引
- ❌ 需要手动运行 `memory_indexer.py`
- ❌ 新用户体验差

### 2. 向量缓存大小

**当前状态:**
```
文件大小：90KB (4 条记录)
预估增长:
- 1000 条 → 90MB
- 10000 条 → 900MB
- 100000 条 → 9GB
```

**问题:**
- ❌ 没有大小限制
- ❌ 没有清理机制
- ❌ 没有压缩策略

### 3. 双索引同步

**当前架构:**
```
向量索引 (integrated_cache.json)
  └── 只包含新交互

SQLite 索引 (memory_index.db)
  └── 需要手动构建
```

**问题:**
- ❌ 两套系统独立
- ❌ 数据不一致
- ❌ 维护成本高

---

## 💡 优化建议

### 1. 自动索引已有文件 ⭐⭐⭐

**方案:**
```python
# search.py
def __init__(self, workspace):
    self.workspace = workspace
    self._load_vector_cache()
    self._index_existing_memories()  # ← 新增

def _index_existing_memories(self):
    """索引已有记忆文件"""
    memory_dir = self.workspace / 'memory'
    for md_file in memory_dir.glob('*.md'):
        if not self._is_indexed(md_file):
            self._index_file(md_file)
```

**优势:**
- ✅ 新安装自动索引
- ✅ 用户体验好
- ✅ 减少手动操作

### 2. 向量缓存优化 ⭐⭐⭐

**方案 A: 大小限制 + LRU 清理**
```python
# search.py
MAX_CACHE_SIZE = 10000  # 最多 10000 条
MAX_CACHE_MB = 100      # 最多 100MB

def _add_to_vector(self, entry):
    if len(self.vector_cache) >= MAX_CACHE_SIZE:
        self._cleanup_lru()  # 清理最旧的
    self.vector_cache.append(entry)
```

**方案 B: 定期压缩**
```python
# 每周运行一次
def compress_cache():
    # 压缩旧记录
    # 删除低重要性记录
    pass
```

**方案 C: 迁移到 SQLite**
```python
# 使用现有的 memory_index.db
# 统一存储，避免 JSON 文件过大
```

**推荐:** 方案 C (统一存储)

### 3. 统一索引系统 ⭐⭐⭐⭐

**方案:**
```python
# 统一使用 SQLite
class UnifiedMemoryIndex:
    def __init__(self, workspace):
        self.db_path = workspace / 'data' / 'memory_index.db'
        self._init_db()
    
    def add(self, entry):
        # 同时添加到向量缓存和 SQLite
        self._add_to_vector(entry)
        self._add_to_sqlite(entry)
    
    def search(self, query, top_k=10):
        # 统一搜索接口
        pass
```

**优势:**
- ✅ 单一数据源
- ✅ 自动同步
- ✅ 易于维护
- ✅ 支持 SQL 查询

---

## 📊 实现优先级

| 优化项 | 优先级 | 工作量 | 影响 |
|--------|--------|--------|------|
| 统一索引系统 | ⭐⭐⭐⭐ | 中 | 高 |
| 自动索引已有文件 | ⭐⭐⭐ | 低 | 中 |
| 向量缓存大小限制 | ⭐⭐⭐ | 低 | 中 |

---

## 🎯 实施计划

### Phase 1: 紧急修复 (1 天)
- [ ] 添加向量缓存大小限制
- [ ] 添加自动索引已有文件

### Phase 2: 架构优化 (3 天)
- [ ] 设计统一索引接口
- [ ] 迁移到 SQLite 存储
- [ ] 添加数据迁移脚本

### Phase 3: 性能优化 (2 天)
- [ ] 添加索引压缩
- [ ] 添加定期清理任务
- [ ] 性能测试和调优

---

## 📝 相关代码位置

```
skills/memory-search/
├── search.py              # 主要修改
├── search_sqlite.py       # 统一接口
├── semantic_search.py     # 索引构建
└── auto_record.py         # 自动记录
```

---

**创建者:** AI Assistant  
**审核状态:** 待审核  
**最后更新:** 2026-03-30
