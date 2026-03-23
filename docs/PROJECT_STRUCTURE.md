# 📁 项目结构规范

**版本：** v5.1  
**更新时间：** 2026-03-23

---

## 🎯 架构原则

### 1. 分离关注点

```
┌─────────────────────────────────────────┐
│         技能层 (Skills)                  │
│  独立功能，可单独使用，有 SKILL.md       │
└─────────────────────────────────────────┘
              ▲ 依赖
┌─────────────────────────────────────────┐
│         库层 (Libs)                      │
│  共享基础设施，被技能依赖，无 SKILL.md   │
└─────────────────────────────────────────┘
```

### 2. 命名规范

| 目录类型 | 命名规范 | 示例 | 原因 |
|----------|----------|------|------|
| **Libs/** | 下划线 `_` | `memory_hub` | Python 包导入规范 |
| **Skills/** | 连字符 `-` | `memory-search` | 人类可读，URL 友好 |

### 3. 导入规则

```python
# Libs (共享库) - 标准 Python 导入
from libs.memory_hub import MemoryHub

# Skills (技能) - 直接导入子模块
import sys
from pathlib import Path
sys.path.insert(0, str(Path('skills') / 'memory-search'))
from search_sqlite import SQLiteMemorySearch
```

---

## 📂 目录结构

### 完整结构

```
workspace-ai-baby/
│
├── libs/                          # 共享库层
│   ├── __init__.py                # 库包入口
│   └── memory_hub/                # 记忆管理中心
│       ├── __init__.py            # 包初始化
│       ├── hub.py                 # 核心接口
│       ├── storage.py             # 存储管理
│       ├── knowledge.py           # 知识管理
│       ├── evaluation.py          # RAG 评估
│       └── models.py              # 数据模型
│
├── skills/                        # 技能层
│   ├── __init__.py                # 技能包入口
│   │
│   ├── memory-search/             # 记忆搜索技能
│   │   ├── SKILL.md               # ⭐ 技能说明
│   │   ├── skill.json             # ⭐ 元数据
│   │   └── search_sqlite.py       # 主入口
│   │
│   ├── rag/                       # RAG 评估技能
│   │   ├── SKILL.md
│   │   ├── skill.json
│   │   └── evaluate.py
│   │
│   ├── self-evolution/            # 自进化技能
│   │   ├── SKILL.md
│   │   ├── skill.json
│   │   └── main.py
│   │
│   ├── aiway/                     # AIWay 社区技能
│   │   ├── SKILL.md
│   │   └── ...
│   │
│   └── websearch/                 # 网页搜索技能
│       ├── SKILL.md
│       └── ...
│
├── scripts/                       # 工具脚本
│   ├── test_agents.py             # Agent 集成测试
│   └── ...
│
├── docs/                          # 文档
│   ├── ARCHITECTURE_v5.1.md       # 架构设计
│   ├── PROJECT_STRUCTURE.md       # 本文件
│   └── ...
│
├── data/                          # 数据目录
│   ├── ai-baby/                   # 主 Agent 数据
│   ├── baby1/                     # Agent 1 数据
│   ├── baby2/                     # Agent 2 数据
│   └── baby3/                     # Agent 3 数据
│
├── public/                        # 公共知识
│   ├── common/                    # 通用知识
│   ├── faq/                       # 常见问题
│   ├── skills/                    # 技能文档
│   └── domain/                    # 领域知识
│
└── memory/                        # 工作记忆
    ├── ai-baby_memory_stream.db
    └── ...
```

---

## 🏷️ 目录规范详解

### Libs/ (共享库)

**定位：** 底层基础设施，被技能依赖

**特点：**
- ❌ 没有 SKILL.md
- ❌ 没有 skill.json
- ✅ 纯代码实现
- ✅ 使用下划线 `_` 命名 (Python 包规范)
- ✅ 支持标准导入：`from libs.memory_hub import MemoryHub`

**示例：**
```
libs/
└── memory_hub/          # ✅ 下划线
    ├── __init__.py      # 包初始化
    ├── hub.py           # 核心类
    └── ...
```

**创建新库：**
1. 在 `libs/` 下创建目录 (使用下划线)
2. 添加 `__init__.py` 导出公共接口
3. 实现核心功能模块
4. 更新 `libs/__init__.py` (可选)

---

### Skills/ (技能)

**定位：** 独立功能，可单独使用

**特点：**
- ✅ 必须有 SKILL.md (技能说明)
- ✅ 必须有 skill.json (元数据)
- ✅ 可以有多个 Python 文件
- ✅ 使用连字符 `-` 命名 (人类友好)
- ✅ 直接执行脚本：`python3 skills/memory-search/search_sqlite.py`

**示例：**
```
skills/
└── memory-search/       # ✅ 连字符
    ├── SKILL.md         # ⭐ 必需
    ├── skill.json       # ⭐ 必需
    └── search_sqlite.py # 主入口
```

**SKILL.md 结构：**
```markdown
---
name: memory_search
description: 记忆搜索技能，支持关键词和语义搜索
homepage: https://github.com/...
metadata:
  emoji: "🧠"
  category: memory
  version: "1.0.0"
---

# 技能说明

功能、用法、示例...
```

**创建新技能：**
1. 在 `skills/` 下创建目录 (使用连字符)
2. 创建 `SKILL.md` (参考其他技能)
3. 创建 `skill.json` (元数据)
4. 实现主入口脚本
5. 测试验证

---

### Scripts/ (工具脚本)

**定位：** 一次性工具、测试脚本

**特点：**
- ❌ 不需要 SKILL.md
- ✅ 直接执行
- ✅ 长期保留
- ✅ 需要版本控制

**示例：**
```
scripts/
├── test_agents.py       # Agent 集成测试
└── ...
```

**注意：** 临时脚本不应放在 `scripts/`，应使用 `temp/` 目录。

---

## 📦 依赖关系

```
┌─────────────────┐
│  memory-search  │
└────────┬────────┘
         │ 使用
         ▼
┌─────────────────┐
│  memory_hub     │  ◄─── 共享库
└─────────────────┘
         ▲
         │ 使用
┌────────┴────────┐
│       rag       │
└─────────────────┘
```

**规则：**
- Skills 可以依赖 Libs
- Skills 之间不应互相依赖
- Libs 不应依赖 Skills

---

## 🔧 导入规范

### 从 Libs 导入

```python
# 方法 1: 标准导入 (推荐)
from libs.memory_hub import MemoryHub

# 方法 2: 添加路径后导入
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.memory_hub import MemoryHub

# 方法 3: 使用 libs 包
from libs import MemoryHub
```

### 从 Skills 导入

```python
# 方法 1: 直接导入子模块 (推荐)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'skills' / 'memory-search'))

from search_sqlite import SQLiteMemorySearch

# 方法 2: 使用技能包
from skills.memory_search import SQLiteMemorySearch
```

---

## ✅ 检查清单

### 创建新 Lib

- [ ] 目录名使用下划线 `_`
- [ ] 添加 `__init__.py` 导出公共接口
- [ ] 实现核心功能
- [ ] 无 SKILL.md (因为是库，不是技能)
- [ ] 测试导入：`from libs.xxx import ...`

### 创建新 Skill

- [ ] 目录名使用连字符 `-`
- [ ] 创建 `SKILL.md`
- [ ] 创建 `skill.json`
- [ ] 实现主入口脚本
- [ ] 测试执行：`python3 skills/xxx/xxx.py`

### 代码审查

- [ ] Libs 使用下划线命名
- [ ] Skills 使用连字符命名
- [ ] 导入路径正确
- [ ] 无循环依赖

---

## 📊 统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **Libs** | 1 个 | memory_hub |
| **Skills** | 5 个 | memory-search, rag, self-evolution, aiway, websearch |
| **Scripts** | 2 个 | test_agents, migrate_data |

---

## 🔄 历史演变

| 时间 | 事件 | 说明 |
|------|------|------|
| 2026-03-23 | 创建 libs/ 目录 | 分离共享库和技能 |
| 2026-03-23 | memory-hub → memory_hub | 移到 libs/，重命名为下划线 |
| 2026-03-23 | 统一命名规范 | Libs 下划线，Skills 连字符 |

---

**维护者：** ai-baby  
**最后更新：** 2026-03-23

---

## 📝 临时脚本管理

### Temp/ (临时脚本目录)

**定位：** 临时脚本、测试代码、一次性工具

**特点：**
- ❌ 不需要 SKILL.md
- ✅ 用完即删
- ✅ 定期清理（建议每周）
- ✅ Git 自动忽略

**命名规范：**

| 方式 | 示例 | 说明 |
|------|------|------|
| **日期命名** | `2026-03-23_test.py` | ✅ 推荐，清晰 |
| **.tmp 后缀** | `debug.tmp.py` | ✅ 明确临时 |
| **描述性** | `test_feature.py` | ⚠️ 需加日期 |

**使用场景：**
- ✅ 临时修复脚本
- ✅ 测试/实验代码
- ✅ 调试工具
- ✅ 一次性数据转换
- ✅ 快速原型验证

**清理规则：**
```bash
# 删除超过 7 天的临时脚本
find temp/ -name "*.py" -mtime +7 -delete

# 删除所有 .tmp 文件
rm temp/*.tmp.py

# 查看临时脚本
ls -lt temp/
```

**工作流：**
```
创建 → 测试 → (有用→迁移 | 无用→删除)
          ↓           ↓
      scripts/    rm temp/xxx.py
```

**示例：**
```bash
# 1. 创建临时脚本
touch temp/2026-03-23_test_embedding.py

# 2. 测试
python3 temp/2026-03-23_test_embedding.py

# 3. 清理
# 有用 → 移到 scripts/
mv temp/2026-03-23_test_embedding.py scripts/test_embedding.py

# 无用 → 删除
rm temp/2026-03-23_test_embedding.py
```

---

---

## 📝 临时脚本管理 (Temp/)

### 定位

**Temp/** 目录专门用于存放临时脚本、测试代码和一次性工具。

| 特性 | 说明 |
|------|------|
| **用途** | 临时脚本、测试代码、调试工具 |
| **保留时间** | < 7 天（建议） |
| **Git** | ❌ 自动忽略（不提交） |
| **清理** | 定期手动或自动清理 |

---

### 命名规范

| 方式 | 示例 | 推荐度 | 说明 |
|------|------|--------|------|
| **日期命名** | `2026-03-23_test_embedding.py` | ⭐⭐⭐ | 最推荐，清晰知道创建时间 |
| **.tmp 后缀** | `debug_memory.tmp.py` | ⭐⭐ | 明确标识为临时文件 |
| **描述性** | `test_new_feature.py` | ⭐ | 建议加上日期前缀 |

**推荐格式：**
```
temp/
├── 2026-03-23_test_embedding.py    # ✅ 日期 + 用途
├── 2026-03-24_migrate_data.tmp.py  # ✅ 日期 + 用途 + .tmp
├── debug_memory.tmp.py             # ✅ 用途 + .tmp
└── test_feature.py                 # ⚠️ 无日期，难判断时效
```

---

### 使用场景

#### ✅ 适合放在 temp/

- 🔧 **临时修复脚本** - 紧急 bug 修复，验证后移到正式位置
- 🧪 **测试/实验代码** - 测试新功能、新 API
- 🐛 **调试工具** - 临时调试脚本、日志分析
- 📝 **一次性数据转换** - 数据迁移、格式转换
- 🚀 **快速原型验证** - PoC、概念验证

#### ❌ 不适合放在 temp/

- 长期使用的工具脚本 → 移到 `scripts/`
- 正式功能代码 → 移到 `skills/` 或 `libs/`
- 重要数据文件 → 移到 `data/`
- 文档 → 移到 `docs/`

---

### 清理规则

#### 自动清理（推荐配置 cron）

```bash
# 每周清理一次，删除超过 7 天的 .py 文件
0 2 * * 0 find /path/to/workspace/temp/ -name "*.py" -mtime +7 -delete

# 每天删除所有 .tmp 文件
0 3 * * * find /path/to/workspace/temp/ -name "*.tmp.py" -delete
```

#### 手动清理

```bash
# 查看临时脚本（按时间排序）
ls -lt temp/

# 查看超过 7 天的文件
find temp/ -name "*.py" -mtime +7 -ls

# 删除超过 7 天的文件
find temp/ -name "*.py" -mtime +7 -delete

# 删除所有 .tmp 文件
rm temp/*.tmp.py

# 清空整个目录
rm temp/*.py
```

---

### 工作流

```
┌──────────────┐
│ 1. 创建脚本   │
│ temp/xxx.py  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 2. 测试/执行 │
│ python3      │
└──────┬───────┘
       │
       ▼
   ┌───┴───┐
   │ 有用？ │
   └───┬───┘
       │
   ┌───┴───┐
   │       │
  是       否
   │       │
   ▼       ▼
┌─────┐ ┌──────┐
│迁移 │ │删除  │
│到   │ │rm    │
│scri │ │temp/ │
│pts/ │ │xxx.py│
└─────┘ └──────┘
```

**示例：**

```bash
# 1. 创建临时脚本（测试 Embedding）
cat > temp/2026-03-23_test_embedding.py << 'EOF'
from libs.memory_hub import MemoryHub
hub = MemoryHub('ai-baby')
print(hub.stats())
EOF

# 2. 执行测试
python3 temp/2026-03-23_test_embedding.py

# 3a. 有用 → 移到 scripts/
mv temp/2026-03-23_test_embedding.py scripts/test_embedding.py

# 3b. 无用 → 删除
rm temp/2026-03-23_test_embedding.py
```

---

### Git 配置

`.gitignore` 已配置：

```gitignore
# 临时文件
temp/
*.tmp
*.bak
*.cache
```

**例外：** `temp/README.md` 可以提交，用于说明目录用途。

---

### 目录结构

```
temp/
├── README.md              # ✅ 提交：使用说明
├── 2026-03-23_test.py     # ❌ 忽略：临时脚本
├── debug.tmp.py           # ❌ 忽略：临时调试
└── data_convert.py        # ❌ 忽略：一次性工具
```

---

### 最佳实践

1. **始终使用日期命名**
   - 方便判断文件时效
   - 便于批量清理（`rm temp/2026-03-*.py`）

2. **添加注释说明用途**
   ```python
   # temp/2026-03-23_test_embedding.py
   # 用途：测试 Memory Hub 的 Embedding 功能
   # 创建：2026-03-23
   # 预计清理：2026-03-30
   ```

3. **定期清理（建议每周）**
   ```bash
   # 周日晚清理
   find temp/ -name "*.py" -mtime +7 -delete
   ```

4. **有用的代码及时迁移**
   - 测试脚本 → `scripts/`
   - 工具函数 → `libs/`
   - 功能模块 → `skills/`

---

### 检查清单

创建临时脚本前：

- [ ] 确认是临时需求（< 7 天）
- [ ] 使用日期命名（`YYYY-MM-DD_xxx.py`）
- [ ] 添加用途注释
- [ ] 执行后及时清理或迁移

每周清理时：

- [ ] 检查超过 7 天的文件
- [ ] 删除无用的临时脚本
- [ ] 迁移有用的代码到正式位置
- [ ] 更新 `temp/README.md`（可选）

---

**最后更新：** 2026-03-23  
**维护者：** ai-baby

