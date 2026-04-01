# 会话隔离与记忆规范

_会话类型、记忆访问权限、数据隔离_

---

## 📊 会话类型

### 1. 主会话 (Main Session)

**定义：** 用户与 Agent 的直接一对一对话

**特征：**
- ✅ 直接聊天（webchat、私聊）
- ✅ 用户与 Agent 单独交互
- ✅ 完整的上下文历史
- ✅ 可以访问私人记忆

**示例：**
```
用户：帮我查一下天气
Agent: 好的，我来查询...
```

---

### 2. 子会话 (Sub-Agent Session)

**定义：** 父 Agent spawn 的子 Agent 执行的独立任务

**特征：**
- ✅ 独立的任务上下文
- ✅ 隔离的记忆空间
- ❌ 不能访问主会话的私人记忆
- ✅ 通过 task 参数接收必要信息

**示例：**
```python
# 父 Agent spawn 子 Agent
subagent = spawn(
    task="帮用户找寿司店（用户喜欢吃寿司）",
    workspace="/path/to/child"
)
```

---

### 3. 群聊会话 (Group Session)

**定义：** 多人群组聊天，Agent 作为参与者之一

**特征：**
- ✅ 多个用户参与
- ✅ 公开的对话内容
- ❌ 不能引用私人记忆
- ❌ 不能泄露其他用户的隐私

**示例：**
```
群聊：
用户 A: 今天天气不错
用户 B: 是啊，适合出去玩
Agent: 👍 （只在被@时回复）
```

---

### 4. 孤立会话 (Isolated Session)

**定义：** 完全隔离的独立执行环境（如 cron 任务）

**特征：**
- ✅ 完全独立的上下文
- ✅ 不继承父会话历史
- ✅ 用于定时任务、后台任务
- ❌ 不能访问私人记忆

**示例：**
```json
{
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行夜间循环"
  }
}
```

---

## 🧠 记忆访问权限

### 权限矩阵

| 记忆类型 | 主会话 | 子会话 | 群聊 | 孤立会话 |
|---------|-------|-------|------|---------|
| `MEMORY.md` | ✅ | ❌ | ❌ | ❌ |
| `memory/YYYY-MM-DD.md` | ✅ | ⚠️ | ❌ | ❌ |
| `data/<agent>/*.db` | ✅ | ✅ (own) | ❌ | ✅ (own) |
| `skills/` | ✅ | ✅ | ✅ | ✅ |
| `docs/` | ✅ | ✅ | ✅ | ✅ |

---

### 详细说明

#### MEMORY.md（长期私人记忆）

**访问规则：**
```python
# ✅ 正确：主会话可以读取
if session_type == "main":
    read("MEMORY.md")

# ❌ 错误：子会话不能读取
if session_type != "main":
    # 不要读取 MEMORY.md
    pass

# ❌ 错误：群聊中不能引用
# 用户（群聊）："我记得之前说过..."
# Agent: 不要引用 MEMORY.md 内容
```

**原因：**
- 包含用户个人隐私
- 只应该在私密对话中使用
- 防止泄露给群聊中的其他人

---

#### memory/YYYY-MM-DD.md（日常记忆）

**访问规则：**
```python
# ✅ 正确：主会话读取今天和昨天的记忆
if session_type == "main":
    read("memory/2026-04-01.md")  # 今天
    read("memory/2026-03-31.md")  # 昨天

# ⚠️ 子会话：一般不读取，除非任务需要
# ❌ 群聊：不读取
```

---

#### data/<agent>/*.db（Agent 专用数据库）

**访问规则：**
```python
# ✅ 正确：每个 Agent 访问自己的数据库
db_path = f"data/{agent_name}/knowledge_base.db"

# ❌ 错误：不要访问其他 Agent 的数据库
# 不要读取 data/other-agent/*.db
```

**隔离机制：**
- 每个 Agent 独立数据库
- 互不干扰
- 可以安全删除（不影响其他 Agent）

---

## 🔄 跨会话知识传递

### 主会话 → 子会话

**方式 1: 通过 task 参数传递**
```python
# ✅ 正确：通过 task 传递必要信息
subagent = spawn(
    task="帮用户找寿司店（用户喜欢吃寿司）",
    workspace="/path/to/child"
)
```

**方式 2: 写入共享文件**
```python
# ✅ 正确：写入共享目录
with open("data/shared/user_preferences.json", "w") as f:
    json.dump({"food_preference": "寿司"}, f)

# 子 Agent 读取
with open("data/shared/user_preferences.json") as f:
    prefs = json.load(f)
```

**❌ 错误：直接共享私人记忆**
```python
# ❌ 不要这样做
subagent = spawn(
    task="...",
    workspace="/path/to/parent"  # 子 Agent 会访问 MEMORY.md
)
```

