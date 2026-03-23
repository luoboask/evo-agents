# Workspace Setup (for OpenClaw)

This file defines a complete, executable setup flow for this repository:
- clone/update repo
- install agent runtime in this workspace
- initialize
- run health check
- run full tests

## Required Inputs

- `WORKSPACE`: absolute path of this repo on local machine
- `AGENT`: agent name (default: `demo-agent`)

Example:

```bash
export WORKSPACE="/absolute/path/to/evo-agents"
export AGENT="demo-agent"
```

## Boundary Rule

- Only operate inside `WORKSPACE`.
- Do not create or manage `~/.openclaw/agents`.
- Runtime state must stay in:
  - `WORKSPACE/.agent-runtime/<agent>`
  - `WORKSPACE/data/<agent>`

## 0) Clone or Update Repository

If repo does not exist:

```bash
git clone "https://gitlab.alibaba-inc.com/haoran.dhr/evo-agents.git" "$WORKSPACE"
```

If repo already exists:

```bash
cd "$WORKSPACE" && git pull --rebase
```

Alternative (SSH):

```bash
git clone "git@gitlab.alibaba-inc.com:haoran.dhr/evo-agents.git" "$WORKSPACE"
```

## 1) Install Agent Workspace

```bash
cd "$WORKSPACE"
python3 scripts/install_agent_workspace.py --workspace "$WORKSPACE" --agent "$AGENT" --force
```

Expected:
- creates `WORKSPACE/.agent-runtime/$AGENT/run.sh`
- creates `WORKSPACE/.agent-runtime/$AGENT/install.json`
- ensures `WORKSPACE/data/$AGENT/config` exists

## 2) Explicit Initialization (idempotent)

```bash
cd "$WORKSPACE"
python3 init_system.py --workspace "$WORKSPACE" --agent "$AGENT"
```

## 3) Health Check

```bash
cd "$WORKSPACE"
./start.sh --workspace "$WORKSPACE" --agent "$AGENT"
```

## 4) Functional Tests

Run lightweight feature tests:

```bash
cd "$WORKSPACE"
python3 scripts/test_features.py --agent "$AGENT"
```

Run full suite:

```bash
cd "$WORKSPACE"
python3 test_all.py --workspace "$WORKSPACE" --agent "$AGENT"
```

Run agent-level isolation test:

```bash
cd "$WORKSPACE"
python3 scripts/test_agents.py --workspace "$WORKSPACE" --agent "$AGENT"
```

## 5) Pass Criteria

Setup is considered successful when all conditions are true:
- install script exits with code `0`
- `init_system.py` exits with code `0`
- `start.sh` exits with code `0`
- `scripts/test_features.py` exits with code `0`
- `test_all.py` exits with code `0`
- `scripts/test_agents.py` exits with code `0`

## 6) Troubleshooting Sequence

If any step fails, run in this order:

```bash
cd "$WORKSPACE"
python3 scripts/upgrade_agent_workspace.py --workspace "$WORKSPACE" --agent "$AGENT"
python3 init_system.py --workspace "$WORKSPACE" --agent "$AGENT"
./start.sh --workspace "$WORKSPACE" --agent "$AGENT"
python3 test_all.py --workspace "$WORKSPACE" --agent "$AGENT"
```

If still failing, collect and report:
- failed command
- exit code
- stderr/stdout snippet
- current `WORKSPACE` and `AGENT`

## 7) One-shot Execution (recommended for OpenClaw)

```bash
set -e
export WORKSPACE="/absolute/path/to/evo-agents"
export AGENT="demo-agent"

if [ ! -d "$WORKSPACE/.git" ]; then
  git clone "https://gitlab.alibaba-inc.com/haoran.dhr/evo-agents.git" "$WORKSPACE"
else
  cd "$WORKSPACE" && git pull --rebase
fi

cd "$WORKSPACE"
python3 scripts/install_agent_workspace.py --workspace "$WORKSPACE" --agent "$AGENT" --force
python3 init_system.py --workspace "$WORKSPACE" --agent "$AGENT"
./start.sh --workspace "$WORKSPACE" --agent "$AGENT"
python3 scripts/test_features.py --agent "$AGENT"
python3 test_all.py --workspace "$WORKSPACE" --agent "$AGENT"
python3 scripts/test_agents.py --workspace "$WORKSPACE" --agent "$AGENT"
```
