# Agent 技能规则配置

_让 Agent 和子 Agent 自动感知技能使用规则_

---

## 🎯 核心机制

**Agent 启动时自动读取 `AGENTS.md`**，所以只需：

1. **AGENTS.md 包含规则引用** → Agent 启动时会看到
2. **子 Agent 继承 workspace** → 自动读取同样的 AGENTS.md

---

## 📁 文件结构

```
workspace/
├── AGENTS.md              ← Agent 启动时读取（包含规则引用）
├── docs/
│   ├── SKILL_RULES.md     ← 技能使用规则详情
│   └── SCHEDULER.md       ← 定时任务配置
└── skills/
    ├── memory-search/
    ├── rag/
    ├── self-evolution/
    └── web-knowledge/
```

---

## 🚀 安装新 Agent

```bash
# 运行 install.sh 会自动配置
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s my-agent
```

**自动完成：**
- ✅ 复制 `docs/SKILL_RULES.md`
- ✅ 复制 `docs/SCHEDULER.md`
- ✅ 更新 `AGENTS.md` 添加规则引用

---

## 📝 子 Agent 如何继承

### 场景 1: 子 Agent 继承 workspace（默认）

```python
# 父 Agent spawn 子 Agent 时
subagent = spawn(
    task="处理这个任务",
    workspace="/path/to/parent/workspace"  # 继承同样的 workspace
)
```

**结果：** 子 Agent 读取同样的 `AGENTS.md`，自动知道规则

### 场景 2: 子 Agent 独立 workspace

```python
subagent = spawn(
    task="处理这个任务",
    workspace="/path/to/child/workspace"
)
```

**需要：** 在子 Agent workspace 也运行 `install.sh`

---

## ✅ 验证

```bash
# 1. 检查 AGENTS.md 是否包含规则引用
grep -A5 "Skill Rules" AGENTS.md

# 2. 检查 docs 目录
ls docs/SKILL_RULES.md docs/SCHEDULER.md

# 3. 测试 Agent
openclaw agent start my-agent
# 对 Agent 说："我之前说过我喜欢吃什么"
# → 应该自动搜索 memory-search
```

---

## 🔧 手动配置

如果 install.sh 没有自动配置：

```bash
cd ~/.openclaw/workspace-my-agent

# 1. 复制规则文档
cp ~/.openclaw/workspace/docs/SKILL_RULES.md docs/
cp ~/.openclaw/workspace/docs/SCHEDULER.md docs/

# 2. 更新 AGENTS.md（在 "Don't ask permission" 之前添加）
cat >> AGENTS.md << 'EOF'

### 🎯 Skill Rules

**Quick reference:**

| When | Use |
|------|-----|
| User mentions history | `memory-search` |
| Real-time info | `web-knowledge` |
| Task completed | `self-evolution` (evolve) |
| End of day | `self-evolution` (nightly) |

**Full rules:** See `docs/SKILL_RULES.md`
EOF
```

---

## 📊 规则内容速查

| 场景 | 技能 |
|------|------|
| 用户提历史 | memory-search |
| 实时信息 | web-knowledge |
| 完成任务 | self-evolution |
| 记忆搜索后 | rag |
| 每天结束 | self-evolution (nightly) |

---

_版本：1.0.0 | 2026-04-01_
