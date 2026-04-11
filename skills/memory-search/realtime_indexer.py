#!/usr/bin/env python3
"""
实时记忆索引器 - 对话结束后立即嵌入

功能:
- 监听会话结束事件
- 立即嵌入新消息
- 更新记忆数据库
- 支持即时检索

用法:
    python3 skills/memory-search/realtime_indexer.py "session_id" "messages.jsonl"
"""

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / 'libs'))

from memory_hub.session_storage import SessionMemoryStorage


class RealtimeIndexer:
    """实时记忆索引器"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.memory_path = Path(f'data/{agent_name}/memory')
        self.storage = SessionMemoryStorage(self.memory_path)
        
        # 确保数据库初始化
        self.memory_path.mkdir(parents=True, exist_ok=True)
    
    def index_session(self, session_id: str, messages: list) -> int:
        """
        索引整个会话
        
        Args:
            session_id: 会话 ID
            messages: 消息列表
        
        Returns:
            索引的消息数
        """
        print(f"📥 索引会话 {session_id[:8]}... ({len(messages)} 条消息)")
        
        indexed = 0
        
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            
            if not content or len(content) < 10:
                continue
            
            # 判断消息类型
            if role == 'user':
                memory_type = 'observation'
                tags = ['user-message', 'session', 'realtime']
                importance = 5.0
            elif role == 'assistant':
                memory_type = 'observation'
                tags = ['assistant-message', 'session', 'realtime']
                importance = 6.0
            else:
                continue
            
            # 保存到记忆数据库
            try:
                self.storage.add_memory(
                    session_id=session_id,
                    content=f"[{role.upper()}] {content[:4000]}",
                    memory_type=memory_type,
                    importance=importance,
                    tags=tags,
                    metadata={
                        'timestamp': timestamp,
                        'role': role,
                        'indexed_at': datetime.now().isoformat(),
                        'realtime': True
                    }
                )
                indexed += 1
            except Exception as e:
                print(f"  ⚠️  索引失败：{e}")
        
        print(f"  ✅ 索引完成：{indexed}/{len(messages)} 条")
        return indexed
    
    def index_message(self, session_id: str, role: str, content: str, timestamp: str = None) -> bool:
        """
        索引单条消息
        
        Args:
            session_id: 会话 ID
            role: 角色 (user/assistant)
            content: 消息内容
            timestamp: 时间戳
        
        Returns:
            是否成功
        """
        if not content or len(content) < 10:
            return False
        
        memory_type = 'observation'
        tags = [f'{role}-message', 'realtime']
        importance = 5.0 if role == 'user' else 6.0
        
        try:
            self.storage.add_memory(
                session_id=session_id,
                content=f"[{role.upper()}] {content[:4000]}",
                memory_type=memory_type,
                importance=importance,
                tags=tags,
                metadata={
                    'timestamp': timestamp or datetime.now().isoformat(),
                    'role': role,
                    'indexed_at': datetime.now().isoformat(),
                    'realtime': True
                }
            )
            return True
        except Exception as e:
            print(f"  ⚠️  索引失败：{e}")
            return False
    
    def get_stats(self) -> dict:
        """获取索引统计"""
        import sqlite3
        db_path = self.memory_path / 'memory_stream.db'
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 总会话数
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM session_memories")
        total_sessions = cursor.fetchone()[0]
        
        # 总记忆数
        cursor.execute("SELECT COUNT(*) FROM session_memories")
        total_memories = cursor.fetchone()[0]
        
        # 实时索引数
        cursor.execute("SELECT COUNT(*) FROM session_memories WHERE metadata LIKE '%realtime%'")
        realtime_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_sessions': total_sessions,
            'total_memories': total_memories,
            'realtime_indexed': realtime_count
        }


def main():
    """主函数 - 命令行使用"""
    if len(sys.argv) < 3:
        print("用法：python3 realtime_indexer.py <agent_name> <session_file.jsonl>")
        print("\n示例:")
        print("  python3 realtime_indexer.py demo51-agent sessions/abc123.jsonl")
        return
    
    agent_name = sys.argv[1]
    session_file = Path(sys.argv[2])
    
    if not session_file.exists():
        print(f"❌ 文件不存在：{session_file}")
        return
    
    # 从文件名提取 session_id
    session_id = session_file.stem
    
    # 读取消息
    messages = []
    with open(session_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                msg = json.loads(line)
                if msg.get('type') == 'message':
                    messages.append(msg.get('message', {}))
            except:
                continue
    
    if not messages:
        print("⚠️  没有消息可索引")
        return
    
    # 索引
    indexer = RealtimeIndexer(agent_name)
    indexed = indexer.index_session(session_id, messages)
    
    # 统计
    stats = indexer.get_stats()
    print(f"\n📊 索引统计:")
    print(f"  总会话数：{stats['total_sessions']}")
    print(f"  总记忆数：{stats['total_memories']}")
    print(f"  实时索引：{stats['realtime_indexed']}")


if __name__ == '__main__':
    main()
