# evo-agents 记忆系统 vs OpenClaw 原生系统

_两个记忆系统的定位、差异和互补关系_

---

## 📊 核心差异对比

| 特性 | OpenClaw 原生 | evo-agents |
|------|------------|-----------|
| **定位** | 会话管理器 | 个人长期助手 |
| **记录内容** | 所有对话 | 重要事件 |
| **隔离级别** | 会话级别 | Agent 级别 |
| **记录方式** | 自动 | 手动/自动 |
| **记忆类型** | 对话历史 | 知识/反思/洞察 |
| **重要性评分** | ❌ 不支持 | ✅ 自动评估 |
| **跨会话连续** | ❌ 不支持 | ✅ 支持 |
| **隐私保护** | ✅ 强（会话隔离） | ⚠️ 弱（共享记忆） |

---

## 🏗️ 架构对比

### OpenClaw 原生系统

```
~/.openclaw/agents/<agent>/
├── sessions/
│   ├── session-id-1.jsonl    ← 会话 1（独立）
│   ├── session-id-2.jsonl    ← 会话 2（独立）
│   └── session-id-3.jsonl    ← 会话 3（独立）
└── memory/
    └── agent_memory_stream.db
```

**特点：**
- ✅ 每个会话独立文件
- ✅ 会话间完全隔离
- ✅ Gateway 自动管理
- ✅ 保护隐私

---

### evo-agents 系统

```
~/.openclaw/workspace-<agent>/
├── memory/
│   ├── 2026-04-01.md         ← 所有会话共享（按日期）
│   ├── 2026-04-02.md         ← 所有会话共享（按日期）
│   └── knowledge_base.db     ← 所有会话共享
└── data/<agent>/memory/
    └── memory_stream.db      ← 所有会话共享
```

**特点：**
- ❌ 没有会话概念
- ✅ 所有会话共享记忆
- ✅ 跨会话连续性
- ✅ 长期知识积累

---

## 📝 记录内容对比

### OpenClaw 原生记录

**记录所有对话：**

```json
// sessions/session-xxx.jsonl
{"role": "user", "content": "帮我查天气"}
{"role": "assistant", "content": "今天晴朗..."}

{"role": "user", "content": "中午吃什么？"}
{"role": "assistant", "content": "推荐寿司..."}
```

**特点：**
- 完整对话历史
- 无需手动调用
- 会话结束自动保存

---

### evo-agents 记录

**只记录重要事件：**

```python
# 手动记录
evolve(
    type="KNOWLEDGE_GAINED",
    content="学习了 RAG 评估系统",
    importance=6.5
)

# 自动记录（夜间循环）
- 系统改进发现
- 反思和洞察
- 知识整合
```

**实际数据库记录：**

```sql
-- memory_stream.db
observation | "系统重装完成" | 7.0
observation | "cron jobs 已配置" | 5.5
reflection | "发现代码 bug 模式" | 6.0
```

**特点：**
- 重要性 ≥ 5.0 才记录
- 包含反思和洞察
- 支持知识结构化

---

## 🔄 实际工作流程

### 用户提问场景

```
用户："我之前说过我喜欢吃什么？"
    ↓
【1】Agent 启动
    ↓
【2】搜索 evo-agents 记忆
    → memory/2026-04-01.md: "用户喜欢吃寿司"
    → knowledge_base.db: "偏好：日料"
    ↓
【3】OpenClaw 检索会话
    → sessions/session-xxx.jsonl: "3 月 20 日提到喜欢三文鱼"
    ↓
【4】综合回答
    "你之前说过喜欢吃寿司，特别是三文鱼！"
```

---

## 🎯 使用场景

### OpenClaw 原生适合

| 场景 | 说明 |
|------|------|
| **查找对话历史** | "上周我说了什么？" |
| **会话隔离** | 多用户/敏感对话 |
| **完整记录** | 审计/追溯需求 |
| **自动备份** | 无需手动管理 |

