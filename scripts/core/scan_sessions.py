#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_sessions.py - 扫描 OpenClaw Agent 会话并增量保存到记忆系统

功能:
- 扫描指定 Agent 下的所有 session
- 检测新增/更新的会话消息
- 增量保存到记忆数据库
- 支持多个 Agent
- 过滤 cron 产生的会话
- 按会话整体存储（而非逐条消息）

用法:
    python3 scan_sessions.py --agent main-agent
    python3 scan_sessions.py --agent main-agent --full-scan
    python3 scan_sessions.py --all-agents
"""

import sys
import os
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
import argparse

# 添加 libs 到路径（只在 __init__ 中添加，确保使用正确的路径）

# MemoryHub 将在 SessionScanner.__init__ 中导入（确保使用正确的路径）


class SessionScanner:
    """会话扫描器 - 扫描并增量保存会话历史"""
    
    def __init__(self, agent_name: str, workspace_root: Path = None):
        self.agent_name = agent_name
        self.workspace_root = workspace_root or self._find_workspace()
        self.openclaw_root = Path.home() / '.openclaw'
        self.agent_sessions_path = self.openclaw_root / 'agents' / agent_name / 'sessions'
        
        # 确保使用正确的 libs 路径
        if str(self.workspace_root / 'libs') not in sys.path:
            sys.path.insert(0, str(self.workspace_root / 'libs'))
        
        # 重新导入 MemoryHub（确保使用正确的路径）
        for mod in ['memory_hub', 'hub', 'path_utils']:
            if mod in sys.modules:
                del sys.modules[mod]
        
        # 确保路径正确
        libs_path = self.workspace_root / 'libs'
        if str(libs_path) not in sys.path:
            sys.path.insert(0, str(libs_path))
        
        from memory_hub import MemoryHub
        
        # 兼容不同版本的 MemoryHub
        try:
            # 新版本：支持 workspace_root 参数
            self.memory = MemoryHub(agent_name=agent_name, workspace_root=self.workspace_root)
        except TypeError:
            # 旧版本：只接受 agent_name
            self.memory = MemoryHub(agent_name=agent_name)
        
        # 状态文件（记录已处理的会话）
        self.state_file = self.workspace_root / 'data' / agent_name / '.session_scan_state.json'
        self.state = self._load_state()
    
    def _find_workspace(self) -> Path:
        """查找 workspace 路径"""
        # 从脚本位置推导
        current = Path(__file__).parent
        for _ in range(5):
            if (current / '.install-config').exists():
                return current
            if (current / '.git').exists():
                return current
            current = current.parent
        
        # 如果找不到，使用 ~/.openclaw/workspace-{agent_name}
        # 这是 evo-agents 的标准路径
        home_workspace = Path.home() / '.openclaw' / f'workspace-{self.agent_name}'
        if home_workspace.exists():
            return home_workspace
        
        return Path.cwd()
    
    def _load_state(self) -> Dict:
        """加载扫描状态"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except:
                pass
        return {
            'last_scan': None,
            'processed_sessions': {},  # session_id -> last_message_id
            'total_saved': 0
        }
    
    def _save_state(self):
        """保存扫描状态"""
        self.state['last_scan'] = datetime.now().isoformat()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
    
    def is_cron_session(self, session: Dict) -> bool:
        """判断是否为 cron 产生的会话"""
        session_id = session.get('sessionId', '')
        session_key = session.get('key', '')
        name = session.get('name', '')
        
        # 检查会话名称是否包含 cron 相关关键词
        cron_keywords = ['cron', 'session-scan', 'nightly-evolution', 'weekly-', 'daily-', 
                         'maintenance', 'compress', 'heartbeat', 'bridge-sync', 'fractal',
                         'aiway', 'rag-', 'memory-', 'test-']
        
        for keyword in cron_keywords:
            if keyword in name.lower() or keyword in session_key.lower():
                return True
        
        # 检查会话 ID 格式（cron 会话通常有特定模式）
        # 也可以通过 session metadata 判断
        
        return False
    
    def get_all_sessions(self) -> List[Dict]:
        """获取所有会话列表（过滤掉 cron 会话）"""
        sessions_file = self.agent_sessions_path / 'sessions.json'
        if not sessions_file.exists():
            return []
        
        try:
            data = json.loads(sessions_file.read_text())
            if isinstance(data, dict):
                # 新格式：{key: session_data, ...}
                sessions = []
                for key, session in data.items():
                    if isinstance(session, dict):
                        session['key'] = key
                        # 过滤掉 cron 产生的会话
                        if not self.is_cron_session(session):
                            sessions.append(session)
                        else:
                            print(f"  ⏭️  跳过 cron 会话：{session.get('name', key)[:40]}")
                return sessions
            elif isinstance(data, dict) and 'sessions' in data:
                # 旧格式：{sessions: [...]}
                all_sessions = data['sessions']
                # 过滤掉 cron 产生的会话
                return [s for s in all_sessions if not self.is_cron_session(s)]
        except Exception as e:
            print(f"⚠️  读取 sessions.json 失败：{e}")
        
        return []
    
    def read_session_history(self, session_id: str) -> List[Dict]:
        """读取会话历史（JSONL 文件）"""
        session_file = self.agent_sessions_path / f'{session_id}.jsonl'
        if not session_file.exists():
            return []
        
        messages = []
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        msg = json.loads(line)
                        if msg.get('type') == 'message':
                            messages.append(msg)
                    except:
                        continue
        except Exception as e:
            print(f"⚠️  读取 {session_file} 失败：{e}")
        
        return messages
    
    def get_last_processed_id(self, session_id: str) -> Optional[str]:
        """获取已处理的最后一条消息 ID"""
        return self.state['processed_sessions'].get(session_id)
    
    def extract_message_content(self, msg: Dict) -> str:
        """提取消息内容"""
        content = msg.get('message', {}).get('content', [])
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        texts.append(item.get('text', ''))
                    elif item.get('type') == 'thinking':
                        # 可选：保存思考内容
                        # texts.append(f"[思考] {item.get('thinking', '')}")
                        pass
            return '\n'.join(texts)
        elif isinstance(content, str):
            return content
        return ''
    
    def save_session_to_memory(self, session_id: str, session_key: str, messages: List[Dict], 
                                is_incremental: bool = False, new_count: int = 0):
        """保存完整会话到记忆系统（包含所有消息）"""
        if not messages:
            return
        
        # 提取会话摘要
        first_msg = messages[0]
        last_msg = messages[-1]
        
        # 统计角色分布
        user_count = sum(1 for m in messages if m.get('message', {}).get('role') == 'user')
        assistant_count = sum(1 for m in messages if m.get('message', {}).get('role') == 'assistant')
        
        # ❗ 新增：提取进化事件（纯规则，无需大模型）
        self.extract_and_record_evolution_events(messages, session_id)
        
        # 生成会话摘要内容（自动压缩）
        session_content = self._generate_session_summary(messages, target_length=8000)
        
        # 检查是否被截断或压缩
        is_truncated = len(session_content) >= 8000 or '[已压缩]' in session_content or '省略' in session_content
        
        # 判断会话类型
        if user_count > 0 and assistant_count > 0:
            memory_type = 'observation'
            tags = ['session', 'conversation', 'multi-turn']
            importance = 7.0  # 完整会话比单条消息更重要
        elif user_count > 0:
            memory_type = 'observation'
            tags = ['session', 'user-input']
            importance = 5.0
        elif assistant_count > 0:
            memory_type = 'observation'
            tags = ['session', 'assistant-response']
            importance = 6.0
        else:
            return
        
        try:
            # 直接调用 session_storage.add_memory() 保存到 session_memories 表
            # 这是唯一正确的方式，确保数据存入正确的表
            memory_id = self.memory.session_storage.add_memory(
                session_id=session_id,
                content=session_content,
                memory_type=memory_type,
                importance=importance,
                tags=tags,
                metadata={
                    'session_key': session_key,
                    'message_count': len(messages),
                    'user_count': user_count,
                    'assistant_count': assistant_count,
                    'first_timestamp': first_msg.get('timestamp', ''),
                    'last_timestamp': last_msg.get('timestamp', ''),
                    'is_incremental': is_incremental,
                    'new_messages': new_count,
                    'is_truncated': is_truncated,
                    'content_length': len(session_content)
                }
            )
            
            if memory_id:
                print(f"    ✓ 保存会话 {session_id[:8]}... ({len(messages)}条消息，ID={memory_id})")
        except Exception as e:
            print(f"⚠️  保存会话失败：{e}")
            import traceback
            traceback.print_exc()
    
    def _compress_message(self, content: str, max_length: int = 300) -> str:
        """压缩单条消息（提取关键信息）"""
        if len(content) <= max_length:
            return content
        
        # 尝试按段落压缩
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 1:
            # 保留首尾段落
            compressed = paragraphs[0]
            for p in paragraphs[1:-1]:
                if len(compressed) + len(p) + 50 < max_length:
                    compressed += '\n\n' + p
            if len(paragraphs) > 2:
                compressed += '\n\n...' + paragraphs[-1][:100]
            return compressed[:max_length]
        
        # 按句子压缩
        sentences = content.replace('。', '。\n').replace('！', '！\n').replace('？', '？\n').split('\n')
        if len(sentences) > 3:
            compressed = '\n'.join(sentences[:3]) + '\n...' + '\n'.join(sentences[-2:])
            return compressed[:max_length]
        
        return content[:max_length] + '...'
    
    def _generate_session_summary(self, messages: List[Dict], target_length: int = 8000) -> str:
        """生成完整会话记录（支持自动压缩）"""
        lines = []
        lines.append(f"=== 完整会话记录 ({len(messages)} 条消息) ===\n")
        
        # 第一阶段：尝试完整存储
        for i, msg in enumerate(messages, 1):
            role = msg.get('message', {}).get('role', 'unknown')
            content = self.extract_message_content(msg)
            timestamp = msg.get('timestamp', '')
            
            if content:
                if timestamp:
                    lines.append(f"\n--- [{i}] {timestamp} ---")
                lines.append(f"[{role.upper()}]: {content}")
        
        result = '\n'.join(lines)
        
        # 如果未超限，直接返回
        if len(result) <= target_length:
            return result
        
        # 第二阶段：压缩过长消息
        print(f"  📦 会话超出限制 ({len(result)} > {target_length})，开始压缩...")
        
        lines = []
        lines.append(f"=== 会话记录 (压缩版，{len(messages)} 条消息) ===\n")
        
        for i, msg in enumerate(messages, 1):
            role = msg.get('message', {}).get('role', 'unknown')
            content = self.extract_message_content(msg)
            timestamp = msg.get('timestamp', '')
            
            if content:
                # 根据消息数量动态调整单条长度限制
                dynamic_limit = max(200, min(500, target_length // len(messages)))
                
                if timestamp:
                    lines.append(f"\n--- [{i}] {timestamp} ---")
                
                # 压缩过长消息
                if len(content) > dynamic_limit:
                    compressed = self._compress_message(content, dynamic_limit)
                    lines.append(f"[{role.upper()}]: {compressed} [已压缩]")
                else:
                    lines.append(f"[{role.upper()}]: {content}")
        
        result = '\n'.join(lines)
        
        # 如果还是超限，只保留首尾消息
        if len(result) > target_length:
            print(f"  📦 二次压缩：保留首尾关键消息...")
            lines = []
            lines.append(f"=== 会话摘要 (精简版，{len(messages)} 条消息) ===\n")
            
            # 保留前 5 条和后 5 条
            keep_count = min(5, len(messages) // 2)
            for i, msg in enumerate(messages, 1):
                if i > keep_count and i <= len(messages) - keep_count:
                    if i == keep_count + 1:
                        lines.append(f"\n... [省略 {len(messages) - 2*keep_count} 条消息] ...\n")
                    continue
                
                role = msg.get('message', {}).get('role', 'unknown')
                content = self.extract_message_content(msg)
                timestamp = msg.get('timestamp', '')
                
                if content:
                    if timestamp:
                        lines.append(f"\n--- [{i}] {timestamp} ---")
                    compressed = self._compress_message(content, 400)
                    lines.append(f"[{role.upper()}]: {compressed}")
            
            result = '\n'.join(lines)
        
        return result[:target_length]
    
    def scan_session(self, session: Dict) -> int:
        """扫描单个会话，返回新增消息数（按会话整体存储）"""
        session_id = session.get('sessionId')
        session_key = session.get('key', '')
        
        if not session_id:
            return 0
        
        # 读取会话历史
        messages = self.read_session_history(session_id)
        if not messages:
            return 0
        
        # 获取已处理的最后一条消息
        last_processed_id = self.get_last_processed_id(session_id)
        
        # 判断是否是新会话或增量更新
        is_incremental = last_processed_id is not None
        
        # 找出新消息
        new_messages = []
        found_last = False if last_processed_id else True
        
        for msg in messages:
            msg_id = msg.get('id')
            if msg_id == last_processed_id:
                found_last = True
                continue
            
            if found_last:
                new_messages.append(msg)
        
        # 按会话整体存储（而非逐条消息）
        if new_messages:
            # 增量更新：只保存新消息
            # 全量：保存整个会话
            if is_incremental and len(new_messages) < len(messages):
                self.save_session_to_memory(
                    session_id, session_key, new_messages,
                    is_incremental=True, new_count=len(new_messages)
                )
            else:
                self.save_session_to_memory(
                    session_id, session_key, messages,
                    is_incremental=False, new_count=len(messages)
                )
        elif not is_incremental:
            # 首次扫描且无新消息，保存整个会话
            self.save_session_to_memory(
                session_id, session_key, messages,
                is_incremental=False, new_count=len(messages)
            )
        
        # 更新状态
        if messages:
            self.state['processed_sessions'][session_id] = messages[-1].get('id')
        
        return len(new_messages)
    
    def scan_all_sessions(self, full_scan: bool = False) -> Dict:
        """扫描所有会话（按会话整体存储）"""
        if full_scan:
            print("🔄 全量扫描模式...")
            self.state['processed_sessions'] = {}  # 清空状态
        
        sessions = self.get_all_sessions()
        if not sessions:
            print("⚠️  没有找到任何会话")
            return {'scanned': 0, 'new_messages': 0, 'sessions_saved': 0}
        
        print(f"📋 发现 {len(sessions)} 个会话（已过滤 cron 会话）")
        
        total_new = 0
        scanned = 0
        sessions_saved = 0
        
        for session in sessions:
            session_id = session.get('sessionId')
            if not session_id:
                continue
            
            new_count = self.scan_session(session)
            total_new += new_count
            scanned += 1
            
            if new_count > 0:
                sessions_saved += 1
                print(f"  ✓ {session_id[:8]}... +{new_count} 条消息 → 1 个会话记录")
        
        # 保存状态
        self.state['total_saved'] += total_new
        self._save_state()
        
        return {
            'scanned': scanned,
            'new_messages': total_new,
            'sessions_saved': sessions_saved,
            'total_saved': self.state['total_saved']
        }
    
    def cleanup_old_sessions(self, days: int = 30):
        """清理过期会话的记忆"""
        cutoff = datetime.now() - timedelta(days=days)
        
        # 获取所有会话记忆
        # TODO: 实现清理逻辑
        
        print(f"🧹 清理 {days} 天前的会话记忆（待实现）")
    
    # =====================================================================
    # 进化事件提取（纯规则，无需大模型）
    # =====================================================================
    
    def extract_and_record_evolution_events(self, messages: List[Dict], session_id: str):
        """从会话中提取进化事件（纯规则匹配）"""
        try:
            from libs.self_evolution.self_evolution_real import RealSelfEvolution
            evolution = RealSelfEvolution()
            
            events_recorded = 0
            
            for msg in messages:
                role = msg.get('message', {}).get('role')
                content = self.extract_message_content(msg)
                
                # 只分析 ASSISTANT 的消息
                if role != 'assistant' or not content:
                    continue
                
                # 匹配事件类型
                event_type = self.match_event_type(content)
                
                if event_type:
                    # 提取信息
                    description = content[:200]  # 截断
                    lesson = self.extract_lesson(content, event_type)
                    
                    # 记录到 evolution.db
                    evolution.record(
                        event_type=event_type,
                        description=f"会话 {session_id[:8]}...: {description}",
                        lesson_learned=lesson
                    )
                    events_recorded += 1
            
            if events_recorded > 0:
                print(f"  📈 提取 {events_recorded} 个进化事件")
        except Exception as e:
            # 静默失败，不影响主流程
            pass
    
    def match_event_type(self, content: str) -> Optional[str]:
        """匹配事件类型（关键词规则）"""
        content_lower = content.lower()
        
        # Bug 修复
        if any(k in content_lower for k in ['修复', 'bug', 'fix', '错误', 'error', '问题']):
            return 'BUG_FIX'
        
        # 功能新增
        if any(k in content_lower for k in ['新增', '添加', '功能', 'feature', 'add', '实现']):
            return 'FEATURE_ADDED'
        
        # 代码优化
        if any(k in content_lower for k in ['优化', '改进', '重构', 'optimize', 'refactor', '性能']):
            return 'CODE_IMPROVED'
        
        # 知识获取
        if any(k in content_lower for k in ['学习', '理解', 'learn', 'understand', '知道', '明白']):
            return 'KNOWLEDGE_GAINED'
        
        # 任务完成
        if any(k in content_lower for k in ['完成', 'done', 'finish', 'completed', '搞定']):
            return 'TASK_COMPLETED'
        
        return None
    
    def extract_lesson(self, content: str, event_type: str) -> str:
        """从内容中提取学习点（规则提取）"""
        lessons = {
            'BUG_FIX': '修复了问题，需要总结避免再次发生',
            'FEATURE_ADDED': '新增功能完成，需要文档化',
            'CODE_IMPROVED': '代码质量提升，需要保持',
            'KNOWLEDGE_GAINED': '获取新知识，需要应用',
            'TASK_COMPLETED': '任务完成，需要复盘'
        }
        return lessons.get(event_type, '任务已完成')


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='扫描 OpenClaw Agent 会话并增量保存')
    parser.add_argument('--agent', type=str, help='Agent 名称')
    parser.add_argument('--all-agents', action='store_true', help='扫描所有 Agent')
    parser.add_argument('--full-scan', action='store_true', help='全量扫描（忽略已处理状态）')
    parser.add_argument('--workspace', type=str, help='Workspace 路径')
    parser.add_argument('--cleanup-days', type=int, default=30, help='清理 N 天前的会话')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔍 OpenClaw 会话扫描器")
    print("=" * 60)
    
    if args.all_agents:
        # 扫描所有 Agent
        agents_path = Path.home() / '.openclaw' / 'agents'
        if not agents_path.exists():
            print("❌ 找不到 OpenClaw agents 目录")
            return
        
        agent_dirs = [d for d in agents_path.iterdir() if d.is_dir()]
        print(f"📋 发现 {len(agent_dirs)} 个 Agent\n")
        
        for agent_dir in agent_dirs:
            agent_name = agent_dir.name
            print(f"\n[{agent_name}]")
            scanner = SessionScanner(agent_name)
            result = scanner.scan_all_sessions(full_scan=args.full_scan)
            print(f"   扫描：{result['scanned']} 个会话")
            print(f"   新增：{result['new_messages']} 条消息")
            print(f"   保存会话记录：{result.get('sessions_saved', 0)} 个")
            print(f"   总计：{result['total_saved']} 条消息")
    else:
        # 扫描指定 Agent
        agent_name = args.agent
        if not agent_name:
            # 尝试从 .install-config 读取
            config_file = Path(args.workspace or '.') / '.install-config'
            if config_file.exists():
                for line in config_file.read_text().splitlines():
                    if line.startswith('agent_name='):
                        agent_name = line.split('=')[1].strip()
                        break
            
            if not agent_name:
                print("❌ 请指定 --agent 参数")
                return
        
        print(f"📦 Agent: {agent_name}")
        
        workspace = Path(args.workspace) if args.workspace else None
        scanner = SessionScanner(agent_name, workspace)
        result = scanner.scan_all_sessions(full_scan=args.full_scan)
        
        print(f"\n📊 扫描结果:")
        print(f"   扫描会话数：{result['scanned']}")
        print(f"   新增消息数：{result['new_messages']}")
        print(f"   保存会话记录：{result.get('sessions_saved', 0)} 个")
        print(f"   累计消息：{result.get('total_saved', 0)} 条")
        
        # 清理过期会话
        if args.cleanup_days:
            scanner.cleanup_old_sessions(args.cleanup_days)
    
    print("\n" + "=" * 60)
    print("✅ 扫描完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
