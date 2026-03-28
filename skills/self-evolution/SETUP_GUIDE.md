# 自进化系统 v5.0 - 安装与设置指南

**5 分钟快速安装，从零开始你的自进化之旅。**

---

## ⚡ 一键安装（推荐）

```bash
# 1. 复制技能到你的 workspace
mkdir -p ~/.openclaw/workspace/skills
cp -r /path/to/self-evolution ~/.openclaw/workspace/skills/

# 2. 进入目录
cd ~/.openclaw/workspace/skills/self-evolution

# 3. 运行自动安装脚本
python3 install.py
```

**就这么简单！** 安装脚本会自动：
- ✅ 检查 Python 和 SQLite3
- ✅ 创建配置文件
- ✅ 创建目录结构
- ✅ 初始化 3 个空数据库
- ✅ 验证安装

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

## 🚀 手动安装（3 步）

### Step 1: 复制技能

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -r /path/to/self-evolution ~/.openclaw/workspace/skills/
cd ~/.openclaw/workspace/skills/self-evolution
```

### Step 2: 创建配置

```bash
# 创建配置文件
cat > config.yaml << 'EOF'
# 自进化系统配置
working_directory: ~/.openclaw/workspace
agent_name: ai-baby

# Embedding 配置
embedding:
  model: nomic-embed-text
  ollama_url: http://localhost:11434

# 分形思考配置
fractal:
  max_depth: 4
  min_confidence: 0.6

# 夜间循环配置
nightly:
  wind_down_hour: 22
  consolidation_hour: 23
EOF
```

### Step 3: 初始化数据库

```bash
python3 -c "
from memory_stream import MemoryStream
from self_evolution_real import RealSelfEvolution

ms = MemoryStream()
print('✅ 记忆流初始化完成')

evolution = RealSelfEvolution()
print('✅ 进化系统初始化完成')
"
```

---

## ✅ 验证安装

```bash
# 运行状态检查
python3 main.py status

# 输出示例:
# ====================================
# 🚀 自进化系统 v5.0 - 状态
# ====================================
# ✅ memory_stream.db (0.01MB)
# ✅ knowledge_base.db (0.01MB)
# ✅ evolution.db (0.01MB)
# ====================================
```

---

## 📚 目录结构

```
self-evolution/
├── main.py                  # 主入口
├── memory_stream.py         # 记忆流管理
├── self_evolution_real.py   # 进化引擎
├── embedding.py             # Embedding 模块
├── config.yaml              # 配置文件
├── memory/                  # 数据库目录
│   ├── memory_stream.db
│   ├── knowledge_base.db
│   └── evolution.db
└── README_*.md              # 功能文档
```

---

## 🎯 下一步

- 📖 `README_FRACTAL.md` - 分形思考系统
- 📖 `README_NIGHTLY.md` - 夜间循环自动化
- 📖 `ARCHITECTURE.md` - 系统架构设计

---

**维护者：** ai-baby  
**版本：** v5.0  
**更新时间：** 2026-03-23
