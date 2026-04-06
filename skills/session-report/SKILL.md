---
name: session-report
description: 从当前会话提取长期有价值的知识，存入记忆系统（用户偏好、项目决策、可复用模式）
author: evo-agents
version: 1.0.0
tags: [memory, knowledge, reflection, report]
disable-model-invocation: false
---

# /session-report - 会话总结报告

> **核心理念**: 会话隔离 ≠ 知识丢失  
> **目标**: 提取跨会话有价值的知识，丢弃临时状态

---

## ⚠️ 核心原则

### ✅ 应该保存的（长期价值）

| 类型 | 示例 | 去向 |
|------|------|------|
| **用户偏好** | "我不喜欢冗长回复"、"偏好 TypeScript" | MEMORY.md (Feedback) |
| **项目决策** | "选择 Redis 因为缓存需求"、"冻结合并直到发布" | MEMORY.md (Project) |
| **外部资源** | "API 文档在 api.example.com" | MEMORY.md (Reference) |
| **用户角色** | "我是数据科学家"、"负责后端开发" | MEMORY.md (User) |
| **工作流指导** | "测试必须用真实数据库" | MEMORY.md (Feedback) |
| **不可推导的知识** | "法律合规要求这个实现方式" | MEMORY.md (Project) |

### ❌ 应该丢弃的（临时状态）

| 类型 | 示例 | 原因 |
|------|------|------|
| **任务状态** | "正在修复 bug #123" | 会话特定，很快过时 |
| **中间代码** | 未完成的实现 | 代码库是权威来源 |
| **一次性对话** | "帮我看看这个文件" | 无普遍价值 |
| **可推导信息** | Git 提交、文件结构 | `git log` / 代码可查 |
| **调试过程** | "试了 A 不行，试 B" | 解决方案已在代码中 |

---

## 🎯 何时使用

### ✅ 适合场景

- 完成了重要任务或项目里程碑
- 做出了关键架构决策并有明确原因
- 发现了新的知识点、坑或 workaround
- 用户给出了工作方式指导（纠正或确认）
- 了解了用户的角色、偏好或目标
- 会话即将结束，想保留精华内容

### ❌ 不适合场景

- 只是临时调试，没有普遍价值
- 任务还在进行中，状态频繁变化
- 纯聊天或简单问答，没有实质性内容
- 涉及敏感信息（密码、密钥等）

---

## 📋 执行流程

### Step 1: 回顾会话历史

```python
# 获取当前会话的对话记录
messages = get_session_history(limit=100)
```

**注意**: 
- 只回顾当前会话，不读取其他会话
- 保持会话隔离性
- 如果会话太长，聚焦最近 20-50 条消息

---

### Step 2: 识别候选内容

使用以下过滤规则：

#### 第 1 层：临时 vs 长期

```python
def is_long_term_value(message):
    """判断是否有长期价值"""
    # ❌ 临时状态
    if contains_temporal_refs(message):  # "现在"、"今天"、"这个 bug"
        return False
    if is_task_status(message):  # "正在做 X"
        return False
    
    # ✅ 长期知识
    if is_user_preference(message):  # "我偏好..."
        return True
    if is_project_decision(message):  # "我们决定..."
        return True
    if is_external_reference(message):  # "文档在..."
        return True
    
    return False
```

#### 第 2 层：私人 vs 共享

```python
def determine_scope(content):
    """确定作用域"""
    if is_personal_preference(content):
        return 'private'  # 用户记忆
    elif is_team_convention(content):
        return 'team'     # 团队记忆
    else:
        return 'project'  # 项目记忆
```

#### 第 3 层：可推导 vs 不可推导

```python
def is_deriviable_from_code(content):
    """判断是否可从代码推导"""
    # ❌ 这些不应该保存（代码/工具可查）
    if is_file_structure(content):      # 文件列表
        return True
    if is_git_history(content):         # 提交历史
        return True
    if is_code_pattern_obvious(content): # 明显的代码模式
        return True
    
    # ✅ 这些应该保存（不可推导）
    # - 决策原因（为什么选 A 不选 B）
    # - 用户偏好（沟通风格）
    # - 外部依赖（第三方系统位置）
    # - 历史教训（过去踩过的坑）
    return False
```

---

### Step 3: 生成结构化报告

