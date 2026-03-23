#!/usr/bin/env python3
"""
记忆流系统 - 使用 Memory Hub
基于 Generative Agents 论文
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 添加 skills 目录到路径以支持 memory_hub 导入
SKILLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILLS_DIR))

# 导入 Memory Hub
try:
    from memory_hub import MemoryHub, MemoryType
    MEMORY_HUB_ENABLED = True
except ImportError:
    MEMORY_HUB_ENABLED = False


class MemoryStream:
    """
    记忆流系统 - 使用 Memory Hub
    
    记忆类型：
    - observation: 原始观察/经历
    - reflection: 反思/洞察
    - knowledge: 知识
    - goal: 目标/意图
    """
    
    def __init__(self, agent_name: str = None):
        """
        初始化记忆流
        
        Args:
            agent_name: Agent 名称（默认从环境变量获取）
        """
        if agent_name is None:
            agent_name = os.environ.get('OPENCLAW_AGENT', 'ai-baby')
        
        self.agent_name = agent_name
        
        if MEMORY_HUB_ENABLED:
            self.hub = MemoryHub(agent_name)
        else:
            self.hub = None
    
    def add_memory(self, content: str, memory_type: str = 'observation',
                   importance: float = 5.0, tags: List[str] = None) -> int:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性 (1-10)
            tags: 标签列表
        
        Returns:
            记忆 ID
        """
        if self.hub:
            return self.hub.add(
                content=content,
                memory_type=memory_type,
                importance=importance,
                tags=tags
            )
        return 0
    
    def search_memories(self, query: str = '', top_k: int = 10,
                       memory_type: Optional[str] = None) -> List[Dict]:
        """
        搜索记忆
        
        Args:
            query: 搜索关键词
            top_k: 返回数量
            memory_type: 过滤类型
        
        Returns:
            记忆列表
        """
        if self.hub:
            return self.hub.search(
                query=query,
                top_k=top_k,
                memory_type=memory_type
            )
        return []
    
    def get_recent_memories(self, hours: int = 24, top_k: int = 10) -> List[Dict]:
        """
        获取最近记忆
        
        Args:
            hours: 最近多少小时
            top_k: 返回数量
        
        Returns:
            记忆列表
        """
        # 获取所有记忆，然后按时间过滤
        memories = self.search_memories(top_k=top_k * 3)
        
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent = []
        
        for m in memories:
            try:
                created_at = datetime.fromisoformat(m['created_at']).timestamp()
                if created_at >= cutoff:
                    recent.append(m)
                    if len(recent) >= top_k:
                        break
            except:
                continue
        
        return recent
    
    def generate_reflection(self, lookback_hours: int = 24,
                           min_memories: int = 5) -> Optional[Dict]:
        """
        生成反思
        
        Args:
            lookback_hours: 回顾多少小时
            min_memories: 最小记忆数
        
        Returns:
            反思记忆
        """
        # 获取最近记忆
        memories = self.get_recent_memories(lookback_hours, min_memories * 2)
        
        if len(memories) < min_memories:
            return None
        
        # 简单反思：总结记忆内容
        contents = [m['content'] for m in memories[:10]]
        reflection_content = f"反思：{'。'.join(contents)}"
        
        # 添加反思记忆
        reflection_id = self.add_memory(
            content=reflection_content,
            memory_type='reflection',
            importance=7.0,
            tags=['reflection', 'summary']
        )
        
        return {
            'id': reflection_id,
            'content': reflection_content,
            'memory_type': 'reflection',
            'importance': 7.0
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if self.hub:
            return self.hub.stats()
        return {'total': 0, 'by_type': {}, 'avg_importance': 0}
    
    def list_memories(self, limit: int = 20) -> List[Dict]:
        """列出所有记忆"""
        return self.search_memories(top_k=limit)


# 便捷函数
def create_memory_stream(agent_name: str = None) -> MemoryStream:
    """创建记忆流实例"""
    return MemoryStream(agent_name)


# 命令行接口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='记忆流系统')
    parser.add_argument('--add', '-a', help='添加记忆')
    parser.add_argument('--type', '-t', default='observation', help='记忆类型')
    parser.add_argument('--importance', '-i', type=float, default=5.0, help='重要性')
    parser.add_argument('--tags', help='标签（逗号分隔）')
    parser.add_argument('--search', '-s', help='搜索记忆')
    parser.add_argument('--list', '-l', action='store_true', help='列出记忆')
    parser.add_argument('--stats', action='store_true', help='统计信息')
    parser.add_argument('--limit', '-n', type=int, default=10, help='返回数量')
    parser.add_argument('--reflect', action='store_true', help='生成反思')
    
    args = parser.parse_args()
    
    # 创建记忆流
    agent_name = os.environ.get('OPENCLAW_AGENT', 'ai-baby')
    ms = MemoryStream(agent_name=agent_name)
    
    # 添加记忆
    if args.add:
        tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
        mem_id = ms.add_memory(args.add, args.type, args.importance, tags)
        print(f"✅ 已添加记忆 #{mem_id}")
    
    # 搜索记忆
    elif args.search:
        results = ms.search_memories(args.search, args.limit)
        print(f"🔍 搜索：{args.search}\n")
        for r in results:
            print(f"  [{r['id']}] {r['content']}")
            print(f"      类型：{r['memory_type']} | 重要性：{r['importance']}")
            print()
    
    # 列出记忆
    elif args.list:
        memories = ms.list_memories(args.limit)
        print(f"📝 最近 {len(memories)} 条记忆:\n")
        for m in memories:
            print(f"  [{m['id']}] {m['content']}")
            print(f"      类型：{m['memory_type']} | 重要性：{m['importance']}")
            print()
    
    # 统计信息
    elif args.stats:
        stats = ms.get_stats()
        print("📊 记忆统计:")
        print(f"  总数：{stats.get('total', 0)}")
        print(f"  按类型：{stats.get('by_type', {})}")
        print(f"  平均重要性：{stats.get('avg_importance', 0)}")
    
    # 生成反思
    elif args.reflect:
        reflection = ms.generate_reflection()
        if reflection:
            print(f"✅ 生成反思：{reflection['content']}")
        else:
            print("⚠️  记忆不足，无法生成反思")
    
    else:
        parser.print_help()
