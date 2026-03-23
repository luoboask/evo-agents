#!/usr/bin/env python3
"""
真实学习记录系统 - 不再自动生成假数据
只记录真实的学习内容（来自用户输入、任务执行、代码运行等）
"""

import json
from datetime import datetime
from pathlib import Path
from knowledge_base import KnowledgeBase

class RealLearningRecorder:
    """真实学习记录器"""
    
    def __init__(self):
        self.workspace = Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self.kb = KnowledgeBase()
    
    def record_learning(self, domain, subtopic, content, insight, 
                       thinking=None, key_point=None, learning_type='实践学习',
                       difficulty='中级', time_spent='未知', outcome='success'):
        """
        记录一次真实学习
        
        Args:
            domain: 领域（如"人工智能"、"前端开发"）
            subtopic: 子主题（如"Transformer"、"React"）
            content: 学习内容描述
            insight: 收获/理解
            thinking: 反思/思考（可选）
            key_point: 关键知识点（可选）
            learning_type: 学习类型（实践学习/理论学习/项目学习等）
            difficulty: 难度
            time_spent: 耗时
            outcome: 结果
        """
        learning = {
            'timestamp': datetime.now().isoformat(),
            'type': learning_type,
            'content': content,
            'outcome': outcome,
            '收获': insight,
            '思考': thinking,
            '知识点': key_point,
            'details': {
                'domain': domain,
                'subtopic': subtopic,
                'difficulty': difficulty,
                'time_spent': time_spent
            }
        }
        
        # 写入学习日志
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.learning_dir / f'scheduled_learning_{today}.jsonl'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(learning, ensure_ascii=False) + '\n')
        
        # 写入知识库
        try:
            self.kb.add_knowledge(learning)
        except Exception as e:
            print(f"⚠️ 知识库写入失败：{e}")
        
        return learning
    
    def record_from_task(self, task_result):
        """从任务执行结果中提取学习"""
        # TODO: 分析任务执行结果，提取学到的内容
        pass
    
    def record_from_code(self, code_change):
        """从代码变更中提取学习"""
        # TODO: 分析代码 diff，提取技术决策和原因
        pass
    
    def query_learning(self, domain=None, subtopic=None, limit=10):
        """查询学习记录"""
        return self.kb.query_by_domain(domain, limit) if domain else []
    
    def get_summary(self):
        """获取学习摘要"""
        return self.kb.get_summary()


# 使用示例
if __name__ == '__main__':
    recorder = RealLearningRecorder()
    
    # 示例：记录一次真实学习
    learning = recorder.record_learning(
        domain='系统架构',
        subtopic='工作台 API',
        content='添加了/api/knowledge 端点，展示知识库内容',
        insight='理解了 RESTful API 设计原则，掌握了 SQLite 查询优化技巧',
        thinking='这个模式可以应用到其他数据展示场景',
        key_point='知识图谱可视化 + SQLite 动态查询',
        learning_type='项目学习',
        difficulty='中级',
        time_spent='45 分钟',
        outcome='completed'
    )
    
    print(f"✅ 学习记录已保存：{learning['content']}")
    print(f"   知识点：{learning['知识点']}")
    print(f"   收获：{learning['收获']}")
