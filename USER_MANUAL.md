# ai-baby 使用手册

**版本：** v5.1  
**最后更新：** 2026-03-23

---

## 🚀 快速开始

### 第一次使用

```bash
# 1. 进入工作区
cd /Users/dhr/.openclaw/workspace-ai-baby

# 2. 初始化系统
python3 init.py

# 3. 查看状态
./start.sh
```

### 日常使用

**无需额外操作！** RAG 记录已自动集成到记忆搜索中。

```python
# 正常使用记忆搜索
from memory_search.search_sqlite import SQLiteMemorySearch

search = SQLiteMemorySearch()
results = search.search("用户问题", top_k=5, semantic=True)
# ✅ 自动记录 RAG 指标
```

---

## 📋 核心功能

### 1. 记忆搜索

**位置：** `skills/memory-search/`

```bash
# 关键词搜索
python3 skills/memory-search/search_sqlite.py "RAG"

# 语义搜索（需要 Ollama）
python3 skills/memory-search/search_sqlite.py "优化检索" --semantic

# 添加记忆
python3 skills/memory-search/search_sqlite.py --add "RAG 评估方法" \
  --type knowledge \
  --details '{"source": "AutoRAG"}' \
  --source "https://..."

# 查看统计
python3 skills/memory-search/search_sqlite.py --stats

# 禁用 RAG 记录（测试用）
python3 skills/memory-search/search_sqlite.py "测试" --no-record
```

**Python 调用:**
```python
from memory_search.search_sqlite import SQLiteMemorySearch

search = SQLiteMemorySearch()

# 搜索
results = search.search("查询", top_k=5, semantic=True)

# 添加记忆
search.add(
    content="记忆内容",
    memory_type="knowledge",
    importance=8.0,
    tags=["RAG", "评估"],
    details={"key": "value"},
    source_url="https://..."
)
```

---

### 2. RAG 评估

**位置：** `skills/rag/`

```bash
# 查看报告
python3 skills/rag/evaluate.py --report --days 7

# 记录一次检索
python3 skills/rag/evaluate.py --record \
  --query "测试查询" \
  --retrieved 5 \
  --latency 100 \
  --feedback positive

# 比较配置
python3 skills/rag/evaluate.py --compare

# 自动调优（需要 10+ 条数据）
python3 skills/rag/auto_tune.py --report

# 建议下一个实验
python3 skills/rag/auto_tune.py --next

# 设计实验
python3 skills/rag/auto_tune.py --design
```

**Python 调用:**
```python
from skills.rag.recorder import start_recording, finish_recording

# 开始记录
start_recording("用户的问题")

# 执行检索...
results = search(...)

# 完成记录
finish_recording(
    retrieved_count=len(results),
    similarity_score=0.85,
    latency_ms=95.0,
    feedback="positive"
)
```

---

### 3. 自进化系统

**位置：** `skills/self-evolution-5.0/`

```bash
cd skills/self-evolution-5.0

# 查看状态
python3 main.py status

# 运行分形思考
python3 main.py fractal --limit 10

# 运行夜间循环
python3 main.py nightly

# 查看记忆
python3 main.py memory list --limit 20

# 记录进化事件
python3 main.py evolve --type KNOWLEDGE_GAINED --content "RAG 系统集成完成"

# 测试 Embedding
python3 main.py embedding "修复 Bug" "修复错误"
```

---

## 📊 数据积累目标

| 阶段 | RAG 数据量 | 目标 | 操作 |
|------|-----------|------|------|
| **初期** | 0-10 条 | 验证系统正常 | 正常使用 |
| **成长期** | 10-50 条 | 第一次自动调优 | 运行 `auto_tune.py --report` |
| **成熟期** | 50+ 条 | 稳定优化 | 每周回顾报告 |

**当前状态:** 5 条（初期 → 成长期）

---

## 📅 日常任务

### 早晨检查
```bash
./start.sh  # 查看系统状态
```

### 对话中（自动）
- ✅ RAG 记录自动开启
- ✅ 记忆搜索自动记录指标

### 晚上检查
- 回顾今日对话质量
- 记录重要事件到记忆

### 每周任务

**周一：RAG 质量检查**
```bash
python3 skills/rag/evaluate.py --report --days 7
python3 skills/rag/auto_tune.py --report  # 如果数据足够
```

**周日：记忆维护**
- 回顾本周新增记忆
- 合并重复内容
- 更新 MEMORY.md

---

## 🔧 配置说明

### RAG 配置 (`skills/rag/config.json`)

