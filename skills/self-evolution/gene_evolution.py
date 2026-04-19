#!/usr/bin/env python3
"""
基因进化器 - 自动优化 Gene 模板

核心功能:
- 计算 Gene 成功率
- 分析失败原因
- 生成优化建议
- 从成功模式创建新 Gene
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class GeneEvolution:
    """Gene 模板进化器"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Path(__file__).parent / 'evolution_effects.db'
        self.genes_path = Path(__file__).parent / 'genes.json'
    
    def calculate_gene_success_rate(self, gene_id: str, days: int = 30) -> float:
        """计算 Gene 成功率"""
        cutoff = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                COUNT(*) as total
            FROM usage_records
            WHERE timestamp > ?
            AND solution_id IN (
                SELECT id FROM solutions WHERE gene_used = ?
            )
        ''', (cutoff.isoformat(), gene_id))
        
        row = cursor.fetchone()
        conn.close()
        
        successes = row[0] or 0
        total = row[1] or 0
        
        return successes / total if total > 0 else 0.5
    
    def analyze_gene_performance(self, gene_id: str) -> Dict:
        """分析 Gene 表现"""
        success_rate = self.calculate_gene_success_rate(gene_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取失败案例
        cursor.execute('''
            SELECT s.problem_type, s.problem_description, u.context
            FROM usage_records u
            JOIN solutions s ON u.solution_id = s.id
            WHERE u.success = 0
            AND s.gene_used = ?
            ORDER BY u.timestamp DESC
            LIMIT 5
        ''', (gene_id,))
        
        failures = [
            {'problem_type': row[0], 'description': row[1][:200], 'context': row[2]}
            for row in cursor.fetchall()
        ]
        
        # 获取成功案例
        cursor.execute('''
            SELECT s.problem_type, s.problem_description, u.context
            FROM usage_records u
            JOIN solutions s ON u.solution_id = s.id
            WHERE u.success = 1
            AND s.gene_used = ?
            ORDER BY u.timestamp DESC
            LIMIT 5
        ''', (gene_id,))
        
        successes = [
            {'problem_type': row[0], 'description': row[1][:200], 'context': row[2]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            'gene_id': gene_id,
            'success_rate': success_rate,
            'failures': failures,
            'successes': successes,
            'total_uses': len(failures) + len(successes)
        }
    
    def generate_optimization_suggestion(self, gene_id: str) -> Optional[str]:
        """生成 Gene 优化建议"""
        performance = self.analyze_gene_performance(gene_id)
        
        if performance['success_rate'] >= 0.6:
            return None  # 成功率足够高，无需优化
        
        # 生成优化提示
        prompt = f"""
Gene {gene_id} 表现分析:

成功率：{performance['success_rate']:.1%}
使用次数：{performance['total_uses']}

失败案例:
{json.dumps(performance['failures'], ensure_ascii=False, indent=2)}

成功案例:
{json.dumps(performance['successes'], ensure_ascii=False, indent=2)}

请分析:
1. 失败的主要原因是什么？
2. Gene 模板的思考层级是否需要调整？
3. 验证步骤是否需要加强？
4. 约束条件是否需要修改？

给出具体优化建议。
"""
        print(f"💡 生成优化建议中...")
        # 这里可以调用 LLM 生成建议
        # suggestion = llm_generate(prompt)
        suggestion = "建议：加强验证步骤，增加边界条件检查"
        
        return suggestion
    
    def get_gene_stats(self) -> Dict:
        """获取 Gene 统计"""
        # 获取所有使用过的 gene
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT gene_used FROM solutions WHERE gene_used IS NOT NULL
        ''')
        
        genes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        stats = []
        for gene_id in genes:
            success_rate = self.calculate_gene_success_rate(gene_id)
            
            stats.append({
                'gene_id': gene_id,
                'success_rate': success_rate,
            })
        
        # 按成功率排序
        stats.sort(key=lambda x: x['success_rate'], reverse=True)
        
        return {
            'total_genes': len(stats),
            'high_performers': [s for s in stats if s['success_rate'] >= 0.7],
            'low_performers': [s for s in stats if s['success_rate'] < 0.5],
            'all_stats': stats
        }
    
    def periodic_optimization(self):
        """定期优化 (建议每周执行)"""
        print("🔍 开始 Gene 表现分析...")
        
        stats = self.get_gene_stats()
        
        print(f"  总 Gene 数：{stats['total_genes']}")
        print(f"  高效 Gene: {len(stats['high_performers'])}")
        print(f"  低效 Gene: {len(stats['low_performers'])}")
        
        if stats['low_performers']:
            print("\n⚠️  低效 Gene 需要优化:")
            for gene in stats['low_performers'][:5]:
                print(f"  - {gene['gene_id']}: {gene['success_rate']:.1%}")
                suggestion = self.generate_optimization_suggestion(gene['gene_id'])
                if suggestion:
                    print(f"    💡 {suggestion}")


# 定期执行 (Cron: 每周)
if __name__ == '__main__':
    evolution = GeneEvolution()
    
    print("📊 Gene 表现统计:")
    stats = evolution.get_gene_stats()
    
    print(f"  总 Gene 数：{stats['total_genes']}")
    print(f"  高效 Gene: {len(stats['high_performers'])}")
    print(f"  低效 Gene: {len(stats['low_performers'])}")
    
    if stats['low_performers']:
        print("\n⚠️  低效 Gene 需要优化:")
        for gene in stats['low_performers'][:5]:
            print(f"  - {gene['gene_id']}: {gene['success_rate']:.1%}")
    
    # 定期优化
    evolution.periodic_optimization()
