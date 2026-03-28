---
name: self-evolution
description: 自进化系统 v5.0，基于 Generative Agents 的完整架构
homepage: https://github.com/luoboask/evo-agents
metadata:
  emoji: "🧬"
  category: system
  version: "5.0.0"
  updated_at: "2026-03-24"
---

# 自进化系统 v5.0

基于 Generative Agents 和 TinkerClaw 的自进化系统，实现记忆流、分形思考、夜间循环的完整架构。

## 核心架构

```
┌─────────────────────────────────────────────────────┐
│              自进化系统 v5.0                          │
├─────────────────────────────────────────────────────┤
│  记忆流 (Memory Stream)                              │
│  - 实时记录交互和观察                                │
│  - 重要性评估和分发                                  │
│  - 支持关键词和语义检索                              │
├─────────────────────────────────────────────────────┤
│  分形思考 (Fractal Thinking)                         │
│  - 4 层深度分析（观察→模式→原则→元规则）              │
│  - 自下而上抽象，自上而下应用                        │
│  - 生成可复用的认知模式                              │
├─────────────────────────────────────────────────────┤
│  夜间循环 (Nightly Cycle)                            │
│  - 每日回顾和反思                                    │
│  - 知识整合和清理                                    │
│  - 系统健康检查                                      │
├─────────────────────────────────────────────────────┤
│  知识库 (Knowledge Base)                             │
│  - 结构化存储学到的知识                              │
│  - 支持分类和标签                                    │
│  - 与记忆流双向同步                                  │
└─────────────────────────────────────────────────────┘
```

## 功能

- **事件驱动进化** - 基于触发事件自动记录和学习
- **分形思考** - 4 层深度分析，生成元规则
- **夜间循环** - 每日自动回顾和整合
- **记忆管理** - 完整的 CRUD 操作
- **知识提取** - 从经验中提取结构化知识

## 可用工具

### evolve(type, content, metadata=null)

记录进化事件。

**参数：**
- `type` (string, required): 事件类型
  - `TASK_COMPLETED` - 任务完成
  - `KNOWLEDGE_GAINED` - 获得新知识
  - `SKILL_IMPROVED` - 技能提升
  - `PROBLEM_SOLVED` - 问题解决
  - `FEEDBACK_RECEIVED` - 收到反馈
  - `GOAL_UPDATED` - 目标更新
- `content` (string, required): 事件内容
- `metadata` (object, optional): 附加元数据

**示例：**
```
evolve(type="KNOWLEDGE_GAINED", content="学习了 RAG 评估系统")
evolve(type="TASK_COMPLETED", content="完成 memory-search 技能优化", metadata={"duration": "2h"})
```

### fractal(limit=10)

执行分形思考分析。

**参数：**
- `limit` (integer, default=10): 分析最近 N 条记忆

**返回：**
- 4 层分析结果（观察、模式、原则、元规则）
- 生成的新知识和认知模式

**示例：**
```
fractal(limit=20)
```

### nightly()

执行夜间循环。

**功能：**
- 回顾当天的所有记忆
- 生成反思和总结
- 整合知识到知识库
- 清理过期或低质量记忆

**示例：**
```
nightly()
```

### status()

查看系统状态。

**返回：**
- 记忆总数和类型分布
- 知识库条目数
- 进化事件统计
- 系统健康状态

**示例：**
```
status()
```

## 配置

在 `config.yaml` 中配置：

```yaml
workspace: "/path/to/workspace"
agent: "ai-baby"
ollama:
  url: "http://localhost:11434"
  embedding_model: "nomic-embed-text"
memory:
  max_stream_size: 1000
  importance_threshold: 5.0
evolution:
  auto_fractal: true
  auto_nightly: true
  nightly_time: "02:00"
```

## 数据存储

```
data/<agent>/
├── memory_stream.db      # 记忆流数据库
├── knowledge_base.db     # 知识库
├── evolution.db          # 进化事件记录
└── config.yaml           # 配置文件
```

## 使用场景

1. **日常学习记录** - 记录每天学到的新知识
2. **技能提升追踪** - 跟踪技能改进历程
3. **问题解决方法论** - 积累解决问题的模式
4. **目标管理** - 追踪目标进展和更新
5. **反思成长** - 定期回顾和反思

## 分形思考示例

```
Level 1 (观察): "用户多次询问记忆搜索功能"
Level 2 (模式): "用户对记忆检索有持续需求"
Level 3 (原则): "提供多种检索方式提升用户体验"
Level 4 (元规则): "当功能使用频率高时，优先优化该功能的易用性"
```

## 最佳实践

- **及时记录** - 事件发生后立即记录，避免遗忘
- **详细描述** - content 尽量具体，包含上下文
- **定期分形** - 每周执行 1-2 次分形思考
- **夜间循环** - 建议配置定时任务每天执行
- **知识整理** - 定期审查和整理知识库

## 依赖

- **Python 3.9+** - 运行环境
- **SQLite3** - 数据库
- **Ollama** - 语义搜索和 Embedding（可选，强烈推荐）
- **Memory Hub** - 共享记忆库

## 注意事项

- 分形思考需要足够的记忆数据（建议 20+ 条）
- 夜间循环建议在低峰时段执行（如凌晨 2 点）
- 记忆流有大小限制，定期清理过期记忆
- 知识库需要定期整理，避免冗余

## 定时任务配置

```bash
# 每天凌晨 2 点执行夜间循环
0 2 * * * cd /path/to/workspace && python3 skills/self-evolution/main.py nightly

# 每周日凌晨 3 点执行分形思考
0 3 * * 0 cd /path/to/workspace && python3 skills/self-evolution/main.py fractal --limit 50
```

---

_版本：5.0.0 | 更新：2026-03-24_
