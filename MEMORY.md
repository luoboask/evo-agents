# MEMORY.md - 长期记忆

_重要的人、事、偏好、决定_

## 用户
- 名称：待填写
- 时区：Asia/Shanghai (GMT+8)
- 连接方式：openclaw-tui

## 重要事件
- 2026-03-16：首次上线，创建 websearch 技能、记忆系统、JVS Claw 调研
- 2026-03-17：工作台优化（修复 HTTP 400、添加 API 端点、深蓝渐变主题 dashboard）
- 2026-03-18：自进化系统 v5.0 完成，创建 sandbox-agent 和 tao-admin，实现多 Agent 数据隔离
- 2026-03-24：同步 evo-agents 优化成果（memory_hub 库、RAG 评估、自进化系统 v5.0、技能元数据规范化）
- 2026-03-25：统一记忆系统改造（双向桥接、并发安全、bge-m3 语义搜索），推广到 ai-baby，清理 master 为模板
- 2026-03-27：evo-agents 全面优化（web-knowledge v6.0、文档规范化、卸载能力、完整测试 96.4% 通过）
- 2026-03-28：evo-agents 路径系统统一、Gitee 加速、unified-memory-skill 简化
- 2026-04-06：Harness Agent 插件系统完成（8 个领域插件、45+ 专业工具、文档国际化）
- 2026-04-07：记忆系统改进（主动记录重要对话、会话结束自动总结）
- 2026-04-08：会话记忆独立表（每会话 50 条限制、两套接口互不干扰）
- 2026-04-12：无感知进化系统完成（进化事件自动提取、分形思考、智能回复增强器）
- 2026-04-13：memory_manager.py 整合（3 脚本合并、Cron 任务修复、MLX 模型下载失败）
- 2026-04-14：每周记忆维护完成、MLX 模型下载完成（52GB Qwen3.5-27B）

## 技能
- **websearch**：基于 Bing 的网页搜索，无需 API key
  - 位置：`skills/websearch/`
  - 用法：`python3 skills/websearch/search.py "query"`
- **memory-search**：混合记忆系统（关键词搜索 + 语义搜索）
  - 位置：`skills/memory-search/`
  - 依赖：Ollama + nomic-embed-text 嵌入模型
- **rag**：RAG 评估系统，记录和分析检索增强生成性能
  - 位置：`skills/rag/`
  - 功能：自动记录、性能分析、自动调优、HTML 报告
- **self-evolution**：自进化系统 v5.0，基于 Generative Agents 架构
  - 位置：`skills/self-evolution/`
  - 功能：事件驱动进化、分形思考、夜间循环
- **integration-sandbox**：导购×营销联调沙箱系统
- **sandbox-executor**：联调沙箱测试场景执行器

## 偏好
- 待了解...

## 决定
- 使用本地 OpenClaw 而非云端 JVS Claw

## Agent
- **main-agent**：默认主 Agent
- **sandbox-agent**：联调沙箱专用 Agent（独立数据库）
- **tao-admin**：自营电商平台 Agent（独立数据库）

## 共享库
- **libs/memory_hub**：记忆管理核心库
  - 统一接口：MemoryHub（add/search/update/delete/stats）
  - 支持关键词搜索 + 语义搜索（Ollama）
  - Embedding 缓存机制
  - RAG 评估集成
