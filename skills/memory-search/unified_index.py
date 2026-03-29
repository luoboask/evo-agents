#!/usr/bin/env python3
"""
统一记忆索引 - Unified Memory Index
使用 SQLite 统一存储向量索引和关系索引
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class UnifiedMemoryIndex:
    """统一记忆索引类"""
    
    def __init__(self, workspace):
        self.workspace = Path(workspace) if isinstance(workspace, str) else workspace
        self.db_path = self.workspace / 'data' / 'memory_index.db'
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(str(self.db_path))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                embedding BLOB,
                metadata TEXT,
                source TEXT,
                mem_type TEXT,
                importance REAL DEFAULT 5.0,
                created_at TEXT,
                updated_at TEXT
            );
            
            CREATE TABLE IF NOT EXISTS file_state (
                path TEXT PRIMARY KEY,
                mtime REAL,
                indexed_at TEXT,
                line_count INTEGER
            );
            
            CREATE INDEX IF NOT EXISTS idx_source ON memories(source);
            CREATE INDEX IF NOT EXISTS idx_type ON memories(mem_type);
            CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance);
            CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at);
        """)
        conn.commit()
        conn.close()
    
    def add(self, entry: Dict, embedding: Optional[List[float]] = None) -> str:
        """添加记忆"""
        import uuid
        
        mem_id = entry.get('id', str(uuid.uuid4()))
        content = entry.get('content', '')
        metadata = entry.get('metadata', {})
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO memories 
            (id, content, embedding, metadata, source, mem_type, importance, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mem_id,
            content,
            json.dumps(embedding) if embedding else None,
            json.dumps(metadata),
            metadata.get('source', ''),
            metadata.get('type', 'general'),
            metadata.get('importance', 5.0),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return mem_id
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """搜索记忆"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 全文搜索
        cursor.execute("""
            SELECT id, content, metadata, source, mem_type, importance, created_at
            FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        """, (f'%{query}%', top_k))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'content': row['content'],
                'metadata': json.loads(row['metadata']) if row['metadata'] else {},
                'source': row['source'],
                'type': row['mem_type'],
                'importance': row['importance'],
                'created_at': row['created_at']
            })
        
        conn.close()
        return results
    
    def index_file(self, file_path: Path) -> int:
        """索引文件"""
        count = 0
        
        try:
            content = file_path.read_text(encoding='utf-8')
            mtime = file_path.stat().st_mtime
            
            for line in content.split('\n'):
                if line.startswith('- [') and ']' in line:
                    start = line.find(']') + 1
                    if start > 0 and line[start:].strip():
                        entry = {
                            'content': line[start:].strip(),
                            'metadata': {
                                'source': str(file_path),
                                'type': 'file'
                            }
                        }
                        self.add(entry)
                        count += 1
            
            # 更新文件状态
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO file_state (path, mtime, indexed_at, line_count)
                VALUES (?, ?, ?, ?)
            """, (str(file_path), mtime, datetime.now().isoformat(), count))
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️  索引失败 {file_path}: {e}")
        
        return count
    
    def index_all(self) -> int:
        """索引所有记忆文件"""
        memory_dir = self.workspace / 'memory'
        total = 0
        
        for md_file in memory_dir.glob('*.md'):
            count = self.index_file(md_file)
            if count > 0:
                print(f"✅ 索引 {md_file.name}: {count} 条")
                total += count
        
        print(f"\n✅ 共索引 {total} 条记忆")
        return total
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM memories")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM file_state")
        files = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_memories': total,
            'indexed_files': files,
            'db_path': str(self.db_path)
        }


if __name__ == '__main__':
    import sys
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    
    index = UnifiedMemoryIndex(workspace)
    
    if len(sys.argv) > 2 and sys.argv[2] == '--index-all':
        index.index_all()
    
    stats = index.get_stats()
    print(f"\n📊 索引统计:")
    print(f"  总记忆数：{stats['total_memories']}")
    print(f"  索引文件：{stats['indexed_files']}")
    print(f"  数据库：{stats['db_path']}")
