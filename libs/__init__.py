# -*- coding: utf-8 -*-
"""
Libs - 共享库层

共享基础设施库，被技能依赖。

使用方式:
    
    from libs.memory_hub import MemoryHub
    
或者:
    
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    from memory_hub import MemoryHub
"""

import sys
from pathlib import Path

# 将 libs 目录添加到 Python 路径
_libs_dir = Path(__file__).parent
if str(_libs_dir) not in sys.path:
    sys.path.insert(0, str(_libs_dir))

__version__ = '1.0.0'
__all__ = ['memory_hub']
