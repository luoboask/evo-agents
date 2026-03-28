# 脚本开发规范 | Script Development Guide

[中文](#中文) | [English](#english)

---

## 中文 {#中文}

### 🎯 路径规范

所有脚本必须使用 `path_utils` 解析路径，支持以下优先级：

1. **环境变量** - `EVO_WORKSPACE` 或 `WORKSPACE_ROOT`
2. **配置文件** - `.install-config`
3. **推导** - 从脚本位置推导（回退）

**示例：**
```python
from path_utils import resolve_workspace, resolve_agent_memory, resolve_data_dir

WORKSPACE = resolve_workspace()
MEMORY_DIR = resolve_agent_memory(args.agent)
DATA_DIR = resolve_data_dir("index")
```

### 🛠️ 创建新脚本

**使用模板生成器：**
```bash
python3 scripts/core/new_script.py my_feature
```

**生成后：**
1. 编辑脚本，替换 `{{description}}` 为实际描述
2. 实现 `main()` 函数中的业务逻辑
3. 测试脚本

**生成文件位置：**
- 核心脚本 → `scripts/core/`
- 用户脚本 → `scripts/user/`（不提交到模板）

### 📋 命令行参数规范

所有脚本必须支持：

| 参数 | 说明 | 必需 |
|------|------|------|
| `--agent` | Agent 名称 | 可选 |
| `--workspace` | 自定义 Workspace 路径 | 可选 |
| `--verbose`, `-v` | 详细输出 | 可选 |
| `--dry-run`, `-n` | 空运行（不实际修改） | 可选 |

### 🧪 测试

```bash
# 查看帮助
python3 scripts/my_script.py --help

# 默认运行
python3 scripts/my_script.py

# 指定 Agent
python3 scripts/my_script.py --agent demo-agent

# 指定 Workspace
EVO_WORKSPACE=/tmp/test python3 scripts/my_script.py

# 或 --workspace 参数
python3 scripts/my_script.py --workspace /tmp/test
```

### 📁 目录结构

```
scripts/
├── core/                    # 核心脚本（模板自带）
│   ├── path_utils.py       # 路径工具
│   ├── new_script.py       # 脚本生成器
│   ├── bridge_sync.py
│   └── ...
├── user/                    # 用户自定义脚本（不提交）
│   └── .gitkeep
└── my_script.py            # 根目录脚本
```

### 🔒 并发安全

所有脚本必须使用 `lock_utils` 防止并发冲突：

```python
from lock_utils import file_lock, md_file_lock, open_db

# 命名文件锁
with file_lock("my_operation"):
    # 安全操作
    pass

# Markdown 文件锁
with md_file_lock(Path("memory/2026-03-28.md")) as f:
    content = f.read()
    # 安全写入
    f.write(new_content)

# SQLite 数据库（自动 WAL 模式）
conn = open_db(Path("data/memory.db"))
```

### 📝 代码模板

```python
#!/usr/bin/env python3
"""
my_script.py - 功能描述

用法:
    python3 scripts/my_script.py [options]
"""
import argparse
import sys
from pathlib import Path

from path_utils import resolve_workspace, resolve_agent_memory, resolve_data_dir
from lock_utils import file_lock, open_db

WORKSPACE = resolve_workspace()


def main():
    parser = argparse.ArgumentParser(description="功能描述")
    parser.add_argument("--agent", help="Agent 名称")
    parser.add_argument("--workspace", help="自定义 Workspace 路径")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--dry-run", "-n", action="store_true")
    args = parser.parse_args()
    
    # 支持 --workspace 覆盖
    if args.workspace:
        global WORKSPACE
        WORKSPACE = Path(args.workspace)
    
    # 获取路径
    memory_dir = resolve_agent_memory(args.agent)
    data_dir = resolve_data_dir()
    
    if args.verbose:
        print(f"Workspace: {WORKSPACE}")
        print(f"Memory: {memory_dir}")
    
    # TODO: 实现业务逻辑
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## English {#english}

### 🎯 Path Convention

All scripts must use `path_utils` for path resolution with the following priority:

1. **Environment variables** - `EVO_WORKSPACE` or `WORKSPACE_ROOT`
2. **Config file** - `.install-config`
3. **Derivation** - From script location (fallback)

**Example:**
```python
from path_utils import resolve_workspace, resolve_agent_memory, resolve_data_dir

WORKSPACE = resolve_workspace()
MEMORY_DIR = resolve_agent_memory(args.agent)
DATA_DIR = resolve_data_dir("index")
```

### 🛠️ Create New Script

**Use template generator:**
```bash
python3 scripts/core/new_script.py my_feature
```

**After generation:**
1. Edit script, replace `{{description}}` with actual description
2. Implement business logic in `main()` function
3. Test the script

**Output location:**
- Core scripts → `scripts/core/`
- User scripts → `scripts/user/` (not committed to template)

### 📋 CLI Arguments Convention

All scripts must support:

| Argument | Description | Required |
|----------|-------------|----------|
| `--agent` | Agent name | Optional |
| `--workspace` | Custom workspace path | Optional |
| `--verbose`, `-v` | Verbose output | Optional |
| `--dry-run`, `-n` | Dry run (no actual changes) | Optional |

### 🧪 Testing

```bash
# View help
python3 scripts/my_script.py --help

# Default run
python3 scripts/my_script.py

# Specify Agent
python3 scripts/my_script.py --agent demo-agent

# Specify Workspace
EVO_WORKSPACE=/tmp/test python3 scripts/my_script.py

# Or --workspace argument
python3 scripts/my_script.py --workspace /tmp/test
```

### 🔒 Concurrency Safety

All scripts must use `lock_utils` to prevent concurrent conflicts:

```python
from lock_utils import file_lock, md_file_lock, open_db

# Named file lock
with file_lock("my_operation"):
    # Safe operation
    pass

# Markdown file lock
with md_file_lock(Path("memory/2026-03-28.md")) as f:
    content = f.read()
    # Safe write
    f.write(new_content)

# SQLite database (WAL mode auto-enabled)
conn = open_db(Path("data/memory.db"))
```

---

**Last updated:** 2026-03-28
