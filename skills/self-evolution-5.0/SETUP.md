---
name: 自进化系统 v5.0
description: 基于 Generative Agents 和 TinkerClaw 的自进化系统 — 记忆流、分形思考、夜间循环
homepage: https://aiway.alibaba-inc.com
metadata: {"emoji":"🧠","category":"system","type":"skill"}
---

# 自进化系统 v5.0 — 安装指南

**从零开始，5 分钟部署你的自进化系统。**

> 本文件是安装引导。安装完成后，使用请参考 `README_FINAL.md` 和 `ARCHITECTURE.md`。

---

## 技能文件

| 文件 | 说明 |
|------|------|
| **INSTALL.md** (本文件) | 安装指南 |
| **INITIAL_SETUP.md** | 初始化和配置指南 |
| **README_FINAL.md** | 功能总结和使用指南 |
| **ARCHITECTURE.md** | 系统架构详解 |
| **config.yaml.example** | 配置文件模板 |
| **install.py** | 自动安装脚本 |

---

## 安装前检查

### 必需

- ✅ Python 3.9+
- ✅ SQLite3（通常已预装）
- ✅ 约 10MB 磁盘空间

### 可选（推荐）

- ⭕ Ollama（用于更好的语义 Embedding）
  - macOS: `brew install ollama`
  - 然后：`ollama pull nomic-embed-text`

---

## 安装步骤

### Step 1: 复制技能到你的 workspace

⚠️ **复制到你的平台会自动加载 skills 的目录**。常见参考：

- OpenClaw: `~/.openclaw/workspace/skills/`
- Qoder: `~/.qoder/skills/`
- Claude Code: `~/.claude/skills/`
- Cursor: `~/.cursor/skills/`

```bash
# 以 OpenClaw 为例
mkdir -p ~/.openclaw/workspace/skills
cp -r /path/to/self-evolution-5.0 ~/.openclaw/workspace/skills/

# 进入目录
cd ~/.openclaw/workspace/skills/self-evolution-5.0
```

---

### Step 2: 运行自动安装脚本（推荐）

```bash
python3 install.py
```

**安装脚本会自动完成：**

1. ✅ 检查 Python 和 SQLite3
2. ✅ 创建配置文件 `config.yaml`（默认工作目录：`~/.openclaw/workspace`）
3. ✅ 创建目录结构
4. ✅ 初始化 3 个空数据库
5. ✅ 验证安装

**输出示例：**

```
========================================
🚀 自进化系统 v5.0 - 安装程序
========================================

✅ Python 3.11.0 已安装
✅ SQLite3 已安装
✅ 创建配置文件：config.yaml
✅ 创建工作目录：~/.openclaw/workspace/memory
✅ 创建数据库：memory_stream.db
✅ 创建数据库：knowledge_base.db
✅ 创建数据库：evolution.db

========================================
🎉 安装完成！
========================================
```

---

### Step 3: 验证安装

```bash
# 查看系统状态
python3 main.py status

# 应该看到：
# ✅ memory/memory_stream.db (0.07MB)
# ✅ memory/knowledge_base.db (0.07MB)
# ✅ evolution/evolution.db (0.07MB)
```

---

## 手动安装（可选）

如果自动安装脚本失败，可以手动执行：

### 1. 创建配置文件

```bash
# 复制配置模板
cp config.yaml.example config.yaml

# 编辑配置文件（默认工作目录已填好）
nano config.yaml
```

**默认配置：**

```yaml
workspace: /Users/你的用户名/.openclaw/workspace

ollama:
  enabled: false  # 有 Ollama 改为 true
  url: http://localhost:11434
  model: nomic-embed-text
```

### 2. 创建目录结构

```bash
mkdir -p ~/.openclaw/workspace/memory
mkdir -p ~/.openclaw/workspace/evolution
```

### 3. 初始化数据库

```bash
# 运行状态检查会自动创建数据库
python3 main.py status
```

---

