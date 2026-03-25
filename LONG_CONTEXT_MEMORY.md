# 长上下文记忆增强方案

_如何让 AI 拥有更长的上下文记忆能力_

---

## 🎯 当前局限

**现有系统的问题：**
- 每次会话独立，上下文有限
- 记忆基于文件，检索效率低
- 缺乏语义关联，难以联想
- 没有压缩机制，记忆膨胀

---

## 🏗️ 推荐架构：三层记忆系统

```
┌─────────────────────────────────────────────────────────┐
│                    三层记忆架构                          │
├─────────────────────────────────────────────────────────┤
│  Layer 3: 工作记忆 (Working Memory)                      │
│  - 当前会话上下文                                        │
│  - 最近 N 轮对话                                         │
│  - 临时变量和状态                                        │
│  - 容量：~4K-8K tokens                                  │
├─────────────────────────────────────────────────────────┤
│  Layer 2: 短期记忆 (Short-term Memory)                   │
│  - 今日/本周相关记忆                                     │
│  - 向量数据库存储                                        │
│  - 语义检索                                              │
│  - 容量：~100K-1M tokens                                │
├─────────────────────────────────────────────────────────┤
│  Layer 1: 长期记忆 (Long-term Memory)                    │
│  - 历史所有重要信息                                      │
│  - 压缩和摘要存储                                        │
│  - 知识图谱关联                                          │
│  - 容量：无上限                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 技术方案对比

### 方案 1: 向量数据库 + RAG（推荐）

**技术栈：**
- **Chroma** / **Pinecone** / **Milvus** - 向量数据库
- **Sentence Transformers** - 文本嵌入
- **LangChain** - RAG 框架

**优点：**
- ✅ 语义检索，理解意图
- ✅ 可扩展，支持海量记忆
- ✅ 检索速度快（毫秒级）
- ✅ 社区成熟，文档丰富

**缺点：**
- ⚠️ 需要额外服务
- ⚠️ 向量维度高，占用内存

**适用场景：** 需要长期、海量记忆

---

### 方案 2: 分层摘要 + 知识图谱

**技术栈：**
- **LLM 摘要** - 自动压缩记忆
- **Neo4j** / **NetworkX** - 知识图谱
- **层次化存储** - 日/周/月/年

**优点：**
- ✅ 结构化，关系清晰
- ✅ 人类可读，可解释
- ✅ 无需额外服务
- ✅ 压缩率高（100:1）

**缺点：**
- ⚠️ 检索不如向量精准
- ⚠️ 需要设计图谱结构

**适用场景：** 需要结构化、可解释的记忆

---

### 方案 3: 外部记忆 + 缓存策略

**技术栈：**
- **Redis** - 高速缓存
- **SQLite** / **PostgreSQL** - 持久化
- **LRU 缓存** - 热点数据

**优点：**
- ✅ 简单，易于实现
- ✅ 性能好，延迟低
- ✅ 可控性强

**缺点：**
- ⚠️ 缺乏语义理解
- ⚠️ 需要精确匹配

**适用场景：** 需要高性能、精确匹配

---

## 🚀 推荐实现：混合方案

```python
# 混合记忆系统
class HybridMemory:
    def __init__(self):
        # 工作记忆 - 当前上下文
        self.working_memory = []
        
        # 短期记忆 - 向量数据库
        self.vector_store = ChromaDB()
        
        # 长期记忆 - 知识图谱 + 摘要
        self.knowledge_graph = Neo4j()
        self.summaries = {}
    
    def remember(self, content, importance="medium"):
        """记忆内容"""
        # 1. 存入工作记忆
        self.working_memory.append(content)
        
        # 2. 重要内容存入向量库
        if importance in ["high", "critical"]:
            self.vector_store.add(content)
        
        # 3. 关键内容存入知识图谱
        if importance == "critical":
            self.knowledge_graph.add_entity(content)
    
    def recall(self, query, context_size="medium"):
        """回忆内容"""
        # 1. 先查工作记忆
        if context_size == "small":
            return self._search_working_memory(query)
        
        # 2. 再查向量库
        if context_size in ["medium", "large"]:
            vector_results = self.vector_store.search(query, k=5)
        
        # 3. 最后查知识图谱
        if context_size == "large":
            graph_results = self.knowledge_graph.query(query)
        
        # 4. 合并排序
        return self._merge_results(vector_results, graph_results)
```

---

## 📦 具体技术选型

### 轻量级方案（推荐用于 OpenClaw）

```bash
# 1. 安装 Chroma（本地向量数据库）
pip install chromadb

# 2. 安装 sentence-transformers
pip install sentence-transformers

# 3. 使用 Ollama 生成嵌入（已有）
# 使用 nomic-embed-text 模型
```

**代码示例：**
```python
import chromadb
from chromadb.config import Settings

# 初始化本地向量库
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="memory/vector_db"
))

# 创建集合
collection = client.create_collection("long_term_memory")

# 添加记忆
collection.add(
    documents=["用户喜欢简洁的回答"],
    metadatas=[{"type": "preference", "date": "2026-03-16"}],
    ids=["mem_001"]
)

# 语义检索
results = collection.query(
    query_texts=["用户偏好什么风格？"],
    n_results=3
)
```

---

## 🎯 实施路线图

### Phase 1: 向量记忆（1-2天）
- [ ] 集成 ChromaDB
- [ ] 实现自动嵌入生成
- [ ] 替换文件搜索为向量搜索

### Phase 2: 分层摘要（2-3天）
- [ ] 实现自动摘要
- [ ] 建立层次化存储
- [ ] 压缩旧记忆

### Phase 3: 知识增强（3-5天）
- [ ] 完善知识图谱
- [ ] 实体关系提取
- [ ] 跨记忆关联

### Phase 4: 智能检索（持续优化）
- [ ] 混合检索策略
- [ ] 相关性排序
- [ ] 上下文压缩

---

## 💡 关键设计原则

1. **渐进加载** - 不要一次性加载所有记忆
2. **重要性分层** - 关键信息多存储，次要信息可丢弃
3. **遗忘机制** - 旧记忆逐渐淡化或归档
4. **关联激活** - 相关记忆自动联想
5. **人类可读** - 保持部分记忆人类可理解

---

## 📊 预期效果

| 指标 | 当前 | 增强后 |
|------|------|--------|
| 上下文长度 | ~4K tokens | ~100K+ tokens |
| 记忆检索 | 文件名匹配 | 语义理解 |
| 关联能力 | 无 | 自动联想 |
| 压缩率 | 1:1 | 100:1 |
| 检索速度 | 秒级 | 毫秒级 |

---

## 🔗 参考资源

- [ChromaDB 文档](https://docs.trychroma.com/)
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [RAG 最佳实践](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [MemGPT 论文](https://arxiv.org/abs/2310.08560)

---

_需要我立即开始实施 Phase 1 吗？_ 🤖
