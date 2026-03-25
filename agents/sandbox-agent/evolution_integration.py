#!/usr/bin/env python3
"""
Sandbox Agent 自进化集成模块

将自进化系统 v5.0 的记忆和学习能力集成到 sandbox-agent 中
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 添加自进化系统路径
EVOLUTION_SYSTEM_PATH = Path(__file__).parent.parent / 'skills' / 'self-evolution-5.0'
sys.path.insert(0, str(EVOLUTION_SYSTEM_PATH))

from memory_stream import MemoryStream
from self_evolution_real import RealSelfEvolution


class SandboxEvolutionIntegration:
    """
    Sandbox Agent 自进化集成
    
    功能：
    1. 记录沙箱执行过程中的进化事件
    2. 从测试结果中学习
    3. 生成改进建议
    4. 记忆沙箱配置和经验
    """
    
    def __init__(self):
        self.memory_stream = MemoryStream()
        self.evolution = RealSelfEvolution()
        
        print(f"🧠 Sandbox 自进化集成已初始化")
        print(f"   记忆流：{self.memory_stream.db_path}")
        print(f"   进化记录：{self.evolution.evolution_db}")
    
    # ═══════════════════════════════════════════════════════════
    # 1. 记录沙箱事件
    # ═══════════════════════════════════════════════════════════
    
    def record_sandbox_event(self, event_type, instance_id, details):
        """
        记录沙箱事件
        
        Args:
            event_type: 事件类型
                - SANDBOX_CREATED: 沙箱创建
                - SANDBOX_STARTED: 沙箱启动
                - INTEGRATION_STARTED: 联调开始
                - INTEGRATION_COMPLETED: 联调完成
                - TEST_PASSED: 测试通过
                - TEST_FAILED: 测试失败
                - BUG_DETECTED: 检测到 Bug
                - BUG_FIXED: Bug 修复
                - PERFORMANCE_ISSUE: 性能问题
                - CONFIG_CHANGED: 配置变更
            
            instance_id: 沙箱实例 ID
            details: 详细信息
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'instance_id': instance_id,
            'details': details
        }
        
        # 记录到进化系统
        if event_type in ['TEST_FAILED', 'BUG_DETECTED']:
            # 失败和 Bug 记录为进化事件
            self.evolution.record_evolution(
                event_type='BUG_DETECTED' if 'BUG' in event_type else 'TEST_FAILED',
                description=f"沙箱 {instance_id}: {details.get('description', '检测到问题')}",
                lesson_learned=details.get('lesson', ''),
                files_changed=details.get('files', [])
            )
        
        # 记录到记忆流
        self.memory_stream.add_memory(
            content=self._format_memory_content(event),
            memory_type='observation',
            importance=self._calculate_importance(event_type, details),
            tags=[
                'sandbox',
                event_type,
                instance_id,
                details.get('requirement_id', 'unknown')
            ],
            metadata=event
        )
        
        print(f"📝 记录沙箱事件：{event_type}")
        print(f"   实例：{instance_id}")
        print(f"   描述：{details.get('description', 'N/A')[:50]}...")
    
    def _format_memory_content(self, event):
        """格式化记忆内容"""
        return (
            f"[沙箱事件] {event['type']}\n"
            f"实例：{event['instance_id']}\n"
            f"描述：{event['details'].get('description', 'N/A')}\n"
            f"时间：{event['timestamp']}"
        )
    
    def _calculate_importance(self, event_type, details):
        """计算事件重要性（1-10）"""
        importance_map = {
            'BUG_DETECTED': 9,
            'TEST_FAILED': 8,
            'INTEGRATION_COMPLETED': 7,
            'BUG_FIXED': 8,
            'PERFORMANCE_ISSUE': 7,
            'CONFIG_CHANGED': 5,
            'SANDBOX_CREATED': 4,
            'SANDBOX_STARTED': 3,
            'INTEGRATION_STARTED': 3,
            'TEST_PASSED': 5
        }
        
        base_importance = importance_map.get(event_type, 5)
        
        # 根据严重程度调整
        severity = details.get('severity', 'medium')
        if severity == 'critical':
            base_importance = min(10, base_importance + 2)
        elif severity == 'high':
            base_importance = min(10, base_importance + 1)
        
        return base_importance
    
    # ═══════════════════════════════════════════════════════════
    # 2. 从测试结果学习
    # ═══════════════════════════════════════════════════════════
    
    def learn_from_test_result(self, instance_id, test_result):
        """
        从测试结果学习
        
        Args:
            instance_id: 沙箱实例 ID
            test_result: 测试结果 {
                'test_case': {...},
                'frontend': {...},
                'backend': {...},
                'validation': {
                    'success': bool,
                    'bugs': [...],
                    'fixes': [...]
                }
            }
        """
        validation = test_result.get('validation', {})
        test_case = test_result.get('test_case', {})
        
        if validation.get('success'):
            # 测试通过 - 记录成功经验
            self.memory_stream.add_memory(
                content=f"[成功经验] 测试用例通过：{test_case.get('name', 'Unknown')}",
                memory_type='observation',
                importance=5,
                tags=['sandbox', 'test_passed', test_case.get('name', 'unknown')],
                metadata={
                    'instance_id': instance_id,
                    'test_case': test_case,
                    'success_factors': validation.get('success_factors', [])
                }
            )
        else:
            # 测试失败 - 记录失败原因和修复方案
            bugs = validation.get('bugs', [])
            fixes = validation.get('fixes', [])
            
            for bug in bugs:
                self.evolution.record_evolution(
                    event_type='BUG_DETECTED',
                    description=f"沙箱测试失败：{bug.get('description', '未知错误')}",
                    lesson_learned=bug.get('lesson', '需要添加边界检查'),
                    files_changed=bug.get('files', [])
                )
            
            for fix in fixes:
                self.memory_stream.add_memory(
                    content=f"[修复方案] {fix.get('description', '修复方案')}",
                    memory_type='reflection',
                    importance=8,
                    tags=['sandbox', 'bug_fix', fix.get('type', 'unknown')],
                    metadata={
                        'instance_id': instance_id,
                        'fix': fix,
                        'applicable_scenarios': fix.get('applicable_scenarios', [])
                    }
                )
        
        print(f"📚 从测试结果学习：{len(test_result.get('validation', {}).get('bugs', []))}个 Bug")
    
    def learn_from_integration_report(self, instance_id, report):
        """
        从联调报告学习
        
        Args:
            instance_id: 沙箱实例 ID
            report: 联调报告 {
                'instance_id': str,
                'requirement_id': str,
                'status': str,
                'summary': {
                    'total': int,
                    'passed': int,
                    'failed': int,
                    'duration': float
                },
                'results': [...]
            }
        """
        summary = report.get('summary', {})
        total = summary.get('total', 0)
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        
        pass_rate = passed / total if total > 0 else 0
        
        # 记录整体结果
        self.memory_stream.add_memory(
            content=f"[联调报告] {report.get('requirement_id', 'Unknown')}: "
                   f"通过率 {pass_rate:.1%} ({passed}/{total})",
            memory_type='observation',
            importance=7 if pass_rate < 0.8 else 5,
            tags=['sandbox', 'integration_report', report.get('requirement_id', 'unknown')],
            metadata=report
        )
        
        # 如果通过率低，生成反思
        if pass_rate < 0.8:
            self.memory_stream.add_memory(
                content=f"[反思] 联调通过率低 ({pass_rate:.1%})，需要改进测试策略或代码质量",
                memory_type='reflection',
                importance=8,
                tags=['sandbox', 'reflection', 'low_pass_rate'],
                metadata={
                    'pass_rate': pass_rate,
                    'suggestions': [
                        '增加单元测试覆盖',
                        '改进边界情况处理',
                        '添加更多错误处理'
                    ]
                }
            )
        
        # 从失败用例中学习
        results = report.get('results', [])
        for result in results:
            if not result.get('validation', {}).get('success'):
                self.learn_from_test_result(instance_id, result)
        
        print(f"📚 从联调报告学习：通过率 {pass_rate:.1%}")
    
    # ═══════════════════════════════════════════════════════════
    # 3. 提供智能建议
    # ═══════════════════════════════════════════════════════════
    
    def get_suggestions_for_requirement(self, requirement_id):
        """
        基于历史经验，为新需求提供建议
        
        Args:
            requirement_id: 需求 ID
        
        Returns:
            建议列表
        """
        # 检索相关的历史记忆
        related_memories = self.memory_stream.retrieve_by_relevance(
            requirement_id,
            limit=10
        )
        
        suggestions = []
        
        # 分析历史经验
        for memory, score in related_memories:
            if memory.memory_type == 'reflection':
                suggestions.append({
                    'type': 'reflection',
                    'content': memory.content,
                    'confidence': score,
                    'source': memory.created_at
                })
        
        # 检索相关的进化事件
        events = self.evolution.get_evolution_history(limit=20)
        for event in events:
            if requirement_id in event.get('description', ''):
                suggestions.append({
                    'type': 'evolution_event',
                    'content': event.get('lesson_learned', ''),
                    'confidence': 0.8,
                    'source': event.get('timestamp', '')
                })
        
        # 按置信度排序
        suggestions.sort(key=lambda x: -x['confidence'])
        
        return suggestions[:5]  # 返回前 5 个建议
    
    def get_common_bugs_for_requirement_type(self, requirement_type):
        """
        获取某类需求的常见 Bug
        
        Args:
            requirement_type: 需求类型，如 "登录", "购物车", "API"
        
        Returns:
            常见 Bug 列表
        """
        # 检索相关记忆
        related_memories = self.memory_stream.retrieve_by_relevance(
            requirement_type,
            limit=20
        )
        
        common_bugs = []
        for memory, score in related_memories:
            if 'bug' in memory.content.lower() or '失败' in memory.content:
                common_bugs.append({
                    'description': memory.content,
                    'importance': memory.importance,
                    'confidence': score
                })
        
        # 按重要性排序
        common_bugs.sort(key=lambda x: -x['importance'])
        
        return common_bugs[:10]
    
    def suggest_test_cases(self, requirement_desc, historical_results):
        """
        基于历史结果建议测试用例
        
        Args:
            requirement_desc: 需求描述
            historical_results: 历史测试结果
        
        Returns:
            测试用例建议列表
        """
        suggestions = []
        
        # 分析历史失败用例
        failed_tests = [r for r in historical_results if not r.get('validation', {}).get('success')]
        
        if failed_tests:
            # 从失败用例中提取模式
            suggestions.append({
                'type': 'regression_test',
                'description': '添加回归测试，覆盖历史失败用例',
                'priority': 'high',
                'reason': f'发现 {len(failed_tests)} 个历史失败用例'
            })
        
        # 基于需求类型建议
        if '登录' in requirement_desc or 'auth' in requirement_desc.lower():
            suggestions.extend([
                {
                    'type': 'security_test',
                    'description': 'SQL 注入测试',
                    'priority': 'high'
                },
                {
                    'type': 'security_test',
                    'description': '暴力破解测试',
                    'priority': 'high'
                },
                {
                    'type': 'boundary_test',
                    'description': '空密码测试',
                    'priority': 'medium'
                }
            ])
        
        if 'API' in requirement_desc:
            suggestions.extend([
                {
                    'type': 'api_test',
                    'description': '参数验证测试',
                    'priority': 'high'
                },
                {
                    'type': 'api_test',
                    'description': '错误处理测试',
                    'priority': 'medium'
                }
            ])
        
        return suggestions
    
    # ═══════════════════════════════════════════════════════════
    # 4. 沙箱配置优化
    # ═══════════════════════════════════════════════════════════
    
    def optimize_sandbox_config(self, instance_id, current_config, performance_data):
        """
        基于性能数据优化沙箱配置
        
        Args:
            instance_id: 沙箱实例 ID
            current_config: 当前配置
            performance_data: 性能数据 {
                'response_time': float,
                'memory_usage': float,
                'cpu_usage': float,
                'error_rate': float
            }
        
        Returns:
            优化建议
        """
        suggestions = []
        
        # 分析性能数据
        if performance_data.get('response_time', 0) > 1000:  # > 1s
            suggestions.append({
                'type': 'performance',
                'issue': '响应时间过长',
                'suggestion': '考虑添加缓存或优化数据库查询',
                'priority': 'high'
            })
        
        if performance_data.get('memory_usage', 0) > 80:  # > 80%
            suggestions.append({
                'type': 'resource',
                'issue': '内存使用过高',
                'suggestion': '检查内存泄漏或增加资源限制',
                'priority': 'high'
            })
        
        if performance_data.get('error_rate', 0) > 5:  # > 5%
            suggestions.append({
                'type': 'reliability',
                'issue': '错误率过高',
                'suggestion': '添加错误处理和重试机制',
                'priority': 'critical'
            })
        
        # 记录优化建议到记忆
        for suggestion in suggestions:
            self.memory_stream.add_memory(
                content=f"[配置优化] {suggestion['issue']}: {suggestion['suggestion']}",
                memory_type='reflection',
                importance=8 if suggestion['priority'] == 'critical' else 6,
                tags=['sandbox', 'optimization', suggestion['type']],
                metadata={
                    'instance_id': instance_id,
                    'suggestion': suggestion,
                    'performance_data': performance_data
                }
            )
        
        return suggestions
    
    # ═══════════════════════════════════════════════════════════
    # 5. 统计和报告
    # ═══════════════════════════════════════════════════════════
    
    def get_evolution_stats(self):
        """获取进化统计"""
        return {
            'memory_stream': self.memory_stream.get_stats(),
            'evolution_events': self.evolution.get_summary()
        }
    
    def generate_learning_report(self, days=7):
        """
        生成学习报告
        
        Args:
            days: 天数
        
        Returns:
            学习报告
        """
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        
        # 获取记忆统计
        memory_stats = self.memory_stream.get_stats()
        
        # 获取进化事件
        evolution_summary = self.evolution.get_summary()
        
        report = {
            'period': f'过去 {days} 天',
            'memory': {
                'total': memory_stats['total_memories'],
                'recent_24h': memory_stats['recent_24h'],
                'by_type': memory_stats['by_type']
            },
            'evolution': evolution_summary,
            'insights': []
        }
        
        # 生成洞察
        if memory_stats['by_type'].get('reflection', {}).get('count', 0) > 10:
            report['insights'].append('反思活跃，系统正在积极学习')
        
        if evolution_summary['by_type'].get('BUG_DETECTED', 0) > 5:
            report['insights'].append('Bug 检测频繁，建议进行代码审查')
        
        return report


