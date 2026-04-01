# Agent 完整规则清单

_从 Agent 工作生命周期角度整理_

---

## 📋 规则矩阵

| 阶段 | 规则 | 状态 | 文档 |
|------|------|------|------|
| 启动 | 读取哪些文件 | ✅ 已有 | AGENTS.md |
| 启动 | 技能使用规则 | ✅ 已有 | SKILL_RULES.md |
| 启动 | Workspace 规范 | ✅ 已有 | WORKSPACE_RULES.md |
| 会话中 | 工具使用权限 | ⚠️ 需补充 | - |
| 会话中 | 文件操作规范 | ⚠️ 需补充 | - |
| 会话中 | 与用户交互 | ✅ 已有 | AGENTS.md |
| 会话中 | 多 Agent 协作 | ⚠️ 需补充 | - |
| 会话结束 | 记忆保存 | ✅ 已有 | AGENTS.md |
| 会话结束 | 状态清理 | ⚠️ 需补充 | - |
| 定期任务 | 心跳检查 | ✅ 已有 | HEARTBEAT.md |
| 定期任务 | 夜间循环 | ✅ 已有 | SCHEDULER.md |
| 错误处理 | 失败恢复 | ⚠️ 需补充 | - |

---

## ⚠️ 需要补充的规则

### 1. 工具使用权限

**当前状态：** 分散在 AGENTS.md 和 RULES.md

**需要明确：**
```
工具使用权限：

✅ 可以自主使用：
- read (读取文件)
- web_search (搜索)
- web_fetch (抓取网页)
- memory_search (搜索记忆)
- sessions_list (查看会话)

⚠️ 需要确认：
- exec (执行命令) - 特别是 rm、delete、sudo
- edit (编辑文件) - 特别是系统文件
- write (写入文件) - 特别是覆盖已有文件
- sessions_send (发送消息到其他会话)

❌ 禁止使用：
- 未授权的工具
- 超出权限的工具
```

---

### 2. 文件操作规范

**当前状态：** 只有 Workspace 规则，缺少操作细节

**需要补充：**
```
文件操作规范：

创建文件：
- ✅ 在 docs/、scripts/、memory/ 目录可以创建
- ⚠️ 在根目录创建需要确认
- ❌ 不要在 .git/、.openclaw/ 目录创建

编辑文件：
- ✅ 可以编辑自己创建的文件
- ⚠️ 编辑用户文件需要确认
- ❌ 不要编辑系统配置文件

删除文件：
- ❌ 绝对不要主动删除
- ✅ 用户明确说"删除"时执行
- ⚠️ 优先使用 trash 而非 rm

移动/复制文件：
- ✅ 整理文件到正确目录
- ⚠️ 移动用户文件需要确认
```

---

### 3. 多 Agent 协作

**当前状态：** 缺少规范

**需要补充：**
```
多 Agent 协作规则：

Spawn 子 Agent：
- ✅ 独立任务可以 spawn
- ✅ 使用 inherit workspace 继承规则
- ⚠️ 独立 workspace 需要配置规则
- ⚠️ 设置合理的 timeout

通信规则：
- ✅ sessions_send 发送消息
- ✅ sessions_yield 等待结果
- ⚠️ 避免频繁轮询
- ❌ 不要在子 Agent 中泄露敏感信息

权限继承：
- 子 Agent 继承父 Agent 的规则
- 子 Agent 不能突破父 Agent 权限
- 子 Agent 的规则文档需要复制
```

---

### 4. 错误处理

**当前状态：** 缺少规范

**需要补充：**
```
错误处理规范：

命令执行失败：
1. 检查错误信息
2. 尝试替代方案
3. 报告用户并建议

文件操作失败：
1. 检查权限
2. 检查路径
3. 报告用户

网络请求失败：
1. 重试 1-2 次
2. 检查网络连接
3. 报告用户

记忆系统失败：
1. 降级到文件存储
2. 记录错误日志
3. 报告用户

通用原则：
- 不要隐藏错误
- 提供替代方案
- 记录错误上下文
```

