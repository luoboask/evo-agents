# 搜索 API 返回格式修复

## 📅 修复时间
**2026-04-08 22:34 GMT+8**

---

## 🐛 问题描述

### 修复前的问题

**错误的返回格式**:
```json
{
  "url": "https://www.zhihu.com/question/342734988",
  "title": "zhihu.comhttps://www.zhihu.com › question",
  "snippet": "..."
}
```

**问题表现**:
- 标题包含域名前缀：`zhihu.com`
- 标题包含 URL：`https://www.zhihu.com`
- 标题包含多余符号：`› question`

**影响**:
- 知识图谱构建时实体名称错误
- 搜索结果展示不友好
- 后续处理需要额外的清洗步骤

---

## ✅ 修复方案

### 1. Bing 搜索结果解析改进

**文件**: `skills/web-knowledge/search.py`  
**方法**: `_parse_results` (第 422-467 行)

**修改内容**:

```python
# 修复前
title_pattern = r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
title_match = re.search(title_pattern, match, re.DOTALL | re.IGNORECASE)
if title_match:
    result['url'] = title_match.group(1)
    title = re.sub(r'<[^>]+>', '', title_match.group(2))
    result['title'] = title.strip()

# 修复后
# 优先匹配 h2/h3 标签中的链接
title_pattern = r'<h[23][^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?</h[23]>'
title_match = re.search(title_pattern, match, re.DOTALL | re.IGNORECASE)

if not title_match:
    # 回退：直接匹配链接
    title_pattern = r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    title_match = re.search(title_pattern, match, re.DOTALL | re.IGNORECASE)

if title_match:
    url = title_match.group(1)
    # 过滤非结果链接
    if url.startswith('/search') or url.startswith('#') or 'bing.com' in url.lower():
        continue
    result['url'] = url
    title = re.sub(r'<[^>]+>', '', title_match.group(2))
    # 清理标题（移除域名前缀和多余内容）
    title = re.sub(r'^[a-z0-9.-]+\s*', '', title)  # 移除开头的域名
    title = re.sub(r'\s*›\s*.*$', '', title)  # 移除 › 后面的内容
    result['title'] = title.strip()
```

**改进点**:
1. ✅ 优先匹配 `<h2>/<h3>` 标签中的链接（更精确）
2. ✅ 添加回退机制（兼容性更好）
3. ✅ 过滤非结果链接
4. ✅ 清理域名前缀：`re.sub(r'^[a-z0-9.-]+\s*', '', title)`
5. ✅ 清理多余内容：`re.sub(r'\s*›\s*.*$', '', title)`
6. ✅ 添加结果质量验证：标题长度必须 > 5 字符

---

### 2. Google 搜索结果解析改进

**文件**: `skills/web-knowledge/search.py`  
**方法**: `_parse_google_results` (第 330-380 行)

**修改内容**:

```python
# 修复前
title_pattern = r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
title_match = re.search(title_pattern, container, re.DOTALL | re.IGNORECASE)
if title_match:
    result['url'] = title_match.group(1)
    title = re.sub(r'<[^>]+>', '', title_match.group(2))
    result['title'] = title.strip()

# 修复后
# 优先匹配 h3 标签中的链接
title_pattern = r'<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?</h3>'
title_match = re.search(title_pattern, container, re.DOTALL | re.IGNORECASE)

if not title_match:
    # 回退：直接匹配链接
    title_pattern = r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    title_match = re.search(title_pattern, container, re.DOTALL | re.IGNORECASE)

if title_match:
    url = title_match.group(1)
    # 过滤非结果链接
    if url.startswith('/search') or url.startswith('#') or 'google' in url.lower():
        continue
    result['url'] = url
    title = re.sub(r'<[^>]+>', '', title_match.group(2))
    # 清理标题（移除域名前缀和多余内容）
    title = re.sub(r'^[a-z0-9.-]+\s*', '', title)  # 移除开头的域名
    title = re.sub(r'\s*›\s*.*$', '', title)  # 移除 › 后面的内容
    result['title'] = title.strip()
```

**改进点**: 与 Bing 搜索相同

---

## 📊 修复效果对比

### 修复前

```json
{
  "url": "https://www.zhihu.com/question/342734988",
  "title": "zhihu.comhttps://www.zhihu.com › question",
  "snippet": "..."
}
```

### 修复后

```json
{
  "url": "https://www.zhihu.com/question/342734988",
  "title": "知识图谱是什么，该如何建立？ - 知乎",
  "snippet": "在新的行业落地图谱应用时，为了节省图谱 schema 构建的时间和人力成本..."
}
```

---

## 🧪 测试验证

### 测试命令

```bash
cd /Users/dhr/cursor/evo-agents
python3 skills/web-knowledge/search.py "知识图谱构建" --limit 3
```

### 测试结果

```
🔍 Search results for: 知识图谱构建

1. 知识图谱是什么，该如何建立？ - 知乎
   https://www.zhihu.com/question/342734988
   在新的行业落地图谱应用时，为了节省图谱 schema 构建的时间和人力成本...

2. 如何从零开始构建一个知识图谱？ - 知乎
   https://www.zhihu.com/question/340558298
   2020 年 11 月 16 日  1、明确知识图谱的应用场景与需求；2、收集、整理知识...

3. 知识图谱的构建流程？ - 知乎
   https://www.zhihu.com/question/299907037
   知识图谱最重要的是，正确的根据业务需求定义问题，确定图结构与实体关系粒度...
```

✅ **标题格式正确，无多余内容！**

---

## 📁 已修改的文件

| 文件 | 修改内容 | 行数变化 |
|------|---------|---------|
| `skills/web-knowledge/search.py` | 修复 Bing 和 Google 搜索结果解析 | +40, -10 |

---

## 🔄 同步状态

| Agent | 状态 |
|-------|------|
| **evo-agents** | ✅ 已提交并推送 |
| **claude-code-agent** | ✅ 已同步 |
| **main-agent** | ✅ 已同步 |

---

## 🎯 影响范围

### 正面影响

✅ **知识图谱构建**
- 实体名称更准确
- 关系提取更可靠

✅ **搜索结果展示**
- 标题清晰易读
- 用户体验更好

✅ **后续处理**
- 减少清洗步骤
- 提高处理效率

### 无破坏性变更

- ✅ 返回格式保持一致（JSON 结构不变）
- ✅ API 接口不变
- ✅ 向后兼容

---

## 🔧 技术细节

### 正则表达式改进

**清理域名前缀**:
```python
title = re.sub(r'^[a-z0-9.-]+\s*', '', title)
# 匹配：zhihu.com, google.com, www.baidu.com 等
```

**清理多余内容**:
```python
title = re.sub(r'\s*›\s*.*$', '', title)
# 匹配： › question, › 搜索，› www 等
```

### 结果质量验证

```python
# 验证标题长度
if result.get('title') and result.get('url') and len(result['title']) > 5:
    results.append(result)
```

---

## 📚 相关文档

- [Web Knowledge 技能文档](./skills/web-knowledge/SKILL.md)
- [知识图谱构建器文档](./skills/knowledge-graph/SKILL.md)

---

**修复完成！** 🎉

搜索 API 现在返回干净、准确的标题格式，适合知识图谱构建和其他下游任务使用。
