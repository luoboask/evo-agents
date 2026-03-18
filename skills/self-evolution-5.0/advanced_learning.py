#!/usr/bin/env python3
"""
高级学习系统 5.0 - Advanced Learning System
实现：实时学习、深度学习、迁移学习、社交学习、创造性学习
"""

import json
import hashlib
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import random


class RealTimeLearner:
    """1. 实时学习器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 实时学习记录
        self.session_log = []
        self.immediate_learnings = []
    
    def learn_from_interaction(self, interaction: dict):
        """从每次交互中实时学习"""
        learning = {
            'timestamp': datetime.now().isoformat(),
            'type': 'realtime',
            'user_input': interaction.get('user_input', '')[:100],
            'my_response': interaction.get('response', '')[:100],
            'outcome': interaction.get('outcome', 'unknown'),
            'lessons': []
        }
        
        # 提取学习点
        if interaction.get('success'):
            learning['lessons'].append({
                'type': 'success_pattern',
                'description': '成功的交互模式',
                'confidence': 0.8
            })
        else:
            learning['lessons'].append({
                'type': 'improvement_needed',
                'description': '需要改进的方面',
                'confidence': 0.9
            })
        
        self.immediate_learnings.append(learning)
        self._save_learning(learning)
        
        return learning
    
    def _save_learning(self, learning: dict):
        """保存学习记录"""
        today = datetime.now().strftime('%Y-%m-%d')
        file = self.learning_dir / f'realtime_learning_{today}.jsonl'
        with open(file, 'a') as f:
            f.write(json.dumps(learning, ensure_ascii=False) + '\n')
    
    def get_recent_learnings(self, limit=10) -> List[dict]:
        """获取最近学习"""
        return self.immediate_learnings[-limit:]


class DeepLearner:
    """2. 深度学习器（模式提取）"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        
        # 神经网络简化版（模式识别）
        self.pattern_weights = defaultdict(float)
        self.feature_extractors = []
        
        self._initialize_extractors()
    
    def _initialize_extractors(self):
        """初始化特征提取器"""
        self.feature_extractors = [
            self._extract_intent,
            self._extract_complexity,
            self._extract_domain,
            self._extract_sentiment
        ]
    
    def _extract_intent(self, text: str) -> str:
        """提取意图"""
        text_lower = text.lower()
        if any(w in text_lower for w in ['怎么', 'how', 'what', '什么']):
            return 'question'
        elif any(w in text_lower for w in ['创建', 'create', 'build', '做']):
            return 'creation'
        elif any(w in text_lower for w in ['分析', 'analyze', 'check']):
            return 'analysis'
        else:
            return 'general'
    
    def _extract_complexity(self, text: str) -> float:
        """提取复杂度"""
        words = text.split()
        return min(1.0, len(words) / 50)
    
    def _extract_domain(self, text: str) -> str:
        """提取领域"""
        text_lower = text.lower()
        domains = {
            'coding': ['code', 'python', '编程', '程序'],
            'learning': ['学习', 'learn', '知识', 'knowledge'],
            'system': ['系统', 'system', '配置', 'config']
        }
        for domain, keywords in domains.items():
            if any(kw in text_lower for kw in keywords):
                return domain
        return 'general'
    
    def _extract_sentiment(self, text: str) -> float:
        """提取情感（简化）"""
        positive = ['好', 'great', 'excellent', '成功', '满意']
        negative = ['坏', 'bad', 'error', '失败', '问题']
        
        text_lower = text.lower()
        pos_count = sum(1 for w in positive if w in text_lower)
        neg_count = sum(1 for w in negative if w in text_lower)
        
        return (pos_count - neg_count) / max(1, pos_count + neg_count)
    
    def learn_pattern(self, interaction: dict) -> dict:
        """学习深层模式"""
        text = interaction.get('user_input', '') + ' ' + interaction.get('response', '')
        
        # 提取特征
        features = {
            'intent': self._extract_intent(text),
            'complexity': self._extract_complexity(text),
            'domain': self._extract_domain(text),
            'sentiment': self._extract_sentiment(text)
        }
        
        # 更新权重
        outcome = interaction.get('outcome', 'neutral')
        reward = 1.0 if outcome == 'success' else -1.0 if outcome == 'failure' else 0.0
        
        for feature, value in features.items():
            key = f"{feature}:{value}"
            self.pattern_weights[key] += reward * 0.1
        
        pattern = {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'reward': reward,
            'confidence': abs(sum(self.pattern_weights.values()) / max(1, len(self.pattern_weights)))
        }
        
        self._save_pattern(pattern)
        return pattern
    
    def _save_pattern(self, pattern: dict):
        """保存模式"""
        file = self.learning_dir / 'deep_patterns.jsonl'
        with open(file, 'a') as f:
            f.write(json.dumps(pattern, ensure_ascii=False) + '\n')
    
    def get_learned_patterns(self) -> Dict[str, float]:
        """获取学习到的模式权重"""
        return dict(self.pattern_weights)


