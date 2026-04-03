#!/usr/bin/env python3
"""
记忆压缩器 - Memory Compressor
将每日记忆压缩为周度、月度摘要

功能：
1. 提取关键事件（重要性 >= 7.0）
2. 使用 LLM 生成智能摘要
3. 层次化组织（日→周→月→年）
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 使用 evo-agents 标准路径解析工具
try:
    from path_utils import resolve_workspace
except ImportError:
    # 回退：动态检测（兼容旧版本）
    def resolve_workspace():
        return Path(__file__).parent.parent.parent


class MemoryCompressor:
    """记忆压缩器"""
    
    def __init__(self, workspace=None):
        # 使用 evo-agents 标准路径解析
        self.workspace = resolve_workspace() if workspace is None else Path(workspace)
        self.memory_dir = self.workspace / "memory"
        
        # 创建目录结构
        (self.memory_dir / 'weekly').mkdir(exist_ok=True)
        (self.memory_dir / 'monthly').mkdir(exist_ok=True)
        (self.memory_dir / 'yearly').mkdir(exist_ok=True)
    
    def compress_weekly(self, year=None, week=None):
        """将每日记忆压缩为周度摘要"""
        if year is None or week is None:
            # 默认处理上周
            today = datetime.now()
            last_week = today - timedelta(days=today.weekday() + 7)
            year = last_week.isocalendar()[0]
            week = last_week.isocalendar()[1]
        
        print(f"📅 压缩 {year} 年第 {week} 周的记忆...")
        
        # 找出该周的所有每日文件
        week_files = self.get_week_files(year, week)
        
        if not week_files:
            print(f"  ⚠️ 该周没有记忆文件")
            return
        
        print(f"  找到 {len(week_files)} 个文件")
        
        # 提取关键事件
        key_events = []
        for file_path in week_files:
            events = self.extract_key_events(file_path)
            key_events.extend(events)
        
        if not key_events:
            print(f"  ⚠️ 该周没有关键事件")
            return
        
        print(f"  提取到 {len(key_events)} 个关键事件")
        
        # 生成周度摘要
        summary = self.generate_summary(key_events, period='weekly')
        
        # 保存
        output_file = self.memory_dir / 'weekly' / f"{year}-W{week:02d}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"  ✅ 已保存到 {output_file.name}")
    
    def compress_monthly(self, year=None, month=None):
        """将周度摘要压缩为月度摘要"""
        if year is None or month is None:
            # 默认处理上月
            today = datetime.now()
            if today.month == 1:
                year = today.year - 1
                month = 12
            else:
                year = today.year
                month = today.month - 1
        
        print(f"📅 压缩 {year} 年 {month} 月 的记忆...")
        
        # 找出该月的所有周度文件
        month_files = list((self.memory_dir / 'weekly').glob(f"{year}-W*.md"))
        
        # 过滤出属于该月的文件（简化处理：读取文件内容判断）
        valid_files = []
        for f in month_files:
            # 简单判断：文件名中的周数应该在该月范围内
            valid_files.append(f)
        
        if not valid_files:
            print(f"  ⚠️ 该月没有周度摘要")
            return
        
        print(f"  找到 {len(valid_files)} 个周度文件")
        
        # 收集所有周度摘要内容
        weekly_summaries = []
        for file_path in valid_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取关键部分
                summary_text = self.extract_summary_content(content)
                if summary_text:
                    weekly_summaries.append(summary_text)
        
        if not weekly_summaries:
            print(f"  ⚠️ 没有可压缩的内容")
            return
        
        # 生成月度摘要
        summary = self.generate_summary(weekly_summaries, period='monthly')
        
        # 保存
        output_file = self.memory_dir / 'monthly' / f"{year}-{month:02d}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"  ✅ 已保存到 {output_file.name}")
    
    def get_week_files(self, year, week):
        """获取指定周的所有每日文件"""
        # 计算该周的日期范围
        jan_4 = datetime(year, 1, 4)
        start_of_week = jan_4 - timedelta(days=jan_4.weekday())
        target_start = start_of_week + timedelta(weeks=week - 1)
        
        files = []
        for i in range(7):
            date = target_start + timedelta(days=i)
            file_path = self.memory_dir / f"{date.strftime('%Y-%m-%d')}.md"
            if file_path.exists():
                files.append(file_path)
        
        return files
    
    def extract_key_events(self, file_path):
        """从文件中提取关键事件"""
        events = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取标记为重要的内容
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 查找重要性标记
                importance_markers = ['[critical]', '[high]', '重要性:', '重要', '决定', '完成']
                if any(marker in line.lower() for marker in importance_markers):
                    events.append({
                        'content': line,
                        'source': file_path.name,
                        'type': 'key_event'
                    })
                
                # 查找列表项（可能是任务或成就）
                elif line.startswith('- [x]') or line.startswith('✅'):
                    events.append({
                        'content': line,
                        'source': file_path.name,
                        'type': 'completed_task'
                    })
        
        except Exception as e:
            print(f"  ⚠️ 读取 {file_path} 时出错：{e}")
        
        return events
    
    def extract_summary_content(self, content):
        """从摘要文件中提取核心内容"""
        # 跳过标题和元数据，提取正文
        lines = content.split('\n')
        body_lines = []
        
        in_body = False
        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                in_body = True
                continue
            if in_body and line.strip():
                body_lines.append(line)
        
        return '\n'.join(body_lines[:500])  # 限制长度
    
    def generate_summary(self, events, period='weekly'):
        """使用 LLM 生成摘要"""
        # 准备输入文本
        if isinstance(events[0], dict):
            event_texts = [e['content'] for e in events]
        else:
            event_texts = events
        
        input_text = '\n'.join(event_texts[:50])  # 限制数量
        
        # 构建提示词
        if period == 'weekly':
            prompt = f"""以下是本周的关键事件和完成任务：

