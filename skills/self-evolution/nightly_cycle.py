#!/usr/bin/env python3
"""
夜间进化循环系统 - 参考 TinkerClaw
https://github.com/globalcaos/tinkerclaw

核心任务：
1. 🍷 Wind Down - 每日复盘，改进指令
2. 😴 Memory Consolidation - 记忆整合，49% 压缩
3. 🧹 Cleaning Lady - 上下文清理
4. 🔍 Auto-Evolution - 搜索可应用的改进
"""

import json
import sqlite3
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent))
from memory_stream import MemoryStream
from self_evolution_real import RealSelfEvolution


class NightlyEvolutionCycle:
    """夜间进化循环系统"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.parent.parent
        self.memory_dir = self.workspace / 'memory'
        self.learning_dir = self.memory_dir / 'learning'
        
        self.memory_stream = MemoryStream()
        self.evolution = RealSelfEvolution()
        
        # 配置
        self.config = {
            'memory_consolidation': {
                'compress_after_days': 7,      # 7 天后的记忆压缩
                'keep_high_importance': 7.0,   # 保留重要性 >= 7 的记忆
                'target_compression_rate': 0.49  # 49% 压缩率（参考 ENGRAM 论文）
            },
            'cleaning': {
                'max_learning_files': 30,      # 保留最近 30 天的学习文件
                'max_log_size_mb': 100,        # 日志文件最大 100MB
                'clean_temp_files': True       # 清理临时文件
            }
        }
    
    def run_full_cycle(self):
        """运行完整的夜间进化循环"""
        print("=" * 70)
        print("🌙 夜间进化循环")
        print(f"   开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        results = {}
        
        # 1. Wind Down - 每日复盘
        print("\n" + "=" * 70)
        print("🍷 Wind Down - 每日复盘")
        print("=" * 70)
        results['wind_down'] = self.wind_down()
        
        # 2. Memory Consolidation - 记忆整合
        print("\n" + "=" * 70)
        print("😴 Memory Consolidation - 记忆整合")
        print("=" * 70)
        results['memory_consolidation'] = self.memory_consolidation()
        
        # 3. Cleaning Lady - 上下文清理
        print("\n" + "=" * 70)
        print("🧹 Cleaning Lady - 上下文清理")
        print("=" * 70)
        results['cleaning'] = self.cleaning_lady()
        
        # 4. Auto-Evolution - 自动进化
        print("\n" + "=" * 70)
        print("🔍 Auto-Evolution - 自动进化")
        print("=" * 70)
        results['auto_evolution'] = self.auto_evolution()
        
        # 总结
        print("\n" + "=" * 70)
        print("📊 夜间循环总结")
        print("=" * 70)
        self._print_summary(results)
        
        # 记录进化事件
        self._record_cycle_completion(results)
        
        print("\n" + "=" * 70)
        print(f"✅ 夜间循环完成：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        return results
    
    def wind_down(self) -> Dict:
        """
        🍷 Wind Down - 每日复盘
        
        类似"一杯红酒配日记"，回顾一天的工作：
        - 什么做得好
        - 什么可以改进
        - 学到了什么
        - 明天要做什么
        """
        print("\n📝 回顾今日事件...")
        
        # 获取今天的进化事件
        today = datetime.now().strftime('%Y-%m-%d')
        events = self.evolution.get_evolution_history(limit=50)
        today_events = [
            e for e in events 
            if e['timestamp'].startswith(today)
        ]
        
        print(f"   今日事件：{len(today_events)}个")
        
        if not today_events:
            print("   ⚠️ 今日无进化事件，跳过复盘")
            return {'status': 'skipped', 'reason': 'no_events'}
        
        # 分析模式
        event_types = {}
        for event in today_events:
            etype = event['event_type']
            event_types[etype] = event_types.get(etype, 0) + 1
        
        print(f"   事件类型分布：{event_types}")
        
        # 生成复盘洞察
        insights = []
        
        # 找出最频繁的事件类型
        if event_types:
            top_type = max(event_types, key=event_types.get)
            insights.append(f"今日焦点：{top_type} ({event_types[top_type]}次)")
        
        # 检查是否有 Bug 修复
        if any('BUG' in et for et in event_types):
            insights.append("发现并修复了问题，这是良好的工程实践")
        
        # 检查是否有学习事件
        if any('KNOWLEDGE' in et or 'LEARNING' in et for et in event_types):
            insights.append("持续学习，保持知识更新")
        
        # 生成明日建议
        suggestions = []
        
        # 如果有很多 FEATURE_ADDED，建议测试和文档
        if event_types.get('FEATURE_ADDED', 0) >= 3:
            suggestions.append("新增功能较多，建议编写测试和文档")
        
        # 如果有很多 BUG_FIX，建议代码审查
        if event_types.get('BUG_FIX', 0) >= 2:
            suggestions.append("Bug 较多，建议进行代码审查或重构")
        
        # 生成复盘记忆
        review_content = f"今日复盘 ({today})：\n"
        review_content += f"- 完成 {len(today_events)} 个进化事件\n"
        review_content += f"- 主要焦点：{', '.join(event_types.keys())}\n"
        review_content += f"- 洞察：{'; '.join(insights)}\n"
        if suggestions:
            review_content += f"- 建议：{'; '.join(suggestions)}"
        
        # 添加到记忆流
        self.memory_stream.add_memory(
            content=review_content,
            memory_type='reflection',
            tags=['每日复盘', today],
            importance=7.0
        )
        
        print(f"   ✅ 生成复盘：{len(insights)}个洞察，{len(suggestions)}个建议")
        
        return {
            'status': 'completed',
            'events_reviewed': len(today_events),
            'insights': insights,
            'suggestions': suggestions
        }
    
    def memory_consolidation(self) -> Dict:
        """
        😴 Memory Consolidation - 记忆整合
        
        参考 ENGRAM 论文：
        - 将短期记忆转化为长期记忆
        - 压缩冗余信息
        - 保留高重要性记忆
        - 目标：49% 压缩率
        """
        print("\n📊 分析记忆状态...")
        
        stats = self.memory_stream.get_stats()
        total = stats.get('total', 0)
        print(f"   当前记忆总数：{total}")
        
        # 获取所有观察记忆
        all_observations = self.memory_stream.list_memories(limit=1000)
        # 过滤出 observation 类型
        all_observations = [m for m in all_observations if m.get('type') == 'observation']
        
        # 分类：保留 vs 压缩
        to_keep = []
        to_compress = []
        
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for mem in all_observations:
            mem_date = datetime.fromisoformat(mem.created_at)
            
            # 高重要性记忆：保留
            if mem.importance >= self.config['memory_consolidation']['keep_high_importance']:
                to_keep.append(mem)
            # 7 天内的记忆：保留
            elif mem_date >= cutoff_date:
                to_keep.append(mem)
            # 其他：标记为压缩
            else:
                to_compress.append(mem)
        
        print(f"   保留：{len(to_keep)}条")
        print(f"   待压缩：{len(to_compress)}条")
        
        # 执行压缩
        compressed_count = 0
        if to_compress:
            print(f"\n🗜️  执行压缩...")
            
            # 按领域分组压缩
            clusters = self.memory_stream._cluster_memories(to_compress)
            
            for topic, memories in clusters.items():
                if len(memories) >= 3:
                    # 生成压缩摘要
                    summary = f"压缩摘要 [{topic}]：{len(memories)}条记忆整合为 1 条\n"
                    summary += f"时间范围：{memories[-1].created_at[:10]} 至 {memories[0].created_at[:10]}\n"
                    summary += f"关键内容：\n"
                    
                    # 提取最重要的 3 条
                    top_memories = sorted(memories, key=lambda m: m.importance, reverse=True)[:3]
                    for i, mem in enumerate(top_memories, 1):
                        summary += f"  {i}. {mem.content[:80]} (重要性：{mem.importance})\n"
                    
                    # 添加压缩后的记忆
                    self.memory_stream.add_memory(
                        content=summary,
                        memory_type='observation',
                        tags=[topic, '压缩摘要'],
                        importance=6.0,
                        metadata={
                            'compressed_from': len(memories),
                            'compression_date': datetime.now().isoformat()
                        }
                    )
                    compressed_count += 1
            
            print(f"   生成 {compressed_count} 个压缩摘要")
        
        # 计算压缩率
        original_count = len(to_compress)
        new_count = compressed_count
        compression_rate = (original_count - new_count) / max(1, original_count)
        
        print(f"\n📈 压缩效果:")
        print(f"   原始：{original_count}条")
        print(f"   压缩后：{new_count}条")
        print(f"   压缩率：{compression_rate*100:.1f}% (目标：49%)")
        
        return {
            'status': 'completed',
            'original_count': original_count,
            'compressed_count': new_count,
            'compression_rate': compression_rate,
            'kept_count': len(to_keep)
        }
    
    def cleaning_lady(self) -> Dict:
        """
        🧹 Cleaning Lady - 上下文清理
        
        清理工作：
        - 删除过期的学习文件
        - 清理临时文件
        - 控制日志大小
        """
        print("\n🗑️  开始清理...")
        
        cleaned_files = []
        freed_space = 0
        
        # 1. 清理过期学习文件
        print("   清理过期学习文件...")
        learning_files = sorted(
            self.learning_dir.glob('scheduled_learning_*.jsonl'),
            reverse=True
        )
        
        # 保留最近 N 天
        max_files = self.config['cleaning']['max_learning_files']
        if len(learning_files) > max_files:
            for file in learning_files[max_files:]:
                size = file.stat().st_size
                try:
                    file.unlink()
                    cleaned_files.append(str(file))
                    freed_space += size
                except Exception as e:
                    print(f"   ⚠️ 删除失败：{file} - {e}")
        
        print(f"   清理 {len(learning_files) - max_files if len(learning_files) > max_files else 0} 个文件")
        
        # 2. 清理临时文件
        if self.config['cleaning']['clean_temp_files']:
            print("   清理临时文件...")
            temp_patterns = ['*.tmp', '*.bak', '*.pyc', '__pycache__']
            
            for pattern in temp_patterns:
                for file in self.workspace.rglob(pattern):
                    try:
                        if file.is_file():
                            size = file.stat().st_size
                            file.unlink()
                            cleaned_files.append(str(file))
                            freed_space += size
                        elif file.is_dir() and not any(file.iterdir()):
                            shutil.rmtree(file)
                            cleaned_files.append(str(file))
                    except Exception as e:
                        pass  # 静默失败
        
        # 3. 检查日志大小
        print("   检查日志文件大小...")
        log_files = list(self.workspace.rglob('*.log'))
        max_size = self.config['cleaning']['max_log_size_mb'] * 1024 * 1024
        
        for log_file in log_files:
            if log_file.stat().st_size > max_size:
                print(f"   ⚠️ 日志文件过大：{log_file} ({log_file.stat().st_size / 1024 / 1024:.1f}MB)")
                # 可以添加日志轮转逻辑
        
        freed_mb = freed_space / 1024 / 1024
        print(f"\n✅ 清理完成:")
        print(f"   清理文件：{len(cleaned_files)}个")
        print(f"   释放空间：{freed_mb:.2f}MB")
        
        return {
            'status': 'completed',
            'files_cleaned': len(cleaned_files),
            'space_freed_mb': freed_mb
        }
    
    def auto_evolution(self) -> Dict:
        """
        🔍 Auto-Evolution - 自动进化
        
        扫描系统状态，发现改进机会：
        - 重复出现的问题 → 需要系统性解决
        - 高频操作 → 可以自动化
        - 知识空白 → 需要学习
        """
        print("\n🔍 扫描改进机会...")
        
        improvements = []
        
        # 1. 分析进化事件模式
        events = self.evolution.get_evolution_history(limit=100)
        
        # 统计事件类型
        event_counts = {}
        for event in events:
            etype = event['event_type']
            event_counts[etype] = event_counts.get(etype, 0) + 1
        
        # 检测重复 Bug
        bug_events = [e for e in events if 'BUG' in e['event_type']]
        if len(bug_events) >= 3:
            improvements.append({
                'type': 'recurring_bug',
                'description': f'检测到 {len(bug_events)} 个 Bug 事件，建议系统性代码审查',
                'priority': 'high'
            })
        
        # 2. 分析记忆流
        memory_stats = self.memory_stream.get_stats()
        
        # 检查反思比例
        total = memory_stats.get('total', 1)
        by_type = memory_stats.get('by_type', {})
        reflection_count = by_type.get('reflection', 0) if isinstance(by_type.get('reflection'), int) else by_type.get('reflection', {}).get('count', 0)
        reflection_ratio = reflection_count / max(1, total)
        
        if reflection_ratio < 0.2:
            improvements.append({
                'type': 'low_reflection',
                'description': f'反思比例偏低 ({reflection_ratio:.1%})，建议增加反思生成频率',
                'priority': 'medium'
            })
        
        # 3. 检查学习目标
        all_memories = self.memory_stream.list_memories(limit=100)
        goals = [m for m in all_memories if m.get('type') == 'goal'][:10]
        completed_goals = [g for g in goals if '完成' in g.get('content', '')]
        
        if len(goals) > 5 and len(completed_goals) < 2:
            improvements.append({
                'type': 'goal_backlog',
                'description': '目标积压，建议优先完成现有目标而非添加新目标',
                'priority': 'medium'
            })
        
        # 4. 系统健康检查
        db_file = self.memory_dir / 'memory_stream.db'
        if db_file.exists():
            db_size_mb = db_file.stat().st_size / 1024 / 1024
            if db_size_mb > 50:
                improvements.append({
                    'type': 'database_growth',
                    'description': f'记忆数据库增长过快 ({db_size_mb:.1f}MB)，建议优化存储',
                    'priority': 'low'
                })
        
        print(f"   发现 {len(improvements)} 个改进机会:")
        for imp in improvements:
            print(f"   - [{imp['priority']}] {imp['description']}")
        
        # 生成进化建议记忆
        if improvements:
            improvement_text = "自动进化建议：\n"
            for imp in improvements:
                improvement_text += f"- [{imp['priority'].upper()}] {imp['description']}\n"
            
            self.memory_stream.add_memory(
                content=improvement_text,
                memory_type='goal',
                tags=['自动进化', '改进建议'],
                importance=7.0
            )
        
        return {
            'status': 'completed',
            'improvements_found': len(improvements),
            'improvements': improvements
        }
    
    def _print_summary(self, results: Dict):
        """打印循环总结"""
        print("\n📊 任务完成情况:")
        
        # Wind Down
        wd = results.get('wind_down', {})
        if wd.get('status') == 'completed':
            print(f"   🍷 Wind Down: ✅ ({wd.get('events_reviewed', 0)}个事件)")
        else:
            print(f"   🍷 Wind Down: ⚠️ {wd.get('reason', 'skipped')}")
        
        # Memory Consolidation
        mc = results.get('memory_consolidation', {})
        if mc.get('status') == 'completed':
            print(f"   😴 Memory Consolidation: ✅ (压缩率 {mc.get('compression_rate', 0)*100:.1f}%)")
        
        # Cleaning
        cl = results.get('cleaning', {})
        if cl.get('status') == 'completed':
            print(f"   🧹 Cleaning Lady: ✅ (清理 {cl.get('files_cleaned', 0)}个文件)")
        
        # Auto-Evolution
        ae = results.get('auto_evolution', {})
        if ae.get('status') == 'completed':
            print(f"   🔍 Auto-Evolution: ✅ ({ae.get('improvements_found', 0)}个改进机会)")
    
    def _record_cycle_completion(self, results: Dict):
        """记录循环完成事件"""
        total_improvements = results.get('auto_evolution', {}).get('improvements_found', 0)
        
        self.evolution.record_evolution(
            event_type='EVOLUTION_CHECK',
            description=f'夜间进化循环完成 - 发现{total_improvements}个改进机会',
            before='循环前状态',
            after=f'完成 4 个任务：Wind Down, Memory Consolidation, Cleaning, Auto-Evolution',
            lesson_learned='夜间循环是持续改进的关键机制，自动化复盘和清理保持系统健康',
            files_changed=['skills/self-evolution/nightly_cycle.py']
        )


# 使用示例
if __name__ == '__main__':
    cycle = NightlyEvolutionCycle()
    cycle.run_full_cycle()
