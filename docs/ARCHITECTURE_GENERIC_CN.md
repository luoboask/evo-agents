# 🏗️ Agent Workspace 通用架构（中文通用版）

**版本：** v6.0（通用版）  
**适用范围：** 任意 Agent + 任意 workspace 路径  
**状态：** 可落地实施

---

## 1. 设计目标

- **单一 Workspace 复用**：同一份代码支持多个 Agent 实例。
- **参数驱动运行**：通过显式参数传入 `workspace` 和 `agent`。
- **数据严格隔离**：每个 Agent 的数据独立存放在 `data/<agent>/`。
- **技能统一共享**：`skills/` 为共享能力层，不按 Agent 拷贝代码。
- **边界清晰**：只管理传入的 workspace，不管理 `~/.openclaw/agents`。

---

## 2. 核心原则

1. **代码与数据分离**
   - 代码：`skills/`、`libs/`、`scripts/`
   - 数据：`data/<agent>/...`

2. **显式优于隐式**
   - 运行时通过参数传入：
     - `--workspace <path>`
     - `--agent <name>`
   - 不依赖环境变量中的隐式上下文。

3. **Workspace 内闭环**
   - 安装、升级、卸载、运行信息均写在 workspace 内。
   - 运行时元数据放在 `.agent-runtime/<agent>/`。

4. **OpenClaw 边界不越界**
   - OpenClaw 的 Agent 注册与平台生命周期由 OpenClaw 自己管理。
   - 本项目只负责 workspace 内能力实现与数据组织。

---

## 3. 分层架构

```text
┌───────────────────────────────────────────┐
│               用户交互层                  │
│   (TUI / WebChat / 外部调用方 / OpenClaw) │
└───────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────┐
│               运行编排层                  │
│  start.sh / install scripts / CLI 入参   │
│  (显式接收 workspace + agent)            │
└───────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────┐
│               能力实现层                  │
│  skills/* + libs/memory_hub              │
└───────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────┐
│               数据与配置层                │
│  data/<agent>/memory|logs|config         │
│  public/ 共享知识                         │
└───────────────────────────────────────────┘
```

---

## 4. 推荐目录结构

```text
<workspace>/
├── start.sh
├── init_system.py
├── config/
│   └── agents.yaml
├── skills/
│   ├── memory-search/
│   ├── rag/
│   ├── self-evolution/
│   └── websearch/
├── libs/
│   └── memory_hub/
├── public/                     # 共享知识（可跨 agent 复用）
├── data/
│   ├── demo-agent/
│   │   ├── memory/
│   │   ├── logs/
│   │   └── config/
│   └── <other-agent>/
├── .agent-runtime/
│   └── demo-agent/
│       ├── run.sh
│       └── install.json
└── docs/
    ├── RUNBOOK.md
    ├── INSTALL_AGENT.md
    └── ARCHITECTURE_GENERIC_CN.md
```

---

## 5. 多 Agent 设计（通用）

### 5.1 Agent 之间共享什么

- `skills/`：共享能力代码
- `libs/`：共享底层库
- `public/`：共享公开知识

### 5.2 Agent 之间隔离什么

- `data/<agent>/memory`：记忆数据库
- `data/<agent>/logs`：日志
- `data/<agent>/config`：运行配置
- `.agent-runtime/<agent>`：该 agent 的运行脚本与安装元数据

### 5.3 配置入口

`config/agents.yaml` 只描述 Agent 的角色与默认数据路径，不绑定平台级生命周期。

---

## 6. 技能系统规范

每个技能目录推荐包含：

- `SKILL.md`：技能说明（面向调用）
- `skill.json`：元数据
- 实现文件（语言不限）

推荐约定：

- 技能逻辑通过参数接收 `agent`（不要隐式读环境）
- 数据访问统一下沉到 `libs/memory_hub`
- CLI 统一支持 `--agent`

---

## 7. 数据管理策略

### 7.1 记忆与评估

- 记忆：`data/<agent>/memory/memory_stream.db`
- 知识库：`data/<agent>/memory/knowledge_base.db`
- RAG 评估：`data/<agent>/logs/*` 或技能内日志路径

### 7.2 知识分层

- `public/`：公共知识（可共享）
- `data/<agent>/...`：私有知识（仅该 agent）

### 7.3 数据生命周期

- 安装：创建 `data/<agent>/...` 目录
- 运行：增量写入
- 卸载：可选保留或清理 `data/<agent>/`

---

## 8. 运行与安装流程（参数化）

### 8.1 启动

```bash
./start.sh --workspace <workspace-path> --agent demo-agent
```

### 8.2 初始化

```bash
python3 init_system.py --workspace <workspace-path> --agent demo-agent
```

### 8.3 安装 Agent 运行入口

```bash
python3 scripts/install_agent_workspace.py \
  --agent demo-agent \
  --workspace <workspace-path>
```

安装后运行：

```bash
<workspace-path>/.agent-runtime/demo-agent/run.sh
```

### 8.4 升级检查

```bash
python3 scripts/upgrade_agent_workspace.py \
  --agent demo-agent \
  --workspace <workspace-path>
```

### 8.5 卸载

```bash
python3 scripts/uninstall_agent_workspace.py \
  --agent demo-agent \
  --workspace <workspace-path> \
  --yes
```

---

## 9. 与平台集成边界（关键）

本项目约束：

- ✅ 管理 `<workspace>` 内目录与能力
- ✅ 管理 `<workspace>/data/*` 与 `.agent-runtime/*`
- ❌ 不管理 `~/.openclaw/agents`（平台侧生命周期）
- ❌ 不假设平台目录结构（避免耦合）

这保证了 workspace 可在不同平台/宿主中复用。

---

## 10. 风险与治理建议

- **风险：参数遗漏导致跑错目录**
  - 建议：入口脚本强制参数校验（已采用）

- **风险：文档与实现漂移**
  - 建议：每次接口变更同步更新 `RUNBOOK.md` 与 `INSTALL_AGENT.md`

- **风险：多 Agent 数据串用**
  - 建议：所有能力调用显式传 `--agent`

---

## 11. 总结

该通用架构的核心是三点：

1. **单 workspace 复用能力**
2. **多 agent 数据隔离**
3. **参数显式传递上下文**

按这个模型实施后，workspace 可以在不同 Agent、不同部署环境中稳定复用，同时保持清晰边界与可维护性。
