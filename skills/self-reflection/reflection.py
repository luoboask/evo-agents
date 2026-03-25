#!/usr/bin/env python3
"""
自我反思模块 - Self-Reflection System
基于 SELF_EVOLUTION.md 的反思层实现
"""

import json
import os
from datetime import datetime
from pathlib import Path


class SelfReflection:
    """自我反思系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.learning_dir = self.workspace / "memory" / "learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)
    
    def log_interaction(self, task_type, tools_used, success, duration, notes=""):
        """记录每次交互的反思"""
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "task_type": task_type,
            "tools_used": tools_used,
            "success": success,
            "duration_seconds": duration,
            "notes": notes,
            "lessons": self._extract_lessons(task_type, tools_used, success, notes)
        }
        
        # 保存到日终反思文件
        today = datetime.now().strftime('%Y-%m-%d')
        reflection_file = self.learning_dir / f"reflections_{today}.jsonl"
        
        with open(reflection_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(reflection, ensure_ascii=False) + '\n')
        
        return reflection
    
    def _extract_lessons(self, task_type, tools_used, success, notes):
        """从交互中提取教训"""
        lessons = []
        
        if not success:
            lessons.append(f"失败类型: {task_type}")
            lessons.append("需要改进工具使用或任务理解")
        
        if "timeout" in notes.lower():
            lessons.append("超时问题: 考虑增加超时时间或优化方法")
        
        if "error" in notes.lower():
            lessons.append("错误处理: 需要更好的错误恢复机制")
        
        return lessons
    
    def daily_summary(self):
        """生成每日反思总结"""
        today = datetime.now().strftime('%Y-%m-%d')
        reflection_file = self.learning_dir / f"reflections_{today}.jsonl"
        
        if not reflection_file.exists():
            return None
        
        reflections = []
        with open(reflection_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    reflections.append(json.loads(line))
        
        # 统计分析
        total = len(reflections)
        successful = sum(1 for r in reflections if r['success'])
        failed = total - successful
        
        # 工具使用统计
        tool_usage = {}
        for r in reflections:
            for tool in r['tools_used']:
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        # 收集所有教训
        all_lessons = []
        for r in reflections:
            all_lessons.extend(r.get('lessons', []))
        
        summary = {
            "date": today,
            "total_interactions": total,
            "success_rate": f"{successful}/{total} ({successful/total*100:.1f}%)",
            "tool_usage": tool_usage,
            "key_lessons": list(set(all_lessons))[:10]  # 去重，最多10条
        }
        
        return summary
    
    def generate_improvement_suggestions(self):
        """基于反思生成改进建议"""
        summary = self.daily_summary()
        if not summary:
            return []
        
        suggestions = []
        
        # 基于成功率
        success_rate = summary['success_rate']
        if '100%' not in success_rate:
            suggestions.append("💡 建议: 回顾失败案例，添加预防性检查")
        
        # 基于工具使用
        tools = summary['tool_usage']
        if len(tools) < 3:
            suggestions.append("💡 建议: 尝试使用更多样化的工具组合")
        
        # 基于教训
        if summary['key_lessons']:
            suggestions.append("💡 建议: 针对常见错误创建自动化检查")
        
        return suggestions
    
    def print_daily_report(self):
        """打印每日反思报告"""
        summary = self.daily_summary()
        
        if not summary:
            print("今天还没有交互记录。")
            return
        
        print("=" * 60)
        print(f"📊 每日反思报告 - {summary['date']}")
        print("=" * 60)
        print()
        print(f"总交互次数: {summary['total_interactions']}")
        print(f"成功率: {summary['success_rate']}")
        print()
        print("工具使用情况:")
        for tool, count in sorted(summary['tool_usage'].items(), key=lambda x: -x[1]):
            print(f"  - {tool}: {count} 次")
        print()
        
        if summary['key_lessons']:
            print("关键教训:")
            for lesson in summary['key_lessons']:
                print(f"  ⚠️  {lesson}")
            print()
        
        suggestions = self.generate_improvement_suggestions()
        if suggestions:
            print("改进建议:")
            for s in suggestions:
                print(f"  {s}")
            print()
        
        print("=" * 60)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自我反思系统')
    parser.add_argument('--report', action='store_true', help='生成每日报告')
    parser.add_argument('--log', action='store_true', help='记录示例交互')
    
    args = parser.parse_args()
    
    reflection = SelfReflection()
    
    if args.report:
        reflection.print_daily_report()
    elif args.log:
        # 记录示例
        reflection.log_interaction(
            task_type="web_search",
            tools_used=["exec", "web_search"],
            success=True,
            duration=5.2,
            notes="成功搜索到 JVS Claw 信息"
        )
        print("✅ 已记录示例交互")
    else:
        reflection.print_daily_report()


if __name__ == '__main__':
    main()
