# -*- coding: utf-8 -*-
"""
用户反馈模块 - 收集和使用用户反馈

使用方式:
from scripts.feedback import submit_feedback, get_avg_rating

# 提交反馈
submit_feedback(solution_id=1, rating=5, comment="很好！")

# 获取平均评分
rating = get_avg_rating(solution_id=1)
"""

from .feedback_collector import FeedbackCollector, submit_feedback, get_avg_rating

__all__ = ['FeedbackCollector', 'submit_feedback', 'get_avg_rating']
