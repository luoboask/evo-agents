#!/usr/bin/env python3
"""
Uninstall an installed agent workspace.

By default removes:
- <workspace>/.agent-runtime/<agent>

With --purge-data also removes:
- <workspace>/data/<agent>
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Uninstall agent workspace")
    parser.add_argument("--agent", required=True, help="Agent name")
    parser.add_argument("--workspace", required=True, help="Workspace path")
    parser.add_argument("--purge-data", action="store_true", help="Also remove agent data")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    agent_root = workspace / ".agent-runtime" / args.agent
    data_root = workspace / "data" / args.agent

    print(f"Agent home: {agent_root}")
    print(f"Agent data: {data_root}")

    if not args.yes:
        confirm = input("Proceed uninstall? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return 0

    remove_path(agent_root)
    if args.purge_data:
        remove_path(data_root)

    print("✅ Uninstall completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
