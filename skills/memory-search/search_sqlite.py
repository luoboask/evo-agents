#!/usr/bin/env python3
"""
SQLite 记忆搜索 - 使用 Memory Hub
支持关键词匹配 + Ollama 向量语义搜索
"""

import argparse
from pathlib import Path

# 导入 Memory Hub (共享库)
# 添加 libs 目录到路径
import sys
LIBS_DIR = Path(__file__).parent.parent.parent / 'libs'
sys.path.insert(0, str(LIBS_DIR))

try:
    from memory_hub import MemoryHub
    MEMORY_HUB_ENABLED = True
except ImportError:
    MEMORY_HUB_ENABLED = False


class SQLiteMemorySearch:
    """SQLite 记忆搜索 - 使用 Memory Hub"""
    
    def __init__(self, agent_name='demo-agent'):
        """
        初始化记忆搜索
        
        Args:
            agent_name: Agent 名称（默认从环境变量获取）
        """
        if MEMORY_HUB_ENABLED:
            self.hub = MemoryHub(agent_name)
            # 验证数据库连接
            stats = self.hub.stats()
            if stats.get('total', 0) == 0:
                print(f"⚠️  警告：{agent_name} 的记忆数据库为空")
        else:
            self.hub = None
    
    def search(self, query, top_k=5, memory_type=None, semantic=False):
        """
        搜索记忆
        
        Args:
            query: 查询关键词
            top_k: 返回数量
            memory_type: 过滤类型
            semantic: 是否使用语义搜索
        
        Returns:
            记忆列表
        """
        if self.hub:
            return self.hub.search(query, top_k=top_k, memory_type=memory_type, semantic=semantic)
        return []
    
    def add(self, content, memory_type='observation', importance=5.0, tags=None, details=None, source_url=None):
        """
        添加记忆
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性
            tags: 标签列表
            details: 详细信息
            source_url: 来源 URL
        
        Returns:
            记忆 ID
        """
        if self.hub:
            metadata = {}
            if details:
                metadata['details'] = details
            if source_url:
                metadata['source_url'] = source_url
            
            return self.hub.add(
                content=content,
                memory_type=memory_type,
                importance=importance,
                tags=tags,
                metadata=metadata
            )
        return None
    
    def stats(self):
        """获取统计信息"""
        if self.hub:
            hub_stats = self.hub.stats()
            # 转换格式以匹配旧接口
            return {
                'total': hub_stats.get('total', 0),
                'by_type': hub_stats.get('by_type', {}),
                'avg_importance': hub_stats.get('avg_importance', 0)
            }
        return {'total': 0, 'by_type': {}, 'avg_importance': 0}
    
    def list_all(self, limit=20):
        """列出所有记忆"""
        if self.hub:
            return self.hub.search('', top_k=limit)
        return []


# ═══════════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='SQLite 记忆搜索')
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--add', '-a', help='添加记忆')
    parser.add_argument('--type', '-t', default='observation', help='记忆类型')
    parser.add_argument('--importance', '-i', type=float, default=5.0, help='重要性')
    parser.add_argument('--tags', help='标签（逗号分隔）')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有记忆')
    parser.add_argument('--stats', '-s', action='store_true', help='统计信息')
    parser.add_argument('--limit', '-n', type=int, default=10, help='返回数量')
    parser.add_argument('--semantic', action='store_true', help='使用语义搜索')
    parser.add_argument('--agent', default='demo-agent', help='Agent 名称')
    
    args = parser.parse_args()
    
    search = SQLiteMemorySearch(agent_name=args.agent)
    
    # 添加记忆
    if args.add:
        tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
        mem_id = search.add(args.add, args.type, args.importance, tags)
        print(f"✅ 已添加记忆 #{mem_id}")
        return
    
    # 统计信息
    if args.stats:
        # 直接从 Memory Hub 获取统计
        if search.hub:
            stats = search.hub.stats()
            print("📊 记忆统计:")
            print(f"  总数：{stats.get('total', 0)}")
            print(f"  按类型：{stats.get('by_type', {})}")
            print(f"  平均重要性：{stats.get('avg_importance', 0)}")
        else:
            print("⚠️  Memory Hub 不可用")
        return
    
    # 列出所有
    if args.list:
        memories = search.list_all(args.limit)
        print(f"📝 最近 {len(memories)} 条记忆:\n")
        for m in memories:
            print(f"  [{m['id']}] {m['content']}")
            print(f"      类型：{m['memory_type']} | 重要性：{m['importance']}")
            print()
        return
    
    # 搜索
    if args.query:
        results = search.search(args.query, args.limit, semantic=args.semantic)
        mode = " (语义)" if args.semantic else ""
        print(f"🔍 搜索：{args.query}{mode}\n")
        if not results:
            print("  未找到相关记忆")
        else:
            for r in results:
                print(f"  [{r['id']}] {r['content']}")
                print(f"      类型：{r['memory_type']} | 重要性：{r['importance']}")
                print()
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == '__main__':
    main()
