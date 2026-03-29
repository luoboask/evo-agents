#!/usr/bin/env python3
"""
记忆去重模块 - 借鉴 Mem0
自动检测并跳过重复记忆
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class MemoryDeduplicator:
    """记忆去重器"""
    
    def __init__(self, workspace_path: Path = None):
        self.workspace = workspace_path or Path.cwd()
        self.memory_dir = self.workspace / 'memory'
        self.similarity_threshold = 0.85  # 相似度阈值
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        计算两段文本的相似度（简化版 Jaccard 相似度）
        
        Args:
            text1: 文本 1
            text2: 文本 2
            
        Returns:
            相似度分数 (0-1)
        """
        # 分词
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # 去除停用词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个'}
        words1 = words1 - stopwords
        words2 = words2 - stopwords
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard 相似度
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def find_similar_memories(self, content: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        查找相似记忆
        
        Args:
            content: 新内容
            top_k: 返回数量
            
        Returns:
            [(记忆内容，相似度), ...]
        """
        similar = []
        
        # 读取今日记忆文件
        today = datetime.now().strftime('%Y-%m-%d')
        memory_file = self.memory_dir / f"{today}.md"
        
        if not memory_file.exists():
            return similar
        
        # 读取现有记忆
        with open(memory_file, 'r', encoding='utf-8') as f:
            content_lines = []
            for line in f:
                if line.startswith('- ['):
                    # 提取记忆内容
                    start = line.find(']') + 1
                    if start > 0:
                        content_lines.append(line[start:].strip())
        
        # 计算相似度
        for existing_content in content_lines:
            similarity = self.compute_similarity(content, existing_content)
            if similarity > 0.5:  # 只保留相似度>0.5 的
                similar.append((existing_content, similarity))
        
        # 排序并返回 top_k
        similar.sort(key=lambda x: -x[1])
        return similar[:top_k]
    
    def is_duplicate(self, content: str, threshold: float = None) -> Tuple[bool, Optional[float]]:
        """
        检查是否是重复记忆
        
        Args:
            content: 新内容
            threshold: 相似度阈值（默认 0.85）
            
        Returns:
            (是否重复，最高相似度)
        """
        threshold = threshold or self.similarity_threshold
        similar = self.find_similar_memories(content, top_k=1)
        
        if similar and similar[0][1] >= threshold:
            return True, similar[0][1]
        
        return False, similar[0][1] if similar else 0.0


if __name__ == '__main__':
    # 测试
    dedup = MemoryDeduplicator()
    
    # 测试相似度计算
    text1 = "如何配置 OpenClaw"
    text2 = "怎么设置 OpenClaw"
    text3 = "今天天气真好"
    
    sim1 = dedup.compute_similarity(text1, text2)
    sim2 = dedup.compute_similarity(text1, text3)
    
    print(f"相似度测试:")
    print(f"  '{text1}' vs '{text2}': {sim1:.2f}")
    print(f"  '{text1}' vs '{text3}': {sim2:.2f}")
    
    # 测试去重
    print(f"\n去重测试:")
    is_dup, score = dedup.is_duplicate("如何配置 OpenClaw")
    print(f"  '如何配置 OpenClaw' 是否重复：{is_dup} (相似度：{score:.2f})")
