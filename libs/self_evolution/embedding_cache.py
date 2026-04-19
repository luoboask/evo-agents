#!/usr/bin/env python3
"""
Embedding 缓存 - 加速语义搜索

核心功能:
- 缓存已计算的 embedding
- 避免重复调用 Ollama
- 持久化保存到文件
"""

import hashlib
import pickle
from pathlib import Path
from typing import List, Dict
import urllib.request
import json


class EmbeddingCache:
    """Embedding 缓存管理器"""
    
    def __init__(self, cache_file: str = None):
        self.cache_file = Path(cache_file) if cache_file else Path(__file__).parent / 'embedding_cache.pkl'
        self.cache: Dict[str, List[float]] = {}
        self._load_cache()
    
    def _load_cache(self):
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
                print(f"📦 已加载 embedding 缓存：{len(self.cache)} 条")
            except Exception as e:
                print(f"⚠️  加载缓存失败：{e}")
                self.cache = {}
    
    def _save_cache(self):
        """保存缓存"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
            print(f"💾 已保存 embedding 缓存：{len(self.cache)} 条")
        except Exception as e:
            print(f"⚠️  保存缓存失败：{e}")
    
    def _hash_text(self, text: str) -> str:
        """文本哈希"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, text: str) -> List[float]:
        """获取 embedding (优先缓存)"""
        text_hash = self._hash_text(text)
        
        if text_hash not in self.cache:
            # 缓存未命中，调用 Ollama
            self.cache[text_hash] = self._call_ollama(text)
            self._save_cache()
        
        return self.cache[text_hash]
    
    def _call_ollama(self, text: str) -> List[float]:
        """调用 Ollama 获取 embedding"""
        try:
            payload = {
                "model": "nomic-embed-text",
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
            print(f"⚠️  Ollama 调用失败：{e}")
            return []
    
    def clear(self):
        """清空缓存"""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
        print("🗑️  缓存已清空")
    
    def stats(self) -> Dict:
        """获取缓存统计"""
        return {
            'total_embeddings': len(self.cache),
            'cache_file': str(self.cache_file),
            'cache_size_mb': self.cache_file.stat().st_size / 1024 / 1024 if self.cache_file.exists() else 0
        }


# 全局缓存实例
_embedding_cache = None

def get_embedding_cache() -> EmbeddingCache:
    """获取全局 Embedding 缓存实例"""
    global _embedding_cache
    if _embedding_cache is None:
        _embedding_cache = EmbeddingCache()
    return _embedding_cache

# 兼容统一管理器
def get_unified_embedding(agent_name: str = None):
    """获取统一 Embedding 管理器（兼容旧代码）"""
    from libs.self_evolution.embedding_manager import get_embedding_manager
    return get_embedding_manager()


def get_cached_embedding(text: str) -> List[float]:
    """获取 cached embedding (全局函数)"""
    global _embedding_cache
    if _embedding_cache is None:
        _embedding_cache = EmbeddingCache()
    return _embedding_cache.get(text)


def clear_embedding_cache():
    """清空缓存 (全局函数)"""
    global _embedding_cache
    if _embedding_cache:
        _embedding_cache.clear()
        _embedding_cache = None


def get_embedding_cache_stats() -> Dict:
    """获取缓存统计 (全局函数)"""
    global _embedding_cache
    if _embedding_cache is None:
        _embedding_cache = EmbeddingCache()
    return _embedding_cache.stats()


# 命令行工具
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'stats':
            cache = EmbeddingCache()
            stats = cache.stats()
            print(f"""
Embedding 缓存统计:
  总 embedding 数：{stats['total_embeddings']}
  缓存文件：{stats['cache_file']}
  缓存大小：{stats['cache_size_mb']:.2f} MB
""")
        
        elif cmd == 'clear':
            cache = EmbeddingCache()
            cache.clear()
            print("✅ 缓存已清空")
        
        elif cmd == 'test':
            cache = EmbeddingCache()
            
            print("测试缓存...")
            text = "API 调用超时"
            
            import time
            start = time.time()
            e1 = cache.get(text)
            t1 = time.time() - start
            
            start = time.time()
            e2 = cache.get(text)
            t2 = time.time() - start
            
            print(f"""
测试结果:
  第 1 次 (缓存未命中): {t1*1000:.1f}ms
  第 2 次 (缓存命中): {t2*1000:.1f}ms
  速度提升：{t1/t2:.1f} 倍
""")
        
        else:
            print("用法：python3 embedding_cache.py [stats|clear|test]")
    else:
        print("用法：python3 embedding_cache.py [stats|clear|test]")
