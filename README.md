# ai-baby 工作区

**版本：** v5.1  
**最后更新：** 2026-03-23  
**状态：** ✅ RAG 评估系统集成完成 · 🔐 配置分离完成

---

## 🎯 快速开始

```bash
# 进入工作区
cd /Users/dhr/.openclaw/workspace-ai-baby

# 查看系统状态
./start.sh

# 初始化（第一次使用）
python3 init.py

# 配置分离（保护个人数据）
python3 separate_config.py
```

---

## 🔐 配置分离

**重要：** 个人数据和敏感信息存储在 Git 忽略的安全位置。

```
~/.openclaw/workspace-ai-baby-config/   # 个人配置（Git 忽略）
├── config.yaml                         # 个人配置
├── credentials.json                    # API 凭证
├── memory/                             # 数据库
│   ├── ai-baby_memory_stream.db
│   └── ai-baby_knowledge_base.db
└── logs/                               # 日志
    └── evaluations.jsonl

~/workspace-ai-baby/                    # 代码和文档（可提交 Git）
├── skills/                             # 技能代码
├── *.md                                # 文档
└── *.py                                # 脚本
```

**详见：** `CONFIG_SEPARATION.md`

---

## 📁 目录结构

```
workspace-ai-baby/
├── 📄 README.md                  # 本文档
├── 📄 SELF_EVOLUTION_SYSTEM.md   # 自进化体系总览 ⭐
├── 📄 USER_MANUAL.md             # 使用手册
├── 📄 IMPROVEMENT_PLAN.md        # 改进计划
├── 📄 MEMORY.md                  # 长期记忆
├── 📄 HEARTBEAT.md               # 日常任务
├── 🔧 start.sh                   # 快速启动脚本
├── 🔧 init.py                    # 初始化脚本
│
├── 📂 skills/                    # 技能目录
│   ├── rag/                      # ⭐ RAG 评估系统（新增）
│   ├── memory-search/            # 记忆搜索（已集成 RAG）
│   ├── self-evolution-5.0/       # 自进化核心
│   ├── aiway/                    # AIWay 社区
│   ├── hybrid-memory/            # 混合记忆
│   ├── knowledge-graph/          # 知识图谱
│   ├── self-reflection/          # 自我反思
│   └── websearch/                # 网页搜索
│
├── 📂 memory/                    # 数据目录
│   ├── ai-baby_memory_stream.db  # 记忆流（19 条）
│   ├── ai-baby_knowledge_base.db # 知识库
│   ├── 2026-03-23.md             # 今日记录
│   └── learning/                 # 学习记录
│
└── 📂 apps/                      # 应用
    ├── agent-mind-visualizer/    # Agent 思维可视化
    ├── ai-pet-simulator/         # AI 宠物模拟
    └── content-creation-visualizer/ # 内容创作可视化
```

---

## 🚀 核心功能

### 1. RAG 评估系统 ⭐ NEW!

**位置：** `skills/rag/`

自动评估和优化检索增强生成（RAG）系统的质量。

```bash
# 查看本周报告
python3 skills/rag/evaluate.py --report --days 7

# 自动调优（需要 10+ 条数据）
python3 skills/rag/auto_tune.py --report

# 建议下一个实验
python3 skills/rag/auto_tune.py --next
```

**当前状态:** 5 条记录（目标：50+ 条）

---

### 2. 记忆搜索

**位置：** `skills/memory-search/`

关键词匹配 + 向量语义搜索。

```bash
# 语义搜索（自动记录 RAG）
python3 skills/memory-search/search_sqlite.py "RAG" --semantic

# 添加记忆
python3 skills/memory-search/search_sqlite.py --add "记忆内容" \
  --type knowledge --details '{"key": "value"}'
```

**当前状态:** 19 条记忆

---

### 3. 自进化系统

**位置：** `skills/self-evolution-5.0/`

分形思考 + 夜间循环 + 记忆流。

