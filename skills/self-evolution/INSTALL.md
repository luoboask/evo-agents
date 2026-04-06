# self-evolution - 自进化系统安装指南

**基于 Generative Agents 的完整自进化系统：记忆流、分形思考、夜间循环。**

> 🧠 记忆流 | 🔮 分形思考 | 🌙 夜间循环 | 📊 模式识别 | 🤖 专家 Agent

---

## ⚡ 一键安装（推荐）

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/self-evolution

# 2. 运行自动安装脚本
python3 install.py

# 3. 验证安装
python3 main.py status
```

**就这么简单！** 安装脚本会自动：
- ✅ 检查 Python 和 SQLite3
- ✅ 创建配置文件 `config.yaml`
- ✅ 创建目录结构
- ✅ 初始化 3 个数据库
- ✅ 验证安装

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 50MB 磁盘空间

### 可选（强烈推荐）

- ⭕ Ollama（用于语义 Embedding）
  ```bash
  brew install ollama
  ollama pull nomic-embed-text
  ```

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/self-evolution/

# 应该看到 40+ 文件，包括：
# main.py, install.py, config.yaml.example
# ARCHITECTURE.md, INSTALL.md, SETUP.md
# 和各种功能模块...
```

### Step 2: 运行自动安装

```bash
cd ~/.openclaw/workspace/skills/self-evolution

# 运行安装脚本
python3 install.py
```

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

### Step 3: 验证安装

```bash
# 查看系统状态
python3 main.py status

# 应该看到：
# ✅ memory/memory_stream.db (0.07MB)
# ✅ memory/knowledge_base.db (0.07MB)
# ✅ evolution/evolution.db (0.07MB)
```

### Step 4: 记录第一个进化事件

```bash
# 记录系统安装完成
python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统安装完成，开始使用"
```

---

## 🔧 配置说明

### 配置文件位置

```bash
~/.openclaw/workspace/skills/self-evolution/config.yaml
```

### 必填配置

```yaml
# 工作目录
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

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/skills/self-evolution/
├── main.py                 # 主入口
├── install.py              # 安装脚本
├── config.yaml             # 配置文件
├── config.yaml.example     # 配置模板
│
├── # 核心模块
├── main.py                 # 主程序
├── memory_stream.py        # 记忆流
├── knowledge_base.py       # 知识库
├── self_evolution_real.py  # 自进化核心
│
├── # 学习模块
├── advanced_learning.py    # 高级学习
├── creative_learning_enhanced.py  # 创造性学习
├── reinforcement_learning_enhanced.py  # 强化学习
├── causal_reasoning_enhanced.py  # 因果推理
│
├── # 思考模块
├── fractal_thinking.py     # 分形思考
├── fractal_thinking_v2.py  # 分形思考 v2
├── nightly_cycle.py        # 夜间循环
├── daily_reflection.py     # 每日反思
│
├── # 专家 Agent
├── specialist_agents.py    # 专家 Agent
├── pattern_recognition.py  # 模式识别
│
├── # 文档
├── ARCHITECTURE.md         # 系统架构
├── INSTALL.md              # 本文件
├── SETUP.md                # 设置指南
├── INITIAL_SETUP.md        # 初始化指南
├── README_FINAL.md         # 功能总结
└── ...

数据目录（自动创建）：
~/.openclaw/workspace/
├── memory/
│   ├── memory_stream.db    # 记忆流数据库
│   ├── knowledge_base.db   # 知识库数据库
│   └── vector_db/          # 向量数据库
└── evolution/
    └── evolution.db        # 进化事件数据库
```

---

## 🎯 常用命令

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

# 模式识别
python3 main.py patterns

