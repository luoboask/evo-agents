# scripts/core/ 脚本清单

[English](#english) | [中文](#中文)

---

## English {#english}

### ✅ Core Scripts (Required)

| Script | Purpose | Keep? |
|--------|---------|-------|
| **activate-features.sh** | Activate advanced features (Ollama, RAG, etc.) | ✅ Yes |
| **add-agent.sh** | Add single sub-agent | ✅ Yes |
| **setup-multi-agent.sh** | Add multiple sub-agents at once | ✅ Yes |
| **cleanup.sh** | Clean build artifacts (node_modules, __pycache__, etc.) | ✅ Yes |
| **session_recorder.py** | Record chat sessions to memory | ✅ Yes |

### ⚠️ Optional Scripts (Feature-specific)

| Script | Purpose | Keep? |
|--------|---------|-------|
| **restore-backup.sh** | Restore workspace from backup | ⚠️ Optional |
| **health_check.py** | System health check | ⚠️ Optional |
| **memory_compressor.py** | Compress old memory files | ⚠️ If using memory system |
| **memory_indexer.py** | Index memory for search | ⚠️ If using semantic search |
| **memory_stats.py** | Memory statistics | ⚠️ If using memory system |
| **unified_search.py** | Search across memory | ⚠️ If using search |

### ❌ Deprecated Scripts (Can Remove)

| Script | Purpose | Status |
|--------|---------|--------|
| **init_system.py** | Old system initialization | ❌ Deprecated |
| **install_agent_workspace.py** | Old agent installer | ❌ Replaced by install.sh |
| **test-multi-agent.sh** | Test multi-agent setup | ❌ Rarely used |
| **test_all.py** | Run all tests | ❌ Development only |
| **uninstall_agent_workspace.py** | Uninstall agent | ❌ Rarely used |
| **upgrade_agent_workspace.py** | Upgrade workspace | ❌ Rarely used |

### 🔧 Utility Scripts (Internal Use)

| Script | Purpose | Keep? |
|--------|---------|-------|
| **lock_utils.py** | File locking utilities | ✅ If used by other scripts |

### 📁 Subdirectories

| Directory | Purpose | Keep? |
|-----------|---------|-------|
| **bridge/** | Memory bridge (SQLite ↔ Markdown) | ⚠️ If using memory system |

---

## 中文 {#中文}

### ✅ 核心脚本（必须）

| 脚本 | 用途 | 保留？ |
|------|------|--------|
| **activate-features.sh** | 激活高级功能（Ollama, RAG 等） | ✅ 是 |
| **add-agent.sh** | 添加单个子 Agent | ✅ 是 |
| **setup-multi-agent.sh** | 批量添加子 Agent | ✅ 是 |
| **cleanup.sh** | 清理构建产物 | ✅ 是 |
| **session_recorder.py** | 记录会话到记忆 | ✅ 是 |

### ⚠️ 可选脚本（特定功能）

| 脚本 | 用途 | 保留？ |
|------|------|--------|
| **restore-backup.sh** | 恢复备份 | ⚠️ 可选 |
| **health_check.py** | 系统健康检查 | ⚠️ 可选 |
| **memory_compressor.py** | 压缩旧记忆文件 | ⚠️ 使用记忆系统时 |
| **memory_indexer.py** | 索引记忆用于搜索 | ⚠️ 使用语义搜索时 |
| **memory_stats.py** | 记忆统计 | ⚠️ 使用记忆系统时 |
| **unified_search.py** | 搜索记忆 | ⚠️ 使用搜索时 |

### ❌ 已废弃脚本（可删除）

| 脚本 | 用途 | 状态 |
|------|------|------|
| **init_system.py** | 旧系统初始化 | ❌ 已废弃 |
| **install_agent_workspace.py** | 旧 Agent 安装器 | ❌ 被 install.sh 替代 |
| **test-multi-agent.sh** | 测试多 Agent 设置 | ❌ 很少使用 |
| **test_all.py** | 运行所有测试 | ❌ 仅开发用 |
| **uninstall_agent_workspace.py** | 卸载 Agent | ❌ 很少使用 |
| **upgrade_agent_workspace.py** | 升级 workspace | ❌ 很少使用 |

### 🔧 工具脚本（内部使用）

| 脚本 | 用途 | 保留？ |
|------|------|--------|
| **lock_utils.py** | 文件锁工具 | ✅ 如果其他脚本使用 |

### 📁 子目录

| 目录 | 用途 | 保留？ |
|------|------|--------|
| **bridge/** | 记忆桥接（SQLite ↔ Markdown） | ⚠️ 使用记忆系统时 |

---

## 📋 建议

### 保留的核心脚本（5 个）
```
scripts/core/
├── activate-features.sh      # 激活功能
├── add-agent.sh              # 添加 Agent
├── setup-multi-agent.sh      # 批量添加 Agent
├── cleanup.sh                # 清理
└── session_recorder.py       # 记录会话
```

### 可选的脚本（根据功能）
```
scripts/core/
├── restore-backup.sh         # 备份恢复
├── health_check.py           # 健康检查
├── memory_*.py               # 记忆系统相关
└── unified_search.py         # 搜索
```

### 可以删除的脚本（6 个）
```
scripts/core/
├── init_system.py            ❌
├── install_agent_workspace.py ❌
├── test-multi-agent.sh       ❌
├── test_all.py               ❌
└── uninstall_agent_workspace.py ❌
└── upgrade_agent_workspace.py ❌
```

---

## 🗑️ 清理命令

**删除已废弃的脚本：**
```bash
cd scripts/core/

# 删除已废弃的脚本
rm -f init_system.py
rm -f install_agent_workspace.py
rm -f test-multi-agent.sh
rm -f test_all.py
rm -f uninstall_agent_workspace.py
rm -f upgrade_agent_workspace.py

# 可选：删除不常用的工具
rm -f health_check.py
rm -f restore-backup.sh
```

---

## 📊 脚本分类总结

| 类别 | 数量 | 说明 |
|------|------|------|
| ✅ 核心 | 5 | 必须保留 |
| ⚠️ 可选 | 6 | 根据功能保留 |
| ❌ 废弃 | 6 | 可以删除 |
| 🔧 工具 | 1 | 内部使用 |
| **总计** | **18** | |

---

**建议：删除 6 个已废弃脚本，保留核心和常用脚本**

### 🗑️ Uninstall Scripts (New)

| Script | Purpose | Keep? |
|--------|---------|-------|
| **uninstall-agent.sh** | Uninstall sub-agent | ✅ Yes |
| **uninstall-workspace.sh** | Uninstall entire workspace | ✅ Yes |