```markdown
## Session Report - {日期时间}

### 🧠 新知识（建议保存）

#### User Memory（用户记忆）
- {用户角色/偏好/目标}

#### Feedback Memory（反馈记忆）
- {工作方式指导 + Why + How to apply}

#### Project Memory（项目记忆）
- {项目决策/目标/事件 + Why + How to apply}

#### Reference Memory（参考记忆）
- {外部资源位置 + 用途}

### 💡 可复用模式
- {可复用的代码模式/工具类}

### ❌ 已丢弃（临时状态）
- {临时任务状态}
- {中间代码片段}
- {一次性对话}

### 📊 统计
- 审查消息数：{N}
- 建议保存：{M} 条
- 已丢弃：{K} 条
```

---

### Step 4: 用户确认（关键！）

```markdown
📋 Session Report 预览

我分析了本次会话的 {N} 条消息，发现以下内容值得保存：

**✅ 建议保存 ({M} 项):**

1. **[User Memory]** 用户偏好 TypeScript 而非 JavaScript
   - 来源：用户说"我更喜欢 TS，类型安全"
   - 作用域：私有
   
2. **[Project Memory]** 选择方案 A（Redis 缓存）因为 QPS 需求
   - 来源：架构讨论，提到"QPS 提升 3 倍"
   - 作用域：团队
   - Why: 性能要求
   - How to apply: 新 API 都应该加缓存层

3. **[Reference Memory]** API 文档在 https://api.example.com/v2
   - 来源：用户分享链接
   - 作用域：团队

**❌ 已丢弃 (临时状态):**
- Bug 修复 #123 的进度（任务特定）
- 中间的代码修改尝试（代码库可查）
- 调试过程的试错记录（解决方案已实现）

---
**操作:**
- `y` 或 `确认` - 保存上述内容到记忆系统
- `n` 或 `取消` - 不保存任何内容
- `edit` - 手动编辑要保存的内容
- `show N` - 查看第 N 项的详细内容
```

**关键设计**:
- ✅ 明确列出每项的来源
- ✅ 标注作用域（私有/团队）
- ✅ 说明为什么值得保存
- ✅ 用户可以逐项审查
- ✅ 默认不保存，需要明确确认

---

### Step 5: 写入记忆系统

根据用户确认和类型调用相应接口：

```python
def save_to_memory(items, user_confirmed):
    for item in items:
        if not user_confirmed.get(item.id, False):
            continue  # 跳过未确认的
        
        if item.type == 'user':
            save_user_memory({
                'name': item.name,
                'description': item.description,
                'content': format_user_memory(item)
            })
        
        elif item.type == 'feedback':
            save_feedback_memory({
                'name': item.name,
                'description': item.description,
                'content': f"{item.rule}\n\n**Why:** {item.why}\n\n**How to apply:** {item.how}"
            })
        
        elif item.type == 'project':
            save_project_memory({
                'name': item.name,
                'description': item.description,
                'content': f"{item.fact}\n\n**Why:** {item.why}\n\n**How to apply:** {item.how}"
            })
        
        elif item.type == 'reference':
            save_reference_memory({
                'name': item.name,
                'description': item.description,
                'content': item.location
            })
    
    return f"✅ 成功保存 {count} 条记忆"
```

---

## 🔒 安全与隐私

### 🚫 绝对禁止保存

- 🔐 API keys、密码、token
- 🔐 用户个人信息（邮箱、电话、地址）
- 🔐 内部系统地址（除非用户明确允许）
- 🔐 未公开的商业模式或机密
- 🔐 第三方保密信息

### 🎯 作用域控制

| 内容类型 | 作用域 | 存储位置 | 可见性 |
|----------|--------|----------|--------|
| 个人偏好 | Private | `MEMORY.md` | 仅主会话 |
| 用户角色 | Private | `MEMORY.md` | 仅主会话 |
| 项目决策 | Team | `MEMORY.md` | 团队成员 |
| 外部资源 | Team | `MEMORY.md` | 团队成员 |

### ⚠️ 检查清单

在保存前自动检查：
- [ ] 不包含敏感词（password, secret, key, token）
- [ ] 不包含完整 URL（除非是公开文档）
- [ ] 不包含文件路径（除非是公共配置）
- [ ] 作用域标注正确
- [ ] 用户已明确确认

---

## 🛠️ 命令参数

