#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG 检索记录器
集成到记忆搜索流程中，自动记录每次检索的指标
"""

from pathlib import Path
import sys
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any

# 添加 libs 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "libs"))
from path_utils import resolve_workspace, resolve_data_dir


class RetrievalRecorder:
    """RAG 检索记录器"""
    
    def __init__(self, workspace=None):
        self.workspace = resolve_workspace() if not workspace else Path(workspace)
        # 使用 data/<agent>/rag/ 而不是 data/rag/
        agent_name = self.workspace.name.replace('workspace-', '')
        self.data_dir = self.workspace / 'data' / agent_name / 'rag'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.data_dir / 'retrieval_log.jsonl'
    
    def record(self, query: str, results: list, latency_ms: float, 
               feedback: Optional[str] = None, metadata: Optional[Dict] = None):
        """记录检索"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'result_count': len(results),
            'latency_ms': latency_ms,
            'feedback': feedback,
            'metadata': metadata or {},
            'results': [{'id': r.get('id', ''), 'score': r.get('score', 0)} for r in results]
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        return entry
    
    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """获取统计信息"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        total = 0
        total_latency = 0
        feedback_count = 0
        
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        ts = datetime.fromisoformat(entry['timestamp'])
                        if ts >= cutoff:
                            total += 1
                            total_latency += entry.get('latency_ms', 0)
                            if entry.get('feedback'):
                                feedback_count += 1
                    except:
                        pass
        
        return {
            'total_queries': total,
            'avg_latency_ms': total_latency / total if total > 0 else 0,
            'feedback_count': feedback_count,
            'log_file': str(self.log_file)
        }


if __name__ == '__main__':
    recorder = RetrievalRecorder()
    stats = recorder.get_stats()
    print(f"RAG 统计:")
    print(f"  总查询：{stats['total_queries']}")
    print(f"  平均延迟：{stats['avg_latency_ms']:.1f}ms")
    print(f"  反馈数：{stats['feedback_count']}")
