# 🎯 OpenClaw 核心技能完整使用指南

> 更新时间：2026-04-06  
> 包含技能：Harness Agent | Session-Report | Memory-Search | Web-Knowledge | Self-Evolution

---

## 📚 技能总览

| 技能 | 定位 | 触发方式 | 核心价值 |
|------|------|---------|---------|
| **Harness Agent** | 复杂任务执行 | 手动调用 | 完成大型项目 |
| **Session-Report** | 记忆写入 | 手动调用 | 保存重要经验 |
| **Memory-Search** | 记忆检索 | 自动 + 手动 | 避免重复讨论 |
| **Web-Knowledge** | 网络搜索 | 自动 + 手动 | 获取实时信息 |
| **Self-Evolution** | 进化分析 | 定期自动 | 持续优化行为 |

---

## 1️⃣ Harness Agent - 复杂任务执行

### 🎯 何时使用

- ✅ 开发完整系统（电商网站、CRM、博客平台）
- ✅ 大型重构项目（微服务迁移、代码库重组）
- ✅ 跨领域复杂任务（需要多专家协作）
- ❌ 简单任务（写个函数、查个 API）→ 直接用普通对话

### 🚀 快速开始

```bash
# 最简单用法 - 自动检测领域
/harness-agent "开发一个待办事项 APP，支持添加/删除/标记完成"

# 指定领域
/harness-agent "策划双十一营销活动" --domain marketing

# 并行执行（加快速度）
/harness-agent "开发电商网站" --parallelism 4

# 预览模式（先看计划，不执行）
/harness-agent "重构支付模块" --dry-run
```

### 📋 完整参数

```bash
/harness-agent "任务描述" \
  --domain <领域> \           # programming/marketing/legal/data-analysis...
  --parallelism <数量> \      # 并行子任务数（默认：根据 CPU）
  --timeout <秒数> \          # 超时时间（默认：7200 秒=2 小时）
  --dry-run \                 # 只生成计划，不执行
  --export-design \           # 导出设计方案为 Markdown
  --verbose                   # 详细输出
```

### 💡 使用示例

```bash
# 示例 1: 编程任务
/harness-agent "开发一个博客系统，支持文章发布、评论、标签分类" \
  --domain programming \
  --parallelism 3

# 示例 2: 数据分析
/harness-agent "分析 Q1 销售数据，找出下滑原因并提出改进建议" \
  --domain data-analysis \
  --enable-memory-search

# 示例 3: 营销策划
/harness-agent "策划新产品发布会，预算 10 万，目标覆盖 50 万人" \
  --domain marketing \
  --parallelism 4
```

### 📁 交付物

每次 Harness 任务完成后会生成：
- `.harness/progress.md` - 进度追踪文件
- `.harness/deliverables/` - 最终交付物（代码/文档/报告）

---

## 2️⃣ Session-Report - 保存重要记忆

### 🎯 何时使用

- ✅ 完成重要任务后（项目上线、架构决策）
- ✅ 了解用户偏好后（沟通风格、技术偏好）
- ✅ 发现新知识点后（外部资源、工具推荐）
- ❌ 日常简单问答 → 不需要每次都运行

### 🚀 快速开始

```bash
# 基础用法 - 预览并确认
/session-report

# 只预览，不保存
/session-report --dry-run

# 只保存特定类型
/session-report --type user        # 只保存用户偏好
/session-report --type feedback    # 只保存反馈记忆
/session-report --type project     # 只保存项目决策
/session-report --type reference   # 只保存外部资源
```

### 📋 完整参数

```bash
/session-report \
  --dry-run \                # 只预览，不保存
  --force \                  # 强制保存（跳过确认）
  --type <类型> \            # user/feedback/project/reference
  --limit <数量> \           # 只回顾最近 N 条消息
  --export <文件>            # 导出为 Markdown 文件
```

### 💡 使用示例

```bash
# 示例 1: 项目完成后总结
# [完成电商项目开发后]
/session-report --type project

# 示例 2: 了解用户偏好后
# [用户说"我不喜欢冗长回复，直接给代码"]
/session-report --type feedback

# 示例 3: 获取外部资源后
# [用户分享"监控在 grafana.internal/d/api-latency"]
/session-report --type reference

# 示例 4: 先预览再决定
/session-report --dry-run
# 查看预览后，如果满意：
/session-report
```

### 📝 保存的内容示例

```markdown
# 保存到 MEMORY.md

## User Memory（用户记忆）
- 用户偏好 TypeScript 而非 JavaScript
- 用户是数据科学家，专注于可观测性领域

## Feedback Memory（反馈记忆）
- 用户偏好简洁回复，不要结尾总结
  Why: 用户能看懂代码，不需要额外解释
  How to apply: 直接给代码，省略总结段落

## Project Memory（项目记忆）
- 电商项目选择 Redis+JWT 方案，因为高 QPS 需求
  Why: 性能要求
  How to apply: 新 API 都应该加缓存层

## Reference Memory（参考记忆）
- Grafana dashboard: grafana.internal/d/api-latency
  用途：监控 API 延迟和错误率
```