class TransferLearner:
    """3. 迁移学习器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        
        # 知识图谱用于迁移
        self.knowledge_domains = defaultdict(list)
        self.transfer_history = []
        
        self._load_knowledge()
    
    def _load_knowledge(self):
        """加载已有知识"""
        kb_file = self.learning_dir / 'knowledge_base.json'
        if kb_file.exists():
            with open(kb_file, 'r') as f:
                kb = json.load(f)
                for pattern in kb.get('patterns', []):
                    domain = pattern.get('subtype', 'general')
                    self.knowledge_domains[domain].append(pattern)
    
    def transfer_knowledge(self, source_domain: str, target_domain: str) -> dict:
        """跨领域知识迁移"""
        transferred = {
            'timestamp': datetime.now().isoformat(),
            'source': source_domain,
            'target': target_domain,
            'transferred_knowledge': [],
            'adaptations': []
        }
        
        # 查找源领域知识
        source_knowledge = self.knowledge_domains.get(source_domain, [])
        
        # 迁移并适配
        for knowledge in source_knowledge[:5]:  # 最多迁移 5 个
            adapted = self._adapt_knowledge(knowledge, source_domain, target_domain)
            transferred['transferred_knowledge'].append(adapted)
        
        # 记录迁移
        self.transfer_history.append(transferred)
        self._save_transfer(transferred)
        
        return transferred
    
    def _adapt_knowledge(self, knowledge: dict, source: str, target: str) -> dict:
        """适配知识到新领域"""
        adapted = knowledge.copy()
        adapted['adapted_from'] = source
        adapted['adapted_to'] = target
        adapted['adaptation_time'] = datetime.now().isoformat()
        return adapted
    
    def _save_transfer(self, transfer: dict):
        """保存迁移记录"""
        file = self.learning_dir / 'knowledge_transfer.jsonl'
        with open(file, 'a') as f:
            f.write(json.dumps(transfer, ensure_ascii=False) + '\n')
    
    def get_transfer_statistics(self) -> dict:
        """获取迁移统计"""
        return {
            'total_transfers': len(self.transfer_history),
            'domains_connected': len(self.knowledge_domains),
            'knowledge_transferred': sum(
                len(t['transferred_knowledge']) for t in self.transfer_history
            )
        }


class SocialLearner:
    """4. 社交学习器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        
        # 社交网络
        self.peers = []
        self.learned_from_others = []
    
    def add_peer(self, peer_info: dict):
        """添加学习对象（其他 AI 或用户）"""
        self.peers.append({
            'id': peer_info.get('id'),
            'type': peer_info.get('type', 'ai'),  # ai or human
            'expertise': peer_info.get('expertise', []),
            'added_at': datetime.now().isoformat()
        })
    
    def learn_from_peer(self, peer_id: str, knowledge: dict) -> dict:
        """从其他 AI/用户学习"""
        learning = {
            'timestamp': datetime.now().isoformat(),
            'peer_id': peer_id,
            'knowledge_type': knowledge.get('type', 'unknown'),
            'content': knowledge.get('content', '')[:200],
            'integration_status': 'pending'
        }
        
        # 整合知识
        if self._validate_knowledge(knowledge):
            learning['integration_status'] = 'integrated'
            self._integrate_knowledge(knowledge)
        
        self.learned_from_others.append(learning)
        self._save_social_learning(learning)
        
        return learning
    
    def _validate_knowledge(self, knowledge: dict) -> bool:
        """验证知识质量"""
        # 简单验证：检查是否有内容
        return bool(knowledge.get('content'))
    
    def _integrate_knowledge(self, knowledge: dict):
        """整合知识到知识库"""
        kb_file = self.learning_dir / 'knowledge_base.json'
        if kb_file.exists():
            with open(kb_file, 'r') as f:
                kb = json.load(f)
        else:
            kb = {'skills': [], 'patterns': [], 'lessons_learned': []}
        
        # 添加到知识库
        if knowledge.get('type') == 'skill':
            kb['skills'].append(knowledge.get('content'))
        elif knowledge.get('type') == 'pattern':
            kb['patterns'].append(knowledge.get('content'))
        
        with open(kb_file, 'w') as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
    
    def _save_social_learning(self, learning: dict):
        """保存社交学习记录"""
        file = self.learning_dir / 'social_learning.jsonl'
        with open(file, 'a') as f:
            f.write(json.dumps(learning, ensure_ascii=False) + '\n')
    
    def get_social_statistics(self) -> dict:
        """获取社交学习统计"""
        return {
            'peers_count': len(self.peers),
            'learnings_count': len(self.learned_from_others),
            'integrated_count': sum(
                1 for l in self.learned_from_others 
                if l['integration_status'] == 'integrated'
            )
        }


