# -*- coding: utf-8 -*-
"""
Cron 任务优化器 - 条件执行，有事才做

功能:
- 检查是否有新内容需要处理
- 跳过无变化的任务
- 记录执行决策
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
# 使用统一路径解析工具
try:
    from path_utils import resolve_workspace
except ImportError:
    def resolve_workspace():
        return Path(__file__).parent.parent.parent


class CronOptimizer:
    """Cron 任务优化器"""
    
    def __init__(self, agent_name: str = "default"):
        self.workspace = resolve_workspace()
        self.data_path = self.workspace / "data" / agent_name
        self.memory_path = self.data_path / "memory"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # 状态文件
        self.state_file = self.memory_path / ".cron_optimizer_state.json"
        self.state = self._load_state()
        
        print(f"⚡ Cron 优化器已初始化 (Agent: {agent_name})")
    
    def _load_state(self) -> Dict:
        """加载状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_state(self):
        """保存状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def should_run_daily_review(self) -> bool:
        """
        检查是否应该执行每日回顾
        
        条件：今日记忆文件不存在或为空
        """
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = self.memory_path / f"{today}.md"
        
        if not today_file.exists():
            return True
        
        # 检查文件是否为空或只有标题
        content = today_file.read_text(encoding='utf-8').strip()
        if len(content) < 50:  # 只有标题
            return True
        
        return False
    
    def should_run_nightly_evolution(self) -> bool:
        """
        检查是否应该执行夜间进化
        
        条件：今天有新进化事件或新记忆
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 检查进化事件
        evolution_db = self.data_path / "memory" / "evolution.db"
        if evolution_db.exists():
            conn = sqlite3.connect(evolution_db)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM evolution_events WHERE timestamp LIKE ?",
                (f"{today}%",)
            )
            count = cursor.fetchone()[0]
            conn.close()
            
            if count > 0:
                return True
        
        # 检查今日记忆
        today_file = self.memory_path / f"{today}.md"
        if today_file.exists():
            content = today_file.read_text(encoding='utf-8').strip()
            if len(content) > 100:  # 有实质内容
                return True
        
        return False
    
    def should_run_session_consolidation(self) -> bool:
        """
        检查是否应该执行会话记忆整合
        
        条件：有待整合的会话记忆
        """
        memory_stream_db = self.memory_path / "memory_stream.db"
        if not memory_stream_db.exists():
            return False
        
        conn = sqlite3.connect(memory_stream_db)
        cursor = conn.cursor()
        
        # 检查超过 24 小时的会话记忆
        cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute(
            "SELECT COUNT(*) FROM session_memories WHERE created_at < ? AND importance >= 6.0",
            (cutoff,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def should_run_weekly_compress(self) -> bool:
        """
        检查是否应该执行周压缩
        
        条件：本周有新记忆
        """
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
        
        # 检查本周记忆文件
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            memory_file = self.memory_path / f"{date}.md"
            if memory_file.exists():
                content = memory_file.read_text(encoding='utf-8').strip()
                if len(content) > 100:
                    return True
        
        return False
    
    def record_execution(self, task_name: str, executed: bool, reason: str):
        """记录执行决策"""
        if 'executions' not in self.state:
            self.state['executions'] = []
        
        self.state['executions'].append({
            'task': task_name,
            'executed': executed,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        
        # 保留最近 100 条记录
        self.state['executions'] = self.state['executions'][-100:]
        self._save_state()
    
    def get_stats(self) -> Dict:
        """获取统计"""
        executions = self.state.get('executions', [])
        
        stats = {
            'total_checks': len(executions),
            'executed': sum(1 for e in executions if e['executed']),
            'skipped': sum(1 for e in executions if not e['executed']),
            'recent': executions[-10:] if executions else []
        }
        
        return stats


def main():
    """命令行使用"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cron 任务优化器')
    parser.add_argument('--agent', type=str, default='default', help='Agent 名称')
    parser.add_argument('--check', type=str, help='检查特定任务')
    parser.add_argument('--stats', action='store_true', help='显示统计')
    
    args = parser.parse_args()
    
    optimizer = CronOptimizer(agent_name=args.agent)
    
    if args.stats:
        stats = optimizer.get_stats()
        print(f"\n📊 Cron 优化统计")
        print(f"总检查次数：{stats['total_checks']}")
        print(f"执行次数：{stats['executed']}")
        print(f"跳过次数：{stats['skipped']}")
        print(f"跳过率：{stats['skipped']/max(1,stats['total_checks'])*100:.1f}%")
        return
    
    if args.check:
        if args.check == 'daily_review':
            should = optimizer.should_run_daily_review()
        elif args.check == 'nightly_evolution':
            should = optimizer.should_run_nightly_evolution()
        elif args.check == 'session_consolidation':
            should = optimizer.should_run_session_consolidation()
        elif args.check == 'weekly_compress':
            should = optimizer.should_run_weekly_compress()
        else:
            print(f"未知任务：{args.check}")
            return
        
        print(f"任务：{args.check}")
        print(f"应该执行：{should}")
        return
    
    # 检查所有任务
    print("\n📋 Cron 任务检查结果")
    print("="*50)
    
    tasks = {
        'daily_review': optimizer.should_run_daily_review(),
        'nightly_evolution': optimizer.should_run_nightly_evolution(),
        'session_consolidation': optimizer.should_run_session_consolidation(),
        'weekly_compress': optimizer.should_run_weekly_compress(),
    }
    
    for task, should in tasks.items():
        status = "✅ 执行" if should else "⏭️  跳过"
        print(f"  {task}: {status}")


if __name__ == "__main__":
    main()
