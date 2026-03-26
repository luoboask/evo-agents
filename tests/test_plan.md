# evo-agents 测试计划

**测试员 Agent:** 测试员  
**测试日期:** 2026-03-26  
**测试版本:** evo-agents v1.0

---

## 📋 测试范围

### 1. 核心功能模块

| 模块 | 测试类型 | 优先级 |
|------|----------|--------|
| Memory Hub | 单元测试、集成测试 | P0 |
| 记忆搜索 (memory-search) | 功能测试、集成测试 | P0 |
| RAG 评估系统 | 功能测试、性能测试 | P0 |
| RAG 自动调优 | 功能测试 | P1 |
| 自进化系统 | 模块导入测试、功能测试 | P1 |
| Web 搜索 | 功能测试 | P2 |

### 2. 系统集成测试

| 测试项 | 描述 | 优先级 |
|--------|------|--------|
| 多 Agent 创建 | 验证脚本创建 Agent | P0 |
| 配置加载 | 验证配置文件解析 | P0 |
| 数据库完整性 | 验证 SQLite 数据库 | P0 |
| Git 忽略配置 | 验证 .gitignore | P1 |
| 目录结构 | 验证必要目录存在 | P1 |

### 3. 边界条件测试

| 测试项 | 描述 |
|--------|------|
| 空数据库 | 首次使用无数据场景 |
| 大数据量 | 大量记忆数据性能 |
| 并发访问 | 多进程同时写入 |
| 异常输入 | 非法参数处理 |

---

## 🧪 测试用例详细设计

### 测试用例 1: Memory Hub 初始化

**用例 ID:** TC-MH-001  
**模块:** libs/memory_hub  
**优先级:** P0

**前置条件:**
- Python 3.9+ 环境
- workspace 目录存在

**测试步骤:**
1. 导入 MemoryHub 类
2. 实例化 MemoryHub(agent_name='test-agent')
3. 验证 data/test-agent/memory 目录创建
4. 调用 stats() 方法

**预期结果:**
- MemoryHub 实例创建成功
- 目录结构自动创建
- stats() 返回包含 total 键的字典

**通过标准:** 无异常抛出，返回有效统计信息

---

### 测试用例 2: 记忆 CRUD 操作

**用例 ID:** TC-MH-002  
**模块:** libs/memory_hub/storage.py  
**优先级:** P0

**前置条件:**
- MemoryHub 实例已创建

**测试步骤:**
1. 添加记忆：add(content='测试内容', memory_type='observation')
2. 获取记忆：get(memory_id)
3. 搜索记忆：search(query='测试')
4. 更新记忆：update(memory_id, content='更新内容')
5. 删除记忆：delete(memory_id)
6. 验证删除：get(memory_id) 应返回 None

**预期结果:**
- 所有操作返回预期值
- 数据库状态正确

**通过标准:** CRUD 操作全部成功，数据一致性验证通过

---

### 测试用例 3: 记忆搜索功能

**用例 ID:** TC-MS-001  
**模块:** skills/memory-search/search_sqlite.py  
**优先级:** P0

**前置条件:**
- 记忆数据库包含测试数据
- Memory Hub 正常初始化

**测试步骤:**
1. 实例化 SQLiteMemorySearch(agent_name='demo2-agent')
2. 关键词搜索：search('测试', top_k=5, semantic=False)
3. 验证返回结果数量和格式
4. (可选) 语义搜索：search('测试', semantic=True)

**预期结果:**
- 搜索返回 List[Dict] 格式结果
- 结果包含 content、memory_type、timestamp 等字段
- 结果数量不超过 top_k

**通过标准:** 搜索功能正常，返回格式正确

---

### 测试用例 4: RAG 评估记录

**用例 ID:** TC-RAG-001  
**模块:** skills/rag/evaluate.py  
**优先级:** P0

**前置条件:**
- RAG 模块可导入

**测试步骤:**
1. 导入 RAGEvaluator
2. 实例化 evaluator = RAGEvaluator(agent_name='demo2-agent')
3. 记录评估：record(query='测试', retrieved_count=5, latency_ms=50.0, feedback='positive')
4. 验证记录写入

**预期结果:**
- 评估记录成功写入
- 日志文件存在或自动创建

**通过标准:** record() 无异常，数据持久化

---

### 测试用例 5: RAG 报告生成

**用例 ID:** TC-RAG-002  
**模块:** skills/rag/evaluate.py  
**优先级:** P1

**前置条件:**
- 存在评估记录

**测试步骤:**
1. 实例化 RAGEvaluator
2. 生成报告：generate_report(days=7)
3. 验证报告格式和内容

**预期结果:**
- 报告包含统计信息
- 包含"RAG 评估报告"标题

**通过标准:** 报告生成成功，格式正确

---

### 测试用例 6: RAG 自动调优

**用例 ID:** TC-RAG-003  
**模块:** skills/rag/auto_tune.py  
**优先级:** P1

**前置条件:**
- auto_tune 模块可导入

