# 📁 项目结构规范（通用版 / 中文）

**版本：** v6.0  
**适用范围：** 任意 Agent + 任意 workspace  
**定位：** 规范目录分层、命名规则、依赖边界与临时脚本管理

---

## 1. 架构原则

### 1.1 分离关注点

```text
┌─────────────────────────────────────────┐
│          技能层 (skills/)               │
│ 独立能力，可单独调用，包含 SKILL.md      │
└─────────────────────────────────────────┘
                    ▲ 依赖
┌─────────────────────────────────────────┐
│            库层 (libs/)                  │
│ 共享基础设施，被技能依赖，不是技能入口    │
└─────────────────────────────────────────┘
```

### 1.2 运行上下文原则

- 统一通过参数传入上下文：
  - `--workspace <path>`
  - `--agent <name>`
- 不依赖隐式环境上下文。

### 1.3 边界原则

- 只管理传入的 workspace。
- 不管理 `~/.openclaw/agents` 等平台内部目录。

---

## 2. 命名规范

| 目录类型 | 命名规范 | 示例 | 说明 |
|---|---|---|---|
| `libs/` 子目录 | 下划线 `_` | `memory_hub` | 适配包导入约定 |
| `skills/` 子目录 | 连字符 `-` | `memory-search` | 可读性高，文档/URL 友好 |
| `scripts/` 文件 | 动词+对象 | `install_agent_workspace.py` | 明确行为 |
| `docs/` 文件 | 主题命名 | `PROJECT_STRUCTURE_GENERIC_CN.md` | 便于索引 |

---

## 3. 推荐目录结构（通用）

```text
<workspace>/
├── libs/                          # 共享库层
│   └── memory_hub/
│       ├── __init__.py
│       ├── hub.py
│       ├── storage.py
│       ├── knowledge.py
│       ├── evaluation.py
│       └── models.py
│
├── skills/                        # 技能层
│   ├── memory-search/
│   │   ├── SKILL.md
│   │   ├── skill.json
│   │   └── search_sqlite.py
│   ├── rag/
│   │   ├── SKILL.md (可选)
│   │   ├── skill.json
│   │   └── evaluate.py
│   ├── self-evolution/
│   │   ├── SKILL.md (可选)
│   │   ├── skill.json
│   │   └── main.py
│   └── websearch/
│       ├── SKILL.md
│       ├── skill.json
│       └── search.py
│
├── scripts/                       # 工具脚本（安装/升级/测试）
├── docs/                          # 架构/运行/安装文档
├── public/                        # 公共知识
├── data/                          # 按 agent 隔离数据
│   └── <agent>/
│       ├── memory/
│       ├── logs/
│       └── config/
├── .agent-runtime/                # workspace 内运行时元数据
│   └── <agent>/
│       ├── run.sh
│       └── install.json
└── temp/                          # 临时脚本目录（不入库）
```

---

## 4. 目录职责说明

### 4.1 `libs/`（共享库）

- 面向“被复用”的基础能力（存储、模型、评估等）。
- 不作为技能入口，不要求 `SKILL.md`。
- 可被多个技能依赖。

### 4.2 `skills/`（技能）

- 面向“可调用能力”的功能模块。
- 推荐包含：
  - `SKILL.md`（能力说明）
  - `skill.json`（元数据）
  - 一个或多个实现文件

### 4.3 `scripts/`（工具脚本）

- 一次性/运维型入口，例如安装、升级、验收测试。
- 需可重复执行，尽量幂等。

### 4.4 `data/`（数据隔离）

- `data/<agent>/...` 为唯一运行数据边界。
- 不同 agent 之间禁止交叉写入。

### 4.5 `.agent-runtime/`（运行时元数据）

- 存放 run 脚本与安装元信息。
- 仅在当前 workspace 生效。

---

## 5. 依赖关系规则

```text
skills/*  ─────► libs/*
skills/*  ✖────► skills/*   (避免横向强耦合)
libs/*    ✖────► skills/*   (禁止反向依赖)
```

规则：

- 技能可以依赖库。
- 技能之间如需复用，先抽到 `libs/`。
- 库层不能依赖技能层。

---

## 6. 导入与调用规范

### 6.1 库导入（推荐）

```python
from libs.memory_hub import MemoryHub
```

### 6.2 技能调用（推荐参数化）

```bash
python3 skills/memory-search/search_sqlite.py "query" --agent demo-agent
python3 skills/rag/evaluate.py --report --days 7 --agent demo-agent
python3 skills/self-evolution/main.py --agent demo-agent status
```

---

## 7. 临时脚本管理（`temp/`）

### 7.1 使用场景

- 调试脚本
- 一次性迁移
- 快速实验

### 7.2 规则

- 临时脚本放 `temp/`，不要放 `scripts/`。
- 命名建议：`YYYY-MM-DD_xxx.py`。
- 使用后及时迁移或删除。

### 7.3 清理建议

```bash
# 查看临时脚本
ls -lt temp/

# 清理 7 天前脚本（示例）
find temp/ -name "*.py" -mtime +7 -delete
```

---

## 8. 新增模块检查清单

### 新增 Lib

- [ ] 使用下划线命名
- [ ] 提供清晰导出接口（`__init__.py`）
- [ ] 不引入对 `skills/` 的依赖

### 新增 Skill

- [ ] 使用连字符命名
- [ ] 添加 `SKILL.md` 与 `skill.json`
- [ ] 提供参数化入口（至少支持 `--agent`）
- [ ] 不直接依赖其他 skill 实现文件

### 代码审查

- [ ] 分层职责清晰
- [ ] 依赖方向正确
- [ ] 路径与上下文由参数显式传入

---

## 9. 总结

这个通用结构的目标是：

1. **能力可复用**（共享 `skills/` + `libs/`）
2. **数据可隔离**（`data/<agent>/`）
3. **运行可控**（显式 `workspace + agent` 参数）
4. **边界清晰**（仅管理当前 workspace）
