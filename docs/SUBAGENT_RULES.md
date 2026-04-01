# 子 Agent 规则

_子 Agent 与主 Agent 的异同_

---

## 🎯 核心原则

**子 Agent 继承父 Agent 的规则，但有特殊限制。**

---

## 📊 规则对比

| 规则 | 主 Agent | 子 Agent | 说明 |
|------|---------|---------|------|
| **技能使用** | ✅ 全部 | ✅ 全部 | 同样的技能规则 |
| **Workspace 规范** | ✅ 全部 | ✅ 全部 | 同样的文件存放规则 |
| **知识库管理** | ✅ 全部 | ⚠️ 受限 | 不能访问私人知识库 |
| **行为边界** | ✅ 全部 | ✅ 全部 | 同样的安全规则 |
| **定时任务** | ✅ 执行 | ❌ 不执行 | 子 Agent 不执行定时任务 |
| **心跳检查** | ✅ 执行 | ❌ 不执行 | 子 Agent 不响应心跳 |

---

## 🧠 知识库访问权限

### 主 Agent

```
✅ skills/          # 公共知识库
✅ docs/            # 公共文档
✅ MEMORY.md        # 私人知识库
✅ memory/*.md      # 日常记忆
✅ data/main-agent/ # 自己的数据库
```

### 子 Agent

```
✅ skills/          # 公共知识库
✅ docs/            # 公共文档
❌ MEMORY.md        # 私人知识库（禁止访问）
❌ memory/*.md      # 日常记忆（禁止访问）
✅ data/<agent>/    # 自己的数据库
```

### 为什么？

- **私人记忆** 可能包含用户隐私，子 Agent 不应该知道
- **任务隔离** 子 Agent 只知道自己任务相关的信息
- **安全边界** 防止子 Agent 泄露私人信息到群聊

---

## 🔄 知识传递方式

### ❌ 错误：直接共享数据库

```python
# 不要这样做
subagent = spawn(
    task="...",
    workspace="/path/to/parent"  # 子 Agent 会访问 MEMORY.md
)
```

### ✅ 正确：通过任务描述传递

```python
# 正确做法
subagent = spawn(
    task="帮用户找寿司店（用户喜欢吃寿司）",  # 通过 task 传递必要信息
    workspace="/path/to/child"  # 独立 workspace
)
```

### ✅ 正确：继承 workspace 但遵守规则

```python
# 继承 workspace（共享技能/文档）
subagent = spawn(
    task="处理这个任务",
    workspace="/path/to/parent",  # 继承同样的 skills/docs
    # 但子 Agent 不会读取 MEMORY.md
)
```

---

## 📋 子 Agent 特殊规则

### 1. 不读取私人记忆

```python
# 子 Agent 启动时：
# ❌ 不要读取 MEMORY.md
# ❌ 不要读取 memory/*.md
# ✅ 读取 AGENTS.md
# ✅ 读取 SOUL.md
# ✅ 读取 skills/ 文档
```

### 2. 只知道自己任务

```python
# 子 Agent 只知道：
# ✅ 父 Agent 通过 task 传递的信息
# ✅ 公共知识库（skills/, docs/）
# ✅ 自己的数据库（data/<agent>/）

# ❌ 不知道：
# - 用户的私人偏好（除非 task 中明确说明）
# - 主 Agent 的历史对话
# - 其他 Agent 的数据
```

### 3. 任务完成后汇报

```python
# 子 Agent 完成任务后：
# ✅ 通过 sessions_yield 返回结果
# ✅ 清理临时文件
# ✅ 保存必要数据到自己的数据库

# ❌ 不要：
# - 修改主 Agent 的数据库
# - 写入 MEMORY.md
# - 泄露私人信息
```

---

## 🛠️ Spawn 子 Agent 指南

### 场景 1: 继承 workspace（推荐）

```python
# 适用：短期任务，需要同样技能
subagent = spawn(
    task="帮我搜索最新的技术新闻",
    workspace="/path/to/parent",  # 继承 skills/docs
    mode="run"  # 一次性任务
)
```

**特点：**
- ✅ 共享同样的技能和文档
- ✅ 配置简单
- ⚠️ 子 Agent 需要遵守规则（不读取 MEMORY.md）

### 场景 2: 独立 workspace

```python
# 适用：长期运行的子 Agent
subagent = spawn(
    task="管理电商后台",
    workspace="/path/to/child",  # 独立 workspace
    mode="session"  # 持久会话
)
```

**特点：**
- ✅ 完全隔离
- ✅ 独立数据库
- ⚠️ 需要单独配置规则文档

### 场景 3: 传递私人信息

```python
# 适用：需要让子 Agent 知道用户偏好
user_preference = read("MEMORY.md").get("food_preference")

subagent = spawn(
    task=f"帮用户找餐厅（用户喜欢：{user_preference}）",
    workspace="/path/to/child"
)
```

**特点：**
- ✅ 通过 task 传递必要信息
- ✅ 不直接共享数据库
- ✅ 用户明确授权

---

## ⚠️ 安全警告

### 绝对禁止

```
❌ 子 Agent 读取 MEMORY.md
❌ 子 Agent 访问主 Agent 数据库
❌ 子 Agent 在群聊中引用私人信息
❌ 父 Agent 把私人数据写入共享目录
```

### 必须确认

```
⚠️ 传递私人信息前询问用户
⚠️ 子 Agent 任务完成后清理数据
⚠️ 独立 workspace 的子 Agent 配置规则文档
```

---

## 📝 AGENTS.md 配置

### 主 Agent

```markdown
# AGENTS.md

## Session Startup
1. Read SOUL.md
2. Read USER.md
3. Read memory/YYYY-MM-DD.md
4. Read MEMORY.md (main session only)  ← 主会话才读

### 🧠 Knowledge Base Rules
| Type | Location | Access |
|------|----------|--------|
| Public | skills/, docs/ | All Agents |
| Private | MEMORY.md | Main session only |  ← 仅主会话
| Agent | data/<agent>/ | Own Agent |
```

### 子 Agent

**同样的 AGENTS.md，但子 Agent 看到 `Main session only` 会知道：**

```
我是子 Agent → 不是主会话 → 不读取 MEMORY.md
```

---

## 🎯 总结

### 子 Agent 感知什么？

| 内容 | 是否感知 | 说明 |
|------|---------|------|
| 技能使用规则 | ✅ 同样 | 同样的 SKILL_RULES.md |
| Workspace 规范 | ✅ 同样 | 同样的 WORKSPACE_RULES.md |
| 知识库分类 | ✅ 同样 | 知道三类知识库 |
| 访问权限 | ⚠️ 受限 | 不能访问私人知识库 |
| 定时任务 | ❌ 不执行 | 子 Agent 不响应心跳/cron |
| 私人记忆 | ❌ 不知道 | 除非 task 中明确传递 |

### 核心原则

1. **规则相同** - 子 Agent 遵守同样的行为规范
2. **权限受限** - 不能访问私人知识库
3. **任务隔离** - 只知道自己的任务
4. **安全传递** - 通过 task 传递必要信息

---

_版本：1.0.0 | 2026-04-01_
