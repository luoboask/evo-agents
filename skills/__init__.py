# -*- coding: utf-8 -*-
"""
Skills - 技能包

统一导入方式:
    
    from skills.memory_search import SQLiteMemorySearch
    from skills.rag import RAGEvaluator
    from skills.self_evolution import MemoryStream
    
注意：memory_hub 是共享库，在 libs/ 目录:
    from libs import MemoryHub
"""

import sys
from pathlib import Path

# 将 skills 目录添加到路径
_skills_dir = Path(__file__).parent
if str(_skills_dir) not in sys.path:
    sys.path.insert(0, str(_skills_dir))

# 同时添加 libs 目录到路径，支持从 skills 导入 libs
_libs_dir = _skills_dir.parent / 'libs'
if str(_libs_dir) not in sys.path:
    sys.path.insert(0, str(_libs_dir))

__all__ = []
