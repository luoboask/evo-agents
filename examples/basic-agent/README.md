# Basic Agent Example | 基础 Agent 示例

This example shows how to set up a simple single agent.

## Quick Start | 快速开始

```bash
# Install | 安装
curl -s https://raw.githubusercontent.com/luoboask/evo-agents/master/install.sh | bash -s my-agent

# Activate features | 激活功能
cd ~/.openclaw/workspace-my-agent
./scripts/core/activate-features.sh

# Record a session | 记录会话
python3 scripts/core/session_recorder.py -t event -c "My first session" --agent my-agent
```

## Files | 文件结构

```
workspace-my-agent/
├── memory/           # Daily memory files
├── scripts/          # Scripts
├── skills/           # Skills
└── data/             # Agent data
```

## Next Steps | 下一步

- Try multi-agent setup: `../multi-agent/`
- Learn about RAG: `../advanced-rag/`
