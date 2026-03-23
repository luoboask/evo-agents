# 🚀 ai-baby Workspace 设置指南

**版本：** v5.1  
**最后更新：** 2026-03-23  
**状态：** ✅ 生产就绪

---

## 📋 概述

ai-baby 是一个基于 OpenClaw 的自进化 AI 助手工作区，包含：

- 🧠 **记忆搜索系统** - 关键词 + 向量语义搜索
- 📊 **RAG 评估系统** - 检索质量监控与优化
- 🧬 **自进化核心** - 分形思考 + 夜间循环
- 🔐 **配置分离** - 敏感数据与代码分离

---

## 🎯 快速开始

### 1. 克隆仓库

```bash
cd /Users/dhr/.openclaw/workspace
git clone <your-repo-url> workspace-ai-baby
cd workspace-ai-baby
```

### 2. 系统初始化

```bash
# 完整初始化（推荐新用户）
python3 init_system.py

# 或模块化初始化
python3 init_system.py -m memory-search  # 只初始化记忆搜索
python3 init_system.py -m rag            # 只初始化 RAG 评估
python3 init_system.py -m self-evolution # 只初始化自进化核心
```

### 3. 验证功能

```bash
# 快速验证所有功能
python3 quick_verify.py

# 查看系统状态
./start.sh
```

### 4. 开始使用

```bash
# 语义搜索
python3 skills/memory-search/search_sqlite.py "查询" --semantic

# 添加记忆
python3 skills/memory-search/search_sqlite.py --add "今天学习了 RAG" \
  --type knowledge --details '{"topic": "RAG"}'

# 查看 RAG 报告
python3 skills/rag/evaluate.py --report --days 7
```

---

## 📁 目录结构

```
workspace-ai-baby/
├── 🔧 初始化工具
│   ├── init_system.py          ⭐ 系统初始化（支持模块化）
│   ├── quick_verify.py         ⭐ 快速功能验证
│   ├── start.sh                ⭐ 查看系统状态
│   └── separate_config.py      配置分离工具
│
├── 📄 核心文档
│   ├── README.md               ⭐ 工作区概览
│   ├── GETTING_STARTED.md      ⭐ 快速开始指南
│   ├── WORKSPACE_SETUP.md      ⭐ 本文档 - 设置指南
│   ├── USER_MANUAL.md          详细使用手册
│   ├── SELF_EVOLUTION_SYSTEM.md 自进化体系详解
│   ├── MODULE_INIT.md          模块化初始化指南
│   ├── CONFIG_SEPARATION.md    配置分离方案
│   └── SECURITY_REPORT.md      安全报告
│
├── 📂 skills/                  # 技能代码（可提交 Git）
│   ├── rag/                    RAG 评估系统
│   ├── memory-search/          记忆搜索
│   ├── self-evolution-5.0/     自进化核心
│   ├── aiway/                  AIWay 社区
│   └── websearch/              网页搜索
│
└── 📂 ~/.openclaw/workspace-ai-baby-config/  # 个人配置（不提交 Git）
    ├── config.yaml             个人配置文件
    ├── credentials.json        API 凭证
    ├── memory/                 数据库
    │   ├── ai-baby_memory_stream.db
    │   └── ai-baby_knowledge_base.db
    └── logs/                   日志
        └── evaluations.jsonl
```

---

## 🔐 配置分离

### 安全原则

**可提交 Git 的内容：**
- ✅ 代码（`skills/`）
- ✅ 文档（`*.md`）
- ✅ 脚本（`*.py`, `*.sh`）
- ✅ 配置模板（`config.yaml.example`）

**不提交 Git 的内容：**
- ❌ 个人配置文件（`config.yaml`）
- ❌ API 凭证（`credentials.json`）
- ❌ 数据库文件（`*.db`）
- ❌ 日志文件（`*.jsonl`, `*.log`）
- ❌ 学习记录（`memory/learning/`）

### 配置文件位置

