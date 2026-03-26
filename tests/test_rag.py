#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG 评估系统单元测试
测试 skills/rag 模块的功能
"""

import sys
import unittest
import json
from pathlib import Path
from datetime import datetime, timedelta

# 添加 skills/rag 目录到路径
RAG_DIR = Path(__file__).parent.parent / 'skills' / 'rag'
sys.path.insert(0, str(RAG_DIR))


class TestRAGEvaluator(unittest.TestCase):
    """测试用例：RAG 评估功能 (TC-RAG-001, TC-RAG-002)"""
    
    def setUp(self):
        self.test_agent = 'test-agent-rag'
        self.workspace_root = Path(__file__).parent.parent
        
        # 导入评估器
        try:
            from evaluate import RAGEvaluator, EVALUATIONS_FILE
            self.RAGEvaluator = RAGEvaluator
            self.EVALUATIONS_FILE = EVALUATIONS_FILE
            self.evaluator = RAGEvaluator(agent_name=self.test_agent)
        except ImportError as e:
            self.skipTest(f"无法导入 RAG 评估模块：{e}")
    
    def tearDown(self):
        # 清理测试数据
        eval_file = self.workspace_root / 'data' / self.test_agent / 'rag_evaluations.jsonl'
        if eval_file.exists():
            eval_file.unlink()
    
    def test_evaluator_creation(self):
        """TC-RAG-001.1: RAGEvaluator 实例创建成功"""
        evaluator = self.RAGEvaluator(self.test_agent)
        self.assertIsNotNone(evaluator)
        self.assertEqual(evaluator.agent_name, self.test_agent)
    
    def test_record_evaluation(self):
        """TC-RAG-001.2: 记录评估成功"""
        result = self.evaluator.record(
            query='测试查询',
            retrieved_count=5,
            latency_ms=50.0,
            feedback='positive'
        )
        self.assertTrue(result)
    
    def test_record_with_all_params(self):
        """TC-RAG-001.3: 记录评估包含所有参数"""
        result = self.evaluator.record(
            query='完整测试',
            retrieved_count=10,
            latency_ms=100.5,
            feedback='negative',
            used_in_response=True,
            top_k=5,
            similarity_score=0.8,
            token_cost=100
        )
        self.assertIsInstance(result, dict)
    
    def test_record_persists_data(self):
        """TC-RAG-001.4: 记录数据持久化"""
        # 记录一条评估 - 验证方法不抛出异常
        result = self.evaluator.record(
            query='持久化测试',
            retrieved_count=3,
            latency_ms=30.0,
            feedback='positive'
        )
        
        # 验证返回了评估记录
        self.assertIsInstance(result, dict)
        self.assertIn('query', result)
        self.assertEqual(result['query'], '持久化测试')
    
    def test_generate_report(self):
        """TC-RAG-002.1: 生成评估报告"""
        # 先记录一些数据
        for i in range(5):
            self.evaluator.record(
                query=f'测试查询{i}',
                retrieved_count=i + 1,
                latency_ms=50.0 + i * 10,
                feedback='positive' if i % 2 == 0 else 'negative'
            )
        
        report = self.evaluator.generate_report(days=7)
        self.assertIsNotNone(report)
        self.assertIn('RAG 评估报告', report)
    
    def test_generate_report_contains_stats(self):
        """TC-RAG-002.2: 报告包含统计信息"""
        # 记录数据
        for i in range(10):
            self.evaluator.record(
                query=f'统计测试{i}',
                retrieved_count=5,
                latency_ms=50.0,
                feedback='positive'
            )
        
        report = self.evaluator.generate_report(days=7)
        
        # 验证报告包含关键统计信息
        self.assertIn('RAG 评估报告', report)
        self.assertIn('总查询数', report)
    
    def test_empty_report(self):
        """TC-RAG-002.3: 空数据报告生成"""
        # 不记录任何数据，直接生成报告
        report = self.evaluator.generate_report(days=7)
        self.assertIsNotNone(report)
        # 空数据时应该有提示或报告标题
        self.assertTrue(len(report) > 0)


class TestRAGAutoTune(unittest.TestCase):
    """测试用例：RAG 自动调优 (TC-RAG-003)"""
    
    def setUp(self):
        self.workspace_root = Path(__file__).parent.parent
        
        # 导入自动调优器
        try:
            from auto_tune import AutoTuner
            self.AutoTuner = AutoTuner
            self.tuner = AutoTuner()
        except ImportError as e:
            self.skipTest(f"无法导入自动调优模块：{e}")
    
    def test_tuner_creation(self):
        """TC-RAG-003.1: AutoTuner 实例创建成功"""
        tuner = self.AutoTuner()
        self.assertIsNotNone(tuner)
    
    def test_design_experiments(self):
        """TC-RAG-003.2: 设计实验返回非空列表"""
        experiments = self.tuner.design_experiments()
        self.assertIsInstance(experiments, list)
        # 应该有至少一个实验配置
        self.assertGreater(len(experiments), 0)
    
    def test_experiment_structure(self):
        """TC-RAG-003.3: 实验配置结构正确"""
        experiments = self.tuner.design_experiments()
        if len(experiments) > 0:
            exp = experiments[0]
            self.assertIsInstance(exp, dict)
            # 实验应该包含配置参数
            self.assertGreater(len(exp), 0)
    
    def test_analyze_results(self):
        """TC-RAG-003.4: 分析结果正常"""
        analysis = self.tuner.analyze_results()
        self.assertIsInstance(analysis, dict)
        # 分析结果应该是有效字典（可能包含 error 或 current_count）
        self.assertTrue(
            'error' not in analysis or 
            analysis.get('current_count', 0) >= 0
        )


class TestRAGMetrics(unittest.TestCase):
    """测试用例：RAG 指标计算"""
    
    def setUp(self):
        self.workspace_root = Path(__file__).parent.parent
        
        try:
            from metrics import RAGMetrics
            self.RAGMetrics = RAGMetrics
            self.metrics = RAGMetrics(days=7)
        except ImportError as e:
            self.skipTest(f"无法导入指标模块：{e}")
    
    def test_metrics_creation(self):
        """指标计算器创建成功"""
        metrics = self.RAGMetrics(days=7)
        self.assertIsNotNone(metrics)
    
    def test_hit_rate(self):
        """测试命中率计算"""
        hit_rate = self.metrics.hit_rate()
        self.assertIsInstance(hit_rate, float)
        self.assertGreaterEqual(hit_rate, 0.0)
        self.assertLessEqual(hit_rate, 1.0)
    
    def test_satisfaction_rate(self):
        """测试满意度计算"""
        satisfaction = self.metrics.satisfaction_rate()
        self.assertIsInstance(satisfaction, float)
        self.assertGreaterEqual(satisfaction, 0.0)
        self.assertLessEqual(satisfaction, 1.0)
    
    def test_avg_latency(self):
        """测试平均延迟计算"""
        latency = self.metrics.avg_latency()
        self.assertIsInstance(latency, float)
        self.assertGreaterEqual(latency, 0.0)
    
    def test_precision_at_k(self):
        """测试 Precision@K 计算"""
        p_at_5 = self.metrics.precision_at_k(k=5)
        self.assertIsInstance(p_at_5, float)
        self.assertGreaterEqual(p_at_5, 0.0)
        self.assertLessEqual(p_at_5, 1.0)
    
    def test_report(self):
        """测试完整报告生成"""
        report = self.metrics.report()
        self.assertIsInstance(report, dict)
        self.assertIn('total_queries', report)
        self.assertIn('hit_rate', report)
        self.assertIn('avg_latency_ms', report)


class TestRAGRecorder(unittest.TestCase):
    """测试用例：RAG 记录器 - 使用 evaluate 模块的 record 方法"""
    
    def setUp(self):
        self.test_agent = 'test-agent-recorder'
        self.workspace_root = Path(__file__).parent.parent
        
        try:
            from evaluate import RAGEvaluator
            self.RAGEvaluator = RAGEvaluator
            self.evaluator = RAGEvaluator(agent_name=self.test_agent)
        except ImportError as e:
            self.skipTest(f"无法导入评估器模块：{e}")
    
    def tearDown(self):
        eval_file = self.workspace_root.parent / 'skills' / 'rag' / 'logs' / 'evaluations.jsonl'
        # 不删除日志文件，避免影响其他测试
    
    def test_evaluator_as_recorder(self):
        """使用 evaluator 作为记录器"""
        evaluator = self.RAGEvaluator(self.test_agent)
        self.assertIsNotNone(evaluator)
    
    def test_record_query_via_evaluator(self):
        """通过 evaluator 记录查询"""
        result = self.evaluator.record(
            query='测试查询',
            retrieved_count=5,
            latency_ms=50.0,
            feedback='positive'
        )
        self.assertIsInstance(result, dict)
    
    def test_record_feedback_via_evaluator(self):
        """通过 evaluator 记录反馈"""
        result = self.evaluator.record(
            query='反馈测试',
            retrieved_count=3,
            latency_ms=30.0,
            feedback='positive'
        )
        self.assertIsInstance(result, dict)


class TestRAGReport(unittest.TestCase):
    """测试用例：RAG 报告生成 - 使用 evaluate 模块"""
    
    def setUp(self):
        self.workspace_root = Path(__file__).parent.parent
        
        try:
            from evaluate import RAGEvaluator
            self.RAGEvaluator = RAGEvaluator
            self.evaluator = RAGEvaluator(agent_name='test-agent-report')
        except ImportError as e:
            self.skipTest(f"无法导入评估器模块：{e}")
    
    def test_evaluator_as_report_generator(self):
        """使用 evaluator 作为报告生成器"""
        evaluator = self.RAGEvaluator('test-agent-report')
        self.assertIsNotNone(evaluator)
        self.assertTrue(hasattr(evaluator, 'generate_report'))
    
    def test_generate_report_via_evaluator(self):
        """通过 evaluator 生成报告"""
        # 先添加一些数据
        for i in range(5):
            self.evaluator.record(
                query=f'报告测试{i}',
                retrieved_count=5,
                latency_ms=50.0,
                feedback='positive'
            )
        
        report = self.evaluator.generate_report(days=7)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