---

### evo-agents 适合

| 场景 | 说明 |
|------|------|
| **长期记忆** | "我的兴趣爱好是什么？" |
| **知识积累** | 学习记录、技能提升 |
| **反思洞察** | 深度思考、模式识别 |
| **系统进化** | 自动改进、夜间循环 |

---

## 💡 互补设计

### 为什么需要两个系统？

| 需求 | OpenClaw | evo-agents | 解决方案 |
|------|---------|-----------|---------|
| **完整对话记录** | ✅ | ❌ | OpenClaw |
| **重要事件提取** | ❌ | ✅ | evo-agents |
| **会话隐私** | ✅ | ❌ | OpenClaw |
| **跨会话连续** | ❌ | ✅ | evo-agents |
| **反思洞察** | ❌ | ✅ | evo-agents |
| **自动记录** | ✅ | ⚠️ | OpenClaw |

**结论：** 两个系统互补，无需整合！

---

## 📋 记录标准

### evo-agents 记录条件

**重要性评分系统：**

```python
if importance >= 7.0:  # 关键事件
    → 记录到 MEMORY.md + knowledge_base.db
elif importance >= 5.0:  # 重要事件
    → 记录到 memory_stream.db
else:  # 普通事件
    → 不记录（OpenClaw 已记录）
```

**会记录的事件：**
- ✅ 系统配置变更（重要性 7.0）
- ✅ 学习新知识（重要性 6.5）
- ✅ 发现 bug 模式（重要性 6.0）
- ✅ 完成任务（重要性 5.5）

**不会记录：**
- ❌ 日常对话（OpenClaw 已记录）
- ❌ 简单命令（无学习价值）
- ❌ 闲聊（无长期价值）

---

## 🔧 技术实现

### OpenClaw 原生

```python
# Gateway 自动管理
def on_message(role, content):
    session_file.write({
        "role": role,
        "content": content,
        "timestamp": now()
    })
```

---

### evo-agents

```python
# 手动/自动调用
def evolve(type, content, importance):
    if importance >= 5.0:
        memory_stream.add({
            "type": type,
            "content": content,
            "importance": importance,
            "timestamp": now()
        })
    
    if importance >= 7.0:
        knowledge_base.save(content)
```

---

## 📊 数据量对比

### 典型使用场景

| 时间跨度 | OpenClaw | evo-agents |
|---------|---------|-----------|
| **1 天** | ~100 条对话 | ~5 条重要事件 |
| **1 周** | ~700 条对话 | ~30 条重要事件 |
| **1 月** | ~3000 条对话 | ~100 条重要事件 |
| **压缩率** | 100% | ~49%（夜间循环） |

---

## 🎯 最佳实践

### 什么时候使用哪个？

**查找对话：**
```bash
# 使用 OpenClaw 原生
openclaw sessions --agent my-agent
```

**查找知识：**
```bash
# 使用 evo-agents
python3 skills/memory-search/search.py "RAG 配置"
```

**记录重要事件：**
```bash
# 使用 evo-agents
python3 skills/self-evolution/main.py evolve \
    --type KNOWLEDGE_GAINED \
    --content "学会了新技能"
```

---

## 📝 总结

### 两个系统的关系

```
OpenClaw 原生          evo-agents
     ↓                    ↓
记录所有对话        提取重要事件
     ↓                    ↓
会话隔离            跨会话连续
     ↓                    ↓
    互补使用，无需整合！
```

### 核心差异

1. **定位不同**
   - OpenClaw：会话管理器
   - evo-agents：长期记忆助手

2. **记录标准不同**
   - OpenClaw：所有对话
   - evo-agents：重要性 ≥ 5.0

3. **隔离级别不同**
   - OpenClaw：会话级别
   - evo-agents：Agent 级别

4. **功能互补**
   - OpenClaw：隐私保护
   - evo-agents：知识积累

---

_版本：1.0.0 | 更新：2026-04-01_
