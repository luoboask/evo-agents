# websearch - 智能网页搜索安装指南

**开箱即用，无需 API key 的网页搜索工具。**

> 基于 Bing 搜索，支持智能引擎选择和自动内容提取

---

## ⚡ 一键安装（推荐）

技能已预装，无需额外配置：

```bash
# 1. 验证技能文件
ls -la ~/.openclaw/workspace/skills/websearch/

# 2. 测试搜索
python3 search.py "OpenClaw 文档"
```

**就这么简单！** 无需 API key，无需配置，开箱即用。

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ 网络连接（访问 Bing）
- ✅ 约 1MB 磁盘空间

### 可选

- ⭕ 无其他依赖

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/websearch/

# 应该看到：
# SKILL.md, search.py, search.sh
```

### Step 2: 检查网络连接

```bash
# 测试 Bing 连接
curl -I https://www.bing.com

# 应该返回 HTTP/2 200 或类似成功响应
```

### Step 3: 测试搜索功能

```bash
cd ~/.openclaw/workspace/skills/websearch

# 测试搜索
python3 search.py "OpenClaw"

# 应该返回搜索结果列表
```

**输出示例：**
```
🔍 搜索结果：OpenClaw

1. OpenClaw 官方文档
   https://docs.openclaw.ai
   OpenClaw 是一个...

2. OpenClaw GitHub
   https://github.com/openclaw/openclaw
   OpenClaw 源码仓库...

...
```

---

## 🔧 配置说明

### 默认配置

websearch 设计为**零配置**，所有默认设置已优化：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 搜索结果数 | 10 | 每次返回的结果数量 |
| 国家/地区 | US | 搜索结果区域 |
| 语言 | en | 搜索结果语言 |
| 新鲜度 | 无限制 | 时间范围过滤 |

### 自定义配置（可选）

编辑 `search.py` 修改默认参数：

```python
# 搜索参数
DEFAULT_COUNT = 10        # 结果数量 (1-10)
DEFAULT_COUNTRY = "US"    # 国家代码
DEFAULT_LANGUAGE = "en"   # 语言代码
DEFAULT_FRESHNESS = None  # 时间过滤：'day', 'week', 'month', 'year'
```

### 命令行参数

```bash
# 基本搜索
python3 search.py "查询内容"

# 指定结果数量
python3 search.py "查询内容" --count 5

# 指定地区
python3 search.py "查询内容" --country CN

# 指定时间范围
python3 search.py "查询内容" --freshness week
```

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/
├── skills/
│   └── websearch/          # 技能代码
│       ├── SKILL.md        # 技能定义
│       ├── INSTALL.md      # 本文件
│       ├── search.py       # 主搜索脚本
│       └── search.sh       # Shell 快捷方式
│
└── ...                     # 其他 workspace 文件
```

**特点：** 
- 无外部依赖
- 无数据库
- 无配置文件
- 纯 Python 脚本

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 基本搜索
python3 search.py "Python 教程"

# 2. 查看帮助
python3 search.py --help

# 3. 使用 Shell 脚本
./search.sh "OpenClaw"
```

---

## 🎯 常用命令

```bash
# 基本搜索
python3 search.py "查询内容"

# 限制结果数量
python3 search.py "AI 新闻" --count 5

# 最近 24 小时的内容
python3 search.py "科技新闻" --freshness day

# 最近一周的内容
python3 search.py "产品发布" --freshness week

# 指定地区（中国）
python3 search.py "人工智能" --country CN

# 指定语言（中文）
python3 search.py "机器学习" --language zh

# 组合使用
python3 search.py "OpenClaw" --count 5 --freshness month --country US
```

### 命令行参数详解

| 参数 | 说明 | 示例 |
|------|------|------|
| `query` | 搜索关键词（必需） | `"Python 教程"` |
| `--count` | 结果数量 (1-10) | `--count 5` |
| `--country` | 国家代码 | `--country CN` |
| `--language` | 语言代码 | `--language zh` |
| `--freshness` | 时间范围 | `--freshness week` |
| `--help` | 显示帮助 | `--help` |

---

## 🌐 支持的国家和地区

常用国家代码：

| 代码 | 国家/地区 |
|------|-----------|
| US | 美国 |
| CN | 中国 |
| GB | 英国 |
| DE | 德国 |
| FR | 法国 |
| JP | 日本 |
| KR | 韩国 |
| ALL | 全球 |

---

## 🌍 支持的语言

常用语言代码：

| 代码 | 语言 |
|------|------|
| en | 英语 |
| zh | 中文 |
| ja | 日语 |
| ko | 韩语 |
| de | 德语 |
| fr | 法语 |
| es | 西班牙语 |
| pt | 葡萄牙语 |

---

## ❓ 常见问题

### Q: 搜索返回空结果

**A:** 检查网络连接：

```bash
# 测试 Bing 连接
curl -I https://www.bing.com

# 如果连接失败，检查网络或代理设置
```

### Q: 搜索结果不相关

**A:** 尝试优化搜索词或调整地区：

```bash
# 使用更具体的关键词
python3 search.py "OpenClaw 安装指南"

# 调整地区
python3 search.py "AI 新闻" --country CN
```

### Q: 如何获取网页全文内容？

**A:** 使用 `web_fetch` 工具提取网页内容：

```bash
# 在 OpenClaw 中
web_fetch --url "https://example.com/article"
```

或在 Python 中使用：
```python
from openclaw import web_fetch
content = web_fetch(url="https://example.com/article")
```

### Q: 搜索结果有广告怎么办？

**A:** websearch 使用 Bing API，返回的是自然搜索结果，不包含广告。

### Q: 如何卸载技能？

**A:** 删除技能目录：

```bash
rm -rf ~/.openclaw/workspace/skills/websearch
```

---

## 📚 相关工具

| 工具 | 说明 |
|------|------|
| **web_search** | 搜索网页（本技能） |
| **web_fetch** | 提取网页内容 |
| **memory-search** | 搜索本地记忆 |

### 组合使用示例

```bash
# 1. 搜索网页
python3 search.py "OpenClaw 文档"

# 2. 提取感兴趣网页的内容
# （在 OpenClaw 会话中使用 web_fetch 工具）

# 3. 将重要信息记录到记忆
# （使用 memory-search 记录）
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **SKILL.md** | 技能定义和用法详解 |
| **INSTALL.md** | 本文件 - 安装指南 |
| **search.py** | 主搜索脚本（内嵌帮助） |

---

## 🆘 获取帮助

遇到问题？

1. 运行 `python3 search.py --help` 查看帮助
2. 检查网络连接
3. 查看技能的 `SKILL.md` 文件
4. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建独立安装文档
- **2026-03-17**: websearch 技能创建
- **2026-03-16**: 初始版本创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
