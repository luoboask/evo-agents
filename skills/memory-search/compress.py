#!/usr/bin/env python3
"""
记忆索引压缩工具 - Memory Index Compressor
压缩旧的向量缓存，减少存储空间
"""

import json
import gzip
from pathlib import Path
from datetime import datetime


class MemoryIndexCompressor:
    """记忆索引压缩器"""
    
    def __init__(self, workspace):
        self.workspace = Path(workspace) if isinstance(workspace, str) else workspace
        self.vector_dir = self.workspace / 'memory' / 'vector_db'
        self.vector_dir.mkdir(parents=True, exist_ok=True)
    
    def compress_cache(self, days_old=30):
        """压缩旧的缓存文件"""
        cache_file = self.vector_dir / "integrated_cache.json"
        
        if not cache_file.exists():
            print("⚠️  缓存文件不存在")
            return 0
        
        # 加载缓存
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        
        if isinstance(cache, list):
            # 分离新旧记录
            cutoff = datetime.now().timestamp() - (days_old * 86400)
            new_entries = []
            old_entries = []
            
            for entry in cache:
                if isinstance(entry, dict):
                    timestamp = entry.get('timestamp', '')
                    try:
                        ts = datetime.fromisoformat(timestamp).timestamp()
                        if ts > cutoff:
                            new_entries.append(entry)
                        else:
                            old_entries.append(entry)
                    except:
                        new_entries.append(entry)
                else:
                    new_entries.append(entry)
            
            # 压缩旧记录
            if old_entries:
                compressed_file = self.vector_dir / f"cache_{days_old}days.json.gz"
                with gzip.open(compressed_file, 'wt', encoding='utf-8') as f:
                    json.dump(old_entries, f, ensure_ascii=False)
                
                # 保存新记录
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(new_entries, f, ensure_ascii=False, indent=2)
                
                original_size = cache_file.stat().st_size
                compressed_size = compressed_file.stat().st_size
                
                print(f"✅ 压缩完成:")
                print(f"   新记录：{len(new_entries)} 条")
                print(f"   旧记录：{len(old_entries)} 条 (压缩到 {compressed_file.name})")
                print(f"   原始大小：{original_size / 1024:.1f} KB")
                print(f"   压缩后：{compressed_size / 1024:.1f} KB")
                print(f"   压缩率：{compressed_size / original_size * 100:.1f}%")
                
                return len(old_entries)
            else:
                print("ℹ️  没有旧记录需要压缩")
                return 0
        else:
            print("⚠️  缓存格式不支持压缩")
            return 0
    
    def decompress_cache(self, compressed_file=None):
        """解压缩缓存文件"""
        if compressed_file is None:
            # 查找最新的压缩文件
            compressed_files = list(self.vector_dir.glob("cache_*days.json.gz"))
            if not compressed_files:
                print("⚠️  没有压缩文件")
                return 0
            compressed_file = sorted(compressed_files)[-1]
        
        # 加载压缩文件
        with gzip.open(compressed_file, 'rt', encoding='utf-8') as f:
            old_entries = json.load(f)
        
        # 加载当前缓存
        cache_file = self.vector_dir / "integrated_cache.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            if isinstance(cache, list):
                cache.extend(old_entries)
            else:
                cache = old_entries
        else:
            cache = old_entries
        
        # 保存合并后的缓存
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 解压缩完成:")
        print(f"   恢复 {len(old_entries)} 条记录")
        
        return len(old_entries)
    
    def get_compression_stats(self):
        """获取压缩统计"""
        stats = {
            'cache_file': self.vector_dir / "integrated_cache.json",
            'compressed_files': list(self.vector_dir.glob("cache_*days.json.gz")),
            'total_size': 0,
            'compressed_size': 0
        }
        
        if stats['cache_file'].exists():
            stats['total_size'] = stats['cache_file'].stat().st_size
        
        for f in stats['compressed_files']:
            stats['compressed_size'] += f.stat().st_size
        
        return stats


if __name__ == '__main__':
    import sys
    
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    compressor = MemoryIndexCompressor(workspace)
    
    if len(sys.argv) > 2:
        if sys.argv[2] == '--compress':
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
            compressor.compress_cache(days)
        elif sys.argv[2] == '--decompress':
            compressor.decompress_cache()
        elif sys.argv[2] == '--stats':
            stats = compressor.get_compression_stats()
            print(f"📊 压缩统计:")
            print(f"   缓存文件：{stats['cache_file']}")
            print(f"   缓存大小：{stats['total_size'] / 1024:.1f} KB")
            print(f"   压缩文件：{len(stats['compressed_files'])} 个")
            print(f"   压缩大小：{stats['compressed_size'] / 1024:.1f} KB")
    else:
        print("用法：python3 compress.py <workspace> [--compress <days>|--decompress|--stats]")
