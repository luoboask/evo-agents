#!/usr/bin/env python3
"""
自纠错模块 - 从错误日志中学习
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class SelfCorrector:
    """自纠错机制（从错误中学习）"""
    
    def __init__(self, workspace_path: Path = None):
        self.workspace = workspace_path or Path.cwd()
        self.error_log = self.workspace / 'data' / 'error_log.jsonl'
        self.correction_log = self.workspace / 'data' / 'correction_log.jsonl'
    
    def log_error(self, error_type: str, error_message: str, context: Dict = None):
        """记录错误"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message,
            'context': context or {},
            'corrected': False
        }
        
        # 确保目录存在
        self.error_log.parent.mkdir(parents=True, exist_ok=True)
        
        # 追加到日志
        with open(self.error_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        print(f"📝 记录错误：{error_type} - {error_message[:50]}...")
    
    def analyze_errors(self, days: int = 7) -> List[Dict]:
        """
        分析最近 N 天的错误模式
        
        Args:
            days: 分析天数
            
        Returns:
            错误模式列表
        """
        cutoff = datetime.now() - timedelta(days=days)
        errors = []
        patterns = {}
        
        if not self.error_log.exists():
            return []
        
        # 读取错误日志
        with open(self.error_log, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    timestamp = datetime.fromisoformat(entry['timestamp'])
                    if timestamp >= cutoff and not entry.get('corrected', False):
                        errors.append(entry)
                        
                        # 统计错误类型
                        error_type = entry['type']
                        patterns[error_type] = patterns.get(error_type, 0) + 1
                except:
                    pass
        
        # 生成模式报告
        pattern_report = []
        for error_type, count in patterns.items():
            if count >= 2:  # 出现 2 次以上的错误类型
                pattern_report.append({
                    'type': error_type,
                    'count': count,
                    'suggestion': f"建议修复 {error_type} 类型错误（出现{count}次）"
                })
        
        return pattern_report
    
    def generate_correction(self, error_pattern: Dict) -> Dict:
        """
        生成纠错方案
        
        Args:
            error_pattern: 错误模式
            
        Returns:
            纠错方案
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_pattern['type'],
            'error_count': error_pattern['count'],
            'correction': f"针对 {error_pattern['type']} 错误的改进措施",
            'status': 'pending'
        }
    
    def apply_correction(self, correction: Dict, memory_system) -> bool:
        """
        应用纠错方案到记忆系统
        
        Args:
            correction: 纠错方案
            memory_system: 记忆系统实例
            
        Returns:
            是否成功应用
        """
        try:
            # 将纠错方案记录为学习
            memory_system.record_interaction(
                role='assistant',
                content=f"自纠错发现：{correction['error_type']}错误出现{correction['error_count']}次\n改进：{correction['correction']}",
                metadata={
                    'type': 'self_correction',
                    'error_type': correction['error_type'],
                    'correction': correction['correction']
                }
            )
            
            # 标记为已纠正
            self._mark_corrected(correction)
            
            print(f"✅ 应用纠错：{correction['error_type']}")
            return True
            
        except Exception as e:
            print(f"❌ 应用纠错失败：{e}")
            return False
    
    def _mark_corrected(self, correction: Dict):
        """标记错误为已纠正"""
        correction['status'] = 'corrected'
        correction['corrected_at'] = datetime.now().isoformat()
        
        # 记录到纠正日志
        self.correction_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.correction_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(correction, ensure_ascii=False) + '\n')
    
    def run_self_correction(self, memory_system, days: int = 7) -> int:
        """
        运行自纠错流程
        
        Args:
            memory_system: 记忆系统实例
            days: 分析天数
            
        Returns:
            应用的纠错数量
        """
        print(f"🔍 分析最近{days}天的错误...")
        
        # 分析错误模式
        patterns = self.analyze_errors(days)
        print(f"   发现 {len(patterns)} 个错误模式")
        
        # 生成并应用纠错
        count = 0
        for pattern in patterns:
            correction = self.generate_correction(pattern)
            if self.apply_correction(correction, memory_system):
                count += 1
        
        return count


if __name__ == '__main__':
    # 测试
    corrector = SelfCorrector()
    
    # 模拟错误日志
    corrector.log_error('import_error', 'ModuleNotFoundError: No module named xxx')
    corrector.log_error('import_error', 'ModuleNotFoundError: No module named yyy')
    corrector.log_error('syntax_error', 'SyntaxError: invalid syntax')
    
    print("\n分析错误模式:")
    patterns = corrector.analyze_errors(days=7)
    for p in patterns:
        print(f"  - {p['type']}: {p['count']}次 - {p['suggestion']}")
