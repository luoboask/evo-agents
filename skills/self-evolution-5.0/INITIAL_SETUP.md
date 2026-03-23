# 自进化系统 v5.0 - 初始化和配置指南

**重要：这是初始版本，不包含任何个人记忆数据。**

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# Python 3.9+ 已安装
# SQLite3 通常已预装

# 可选：安装 Ollama（用于更好的 Embedding）
# macOS: brew install ollama
# 然后运行：ollama pull nomic-embed-text
```

### 2. 配置工作目录

编辑 `config.yaml`（如不存在则创建）：

```yaml
# 你的工作目录（代码将在这里创建数据库）
workspace: /your/path/to/workspace

# Ollama 配置（可选）
ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text

# 记忆压缩配置
memory:
  compress_after_days: 7
  keep_high_importance: 7.0

# 模式识别阈值
patterns:
  recurring_bug_threshold: 2
  feature_bloat_threshold: 3
  min_similarity: 0.35
```

### 3. 初始化数据库

```bash
cd /path/to/self-evolution-5.0

# 检查状态（会自动创建空数据库）
python3 main.py status

# 记录第一个进化事件
python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统初始化完成"
```

### 4. 验证安装

```bash
# 应该看到：
# ✅ memory/memory_stream.db (0.07MB)
# ✅ memory/knowledge_base.db (0.07MB)
# ✅ skills/evolution-workbench/evolution.db (0.07MB)
```

---

## 📊 初始状态说明

**首次运行时，所有数据库都是空的：**

| 数据库 | 初始状态 | 说明 |
|--------|----------|------|
| `memory_stream.db` | 0 条记忆 | 随着使用自动增长 |
| `knowledge_base.db` | 0 条知识 | 学习时自动记录 |
| `evolution.db` | 0 次事件 | 手动或自动记录 |

**这是正常的！** 系统会从零开始积累你的个人数据。

---

## 🔧 配置定时任务（可选）

### macOS/Linux (crontab)

```bash
crontab -e

# 每天凌晨 2 点运行夜间循环
0 2 * * * cd /path/to/self-evolution-5.0 && python3 main.py nightly >> /tmp/nightly.log 2>&1

# 每 4 小时运行分形分析
0 */4 * * * cd /path/to/self-evolution-5.0 && python3 main.py fractal --limit 5 >> /tmp/fractal.log 2>&1
```

### Windows (任务计划程序)

```powershell
# 创建任务计划（管理员权限）
$action = New-ScheduledTaskAction -Execute "python3" -Argument "main.py nightly" -WorkingDirectory "C:\path\to\self-evolution-5.0"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "SelfEvolution-Nightly" -Action $action -Trigger $trigger
```

---

## 📝 常用命令

```bash
# 查看系统状态
python3 main.py status

# 记录进化事件
python3 main.py evolve --type BUG_FIX --content "修复了 XX 问题"

# 运行分形思考
python3 main.py fractal --limit 10

# 运行夜间循环
python3 main.py nightly

# 查看记忆
python3 main.py memory list --limit 20

# 测试 Embedding
python3 main.py embedding "修复 Bug" "修复错误"
```

---

## 🎯 进化事件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `BUG_FIX` | Bug 修复 | 修复了内存泄漏 |
| `FEATURE_ADDED` | 功能新增 | 添加了搜索功能 |
| `CODE_IMPROVED` | 代码优化 | 重构了 XX 模块 |
| `KNOWLEDGE_GAINED` | 知识获取 | 学习了新的算法 |
| `EVOLUTION_CHECK` | 进化检查 | 定期系统检查 |

---

## 📚 文档

- `ARCHITECTURE.md` - 完整架构说明
- `README_FINAL.md` - 功能总结
- `README_FRACTAL.md` - 分形思考使用指南
- `README_NIGHTLY.md` - 夜间循环使用指南

---

## ⚠️ 注意事项

1. **工作目录配置**：首次使用前必须配置 `config.yaml` 中的 `workspace` 路径
2. **数据库位置**：数据库会创建在 `workspace/memory/` 目录下
3. **Ollama 可选**：没有 Ollama 会自动降级到 TF-IDF 算法
4. **隐私保护**：所有数据存储在本地，不会上传到任何服务器

---

## 🐛 故障排除

### 问题：运行时报错 "database not found"

**解决：** 先运行 `python3 main.py status` 会自动创建空数据库。

### 问题：Embedding 失败

**解决：** 检查 Ollama 是否运行：`ollama list`，或禁用 Ollama 使用降级方案。

### 问题：路径错误

**解决：** 检查 `config.yaml` 中的 `workspace` 路径是否正确，确保有写入权限。

---

**最后更新：** 2026-03-20  
**版本：** 5.0.0 (初始发布版)
