# Workspace 自检指南 | Self-Check Guide

[中文](#中文) | [English](#english)

---

## 中文 {#中文}

### 🎯 什么是自检？

自检脚本帮助 Agent 自主检测 Workspace 的完整性，发现潜在问题并提供修复建议。

### 🛠️ 使用方法

**快速检查：**
```bash
cd ~/.openclaw/workspace-my-agent
python3 scripts/core/self_check.py
```

**完整检查：**
```bash
python3 scripts/core/self_check.py --full
```

**自动修复（推荐）：**
```bash
# 先预览
python3 scripts/core/self_check.py --dry-run

# 执行修复
python3 scripts/core/self_check.py --fix
```

**生成 JSON 报告：**
```bash
python3 scripts/core/self_check.py --report
```

### 📋 检查项目

| 类别 | 检查项 | 说明 |
|------|--------|------|
| **目录结构** | scripts/core, scripts/user, skills, docs, memory, data, config, public | 关键目录是否存在 |
| **关键文件** | README.md, install.sh, path_utils.py, uninstall-workspace.sh | 核心文件是否存在 |
| **运行时数据** | scripts/data, scripts/memory | 检测不应该存在的目录 |
| **Git 配置** | .git 目录，.gitignore | Git 仓库配置 |
| **OpenClaw** | 注册状态 | 是否已注册到 OpenClaw |
| **路径系统** | path_utils 功能 | 路径解析是否正常 |
| **技能** | memory-search, rag, self-evolution, web-knowledge | 通用技能完整性 |
| **数据库** | memory_index.db | 索引数据库健康 |

### 🔍 输出说明

**通过：** `✅ 目录：scripts/core: 核心脚本目录 存在`

**警告：** `⚠️ 异常目录：scripts/data: 脚本运行时数据目录 不应该存在`

**错误：** `❌ 文件：README.md: 主文档 不存在`

### 🔧 自动修复

**可自动修复的问题：**

| 问题类型 | 修复方式 |
|---------|---------|
| 缺失目录 | 创建目录 + .gitkeep |
| 异常目录 | 删除目录（如 scripts/data） |
| data/ 脏数据 | 清理非 .gitkeep 文件 |
| 索引数据库损坏 | 运行 memory_indexer.py --full |

**修复流程：**
```bash
# 1. 预览（推荐先看）
python3 scripts/core/self_check.py --dry-run

# 输出示例：
#   📝 [预览] 创建目录：memory
#   📝 [预览] 删除目录：scripts/data

# 2. 执行修复
python3 scripts/core/self_check.py --fix

# 输出示例：
#   ✅ 已创建目录：memory
#   ✅ 已删除目录：scripts/data
#   ✅ 已修复：2 个问题
```

### 📊 JSON 报告示例

```json
{
  "timestamp": "2026-03-28T09:30:00",
  "workspace": "/Users/dhr/.openclaw/workspace-my-agent",
  "total": 25,
  "passed": 24,
  "failed": 1,
  "errors": 1,
  "warnings": 0,
  "results": [...]
}
```

### 🤖 Agent 自动自检

Agent 可以在以下时机自动执行自检：

1. **启动时** - 检测环境完整性
2. **心跳检查** - 定期检查
3. **执行敏感操作前** - 确保环境正常
4. **发现问题时** - 自动修复

**示例代码：**
```python
import subprocess
import json

# 自动修复模式
result = subprocess.run(
    ["python3", "scripts/core/self_check.py", "--fix", "--report"],
    capture_output=True,
    text=True
)
report = json.loads(result.stdout)

if report["errors"] > 0:
    print(f"⚠️ 发现 {report['errors']} 个无法修复的错误")
    for r in report["results"]:
        if not r["passed"] and r["severity"] == "error":
            print(f"  - {r['name']}: {r['suggestion']}")
elif report["warnings"] > 0:
    print(f"✅ 已修复所有可修复的问题，还有 {report['warnings']} 个警告")
else:
    print(f"✅ Workspace 状态良好，已修复 {report.get('fixed', 0)} 个问题")
```

---

## English {#english}

### 🎯 What is Self-Check?

Self-check script helps Agent autonomously detect Workspace integrity issues and provide fix suggestions.

### 🛠️ Usage

**Quick check:**
```bash
cd ~/.openclaw/workspace-my-agent
python3 scripts/core/self_check.py
```

**Full check:**
```bash
python3 scripts/core/self_check.py --full
```

**Generate JSON report:**
```bash
python3 scripts/core/self_check.py --report
```

### 📋 Check Items

| Category | Items | Description |
|----------|-------|-------------|
| **Directory Structure** | scripts/core, scripts/user, skills, docs, etc. | Critical directories |
| **Critical Files** | README.md, install.sh, path_utils.py, etc. | Core files |
| **Runtime Data** | scripts/data, scripts/memory | Detect forbidden directories |
| **Git Config** | .git, .gitignore | Git repository |
| **OpenClaw** | Registration status | Registered to OpenClaw |
| **Path System** | path_utils functionality | Path resolution |
| **Skills** | memory-search, rag, self-evolution, web-knowledge | Universal skills |
| **Database** | memory_index.db | Index database health |

### 🤖 Agent Auto Self-Check

Agent can automatically run self-check:

1. **On startup** - Detect environment integrity
2. **Heartbeat** - Periodic checks
3. **Before sensitive operations** - Ensure environment is healthy

---

**Last updated:** 2026-03-28
