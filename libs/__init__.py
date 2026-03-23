# -*- coding: utf-8 -*-
"""
Libs - 共享库

统一导入方式:
    
    from libs import memory_hub
    from memory_hub import MemoryHub
    
或者:
    
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    from memory_hub import MemoryHub
"""

import sys
from pathlib import Path

# 将 libs 目录添加到路径
_libs_dir = Path(__file__).parent
if str(_libs_dir) not in sys.path:
    sys.path.insert(0, str(_libs_dir))

# 预加载常用库
try:
    from memory_hub import MemoryHub
except Exception as e:
    print(f"⚠️  Warning: Could not preload memory_hub: {e}")
    MemoryHub = None

__all__ = ['MemoryHub']