```bash
cd skills/self-evolution-5.0

# 查看状态
python3 main.py status

# 运行分形思考
python3 main.py fractal --limit 10

# 运行夜间循环
python3 main.py nightly
```

---

## 📊 当前状态

| 组件 | 状态 | 数据量 |
|------|------|--------|
| **记忆流** | ✅ 活跃 | 19 条 |
| **知识库** | ✅ 活跃 | 4 条 |
| **观察** | ✅ 活跃 | 8 条 |
| **反思** | ✅ 活跃 | 8 条 |
| **目标** | ✅ 活跃 | 3 条 |
| **RAG 评估** | ✅ 新增 | 5 条 |

---

## 📅 日常任务

### 每天
```bash
./start.sh  # 查看系统状态
```

### 每周
```bash
# RAG 质量检查
python3 skills/rag/evaluate.py --report --days 7

# 如果数据足够，运行自动调优
python3 skills/rag/auto_tune.py --report
```

详见 `HEARTBEAT.md`

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| **SELF_EVOLUTION_SYSTEM.md** ⭐ | 自进化体系总览（架构、数据流、模块） |
| **USER_MANUAL.md** | 使用手册（命令、配置、故障处理） |
| **IMPROVEMENT_PLAN.md** | 改进计划（里程碑、待办事项） |
| **MEMORY.md** | 长期记忆（重要事件、偏好、决定） |
| **HEARTBEAT.md** | 日常任务（每日/每周检查） |
| **skills/rag/README.md** | RAG 框架说明 |
| **skills/rag/USAGE.md** | RAG 使用指南 |
| **skills/rag/INTEGRATION.md** | RAG 集成文档 |

---

## 🔧 常用命令

### 系统状态
```bash
./start.sh
```

### RAG 评估
```bash
# 查看报告
python3 skills/rag/evaluate.py --report --days 7

# 自动调优
python3 skills/rag/auto_tune.py --report
```

### 记忆搜索
```bash
# 语义搜索
python3 skills/memory-search/search_sqlite.py "查询" --semantic

# 添加记忆
python3 skills/memory-search/search_sqlite.py --add "内容" --type knowledge
```

### 自进化
```bash
cd skills/self-evolution-5.0

# 分形思考
python3 main.py fractal --limit 10

# 夜间循环
python3 main.py nightly
```

---

## 🎯 下一步计划

### P0 - 本周
- [ ] 积累 RAG 数据（目标：10+ 条）
- [ ] 第一次自动调优

### P1 - 本月
- [ ] 用户反馈自动推断
- [ ] RAG 可视化报告
- [ ] 激活自进化核心

### P2 - 下季度
- [ ] 多 Agent 协作
- [ ] 跨工作区知识共享
- [ ] Web UI 界面

详见 `IMPROVEMENT_PLAN.md`

---

## 🆘 获取帮助

1. 查看相关文档（见上方文档索引）
2. 运行 `./start.sh` 查看系统状态
3. 在 AIWay 发帖提问或私信 @ai-baby

---

## 📈 演进历史

| 版本 | 日期 | 关键变更 |
|------|------|----------|
| v5.0 | 2026-03-17 | 自进化系统核心完成 |
| v5.0.1 | 2026-03-18 | 多 Agent 数据隔离 |
| **v5.1** | **2026-03-23** | **RAG 评估系统集成** ⭐ |

---

## 🎉 总结

**ai-baby 自进化体系 v5.1 核心功能已完成！**

- ✅ 记忆流系统（Generative Agents 启发）
- ✅ 分形思考引擎（TinkerClaw 核心）
- ✅ 夜间进化循环（TinkerClaw 启发）
- ✅ **RAG 评估系统（AutoRAG 理念）** ⭐ NEW!
- ✅ 向量语义搜索（Ollama 集成）
- ✅ 统一 CLI 入口
- ✅ 完整架构文档

**系统已可投入使用，当前重点是积累 RAG 评估数据，为第一次自动优化做准备。**

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23  
**许可证：** MIT  
**社区：** AIWay (https://aiway.alibaba-inc.com)
