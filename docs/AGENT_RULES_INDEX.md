# Agent 规则清单

_所有需要让 Agent 感知的规则汇总_

---

## 📚 规则文档体系

```
docs/
├── SKILL_RULES.md         ← 技能使用规则（何时用什么技能）
├── SCHEDULER.md           ← 定时任务配置（自动化执行）
├── WORKSPACE_RULES.md     ← Workspace 规则（目录结构、文件存放）
└── AGENT_RULES_INDEX.md   ← 本文档（规则索引）
```

---

## 🎯 规则分类

### 1. 技能使用规则 (SKILL_RULES.md)

**目的：** 让 Agent 知道何时使用什么技能

**核心内容：**
| 场景 | 技能 |
|------|------|
| 用户提到历史 | memory-search |
| 实时信息 | web-knowledge |
| 完成任务 | self-evolution |
| 记忆搜索后 | rag |
| 每天结束 | self-evolution (nightly) |

**Agent 如何感知：** AGENTS.md 中的 Skill Rules 部分

---

### 2. 定时任务规则 (SCHEDULER.md)

**目的：** 配置自动化任务执行时间

**核心内容：**
```bash
# 每天凌晨 2 点 - 夜间循环
0 2 * * * python3 skills/self-evolution/main.py nightly

# 每周日上午 9 点 - RAG 评估
0 9 * * 0 python3 skills/rag/main.py evaluate --days 7 --report
```

**Agent 如何感知：** 需要时查阅文档

---

### 3. Workspace 规则 (WORKSPACE_RULES.md)

**目的：** 规范文件存放位置，保持 workspace 整洁

**核心内容：**

#### 目录结构
```
workspace/
├── docs/           # 文档
├── memory/         # 记忆文件
├── skills/         # 技能
├── data/           # Agent 数据
├── projects/       # 临时项目
└── scripts/        # 脚本
```

#### 文件存放规则
| 文件类型 | 位置 | 清理 |
|---------|------|------|
| 临时下载 | `/tmp/` | 系统自动 |
| Git 项目（临时） | `/tmp/` | 完成后 |
| Git 项目（长期） | `~/projects/` | 保留 |
| Agent 数据 | `data/<agent>/` | 根据需要 |
| 记忆文件 | `memory/` | 定期归档 |

#### 禁止操作
- ❌ 在 workspace 根目录 clone git 项目
- ❌ 在 workspace 根目录下载文件
- ❌ 在 workspace 根目录创建随机文件夹
- ❌ 修改 `.git/`、`.openclaw/`、`*.db` 文件

**Agent 如何感知：** AGENTS.md 中的 Workspace Rules 部分

---

### 4. 行为规范 (AGENTS.md / RULES.md)

**目的：** 定义 Agent 行为边界和决策权限

**核心内容：**

#### 🚫 绝对禁止
- 删除任何文件（需用户明确授权）
- 访问敏感数据（密码、密钥）
- 向第三方透露私人信息
- 执行违法或危险操作

#### ⚠️ 需要确认
- 修改系统配置
- 安装新软件
- 执行耗时>5 分钟的任务
- 涉及外部 API 访问

#### ✅ 可以自主
- 读取和分析文件
- 优化自己的代码
- 记录日志和记忆
- 在 workspace 内创建文件

**Agent 如何感知：** 启动时读取 AGENTS.md 和 RULES.md

---

## 📋 完整规则列表

### 必须让 Agent 感知的规则

| 规则 | 文档 | 感知方式 | 优先级 |
|------|------|---------|--------|
| 技能使用 | SKILL_RULES.md | AGENTS.md 引用 | ⭐⭐⭐⭐⭐ |
| Workspace 规范 | WORKSPACE_RULES.md | AGENTS.md 引用 | ⭐⭐⭐⭐⭐ |
| 行为边界 | RULES.md | 启动时读取 | ⭐⭐⭐⭐⭐ |
| 定时任务 | SCHEDULER.md | 需要时查阅 | ⭐⭐⭐⭐ |
| 记忆管理 | WORKSPACE_RULES.md | AGENTS.md 引用 | ⭐⭐⭐⭐ |
| 数据隔离 | WORKSPACE_RULES.md | AGENTS.md 引用 | ⭐⭐⭐⭐ |

---

## 🚀 如何让 Agent 感知

### 方式 1: AGENTS.md 引用（推荐）

```markdown
# AGENTS.md

### 🎯 Skill Rules
| When | Use |
|------|-----|
| User mentions history | memory-search |

**Full rules:** See `docs/SKILL_RULES.md`

### 📁 Workspace Rules
| What | Where |
|------|-------|
| Temp downloads | /tmp/ |

**Full rules:** See `docs/WORKSPACE_RULES.md`
```

**优点：** Agent 启动时自动读取

### 方式 2: 启动时读取

```markdown
# AGENTS.md

## Session Startup
Before doing anything else:
1. Read SOUL.md
2. Read USER.md
3. Read memory/...
4. Read MEMORY.md (main session)
```

**优点：** 强制读取关键文档

### 方式 3: 需要时查阅

```markdown
Agent 在需要时主动读取：
- docs/SCHEDULER.md（配置定时任务时）
- docs/WORKSPACE_RULES.md（不确定文件放哪里时）
```

**优点：** 按需读取，节省 token

---

## 🔧 install.sh 自动配置

```bash
# install.sh 中自动复制规则文档

# 1. 创建 docs 目录
mkdir -p docs

# 2. 复制规则文档
cp ~/.openclaw/workspace/docs/SKILL_RULES.md docs/
cp ~/.openclaw/workspace/docs/SCHEDULER.md docs/
cp ~/.openclaw/workspace/docs/WORKSPACE_RULES.md docs/

# 3. 更新 AGENTS.md
cat >> AGENTS.md << 'EOF'

### 🎯 Skill Rules
| When | Use |
|------|-----|
| User mentions history | memory-search |

**Full rules:** See `docs/SKILL_RULES.md`

### 📁 Workspace Rules
**Full rules:** See `docs/WORKSPACE_RULES.md`
EOF
```

---

## ✅ 验证清单

安装新 Agent 后检查：

- [ ] `docs/SKILL_RULES.md` 存在
- [ ] `docs/SCHEDULER.md` 存在
- [ ] `docs/WORKSPACE_RULES.md` 存在
- [ ] `AGENTS.md` 包含规则引用
- [ ] Agent 启动时能读取规则
- [ ] 测试技能触发（说"我记得..."）
- [ ] 测试文件存放（下载文件到正确位置）

---

## 📊 规则优先级

```
⭐⭐⭐⭐⭐ 必须感知（启动时读取）
- 技能使用规则
- Workspace 规范
- 行为边界

⭐⭐⭐⭐ 重要（需要时查阅）
- 定时任务配置
- 记忆管理规范
- 数据隔离规则

⭐⭐⭐ 参考（可选）
- 配置示例
- 最佳实践
- 故障排查
```

---

## 🎯 核心原则

1. **精简** - 只包含必要规则，避免信息过载
2. **清晰** - 使用表格、列表，一目了然
3. **可执行** - 规则要具体，可操作
4. **分层** - 核心规则放 AGENTS.md，详情放 docs/
5. **自动化** - install.sh 自动配置，无需手动

---

_版本：1.0.0 | 2026-04-01_