class CreativeLearner:
    """5. 创造性学习器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        
        # 创造性发现
        self.discoveries = []
        self.creative_connections = []
    
    def make_discovery(self, discovery: dict) -> dict:
        """做出新发现"""
        creative_discovery = {
            'timestamp': datetime.now().isoformat(),
            'type': 'creative',
            'description': discovery.get('description', ''),
            'novelty_score': self._calculate_novelty(discovery),
            'impact_score': self._calculate_impact(discovery),
            'connections': []
        }
        
        # 寻找关联
        creative_discovery['connections'] = self._find_creative_connections(discovery)
        
        self.discoveries.append(creative_discovery)
        self._save_discovery(creative_discovery)
        
        return creative_discovery
    
    def _calculate_novelty(self, discovery: dict) -> float:
        """计算新颖性分数"""
        # 简化实现：基于描述长度和独特性
        desc = discovery.get('description', '')
        unique_words = len(set(desc.lower().split()))
        return min(1.0, unique_words / 20)
    
    def _calculate_impact(self, discovery: dict) -> float:
        """计算影响力分数"""
        # 简化实现：基于潜在应用范围
        impact_keywords = ['all', 'every', 'system', 'global', 'universal']
        desc = discovery.get('description', '').lower()
        impact_count = sum(1 for kw in impact_keywords if kw in desc)
        return min(1.0, impact_count * 0.2)
    
    def _find_creative_connections(self, discovery: dict) -> List[dict]:
        """寻找创造性关联"""
        connections = []
        
        # 随机发现关联（模拟创造性思维）
        domains = ['coding', 'learning', 'system', 'communication']
        for _ in range(random.randint(1, 3)):
            connections.append({
                'domain': random.choice(domains),
                'strength': random.uniform(0.5, 1.0),
                'description': f"Creative connection to {random.choice(domains)}"
            })
        
        return connections
    
    def _save_discovery(self, discovery: dict):
        """保存发现"""
        file = self.learning_dir / 'creative_discoveries.jsonl'
        with open(file, 'a') as f:
            f.write(json.dumps(discovery, ensure_ascii=False) + '\n')
    
    def get_creative_statistics(self) -> dict:
        """获取创造性学习统计"""
        if not self.discoveries:
            return {
                'total_discoveries': 0,
                'avg_novelty': 0,
                'avg_impact': 0
            }
        
        return {
            'total_discoveries': len(self.discoveries),
            'avg_novelty': sum(d['novelty_score'] for d in self.discoveries) / len(self.discoveries),
            'avg_impact': sum(d['impact_score'] for d in self.discoveries) / len(self.discoveries),
            'total_connections': sum(len(d['connections']) for d in self.discoveries)
        }


class AdvancedLearningSystem:
    """高级学习系统 5.0 - 统一控制器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        
        # 初始化 5 个学习器
        self.realtime_learner = RealTimeLearner(workspace)
        self.deep_learner = DeepLearner(workspace)
        self.transfer_learner = TransferLearner(workspace)
        self.social_learner = SocialLearner(workspace)
        self.creative_learner = CreativeLearner(workspace)
        
        print("🚀 高级学习系统 5.0 已启动")
        print(f"   工作空间：{self.workspace}")
        print()
    
    def learn_comprehensively(self, interaction: dict) -> dict:
        """综合学习（5 种方式同时）"""
        print("=" * 60)
        print("🧠 综合学习过程")
        print("=" * 60)
        print()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'interaction': interaction,
            'learnings': {}
        }
        
        # 1. 实时学习
        print("1️⃣ 实时学习...")
        realtime = self.realtime_learner.learn_from_interaction(interaction)
        results['learnings']['realtime'] = realtime
        print(f"   学习点：{len(realtime.get('lessons', []))} 个")
        print()
        
        # 2. 深度学习
        print("2️⃣ 深度学习（模式提取）...")
        pattern = self.deep_learner.learn_pattern(interaction)
        results['learnings']['deep'] = pattern
        print(f"   特征：{len(pattern.get('features', {}))} 个")
        print(f"   置信度：{pattern.get('confidence', 0):.2f}")
        print()
        
        # 3. 迁移学习
        print("3️⃣ 迁移学习...")
        domain = pattern.get('features', {}).get('domain', 'general')
        transfer = self.transfer_learner.transfer_knowledge('general', domain)
        results['learnings']['transfer'] = transfer
        print(f"   迁移知识：{len(transfer.get('transferred_knowledge', []))} 个")
        print()
        
        # 4. 社交学习
        print("4️⃣ 社交学习...")
        # 模拟从用户学习
        social = self.social_learner.learn_from_peer('user', {
            'type': 'preference',
            'content': interaction.get('user_input', '')[:100]
        })
        results['learnings']['social'] = social
        print(f"   整合状态：{social.get('integration_status')}")
        print()
        
        # 5. 创造性学习
        print("5️⃣ 创造性学习...")
        discovery = self.creative_learner.make_discovery({
            'description': f"New pattern in {domain} domain"
        })
        results['learnings']['creative'] = discovery
        print(f"   新颖性：{discovery.get('novelty_score', 0):.2f}")
        print(f"   影响力：{discovery.get('impact_score', 0):.2f}")
        print()
        
        print("=" * 60)
        print("✅ 综合学习完成")
        print("=" * 60)
        
        return results
    
    def get_learning_statistics(self) -> dict:
        """获取学习统计"""
        return {
            'realtime': len(self.realtime_learner.immediate_learnings),
            'deep_patterns': len(self.deep_learner.pattern_weights),
            'transfers': self.transfer_learner.get_transfer_statistics(),
            'social': self.social_learner.get_social_statistics(),
            'creative': self.creative_learner.get_creative_statistics()
        }


# 使用示例
if __name__ == '__main__':
    system = AdvancedLearningSystem()
    
    # 模拟交互
    interaction = {
        'user_input': '怎么优化搜索性能？我需要更快的响应时间。',
        'response': '使用缓存和索引可以显著提升搜索性能...',
        'outcome': 'success'
    }
    
    # 综合学习
    results = system.learn_comprehensively(interaction)
    
    # 显示统计
    print("\n📊 学习统计:")
    stats = system.get_learning_statistics()
    print(f"   实时学习：{stats['realtime']} 次")
    print(f"   深度模式：{stats['deep_patterns']} 个")
    print(f"   知识迁移：{stats['transfers']}")
    print(f"   社交学习：{stats['social']}")
    print(f"   创造性：{stats['creative']}")
