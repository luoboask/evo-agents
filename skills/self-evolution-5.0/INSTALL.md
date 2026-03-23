# 自进化系统 v5.0 - 安装指南

**5 分钟快速安装，从零开始你的自进化之旅。**

---

## ⚡ 一键安装（推荐）

```bash
# 1. 复制技能到你的 workspace
mkdir -p ~/.openclaw/workspace/skills
cp -r /path/to/self-evolution-5.0 ~/.openclaw/workspace/skills/

# 2. 进入目录
cd ~/.openclaw/workspace/skills/self-evolution-5.0

# 3. 运行自动安装脚本
python3 install.py
```

**就这么简单！** 安装脚本会自动：
- ✅ 检查 Python 和 SQLite3
- ✅ 创建配置文件（默认工作目录：`~/.openclaw/workspace`）
- ✅ 创建目录结构
- ✅ 初始化 3 个空数据库
- ✅ 验证安装

---

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 10MB 磁盘空间

### 可选（推荐）

- ⭕ Ollama（用于更好的语义 Embedding）
  - macOS: `brew install ollama`
  - 然后：`ollama pull nomic-embed-text`

---

## 🚀 快速安装（3 步）

### Step 1: 复制技能到你的 workspace

```bash
# 默认安装位置：~/.openclaw/workspace/skills/self-evolution-5.0
mkdir -p ~/.openclaw/workspace/skills
cp -r /path/to/self-evolution-5.0 ~/.openclaw/workspace/skills/

# 进入目录
cd ~/.openclaw/workspace/skills/self-evolution-5.0
```

**或者直接用这个命令：**

```bash
# 如果你在当前技能目录
cd ~/.openclaw/workspace/skills/self-evolution-5.0
```

---

### Step 2: 运行安装脚本

```bash
# 自动安装脚本会：
# 1. 检查 Python 和 SQLite3
# 2. 创建配置文件
# 3. 初始化空数据库
# 4. 验证安装

python3 install.py
```

**安装脚本输出示例：**

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

下一步：
1. 编辑 config.yaml 配置你的选项（可选）
2. 运行：python3 main.py status
3. 记录第一个事件：python3 main.py evolve --type KNOWLEDGE_GAINED --content "安装完成"
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

## 🔧 手动安装（可选）

如果自动安装脚本失败，可以手动执行：

### 1. 创建配置文件

```bash
# 复制配置模板
cp config.yaml.example config.yaml

# 编辑配置文件
nano config.yaml
```

**修改以下配置：**

```yaml
# 工作目录（默认即可）
workspace: /Users/你的用户名/.openclaw/workspace

# Ollama 配置（可选）
ollama:
  enabled: false  # 有 Ollama 改为 true
  url: http://localhost:11434
  model: nomic-embed-text
```

### 2. 创建目录结构

```bash
# 创建工作目录
mkdir -p ~/.openclaw/workspace/memory
mkdir -p ~/.openclaw/workspace/evolution
```

### 3. 初始化数据库

```bash
# 运行状态检查会自动创建数据库
python3 main.py status
```

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/
├── skills/
│   └── self-evolution-5.0/      # 技能代码
│       ├── main.py              # 主入口
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

## ⚙️ 配置说明

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

## 🎯 安装后做什么？

### 1. 记录第一个进化事件

```bash
python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统安装完成，开始使用"
```

### 2. 查看系统状态

```bash
python3 main.py status
```

### 3. 运行一次分形思考

```bash
python3 main.py fractal --limit 5
```

### 4. 配置定时任务（可选）

```bash
# 编辑 crontab
crontab -e

# 添加每天凌晨 2 点的夜间循环
0 2 * * * cd ~/.openclaw/workspace/skills/self-evolution-5.0 && python3 main.py nightly >> /tmp/nightly.log 2>&1
```

---

## ❓ 常见问题

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

**A:** 删除技能和数据：

```bash
# 删除技能代码
rm -rf ~/.openclaw/workspace/skills/self-evolution-5.0

# 删除数据（谨慎！）
rm -rf ~/.openclaw/workspace/memory
rm -rf ~/.openclaw/workspace/evolution
```

---

## 📚 下一步

安装完成后，阅读以下文档：

1. **INITIAL_SETUP.md** - 初始化和使用指南
2. **ARCHITECTURE.md** - 系统架构详解
3. **README_FINAL.md** - 功能总结

---

## 🆘 获取帮助

遇到问题？

1. 查看 `main.py --help` 获取命令帮助
2. 检查日志：`/tmp/nightly.log` 或 `/tmp/fractal.log`
3. 在 AIWay 发帖提问或私信 @ai-baby

---

**最后更新：** 2026-03-20  
**版本：** 5.0.0
