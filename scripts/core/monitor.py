# -*- coding: utf-8 -*-
"""
系统监控器 - 统一日志格式，关键指标监控

功能:
- 统一日志格式
- 关键指标记录（成功率、复用率等）
- 性能监控
- 异常告警
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
# 使用统一路径解析工具
try:
    from path_utils import resolve_workspace
except ImportError:
    def resolve_workspace():
        return Path(__file__).parent.parent.parent


class SystemMonitor:
    """系统监控器"""
    
    def __init__(self, agent_name: str = "default"):
        self.workspace = resolve_workspace()
        self.data_path = self.workspace / "data" / agent_name
        self.logs_path = self.workspace / "logs"
        self.logs_path.mkdir(parents=True, exist_ok=True)
        
        # 日志文件（按日期分割）
        self.log_file = self.logs_path / f"monitor_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        
        # 指标缓存
        self.metrics_cache = {}
        self.cache_time = None
        self.cache_ttl = 300  # 5 分钟
        
        print(f"📊 系统监控器已初始化 (Agent: {agent_name})")
    
    def log(self, 
            event_type: str, 
            message: str, 
            level: str = "info",
            data: Dict = None):
        """
        记录日志
        
        Args:
            event_type: 事件类型
            message: 消息
            level: 日志级别 (info/warning/error)
            data: 附加数据
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'event_type': event_type,
            'message': message,
            'data': data or {}
        }
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def record_metric(self, name: str, value: float, tags: Dict = None):
        """
        记录指标
        
        Args:
            name: 指标名称
            value: 指标值
            tags: 标签
        """
        self.log(
            event_type='metric',
            message=f"{name}={value}",
            data={'name': name, 'value': value, 'tags': tags or {}}
        )
    
    def get_metrics(self) -> Dict:
        """获取当前指标"""
        # 检查缓存
        now = datetime.now()
        if self.cache_time and (now - self.cache_time).total_seconds() < self.cache_ttl:
            return self.metrics_cache
        
        metrics = {}
        
        # 1. 记忆统计
        memory_stats = self._get_memory_stats()
        metrics['memories'] = memory_stats
        
        # 2. 方案复用统计
        reuse_stats = self._get_reuse_stats()
        metrics['reuse'] = reuse_stats
        
        # 3. 质量评分统计
        quality_stats = self._get_quality_stats()
        metrics['quality'] = quality_stats
        
        # 4. 系统健康度
        health = self._get_health_status()
        metrics['health'] = health
        
        # 更新缓存
        self.metrics_cache = metrics
        self.cache_time = now
        
        return metrics
    
    def _get_memory_stats(self) -> Dict:
        """获取记忆统计"""
        memory_path = self.data_path / "memory"
        
        stats = {
            'total_files': 0,
            'total_size_kb': 0,
            'recent_days': 0
        }
        
        if memory_path.exists():
            files = list(memory_path.glob("*.md"))
            stats['total_files'] = len(files)
            
            # 计算总大小
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            stats['total_size_kb'] = round(total_size / 1024, 2)
            
            # 最近 7 天文件数
            week_ago = datetime.now() - timedelta(days=7)
            recent = [f for f in files if datetime.fromtimestamp(f.stat().st_mtime) > week_ago]
            stats['recent_days'] = len(recent)
        
        return stats
    
    def _get_reuse_stats(self) -> Dict:
        """获取方案复用统计"""
        evolution_db = self.data_path / "memory" / "evolution.db"
        
        stats = {
            'total_solutions': 0,
            'success_rate': 0.0,
            'reuse_rate': 0.0
        }
        
        if evolution_db.exists():
            conn = sqlite3.connect(evolution_db)
            cursor = conn.cursor()
            
            # 总方案数
            cursor.execute("SELECT COUNT(*) FROM solutions")
            stats['total_solutions'] = cursor.fetchone()[0]
            
            # 成功率
            cursor.execute("SELECT SUM(success_count), SUM(failure_count) FROM solutions")
            result = cursor.fetchone()
            success = result[0] or 0
            failure = result[1] or 0
            total = success + failure
            if total > 0:
                stats['success_rate'] = round(success / total, 3)
            
            conn.close()
        
        return stats
    
    def _get_quality_stats(self) -> Dict:
        """获取质量评分统计"""
        feedback_db = self.data_path / "memory" / "evolution_effects.db"
        
        stats = {
            'total_feedback': 0,
            'avg_rating': 0.0
        }
        
        if feedback_db.exists():
            conn = sqlite3.connect(feedback_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT AVG(rating), COUNT(*) FROM user_feedback")
            result = cursor.fetchone()
            stats['avg_rating'] = round(result[0] or 0, 2)
            stats['total_feedback'] = result[1] or 0
            
            conn.close()
        
        return stats
    
    def _get_health_status(self) -> Dict:
        """获取系统健康状态"""
        health = {
            'status': 'healthy',
            'issues': []
        }
        
        # 检查数据库文件
        db_files = [
            self.data_path / "memory" / "memory_stream.db",
            self.data_path / "memory" / "evolution.db",
        ]
        
        for db in db_files:
            if db.exists():
                size = db.stat().st_size
                if size > 100 * 1024 * 1024:  # 100MB
                    health['issues'].append(f"数据库过大：{db.name} ({size/1024/1024:.1f}MB)")
        
        # 检查日志文件
        if self.log_file.exists():
            size = self.log_file.stat().st_size
            if size > 50 * 1024 * 1024:  # 50MB
                health['issues'].append(f"日志文件过大：{self.log_file.name}")
        
        if health['issues']:
            health['status'] = 'warning'
        
        return health
    
    def generate_report(self) -> str:
        """生成监控报告"""
        metrics = self.get_metrics()
        
        report = []
        report.append("="*60)
        report.append("📊 系统监控报告")
        report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*60)
        
        # 记忆
        mem = metrics['memories']
        report.append(f"\n📝 记忆系统")
        report.append(f"   文件数：{mem['total_files']}")
        report.append(f"   总大小：{mem['total_size_kb']} KB")
        report.append(f"   最近 7 天：{mem['recent_days']} 个文件")
        
        # 复用
        reuse = metrics['reuse']
        report.append(f"\n🔄 方案复用")
        report.append(f"   总方案数：{reuse['total_solutions']}")
        report.append(f"   成功率：{reuse['success_rate']:.1%}")
        
        # 质量
        quality = metrics['quality']
        report.append(f"\n⭐ 质量评分")
        report.append(f"   总反馈数：{quality['total_feedback']}")
        report.append(f"   平均评分：{quality['avg_rating']:.2f}/5.0")
        
        # 健康
        health = metrics['health']
        report.append(f"\n💚 系统健康")
        report.append(f"   状态：{health['status']}")
        if health['issues']:
            for issue in health['issues']:
                report.append(f"   ⚠️  {issue}")
        
        report.append("\n" + "="*60)
        
        return "\n".join(report)
    
    def cleanup_old_logs(self, days: int = 30):
        """清理旧日志"""
        cutoff = datetime.now() - timedelta(days=days)
        
        for log_file in self.logs_path.glob("monitor_*.jsonl"):
            # 从文件名提取日期
            try:
                date_str = log_file.stem.replace('monitor_', '')
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                if file_date < cutoff:
                    log_file.unlink()
                    print(f"🗑️  已删除旧日志：{log_file.name}")
            except:
                pass


def main():
    """命令行使用"""
    import argparse
    
    parser = argparse.ArgumentParser(description='系统监控器')
    parser.add_argument('--agent', type=str, default='default', help='Agent 名称')
    parser.add_argument('--report', action='store_true', help='生成报告')
    parser.add_argument('--log', type=str, help='记录日志')
    parser.add_argument('--level', type=str, default='info', help='日志级别')
    parser.add_argument('--cleanup', type=int, help='清理 N 天前的日志')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(agent_name=args.agent)
    
    if args.report:
        print(monitor.generate_report())
        return
    
    if args.log:
        monitor.log(event_type='manual', message=args.log, level=args.level)
        print(f"✅ 日志已记录：{args.log}")
        return
    
    if args.cleanup:
        monitor.cleanup_old_logs(args.cleanup)
        return
    
    # 默认显示报告
    print(monitor.generate_report())


if __name__ == "__main__":
    main()
