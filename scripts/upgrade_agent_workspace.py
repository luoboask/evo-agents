#!/usr/bin/env python3
"""
Upgrade/check an installed agent workspace.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def load_install_meta(agent: str) -> tuple[Path, dict]:
    workspace = Path.cwd()
    agent_root = workspace / ".agent-runtime" / agent
    meta_path = agent_root / "install.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing install metadata: {meta_path}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return agent_root, meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Upgrade/check installed agent workspace")
    parser.add_argument("--agent", required=True, help="Agent name")
    parser.add_argument("--workspace", required=True, help="Workspace path")
    parser.add_argument(
        "--skip-healthcheck", action="store_true", help="Skip start.sh healthcheck"
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists():
        print(f"❌ Workspace not found: {workspace}")
        return 1
    os.chdir(str(workspace))

    agent_root, meta = load_install_meta(args.agent)

    workspace_path = Path(meta["workspace"])

    if workspace_path != workspace:
        print("❌ install metadata workspace mismatch")
        print(f"   meta: {workspace_path}")
        print(f"   arg : {workspace}")
        return 1

    if not args.skip_healthcheck:
        print("🩺 Running healthcheck ...")
        code = subprocess.run(
            ["./start.sh", "--workspace", str(workspace_path), "--agent", args.agent],
            cwd=str(workspace_path),
        ).returncode
        if code != 0:
            print("⚠️ Healthcheck returned non-zero.")

    print("✅ Upgrade/check completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
