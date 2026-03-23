# -*- coding: utf-8 -*-
"""
Memory Hub - 记忆中心

统一导入方式（推荐）:
    
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / 'memory-hub'))
    
    from hub import MemoryHub
    from knowledge import KnowledgeInterface
    from evaluation import EvaluationInterface

或者使用便捷导入:
    
    from skills.memory_hub import MemoryHub  # 需要 skills/__init__.py 支持
"""

# 自动将当前目录添加到 Python 路径，支持直接导入子模块
import sys
from pathlib import Path

_current_dir = Path(__file__).parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

# 使用绝对路径导入，避免相对导入问题
_hub_path = _current_dir / 'hub.py'
if _hub_path.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location('hub', _hub_path)
    hub_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hub_module)
    
    # 导出所有公共接口
    MemoryHub = hub_module.MemoryHub
    
    # 导入其他模块
    _knowledge_path = _current_dir / 'knowledge.py'
    if _knowledge_path.exists():
        spec = importlib.util.spec_from_file_location('knowledge', _knowledge_path)
        knowledge_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(knowledge_module)
        KnowledgeInterface = knowledge_module.KnowledgeInterface
    
    _evaluation_path = _current_dir / 'evaluation.py'
    if _evaluation_path.exists():
        spec = importlib.util.spec_from_file_location('evaluation', _evaluation_path)
        evaluation_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluation_module)
        EvaluationInterface = evaluation_module.EvaluationInterface
    
    _storage_path = _current_dir / 'storage.py'
    if _storage_path.exists():
        spec = importlib.util.spec_from_file_location('storage', _storage_path)
        storage_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(storage_module)
        StorageManager = storage_module.StorageManager
    
    _models_path = _current_dir / 'models.py'
    if _models_path.exists():
        spec = importlib.util.spec_from_file_location('models', _models_path)
        models_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(models_module)
        Memory = models_module.Memory
        MemoryType = models_module.MemoryType
        Knowledge = models_module.Knowledge

__all__ = [
    'MemoryHub',
    'KnowledgeInterface',
    'EvaluationInterface',
    'StorageManager',
    'Memory',
    'MemoryType',
    'Knowledge'
]

__version__ = '1.0.0'
