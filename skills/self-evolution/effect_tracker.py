#!/usr/bin/env python3
"""
效果追踪器 - 追踪进化方案的实际效果

核心功能:
- 记录解决方案的使用效果
- 统计成功/失败次数
- 识别真正有效的方案
- 淘汰无效方案
"""

import sqlite3
import hashlib
import fcntl
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class EffectTracker:
    """效果追踪器"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Path(__file__).parent / 'evolution_effects.db'
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 解决方案表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_hash TEXT UNIQUE,
                problem_type TEXT,
                problem_description TEXT,
                solution TEXT,
                gene_used TEXT,
                created_at TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                last_used TEXT,
                user_feedback TEXT
            )
        ''')
        
        # 使用记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solution_id INTEGER,
                timestamp TEXT,
                success BOOLEAN,
                user_feedback TEXT,
                context TEXT,
                FOREIGN KEY (solution_id) REFERENCES solutions(id)
            )
        ''')
        
        # 策略切换记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_switches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                old_strategy TEXT,
                new_strategy TEXT,
                reason TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _hash_problem(self, problem: str) -> str:
        """问题哈希 (用于快速匹配)"""
        return hashlib.md5(problem.encode()).hexdigest()[:16]
    
    def record_solution(self, 
                       problem: str, 
                       problem_type: str,
                       solution: str,
                       gene_used: str = None):
        """记录新解决方案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        problem_hash = self._hash_problem(problem)
        
        cursor.execute('''
            INSERT OR REPLACE INTO solutions 
            (problem_hash, problem_type, problem_description, solution, 
             gene_used, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (problem_hash, problem_type, problem[:500], solution, 
              gene_used, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"📝 记录解决方案：{problem_type}")
    
    def mark_used(self, 
                  problem: str, 
                  success: bool, 
                  user_feedback: str = None,
                  context: str = None):
        """标记解决方案已使用 (带锁，并发安全)"""
        
        # 获取文件锁
        lock_file = self.db_path.with_suffix('.lock')
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(lock_file, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                problem_hash = self._hash_problem(problem)
                
                # 查找匹配的解决方案
                cursor.execute('''
                    SELECT id FROM solutions WHERE problem_hash = ?
                ''', (problem_hash,))
                
                row = cursor.fetchone()
                if not row:
                    conn.close()
                    return
                
                solution_id = row[0]
                
                # 更新统计
                if success:
                    cursor.execute('''
                        UPDATE solutions 
                        SET success_count = success_count + 1,
                            last_used = ?
                        WHERE id = ?
                    ''', (datetime.now().isoformat(), solution_id))
                else:
                    cursor.execute('''
                        UPDATE solutions 
                        SET failure_count = failure_count + 1,
                            last_used = ?
                        WHERE id = ?
                    ''', (datetime.now().isoformat(), solution_id))
                
                # 记录使用详情
                cursor.execute('''
                    INSERT INTO usage_records 
                    (solution_id, timestamp, success, user_feedback, context)
                    VALUES (?, ?, ?, ?, ?)
                ''', (solution_id, datetime.now().isoformat(), success, 
                      user_feedback, context))
                
                conn.commit()
                conn.close()
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{status} 记录解决方案使用效果")
    
    def get_effective_solutions(self, 
                               min_success: int = 3, 
                               max_failure: int = 1) -> List[Dict]:
        """获取真正有效的解决方案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM solutions 
            WHERE success_count >= ? 
            AND failure_count <= ?
            ORDER BY success_count DESC
        ''', (min_success, max_failure))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_ineffective_solutions(self, max_failure: int = 5) -> List[Dict]:
        """获取无效解决方案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM solutions 
            WHERE failure_count >= ?
            ORDER BY failure_count DESC
        ''', (max_failure,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def prune_ineffective(self, max_failure: int = 5) -> int:
        """淘汰无效方案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM solutions 
            WHERE failure_count >= ?
        ''', (max_failure,))
        
        deleted = cursor.rowcount
        
        # 同时删除关联的使用记录
        cursor.execute('''
            DELETE FROM usage_records 
            WHERE solution_id NOT IN (SELECT id FROM solutions)
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"🗑️  淘汰 {deleted} 个无效解决方案")
        return deleted
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总方案数
        cursor.execute('SELECT COUNT(*) FROM solutions')
        total = cursor.fetchone()[0]
        
        # 有效方案数
        cursor.execute('''
            SELECT COUNT(*) FROM solutions 
            WHERE success_count >= 3 AND failure_count <= 1
        ''')
        effective = cursor.fetchone()[0]
        
        # 无效方案数
        cursor.execute('''
            SELECT COUNT(*) FROM solutions 
            WHERE failure_count >= 5
        ''')
        ineffective = cursor.fetchone()[0]
        
        # 平均成功率
        cursor.execute('''
            SELECT AVG(success_count * 1.0 / (success_count + failure_count + 1)) 
            FROM solutions
        ''')
        avg_success_rate = cursor.fetchone()[0] or 0.5
        
        conn.close()
        
        return {
            'total_solutions': total,
            'effective_solutions': effective,
            'ineffective_solutions': ineffective,
            'effective_rate': effective / total if total > 0 else 0,
            'average_success_rate': avg_success_rate
        }
    
    def _row_to_dict(self, row) -> Dict:
        """数据库行转字典"""
        return {
            'id': row[0],
            'problem_hash': row[1],
            'problem_type': row[2],
            'problem_description': row[3],
            'solution': row[4],
            'gene_used': row[5],
            'created_at': row[6],
            'success_count': row[7],
            'failure_count': row[8],
            'last_used': row[9],
            'user_feedback': row[10]
        }


# 命令行工具
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='效果追踪器')
    parser.add_argument('--stats', action='store_true', help='显示统计')
    parser.add_argument('--prune', action='store_true', help='淘汰无效方案')
    parser.add_argument('--effective', action='store_true', help='列出有效方案')
    
    args = parser.parse_args()
    
    tracker = EffectTracker()
    
    if args.stats:
        stats = tracker.get_stats()
        print("📊 效果统计:")
        print(f"  总方案数：{stats['total_solutions']}")
        print(f"  有效方案：{stats['effective_solutions']} ({stats['effective_rate']:.1%})")
        print(f"  无效方案：{stats['ineffective_solutions']}")
        print(f"  平均成功率：{stats['average_success_rate']:.1%}")
    
    if args.prune:
        tracker.prune_ineffective()
    
    if args.effective:
        solutions = tracker.get_effective_solutions()
        print(f"✅ 有效方案 ({len(solutions)} 个):")
        for s in solutions[:10]:
            print(f"  - {s['problem_type']}: {s['success_count']} 次成功")