---

## 3️⃣ Memory-Search - 检索历史记忆

### 🎯 何时使用

- ✅ **自动触发** - 每次对话前自动检索相关记忆
- ✅ 手动查询 - "我之前说过喜欢什么？"
- ❌ 不需要手动调用 - 默认自动工作

### 🚀 使用方式

#### 方式 A: 自动检索（默认）

```python
# 无需手动调用，每次对话前自动执行
# AI 会自动：
# 1. 提取当前对话的关键词
# 2. 检索 MEMORY.md 中的相关记忆
# 3. 将相关记忆注入上下文
```

#### 方式 B: 手动查询

```bash
# 通过 Python 脚本查询
python3 skills/memory-search/search.py "用户偏好"

# 或在对话中直接问
"我之前说过关于 TypeScript 的内容吗？"
→ AI 自动调用 memory-search
```

### 💡 典型场景

```
场景 1: 避免重复讨论
用户："帮我写个函数"
AI: [自动检索到"用户偏好简洁回复"]
→ 直接给代码，不废话

场景 2: 延续之前的决策
用户："库存管理怎么做？"
AI: [检索到"4 月 15 日决定用 Redis 缓存"]
→ "基于上次的决策，继续使用 Redis 方案..."

场景 3: 个性化服务
用户："我是新来的，介绍一下项目"
AI: [检索到"用户是数据科学家"]
→ 用数据分析相关的类比来解释
```

---

## 4️⃣ Web-Knowledge - 网络知识获取

### 🎯 何时使用

- ✅ 需要最新信息（技术趋势、新闻动态）
- ✅ 训练数据截止后的内容（2026 年的信息）
- ✅ 实时数据（股价、天气、比赛结果）
- ❌ 历史知识、经典理论 → 直接用模型知识

### 🚀 快速开始

```bash
# 基础搜索
python3 skills/web-knowledge/search.py "2026 年电商支付方案"

# 限制结果数量
python3 skills/web-knowledge/search.py "AI 新闻" --limit 3

# 深度研究模式（多角度搜索）
python3 -c "
from search import deep_research
report = deep_research('AI agent 框架对比', num_angles=4, verbose=True)
"

# 导出为 Markdown
python3 -c "
from search import deep_research, export_to_markdown
report = deep_research('RAG 系统优化')
export_to_markdown(report, 'rag-report.md')
"
```

### 📋 完整参数

```bash
python3 skills/web-knowledge/search.py "关键词" \
  --limit <数量> \           # 返回结果数（默认：10）
  --json \                   # 输出 JSON 格式
  --engine <引擎> \          # bing/baidu/google/duckduckgo
  --verbose                  # 详细输出
```

### 💡 使用示例

```bash
# 示例 1: 获取最新技术
python3 skills/web-knowledge/search.py "Python 3.13 新特性"

# 示例 2: 市场调研
python3 skills/web-knowledge/search.py "2026 年跨境电商趋势"

# 示例 3: 竞品分析
python3 skills/web-knowledge/search.py "Notion vs Obsidian vs Logseq"

# 示例 4: 深度研究
python3 -c "
from search import deep_research
report = deep_research('微服务架构最佳实践', num_angles=4)
print(report['summary']['executive_summary'])
"
```

### 🔗 与 Harness 配合

```bash
# Harness 执行中自动调用 web-knowledge
/harness-agent "开发电商网站" \
  --domain programming \
  --enable-web-research  # 自动搜索最新技术栈
```

---

## 5️⃣ Self-Evolution - 定期进化分析

### 🎯 何时使用

- ✅ **自动触发** - 每周/每月自动运行
- ✅ 查看报告 - 了解自己的成长轨迹
- ❌ 不需要手动调用 - 后台自动工作

### 📊 报告内容

```markdown
# Self-Evolution 周报

## 本周概览
- 总会话：142 次
- Harness 任务：5 个
- 保存记忆：18 条

## 发现的模式
✅ 成功模式:
- 使用 Harness 的项目提前完成
- 简洁回复获得更高满意度

⚠️ 待改进:
- 晚上 20:00-22:00 最活跃
- 建议在黄金时段减少等待时间

## 优化建议
1. 继续保持 Harness 工作流程
2. 默认开启简洁回复模式
3. 在黄金时段预加载常用工具
```

### 🚀 查看报告

```bash
# 查看最新周报
cat skills/self-evolution/reports/weekly_2026-W14.md

# 查看月报
cat skills/self-evolution/reports/monthly_2026-04.md

# 查看所有报告
ls -la skills/self-evolution/reports/
```

### 💡 应用建议

```bash
# 每周一花 5 分钟查看周报
cat skills/self-evolution/reports/weekly_$(date +%Y-W%V).md

# 根据建议调整工作方式
# 例如：报告说"简洁回复更好" → 以后对话更简洁
```

