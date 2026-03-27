# -*- coding: utf-8 -*-
"""
Embedding Cache - 嵌入缓存
缓存 Ollama 生成的 embedding，避免重复计算
零依赖，仅使用 Python 标准库
"""

import hashlib
import pickle
from pathlib import Path
from typing import List, Optional


class EmbeddingCache:
    """Embedding 缓存 - 避免重复生成 embedding"""
    
    def __init__(self, cache_file: str = "embedding_cache.pkl"):
        """
        初始化缓存
        
        Args:
            cache_file: 缓存文件路径
        """
        self.cache_file = Path(cache_file)
        self.cache: dict = self._load_cache()
        self.hits = 0
        self.misses = 0
        self.dirty = False  # 是否需要保存
    
    def _load_cache(self) -> dict:
        """从磁盘加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    cache = pickle.load(f)
                    print(f"📦 加载了 {len(cache)} 个 embedding 缓存")
                    return cache
            except Exception as e:
                print(f"⚠️  加载缓存失败：{e}")
                return {}
        return {}
    
    def _save_cache(self):
        """保存缓存到磁盘"""
        try:
            # 确保目录存在
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
            
            print(f"💾 已保存 {len(self.cache)} 个 embedding 缓存")
            self.dirty = False
        except Exception as e:
            print(f"⚠️  保存缓存失败：{e}")
    
    def _hash(self, text: str) -> str:
        """
        生成文本哈希
        
        Args:
            text: 输入文本
            
        Returns:
            16 字符哈希
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    
    def get(self, text: str) -> Optional[List[float]]:
        """
        获取缓存的 embedding
        
        Args:
            text: 输入文本
            
        Returns:
            embedding 向量，如果未缓存则返回 None
        """
        key = self._hash(text)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, text: str, embedding: List[float]):
        """
        缓存 embedding
        
        Args:
            text: 输入文本
            embedding: embedding 向量
        """
        key = self._hash(text)
        
        # 如果已存在，不覆盖（避免重复计算）
        if key not in self.cache:
            self.cache[key] = embedding
            self.dirty = True
            
            # 每 100 个新缓存保存一次，避免频繁磁盘 IO
            if len(self.cache) % 100 == 0:
                self._save_cache()
    
    def stats(self) -> dict:
        """
        获取缓存统计
        
        Returns:
            统计信息字典
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0.0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'cache_size': len(self.cache),
            'dirty': self.dirty
        }
    
    def clear(self):
        """清空缓存"""
        self.cache = {}
        self.hits = 0
        self.misses = 0
        self.dirty = True
        
        if self.cache_file.exists():
            self.cache_file.unlink()
        
        print("🗑️  已清空 embedding 缓存")
    
    def __del__(self):
        """析构函数 - 保存缓存"""
        if self.dirty and len(self.cache) > 0:
            self._save_cache()