**测试步骤:**
1. 导入 AutoTuner
2. 实例化 tuner = AutoTuner()
3. 设计实验：design_experiments()
4. 分析结果：analyze_results()

**预期结果:**
- 实验设计返回非空列表
- 分析结果包含有效数据

**通过标准:** 调优功能正常，无异常

---

### 测试用例 7: 自进化核心模块

**用例 ID:** TC-SE-001  
**模块:** skills/self-evolution/  
**优先级:** P1

**前置条件:**
- self-evolution 目录存在

**测试步骤:**
1. 验证核心文件存在：main.py, memory_stream.py, fractal_thinking.py, nightly_cycle.py
2. 尝试导入 MemoryStream
3. 尝试导入 FractalThinkingEngine

**预期结果:**
- 核心文件完整
- 模块可导入（依赖满足时）

**通过标准:** 文件完整，模块导入无致命错误

---

### 测试用例 8: 数据库完整性

**用例 ID:** TC-DB-001  
**模块:** libs/memory_hub/storage.py  
**优先级:** P0

**前置条件:**
- 数据库文件存在或可创建

**测试步骤:**
1. 连接 SQLite 数据库
2. 验证表结构：memories 表存在
3. 检查索引：idx_content, idx_memory_type 等
4. 验证数据完整性约束

**预期结果:**
- 表结构符合设计
- 索引存在
- 无损坏数据

**通过标准:** 数据库结构完整，查询正常

---

### 测试用例 9: 配置加载

**用例 ID:** TC-CFG-001  
**模块:** config/  
**优先级:** P0

**前置条件:**
- 配置文件存在（或使用默认配置）

**测试步骤:**
1. 读取 config.yaml（如果存在）
2. 验证必需配置项：workspace, database, rag
3. 验证配置值类型正确

**预期结果:**
- 配置加载成功
- 必需配置项存在

**通过标准:** 配置验证通过

---

### 测试用例 10: Git 忽略配置

**用例 ID:** TC-GIT-001  
**模块:** .gitignore  
**优先级:** P1

**前置条件:**
- .gitignore 文件存在

**测试步骤:**
1. 读取 .gitignore 内容
2. 验证关键规则：*.db, *.jsonl, credentials.json, config.yaml
3. 验证 Agent 数据目录规则

**预期结果:**
- 敏感文件被忽略
- 运行时数据被忽略

**通过标准:** 关键规则存在

---

## 📊 测试执行计划

### 阶段 1: 单元测试 (P0) ✅ 已完成
- [x] TC-MH-001: Memory Hub 初始化
- [x] TC-MH-002: 记忆 CRUD 操作
- [x] TC-MS-001: 记忆搜索功能
- [x] TC-RAG-001: RAG 评估记录
- [x] TC-DB-001: 数据库完整性
- [x] TC-CFG-001: 配置加载

### 阶段 2: 集成测试 (P1) ✅ 已完成
- [x] TC-RAG-002: RAG 报告生成
- [x] TC-RAG-003: RAG 自动调优
- [x] TC-SE-001: 自进化核心模块
- [x] TC-GIT-001: Git 忽略配置

### 阶段 3: 边界测试 (P2) ✅ 已完成
- [x] 空数据库场景
- [x] 大数据量性能
- [x] 异常输入处理
- [x] 特殊字符处理
- [x] Unicode 内容处理

---

## ✅ 测试执行结果 (2026-03-26)

**总测试数:** 70  
**通过:** 70 (100%)  
**失败:** 0  
**跳过:** 1  

详细结果请查看：`tests/TEST_REPORT.md`

---

## 🐛 Bug 报告模板

```markdown
### Bug ID: BUG-XXX

**严重程度:** Critical/Major/Minor  
**模块:** [模块名称]  
**发现日期:** YYYY-MM-DD

**描述:**
[问题描述]

**复现步骤:**
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

**预期结果:**
[应该发生什么]

**实际结果:**
[实际发生了什么]

**环境信息:**
- Python 版本：x.x.x
- OS: macOS/Linux/Windows
- Workspace: demo2-agent

**附件:**
- 错误日志
- 截图（如适用）
```

---

## 📈 测试报告模板

```markdown
# 测试报告

**测试周期:** YYYY-MM-DD ~ YYYY-MM-DD  
**测试员:** 测试员 Agent  
**版本:** evo-agents v1.0

## 执行摘要

| 指标 | 数值 |
|------|------|
| 总测试用例 | XX |
| 通过 | XX |
| 失败 | XX |
| 跳过 | XX |
| 通过率 | XX% |

## 缺陷统计

| 严重程度 | 数量 | 已修复 | 待修复 |
|----------|------|--------|--------|
| Critical | X | X | X |
| Major | X | X | X |
| Minor | X | X | X |

## 详细结果

[每个测试用例的详细结果]

## 风险和建议

[测试发现的风险和改进建议]
```

---

**文档版本:** 1.0  
**最后更新:** 2026-03-26