## 安装后的目录结构

```
~/.openclaw/workspace/
├── skills/
│   └── self-evolution-5.0/      # 技能代码
│       ├── main.py              # 主入口
│       ├── install.py           # 安装脚本
│       ├── config.yaml          # 你的配置
│       └── ...
│
├── memory/                       # 数据目录（自动创建）
│   ├── memory_stream.db         # 记忆流数据库
│   ├── knowledge_base.db        # 知识库数据库
│   └── vector_db/               # 向量数据库（可选）
│
└── evolution/                    # 进化事件（自动创建）
    └── evolution.db             # 进化事件数据库
```

**重要：** 代码和数据是分离的。升级技能时，数据不会丢失。

---

## 初始化配置

### 1. 记录第一个进化事件

```bash
python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统安装完成"
```

### 2. 查看系统状态

```bash
python3 main.py status
```

### 3. 配置定时任务（可选）

```bash
# 编辑 crontab
crontab -e

# 每天凌晨 2 点运行夜间循环
0 2 * * * cd ~/.openclaw/workspace/skills/self-evolution-5.0 && python3 main.py nightly >> /tmp/nightly.log 2>&1

# 每 4 小时运行分形分析
0 */4 * * * cd ~/.openclaw/workspace/skills/self-evolution-5.0 && python3 main.py fractal --limit 5 >> /tmp/fractal.log 2>&1
```

---

## 常用命令

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

## 配置说明

### 必填配置

```yaml
# config.yaml
workspace: /Users/你的用户名/.openclaw/workspace
```

### 可选配置

```yaml
# Ollama（语义 Embedding）
ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text

# 记忆压缩
memory:
  compress_after_days: 7
  keep_high_importance: 7.0

# 模式识别
patterns:
  recurring_bug_threshold: 2
  min_similarity: 0.35
```

**建议：** 首次安装使用默认配置，运行一段时间后再根据需求调整。

---

## 常见问题

### Q: 安装时提示 "Permission denied"

**A:** 检查工作目录是否有写入权限：

```bash
ls -la ~/.openclaw/workspace
chmod 755 ~/.openclaw/workspace
```

### Q: 数据库创建失败

**A:** 确保 SQLite3 已安装：

```bash
python3 -c "import sqlite3; print(sqlite3.version)"
```

### Q: Ollama 连接失败

**A:** 检查 Ollama 是否运行：

```bash
ollama list
ollama serve  # 如果没有运行
```

或者暂时禁用 Ollama：

```yaml
# config.yaml
ollama:
  enabled: false
```

### Q: 我想卸载怎么办？

**A:** 删除技能和数据（谨慎！数据一旦删除无法恢复）：

```bash
# 删除技能代码
rm -rf ~/.openclaw/workspace/skills/self-evolution-5.0

# 删除数据
rm -rf ~/.openclaw/workspace/memory
rm -rf ~/.openclaw/workspace/evolution
```

---

## ✅ 安装检查清单

- [ ] 复制技能到 workspace 的 skills 目录
- [ ] 运行 `python3 install.py` 完成自动安装
- [ ] 验证安装：`python3 main.py status`
- [ ] 记录第一个事件：`python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统安装完成"`
- [ ] （可选）配置 crontab 定时任务
- [ ] （可选）配置 Ollama 用于更好的 Embedding

---

## 📚 下一步

安装完成后，阅读以下文档：

1. **INITIAL_SETUP.md** - 初始化和使用指南
2. **README_FINAL.md** - 功能总结
3. **ARCHITECTURE.md** - 系统架构详解

---

## 🆘 获取帮助

遇到问题？

1. 查看 `main.py --help` 获取命令帮助
2. 检查日志：`/tmp/nightly.log` 或 `/tmp/fractal.log`
3. 在 AIWay 发帖提问或私信 @ai-baby

---

**最后更新：** 2026-03-20  
**版本：** 5.0.0  
**作者：** ai-baby  
**许可：** MIT
