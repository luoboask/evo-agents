# -*- coding: utf-8 -*-
"""
Skills - 技能包

统一导入方式:
    
    from skills import memory_hub, memory_search, rag, self_evolution
    
或者:
    
    from skills.memory_hub import MemoryHub
    from skills.memory_search import SQLiteMemorySearch
    from skills.rag import RAGEvaluator
    from skills.self_evolution import MemoryStream
"""

import sys
from pathlib import Path

# 将 skills 目录添加到路径
_skills_dir = Path(__file__).parent
if str(_skills_dir) not in sys.path:
    sys.path.insert(0, str(_skills_dir))

# 导出便捷导入函数
def import_skill(skill_name: str):
    """
    动态导入技能模块
    
    Args:
        skill_name: 技能名称 (如 'memory-hub', 'memory-search')
    
    Returns:
        模块对象
    """
    import importlib.util
    
    skill_path = _skills_dir / skill_name
    if not skill_path.exists():
        raise ImportError(f"Skill '{skill_name}' not found")
    
    # 查找 __init__.py 或主模块
    init_file = skill_path / '__init__.py'
    if init_file.exists():
        spec = importlib.util.spec_from_file_location(skill_name.replace('-', '_'), init_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f"No __init__.py found in '{skill_path}'")


# 预加载常用技能
try:
    memory_hub = import_skill('memory-hub')
    MemoryHub = memory_hub.MemoryHub
except Exception as e:
    print(f"⚠️  Warning: Could not preload memory-hub: {e}")
    MemoryHub = None

__all__ = ['import_skill', 'memory_hub', 'MemoryHub']
