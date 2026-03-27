# Web Knowledge - 网络知识获取技能

## 快速开始

### 1. 搜索

```bash
# 搜索任意问题
python3 skills/web-knowledge/search.py "Python 异步编程教程"

# 限制结果数量
python3 skills/web-knowledge/search.py "AI 新闻" --limit 3

# 导出 JSON
python3 skills/web-knowledge/search.py "OpenClaw" --json > results.json
```

### 2. 爬取网页内容

```bash
# 爬取单页
python3 skills/web-knowledge/crawl.py "https://example.com/article"

# 爬取并保存为 Markdown
python3 skills/web-knowledge/crawl.py "https://example.com/article" --output markdown > article.md

# 爬取并保存为 JSON（结构化数据）
python3 skills/web-knowledge/crawl.py "https://example.com/article" --output json > article.json
```

### 3. 批量爬取

创建 `urls.txt` 文件：
```text
https://example.com/article1
https://example.com/article2
https://example.com/article3
```

执行批量爬取：
```bash
# 默认 3 线程并行
python3 skills/web-knowledge/crawl.py --urls urls.txt

# 指定 5 线程
python3 skills/web-knowledge/crawl.py --urls urls.txt --workers 5

# 导出 JSON
python3 skills/web-knowledge/crawl.py --urls urls.txt --output json > all_articles.json
```

## 搜索引擎

自动选择最佳引擎，智能降级：

| 引擎 | 适用场景 | 可用性 |
|------|----------|--------|
| Bing | 通用搜索，英文内容 | ✅ 全球可用（首选） |
| 百度 | 中文内容优先 | ⚠️ 中国大陆，有反爬 |
| Google | 技术资源、学术内容 | ⚠️ 需要科学上网 |
| DuckDuckGo | 隐私保护搜索 | ⚠️ 国内无法访问 |

**引擎优先级：** Bing > 百度 > Google > DuckDuckGo

当某个引擎失败时，会自动切换到下一个可用引擎。

## 输出格式

| 格式 | 用途 |
|------|------|
| markdown | 阅读、存入记忆 |
| json | 程序处理、结构化存储 |
| text | 纯文本、精简版 |

## 典型工作流

### 研究某个主题

```bash
# 1. 先搜索相关资源
python3 skills/web-knowledge/search.py "Python async 最佳实践" --limit 10

# 2. 筛选有价值的 URL，创建 urls.txt

# 3. 批量爬取内容
python3 skills/web-knowledge/crawl.py --urls urls.txt --output markdown > research.md
```

### 监控特定网站

```bash
# 1. 创建监控列表
echo "https://example.com/blog" > monitor.txt
echo "https://example.com/news" >> monitor.txt

# 2. 定期爬取（配合 cron）
python3 skills/web-knowledge/crawl.py --urls monitor.txt --output json > $(date +%Y%m%d).json
```

## 性能调优

```bash
# 慢速网站 - 增加超时
python3 skills/web-knowledge/crawl.py "url" --timeout 60

# 大批量 - 增加并发（注意目标网站负载）
python3 skills/web-knowledge/crawl.py --urls urls.txt --workers 10

# 快速测试 - 减少结果数
python3 skills/web-knowledge/search.py "query" --limit 3
```
