# Multi-Agent Example | 多 Agent 示例

This example shows how to set up multiple collaborating agents.

## Quick Start | 快速开始

```bash
# Install main agent | 安装主 Agent
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s team-agent

# Add sub-agents | 添加子 Agent
cd ~/.openclaw/workspace-team-agent
./scripts/core/setup-multi-agent.sh researcher writer editor
```

## Agent Roles | Agent 角色

| Agent | Role | Description |
|-------|------|-------------|
| researcher | Research | Find information |
| writer | Writing | Create content |
| editor | Editing | Review and improve |

## Example Workflow | 示例流程

```bash
# Record research task
python3 scripts/core/session_recorder.py -t event -c "Research topic X" --agent researcher-agent

# Record writing task
python3 scripts/core/session_recorder.py -t event -c "Write article" --agent writer-agent

# Record editing task
python3 scripts/core/session_recorder.py -t event -c "Edit article" --agent editor-agent
```
