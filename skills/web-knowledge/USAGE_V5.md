# Web Knowledge v5.0 - 增强版使用指南

## 🎉 新增功能

### ✅ 完全免费，无需 API Key
- 6 大搜索引擎随意切换
- 自动故障转移
- 智能缓存机制

### ✅ 多引擎支持
| 引擎 | 适用场景 | 语言 |
|------|---------|------|
| **Bing 中国** | 中文搜索（默认） | 中文 |
| **百度** | 中文内容 | 中文 |
| **搜狗** | 微信/公众号内容 | 中文 |
| **DuckDuckGo** | 隐私保护 | 英文 |
| **Bing 国际** | 英文技术文档 | 英文 |
| **Google** | 全球内容 | 多语言 |

### ✅ 深度研究模式
- 多角度搜索（4-8 个不同角度）
- 智能去重
- 综合摘要生成
- 矛盾点检测

### ✅ 结果质量评分
- 标题相关性 (40%)
- 摘要相关性 (30%)
- 时效性 (20%)
- 权威性 (10%)

---

## 🚀 快速开始

### 基础搜索

```bash
# 最简单用法
python3 skills/web-knowledge/search_v5.py "2026 年电商支付方案"

# 指定数量
python3 skills/web-knowledge/search_v5.py "AI agent 框架" --num-results 20

# 详细输出
python3 skills/web-knowledge/search_v5.py "Python 3.13 新特性" --verbose
```

### 指定搜索引擎

```bash
# 使用百度
python3 skills/web-knowledge/search_v5.py "跨境电商合规" --engine baidu

# 使用 Bing 国际
python3 skills/web-knowledge/search_v5.py "machine learning tutorial" --engine bing

# 使用 DuckDuckGo（隐私保护）
python3 skills/web-knowledge/search_v5.py "privacy tools" --engine duckduckgo
```

### 时间范围过滤

```bash
# 只看 2026 年的内容
python3 skills/web-knowledge/search_v5.py "Python 新特性" --date-after 2026-01-01

# 一周内的内容
python3 skills/web-knowledge/search_v5.py "AI 新闻" --date-after $(date -d "7 days ago" +%Y-%m-%d)
```

### 深度研究模式 ⭐

```bash
# 启动深度研究
python3 skills/web-knowledge/search_v5.py "AI agent 框架对比" --deep-research

# 深度研究 + 导出报告
python3 skills/web-knowledge/search_v5.py "跨境电商独立站搭建" --deep-research --export report.md
```

### 导出结果

```bash
# 导出为 Markdown
python3 skills/web-knowledge/search_v5.py "机器学习教程" --export results.md

# 查看导出的文件
cat results.md
```

---

## 📊 深度研究模式详解

### 工作原理

```
用户输入："AI agent 框架对比"
     ↓
Step 1: 生成 4 个搜索角度
  1. AI agent 框架最佳实践
  2. AI agent 框架完整教程
  3. AI agent 框架案例分析
  4. AI agent 框架 2026 年最新趋势
     ↓
Step 2: 每个角度搜索 5 条结果
  → 共收集 20 条结果
     ↓
Step 3: 智能去重
  → 去除重复 URL 和相似标题
  → 剩余 15 条独特结果
     ↓
Step 4: 生成综合摘要
  - 执行摘要
  - 关键点提取
  - 来源整理
     ↓
Step 5: 输出完整报告
```

### 输出示例

```
🔬 深度研究报告
======================================================================
主题：AI agent 框架对比
时间：2026-04-06T09:59:00
搜索角度：4 个
总结果：20 条 → 去重后：15 条
======================================================================

📝 综合摘要:
关于"AI agent 框架对比"的搜索共找到 15 条相关结果。
以下是 10 个关键发现：

关键点:
  1. LangGraph 提供状态化 Agent 编排...
  2. AutoGen 支持多 Agent 对话...
  3. CrewAI 专注于角色分工...
  ...

📊 Top 结果:
  [1] LangChain vs AutoGen vs CrewAI 全面对比 (评分：85.0)
  [2] 2026 年最佳 AI Agent 框架评测 (评分：82.5)
  ...
```

---

## 💡 高级技巧

### 1. 组合使用

```bash
# 深度研究 + 指定引擎 + 导出
python3 skills/web-knowledge/search_v5.py \
  "RAG 系统架构设计" \
  --deep-research \
  --engine bing \
  --export rag-architecture.md
```

### 2. 禁用缓存（获取最新结果）