```bash
# 完整流程（回顾→筛选→确认→保存）
/session-report

# 只生成报告，不保存（dry run）
/session-report --dry-run

# 强制保存（跳过确认，慎用！）
/session-report --force

# 只保存特定类型
/session-report --type user       # 只保存用户记忆
/session-report --type feedback   # 只保存反馈记忆
/session-report --type project    # 只保存项目记忆
/session-report --type reference  # 只保存参考记忆

# 指定目标记忆文件
/session-report --target memory/YYYY-MM-DD.md

# 限制回顾的消息数
/session-report --limit 50

# 导出为 Markdown 文件
/session-report --export report.md
```

---

## 📊 与会话隔离的关系

### 不破坏隔离的设计

```
┌─────────────┐              ┌─────────────┐
│   会话 A     │              │   会话 B     │
│             │              │             │
│ 临时状态     │              │ 临时状态     │
│ (bug #123)  │              │ (feature X) │
│    ↓        │              │    ↓        │
│   丢弃 ❌    │              │   丢弃 ❌    │
│             │              │             │
│ 长期知识     │              │             │
│ (用户偏好)   │              │             │
│    ↓        │              │    ↑        │
│  MEMORY.md  ├──────────────┤             │
│             │   共享知识    │             │
└─────────────┘              └─────────────┘

隔离的是：临时状态、任务上下文、中间过程
共享的是：用户偏好、项目决策、外部资源
```

### 反而增强隔离的价值

| 没有 session-report | 有 session-report |
|---------------------|-------------------|
| 会话结束后一切归零 | 知识沉淀下来 |
| 每次重新解释背景 | 未来会话自动获得背景 |
| 同样的错误犯两次 | 从历史经验学习 |
| 隔离=孤立 | 隔离但互联 |

---

## 🔄 与其他技能配合

### 与 memory-search

```
/session-report              memory-search
     │                            │
     ▼                            ▼
写入记忆系统  ─────────────→  检索记忆
     │                            │
     └──────────────┬─────────────┘
                    │
                    ▼
          未来会话自动获得背景知识
```

**协同效应**:
- `session-report` 负责**写入**高质量记忆
- `memory-search` 负责**读取**相关记忆
- 形成完整的记忆闭环

---

### 与 self-evolution

```
/session-report              self-evolution
     │                            │
     ▼                            ▼
提取经验教训  ─────────────→  进化 Agent 行为
     │                            │
     └──────────────┬─────────────┘
                    │
                    ▼
          Agent 越来越符合用户偏好
```

**协同效应**:
- `session-report` 发现模式（"用户总是纠正 X"）
- `self-evolution` 调整行为（减少 X 行为）

---

### 与 project-explorer（待创建）

```
project-explorer           /session-report
     │                            │
     ▼                            ▼
分析代码库  ─────────────→  保存发现
     │                            │
     └──────────────┬─────────────┘
                    │
                    ▼
          形成完整的项目知识库
```

---

## ⚠️ 常见误区与避免方法

### ❌ 误区 1: 保存所有对话

**错误做法**:
```markdown
用户：帮我修一下这个 bug
AI: 好的，正在查看...
用户：怎么样了？
AI: 找到了，是空指针...

→ 全部保存 ❌
```

**正确做法**:
```markdown
从对话中提取:
- [Project Memory] User 服务有空指针风险，需加 null 检查 ✅
- [Feedback Memory] 用户希望主动报告问题，不要等询问 ✅

丢弃:
- 临时对话流程 ❌
```

---

### ❌ 误区 2: 过度总结

**错误做法**:
```markdown
保存："用户今天问了 3 个问题，分别是 A、B、C"
```

**问题**: 这是会话状态，不是长期知识

**正确做法**:
```markdown
保存："用户偏好先了解背景再给解决方案"（从 3 个问题中抽象出的模式）
```

---

### ❌ 误区 3: 不区分作用域

**错误做法**:
```markdown
把所有内容都保存到项目记忆
```

**问题**: 个人偏好污染项目空间

**正确做法**:
```markdown
个人偏好 → User Memory（私有）
项目约定 → Project Memory（团队）
```

---

### ❌ 误区 4: 跳过用户确认

**错误做法**:
```python
# 自动保存所有内容
save_to_memory(extracted_items)  # ❌
```

**正确做法**:
```python
# 先生成预览
preview = generate_preview(extracted_items)

# 用户确认
if user_confirms(preview):
    save_to_memory(extracted_items)  # ✅
```

---