# ═══════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 70)
    print("🧠 Sandbox Agent 自进化集成 - 演示")
    print("=" * 70)
    
    # 创建集成实例
    integration = SandboxEvolutionIntegration()
    
    # 1. 记录沙箱事件
    print("\n1. 记录沙箱事件")
    integration.record_sandbox_event(
        event_type='SANDBOX_CREATED',
        instance_id='sandbox-REQ-001-abc123',
        details={
            'requirement_id': 'REQ-001',
            'description': '创建用户登录沙箱',
            'config': {'port': 8080}
        }
    )
    
    # 2. 记录 Bug
    print("\n2. 记录 Bug")
    integration.record_sandbox_event(
        event_type='BUG_DETECTED',
        instance_id='sandbox-REQ-001-abc123',
        details={
            'requirement_id': 'REQ-001',
            'description': 'SQL 注入漏洞',
            'severity': 'critical',
            'lesson': '所有 SQL 查询必须使用参数化'
        }
    )
    
    # 3. 从测试结果学习
    print("\n3. 从测试结果学习")
    test_result = {
        'test_case': {'name': '登录测试'},
        'validation': {
            'success': False,
            'bugs': [
                {
                    'description': '空密码未处理',
                    'lesson': '需要添加输入验证'
                }
            ],
            'fixes': [
                {
                    'description': '添加密码长度检查',
                    'type': 'input_validation'
                }
            ]
        }
    }
    integration.learn_from_test_result('sandbox-REQ-001-abc123', test_result)
    
    # 4. 获取建议
    print("\n4. 获取建议")
    suggestions = integration.get_suggestions_for_requirement('REQ-001')
    print(f"   找到 {len(suggestions)} 条建议")
    for i, s in enumerate(suggestions[:3], 1):
        print(f"   {i}. {s['content'][:50]}...")
    
    # 5. 生成报告
    print("\n5. 生成学习报告")
    report = integration.generate_learning_report(days=7)
    print(f"   时期：{report['period']}")
    print(f"   记忆总数：{report['memory']['total']}")
    print(f"   进化事件：{report['evolution']['total_events']}")
    print(f"   洞察：{report['insights']}")
    
    print("\n" + "=" * 70)
    print("✅ 演示完成")
    print("=" * 70)
