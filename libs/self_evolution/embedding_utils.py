# -*- coding: utf-8 -*-
"""
Embedding 工具函数 - 通用 embedding 和相似度计算

功能：
- 调用 Ollama 获取 embedding
- 余弦相似度计算
- 缓存机制（可选）
"""

import hashlib
import json
import math
import urllib.request
from pathlib import Path
from typing import List, Dict, Optional


# 默认嵌入模型
EMBED_MODEL = "nomic-embed-text"


def get_embedding(text: str, model: str = EMBED_MODEL) -> List[float]:
    """
    调用 Ollama 获取文本 embedding
    
    Args:
        text: 输入文本
        model: 嵌入模型名称
    
    Returns:
        embedding 向量
    """
    try:
        payload = {
            "model": model,
            "prompt": text
        }
        req = urllib.request.Request(
            'http://localhost:11434/api/embeddings',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode())
        return data.get('embedding', [])
    except Exception as e:
        print(f"⚠️  Ollama embedding 失败：{e}")
        return []


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    计算余弦相似度
    
    Args:
        a: 向量 a
        b: 向量 b
    
    Returns:
        相似度 (0.0-1.0)
    """
    if not a or not b:
        return 0.0
    
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


class EmbeddingCache:
    """简单的 Embedding 缓存"""
    
    def __init__(self, cache_file: str = None):
        if cache_file:
            self.cache_file = Path(cache_file)
        else:
            self.cache_file = Path(__file__).parent.parent / "data" / "embedding_cache.pkl"
        
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[str, List[float]] = {}
        self._load()
    
    def _load(self):
        """加载缓存"""
        if self.cache_file.exists():
            try:
                import pickle
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
            except:
                self.cache = {}
    
    def _save(self):
        """保存缓存"""
        try:
            import pickle
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            print(f"⚠️  保存缓存失败：{e}")
    
    def _hash_text(self, text: str) -> str:
        """文本哈希"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, text: str, model: str = EMBED_MODEL) -> List[float]:
        """获取 embedding（优先缓存）"""
        key = f"{model}:{self._hash_text(text)}"
        
        if key not in self.cache:
            self.cache[key] = get_embedding(text, model)
            self._save()
        
        return self.cache[key]
