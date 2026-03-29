#!/usr/bin/env python3
"""
path_utils - 统一路径解析工具库

独立库，不依赖任何模块，被 skills 和 scripts 共享
"""
import os
from pathlib import Path


def resolve_workspace() -> Path:
    """解析 Workspace 路径
    
    优先级:
    1. EVO_WORKSPACE 或 WORKSPACE_ROOT 环境变量
    2. .install-config 配置文件
    3. 从脚本位置推导（回退）
    """
    # 1. 环境变量（最高优先级）
    env_path = os.environ.get("EVO_WORKSPACE") or os.environ.get("WORKSPACE_ROOT")
    if env_path:
        return Path(env_path)
    
    # 2. 配置文件
    script_dir = Path(__file__).resolve().parent
    config_file = script_dir.parent.parent / ".install-config"
    if config_file.exists():
        for line in config_file.read_text().splitlines():
            if line.startswith("workspace_path="):
                return Path(line.split("=", 1)[1].strip())
    
    # 3. 推导（回退）
    # 支持两种结构：
    # - libs/path_utils/__init__.py → workspace 根目录
    # - scripts/core/path_utils.py → workspace 根目录
    current = script_dir
    for _ in range(5):
        if current.name.startswith("workspace-") or (current.parent.name == ".openclaw" and current.name.startswith("workspace-")):
            return current
        if (current / ".git").exists():
            return current
        current = current.parent
    
    return current


def resolve_agent_memory(agent: str = None) -> Path:
    """解析 Agent 记忆目录"""
    workspace = resolve_workspace()
    if not agent:
        return workspace / "memory"
    
    agent_memory = workspace / "agents" / agent / "memory"
    if agent_memory.exists():
        return agent_memory
    
    return workspace / "memory"


def resolve_data_dir(subdir: str = None) -> Path:
    """解析数据目录"""
    workspace = resolve_workspace()
    data_dir = workspace / "data"
    return data_dir / subdir if subdir else data_dir


# 快捷导入
WORKSPACE = resolve_workspace()
MEMORY_DIR = WORKSPACE / "memory"
DATA_DIR = WORKSPACE / "data"
