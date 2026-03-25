# self-reflection - 自我反思系统安装指南

**基于反思层的自我进化系统：记录交互、提取教训、持续改进。**

> 📝 交互记录 | 💡 教训提取 | 📊 反思分析 | 🔄 持续改进

---

## ⚡ 一键安装（推荐）

技能已预装，只需验证和测试：

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/self-reflection

# 2. 测试模块导入
python3 -c "from reflection import SelfReflection; print('✅ 模块加载成功')"

# 3. 测试运行
python3 -c "
from reflection import SelfReflection
sr = SelfReflection()
print('✅ 自我反思系统初始化成功')
"
```

**就这么简单！** 技能已预装，无需额外依赖。

---

## 📋 安装前检查

### 必需

- ✅ Python 3.9+ 
- ✅ SQLite3（通常已预装）
- ✅ 约 5MB 磁盘空间

### 可选

- ⭕ 无其他依赖

---

## 🚀 详细安装步骤

### Step 1: 验证技能文件

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/self-reflection/

# 应该看到：
# reflection.py, auto_reflection.py, auto_evolve.py, evolution_control.py,
# improvement_generator.py, predictive_maintenance.py, triggers.py
```

### Step 2: 检查 Python 依赖

```bash
# Python 版本
python3 --version  # 需要 3.9+

# SQLite3
python3 -c "import sqlite3; print('SQLite3:', sqlite3.version)"

# 测试模块导入
python3 -c "from reflection import SelfReflection; print('✅ SelfReflection 加载成功')"
```

### Step 3: 测试运行

```bash
cd ~/.openclaw/workspace/skills/self-reflection

# 测试初始化
python3 -c "
from reflection import SelfReflection
sr = SelfReflection()
print('✅ 自我反思系统初始化成功')
print(f'学习目录：{sr.learning_dir}')
"
```

---

## 🔧 配置说明

### 数据路径配置

编辑 `reflection.py` 中的数据路径（如需要）：

```python
# 默认配置
self.workspace = Path("/Users/dhr/.openclaw/workspace")
self.learning_dir = self.workspace / "memory" / "learning"
self.learning_dir.mkdir(parents=True, exist_ok=True)
```

### 反思文件命名

反思文件按日期存储：

```
memory/learning/
├── reflections_2026-03-22.jsonl
├── reflections_2026-03-23.jsonl
└── ...
```

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/skills/self-reflection/
├── reflection.py           # 自我反思核心模块
├── auto_reflection.py      # 自动反思
├── auto_evolve.py          # 自动进化
├── evolution_control.py    # 进化控制中心
├── improvement_generator.py # 改进建议生成
├── predictive_maintenance.py # 预测性维护
├── triggers.py             # 触发器
└── INSTALL.md              # 本文件

数据目录（自动创建）：
~/.openclaw/workspace/memory/learning/
├── reflections_YYYY-MM-DD.jsonl  # 每日反思
└── improvements/                 # 改进建议
```

---

## 🎯 使用方法

### Python 调用

```python
from reflection import SelfReflection

# 初始化
sr = SelfReflection()

# 记录交互反思
reflection = sr.log_interaction(
    task_type="web_search",
    tools_used=["websearch", "memory-search"],
    success=True,
    duration=2.5,
    notes="搜索成功，但响应时间较长"
)

print(f"教训：{reflection['lessons']}")

# 查询反思
reflections = sr.get_reflections_by_date("2026-03-22")
for r in reflections:
    print(f"[{r['timestamp']}] {r['task_type']}: {r['lessons']}")
```

### 自动反思

```python
from auto_reflection import AutoReflection

ar = AutoReflection()

# 自动分析最近的交互并生成反思
ar.analyze_recent(limit=10)
```

### 进化控制

```bash
# 一键完整检查
python3 evolution_control.py full-check

# 生成改进建议
python3 evolution_control.py generate-improvements

