#!/usr/bin/env python3
"""
Agent 感知拦截器 - 自动增强所有回复

这个脚本拦截 Agent 的输入输出，自动：
1. 检索相关记忆
2. 检索元规则
3. 增强回复
4. 记录进化事件

用法（作为 OpenClaw 的预处理脚本）:
    python3 skills/agent_perception_interceptor.py "用户消息" "原始回复"
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'libs'))

from memory_hub.session_storage import SessionMemoryStorage


class AgentPerceptionInterceptor:
    """Agent 感知拦截器"""
    
    def __init__(self, agent_name='demo51-agent'):
        self.agent_name = agent_name
        self.memory_path = Path(f'data/{agent_name}/memory/memory_stream.db')
        self.conn = None  # 延迟连接
    
    def _connect(self):
        """延迟连接数据库"""
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect(self.memory_path)
            self.conn.row_factory = sqlite3.Row
    
    def enhance(self, user_message: str, original_response: str) -> str:
        """增强回复"""
        self._connect()
        cursor = self.conn.cursor()
        
        # 检索相关记忆（按关键词匹配）
        keywords = self._extract_keywords(user_message)
        memories = []
        
        if keywords:
            for keyword in keywords[:3]:  # 最多 3 个关键词
                cursor.execute('''
                SELECT content, importance FROM session_memories 
                WHERE memory_type = 'observation' 
                AND content LIKE ?
                ORDER BY importance DESC, id DESC
                LIMIT 2
                ''', (f'%{keyword}%',))
                memories.extend([(row['content'], row['importance']) for row in cursor.fetchall()])
        
        # 去重
        seen = set()
        unique_memories = []
        for m in memories:
            if m[0][:50] not in seen:
                seen.add(m[0][:50])
                unique_memories.append(m)
        
        memories = unique_memories[:3]
        
        # 检索元规则（按重要性排序）
        cursor.execute('''
        SELECT content, importance FROM session_memories 
        WHERE memory_type = 'goal' 
        ORDER BY importance DESC, id DESC
        LIMIT 5
        ''')
        rules = [(row['content'], row['importance']) for row in cursor.fetchall()]
        
        # 如果没有检索到，返回原始回复
        if not memories and not rules:
            return original_response
        
        # 构建增强回复
        enhanced = original_response
        
        # 添加历史经验
        if memories:
            enhanced += "\n\n📚 **根据历史经验：**\n"
            for i, (content, importance) in enumerate(memories, 1):
                content = content[:150].replace('\n', ' ')
                enhanced += f"\n{i}. [{importance:.1f}分] {content}"
        
        # 添加元规则
        if rules:
            enhanced += "\n\n📜 **根据元规则：**\n"
            for i, (content, importance) in enumerate(rules, 1):
                enhanced += f"\n{i}. [{importance:.1f}分] {content}"
        
        return enhanced
    
    def _extract_keywords(self, message: str) -> list:
        """从消息中提取关键词"""
        # 简单的中文分词（按空格和标点）
        import re
        words = re.split(r'[\s,，.。?？!！]+', message)
        
        # 过滤停用词和短词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        keywords = [w for w in words if len(w) >= 2 and w not in stopwords]
        
        return keywords
    
    def record_interaction(self, user_message: str, response: str):
        """记录交互到进化事件"""
        import sqlite3
        db_path = Path(f'data/{self.agent_name}/evolution.db')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 简单分类
        event_type = 'TASK_COMPLETED'
        if any(k in user_message for k in ['Bug', '修复', '错误', '问题']):
            event_type = 'BUG_FIX'
        elif any(k in user_message for k in ['优化', '改进', '性能']):
            event_type = 'CODE_IMPROVED'
        elif any(k in user_message for k in ['学习', '理解', '知道']):
            event_type = 'KNOWLEDGE_GAINED'
        
        cursor.execute('''
        INSERT INTO evolution_events (timestamp, event_type, description, lesson_learned)
        VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), event_type, f'用户：{user_message[:50]}...', f'回复：{response[:50]}...'))
        
        conn.commit()
        conn.close()
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None


def main():
    """主函数 - 用于命令行测试"""
    if len(sys.argv) < 3:
        print("用法：python3 agent_perception_interceptor.py \"用户消息\" \"原始回复\"")
        print("\n示例:")
        print('  python3 agent_perception_interceptor.py "如何优化数据库？" "可以添加索引"')
        return
    
    user_message = sys.argv[1]
    original_response = sys.argv[2]
    
    interceptor = AgentPerceptionInterceptor()
    enhanced = interceptor.enhance(user_message, original_response)
    
    print("📤 用户：", user_message)
    print("\n📥 Agent:")
    print(enhanced)
    
    # 记录交互
    interceptor.record_interaction(user_message, enhanced)
    print("\n✅ 交互已记录")
    
    interceptor.close()


if __name__ == '__main__':
    main()