---

## 🔄 技能协同工作流

### 完整案例：开发电商网站

```bash
# Day 1: 项目启动
/harness-agent "开发电商网站" --domain programming
# → 执行复杂任务

/session-report --type project
# → 保存项目决策到记忆

# Day 3: 继续开发
用户："帮我写个用户认证 API"
# → memory-search 自动检索到"用户偏好简洁"
# → AI 直接给代码，不废话

# Day 7: 需要了解最新技术
用户："支付集成选哪个方案？"
# → web-knowledge 自动搜索"2026 年支付方案对比"
# → 获取最新信息

# Day 14: 中期检查
# → self-evolution 自动运行周报
# → 发现"使用 Harness 的项目进度更快"
# → 建议：继续使用 Harness

# Day 30: 项目上线
/session-report --type project --type feedback
# → 保存成功经验到记忆

# Day 35: 月度回顾
# → self-evolution 生成月报
# → 总结整个项目的经验和教训
```

---

## 📋 最佳实践清单

### ✅ 推荐做法

1. **复杂任务用 Harness**
   ```bash
   # ✅ 正确
   /harness-agent "开发完整系统"
   
   # ❌ 错误
   "帮我写个大系统"  # 没有用 Harness
   ```

2. **重要讨论后用 Session-Report**
   ```bash
   # ✅ 正确
   [完成架构讨论后]
   /session-report --type project
   
   # ❌ 错误
   [简单问答后]
   /session-report  # 没必要
   ```

3. **让 Memory-Search 自动工作**
   ```bash
   # ✅ 正确 - 无需手动调用
   # 每次对话自动检索记忆
   
   # ❌ 错误
   # 每次都手动 query memory
   ```

4. **需要最新信息用 Web-Knowledge**
   ```bash
   # ✅ 正确
   python3 search.py "2026 年最新技术"
   
   # ❌ 错误
   # 问模型 2026 年的新闻（模型不知道）
   ```

5. **定期查看 Self-Evolution 报告**
   ```bash
   # ✅ 正确
   每周花 5 分钟看周报，调整工作方式
   
   # ❌ 错误
   # 从不查看进化报告
   ```

---

## 🎯 快速参考卡片

```bash
# ========== Harness Agent ==========
/harness-agent "任务"                    # 基础用法
/harness-agent "任务" --domain xxx       # 指定领域
/harness-agent "任务" --parallelism 4    # 并行执行
/harness-agent "任务" --dry-run          # 只预览

# ========== Session-Report ==========
/session-report                          # 预览并确认
/session-report --dry-run                # 只预览
/session-report --type project           # 只保存项目记忆
/session-report --force                  # 强制保存

# ========== Memory-Search ==========
# 自动工作，无需手动调用
# 或在对话中问："我之前说过..."

# ========== Web-Knowledge ==========
python3 search.py "关键词"               # 基础搜索
python3 search.py "关键词" --limit 3     # 限制数量
python3 -c "from search import deep_research; deep_research('主题')"  # 深度研究

# ========== Self-Evolution ==========
cat skills/self-evolution/reports/weekly_*.md  # 查看周报
cat skills/self-evolution/reports/monthly_*.md # 查看月报
```

---

## ❓ 常见问题

### Q: 什么时候用 Harness，什么时候直接对话？

**A**: 
- **Harness**: 开发完整系统、大型重构、跨领域复杂任务
- **直接对话**: 写个函数、查个 API、简单咨询

**判断标准**: 任务是否超过 1 小时？是否需要多个步骤？如果是 → 用 Harness

---

### Q: Session-Report 会不会保存太多垃圾记忆？

**A**: 不会！三层过滤机制：
1. 临时 vs 长期 → 丢弃临时状态
2. 私人 vs 共享 → 正确分类
3. 可推导 vs 不可推导 → 丢弃可推导内容

实际保存率 < 5%，都是精华。

---

### Q: Memory-Search 会影响对话速度吗？

**A**: 几乎不影响。检索在毫秒级完成，而且只在必要时检索。

---

### Q: Web-Knowledge 需要 API Key 吗？

**A**: 不需要！完全免费，使用 Bing/百度等公开搜索引擎。

---

### Q: Self-Evolution 多久运行一次？

**A**: 
- 周报：每周五凌晨 2 点
- 月报：每月 1 号凌晨 3 点
- 通过 cron 自动触发

---

## 📚 相关文档

- Harness Agent 详细文档：`skills/harness-agent/SKILL.md`
- Session-Report 详细文档：`skills/session-report/SKILL.md`
- Memory-Search 详细文档：`skills/memory-search/README.md`
- Web-Knowledge 详细文档：`skills/web-knowledge/README.md`
- Self-Evolution 详细文档：`skills/self-evolution/README.md`

---

_最后更新：2026-04-06_  
_版本：v1.0_  
_维护者：evo-agents 团队_
