# sitecustomize.py - 自动添加 libs 到 Python 导入路径
# 这个文件会在 Python 启动时自动执行

import sys
from pathlib import Path

# 获取当前文件所在目录（workspace 根目录）
workspace = Path(__file__).parent.resolve()

# 添加 libs 目录到导入路径
libs_path = workspace / 'libs'
if libs_path.exists() and str(libs_path) not in sys.path:
    sys.path.insert(0, str(libs_path))

# 添加 skills 目录到导入路径
skills_path = workspace / 'skills'
if skills_path.exists() and str(skills_path) not in sys.path:
    sys.path.insert(0, str(skills_path))
