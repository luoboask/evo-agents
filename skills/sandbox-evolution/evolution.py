#!/usr/bin/env python3
"""
Sandbox Evolution - 沙箱自进化核心模块
"""

from memory_stream import MemoryStream
from self_evolution_real import RealSelfEvolution


class SandboxEvolution:
    """
    沙箱自进化（独立数据库，数据隔离）
    
    功能：
    1. 记录沙箱事件
    2. 从测试结果学习
    3. 提供智能建议
    4. 优化沙箱配置
    
    数据隔离：
    - sandbox-agent 使用独立数据库
    - 不与 main-agent 共享数据
    - 沙箱清理时可一起删除
    """
    
    def __init__(self, agent_id: str = 'sandbox'):
        # 使用独立数据库（数据隔离）
        self.memory_stream = MemoryStream(agent_id=agent_id)
        self.evolution = RealSelfEvolution(agent_id=agent_id)
        self.agent_id = agent_id
        
        print(f"🧠 Sandbox Evolution 已初始化（Agent: {agent_id}）")
        print(f"   记忆流：{self.memory_stream.db_path}")
        print(f"   进化库：{self.evolution.evolution_db}")
        print(f"   ✅ 数据隔离：已启用")
    
    def record_sandbox_event(self, event_type, instance_id, details):
        """记录沙箱事件"""
        # 记录到进化系统
        if event_type in ['TEST_FAILED', 'BUG_DETECTED']:
            self.evolution.record_evolution(
                event_type=event_type,
                description=f"沙箱 {instance_id}: {details.get('description', '检测到问题')}",
                lesson_learned=details.get('lesson', ''),
                files_changed=details.get('files', [])
            )
        
        # 记录到记忆流
        self.memory_stream.add_memory(
            content=f"[沙箱事件] {event_type} - 实例：{instance_id}",
            memory_type='observation',
            importance=self._calculate_importance(event_type, details),
            tags=['sandbox', event_type, instance_id],
            metadata={
                'event_type': event_type,
                'instance_id': instance_id,
                'details': details
            }
        )
        
        return {
            'success': True,
            'event_type': event_type,
            'instance_id': instance_id
        }
    
    def learn_from_test_result(self, instance_id, test_result, report):
        """从测试结果学习"""
        validation = test_result.get('validation', {})
        
        if not validation.get('success'):
            # 测试失败 - 记录 Bug
            bugs = validation.get('bugs', [])
            for bug in bugs:
                self.evolution.record_evolution(
                    event_type='BUG_DETECTED',
                    description=f"沙箱测试失败：{bug.get('description', '未知错误')}",
                    lesson_learned=bug.get('lesson', '需要改进'),
                    files_changed=bug.get('files', [])
                )
        
        # 从联调报告学习
        if report:
            summary = report.get('summary', {})
            pass_rate = summary.get('passed', 0) / max(1, summary.get('total', 1))
            
            if pass_rate < 0.8:
                self.memory_stream.add_memory(
                    content=f"[反思] 联调通过率低 ({pass_rate:.1%})，需要改进",
                    memory_type='reflection',
                    importance=8,
                    tags=['sandbox', 'reflection', 'low_pass_rate'],
                    metadata={'pass_rate': pass_rate}
                )
        
        return {
            'success': True,
            'learned': True
        }
    
    def get_suggestions_for_requirement(self, requirement_id):
        """获取智能建议"""
        # 检索相关记忆
        related_memories = self.memory_stream.retrieve_by_relevance(
            requirement_id,
            limit=10
        )
        
        suggestions = []
        for memory, score in related_memories:
            if memory.memory_type == 'reflection':
                suggestions.append({
                    'content': memory.content,
                    'confidence': score,
                    'source': memory.created_at
                })
        
        # 检索进化事件
        events = self.evolution.get_evolution_history(limit=20)
        for event in events:
            if requirement_id in event.get('description', ''):
                suggestions.append({
                    'content': event.get('lesson_learned', ''),
                    'confidence': 0.8,
                    'source': event.get('timestamp', '')
                })
        
        # 按置信度排序
        suggestions.sort(key=lambda x: -x['confidence'])
        
        return suggestions[:5]
    
    def get_common_bugs_for_requirement_type(self, requirement_type):
        """获取常见 Bug"""
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
        
        common_bugs.sort(key=lambda x: -x['importance'])
        
        return common_bugs[:10]
    
    def optimize_sandbox_config(self, instance_id, current_config, performance_data):
        """优化沙箱配置"""
        suggestions = []
        
        if performance_data.get('response_time', 0) > 1000:
            suggestions.append({
                'type': 'performance',
                'issue': '响应时间过长',
                'suggestion': '考虑添加缓存或优化数据库查询',
                'priority': 'high'
            })
        
        if performance_data.get('memory_usage', 0) > 80:
            suggestions.append({
                'type': 'resource',
                'issue': '内存使用过高',
                'suggestion': '检查内存泄漏或增加资源',
                'priority': 'high'
            })
        
        if performance_data.get('error_rate', 0) > 5:
            suggestions.append({
                'type': 'reliability',
                'issue': '错误率过高',
                'suggestion': '添加错误处理和重试机制',
                'priority': 'critical'
            })
        
        return {
            'success': True,
            'suggestions': suggestions
        }
    
    def get_evolution_stats(self):
        """获取进化统计"""
        return {
            'memory_stream': self.memory_stream.get_stats(),
            'evolution_events': self.evolution.get_summary()
        }
    
    def generate_learning_report(self, days=7):
        """生成学习报告"""
        from datetime import timedelta
        from datetime import datetime
        
        cutoff = datetime.now() - timedelta(days=days)
        memory_stats = self.memory_stream.get_stats()
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
        
        if memory_stats['by_type'].get('reflection', {}).get('count', 0) > 10:
            report['insights'].append('反思活跃，系统正在积极学习')
        
        if evolution_summary['by_type'].get('BUG_DETECTED', 0) > 5:
            report['insights'].append('Bug 检测频繁，建议进行代码审查')
        
        return report
    
    def _calculate_importance(self, event_type, details):
        """计算事件重要性"""
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
        
        severity = details.get('severity', 'medium')
        if severity == 'critical':
            base_importance = min(10, base_importance + 2)
        elif severity == 'high':
            base_importance = min(10, base_importance + 1)
        
        return base_importance
