#!/usr/bin/env python3
"""
Install evo-agents workspace for a specific agent.

This script sets up:
- <workspace>/.agent-runtime/<agent>/config
- <workspace>/.agent-runtime/<agent>/run.sh (single command entrypoint)
- <workspace>/.agent-runtime/<agent>/install.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import stat
import subprocess
import sys
from pathlib import Path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def safe_remove(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def run_cmd(command: list[str], cwd: Path) -> int:
    proc = subprocess.run(command, cwd=str(cwd))
    return proc.returncode


def install(
    agent: str,
    force: bool,
    skip_init: bool,
    skip_healthcheck: bool,
    workspace: Path,
) -> int:
    workspace = workspace.resolve()
    if not (workspace / "start.sh").exists():
        print(f"❌ Invalid workspace: {workspace}")
        return 1

    runtime_root = workspace / ".agent-runtime"
    agent_root = runtime_root / agent
    data_root = workspace / "data" / agent
    config_dir = data_root / "config"

    ensure_dir(agent_root)
    ensure_dir(data_root)
    ensure_dir(config_dir / "memory")
    ensure_dir(config_dir / "logs")

    if (agent_root / "install.json").exists() and not force:
        print(f"❌ {agent_root} already initialized. Use --force to replace.")
        return 1
    if force and agent_root.exists():
        safe_remove(agent_root)
        ensure_dir(agent_root)

    run_sh = agent_root / "run.sh"
    run_content = f"""#!/usr/bin/env bash
set -e

cd "{workspace}"
exec ./start.sh --workspace "{workspace}" --agent "{agent}" "$@"
"""
    write_executable(run_sh, run_content)

    meta = {
        "agent": agent,
        "workspace": str(workspace),
        "runtime_root": str(agent_root),
        "config_dir": str(config_dir),
        "data_root": str(data_root),
        "run_script": str(run_sh),
    }
    (agent_root / "install.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if not skip_init:
        print("🔧 Running init_system.py ...")
        code = run_cmd(["python3", "init_system.py", "--workspace", str(workspace), "--agent", agent], cwd=workspace)
        if code != 0:
            print("⚠️ init_system.py returned non-zero. You can rerun manually.")

    if not skip_healthcheck:
        print("🩺 Running start.sh healthcheck ...")
        code = run_cmd(["./start.sh", "--workspace", str(workspace), "--agent", agent], cwd=workspace)
        if code != 0:
            print("⚠️ start.sh returned non-zero. Check run.sh output manually.")

    print("\n✅ Install completed")
    print(f"- Workspace : {workspace}")
    print(f"- Runtime   : {agent_root}")
    print(f"- Run command: {run_sh}")
    print(f"- Config dir : {config_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install workspace for an agent")
    parser.add_argument("--agent", required=True, help="Agent name")
    parser.add_argument("--workspace", required=True, help="Workspace path")
    parser.add_argument("--force", action="store_true", help="Replace existing install")
    parser.add_argument("--skip-init", action="store_true", help="Skip init_system.py")
    parser.add_argument(
        "--skip-healthcheck", action="store_true", help="Skip ./start.sh after install"
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser()
    if not workspace.exists():
        print(f"❌ Workspace not found: {workspace}")
        return 1

    return install(
        agent=args.agent,
        force=args.force,
        skip_init=args.skip_init,
        skip_healthcheck=args.skip_healthcheck,
        workspace=workspace,
    )


if __name__ == "__main__":
    sys.exit(main())