## 📝 记忆格式模板

### User Memory 格式

```markdown
---
name: 用户角色与偏好
type: user
scope: private
---

**角色**: 数据科学家，专注于可观测性/logging 领域

**技术背景**:
- 精通 Python 和 SQL
- 熟悉数据管道和 ETL
- 有机器学习项目经验

**沟通偏好**:
- 喜欢详细的技术解释
- 偏好代码示例
- 重视性能和安全考虑

**如何应用**:
解释问题时应该：
- 使用数据分析相关的类比
- 强调日志和监控的最佳实践
- 提供可量化的结果
- 优先推荐 Python 解决方案
```

---

### Feedback Memory 格式

```markdown
---
name: 测试必须用真实数据库
type: feedback
scope: team
---

集成测试必须 hit 真实数据库，不能使用 mock。

**Why**: 
去年 mock 测试通过但生产迁移失败，mock/生产差异掩盖了损坏的迁移。
具体事件：Q4 发布时，mock 的数据库测试全部通过，但生产迁移因字段类型不匹配失败，
导致 2 小时停机。

**How to apply**:
- 所有集成测试必须配置真实数据库连接
- 使用测试数据库（非生产）
- 单元测试可以 mock
- 端到端测试必须真实环境
- CI/CD 配置中启用真实数据库
```

---

### Project Memory 格式

```markdown
---
name: 移动端发布冻结
type: project
scope: team
---

2026-03-05 后冻结所有非关键合并，直到移动端发布完成。

**Why**: 
移动端团队需要稳定的代码库进行最终测试和发布准备。
任何非关键变更都可能引入回归 bug，影响发布计划。

**How to apply**:
- 标记所有新 PR 为"on hold"，除非是关键 bug 修复
- 告知团队成员冻结期
- 发布完成后解冻（预计 2026-03-12）
- 紧急修复需要移动端负责人批准
```

---

### Reference Memory 格式

```markdown
---
name: Linear 项目追踪
type: reference
scope: team
---

管道相关的 bug 和需求追踪在 Linear 项目 "INGEST" 中。

**URL**: https://linear.app/company/project/INGEST

**用途**:
- 所有管道 bug 都应该创建在这个项目
- 需求优先级在这个项目中管理
- 每周状态更新同步到这里

**相关团队**:
- 数据平台团队（主要维护）
- 后端团队（协作者）
```

---

## 🎯 最佳实践

### ✅ 应该做的

1. **及时总结** - 会话结束后立即运行，记忆犹新
2. **宁缺毋滥** - 只保存真正有价值的内容
3. **明确原因** - 每条记忆都要有 Why 和 How to apply
4. **定期回顾** - 每月检查记忆，更新或删除过时的
5. **用户主导** - 让用户决定什么值得保存

### ❌ 不应该做的

1. **不要自动保存** - 总是需要用户确认
2. **不要保存细节** - 保存模式和原则，不是具体对话
3. **不要重复** - 先检查是否已有类似记忆
4. **不要过时** - 项目决策变化后及时更新
5. **不要敏感** - 绝不保存密码、密钥等

---

## 🔧 故障排查

### 问题 1: 找不到会话历史

**可能原因**:
- 会话已过期或被清理
- 权限不足无法读取历史

**解决方法**:
```bash
# 检查会话状态
openclaw sessions list

# 手动指定会话
/session-report --session <session-id>
```

---

### 问题 2: 提取内容太多

**可能原因**:
- 会话太长，包含大量临时对话
- 过滤规则不够严格

**解决方法**:
```bash
# 限制回顾的消息数
/session-report --limit 30

# 只关注特定类型
/session-report --type feedback --type project
```

---

### 问题 3: 用户不确定是否保存

**建议**:
- 使用 `--dry-run` 先预览
- 逐条审查 (`show N`)
- 从保守开始，以后可以补充

---

## 📈 效果评估

### 短期效果（1-2 周）

- ✅ 重要决策不再遗忘
- ✅ 减少重复解释背景
- ✅ 用户感到被理解

### 中期效果（1-2 月）

- ✅ 形成项目知识库
- ✅ 新成员快速上手
- ✅ 同样错误不犯第二次

### 长期效果（3 月+）

- ✅ Agent 行为高度个性化
- ✅ 团队协作效率提升
- ✅ 知识资产持续积累

---

_最后更新：2026-04-06_  
_版本：1.0.0_