**个人配置**（自动创建，不提交 Git）：
```bash
~/.openclaw/workspace-ai-baby-config/
├── config.yaml              # 个人配置
├── credentials.json         # API 凭证
├── memory/                  # 数据库
│   ├── ai-baby_memory_stream.db
│   └── ai-baby_knowledge_base.db
└── logs/                    # 日志
    └── evaluations.jsonl
```

**配置模板**（提交 Git）：
```bash
workspace-ai-baby/
└── config.yaml.example      # 配置模板（示例）
```

### .gitignore 规则

```gitignore
# 数据库
*.db
*.sqlite

# 日志
*.jsonl
*.log
logs/

# 凭证
credentials.json
config.yaml

# 学习记录
memory/learning/

# Python
__pycache__/
*.pyc
*.egg-info/

# 系统
.DS_Store
Thumbs.db
```

---

## 🛠️ 系统要求

### 必需

- ✅ Python 3.9+
- ✅ Git
- ✅ SQLite3（通常已预装）
- ✅ 约 50MB 磁盘空间

### 可选（推荐）

- ⭕ Ollama（用于向量语义搜索）
  ```bash
  # macOS
  brew install ollama
  ollama pull nomic-embed-text
  
  # 验证
  ollama list
  ```

- ⭕ pip 包
  ```bash
  pip3 install pyyaml
  ```

---

## 📋 初始化检查清单

运行 `python3 init_system.py` 后，应该看到：

### 环境检查
- [ ] ✅ Python 3.9+ 已安装
- [ ] ✅ 依赖包完整（yaml, sqlite3）
- [ ] ✅ Git 已安装

### 配置检查
- [ ] ✅ 配置目录创建成功
- [ ] ✅ 配置文件生成
- [ ] ✅ .gitignore 配置正确

### 功能检查
- [ ] ✅ 数据库检查通过
- [ ] ✅ 记忆搜索功能正常
- [ ] ✅ RAG 评估功能正常
- [ ] ✅ 自进化核心模块完整

**预期输出：**
```
🎉 系统初始化完成！所有检查通过！
```

---

## 🔧 常用命令

### 系统管理

```bash
# 初始化（首次使用）
python3 init_system.py

# 模块化初始化
python3 init_system.py -m rag

# 快速验证
python3 quick_verify.py

# 查看状态
./start.sh
```

### 记忆搜索

```bash
# 语义搜索
python3 skills/memory-search/search_sqlite.py "RAG" --semantic

# 添加记忆
python3 skills/memory-search/search_sqlite.py --add "内容" \
  --type knowledge \
  --details '{"key": "value"}' \
  --source "https://..."

# 查看统计
python3 skills/memory-search/search_sqlite.py --stats
```

### RAG 评估

```bash
# 查看报告
python3 skills/rag/evaluate.py --report --days 7

# 自动调优（需要 10+ 条数据）
python3 skills/rag/auto_tune.py --report
```

### 自进化功能

```bash
cd skills/self-evolution-5.0

# 查看状态
python3 main.py status

# 运行分形思考
python3 main.py fractal --limit 10
```

---

## 🆘 故障处理

### 问题 1: Python 版本过低

```bash
# 检查版本
python3 --version

# 升级（macOS）
brew install python@3.10
```

### 问题 2: 依赖包缺失

```bash
# 安装依赖
pip3 install pyyaml
```

### 问题 3: 数据库不存在

```bash
# 运行初始化会自动创建
python3 init_system.py

# 或手动测试
python3 quick_verify.py
```

### 问题 4: Ollama 未运行

```bash
# 检查状态
ollama list

# 启动服务
ollama serve
```

### 问题 5: 配置加载失败

```bash
# 检查配置文件
cat ~/.openclaw/workspace-ai-baby-config/config.yaml

# 重新创建配置
python3 separate_config.py
```

---

## 📊 项目结构说明

### 核心模块

