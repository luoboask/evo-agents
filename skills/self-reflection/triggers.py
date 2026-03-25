#!/usr/bin/env python3
"""
自我进化触发器 - Evolution Triggers
定义何时、如何触发自我进化
"""

import json
import os
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque


class EvolutionTriggers:
    """自我进化触发器系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.learning_dir = self.workspace / "memory" / "learning"
        self.triggers_file = self.learning_dir / "triggers.json"
        
        # 触发器配置
        self.config = self._load_config()
        
        # 触发历史
        self.trigger_history = deque(maxlen=100)
        
        # 运行状态
        self.running = False
        self.monitor_thread = None
    
    def _load_config(self):
        """加载触发器配置"""
        default_config = {
            "immediate_triggers": {
                "failure_rate_threshold": 0.3,  # 失败率超过30%触发
                "response_time_threshold": 30,   # 响应时间超过30秒触发
                "error_pattern_threshold": 3,    # 同一错误出现3次触发
            },
            "periodic_triggers": {
                "daily_reflection": "23:00",     # 每天23:00反思
                "weekly_review": "Sunday",       # 每周日复盘
                "monthly_evolution": 1,          # 每月1号进化
            },
            "threshold_triggers": {
                "memory_size_mb": 50,            # 记忆超过50MB触发归档
                "skill_count": 20,               # 技能超过20个触发合并
                "interaction_count": 100,        # 交互超过100次触发优化
            },
            "user_initiated": {
                "command": "evolve",             # 用户输入 evolve 触发
                "feedback_threshold": 0.5,       # 用户满意度低于0.5触发
            }
        }
        
        if self.triggers_file.exists():
            with open(self.triggers_file, 'r') as f:
                saved = json.load(f)
                default_config.update(saved)
        
        return default_config
    
    def _save_config(self):
        """保存配置"""
        with open(self.triggers_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    # ═══════════════════════════════════════════════════════════════
    # 触发器类型 1: 即时触发 (Immediate Triggers)
    # ═══════════════════════════════════════════════════════════════
    
    def check_immediate_triggers(self, context):
        """检查即时触发条件"""
        triggers = []
        
        # 1. 高失败率
        if context.get("failure_rate", 0) > self.config["immediate_triggers"]["failure_rate_threshold"]:
            triggers.append({
                "type": "immediate",
                "name": "high_failure_rate",
                "priority": "critical",
                "message": f"失败率 {context['failure_rate']*100:.0f}% 超过阈值",
                "action": "analyze_failures_and_fix"
            })
        
        # 2. 响应时间过长
        if context.get("response_time", 0) > self.config["immediate_triggers"]["response_time_threshold"]:
            triggers.append({
                "type": "immediate",
                "name": "slow_response",
                "priority": "high",
                "message": f"响应时间 {context['response_time']:.1f}s 超过阈值",
                "action": "optimize_performance"
            })
        
        # 3. 重复错误模式
        error_pattern = self._check_error_pattern(context.get("error_type"))
        if error_pattern["count"] >= self.config["immediate_triggers"]["error_pattern_threshold"]:
            triggers.append({
                "type": "immediate",
                "name": "repeated_error",
                "priority": "high",
                "message": f"错误 '{error_pattern['type']}' 重复出现 {error_pattern['count']} 次",
                "action": "fix_root_cause"
            })
        
        return triggers
    
    def _check_error_pattern(self, error_type):
        """检查错误模式"""
        if not error_type:
            return {"type": None, "count": 0}
        
        # 读取最近日志
        recent_logs = self._get_recent_logs(1)
        same_errors = [l for l in recent_logs if l.get("error_type") == error_type]
        
        return {"type": error_type, "count": len(same_errors)}
    
    # ═══════════════════════════════════════════════════════════════
    # 触发器类型 2: 周期性触发 (Periodic Triggers)
    # ═══════════════════════════════════════════════════════════════
    
    def check_periodic_triggers(self):
        """检查周期性触发条件"""
        triggers = []
        now = datetime.now()
        
        # 1. 每日反思
        daily_time = self.config["periodic_triggers"]["daily_reflection"]
        if now.strftime("%H:%M") == daily_time:
            triggers.append({
                "type": "periodic",
                "name": "daily_reflection",
                "priority": "medium",
                "message": "每日反思时间到了",
                "action": "daily_retrospective"
            })
        
        # 2. 每周复盘
        weekly_day = self.config["periodic_triggers"]["weekly_review"]
        if now.strftime("%A") == weekly_day and now.hour == 0:
            triggers.append({
                "type": "periodic",
                "name": "weekly_review",
                "priority": "medium",
                "message": "每周复盘时间到了",
                "action": "weekly_review"
            })
        
        # 3. 每月进化
        monthly_day = self.config["periodic_triggers"]["monthly_evolution"]
        if now.day == monthly_day and now.hour == 0:
            triggers.append({
                "type": "periodic",
                "name": "monthly_evolution",
                "priority": "high",
                "message": "每月进化时间到了",
                "action": "monthly_evolution_plan"
            })
        
        return triggers
    
    # ═══════════════════════════════════════════════════════════════
    # 触发器类型 3: 阈值触发 (Threshold Triggers)
    # ═══════════════════════════════════════════════════════════════
    
    def check_threshold_triggers(self):
        """检查阈值触发条件"""
        triggers = []
        
        # 1. 记忆大小
        memory_dir = self.workspace / "memory"
        total_size = sum(f.stat().st_size for f in memory_dir.rglob("*") if f.is_file())
        memory_mb = total_size / (1024 * 1024)
        
        if memory_mb > self.config["threshold_triggers"]["memory_size_mb"]:
            triggers.append({
                "type": "threshold",
                "name": "memory_overflow",
                "priority": "medium",
                "message": f"记忆大小 {memory_mb:.1f}MB 超过阈值",
                "action": "archive_old_memories"
            })
        
        # 2. 技能数量
        skills_dir = self.workspace / "skills"
        skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
        
        if skill_count > self.config["threshold_triggers"]["skill_count"]:
            triggers.append({
                "type": "threshold",
                "name": "too_many_skills",
                "priority": "low",
                "message": f"技能数量 {skill_count} 超过阈值",
                "action": "merge_similar_skills"
            })
        
        # 3. 交互次数
        today_logs = self._get_recent_logs(1)
        if len(today_logs) > self.config["threshold_triggers"]["interaction_count"]:
            triggers.append({
                "type": "threshold",
                "name": "high_interaction",
                "priority": "low",
                "message": f"今日交互 {len(today_logs)} 次，建议优化",
                "action": "optimize_common_workflows"
            })
        
        return triggers
    
    # ═
    # ═══════════════════════════════════════════════════════════════
    # 触发器类型 4: 用户触发 (User Initiated)
    # ═══════════════════════════════════════════════════════════════
    
    def check_user_trigger(self, user_input):
        """检查用户是否触发进化"""
        triggers = []
        
        # 1. 命令触发
        trigger_command = self.config["user_initiated"]["command"]
        if trigger_command.lower() in user_input.lower():
            triggers.append({
                "type": "user",
                "name": "user_command",
                "priority": "high",
                "message": "用户请求进化",
                "action": "full_evolution_check"
            })
        
        return triggers
    
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
    
    def execute_trigger(self, trigger):
        """执行触发器"""
        print(f"🚀 触发进化: {trigger['name']}")
        print(f"   原因: {trigger['message']}")
        print(f"   行动: {trigger['action']}")
        return True
    
    def check_all_triggers(self, context=None, user_input=None):
        """检查所有触发器"""
        all_triggers = []
        
        if context:
            all_triggers.extend(self.check_immediate_triggers(context))
        
        all_triggers.extend(self.check_periodic_triggers())
        all_triggers.extend(self.check_threshold_triggers())
        
        if user_input:
            all_triggers.extend(self.check_user_trigger(user_input))
        
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_triggers.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return all_triggers
    
    def print_trigger_report(self):
        """打印触发器报告"""
        print("\n" + "=" * 60)
        print("🎯 自我进化触发器系统")
        print("=" * 60)
        print()
        
        print("📋 触发器配置:")
        print("\n即时触发:")
        for key, value in self.config["immediate_triggers"].items():
            print(f"  - {key}: {value}")
        
        print("\n周期性触发:")
        for key, value in self.config["periodic_triggers"].items():
            print(f"  - {key}: {value}")
        
        print("\n阈值触发:")
        for key, value in self.config["threshold_triggers"].items():
            print(f"  - {key}: {value}")
        
        print("\n" + "-" * 60)
        print("🔍 当前触发检查:")
        triggers = self.check_all_triggers()
        
        if triggers:
            print(f"\n发现 {len(triggers)} 个触发器:")
            for t in triggers:
                emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                print(f"  {emoji.get(t['priority'], '⚪')} [{t['priority']}] {t['name']}: {t['message']}")
        else:
            print("\n✅ 暂无触发器激活")
        
        print()
        print("=" * 60)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='自我进化触发器')
    parser.add_argument('--check', action='store_true', help='检查所有触发器')
    parser.add_argument('--config', action='store_true', help='显示配置')
    parser.add_argument('--simulate', type=str, help='模拟触发 (failure/slow/error)')
    args = parser.parse_args()
    
    triggers = EvolutionTriggers()
    
    if args.config:
        print(json.dumps(triggers.config, indent=2))
    elif args.simulate:
        if args.simulate == "failure":
            context = {"failure_rate": 0.5}
            result = triggers.check_immediate_triggers(context)
            print(f"模拟高失败率 (50%):")
            for r in result:
                print(f"  - {r['name']}: {r['message']}")
    else:
        triggers.print_trigger_report()


if __name__ == '__main__':
    main()
