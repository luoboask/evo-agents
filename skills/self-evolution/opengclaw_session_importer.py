#!/usr/bin/env python3
"""
OpenClaw 会话导入器
从 OpenClaw 会话记录中提取重要对话到记忆系统
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class OpenClawSessionImporter:
    """OpenClaw 会话导入器"""
    
    def __init__(self, agent_name: str = None):
        self.agent_name = agent_name or Path.cwd().name.replace('workspace-', '')
        self.sessions_dir = Path.home() / '.openclaw' / 'agents' / self.agent_name / 'sessions'
        
    def get_recent_sessions(self, days: int = 1) -> List[Dict]:
        """获取最近的会话记录（OpenClaw 格式）"""
        sessions = []
        cutoff = datetime.now() - timedelta(days=days)
        
        if not self.sessions_dir.exists():
            return sessions
        
        # 读取所有会话文件
        for session_file in self.sessions_dir.glob('*.jsonl'):
            with open(session_file, 'r', encoding='utf-8') as f:
                current_user = None
                for line in f:
                    try:
                        entry = json.loads(line)
                        entry_type = entry.get('type', '')
                        
                        # 提取用户消息
                        if entry_type == 'message':
                            msg = entry.get('message', {})
                            role = msg.get('role', '')
                            content = msg.get('content', '')
                            if isinstance(content, list):
                                content = ' '.join([c.get('text', '') for c in content])
                            
                            if role == 'user':
                                current_user = content
                            elif role == 'assistant' and current_user:
                                # 保存对话对
                                sessions.append({
                                    'user_message': current_user,
                                    'agent_response': content,
                                    'timestamp': entry.get('timestamp', '')
                                })
                                current_user = None
                    except:
                        pass
        
        return sessions
    
    def evaluate_importance(self, user_message: str, agent_response: str) -> float:
        """评估对话重要性（1-10 分）"""
        score = 5.0  # 基础分
        
        # 关键词加分
        important_keywords = ['决定', '记住', '重要', '必须', '配置', '教程', '如何']
        if any(kw in user_message.lower() for kw in important_keywords):
            score += 2
        
        # 技术问题加分
        tech_keywords = ['代码', '函数', 'api', '数据库', '配置', '错误', 'bug', 'python']
        if any(kw in user_message.lower() for kw in tech_keywords):
            score += 2
        
        # 长对话加分
        if len(user_message) > 50 or len(agent_response) > 200:
            score += 1
        
        # 包含代码加分
        if '```' in user_message or '```' in agent_response:
            score += 2
        
        return max(1.0, min(10.0, score))
    
    def import_to_memory(self, sessions: List[Dict], memory_system) -> int:
        """导入会话到记忆系统"""
        count = 0
        
        for session in sessions:
            user_message = session.get('user_message', '')
            agent_response = session.get('agent_response', '')
            
            if not user_message or not agent_response:
                continue
            
            # 评估重要性
            importance = self.evaluate_importance(user_message, agent_response)
            
            # 只记录重要的对话（>= 7 分）
            if importance >= 7.0:
                # 添加到记忆系统
                content = f"User: {user_message}\nAgent: {agent_response}"
                memory_system.record_interaction(
                    role='assistant',
                    content=content,
                    metadata={
                        'type': 'dialogue_import',
                        'source': 'opengclaw_session',
                        'importance': importance,
                        'user_message': user_message,
                        'agent_response': agent_response
                    }
                )
                count += 1
                print(f"✅ 导入重要对话（重要性：{importance}/10）")
        
        return count
    
    def run_nightly_import(self, memory_system, days: int = 1) -> Dict:
        """运行夜间导入（每日凌晨执行）"""
        print(f"🌙 开始夜间会话导入（最近 {days} 天）...")
        
        sessions = self.get_recent_sessions(days)
        print(f"📊 找到 {len(sessions)} 条会话")
        
        count = self.import_to_memory(sessions, memory_system)
        print(f"✅ 导入 {count} 条重要对话到记忆系统")
        
        return {
            'total_sessions': len(sessions),
            'imported': count,
            'date': datetime.now().isoformat()
        }


if __name__ == '__main__':
    # 测试
    importer = OpenClawSessionImporter()
    sessions = importer.get_recent_sessions(days=1)
    print(f"找到 {len(sessions)} 条会话")
    
    if sessions:
        # 显示第一条
        s = sessions[0]
        print(f"\n示例会话:")
        print(f"  用户：{s.get('user_message', '')[:100]}")
        print(f"  Agent: {s.get('agent_response', '')[:100]}")
        print(f"  重要性：{importer.evaluate_importance(s.get('user_message', ''), s.get('agent_response', ''))}/10")