| 模块 | 位置 | 功能 |
|------|------|------|
| **记忆搜索** | `skills/memory-search/` | 关键词 + 语义搜索 |
| **RAG 评估** | `skills/rag/` | 检索质量评估 |
| **自进化核心** | `skills/self-evolution-5.0/` | 分形思考 + 夜间循环 |
| **AIWay** | `skills/aiway/` | 社区集成 |
| **网页搜索** | `skills/websearch/` | 无需 API key 的搜索 |

### 数据流

```
用户提问
    ↓
记忆搜索（自动 RAG 记录）
    ↓
检索结果 + 相似度分数
    ↓
生成回复
    ↓
RAG 记录完成 → logs/evaluations.jsonl
```

---

## 🔒 安全最佳实践

### 1. 配置分离

- ✅ 个人配置存储在 `~/.openclaw/workspace-ai-baby-config/`
- ✅ 代码和文档存储在 `workspace-ai-baby/`
- ✅ .gitignore 保护敏感文件

### 2. Git 安全

- ✅ 提交前检查：`git status`
- ✅ 查看变更：`git diff --cached`
- ✅ 使用 `git-secrets` 扫描敏感信息

### 3. 备份策略

```bash
# 定期备份个人配置
cp -r ~/.openclaw/workspace-ai-baby-config /backup/location/

# 或使用 Time Machine（macOS）
```

### 4. 凭证管理

- ✅ 使用环境变量存储密钥
- ✅ 不硬编码在代码中
- ✅ 定期轮换 API 密钥

---

## 📈 开发工作流

### 1. 克隆和设置

```bash
git clone <repo-url>
cd workspace-ai-baby
python3 init_system.py
```

### 2. 日常开发

```bash
# 查看状态
./start.sh

# 运行测试
python3 quick_verify.py

# 提交代码
git add .
git commit -m "feat: xxx"
git push
```

### 3. 更新工作区

```bash
# 拉取最新代码
git pull

# 重新初始化（如果有新依赖）
python3 init_system.py
```

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| **README.md** | 工作区概览和快速开始 |
| **GETTING_STARTED.md** | 详细快速开始指南 |
| **WORKSPACE_SETUP.md** | 本文档 - 设置指南 |
| **USER_MANUAL.md** | 详细使用手册 |
| **SELF_EVOLUTION_SYSTEM.md** | 自进化体系详解 |
| **MODULE_INIT.md** | 模块化初始化指南 |
| **CONFIG_SEPARATION.md** | 配置分离方案 |
| **SECURITY_REPORT.md** | 安全报告 |

---

## 🎯 下一步

### 今天
- [ ] 运行 `python3 init_system.py`
- [ ] 运行 `python3 quick_verify.py`
- [ ] 尝试记忆搜索
- [ ] 添加第一条记忆

### 本周
- [ ] 积累 RAG 数据（目标：10+ 条）
- [ ] 查看 RAG 报告
- [ ] 运行第一次自动调优

### 本月
- [ ] 激活自进化核心
- [ ] 配置定时任务
- [ ] 查看改进计划

---

## 🎉 总结

**完成设置后，你将拥有：**

✅ 完整的自进化 AI 助手系统  
✅ 安全的配置管理（代码/配置分离）  
✅ RAG 评估和优化能力  
✅ 记忆搜索和语义检索  
✅ 分形思考和夜间循环  
✅ 完善的安全保护  

**开始使用吧！**

```bash
python3 init_system.py  # 初始化
python3 quick_verify.py # 验证
./start.sh              # 查看状态
```

---

## 📞 获取帮助

- 📖 查看文档：`GETTING_STARTED.md`, `USER_MANUAL.md`
- 🔍 系统状态：`./start.sh`
- 🐛 故障处理：本文档"故障处理"章节
- 💬 社区：AIWay (https://aiway.alibaba-inc.com)

---

**维护者：** ai-baby  
**许可证：** MIT  
**最后更新：** 2026-03-23  
**版本：** v5.1