---

### 5. 资源管理

**当前状态：** 缺少规范

**需要补充：**
```
资源管理规范：

Token 管理：
- 避免过长的上下文
- 定期清理会话历史
- 重要信息写入文件

超时管理：
- exec 设置合理 timeout
- 长任务使用后台执行
- 定期报告进度

并发管理：
- 避免同时执行多个长任务
- 子 Agent 数量限制
- 数据库并发访问注意

存储管理：
- 定期清理 /tmp/
- 记忆文件定期归档
- 日志文件限制大小
```

---

### 6. 会话管理

**当前状态：** 分散

**需要补充：**
```
会话管理规范：

会话开始：
1. 读取 AGENTS.md
2. 读取 SOUL.md、USER.md
3. 读取 memory/ 文件
4. 检查 HEARTBEAT.md

会话中：
1. 记录重要交互到记忆
2. 完成任务后 evolve 记录
3. 不确定时询问用户

会话结束：
1. 保存当前状态
2. 更新记忆文件
3. 清理临时文件

长会话管理：
- 定期总结进度
- 分段保存结果
- 避免上下文过长
```

---

## 📝 建议补充的文档

### docs/TOOL_USAGE.md
```markdown
# 工具使用规范

## 权限分级

### 自由使用
- read, web_search, web_fetch
- memory_search, memory_get
- sessions_list, sessions_history

### 需要确认
- exec (特别是 rm、sudo、delete)
- edit (系统文件、用户文件)
- write (覆盖已有文件)
- sessions_send (跨会话消息)

### 禁止使用
- 未授权的工具
- 超出权限的操作
```

### docs/ERROR_HANDLING.md
```markdown
# 错误处理规范

## 处理流程
1. 分析错误原因
2. 尝试替代方案
3. 记录错误上下文
4. 报告用户

## 常见错误
- 权限不足
- 文件不存在
- 网络超时
- 资源限制
```

### docs/MULTI_AGENT.md
```markdown
# 多 Agent 协作规范

## Spawn 规则
- 何时 spawn 子 Agent
- 如何配置 workspace
- 权限继承规则

## 通信规则
- sessions_send 使用场景
- sessions_yield 等待结果
- 避免频繁轮询
```

---

## 🎯 优先级排序

### ⭐⭐⭐⭐⭐ 必须补充
1. **工具使用权限** - exec、edit、write 的权限边界
2. **文件操作规范** - 创建、编辑、删除的详细规则
3. **错误处理** - 失败时如何应对

### ⭐⭐⭐⭐ 重要
4. **多 Agent 协作** - spawn、通信、权限继承
5. **会话管理** - 开始、进行中、结束的规范

### ⭐⭐⭐ 建议
6. **资源管理** - token、超时、并发、存储

---

## 📊 完整规则体系

```
docs/
├── SKILL_RULES.md          ✅ 技能使用
├── WORKSPACE_RULES.md      ✅ 目录结构、文件存放
├── SCHEDULER.md            ✅ 定时任务
├── TOOL_USAGE.md           ⚠️ 工具权限（需创建）
├── ERROR_HANDLING.md       ⚠️ 错误处理（需创建）
├── MULTI_AGENT.md          ⚠️ 多 Agent 协作（需创建）
└── AGENT_RULES_INDEX.md    ✅ 规则索引
```

---

## 🔧 更新 AGENTS.md

在现有基础上添加：

```markdown
### 🛠️ Tool Usage

| Tool | Permission |
|------|-----------|
| read, web_search | ✅ Free |
| exec (rm/sudo) | ⚠️ Confirm |
| edit, write | ⚠️ Confirm |

**Full rules:** See `docs/TOOL_USAGE.md`

### ⚠️ Error Handling

1. Analyze error
2. Try alternatives
3. Report to user

**Full rules:** See `docs/ERROR_HANDLING.md`
```

---

_版本：1.0.0 | 2026-04-01_
