#!/usr/bin/env python3
"""
自动反思系统 - Auto Reflection
在每次工具调用后自动记录和反思
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path


class AutoReflection:
    """自动反思钩子"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.learning_dir = self.workspace / "memory" / "learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 性能基准
        self.baselines = self._load_baselines()
    
    def _load_baselines(self):
        """加载性能基准"""
        baseline_file = self.learning_dir / "performance_baselines.json"
        if baseline_file.exists():
            with open(baseline_file, 'r') as f:
                return json.load(f)
        return {
            "exec": {"avg_time": 5.0, "success_rate": 0.95},
            "web_search": {"avg_time": 10.0, "success_rate": 0.90},
            "memory_search": {"avg_time": 2.0, "success_rate": 0.98},
        }
    
    def _save_baselines(self):
        """保存性能基准"""
        baseline_file = self.learning_dir / "performance_baselines.json"
        with open(baseline_file, 'w') as f:
            json.dump(self.baselines, f, indent=2)
    
    def log_tool_call(self, tool_name, args, result, duration, success, error=None):
        """
        自动记录每次工具调用
        
        Args:
            tool_name: 工具名称
            args: 调用参数（会脱敏）
            result: 结果摘要
            duration: 执行时间
            success: 是否成功
            error: 错误信息
        """
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "duration": duration,
            "success": success,
            "result_size": len(str(result)) if result else 0,
        }
        
        if error:
            reflection["error_type"] = type(error).__name__ if error else None
            reflection["error_msg"] = str(error)[:200] if error else None
        
        # 性能分析
        baseline = self.baselines.get(tool_name, {})
        if baseline:
            avg_time = baseline.get("avg_time", 10.0)
            if duration > avg_time * 2:
                reflection["performance_issue"] = f"耗时 {duration:.1f}s，超过基准 {avg_time:.1f}s 的 2 倍"
            elif duration < avg_time * 0.5:
                reflection["performance_optimization"] = f"耗时 {duration:.1f}s，比基准快 50%"
        
        # 成功率趋势
        if not success:
            reflection["lesson"] = f"{tool_name} 调用失败，需要检查原因"
        
        # 保存到日志
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.learning_dir / f"auto_reflections_{today}.jsonl"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(reflection, ensure_ascii=False) + '\n')
        
        # 实时输出反思（如果是交互模式）
        if self._is_interactive():
            self._print_reflection(reflection)
        
        return reflection
    
    def _is_interactive(self):
        """检查是否在交互模式"""
        return sys.stdin.isatty() if hasattr(sys.stdin, 'isatty') else False
    
    def _print_reflection(self, reflection):
        """打印实时反思"""
        tool = reflection["tool"]
        duration = reflection["duration"]
        success = reflection["success"]
        
        status = "✅" if success else "❌"
        print(f"\n🤖 [{status}] {tool} ({duration:.1f}s)", file=sys.stderr)
        
        if "performance_issue" in reflection:
            print(f"   ⚠️  {reflection['performance_issue']}", file=sys.stderr)
        elif "performance_optimization" in reflection:
            print(f"   🚀 {reflection['performance_optimization']}", file=sys.stderr)
        
        if "lesson" in reflection:
            print(f"   💡 {reflection['lesson']}", file=sys.stderr)
    
    def analyze_patterns(self, days=7):
        """分析使用模式，生成改进建议"""
        # 读取最近几天的日志
        all_reflections = []
        for i in range(days):
            date = (datetime.now() - __import__('datetime').timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = self.learning_dir / f"auto_reflections_{date}.jsonl"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            all_reflections.append(json.loads(line))
        
        if not all_reflections:
            return []
        
        # 统计分析
        tool_stats = {}
        for r in all_reflections:
            tool = r["tool"]
            if tool not in tool_stats:
                tool_stats[tool] = {"total": 0, "success": 0, "total_time": 0}
            tool_stats[tool]["total"] += 1
            if r["success"]:
                tool_stats[tool]["success"] += 1
            tool_stats[tool]["total_time"] += r["duration"]
        
        # 生成建议
        suggestions = []
        for tool, stats in tool_stats.items():
            success_rate = stats["success"] / stats["total"]
            avg_time = stats["total_time"] / stats["total"]
            
            # 成功率低
            if success_rate < 0.8:
                suggestions.append({
                    "priority": "high",
                    "tool": tool,
                    "issue": f"成功率仅 {success_rate*100:.0f}%",
                    "suggestion": f"需要改进 {tool} 的稳定性，考虑添加重试或备选方案"
                })
            
            # 性能下降
            baseline = self.baselines.get(tool, {})
            if baseline and avg_time > baseline.get("avg_time", avg_time) * 1.5:
                suggestions.append({
                    "priority": "medium",
                    "tool": tool,
                    "issue": f"平均耗时 {avg_time:.1f}s，比基准慢",
                    "suggestion": f"优化 {tool} 的性能，检查是否有阻塞操作"
                })
        
        return suggestions
    
    def print_improvement_report(self):
        """打印改进建议报告"""
        suggestions = self.analyze_patterns()
        
        if not suggestions:
            print("📊 暂无改进建议，系统运行良好！")
            return
        
        print("\n" + "=" * 60)
        print("🔧 自动改进建议报告")
        print("=" * 60)
        print()
        
        # 按优先级排序
        high_priority = [s for s in suggestions if s["priority"] == "high"]
        medium_priority = [s for s in suggestions if s["priority"] == "medium"]
        
        if high_priority:
            print(f"⚠️  高优先级 ({len(high_priority)} 项):")
            for s in high_priority:
                print(f"   [{s['tool']}] {s['issue']}")
                print(f"   → {s['suggestion']}")
                print()
        
        if medium_priority:
            print(f"💡 中优先级 ({len(medium_priority)} 项):")
            for s in medium_priority:
                print(f"   [{s['tool']}] {s['issue']}")
                print(f"   → {s['suggestion']}")
                print()
        
        print("=" * 60)


# 装饰器模式：包装工具调用
def with_reflection(tool_func, tool_name):
    """包装工具调用，自动记录反思"""
    def wrapper(*args, **kwargs):
        start = time.time()
        success = True
        error = None
        result = None
        
        try:
            result = tool_func(*args, **kwargs)
        except Exception as e:
            success = False
            error = e
            raise
        finally:
            duration = time.time() - start
            # 创建反思记录
            reflector = AutoReflection()
            reflector.log_tool_call(
                tool_name=tool_name,
                args=str(args)[:100],
                result=str(result)[:100] if result else None,
                duration=duration,
                success=success,
                error=error
            )
        
        return result
    
    return wrapper


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动反思系统')
    parser.add_argument('--report', action='store_true', help='生成改进建议报告')
    parser.add_argument('--demo', action='store_true', help='运行演示')
    
    args = parser.parse_args()
    
    reflector = AutoReflection()
    
    if args.report:
        reflector.print_improvement_report()
    elif args.demo:
        print("🎮 运行演示：模拟工具调用并自动记录反思")
        print()
        
        # 模拟成功调用
        reflector.log_tool_call(
            tool_name="web_search",
            args="{'query': 'OpenClaw'}",
            result="3 results found",
            duration=8.5,
            success=True
        )
        
        # 模拟失败调用
        reflector.log_tool_call(
            tool_name="web_search",
            args="{'query': 'test'}",
            result=None,
            duration=25.3,
            success=False,
            error=Exception("Timeout")
        )
        
        # 模拟慢调用
        reflector.log_tool_call(
            tool_name="exec",
            args="{'command': 'sleep 10'}",
            result="done",
            duration=15.2,
            success=True
        )
        
        print("\n✅ 演示完成，已记录到反思日志")
        print("📊 生成改进建议报告...")
        reflector.print_improvement_report()
    else:
        reflector.print_improvement_report()


if __name__ == '__main__':
    main()