# 查看系统状态
python3 evolution_control.py status
```

---

## 📊 反思数据结构

```json
{
  "timestamp": "2026-03-22T02:07:00",
  "task_type": "web_search",
  "tools_used": ["websearch", "memory-search"],
  "success": true,
  "duration_seconds": 2.5,
  "notes": "搜索成功，但响应时间较长",
  "lessons": [
    "需要优化网络请求超时设置",
    "考虑添加缓存机制"
  ]
}
```

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 测试模块导入
cd ~/.openclaw/workspace/skills/self-reflection
python3 -c "from reflection import SelfReflection; print('✅ 加载成功')"

# 2. 测试基本操作
python3 -c "
from reflection import SelfReflection
sr = SelfReflection()
reflection = sr.log_interaction('test', ['test'], True, 1.0, '安装验证')
print(f'✅ 基本操作成功，教训数：{len(reflection[\"lessons\"])}')
"

# 3. 检查学习目录
ls -la ~/.openclaw/workspace/memory/learning/
```

---

## 🎯 使用场景

### 场景 1: 任务完成后记录反思

```python
from reflection import SelfReflection

sr = SelfReflection()

# 完成任务后
sr.log_interaction(
    task_type="skill_installation",
    tools_used=["write", "exec"],
    success=True,
    duration=120,
    notes="成功为所有技能创建了 INSTALL.md 文档"
)
```

### 场景 2: 分析失败原因

```python
# 失败任务后
sr.log_interaction(
    task_type="web_search",
    tools_used=["websearch"],
    success=False,
    duration=30,
    notes="网络连接超时"
)

# 系统会自动提取教训：
# - 失败类型：web_search
# - 需要改进工具使用或任务理解
# - 网络连接问题需要处理
```

### 场景 3: 每日反思回顾

```bash
# 运行每日反思
python3 auto_reflection.py --daily

# 生成改进建议
python3 improvement_generator.py
```

---

## ❓ 常见问题

### Q: 导入模块失败

**A:** 检查 Python 路径：

```bash
cd ~/.openclaw/workspace/skills/self-reflection
python3 -c "import sys; print(sys.path)"
```

### Q: 学习目录不存在

**A:** 首次运行时会自动创建：

```bash
python3 -c "
from reflection import SelfReflection
sr = SelfReflection()
print(f'学习目录：{sr.learning_dir}')
"
```

### Q: 如何查看历史反思？

**A:** 查看反思文件：

```bash
# 查看今日反思
cat ~/.openclaw/workspace/memory/learning/reflections_$(date +%Y-%m-%d).jsonl

# 查看所有反思文件
ls -la ~/.openclaw/workspace/memory/learning/
```

### Q: 如何备份反思数据？

**A:** 备份学习目录：

```bash
cp -r ~/.openclaw/workspace/memory/learning \
   /path/to/backup/learning-$(date +%Y%m%d)
```

### Q: self-reflection 和 memory-search 有什么区别？

**A:** 

| 功能 | self-reflection | memory-search |
|------|-----------------|---------------|
| 主要用途 | 反思和改进 | 记忆存储和检索 |
| 数据类型 | 交互反思、教训 | 会话记忆、知识 |
| 分析方式 | 教训提取 | 关键词/语义搜索 |
| 输出 | 改进建议 | 搜索结果 |

**建议：** 两者配合使用，self-reflection 负责分析改进，memory-search 负责记忆检索。

### Q: 如何卸载技能？

**A:** 删除技能目录（数据保留）：

```bash
rm -rf ~/.openclaw/workspace/skills/self-reflection
```

---

## 📚 相关技能

| 技能 | 说明 |
|------|------|
| **self-reflection** | 自我反思系统 |
| **memory-search** | 记忆搜索检索 |
| **evolution-workbench** | 进化监控仪表板 |

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **INSTALL.md** | 本文件 - 安装指南 |
| **reflection.py** | 反思核心模块（内嵌文档） |
| **auto_reflection.py** | 自动反思模块 |
| **evolution_control.py** | 进化控制中心 |

---

## 🆘 获取帮助

遇到问题？

1. 运行测试命令验证安装
2. 检查 Python 模块导入
3. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建独立安装文档
- **2026-03-17**: self-reflection 技能创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
