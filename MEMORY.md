# Long-Term Memory

## About My Human

- **haoran.dhr**，开发者，macOS Apple Silicon，时区 GMT+8
- 中文交流，简洁直接，不喜欢废话和花架子
- 期望 AI 主动、有记忆、能自己推断上下文
- 在用 OpenClaw 运行 Agent，对 AI Agent 架构有深入理解

## Key Context

### evo-agents 工作空间 (workspace-ai-baby)
- **创建时间**：2026-03-19
- **大改造**：2026-03-23，70 分钟完成 5 阶段重构
  - Phase 1: Memory Hub 统一管理层 (840 行)
  - Phase 2: 技能更新（代码减少 56%）
  - Phase 3: 知识结构（4 分类）
  - Phase 4: 多 Agent 配置
  - Phase 5: 数据迁移
  - 40+ 次 Git 提交，60+ 新文件
- **技能模块**：memory-search, rag, self-evolution, websearch, aiway
- **Python 记忆系统**：memory_stream.db + knowledge_base.db + public/ 知识文件
- **夜间循环**：nightly_cycle.py 自动跑（复盘、压缩、清理、进化扫描）

### 2026-03-25 发现的架构问题
- **两套记忆系统断裂**：OpenClaw 原生 Markdown 记忆 vs Python SQLite 记忆互不相通
- OpenClaw 模板文件（AGENTS.md/USER.md/MEMORY.md）从未被之前的 agent 正式使用
- 之前的 agent 只顾建系统写代码，没有记住用户是谁
- **修复方向**：以 OpenClaw 原生记忆（Markdown）为主，SQLite 作补充索引
- 每次对话后要回写关键信息到 Markdown 文件

## Lessons Learned

- **记忆要服务于 LLM，不是服务于代码** — 每次醒来的是 LLM，读的是 Markdown
- **系统再精致，不认识主人就是废的** — 先记人，再记技术
- **两套系统并存必须有桥接** — 否则必然断裂
- **Text > Brain** — 写下来，不然下一个 session 又一脸懵

## Core Principles

- **Text > Brain** — Write it down or it doesn't survive
- **Learn → Record → Apply** — Don't just learn, document and use
- Be genuinely helpful, not performatively helpful
- Actions > filler words
- Earn trust through competence
- Respect boundaries, especially with external actions

## Pending

- [ ] 统一记忆系统（Markdown 为主 + SQLite 索引）
- [ ] 确认用户社交平台账号，方便以后发帖

---
_Last updated: 2026-03-25_
