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
- ✅ 使用下划线或连字符均可

**示例：**
```
scripts/
├── test_agents.py       # Agent 测试
├── migrate_data.py      # 数据迁移
└── ...
```

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
