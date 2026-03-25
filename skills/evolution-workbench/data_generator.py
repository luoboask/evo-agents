#!/usr/bin/env python3
"""
动态数据生成器
生成真实的进化数据并存储到数据库
"""

import random
import json
from datetime import datetime, timedelta
from database import EvolutionDatabase


class DynamicDataGenerator:
    """动态数据生成器"""
    
    def __init__(self):
        self.db = EvolutionDatabase()
        self.generate_initial_data()
    
    def generate_initial_data(self):
        """生成初始数据"""
        print("🔄 生成初始动态数据...")
        
        # 生成实例数据
        self._generate_instances()
        
        # 生成事件数据
        self._generate_events()
        
        # 生成 Bug 数据
        self._generate_bugs()
        
        # 生成预测数据
        self._generate_predictions()
        
        # 生成智能评分历史
        self._generate_intelligence_history()
        
        # 生成指标数据
        self._generate_metrics()
        
        print("✅ 初始数据生成完成")
    
    def _generate_instances(self):
        """生成实例数据"""
        instances = [
            {
                'id': 'sandbox-REQ-001-a1b2c3d4',
                'requirement_id': 'REQ-001',
                'status': 'RUNNING',
                'config': {
                    'frontend_code': './frontend/login',
                    'backend_code': './backend/login',
                    'requirement_desc': '用户登录功能'
                },
                'port': 8154,
                'results': {'passed': 5, 'failed': 0}
            },
            {
                'id': 'sandbox-REQ-002-e5f6g7h8',
                'requirement_id': 'REQ-002',
                'status': 'COMPLETED',
                'config': {
                    'frontend_code': './frontend/products',
                    'backend_code': './backend/products',
                    'requirement_desc': '商品列表功能'
                },
                'port': 8231,
                'results': {'passed': 8, 'failed': 1}
            },
            {
                'id': 'sandbox-REQ-003-i9j0k1l2',
                'requirement_id': 'REQ-003',
                'status': 'CREATED',
                'config': {
                    'frontend_code': './frontend/cart',
                    'backend_code': './backend/cart',
                    'requirement_desc': '购物车功能'
                },
                'port': 8376,
                'results': {}
            }
        ]
        
        for inst in instances:
            try:
                self.db.create_instance(
                    inst['id'],
                    inst['requirement_id'],
                    inst['config'],
                    inst['port']
                )
                
                # 更新状态
                if inst['status'] == 'RUNNING':
                    self.db.update_instance_status(
                        inst['id'],
                        'RUNNING',
                        started_at=(datetime.now() - timedelta(hours=2)).isoformat(),
                        results=inst['results']
                    )
                elif inst['status'] == 'COMPLETED':
                    self.db.update_instance_status(
                        inst['id'],
                        'COMPLETED',
                        started_at=(datetime.now() - timedelta(days=1)).isoformat(),
                        stopped_at=(datetime.now() - timedelta(hours=20)).isoformat(),
                        results=inst['results']
                    )
            except:
                pass  # 已存在则跳过
    
    def _generate_events(self):
        """生成事件数据"""
        events = [
            ('INSTANCE_CREATED', '创建实例 sandbox-REQ-003-i9j0k1l2', 'REQ-003'),
            ('INSTANCE_STARTED', '启动实例 sandbox-REQ-003-i9j0k1l2', 'REQ-003'),
            ('TEST_GENERATED', '生成 12 个测试用例', 'REQ-002'),
            ('INTEGRATION_COMPLETED', '联调完成，通过 8/9', 'REQ-002'),
            ('BUG_DETECTED', '发现 Bug: 接口路径不匹配', 'REQ-002'),
            ('BUG_AUTO_FIXED', '自动修复 Bug: 更新路径', 'REQ-002'),
            ('INSTANCE_STOPPED', '停止实例 sandbox-REQ-002-e5f6g7h8', 'REQ-002'),
            ('PREDCTION_FULFILLED', '预测实现: 技能数量达到 9 个', None),
        ]
        
        for event_type, desc, req_id in events:
            try:
                self.db.log_event(event_type, desc, req_id)
            except:
                pass
    
    def _generate_bugs(self):
        """生成 Bug 数据"""
        bugs = [
            ('INTERFACE_MISMATCH', 'HIGH', '接口路径不匹配: /api/user vs /api/users', 'REQ-002'),
            ('DATA_FORMAT_ERROR', 'MEDIUM', '响应字段类型错误: age 应为 number', 'REQ-002'),
            ('STATUS_CODE_MISMATCH', 'LOW', '期望 401 实际返回 403', 'REQ-002'),
            ('INTERFACE_MISMATCH', 'CRITICAL', '缺少 /api/login 接口', 'REQ-001'),
        ]
        
        for bug_type, severity, desc, req_id in bugs:
            try:
                bug_id = self.db.record_bug(bug_type, severity, desc, req_id)
                # 标记部分已修复
                if random.random() > 0.3:
                    self.db.fix_bug(bug_id, {'method': 'auto', 'timestamp': datetime.now().isoformat()})
            except:
                pass
    
    def _generate_predictions(self):
        """生成预测数据"""
        predictions = [
            ('memory_growth', '记忆大小将在3天内超过5MB', 70, '建议启用自动归档'),
            ('skill_expansion', '技能数量将在1周内达到12个', 80, '准备技能合并策略'),
            ('intelligence_growth', '智能评分将在1周内达到A级(90%)', 75, '继续当前进化策略'),
            ('bug_reduction', 'Bug 数量将下降50%', 65, '加强自动修复'),
        ]
        
        for i, (pred_type, text, conf, action) in enumerate(predictions):
            try:
                pred_id = self.db.add_prediction(pred_type, text, conf, action)
                # 标记第一个已实现
                if i == 0:
                    self.db.fulfill_prediction(pred_id)
            except:
                pass
    
    def _generate_intelligence_history(self):
        """生成智能评分历史"""
        base_score = 20
        for i in range(30):
            # 模拟逐渐提升
            improvement = random.randint(0, 2)
            base_score = min(25, base_score + improvement)
            
            dimensions = {
                '基础能力': min(5, 3 + i//10),
                '学习能力': min(5, 3 + i//10),
                '自主能力': min(5, 2 + i//15),
                '认知能力': min(5, 3 + i//10),
                '交互能力': min(5, 3 + i//10),
            }
            
            percentage = (base_score / 25) * 100
            grade = 'S+' if percentage >= 95 else 'S' if percentage >= 90 else 'A+' if percentage >= 85 else 'A'
            
            try:
                self.db.record_intelligence_score(
                    base_score, 25, percentage, grade, dimensions
                )
            except:
                pass
    
    def _generate_metrics(self):
        """生成指标数据"""
        # 成功率指标
        for i in range(24):
            timestamp = datetime.now() - timedelta(hours=i)
            success_rate = 85 + random.randint(-5, 10)
            
            try:
                self.db.record_metric(
                    'success_rate',
                    success_rate,
                    {'hour': timestamp.hour}
                )
            except:
                pass
        
        # 响应时间指标
        for i in range(24):
            timestamp = datetime.now() - timedelta(hours=i)
            response_time = 2.5 + random.uniform(-1, 1)
            
            try:
                self.db.record_metric(
                    'response_time',
                    response_time,
                    {'hour': timestamp.hour}
                )
            except:
                pass
    
    def update_realtime_data(self):
        """更新实时数据"""
        # 记录当前指标
        self.db.record_metric('active_instances', random.randint(1, 5))
        self.db.record_metric('success_rate', 87 + random.randint(-3, 5))
        self.db.record_metric('memory_usage', 2.5 + random.uniform(-0.5, 1))


if __name__ == '__main__':
    gen = DynamicDataGenerator()
    print("\n📊 当前统计:")
    stats = gen.db.get_stats()
    print(json.dumps(stats, indent=2))
