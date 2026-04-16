#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evolution_events.py - 结构化进化事件记录

功能:
- 记录结构化的进化事件（jsonl 格式）
- 支持 blast_radius 评估
- 支持成功/失败追踪
- 提供查询和统计接口

格式:
{"run_id": "...", "intent": "repair", "signals": [...], "blast_radius": {...}, "outcome": {...}, "timestamp": "..."}

用法:
    from evolution_events import EvolutionEventRecorder
    
    recorder = EvolutionEventRecorder('main-agent')
    recorder.record(
        intent='repair',
        signals=['log_error', 'errsig:xxx'],
        blast_radius={'files': 1, 'lines': 2},
        outcome={'status': 'success', 'score': 0.85}
    )
"""

import json
import uuid
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter


class EvolutionEventRecorder:
    """进化事件记录器"""
    
    def __init__(self, agent_name: str, workspace_root: Path = None):
        self.agent_name = agent_name
        self.workspace_root = workspace_root or self._find_workspace()
        self.events_file = self.workspace_root / 'data' / agent_name / 'evolution_events.jsonl'
        
        # 确保目录存在
        self.events_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _find_workspace(self) -> Path:
        """查找 workspace 路径"""
        current = Path(__file__).parent
        for _ in range(5):
            if (current / '.install-config').exists():
                return current
            if (current / '.git').exists():
                return current
            current = current.parent
        
        home_workspace = Path.home() / '.openclaw' / f'workspace-{self.agent_name}'
        if home_workspace.exists():
            return home_workspace
        
        return Path.cwd()
    
    def _generate_run_id(self) -> str:
        """生成唯一的 run_id"""
        return f"run_{uuid.uuid4().hex[:12]}"
    
    def record(self, 
               intent: str, 
               signals: List[str], 
               blast_radius: Dict[str, int],
               outcome: Dict[str, any],
               genes_used: List[str] = None,
               meta: Dict[str, any] = None) -> str:
        """
        记录进化事件
        
        Args:
            intent: 意图 (repair/optimize/innovate)
            signals: 触发信号列表
            blast_radius: 变更范围 {'files': N, 'lines': N}
            outcome: 结果 {'status': 'success'/'failed', 'score': 0.0-1.0}
            genes_used: 使用的 Gene 模板（可选）
            meta: 元数据（可选）
        
        Returns:
            run_id: 事件 ID
        """
        run_id = self._generate_run_id()
        
        event = {
            'run_id': run_id,
            'intent': intent,
            'signals': signals,
            'blast_radius': blast_radius,
            'outcome': outcome,
            'genes_used': genes_used or [],
            'meta': meta or {},
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        # 追加到 jsonl 文件
        with open(self.events_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        return run_id
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """获取最近 N 个事件"""
        if not self.events_file.exists():
            return []
        
        events = []
        with open(self.events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except:
                        pass
        
        return events[-limit:]
    
    def analyze_signal_frequency(self, window: int = 8) -> Dict:
        """
        分析信号频率（用于去重）
        
        Returns:
            {
                'suppressed_signals': Set[str],  # 应抑制的信号（出现 3+ 次）
                'signal_freq': Dict[str, int],   # 信号频率统计
                'empty_cycle_count': int,        # 空转次数
                'empty_cycle_ratio': float,      # 空转比例
                'consecutive_failures': int,     # 连续失败次数
                'failure_ratio': float           # 失败比例
            }
        """
        recent = self.get_recent_events(window)
        if not recent:
            return {
                'suppressed_signals': set(),
                'signal_freq': {},
                'empty_cycle_count': 0,
                'empty_cycle_ratio': 0.0,
                'consecutive_failures': 0,
                'failure_ratio': 0.0
            }
        
        # 统计信号频率
        signal_freq = Counter()
        for evt in recent:
            for sig in evt.get('signals', []):
                # 归一化：去掉详情后缀
                key = sig.split(':')[0] if ':' in sig else sig
                signal_freq[key] += 1
        
        # 抑制高频信号（出现 3+ 次）
        suppressed = {sig for sig, count in signal_freq.items() if count >= 3}
        
        # 检测空转（blast_radius.files === 0）
        empty_cycles = sum(
            1 for evt in recent 
            if evt.get('blast_radius', {}).get('files', 0) == 0
        )
        
        # 检测连续失败（从尾部向前）
        consecutive_failures = 0
        for evt in reversed(recent):
            if evt.get('outcome', {}).get('status') == 'failed':
                consecutive_failures += 1
            else:
                break
        
        # 计算失败比例
        failure_count = sum(
            1 for evt in recent 
            if evt.get('outcome', {}).get('status') == 'failed'
        )
        
        return {
            'suppressed_signals': suppressed,
            'signal_freq': dict(signal_freq),
            'empty_cycle_count': empty_cycles,
            'empty_cycle_ratio': empty_cycles / len(recent) if recent else 0.0,
            'consecutive_failures': consecutive_failures,
            'failure_ratio': failure_count / len(recent) if recent else 0.0
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.events_file.exists():
            return {'total': 0}
        
        events = []
        with open(self.events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except:
                        pass
        
        if not events:
            return {'total': 0}
        
        # 按意图统计
        intent_counts = Counter(evt.get('intent', 'unknown') for evt in events)
        
        # 按结果统计
        outcome_counts = Counter(
            evt.get('outcome', {}).get('status', 'unknown') for evt in events
        )
        
        # 计算平均 blast_radius
        total_files = sum(evt.get('blast_radius', {}).get('files', 0) for evt in events)
        total_lines = sum(evt.get('blast_radius', {}).get('lines', 0) for evt in events)
        
        # 计算成功率
        success_count = outcome_counts.get('success', 0)
        success_rate = success_count / len(events) if events else 0.0
        
        return {
            'total': len(events),
            'by_intent': dict(intent_counts),
            'by_outcome': dict(outcome_counts),
            'avg_files': total_files / len(events),
            'avg_lines': total_lines / len(events),
            'success_rate': success_rate,
            'file_path': str(self.events_file)
        }


def main():
    """命令行工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description='进化事件记录工具')
    parser.add_argument('--agent', default='main-agent', help='Agent 名称')
    parser.add_argument('--workspace', type=Path, help='Workspace 路径')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--recent', type=int, nargs='?', const=10, help='显示最近 N 个事件')
    parser.add_argument('--analyze', action='store_true', help='分析信号频率')
    
    args = parser.parse_args()
    
    recorder = EvolutionEventRecorder(args.agent, args.workspace)
    
    if args.stats:
        stats = recorder.get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif args.recent:
        events = recorder.get_recent_events(args.recent)
        for evt in reversed(events):
            print(json.dumps(evt, indent=2, ensure_ascii=False))
            print('---')
    
    elif args.analyze:
        analysis = recorder.analyze_signal_frequency()
        # 转换 set 为 list 以便 JSON 序列化
        analysis['suppressed_signals'] = list(analysis['suppressed_signals'])
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
