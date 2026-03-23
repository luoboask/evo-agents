---
name: web_search
description: 网页搜索技能，基于 Bing 搜索
homepage: https://github.com/your-org/evo-agents
metadata:
  emoji: "🌐"
  category: search
  version: "1.0.0"
  updated_at: "2026-03-23"
---

# 网页搜索技能

网页搜索技能提供互联网搜索功能，基于 Bing 搜索 API，无需 API key。

## 功能

- **网页搜索** - 搜索互联网获取最新信息
- **内容提取** - 自动提取网页可读内容
- **时间过滤** - 按时间范围筛选结果
- **区域搜索** - 支持特定区域和语言

## 可用工具

### web_search(query, count=10, freshness=null, country="US", language="en")

搜索互联网。

**参数：**
- `query` (string, required): 搜索关键词
- `count` (integer, default=10): 返回结果数量 (1-10)
- `freshness` (string, optional): 时间过滤
  - `day` - 过去 24 小时
  - `week` - 过去一周
  - `month` - 过去一月
  - `year` - 过去一年
- `country` (string, default="US"): 国家代码 (2 字母)
- `language` (string, default="en"): 语言代码

**返回：**
- 搜索结果列表（标题、URL、摘要）
- 总结果数
- 搜索时间

**示例：**
```
web_search(query="RAG 优化方法", count=10, freshness="week")
web_search(query="AI Agent 架构", country="CN", language="zh")
```

### web_fetch(url, extract_mode="markdown", max_chars=10000)

提取网页内容。

**参数：**
- `url` (string, required): 网页 URL
- `extract_mode` (string, default="markdown"): 提取模式 (markdown/text)
- `max_chars` (integer, default=10000): 最大字符数

**返回：**
- 网页标题
- 提取的内容
- 元数据

**示例：**
```
web_fetch(url="https://example.com/article", extract_mode="markdown")
```

## 搜索技巧

### 高级搜索语法

- **精确匹配**: `"exact phrase"`
- **排除词**: `query -exclude`
- **站内搜索**: `site:example.com query`
- **文件类型**: `query filetype:pdf`
- **标题搜索**: `intitle:query`

### 时间过滤

- **最新信息**: `freshness="day"`
- **本周内容**: `freshness="week"`
- **月度回顾**: `freshness="month"`

### 区域搜索

- **中国**: `country="CN"`
- **美国**: `country="US"`
- **全球**: `country="ALL"`

## 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "websearch": {
        "enabled": true,
        "env": {
          "SEARCH_TIMEOUT": "10",
          "MAX_RESULTS": "10"
        }
      }
    }
  }
}
```

## 使用场景

1. **信息检索** - 查找最新技术文档
2. **竞品分析** - 搜索竞品信息
3. **学习研究** - 查找教程和资料
4. **新闻追踪** - 关注最新动态

## 最佳实践

- **精确查询** - 使用具体关键词
- **时间过滤** - 需要最新信息时使用 freshness
- **结果验证** - 交叉验证多个来源
- **适度使用** - 避免频繁搜索

## 注意事项

- 搜索频率过高可能被限制
- 某些网站可能无法访问
- 搜索结果可能包含广告
- 注意隐私和数据安全

## 限制

- 每次搜索最多返回 10 个结果
- 不支持图片搜索
- 不支持视频搜索
- 部分网站可能无法提取内容
