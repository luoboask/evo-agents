#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG 检索记录器
集成到记忆搜索流程中，自动记录每次检索的指标
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# 添加 libs 到路径
from typing import Optional, Dict, Any

# 配置
SKILLS_DIR = Path(__file__).parent
# 使用 memory_hub 的相同路径：data/${agent_name}/logs/evaluations.jsonl
DATA_DIR = SKILLS_DIR.parent.parent / "data" / os.environ.get("OPENCLAW_AGENT", os.path.basename(str(resolve_workspace())).replace("workspace-", ""))
LOGS_DIR = DATA_DIR / "logs"
EVALUATIONS_FILE = LOGS_DIR / "evaluations.jsonl"

# 确保目录存在
LOGS_DIR.mkdir(parents=True, exist_ok=True)


class RetrievalRecorder:
    """检索记录器 - 用于集成到记忆搜索流程"""
    
    def __init__(self):
        self.current_query = None
        self.start_time = None
        
    def start(self, query: str):
        """开始记录一次检索"""
        self.current_query = query
        self.start_time = time.time()
    
    def finish(self, retrieved_count: int, similarity_score: Optional[float] = None,
               feedback: Optional[str] = None, used_in_response: bool = True,
               top_k: Optional[int] = None, token_cost: Optional[int] = None) -> Dict:
        """
        完成检索记录
        
        Returns:
            评估记录字典
        """
        latency_ms = (time.time() - self.start_time) * 1000 if self.start_time else 0
        
        # 加载当前配置
        config_file = SKILLS_DIR / "config.json"
        current_config = {"top_k": 5, "similarity_threshold": 0.7, "chunk_size": 512}
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                current_config = config.get("current_config", current_config)
        
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "query": self.current_query,
            "retrieved_count": retrieved_count,
            "latency_ms": round(latency_ms, 2),
            "feedback": feedback,
            "used_in_response": used_in_response,
            "config": {
                "top_k": top_k or current_config["top_k"],
                "similarity_threshold": similarity_score or current_config["similarity_threshold"],
                "chunk_size": current_config["chunk_size"]
            },
            "similarity_score": similarity_score,
            "token_cost": token_cost
        }
        
        # 追加到日志文件
        with open(EVALUATIONS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evaluation, ensure_ascii=False) + '\n')
        
        # 重置
        self.current_query = None
        self.start_time = None
        
        return evaluation
    
    def record_feedback(self, query: str, feedback: str):
        """
        为之前的检索添加反馈
        
        用于事后补充用户反馈
        """
        # 读取所有记录
        evaluations = []
        if EVALUATIONS_FILE.exists():
            with open(EVALUATIONS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        evaluations.append(json.loads(line.strip()))
                    except:
                        continue
        
        # 找到最近的匹配查询并更新反馈
        for eval_data in reversed(evaluations):
            if eval_data.get("query") == query:
                eval_data["feedback"] = feedback
                break
        
        # 写回文件
        with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
            for eval_data in evaluations:
                f.write(json.dumps(eval_data, ensure_ascii=False) + '\n')


# 便捷函数
_recorder = RetrievalRecorder()

def start_recording(query: str):
    """开始记录检索"""
    _recorder.start(query)

def finish_recording(retrieved_count: int, similarity_score: Optional[float] = None,
                     feedback: Optional[str] = None, **kwargs) -> Dict:
    """完成检索记录"""
    return _recorder.finish(retrieved_count, similarity_score, feedback, **kwargs)

def record_feedback(query: str, feedback: str):
    """记录用户反馈"""
    _recorder.record_feedback(query, feedback)


if __name__ == "__main__":
    # 测试
    print("测试检索记录器...")
    
    start_recording("测试查询")
    time.sleep(0.1)  # 模拟检索延迟
    result = finish_recording(
        retrieved_count=5,
        similarity_score=0.85,
        top_k=5
    )
    
    print(f"✅ 记录完成：{result['timestamp']}")
    print(f"   Query: {result['query']}")
    print(f"   Retrieved: {result['retrieved_count']}")
    print(f"   Latency: {result['latency_ms']}ms")
    print(f"   Similarity: {result['similarity_score']}")