# 专家 Agent 咨询
python3 main.py ask --agent architect --question "如何优化系统架构"
```

### 进化事件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `BUG_FIX` | Bug 修复 | 修复了内存泄漏 |
| `FEATURE_ADDED` | 功能新增 | 添加了搜索功能 |
| `CODE_IMPROVED` | 代码优化 | 重构了 XX 模块 |
| `KNOWLEDGE_GAINED` | 知识获取 | 学习了新的算法 |
| `EVOLUTION_CHECK` | 进化检查 | 定期系统检查 |

---

## 🔮 分形思考

分形思考是多层次的深度分析系统：

```bash
# 基础分形（5 层）
python3 main.py fractal --limit 5

# 深度分形（10 层）
python3 main.py fractal --limit 10

# 带主题的分形
python3 main.py fractal --topic "系统架构" --limit 5
```

**输出示例：**
```
🔮 分形思考：系统架构
════════════════════════════════════════

L1: 表层分析
   当前系统采用模块化设计...

L2: 结构分析
   模块间的依赖关系呈现...

L3: 模式识别
   识别到 3 个重复模式...

L4: 原理分析
   底层原理基于...

L5: 本质洞察
   核心是...
```

---

## 🌙 夜间循环

夜间循环是系统在空闲时的自我整理和学习：

```bash
# 手动运行夜间循环
python3 main.py nightly

# 配置 crontab 自动运行
crontab -e
# 添加：每天凌晨 2 点
0 2 * * * cd ~/.openclaw/workspace/skills/self-evolution && python3 main.py nightly >> /tmp/nightly.log 2>&1
```

**夜间循环执行：**
1. 📊 整理当日记忆
2. 🔍 模式识别和分析
3. 🧠 知识压缩和归档
4. 💡 生成改进建议
5. 📈 更新系统状态

---

## ✅ 安装验证清单

```bash
# 1. 检查 Python
python3 --version

# 2. 检查 SQLite3
python3 -c "import sqlite3; print(sqlite3.version)"

# 3. 运行安装脚本
python3 install.py

# 4. 验证数据库
python3 main.py status

# 5. 记录第一个事件
python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统安装完成"

# 6. 测试分形思考
python3 main.py fractal --limit 3

# 7. （可选）测试 Ollama
ollama list
```

---

## ❓ 常见问题

### Q: 安装时提示 "Permission denied"

**A:** 检查工作目录权限：

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

或暂时禁用 Ollama：
```yaml
# config.yaml
ollama:
  enabled: false
```

### Q: 分形思考运行很慢

**A:** 减少层数或使用缓存：

```bash
# 减少层数
python3 main.py fractal --limit 3

# 启用缓存（在 config.yaml 中）
fractal:
  use_cache: true
```

### Q: 如何卸载？

**A:** 删除技能和数据（谨慎！数据一旦删除无法恢复）：

```bash
# 删除技能代码
rm -rf ~/.openclaw/workspace/skills/self-evolution

# 删除数据（谨慎！）
rm -rf ~/.openclaw/workspace/memory
rm -rf ~/.openclaw/workspace/evolution
```

---

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| **INSTALL.md** | 本文件 - 安装指南 |
| **SETUP.md** | 设置指南 |
| **INITIAL_SETUP.md** | 初始化配置 |
| **ARCHITECTURE.md** | 系统架构详解 |
| **README_FINAL.md** | 功能总结 |
| **README_FRACTAL.md** | 分形思考指南 |
| **README_NIGHTLY.md** | 夜间循环指南 |
| **OLLAMA_SETUP.md** | Ollama 配置 |
| **MULTI_AGENT_DESIGN.md** | 多 Agent 设计 |

---

## 🆘 获取帮助

遇到问题？

1. 查看 `main.py --help` 获取命令帮助
2. 检查日志：`/tmp/nightly.log` 或 `/tmp/fractal.log`
3. 在 AIWay 发帖提问或私信 @ai-baby
4. OpenClaw 社区：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建统一风格安装文档
- **2026-03-20**: v5.0 最终版本发布
- **2026-03-19**: 自进化系统创建

---

**最后更新：** 2026-03-22  
**版本：** 5.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** ai-baby  
**许可：** MIT
