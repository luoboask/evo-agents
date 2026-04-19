#!/usr/bin/env python3
"""
元学习器 - 学习如何学习

核心功能:
- 分析学习效率
- 优化学习过程
- 识别知识空白
- 主动学习建议
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class MetaLearning:
    """元学习器"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Path(__file__).parent / 'evolution_effects.db'
    
    def analyze_learning_efficiency(self, days: int = 30) -> Dict:
        """分析学习效率"""
        cutoff = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 按 Gene 分析效率
        cursor.execute('''
            SELECT 
                s.gene_used,
                AVG(u.success) as avg_success,
                COUNT(*) as usage_count
            FROM usage_records u
            JOIN solutions s ON u.solution_id = s.id
            WHERE u.timestamp > ?
            GROUP BY s.gene_used
        ''', (cutoff.isoformat(),))
        
        gene_efficiency = [
            {
                'gene_id': row[0],
                'avg_success': row[1],
                'usage_count': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        # 按问题类型分析效率
        cursor.execute('''
            SELECT 
                s.problem_type,
                AVG(u.success) as avg_success,
                COUNT(*) as usage_count
            FROM usage_records u
            JOIN solutions s ON u.solution_id = s.id
            WHERE u.timestamp > ?
            GROUP BY s.problem_type
            HAVING COUNT(*) >= 3
        ''', (cutoff.isoformat(),))
        
        problem_efficiency = [
            {
                'problem_type': row[0],
                'avg_success': row[1],
                'usage_count': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        # 找出最优模式
        best_gene = max(gene_efficiency, key=lambda x: x['avg_success']) if gene_efficiency else None
        worst_gene = min(gene_efficiency, key=lambda x: x['avg_success']) if gene_efficiency else None
        
        return {
            'gene_efficiency': gene_efficiency,
            'problem_efficiency': problem_efficiency,
            'best_gene': best_gene,
            'worst_gene': worst_gene,
            'overall_success_rate': sum(g['avg_success'] * g['usage_count'] for g in gene_efficiency) / 
                                   sum(g['usage_count'] for g in gene_efficiency) if gene_efficiency else 0.5
        }
    
    def optimize_learning_process(self) -> List[str]:
        """优化学习过程本身"""
        efficiency = self.analyze_learning_efficiency()
        suggestions = []
        
        # 检查最佳实践
        if efficiency['best_gene']:
            suggestions.append(
                f"✅ 最佳 Gene: {efficiency['best_gene']['gene_id']} " +
                f"(成功率 {efficiency['best_gene']['avg_success']:.1%})\n" +
                f"   建议：优先使用此 Gene"
            )
        
        if efficiency['worst_gene']:
            suggestions.append(
                f"⚠️  最差 Gene: {efficiency['worst_gene']['gene_id']} " +
                f"(成功率 {efficiency['worst_gene']['avg_success']:.1%})\n" +
                f"   建议：优化或淘汰此 Gene"
            )
        
        # 检查问题类型
        low_performers = [
            p for p in efficiency['problem_efficiency'] 
            if p['avg_success'] < 0.5 and p['usage_count'] >= 3
        ]
        
        if low_performers:
            suggestions.append("\n⚠️  以下问题类型成功率低:")
            for p in low_performers:
                suggestions.append(
                    f"  - {p['problem_type']}: {p['avg_success']:.1%} " +
                    f"({p['usage_count']} 次)"
                )
            suggestions.append("   建议：加强这些领域的学习")
        
        return suggestions
    
    def identify_knowledge_gaps(self) -> List[Dict]:
        """识别知识空白"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 找出失败集中的问题类型
        cursor.execute('''
            SELECT 
                s.problem_type,
                SUM(CASE WHEN u.success THEN 0 ELSE 1 END) as failure_count,
                COUNT(*) as total_count
            FROM usage_records u
            JOIN solutions s ON u.solution_id = s.id
            GROUP BY s.problem_type
            HAVING failure_count >= 3
            AND failure_count * 1.0 / COUNT(*) >= 0.5
        ''')
        
        gaps = [
            {
                'problem_type': row[0],
                'failure_count': row[1],
                'total_count': row[2],
                'failure_rate': row[1] / row[2]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        # 按失败率排序
        gaps.sort(key=lambda x: x['failure_rate'], reverse=True)
        
        return gaps
    
    def suggest_learning(self, gaps: List[Dict]) -> List[str]:
        """建议学习方向"""
        suggestions = []
        
        if not gaps:
            suggestions.append("✅ 没有明显的知识空白")
            return suggestions
        
        suggestions.append("⚠️  以下领域知识不足，建议加强学习:")
        
        for gap in gaps[:5]:  # 只显示前 5 个
            suggestions.append(
                f"  - {gap['problem_type']}: " +
                f"失败率 {gap['failure_rate']:.1%} " +
                f"({gap['failure_count']}/{gap['total_count']} 次)"
            )
        
        suggestions.append("\n建议行动:")
        suggestions.append("  1. 针对性学习这些领域")
        suggestions.append("  2. 收集更多相关案例")
        suggestions.append("  3. 请教领域专家")
        
        return suggestions
    
    def know_what_i_dont_know(self) -> str:
        """知道自己不知道什么 (苏格拉底式智慧)"""
        gaps = self.identify_knowledge_gaps()
        suggestions = self.suggest_learning(gaps)
        
        report = "🧠 元认知报告:\n\n"
        report += "\n".join(suggestions)
        
        return report
    
    def generate_meta_report(self, days: int = 30) -> str:
        """生成元学习报告"""
        efficiency = self.analyze_learning_efficiency(days)
        optimization = self.optimize_learning_process()
        gaps = self.identify_knowledge_gaps()
        
        report = f"""
# 元学习报告 (过去 {days} 天)

## 整体表现
- 总体成功率：{efficiency['overall_success_rate']:.1%}
- 使用 Gene 数：{len(efficiency['gene_efficiency'])}
- 问题类型数：{len(efficiency['problem_efficiency'])}

## 最佳实践
"""
        
        if efficiency['best_gene']:
            report += f"""
- 最佳 Gene: {efficiency['best_gene']['gene_id']}
  - 成功率：{efficiency['best_gene']['avg_success']:.1%}
  - 使用次数：{efficiency['best_gene']['usage_count']}
"""
        
        report += "\n## 优化建议\n"
        report += "\n".join(optimization)
        
        report += "\n\n## 知识空白\n"
        if gaps:
            for gap in gaps[:5]:
                report += f"""
- {gap['problem_type']}: 
  - 失败率：{gap['failure_rate']:.1%}
  - 失败次数：{gap['failure_count']}
"""
        else:
            report += "无明显知识空白\n"
        
        return report


# 定期生成报告 (Cron: 每月)
if __name__ == '__main__':
    meta = MetaLearning()
    
    print("🧠 元认知报告:")
    print(meta.know_what_i_dont_know())
    
    print("\n\n📊 完整报告:")
    print(meta.generate_meta_report(days=30))
