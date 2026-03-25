#!/usr/bin/env python3
"""
自动进化执行器 - Auto Evolution Executor
定时自动检查并执行进化
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class Logger:
    """Simple logger that writes to both stdout and a log file"""
    def __init__(self, log_path):
        self.log_path = log_path
        self.terminal = sys.stdout
        
    def write(self, message):
        self.terminal.write(message)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(message)
        self.terminal.flush()
        
    def flush(self):
        self.terminal.flush()


def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=60, cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def auto_evolve():
    """自动进化主流程"""
    workspace = Path("/Users/dhr/.openclaw/workspace")
    log_path = workspace / "memory" / "learning" / "cron_evolution.log"
    
    # Set up logging to both stdout and file
    logger = Logger(log_path)
    sys.stdout = logger
    
    print()
    print("=" * 70)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Hourly Evolution Check")
    print("=" * 70)
    print()
    
    # 1. 系统健康检查
    print("📊 步骤 1: 系统健康检查...")
    success, stdout, stderr = run_command(
        "python3 skills/self-reflection/predictive_maintenance.py --check",
        cwd=workspace
    )
    
    health_issues = []
    if "HIGH" in stdout or "CRITICAL" in stdout:
        # 提取问题
        for line in stdout.split('\n'):
            if '🔴' in line or '🟠' in line:
                health_issues.append(line.strip())
        print(f"   ⚠️  发现 {len(health_issues)} 个高优先级问题")
    else:
        print("   ✅ 系统健康")
    
    # 2. 触发器检查
    print("\n🎯 步骤 2: 触发器检查...")
    success, stdout, stderr = run_command(
        "python3 skills/self-reflection/triggers.py --check",
        cwd=workspace
    )
    
    triggers = []
    if "触发器" in stdout:
        # 提取触发器
        for line in stdout.split('\n'):
            if '🔴' in line or '🟠' in line or '🟡' in line:
                triggers.append(line.strip())
        print(f"   ⚠️  发现 {len(triggers)} 个触发器")
    else:
        print("   ✅ 无触发器激活")
    
    # 3. 决定是否进化
    print("\n🧬 步骤 3: 进化决策...")
    should_evolve = len(health_issues) > 0 or len(triggers) > 0
    
    if not should_evolve:
        print("   ✅ 无需进化，系统运行良好")
        print()
        print("=" * 70)
        return
    
    print(f"   🚀 需要进化: {len(health_issues)} 个问题, {len(triggers)} 个触发器")
    
    # 4. 执行进化（简化版）
    print("\n🔧 步骤 4: 执行进化...")
    
    # 记录进化事件
    evolution_event = {
        "timestamp": datetime.now().isoformat(),
        "type": "auto_evolution",
        "triggered_by": {
            "health_issues": health_issues,
            "triggers": triggers
        },
        "actions": []
    }
    
    # 这里可以添加自动改进逻辑
    # 例如：如果发现网络问题，自动切换到 search_v3
    if any("网络" in issue or "web_search" in issue for issue in health_issues):
        print("   📝 建议: 使用 search_v3 替代 search_v2")
        evolution_event["actions"].append("recommend_search_v3")
    
    if any("memory" in issue.lower() for issue in health_issues):
        print("   📝 建议: 归档旧记忆文件")
        evolution_event["actions"].append("recommend_archive")
    
    # 保存进化事件
    learning_dir = workspace / "memory" / "learning"
    learning_dir.mkdir(parents=True, exist_ok=True)
    
    with open(learning_dir / "auto_evolution_events.jsonl", 'a') as f:
        f.write(json.dumps(evolution_event, ensure_ascii=False) + '\n')
    
    # 5. 生成报告
    print("\n📋 步骤 5: 生成报告...")
    print()
    print("=" * 70)
    print("🎉 自动进化完成!")
    print("=" * 70)
    print()
    print(f"发现问题: {len(health_issues)}")
    print(f"触发器: {len(triggers)}")
    print(f"建议行动: {len(evolution_event['actions'])}")
    print()
    
    if evolution_event["actions"]:
        print("建议行动:")
        for action in evolution_event["actions"]:
            print(f"  - {action}")
        print()
    
    print("💡 提示: 运行 'python3 skills/self-reflection/evolution_control.py'")
    print("         查看详细报告并手动实施改进")
    print("=" * 70)


if __name__ == '__main__':
    auto_evolve()
