# 记忆容量管理使用指南

> 灵感来自 Hermes Agent 的记忆系统设计

## 📊 容量限制

| 文件 | 限制 | 约等于 | 用途 |
|------|------|--------|------|
| `MEMORY.md` | 2,200 chars | ~800 tokens | Agent 的个人笔记 |
| `USER.md` | 1,375 chars | ~500 tokens | 用户画像和偏好 |

**为什么有限制？**
- 保持系统 prompt 大小可控
- 强制只保存最重要的信息
- 提高 token 使用效率
- 避免上下文膨胀

---

## 🔧 API 使用

### 1. 获取使用率

```python
from libs.memory_hub.hub import MemoryHub

hub = MemoryHub(agent_name='main')

# MEMORY.md 使用率
memory_usage = hub.get_memory_usage()
print(memory_usage)
# {
#   'current': 1474,
#   'limit': 2200,
#   'percentage': 67.0,
#   'available': 726
# }

# USER.md 使用率
user_usage = hub.get_user_usage()
print(user_usage)
# {
#   'current': 475,
#   'limit': 1375,
#   'percentage': 34.5,
#   'available': 900
# }
```

### 2. 检查是否可以添加

```python
# 检查容量
check = hub.check_memory_capacity("新记忆内容...")
print(check)
# {
#   'can_add': True,
#   'current': 1474,
#   'limit': 2200,
#   'new_would_fit': True,
#   'usage': '1,474/2,200'
# }

if not check['new_would_fit']:
    print("⚠️  记忆空间不足，需要先压缩")
```

### 3. 系统 Prompt 显示

```python
# 格式化显示（用于系统 prompt）
display = hub.format_memory_usage_display()
print(display)
```

**输出示例:**
```
══════════════════════════════════════════════
MEMORY (your personal notes) [67% — 1,474/2,200 chars] [█████████████░░░░░░░░░]
══════════════════════════════════════════════

══════════════════════════════════════════════
USER PROFILE [34% — 475/1,375 chars] [██████░░░░░░░░░░░░░░]
══════════════════════════════════════════════
```

---

## 📐 压缩策略

### 何时压缩？

- **> 80%** — 开始考虑压缩
- **> 90%** — 应该压缩
- **> 100%** — 必须压缩（已超限）

### 压缩方法

#### 1. 合并相关条目

**压缩前:**
```
- User prefers Python 3.12
- User uses pyproject.toml for project config
- User's default editor is nvim
- User works on project "atlas"
```

**压缩后:**
```
User runs Python 3.12 with pyproject.toml, edits in nvim, working on "atlas" project.
```

#### 2. 移除冗余描述

**压缩前:**
```
On January 5th, 2026, the user asked me to look at their project which is
located at ~/code/api. I discovered it uses Go version 1.22 and...
```

**压缩后:**
```
Project ~/code/api uses Go 1.22. (2026-01-05)
```

#### 3. 移到 references/

对于详细的配置、代码示例等：

```bash
# 创建引用文档
mkdir -p references/
# 将详细内容移到 references/api-config.md
# MEMORY.md 只保留摘要和引用
```

**MEMORY.md:**
```
API 配置详见 references/api-config.md
- Base URL: https://api.example.com
- Auth: OAuth2
- Rate limit: 1000/hour
```

---

## 🛠️ 工具使用

### 压缩工具

```bash
# 预览模式（不实际修改）
python3 scripts/compress_memory.py --dry-run

# 执行压缩（会创建备份）
python3 scripts/compress_memory.py
```

### 输出示例

```
============================================================
MEMORY.md 压缩工具
============================================================

📊 分析 MEMORY.md...
   总字符数：2,668
   限制：2,200
   超出：468 chars
   章节数：9

💡 压缩建议:
⚠️  超出限制 468 字符

📌 建议压缩以下大章节:
   - 🚨 重要规则：GitHub 推送规范：1,288 chars (48.3%)
   - 技能：505 chars (18.9%)
   - 重要事件：455 chars (17.1%)

💡 压缩策略:
   1. 移除冗余描述和重复信息
   2. 合并相关的短条目
   3. 删除过时的上下文
   4. 使用更简洁的表达方式
   5. 将详细信息移到 references/ 目录
```

---

## 📝 最佳实践

### ✅ 好的记忆条目

```markdown
# 紧凑、信息密集
User runs macOS 14 Sonoma, uses Homebrew, has Docker Desktop and Podman. 
Shell: zsh with oh-my-zsh. Editor: VS Code with Vim keybindings.

# 具体、可操作的约定
Project ~/code/api uses Go 1.22, sqlc for DB queries, chi router. 
Run tests with 'make test'. CI via GitHub Actions.

# 带上下文的经验教训
The staging server (10.0.1.50) needs SSH port 2222, not 22. 
Key is at ~/.ssh/staging_ed25519.
```

### ❌ 避免的记忆条目

```markdown
# 太模糊
User has a project.

# 太冗长
On January 5th, 2026, the user asked me to look at their project which is
located at ~/code/api. I discovered it uses Go version 1.22 and the user
prefers to run tests using make command...

# 原始数据.dump
[大量代码块、日志文件、数据表格]
```

---

## 🔄 工作流

### 日常使用

1. **Agent 自动保存** — Agent 在学习到新信息时自动添加到记忆
2. **容量检查** — 每次添加前检查 `check_memory_capacity()`
3. **超限警告** — 如果超限，返回错误提示用户压缩

### 定期维护

**每周检查:**
```bash
# 查看使用率
python3 libs/memory_hub/test_capacity.py

# 如需要，压缩
python3 scripts/compress_memory.py
```

**每月清理:**
1. 回顾 MEMORY.md 所有章节
2. 删除过时的上下文
3. 合并相关条目
4. 将详细信息移到 references/

---

## 🎯 与 Hermes Agent 对比

| 特性 | Hermes Agent | evo-agents (本实现) |
|------|--------------|---------------------|
| MEMORY 限制 | 2,200 chars | ✅ 2,200 chars |
| USER 限制 | 1,375 chars | ✅ 1,375 chars |
| 使用率显示 | ✅ [67% — 1,474/2,200] | ✅ 相同格式 |
| 进度条 | ✅ [████████░░] | ✅ 相同样式 |
| 容量检查 | ✅ add 前检查 | ✅ 相同逻辑 |
| 自动压缩 | ❌ 手动 | ✅ 工具辅助 |
|  substring 匹配 | ✅ replace/remove | 🔄 待实现 |

---

## 📚 相关文件

- `hub.py` — MemoryHub 主类（添加容量管理方法）
- `test_capacity.py` — 测试脚本
- `scripts/compress_memory.py` — 压缩工具
- 本文件 — 使用指南

---

## 🚀 下一步

1. ✅ 容量限制和使用率计算
2. ✅ 系统 prompt 显示格式
3. ✅ 压缩工具
4. 🔄 实现 substring 匹配（replace/remove）
5. 🔄 集成到自进化系统（自动触发压缩）
6. 🔄 添加记忆质量评分

---

**灵感来源:** [Hermes Agent - Persistent Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
