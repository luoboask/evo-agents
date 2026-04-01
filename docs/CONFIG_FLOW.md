# Agent 技能规则配置流程

_让 Agent 和子 Agent 自动感知技能使用规则_

---

## 🎯 核心机制

**Agent 启动时读取 `AGENTS.md`** → 在文件中添加技能规则引用 → Agent 自动看到

---

## 📋 安装流程

### 1. 运行 install.sh

```bash
curl -fsSL https://gitee.com/luoboask/evo-agents/raw/master/install.sh | bash -s my-agent
```

### 2. install.sh 自动执行

```bash
# install.sh 中的逻辑：

# 1. 克隆 evo-agents 仓库
git clone https://gitee.com/luoboask/evo-agents.git ~/.openclaw/workspace-my-agent

# 2. 创建 docs 目录
mkdir -p docs/

# 3. 复制技能规则文档
cp ~/.openclaw/workspace/docs/SKILL_RULES.md docs/
cp ~/.openclaw/workspace/docs/SCHEDULER.md docs/

# 4. 更新 AGENTS.md（追加到末尾）
cat >> AGENTS.md << 'EOF'

## 🎯 Skill Rules

| When | Use |
|------|-----|
| User mentions history | memory-search |
| Real-time info | web-knowledge |
| Task completed | self-evolution |

**Full rules:** See `docs/SKILL_RULES.md`
EOF

# 5. 注册到 OpenClaw
openclaw agents add my-agent --workspace ~/.openclaw/workspace-my-agent
```

---

## 📁 最终结构

```
~/.openclaw/workspace-my-agent/
├── AGENTS.md                  ← 包含技能规则引用
├── docs/
│   ├── SKILL_RULES.md         ← 技能使用规则详情
│   └── SCHEDULER.md           ← 定时任务配置
└── skills/
    ├── memory-search/
    ├── rag/
    ├── self-evolution/
    └── web-knowledge/
```

---

## 🤖 Agent 如何感知

### 主 Agent

```
Agent 启动流程:
1. 读取 AGENTS.md
2. → 看到 "Skill Rules" 部分
3. → 知道何时使用什么技能
```

### 子 Agent

**场景 1: 继承 workspace（默认）**
```python
subagent = spawn(task="...", workspace="/path/to/parent")
# 子 agent 读取同样的 AGENTS.md → 自动知道规则
```

**场景 2: 独立 workspace**
```python
subagent = spawn(task="...", workspace="/path/to/child")
# 需要在子 workspace 也运行 install.sh
```

---

## ✅ 验证

```bash
cd ~/.openclaw/workspace-my-agent

# 1. 检查 AGENTS.md 是否包含规则
grep -A5 "Skill Rules" AGENTS.md

# 2. 检查 docs 目录
ls docs/SKILL_RULES.md

# 3. 测试 Agent
openclaw agent start my-agent
# 说："我之前说过我喜欢吃什么"
# → 应该搜索 memory-search
```

---

## 🔧 手动配置（如 install.sh 未执行）

```bash
cd ~/.openclaw/workspace-my-agent

# 1. 复制规则文档
mkdir -p docs
cp ~/.openclaw/workspace/docs/SKILL_RULES.md docs/

# 2. 追加到 AGENTS.md
cat >> AGENTS.md << 'EOF'

## 🎯 Skill Rules

| When | Use |
|------|-----|
| User mentions history | memory-search |
| Real-time info | web-knowledge |
| Task completed | self-evolution |

**Full rules:** See `docs/SKILL_RULES.md`
EOF
```

---

## 📊 关键点总结

| 问题 | 答案 |
|------|------|
| AGENTS.md 哪来的？ | evo-agents 仓库克隆 |
| 何时添加规则？ | install.sh 执行时追加 |
| openclaw agents add 会修改吗？ | 不会，只注册配置 |
| 子 agent 如何继承？ | 继承 workspace 就读同样的 AGENTS.md |
| 独立 workspace 怎么办？ | 单独运行 install.sh |

---

_版本：1.0.0 | 2026-04-01_