---

### 子会话 → 主会话

**方式：通过 sessions_yield 返回结果**
```python
# 父 Agent
subagent = spawn(task="...", mode="run")
result = sessions_yield()  # 等待子 Agent 返回

# 父 Agent 将结果记录到私人记忆
memory.record(f"子 Agent 找到：{result}")
```

---

### 群聊 → 主会话

**方式：用户主动提及**
```
群聊：
用户：我记得你之前说过...

主会话：
用户：（继续私聊）
Agent：可以引用私人记忆
```

**❌ 错误：Agent 主动在群聊引用私人记忆**
```
群聊：
用户：今天吃什么？
Agent: 我记得您喜欢吃寿司（❌ 不要这样说）
```

---

## 🛡️ 会话隔离机制

### 上下文隔离

```
主会话：
├── 完整的对话历史
├── 私人记忆访问权限
└── 用户偏好上下文

子会话：
├── 仅任务相关上下文
├── 无私人记忆访问
└── 通过 task 传递的信息

群聊：
├── 仅公开对话内容
├── 无私人记忆访问
└── 不泄露个人隐私

孤立会话：
├── 完全独立上下文
├── 无历史继承
└── 仅任务指令
```

---

### 数据库隔离

```
data/
├── main-agent/
│   ├── memory_stream.db      # 主 Agent 记忆
│   └── knowledge_base.db     # 主 Agent 知识
├── sandbox-agent/
│   ├── memory_stream.db      # 沙箱 Agent 记忆
│   └── knowledge_base.db     # 沙箱 Agent 知识
└── tao-admin/
    ├── memory_stream.db      # 电商 Agent 记忆
    └── knowledge_base.db     # 电商 Agent 知识
```

**规则：**
- ✅ 每个 Agent 访问自己的数据库
- ❌ 不要跨 Agent 访问数据库
- ⚠️ 共享数据需要明确授权

---

## 📝 最佳实践

### 1. 会话类型判断

```python
# 判断当前会话类型
if channel_type == "direct" and not is_group:
    session_type = "main"
elif is_spawned:
    session_type = "sub"
elif is_group:
    session_type = "group"
else:
    session_type = "isolated"

# 根据会话类型决定记忆访问
if session_type == "main":
    read("MEMORY.md")
```

---

### 2. 隐私保护

```python
# ✅ 正确：群聊中不引用私人记忆
# 群聊用户："今天吃什么？"
Agent: "我可以帮你们查附近的餐厅"

# ❌ 错误：泄露私人偏好
Agent: "我记得您喜欢吃寿司"  # 群聊中不要说
```

---

### 3. 子 Agent 信息传递

```python
# ✅ 正确：明确传递必要信息
subagent = spawn(
    task=f"找餐厅（用户偏好：{user_preference}）",
    workspace="/path/to/child"
)

# ❌ 错误：让子 Agent 自己读取私人记忆
subagent = spawn(
    task="找餐厅",
    workspace="/path/to/parent"  # 会访问 MEMORY.md
)
```

---

### 4. 记忆记录

```python
# ✅ 正确：主会话记录到私人记忆
if session_type == "main":
    memory.record("用户喜欢吃寿司")

# ✅ 正确：子会话记录到自己的数据库
if session_type == "sub":
    db.save(task_result)

# ❌ 错误：子会话写入私人记忆
if session_type != "main":
    # 不要写入 MEMORY.md
    pass
```

---

## ⚠️ 安全警告

### 绝对禁止

```
❌ 在群聊中引用 MEMORY.md 内容
❌ 子 Agent 直接访问主 Agent 数据库
❌ 孤立会话访问私人记忆
❌ 跨 Agent 共享私人信息未授权
```

### 必须确认

```
⚠️ 传递私人信息前询问用户
⚠️ 子 Agent 任务完成后清理敏感数据
⚠️ 群聊中不主动提及用户隐私
```

---

## 📊 总结

| 会话类型 | 记忆访问 | 数据访问 | 隐私保护 |
|---------|---------|---------|---------|
| 主会话 | ✅ 全部 | ✅ 自己的 | ✅ 可以引用 |
| 子会话 | ❌ 私人记忆 | ✅ 自己的 | ⚠️ 通过 task 传递 |
| 群聊 | ❌ 私人记忆 | ❌ | ❌ 不能泄露 |
| 孤立会话 | ❌ 私人记忆 | ✅ 自己的 | ❌ 无上下文 |

**核心原则：**
1. **主会话** - 完整权限，可以访问私人记忆
2. **子会话** - 任务隔离，通过 task 传递信息
3. **群聊** - 隐私保护，不引用私人记忆
4. **孤立会话** - 完全独立，无历史继承

---

_版本：1.0.0 | 2026-04-01_