```bash
python3 skills/web-knowledge/search_v5.py "今日 AI 新闻" --no-cache
```

### 3. 批量搜索

```bash
# 创建搜索列表
cat > queries.txt << EOF
AI agent 框架
RAG 系统优化
LLM 微调技术
EOF

# 批量执行
while read query; do
    python3 skills/web-knowledge/search_v5.py "$query" --export "${query// /_}.md"
done < queries.txt
```

---

## 🔧 性能优化

### 缓存机制
- 默认启用 1 小时缓存
- 相同查询直接返回缓存
- 节省时间和带宽

### 智能超时
- 基础超时：10 秒
- 指数退避：10s → 20s → 40s
- 最大超时：60 秒

### 健康监控
- 自动标记失败引擎
- 5 分钟内失败 3 次 → 暂时停用
- 成功后自动恢复

---

## 📋 完整参数说明

```bash
usage: search_v5.py [-h] [--engine {bing,bing-cn,baidu,google,duckduckgo,sogou}]
                    [--num-results NUM_RESULTS] [--date-after DATE_AFTER]
                    [--date-before DATE_BEFORE] [--deep-research]
                    [--export EXPORT] [--no-cache] [--verbose]
                    query

必选参数:
  query                 搜索关键词

可选参数:
  -h, --help           显示帮助信息
  --engine, -e         指定搜索引擎
  --num-results, -n    返回结果数量 (默认：10)
  --date-after         日期之后 (YYYY-MM-DD)
  --date-before        日期之前 (YYYY-MM-DD)
  --deep-research      深度研究模式
  --export, -o         导出到文件
  --no-cache           禁用缓存
  --verbose, -v        详细输出
```

---

## 🆚 与旧版对比

| 功能 | 旧版 (v4) | 新版 (v5) | 提升 |
|------|----------|----------|------|
| **搜索引擎** | 4 个 | **6 个** | +50% |
| **深度研究** | ❌ | ✅ | 从 0 到 1 |
| **质量评分** | ❌ | ✅ | 智能化 |
| **缓存** | 简单 | **智能 TTL** | 更高效 |
| **超时处理** | 固定 | **指数退避** | 更稳定 |
| **导出格式** | 纯文本 | **Markdown** | 更美观 |

---

## 🎯 最佳实践

### ✅ 推荐用法

```bash
# 日常搜索 - 用默认设置
python3 skills/web-knowledge/search_v5.py "问题描述"

# 重要研究 - 用深度模式
python3 skills/web-knowledge/search_v5.py "研究主题" --deep-research

# 最新信息 - 禁用缓存
python3 skills/web-knowledge/search_v5.py "今日新闻" --no-cache

# 技术资料 - 用英文引擎
python3 skills/web-knowledge/search_v5.py "technical topic" --engine bing
```

### ❌ 避免的错误

```bash
# ❌ 每次都禁用缓存（慢）
python3 search.py "常见问题" --no-cache  # 没必要！

# ✅ 只在需要最新信息时禁用
python3 search.py "突发新闻" --no-cache  # 合适！

# ❌ 一次搜索几百条结果
python3 search.py "topic" -n 500  # 太多！

# ✅ 合理数量
python3 search.py "topic" -n 10-20  # 合适！
```

---

## 🔮 未来计划

### v5.1 (计划中)
- [ ] 日期解析和精确过滤
- [ ] 矛盾点自动检测
- [ ] 知识空白识别

### v5.2 (计划中)
- [ ] 网页全文抓取
- [ ] HTML → Markdown 转换
- [ ] 图片搜索支持

### v6.0 (愿景)
- [ ] 多语言自动翻译
- [ ] 跨语言搜索
- [ ] AI 驱动的智能摘要

---

## 💬 常见问题

### Q: 为什么有些引擎搜索结果少？
A: 某些引擎（如 Google）有反爬虫机制，可能返回较少结果。建议切换到 Bing 或百度。

### Q: 深度研究为什么这么慢？
A: 深度研究会执行 4-8 次搜索，所以时间是普通的 4-8 倍。建议用于重要研究场景。

### Q: 缓存存在哪里？
A: `~/.openclaw/workspace/.cache/web-search/`，自动清理过期缓存。

### Q: 如何贡献新引擎？
A: 在 `engines` 字典中添加新引擎，实现对应的解析器即可。

---

_版本：v5.0 (完全免费版)_  
_更新时间：2026-04-06_  
_特点：无需 API Key · 多引擎支持 · 深度研究模式_
