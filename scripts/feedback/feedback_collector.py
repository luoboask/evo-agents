# -*- coding: utf-8 -*-
"""
用户反馈收集器 - 收集用户对回答的评分

功能:
- 1-5 分评分
- 存储到 effect_tracker
- 用于质量评分优化
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class FeedbackCollector:
    """用户反馈收集器"""
    
    def __init__(self, agent_name: str = "default", db_path: str = None):
        """
        初始化反馈收集器
        
        Args:
            agent_name: Agent 名称
            db_path: 数据库路径（默认在 data/{agent}/memory/evolution_effects.db）
        """
        if db_path:
            self.db_path = Path(db_path)
        else:
            workspace = Path(__file__).parent.parent.parent
            self.db_path = workspace / "data" / agent_name / "memory" / "evolution_effects.db"
        
        # 确保目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_db()
        print(f"📝 用户反馈收集器已初始化")
        print(f"   数据库：{self.db_path}")
    
    def _init_db(self):
        """初始化数据库表"""
        # 确保目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 用户反馈表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solution_id INTEGER,
                problem TEXT,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                comment TEXT,
                user_id TEXT,
                session_id TEXT,
                created_at TEXT,
                FOREIGN KEY (solution_id) REFERENCES solutions(id)
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_solution ON user_feedback(solution_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_rating ON user_feedback(rating)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_created ON user_feedback(created_at)')
        
        conn.commit()
        conn.close()
    
    def submit_feedback(self,
                       solution_id: int,
                       rating: int,
                       problem: str = None,
                       comment: str = None,
                       user_id: str = None,
                       session_id: str = None) -> int:
        """
        提交用户反馈
        
        Args:
            solution_id: 方案 ID
            rating: 评分 (1-5)
            problem: 问题描述
            comment: 评论
            user_id: 用户 ID
            session_id: 会话 ID
        
        Returns:
            反馈 ID
        """
        if rating < 1 or rating > 5:
            raise ValueError("评分必须在 1-5 之间")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_feedback 
            (solution_id, problem, rating, comment, user_id, session_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            solution_id,
            problem,
            rating,
            comment,
            user_id,
            session_id,
            datetime.now().isoformat()
        ))
        
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # 更新 effect_tracker 中的成功率
        self._update_solution_stats(solution_id)
        
        print(f"✅ 已提交反馈：方案{solution_id} 评分{rating}")
        return feedback_id
    
    def _update_solution_stats(self, solution_id: int):
        """更新方案统计（成功率）"""
        # 简化：不依赖 effect_tracker 的 solutions 表
        # 反馈数据独立存储，通过 get_avg_rating() 查询
        pass
    
    def get_feedback(self, solution_id: int) -> List[Dict]:
        """获取方案的反馈"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM user_feedback
            WHERE solution_id = ?
            ORDER BY created_at DESC
        ''', (solution_id,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_avg_rating(self, solution_id: int) -> float:
        """获取平均评分"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT AVG(rating) FROM user_feedback
            WHERE solution_id = ?
        ''', (solution_id,))
        
        result = cursor.fetchone()
        avg = result[0] or 0.0
        
        conn.close()
        return avg
    
    def get_stats(self, solution_id: int = None) -> Dict:
        """获取反馈统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        if solution_id:
            # 单个方案统计
            cursor.execute('''
                SELECT AVG(rating), COUNT(*), MAX(created_at)
                FROM user_feedback
                WHERE solution_id = ?
            ''', (solution_id,))
            result = cursor.fetchone()
            stats = {
                'solution_id': solution_id,
                'avg_rating': result[0] or 0.0,
                'count': result[1] or 0,
                'last_feedback': result[2]
            }
        else:
            # 全局统计
            cursor.execute('''
                SELECT AVG(rating), COUNT(DISTINCT solution_id), COUNT(*)
                FROM user_feedback
            ''')
            result = cursor.fetchone()
            stats = {
                'avg_rating': result[0] or 0.0,
                'solutions_with_feedback': result[1] or 0,
                'total_feedback': result[2] or 0
            }
        
        conn.close()
        return stats
    
    def export_feedback(self, output_file: str = None):
        """导出反馈数据"""
        if not output_file:
            output_file = self.db_path.parent / "feedback_export.json"
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_feedback ORDER BY created_at DESC')
        feedback_list = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已导出 {len(feedback_list)} 条反馈到 {output_file}")
        return feedback_list


# 快捷函数
def submit_feedback(solution_id: int, rating: int, **kwargs):
    """快捷提交反馈"""
    collector = FeedbackCollector()
    return collector.submit_feedback(solution_id, rating, **kwargs)


def get_avg_rating(solution_id: int) -> float:
    """快捷获取平均评分"""
    collector = FeedbackCollector()
    return collector.get_avg_rating(solution_id)