```json
{
  "top_k_options": [3, 5, 10],
  "similarity_thresholds": [0.6, 0.7, 0.8],
  "chunk_sizes": [256, 512, 1024],
  "weights": {
    "accuracy": 0.6,   // 准确率权重
    "latency": 0.3,    // 延迟权重
    "cost": 0.1        // 成本权重
  },
  "current_config": {
    "top_k": 5,
    "similarity_threshold": 0.7,
    "chunk_size": 512
  }
}
```

**调整权重示例:**

**注重准确率:**
```json
"weights": {"accuracy": 0.8, "latency": 0.15, "cost": 0.05}
```

**注重速度:**
```json
"weights": {"accuracy": 0.4, "latency": 0.5, "cost": 0.1}
```

---

## 📈 监控指标

### RAG 评估指标

| 指标 | 优秀 | 良好 | 需改进 |
|------|------|------|--------|
| **延迟** | <50ms | 50-150ms | >150ms |
| **正面反馈率** | >70% | 50-70% | <50% |
| **检索使用率** | >80% | 50-80% | <50% |
| **平均相似度** | >0.8 | 0.6-0.8 | <0.6 |

### 记忆流指标

| 指标 | 说明 |
|------|------|
| 记忆总数 | 持续增长的记忆数量 |
| 按类型分布 | observation/goal/reflection/knowledge |
| 平均重要性 | 记忆的平均重要性分数 |

---

## 🆘 故障处理

### RAG 记录未生效

```bash
# 检查导入
python3 -c "from skills.rag.recorder import start_recording; print('OK')"

# 查看日志文件
ls -la skills/rag/logs/evaluations.jsonl

# 测试记录
python3 skills/rag/recorder.py
```

### 记忆搜索失败

```bash
# 检查数据库
ls -la memory/ai-baby_memory_stream.db

# 测试搜索
python3 skills/memory-search/search_sqlite.py "测试" --stats

# 重新初始化
python3 init.py
```

### 自进化系统异常

```bash
cd skills/self-evolution-5.0

# 检查状态
python3 main.py status

# 查看日志
tail -20 /tmp/nightly.log

# 重新初始化
python3 install.py
```

### Ollama 连接失败

```bash
# 检查 Ollama 状态
ollama list
ollama serve  # 如果没有运行

# 测试 Embedding
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "nomic-embed-text", "prompt": "test"}'
```

---

## 📚 文档索引

### 体系文档
- `SELF_EVOLUTION_SYSTEM.md` - 体系总览 ⭐
- `MEMORY.md` - 长期记忆
- `HEARTBEAT.md` - 日常任务

### RAG 评估文档
- `skills/rag/README.md` - 框架说明
- `skills/rag/USAGE.md` - 使用指南
- `skills/rag/INTEGRATION.md` - 集成文档

### 自进化文档
- `skills/self-evolution-5.0/ARCHITECTURE.md` - 架构详解
- `skills/self-evolution-5.0/README_FINAL.md` - 功能总结
- `skills/self-evolution-5.0/INSTALL.md` - 安装指南

### 使用文档
- `USER_MANUAL.md` - 本文档
- `start.sh` - 快速启动脚本
- `init.py` - 初始化脚本

---

## 💡 最佳实践

### 学习原则
1. **Text > Brain** 📝 - 写下来才能存活
2. **Learn → Record → Apply** - 学习闭环
3. **Demonstrate > Explain** - 展示胜过解释

### RAG 优化原则
1. **评估驱动** - 没有度量就没有优化
2. **小步迭代** - 每次只改一个参数
3. **用户优先** - 满意度胜过指标
4. **持续积累** - 数据越多越准确

### 工程原则
1. **复用优先** - 避免重复造轮子
2. **文档即代码** - 详细记录设计决策
3. **自动化** - 能自动就不手动

---

## 🎯 下一步计划

### P0 - 本周
- [ ] 积累 RAG 数据（目标：50+ 条）
- [ ] 第一次配置优化（需要 10+ 条）

### P1 - 本月
- [ ] 用户反馈自动推断
- [ ] RAG 可视化报告
- [ ] 激活自进化核心

### P2 - 下季度
- [ ] 多 Agent 协作
- [ ] 跨工作区知识共享
- [ ] Web UI 界面

---

## 🆘 获取帮助

1. 查看相关文档（见文档索引）
2. 运行 `./start.sh` 查看系统状态
3. 在 AIWay 发帖提问或私信 @ai-baby

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23  
**许可证：** MIT
