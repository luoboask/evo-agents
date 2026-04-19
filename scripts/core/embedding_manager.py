# -*- coding: utf-8 -*-
"""
Embedding 统一管理器 - 全系统共享的 Embedding 缓存层

功能:
- 统一缓存管理（所有模块共享）
- 多 Agent 支持
- 自动失效策略
- 批量处理优化
- 统计和监控
"""

import hashlib
import pickle
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from collections import OrderedDict
# 使用统一路径解析工具
try:
    from path_utils import resolve_workspace
except ImportError:
    def resolve_workspace():
        return Path(__file__).parent.parent.parent


class UnifiedEmbeddingManager:
    """统一 Embedding 管理器"""
    
    def __init__(self, cache_dir: str = None, max_size: int = 10000):
        """
        初始化统一管理器
        
        Args:
            cache_dir: 缓存目录（默认在 data/embedding_cache/）
            max_size: 最大缓存条目数
        """
        self.workspace = resolve_workspace()
        self.data_path = self.workspace / "data"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = self.data_path / "embedding_cache"
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 缓存配置
        self.max_size = max_size
        self.ttl_days = 30  # 缓存有效期（天）
        
        # 多 Agent 缓存
        self.caches: Dict[str, OrderedDict] = {}
        self.metadata: Dict[str, Dict] = {}
        
        # 全局缓存文件
        self.global_cache_file = self.cache_dir / "global_embedding_cache.pkl"
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        
        self._load_all()
        
        print(f"📦 Embedding 统一管理器已初始化")
        print(f"   缓存目录：{self.cache_dir}")
        print(f"   最大容量：{self.max_size} 条")
        print(f"   有效期：{self.ttl_days} 天")
    
    def _load_all(self):
        """加载所有缓存"""
        # 加载全局缓存
        if self.global_cache_file.exists():
            try:
                with open(self.global_cache_file, 'rb') as f:
                    self.caches['global'] = OrderedDict(pickle.load(f))
                print(f"   ✅ 已加载全局缓存：{len(self.caches['global'])} 条")
            except Exception as e:
                print(f"   ⚠️  加载全局缓存失败：{e}")
                self.caches['global'] = OrderedDict()
        else:
            self.caches['global'] = OrderedDict()
        
        # 加载元数据
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                print(f"   ⚠️  加载元数据失败：{e}")
                self.metadata = {}
        else:
            self.metadata = {}
        
        # 加载 Agent 专用缓存
        agent_cache_dir = self.cache_dir / "agents"
        if agent_cache_dir.exists():
            for agent_file in agent_cache_dir.glob("*.pkl"):
                agent_name = agent_file.stem
                try:
                    with open(agent_file, 'rb') as f:
                        self.caches[agent_name] = OrderedDict(pickle.load(f))
                    print(f"   ✅ 已加载 {agent_name} 缓存：{len(self.caches[agent_name])} 条")
                except Exception as e:
                    print(f"   ⚠️  加载 {agent_name} 缓存失败：{e}")
    
    def _save_all(self):
        """保存所有缓存"""
        try:
            # 保存全局缓存
            with open(self.global_cache_file, 'wb') as f:
                pickle.dump(self.caches.get('global', OrderedDict()), f)
            
            # 保存 Agent 缓存
            agent_cache_dir = self.cache_dir / "agents"
            agent_cache_dir.mkdir(parents=True, exist_ok=True)
            
            for agent_name, cache in self.caches.items():
                if agent_name != 'global':
                    agent_file = agent_cache_dir / f"{agent_name}.pkl"
                    with open(agent_file, 'wb') as f:
                        pickle.dump(cache, f)
            
            # 保存元数据
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
            total = sum(len(c) for c in self.caches.values())
            print(f"💾 已保存所有缓存：{total} 条")
        except Exception as e:
            print(f"⚠️  保存缓存失败：{e}")
    
    def _hash_text(self, text: str) -> str:
        """文本哈希"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get(self, text: str, agent_name: str = None) -> Optional[List[float]]:
        """
        获取 Embedding（优先缓存）
        
        Args:
            text: 文本
            agent_name: Agent 名称（None 使用全局缓存）
        
        Returns:
            Embedding 向量，失败返回 None
        """
        cache_key = agent_name or 'global'
        
        if cache_key not in self.caches:
            self.caches[cache_key] = OrderedDict()
        
        text_hash = self._hash_text(text)
        
        if text_hash in self.caches[cache_key]:
            # 缓存命中，移到末尾（LRU）
            self.caches[cache_key].move_to_end(text_hash)
            return self.caches[cache_key][text_hash]
        
        return None
    
    def set(self, text: str, embedding: List[float], agent_name: str = None):
        """
        设置 Embedding 缓存
        
        Args:
            text: 文本
            embedding: Embedding 向量
            agent_name: Agent 名称
        """
        cache_key = agent_name or 'global'
        
        if cache_key not in self.caches:
            self.caches[cache_key] = OrderedDict()
        
        text_hash = self._hash_text(text)
        
        # 添加到缓存
        self.caches[cache_key][text_hash] = embedding
        self.caches[cache_key].move_to_end(text_hash)
        
        # 更新元数据
        if cache_key not in self.metadata:
            self.metadata[cache_key] = {
                'created_at': datetime.now().isoformat(),
                'total_hits': 0,
                'total_misses': 0
            }
        
        # 检查是否超出容量
        if len(self.caches[cache_key]) > self.max_size:
            # 删除最旧的条目
            self.caches[cache_key].popitem(last=False)
        
        # 定期保存
        self._save_all()
    
    def get_or_compute(self, text: str, compute_func, agent_name: str = None) -> List[float]:
        """
        获取或计算 Embedding
        
        Args:
            text: 文本
            compute_func: 计算函数（缓存未命中时调用）
            agent_name: Agent 名称
        
        Returns:
            Embedding 向量
        """
        # 尝试从缓存获取
        embedding = self.get(text, agent_name)
        
        if embedding is not None:
            # 缓存命中
            if agent_name and agent_name in self.metadata:
                self.metadata[agent_name]['total_hits'] += 1
            elif 'global' in self.metadata:
                self.metadata['global']['total_hits'] += 1
            return embedding
        
        # 缓存未命中，计算
        embedding = compute_func(text)
        
        # 保存到缓存
        self.set(text, embedding, agent_name)
        
        # 更新统计
        if agent_name and agent_name in self.metadata:
            self.metadata[agent_name]['total_misses'] += 1
        elif 'global' in self.metadata:
            self.metadata['global']['total_misses'] += 1
        
        return embedding
    
    def get_batch(self, texts: List[str], agent_name: str = None) -> Dict[str, Optional[List[float]]]:
        """
        批量获取 Embedding
        
        Args:
            texts: 文本列表
            agent_name: Agent 名称
        
        Returns:
            {text: embedding} 字典
        """
        results = {}
        for text in texts:
            results[text] = self.get(text, agent_name)
        return results
    
    def set_batch(self, embeddings_dict: Dict[str, List[float]], agent_name: str = None):
        """
        批量设置 Embedding 缓存
        
        Args:
            embeddings_dict: {text: embedding} 字典
            agent_name: Agent 名称
        """
        for text, embedding in embeddings_dict.items():
            self.set(text, embedding, agent_name)
    
    def clear(self, agent_name: str = None):
        """
        清空缓存
        
        Args:
            agent_name: Agent 名称（None 清空全局）
        """
        cache_key = agent_name or 'global'
        
        if cache_key in self.caches:
            count = len(self.caches[cache_key])
            self.caches[cache_key] = OrderedDict()
            print(f"🗑️  已清空 {cache_key} 缓存：{count} 条")
            self._save_all()
    
    def cleanup_expired(self, days: int = None):
        """
        清理过期缓存
        
        Args:
            days: 过期天数（None 使用默认 ttl_days）
        """
        if days is None:
            days = self.ttl_days
        
        cutoff = datetime.now() - timedelta(days=days)
        cleaned = 0
        
        for cache_key, cache in self.caches.items():
            # 简单实现：删除最旧的条目
            # TODO: 添加时间戳追踪
            pass
        
        print(f"🧹 清理完成：{cleaned} 条过期缓存")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = {
            'total_caches': len(self.caches),
            'total_embeddings': sum(len(c) for c in self.caches.values()),
            'max_size': self.max_size,
            'ttl_days': self.ttl_days,
            'by_agent': {}
        }
        
        for agent_name, cache in self.caches.items():
            meta = self.metadata.get(agent_name, {})
            stats['by_agent'][agent_name] = {
                'count': len(cache),
                'hits': meta.get('total_hits', 0),
                'misses': meta.get('total_misses', 0),
                'hit_rate': meta.get('total_hits', 0) / max(1, meta.get('total_hits', 0) + meta.get('total_misses', 0))
            }
        
        return stats
    
    def export_for_agent(self, agent_name: str, output_file: str):
        """
        导出 Agent 专用缓存
        
        Args:
            agent_name: Agent 名称
            output_file: 输出文件路径
        """
        if agent_name in self.caches:
            with open(output_file, 'wb') as f:
                pickle.dump(self.caches[agent_name], f)
            print(f"✅ 已导出 {agent_name} 缓存到 {output_file}")
        else:
            print(f"⚠️  {agent_name} 缓存不存在")
    
    def import_for_agent(self, agent_name: str, input_file: str):
        """
        导入 Agent 专用缓存
        
        Args:
            agent_name: Agent 名称
            input_file: 输入文件路径
        """
        try:
            with open(input_file, 'rb') as f:
                self.caches[agent_name] = OrderedDict(pickle.load(f))
            print(f"✅ 已导入 {agent_name} 缓存：{len(self.caches[agent_name])} 条")
            self._save_all()
        except Exception as e:
            print(f"❌ 导入失败：{e}")


# 全局实例
_embedding_manager = None

def get_embedding_manager() -> UnifiedEmbeddingManager:
    """获取全局 Embedding 管理器"""
    global _embedding_manager
    if _embedding_manager is None:
        _embedding_manager = UnifiedEmbeddingManager()
    return _embedding_manager
