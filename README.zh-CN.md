# evo-agents

[English](./README.md) | [简体中文](./README.zh-CN.md)

可复用的自进化 Agent 工作区模板，强调显式运行上下文（`--workspace`、`--agent`）、多 Agent 数据隔离、以及能力层共享复用。

## 🦞 OpenClaw 一键引导

如果需要从拉库到安装、健康检查、全量验收的一条龙流程，请直接使用 `workspace-setup.md`。

## 仓库定位

`evo-agents` 的目标是让一份 workspace 代码稳定服务多个 agent 实例，同时保持运行可控、边界清晰：

- 显式参数优先，避免隐式环境耦合
- 代码与数据天然分离
- 运行时元数据收敛在 workspace 内
- 不越界管理平台生命周期目录

详细设计文档：

- `docs/ARCHITECTURE_GENERIC_CN.md`
- `docs/PROJECT_STRUCTURE_GENERIC_CN.md`

## 架构摘要

分层模型：

- **交互层**：OpenClaw / 外部调用方
- **运行编排层**：`start.sh`、安装升级脚本、CLI 入参解析
- **能力实现层**：`skills/*` + `libs/memory_hub`
- **数据配置层**：`data/<agent>/...` + `public/`

核心规则：

- **代码与数据分离**：代码在 `skills/`、`libs/`、`scripts/`；运行数据在 `data/<agent>/...`
- **显式运行上下文**：主入口统一传 `--workspace` 与 `--agent`
- **workspace 内闭环**：运行元数据位于 `.agent-runtime/<agent>/`
- **平台边界清晰**：不管理 `~/.openclaw/agents`

## 目录结构

```text
evo-agents/
├── start.sh
├── init_system.py
├── skills/                      # 可调用能力模块
├── libs/memory_hub/             # 共享基础库
├── scripts/                     # 安装/升级/卸载/测试脚本
├── data/<agent>/                # 每个 agent 独立运行数据
├── .agent-runtime/<agent>/      # run.sh + 安装元数据
├── public/                      # 可共享知识资产
├── docs/                        # 架构与结构规范文档
└── workspace-setup.md           # OpenClaw 一键引导流程
```

依赖方向：

- `skills/*` -> `libs/*`：允许
- `skills/*` -> `skills/*`：不推荐（共用逻辑应下沉 `libs/`）
- `libs/*` -> `skills/*`：禁止

## 快速开始

```bash
# 1) 首次初始化
python3 init_system.py --workspace <workspace-root> --agent demo-agent

# 2) 启动与健康检查
./start.sh --workspace <workspace-root> --agent demo-agent
```

## Agent 生命周期脚本

```bash
# 安装指定 agent 的运行入口
python3 scripts/install_agent_workspace.py \
  --workspace <workspace-root> \
  --agent demo-agent

# 升级/检查
python3 scripts/upgrade_agent_workspace.py \
  --workspace <workspace-root> \
  --agent demo-agent

# 卸载（可选清理数据）
python3 scripts/uninstall_agent_workspace.py \
  --workspace <workspace-root> \
  --agent demo-agent \
  --purge-data \
  --yes
```

## 常用命令

```bash
# 记忆检索
python3 skills/memory-search/search_sqlite.py "query" --agent demo-agent
python3 skills/memory-search/search_sqlite.py "query" --semantic --agent demo-agent

# RAG 评估
python3 skills/rag/evaluate.py --report --days 7 --agent demo-agent

# 自进化
python3 skills/self-evolution/main.py --agent demo-agent status
python3 skills/self-evolution/main.py --agent demo-agent fractal --limit 10
python3 skills/self-evolution/main.py --agent demo-agent nightly
```

## 验收测试

```bash
python3 scripts/test_features.py --agent demo-agent
python3 test_all.py --workspace <workspace-root> --agent demo-agent
python3 scripts/test_agents.py --workspace <workspace-root> --agent demo-agent
```

