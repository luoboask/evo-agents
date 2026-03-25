#!/usr/bin/env python3
"""
动态智能进化工作台
从 SQLite 数据库读取实时数据
"""

import json
import os
import sys
from datetime import datetime
from database import EvolutionDatabase
from data_generator import DynamicDataGenerator


class DynamicDashboard:
    """动态智能进化工作台"""
    
    def __init__(self):
        self.db = EvolutionDatabase()
        self.data_gen = DynamicDataGenerator()
        self.width = 80
    
    def render(self):
        """渲染工作台"""
        # 更新实时数据
        self.data_gen.update_realtime_data()
        
        # 清屏
        if os.name != 'nt':
            os.system('clear')
        
        # 渲染各个部分
        self._render_header()
        self._render_intelligence()
        self._render_instances()
        self._render_bugs()
        self._render_predictions()
        self._render_events()
        self._render_metrics()
        self._render_footer()
    
    def _render_header(self):
        """渲染头部"""
        print("╔" + "═" * (self.width - 2) + "╗")
        print("║" + " " * 20 + "🧬 智能进化工作台 v3 (动态)" + " " * 29 + "║")
        print("╚" + "═" * (self.width - 2) + "╝")
        print()
    
    def _render_intelligence(self):
        """渲染智能评估"""
        print("🧠 智能评估（实时）")
        print("─" * self.width)
        
        # 获取最新智能评分
        latest = self.db.get_latest_intelligence()
        
        if latest:
            print(f"\n  综合评分: {latest['total']}/{latest['max']} ({latest['percentage']:.1f}%) [{latest['grade']}级]")
            print()
            
            # 显示各维度
            for dim_name, score in latest['dimensions'].items():
                bar = "█" * score + "░" * (5 - score)
                print(f"  {dim_name:<12} {bar} {score}/5")
        else:
            print("\n  暂无智能评分数据")
        
        print()
    
    def _render_instances(self):
        """渲染实例列表"""
        print("📦 沙箱实例（实时）")
        print("─" * self.width)
        
        instances = self.db.list_instances(limit=5)
        
        if instances:
            print(f"\n  共 {len(instances)} 个实例:\n")
            for inst in instances:
                status_icon = {
                    'RUNNING': '🟢',
                    'COMPLETED': '✅',
                    'CREATED': '⏳',
                    'ERROR': '❌'
                }.get(inst['status'], '⚪')
                
                print(f"  {status_icon} [{inst['status']}] {inst['id']}")
                print(f"     需求: {inst['requirement_id']}")
                print(f"     端口: {inst['port']}")
                
                if inst.get('results'):
                    passed = inst['results'].get('passed', 0)
                    total = passed + inst['results'].get('failed', 0)
                    print(f"     结果: {passed}/{total} 通过")
                print()
        else:
            print("\n  暂无实例")
        
        print()
    
    def _render_bugs(self):
        """渲染 Bug 列表"""
        print("🐛 Bug 追踪（实时）")
        print("─" * self.width)
        
        bugs = self.db.get_bugs(fixed=False, limit=5)
        
        if bugs:
            print(f"\n  未修复 Bug: {len(bugs)} 个\n")
            for bug in bugs:
                severity_icon = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(bug['severity'], '⚪')
                
                print(f"  {severity_icon} [{bug['severity']}] {bug['type']}")
                print(f"     {bug['description'][:60]}...")
                print(f"     实例: {bug['instance_id'] or 'N/A'}")
                print()
        else:
            print("\n  ✅ 暂无未修复 Bug")
        
        print()
    
    def _render_predictions(self):
        """渲染预测"""
        print("🔮 预测分析（实时）")
        print("─" * self.width)
        
        predictions = self.db.get_predictions(fulfilled=False, limit=5)
        
        if predictions:
            print(f"\n  待实现预测: {len(predictions)} 个\n")
            for pred in predictions:
                conf_bar = "█" * (pred['confidence'] // 10) + "░" * (10 - pred['confidence'] // 10)
                status = "✅ 已实现" if pred['fulfilled'] else "⏳ 进行中"
                
                print(f"  [{pred['type']}] {status}")
                print(f"     {pred['text']}")
                print(f"     置信度: {conf_bar} {pred['confidence']}%")
                print(f"     建议: {pred['action']}")
                print()
        else:
            print("\n  暂无预测")
        
        print()
    
    def _render_events(self):
        """渲染事件"""
        print("📜 最近事件（实时）")
        print("─" * self.width)
        
        events = self.db.get_recent_events(limit=8)
        
        if events:
            print()
            for event in events:
                time = event['timestamp'][11:19] if len(event['timestamp']) > 19 else event['timestamp']
                print(f"  [{time}] {event['type']}")
                print(f"     {event['description']}")
                if event['instance_id']:
                    print(f"     实例: {event['instance_id']}")
                print()
        else:
            print("\n  暂无事件")
        
        print()
    
    def _render_metrics(self):
        """渲染指标"""
        print("📊 实时指标")
        print("─" * self.width)
        
        # 获取统计数据
        stats = self.db.get_stats()
        
        print(f"\n  实例统计:")
        for status, count in stats.get('instances', {}).items():
            print(f"    - {status}: {count}")
        
        print(f"\n  Bug 统计:")
        for severity, count in stats.get('bugs', {}).items():
            print(f"    - {severity}: {count}")
        
        print(f"\n  待实现预测: {stats.get('pending_predictions', 0)}")
        print(f"  今日事件: {stats.get('today_events', 0)}")
        
        print()
    
    def _render_footer(self):
        """渲染底部"""
        print("─" * self.width)
        print(f"💡 数据来自 SQLite: {self.db.db_path}")
        print(f"🔄 最后更新: {datetime.now().strftime('%H:%M:%S')}")
        print(f"💻 运行: python3 dashboard_dynamic.py --watch 实时监控")
        print()


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='动态智能进化工作台')
    parser.add_argument('--watch', action='store_true', help='实时监控模式')
    parser.add_argument('--refresh', type=int, default=10, help='刷新间隔（秒）')
    args = parser.parse_args()
    
    dashboard = DynamicDashboard()
    
    if args.watch:
        try:
            while True:
                dashboard.render()
                import time
                time.sleep(args.refresh)
        except KeyboardInterrupt:
            print("\n👋 已退出")
    else:
        dashboard.render()


if __name__ == '__main__':
    main()
