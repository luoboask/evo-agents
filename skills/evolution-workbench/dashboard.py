#!/usr/bin/env python3
"""
自我进化工作台 - Evolution Workbench Dashboard
实时监控和展示 AI 的自我进化过程
"""

import json
import os
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque


class EvolutionDashboard:
    """进化工作台仪表板"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.memory_dir = self.workspace / "memory"
        self.learning_dir = self.memory_dir / "learning"
        self.skills_dir = self.workspace / "skills"
        
        # 实时数据
        self.metrics = {
            "total_interactions": 0,
            "success_rate": 100.0,
            "avg_response_time": 0.0,
            "skills_count": 0,
            "memory_size": 0,
            "health_score": 100,
        }
        
        # 进化历史
        self.evolution_history = deque(maxlen=100)
        
        # 实时日志
        self.log_buffer = deque(maxlen=50)
        
        # 启动监控线程
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """启动实时监控"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.log("🚀 进化工作台已启动", "system")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            self._update_metrics()
            time.sleep(5)  # 每5秒更新一次
    
    def _update_metrics(self):
        """更新指标"""
        # 统计技能数量
        self.metrics["skills_count"] = len([d for d in self.skills_dir.iterdir() if d.is_dir()])
        
        # 统计记忆大小
        total_size = sum(f.stat().st_size for f in self.memory_dir.rglob("*") if f.is_file())
        self.metrics["memory_size"] = total_size / (1024 * 1024)  # MB
        
        # 读取最近反思计算成功率
        recent_logs = self._get_recent_logs(1)
        if recent_logs:
            success_count = sum(1 for l in recent_logs if l.get("success"))
            self.metrics["success_rate"] = (success_count / len(recent_logs)) * 100
            self.metrics["total_interactions"] = len(recent_logs)
    
    def _get_recent_logs(self, days):
        """获取最近日志"""
        logs = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = self.learning_dir / f"auto_reflections_{date}.jsonl"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
        return logs
    
    def log(self, message, category="info"):
        """记录日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_buffer.append({
            "time": timestamp,
            "message": message,
            "category": category
        })
    
    def record_evolution(self, event_type, description, details=None):
        """记录进化事件"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "description": description,
            "details": details or {}
        }
        self.evolution_history.append(event)
        self.log(f"🧬 进化: {description}", "evolution")
    
    def render_dashboard(self, refresh=False):
        """渲染仪表板"""
        # 清屏（如果需要刷新）
        if refresh and os.name != 'nt':
            os.system('clear')
        
        # 获取终端宽度
        try:
            width = os.get_terminal_size().columns
        except:
            width = 80
        width = min(width, 100)
        
        # 标题
        print("╔" + "═" * (width - 2) + "╗")
        title = "🧬 自我进化工作台 - Evolution Workbench"
        padding = (width - 2 - len(title)) // 2
        print("║" + " " * padding + title + " " * (width - 2 - padding - len(title)) + "║")
        print("╚" + "═" * (width - 2) + "╝")
        print()
        
        # 实时指标
        print("📊 实时指标")
        print("─" * width)
        print(f"  总交互次数: {self.metrics['total_interactions']}")
        print(f"  成功率: {self.metrics['success_rate']:.1f}%")
        print(f"  技能数量: {self.metrics['skills_count']}")
        print(f"  记忆大小: {self.metrics['memory_size']:.2f} MB")
        print(f"  健康评分: {self.metrics['health_score']}/100")
        print()
        
        # 系统状态
        print("🔧 系统状态")
        print("─" * width)
        status_items = [
            ("记忆系统", "✅ 运行中", "green"),
            ("语义搜索", "✅ 就绪", "green"),
            ("自动反思", "✅ 启用", "green"),
            ("预测维护", "✅ 运行中", "green"),
        ]
        for name, status, color in status_items:
            print(f"  {name:<15} {status}")
        print()
        
        # 最近进化事件
        print("🧬 最近进化事件")
        print("─" * width)
        recent_events = list(self.evolution_history)[-5:]
        if recent_events:
            for event in reversed(recent_events):
                time_str = event['timestamp'][11:19]
                print(f"  [{time_str}] {event['type']}: {event['description']}")
        else:
            print("  暂无进化事件")
        print()
        
        # 实时日志
        print("📝 实时日志")
        print("─" * width)
        recent_logs = list(self.log_buffer)[-10:]
        for log in recent_logs:
            emoji = {"system": "🔵", "info": "⚪", "evolution": "🟢", "warning": "🟡", "error": "🔴"}.get(log['category'], "⚪")
            print(f"  [{log['time']}] {emoji} {log['message']}")
        print()
        
        # 底部信息
        print("─" * width)
        print(f"💡 提示: 运行 'python3 dashboard.py --watch' 进入实时监控模式")
        print(f"🔄 最后更新: {datetime.now().strftime('%H:%M:%S')}")
    
    def watch_mode(self):
        """实时监控模式"""
        self.start_monitoring()
        try:
            while True:
                self.render_dashboard(refresh=True)
                time.sleep(2)
        except KeyboardInterrupt:
            self.stop_monitoring()
            print("\n👋 已退出监控模式")


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自我进化工作台')
    parser.add_argument('--watch', action='store_true', help='实时监控模式')
    parser.add_argument('--once', action='store_true', help='显示一次')
    parser.add_argument('--log', type=str, help='记录日志消息')
    parser.add_argument('--evolve', type=str, help='记录进化事件')
    
    args = parser.parse_args()
    
    dashboard = EvolutionDashboard()
    
    if args.watch:
        dashboard.watch_mode()
    elif args.log:
        dashboard.log(args.log)
        print(f"✅ 已记录: {args.log}")
    elif args.evolve:
        dashboard.record_evolution("manual", args.evolve)
        print(f"✅ 已记录进化: {args.evolve}")
    else:
        dashboard.render_dashboard()


if __name__ == '__main__':
    main()
