# 🚀 ai-baby 快速开始指南

**版本：** v5.1  
**最后更新：** 2026-03-23

---

## 🎯 三步开始使用

### Step 1: 系统初始化（首次使用）

```bash
cd /Users/dhr/.openclaw/workspace-ai-baby

# 完整初始化（推荐新用户）
python3 init_system.py
```

**这会：**
- ✅ 检查 Python 环境（需要 3.9+）
- ✅ 检查依赖包
- ✅ 创建配置目录
- ✅ 检查数据库
- ✅ 验证 Git 配置
- ✅ 运行功能测试

**预期输出：**
```
🎉 系统初始化完成！所有检查通过！
```

---

### 模块化初始化（高级）

如果只想初始化特定模块：

```bash
# 列出可用模块
python3 init_system.py --list

# 只初始化记忆搜索
python3 init_system.py -m memory-search

# 只初始化 RAG 评估
python3 init_system.py -m rag

# 只初始化自进化核心
python3 init_system.py -m self-evolution

# 初始化所有模块
python3 init_system.py -m all
```

**适用场景：**
- 只使用部分功能
- 某个模块出现问题需要重新初始化
- 快速检查特定模块状态

---

### Step 2: 查看系统状态

```bash
# 查看系统状态
./start.sh
```

**输出示例：**
```
📊 记忆统计:
  数据库：~/.openclaw/workspace-ai-baby-config/memory/...
  总数：23
  按类型：{'goal': 3, 'knowledge': 4, ...}

✅ 准备就绪
```

---

### Step 3: 开始使用

```bash
# 语义搜索
python3 skills/memory-search/search_sqlite.py "RAG" --semantic

# 添加记忆
python3 skills/memory-search/search_sqlite.py --add "今天学习了 RAG" \
  --type knowledge --details '{"topic": "RAG"}'

# 查看 RAG 报告
python3 skills/rag/evaluate.py --report --days 7
```

---

## 🔧 常用命令

### 系统管理

```bash
# 初始化和验证
python3 init_system.py

# 查看系统状态
./start.sh

# 快速验证功能
python3 quick_verify.py

# 配置分离（保护敏感数据）
python3 separate_config.py
```

### 记忆搜索

```bash
# 关键词搜索
python3 skills/memory-search/search_sqlite.py "查询"

# 语义搜索（需要 Ollama）
python3 skills/memory-search/search_sqlite.py "查询" --semantic

# 添加记忆
python3 skills/memory-search/search_sqlite.py --add "内容" \
  --type knowledge \
  --details '{"key": "value"}' \
  --source "https://..."

# 查看统计
python3 skills/memory-search/search_sqlite.py --stats

# 列出记忆
python3 skills/memory-search/search_sqlite.py --list --limit 20
```

### RAG 评估

```bash
# 查看报告
python3 skills/rag/evaluate.py --report --days 7

# 记录检索
python3 skills/rag/evaluate.py --record \
  --query "测试查询" \
  --retrieved 5 \
  --latency 100 \
  --feedback positive

# 自动调优（需要 10+ 条数据）
python3 skills/rag/auto_tune.py --report

# 建议下一个实验
python3 skills/rag/auto_tune.py --next
```

### 自进化功能

```bash
cd skills/self-evolution

# 查看状态
python3 main.py status

# 运行分形思考
python3 main.py fractal --limit 10

# 运行夜间循环
python3 main.py nightly

# 记录进化事件
python3 main.py evolve --type KNOWLEDGE_GAINED --content "系统初始化完成"
```

---

## 📁 目录结构

```
workspace-ai-baby/
├── 🔧 init_system.py          ⭐ 系统初始化
├── 🔧 quick_verify.py         ⭐ 快速验证
├── 🔧 start.sh                ⭐ 查看状态
├── 🔧 separate_config.py      配置分离
│
├── 📄 README.md               工作区说明
├── 📄 GETTING_STARTED.md      本文档
├── 📄 CONFIG_SEPARATION.md    配置分离方案
├── 📄 SECURITY_REPORT.md      安全报告
│
├── 📂 skills/
│   ├── rag/                   RAG 评估系统
│   ├── memory-search/         记忆搜索
│   └── self-evolution/    自进化核心
│
└── 📂 ~/.openclaw/workspace-ai-baby-config/  # 个人配置（Git 忽略）
    ├── config.yaml
    ├── memory/
    └── logs/
```

---

## ✅ 初始化检查清单

运行 `python3 init_system.py` 后，应该看到：

- [ ] ✅ Python 3.9+ 已安装
- [ ] ✅ 依赖包完整（yaml, sqlite3）
- [ ] ✅ 配置目录创建成功
- [ ] ✅ 数据库检查通过
- [ ] ✅ .gitignore 配置正确
- [ ] ✅ 功能测试全部通过

**如果有警告：**
- 按照提示修复
- 重新运行 `python3 init_system.py`

---

## 🔐 配置说明

### 个人配置文件

位置：`~/.openclaw/workspace-ai-baby-config/config.yaml`

```yaml
# 工作区
workspace: /Users/dhr/.openclaw/workspace-ai-baby

# Ollama
ollama:
  enabled: true
  url: http://localhost:11434
  model: nomic-embed-text

# 数据库
database:
  memory_stream: ~/.openclaw/workspace-ai-baby-config/memory/...
  knowledge_base: ~/.openclaw/workspace-ai-baby-config/memory/...

# RAG
rag:
  log_path: ~/.openclaw/workspace-ai-baby-config/logs/...
  top_k: 5
  similarity_threshold: 0.7
```

**⚠️ 注意：** 此文件包含个人配置，不会上传到 Git

---

## 🆘 故障处理

### 问题 1: Python 版本过低

```bash
# 检查版本
python3 --version

# 升级 Python（macOS）
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

# 或手动测试功能
python3 quick_verify.py
```

### 问题 4: 配置加载失败

```bash
# 检查配置文件
cat ~/.openclaw/workspace-ai-baby-config/config.yaml

# 重新创建配置
python3 separate_config.py
```

### 问题 5: Git 提交敏感文件

```bash
# 从 Git 历史移除
git rm --cached -r path/to/sensitive/file

# 提交更改
git commit -m "chore: 移除敏感文件"
```

---

## 📚 更多文档

| 文档 | 说明 |
|------|------|
| **README.md** | 工作区概览 |
| **GETTING_STARTED.md** | 本文档 - 快速开始 |
| **USER_MANUAL.md** | 详细使用手册 |
| **SELF_EVOLUTION_SYSTEM.md** | 自进化体系详解 |
| **CONFIG_SEPARATION.md** | 配置分离方案 |
| **SECURITY_REPORT.md** | 安全报告 |

---

## 🎯 下一步

### 今天
- [x] 运行 `python3 init_system.py`
- [x] 运行 `./start.sh`
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

**完成初始化后，你将拥有：**

✅ 完整的自进化系统  
✅ 安全的配置管理  
✅ RAG 评估能力  
✅ 记忆搜索功能  
✅ 分形思考引擎  

**开始使用吧！**

```bash
python3 init_system.py  # 初始化
./start.sh              # 查看状态
python3 quick_verify.py # 验证功能
```

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23  
**许可证：** MIT
