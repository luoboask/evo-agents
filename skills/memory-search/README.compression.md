# Memory Compression - 记忆压缩器

将每日记忆智能压缩为周度、月度、年度摘要，减少文件数量，保留关键信息。

## ✨ 功能特性

- **关键事件提取** - 自动识别重要性 >= 7.0 的事件
- **智能摘要生成** - 使用 Ollama LLM 生成结构化摘要（可选）
- **层次化组织** - 日→周→月→年 四级结构
- **失败回退** - 如果 LLM 不可用，生成基础列表式摘要

## 📦 依赖要求

### 必需
- Python 3.9+

### 可选（增强功能）
- Ollama + `qwen2.5:1.5b` 模型（智能摘要生成）

```bash
# 安装 Ollama（如未安装）
brew install ollama  # macOS

# 拉取模型
ollama pull qwen2.5:1.5b
```

## 🚀 使用方法

### 基础用法

```bash
# 进入技能目录
cd ~/.openclaw/workspace-<agent>/skills/memory-search

# 压缩上周记忆（默认）
python3 compress.py

# 压缩指定周
python3 compress.py --weekly --year 2026 --week 13

# 压缩上月
python3 compress.py --monthly

# 压缩所有（周度 + 月度）
python3 compress.py --all

# 查看统计信息
python3 compress.py --stats
```

### 输出示例

```bash
$ python3 compress.py --weekly

📅 压缩 2026 年第 13 周的记忆...
  找到 6 个文件
  提取到 19 个关键事件
  ✅ 已保存到 2026-W13.md
```

### 生成的文件结构

```
memory/
├── 2026-04-01.md          ← 每日记录（原始，保留）
├── 2026-04-02.md
├── ...
├── weekly/
│   ├── 2026-W13.md        ← 新生成的周度摘要
│   └── 2026-W14.md
├── monthly/
│   ├── 2026-03.md         ← 月度摘要
│   └── 2026-04.md
└── yearly/
    └── 2026.md            ← 年度摘要
```

### 自动化（推荐）

**每周日凌晨 2 点自动压缩上周记忆：**

```bash
crontab -e

# 添加以下行：
0 2 * * 0 cd ~/.openclaw/workspace-<agent>/skills/memory-search && python3 compress.py --weekly >> /tmp/memory_compress.log 2>&1

# 每月 1 日凌晨 3 点自动压缩上月记忆：
0 3 1 * * cd ~/.openclaw/workspace-<agent>/skills/memory-search && python3 compress.py --monthly >> /tmp/memory_compress.log 2>&1
```

## 📊 摘要示例

**周度摘要 (`weekly/2026-W13.md`)：**

```markdown
---
生成时间：2026-04-04 04:42:00
事件数量：19
模型：qwen2.5:1.5b
---

# 周度摘要

## 🎯 主要成就
- 完成记忆系统增强功能开发
- 实现知识图谱 AI 实体识别
- 优化搜索性能

## 💡 重要决策
- 采用 optional skills 方式发布增强功能
- 使用 Ollama 作为本地 LLM 方案

## 📚 学到的知识
- 掌握了知识图谱构建技术
- 了解了记忆压缩最佳实践

## 📋 待办事项
- 编写完整文档
- 收集用户反馈
```

## 🔧 命令行参数

| 参数 | 说明 |
|------|------|
| `--weekly` | 压缩周度摘要 |
| `--monthly` | 压缩月度摘要 |
| `--all` | 压缩所有（周度 + 月度） |
| `--stats` | 只显示统计信息 |
| `--year <年份>` | 指定年份 |
| `--week <周数>` | 指定周数 |
| `--month <月份>` | 指定月份 |

## ⚠️ 故障排除

### Q: 摘要生成失败？

**A:** 检查 Ollama 服务和模型：
```bash
ollama list
ollama run qwen2.5:1.5b "测试"
```

如果 LLM 不可用，系统会自动生成基础摘要（列表式）。

### Q: 找不到本周的记忆文件？

**A:** 确认记忆文件命名格式为 `YYYY-MM-DD.md`：
```bash
ls -la ../memory/*.md
```

### Q: 如何清理旧的每日文件？

**A:** 保留最近 4 周的每日文件，删除更早的：
```bash
find ../memory -maxdepth 1 -name "*.md" -mtime +30 -delete
```

**注意：** 周度、月度摘要已保存关键信息，可以安全删除旧的每日文件。

## 📝 最佳实践

### 1. 保留策略

| 类型 | 保留时长 | 清理频率 |
|------|---------|---------|
| 每日文件 | 30 天 | 每月清理 |
| 周度摘要 | 3 个月 | 每季度清理 |
| 月度摘要 | 12 个月 | 每年清理 |
| 年度摘要 | 永久 | - |

### 2. 压缩时机

- **周度压缩**：每周日凌晨（此时上周数据完整）
- **月度压缩**：每月 1 日凌晨
- **年度压缩**：每年 1 月 1 日（手动执行）

### 3. 备份建议

```bash
# 压缩前备份
tar -czf memory_backup_$(date +%Y%m%d).tar.gz ../memory/

# 只备份摘要文件（更小）
tar -czf memory_summary_backup_$(date +%Y%m%d).tar.gz \
    ../memory/weekly/ ../memory/monthly/ ../memory/yearly/
```

## 🔗 相关技能

- **knowledge-graph** - 知识图谱构建（从记忆中提取实体关系）
- **search.py** - 记忆搜索（可搜索压缩后的摘要）

---

**最后更新：** 2026-04-04  
**版本：** v2.0 (Enhanced with AI)
