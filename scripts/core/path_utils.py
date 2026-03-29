#!/usr/bin/env python3
"""
path_utils - 路径工具（转发到 libs/path_utils）

这个文件是为了保持向后兼容
scripts/core/ 下的脚本可以直接 from path_utils import
实际实现由 libs/path_utils 提供
"""
import sys
from pathlib import Path

# 添加 libs 到路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "libs"))

# 从 libs/path_utils 导入所有
from path_utils import (
    resolve_workspace,
    resolve_agent_memory,
    resolve_data_dir,
    WORKSPACE,
    MEMORY_DIR,
    DATA_DIR
)

__all__ = [
    'resolve_workspace',
    'resolve_agent_memory',
    'resolve_data_dir',
    'WORKSPACE',
    'MEMORY_DIR',
    'DATA_DIR'
]