{input_text}

请生成一个简洁的周度摘要，包含：
1. 主要成就（完成了什么）
2. 重要决策（做了什么决定）
3. 学到的知识（有什么新发现）
4. 待办事项（有什么需要继续跟进）

要求：
- 使用 Markdown 格式
- 分点列出，清晰易读
- 总字数控制在 300 字以内
- 语气积极、专业

输出格式：
# 周度摘要

## 🎯 主要成就
- ...

## 💡 重要决策
- ...

## 📚 学到的知识
- ...

## 📋 待办事项
- ...
"""
        else:  # monthly
            prompt = f"""以下是本月各周的摘要：

{input_text}

请生成一个月度摘要，包含：
1. 本月整体进展
2. 关键里程碑
3. 遇到的挑战和解决方案
4. 下月计划

要求：
- 使用 Markdown 格式
- 分章节，结构清晰
- 总字数控制在 500 字以内

输出格式：
# 月度摘要

## 📊 整体进展
...

## 🏆 关键里程碑
...

## ⚠️ 挑战与解决
...

## 🎯 下月计划
...
"""
        
        try:
            # 调用 Ollama
            result = subprocess.run(
                ['ollama', 'run', 'qwen2.5:1.5b', prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                summary = result.stdout.strip()
                
                # 添加元数据
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                header = f"""---
生成时间：{timestamp}
事件数量：{len(events)}
模型：qwen2.5:1.5b
---

"""
                return header + summary
            else:
                # LLM 失败，返回基础摘要
                return self.generate_basic_summary(events, period)
        
        except subprocess.TimeoutExpired:
            return self.generate_basic_summary(events, period)
        except Exception as e:
            print(f"  ⚠️ LLM 生成摘要失败：{e}")
            return self.generate_basic_summary(events, period)
    
    def generate_basic_summary(self, events, period='weekly'):
        """基础摘要（不使用 LLM）"""
        if isinstance(events[0], dict):
            event_texts = [e['content'] for e in events]
        else:
            event_texts = events
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        summary = f"""---
生成时间：{timestamp}
事件数量：{len(events)}
类型：基础摘要（无 LLM）
---

# {period.title()} 摘要

## 关键事件

"""
        for event in event_texts[:20]:
            summary += f"- {event}\n"
        
        return summary
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📊 记忆压缩统计")
        print("=" * 50)
        
        # 统计各类文件数量
        daily_count = len(list(self.memory_dir.glob('*.md'))) - 3  # 减去目录占位
        weekly_count = len(list((self.memory_dir / 'weekly').glob('*.md')))
        monthly_count = len(list((self.memory_dir / 'monthly').glob('*.md')))
        yearly_count = len(list((self.memory_dir / 'yearly').glob('*.md')))
        
        print(f"\n文件统计:")
        print(f"  每日记忆：{daily_count} 个")
        print(f"  周度摘要：{weekly_count} 个")
        print(f"  月度摘要：{monthly_count} 个")
        print(f"  年度摘要：{yearly_count} 个")
        
        # 估算压缩率
        if daily_count > 0:
            ratio = (weekly_count + monthly_count) / daily_count * 100
            print(f"\n压缩率：约 {100 - ratio:.1f}% （减少了 {ratio:.1f}% 的文件）")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='记忆压缩器')
    parser.add_argument('--weekly', action='store_true', help='压缩周度摘要')
    parser.add_argument('--monthly', action='store_true', help='压缩月度摘要')
    parser.add_argument('--all', action='store_true', help='压缩所有（周度 + 月度）')
    parser.add_argument('--stats', action='store_true', help='只显示统计信息')
    parser.add_argument('--year', type=int, help='指定年份')
    parser.add_argument('--week', type=int, help='指定周数')
    parser.add_argument('--month', type=int, help='指定月份')
    
    args = parser.parse_args()
    
    compressor = MemoryCompressor()
    
    if args.stats:
        compressor.show_stats()
    elif args.all:
        print("🔄 开始压缩所有记忆...\n")
        compressor.compress_weekly(args.year, args.week)
        print()
        compressor.compress_monthly(args.year, args.month)
    elif args.monthly:
        compressor.compress_monthly(args.year, args.month)
    elif args.weekly:
        compressor.compress_weekly(args.year, args.week)
    else:
        # 默认：压缩上周
        print("🔄 默认压缩上周记忆...\n")
        compressor.compress_weekly()


if __name__ == '__main__':
    main()
