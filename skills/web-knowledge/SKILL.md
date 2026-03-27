---
name: web-knowledge
description: 'Web search and knowledge crawling. Multi-engine search + page content extraction. No API key required.'
---

# Web Knowledge Skill

智能网络知识获取技能（搜索 + 爬取）。

## Features

### 🔍 搜索引擎
- ✅ **多引擎支持** - Bing、百度、Google、DuckDuckGo
- ✅ **智能引擎选择** - 自动选择最佳搜索引擎
- ✅ **健康监控** - 实时监控引擎状态
- ✅ **自动切换** - 引擎故障时自动切换备选
- ✅ **自适应超时** - 基于历史表现动态调整
- ✅ **指数退避重试** - 失败时智能重试

### 🕷️ 网页爬取
- ✅ **单页爬取** - 给定 URL，提取正文、标题、作者、日期等
- ✅ **批量爬取** - 支持多个 URL 并行/串行爬取
- ✅ **智能解析** - 识别文章/文档/产品页/列表页
- ✅ **内容清洗** - 去除广告、导航、无关元素
- ✅ **多格式输出** - Markdown/JSON/纯文本

## Usage

### 搜索功能

```bash
# 基本搜索（自动选择最佳引擎）
python3 skills/web-knowledge/search.py "your search query"

# 限制结果数量
python3 skills/web-knowledge/search.py "your search query" --limit 3

# JSON 输出
python3 skills/web-knowledge/search.py "your search query" --json

# 指定最大重试次数
python3 skills/web-knowledge/search.py "your search query" --max-retries 5
```

### 爬取功能

```bash
# 爬取单个网页（Markdown 输出）
python3 skills/web-knowledge/crawl.py "https://example.com/article"

# 爬取单个网页（JSON 输出）
python3 skills/web-knowledge/crawl.py "https://example.com/article" --output json

# 爬取单个网页（纯文本输出）
python3 skills/web-knowledge/crawl.py "https://example.com/article" --output text

# 批量爬取（从文件读取 URL 列表）
python3 skills/web-knowledge/crawl.py --urls urls.txt

# 批量爬取（指定并发数）
python3 skills/web-knowledge/crawl.py --urls urls.txt --workers 5

# 批量爬取（调整超时）
python3 skills/web-knowledge/crawl.py --urls urls.txt --timeout 60
```

### URL 列表文件格式

```text
# urls.txt - 每行一个 URL，# 开头为注释
https://example.com/article1
https://example.com/article2
https://example.com/article3
```

## Examples

### 搜索示例

```bash
# 搜索技术问题
python3 skills/web-knowledge/search.py "Python async await 最佳实践"

# 搜索最新新闻
python3 skills/web-knowledge/search.py "2026 AI 最新进展" --limit 10

# 搜索并导出 JSON
python3 skills/web-knowledge/search.py "OpenClaw documentation" --json > results.json
```

### 爬取示例

```bash
# 爬取技术文章
python3 skills/web-knowledge/crawl.py "https://medium.com/article/python-tips"

# 爬取并保存为 Markdown
python3 skills/web-knowledge/crawl.py "https://example.com/blog/post" --output markdown > article.md

# 批量爬取研究论文
python3 skills/web-knowledge/crawl.py --urls papers.txt --output json --workers 3 > papers.json

# 爬取并调整超时（慢速网站）
python3 skills/web-knowledge/crawl.py "https://slow-site.com/article" --timeout 60
```

## Output Format

### 搜索输出（默认）

```
🔍 Search results for: Python async await

1. Python Async/Await 完全指南
   https://example.com/guide
   详细介绍 Python 异步编程的核心概念...

2. 异步编程最佳实践
   https://example.com/best-practices
   总结实际项目中的异步编程经验...
```

### 爬取输出（Markdown）

```markdown
# 文章标题

**URL:** https://example.com/article
**作者:** 作者名
**日期:** 2026-03-27
**站点:** 站点名称

---

文章正文内容段落 1...

文章正文内容段落 2...
```

### 爬取输出（JSON）

```json
{
  "success": true,
  "url": "https://example.com/article",
  "page_type": "article",
  "type_scores": {
    "article": 5,
    "document": 1,
    "product": 0,
    "list": 0
  },
  "metadata": {
    "title": "文章标题",
    "author": "作者名",
    "publish_date": "2026-03-27",
    "site_name": "站点名称",
    "description": "文章描述",
    "language": "zh"
  },
  "content": ["段落 1...", "段落 2..."],
  "content_length": 1234,
  "duration": 2.5,
  "timestamp": "2026-03-27T10:00:00"
}
```

## Page Type Detection

爬虫会自动识别页面类型：

| 类型 | 特征 | 用途 |
|------|------|------|
| article | 文章/博客，有作者、日期 | 新闻、博客、教程 |
| document | 技术文档、API 文档 | 官方文档、手册 |
| product | 产品页面，有价格、购买按钮 | 电商、产品介绍 |
| list | 列表页、首页、分页 | 索引、目录 |
| general | 通用页面，无明显特征 | 其他类型 |

## Evolution History

- **v1**: Basic Bing search
- **v2**: Added retry mechanism and fallback
- **v3**: Smart engine selection, health monitoring, adaptive timeout
- **v4**: 指数退避重试、错误分类、健康监控优化
- **v5**: 新增百度/Google 搜索引擎
- **v6**: 新增网页内容爬取功能（crawl.py）

## Tips

1. **中文搜索优先百度** - 百度对中文内容覆盖更全（中国大陆可用）
2. **技术搜索优先 Google** - Google 技术资源更丰富（需要科学上网）
3. **Bing 最稳定** - 全球可用，反爬较低，默认首选
4. **DuckDuckGo** - 隐私保护，但国内无法访问
5. **批量爬取控制并发** - 默认 3 线程，避免目标网站压力过大
6. **慢速网站调整超时** - 使用 `--timeout 60` 应对慢速网站
7. **爬取结果缓存** - 爬取内容会自动缓存到 `memory/web_cache/`

## Limitations

- ❌ 不支持需要登录的网站
- ❌ 不支持重度 JS 渲染的网站（需要 Playwright）
- ❌ 不支持需要交互的网站
- ❌ 反爬严格的网站可能失败
- ⚠️ 百度/Google 有反爬，可能自动降级到 Bing
- ⚠️ DuckDuckGo 在中国大陆无法访问

## Troubleshooting

### 搜索失败
```bash
# 检查网络连接
curl -I https://www.bing.com

# 手动指定引擎
python3 skills/web-knowledge/search.py "query" --engine baidu
```

### 爬取失败
```bash
# 增加超时
python3 skills/web-knowledge/crawl.py "url" --timeout 60

# 检查 URL 是否可访问
curl -I "https://example.com"
```

### 内容为空
- 可能是 JS 渲染页面，需要 Playwright
- 可能是反爬机制，尝试更换 User-Agent
- 可能是页面结构特殊，需要自定义解析
