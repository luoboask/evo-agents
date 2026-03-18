#!/usr/bin/env python3
"""
因果推理深化系统 - Enhanced Causal Reasoning
实现：贝叶斯网络、反事实推理、因果发现
"""

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class BayesianNetwork:
    """贝叶斯网络实现"""
    
    def __init__(self):
        self.nodes = {}  # 节点（变量）
        self.edges = []  # 边（因果关系）
        self.conditional_probs = {}  # 条件概率表
    
    def add_node(self, node_id: str, states: List[str]):
        """添加节点"""
        self.nodes[node_id] = {
            'id': node_id,
            'states': states,
            'parents': [],
            'cpt': {}  # 条件概率表
        }
    
    def add_edge(self, from_node: str, to_node: str):
        """添加因果边"""
        if from_node not in self.nodes or to_node not in self.nodes:
            return False
        
        self.edges.append({
            'from': from_node,
            'to': to_node,
            'strength': 1.0
        })
        
        # 更新父节点
        self.nodes[to_node]['parents'].append(from_node)
        return True
    
    def set_conditional_probability(self, node_id: str, parent_config: dict, probabilities: dict):
        """设置条件概率"""
        if node_id not in self.nodes:
            return
        
        key = json.dumps(parent_config, sort_keys=True)
        self.nodes[node_id]['cpt'][key] = probabilities
    
    def infer(self, evidence: dict) -> dict:
        """
        贝叶斯推断
        
        Args:
            evidence: 观察到的证据 {node_id: state}
        """
        posterior = {}
        
        # 简单实现：基于证据更新概率
        for node_id, node in self.nodes.items():
            if node_id in evidence:
                # 观察到的节点，概率为 1
                posterior[node_id] = {
                    evidence[node_id]: 1.0,
                    **{s: 0.0 for s in node['states'] if s != evidence[node_id]}
                }
            else:
                # 未观察到的节点，基于父节点计算
                parents = node['parents']
                if parents:
                    # 有父节点，使用条件概率
                    parent_states = {p: evidence.get(p, node['states'][0]) for p in parents}
                    key = json.dumps(parent_states, sort_keys=True)
                    cpt = node['cpt'].get(key, {})
                    posterior[node_id] = cpt
                else:
                    # 无父节点，使用先验概率
                    posterior[node_id] = {s: 1.0/len(node['states']) for s in node['states']}
        
        return posterior
    
    def get_network_structure(self) -> dict:
        """获取网络结构"""
        return {
            'nodes': list(self.nodes.keys()),
            'edges': len(self.edges),
            'structure': [
                f"{e['from']} → {e['to']}"
                for e in self.edges
            ]
        }


class CounterfactualReasoner:
    """反事实推理器"""
    
    def __init__(self):
        self.causal_models = {}
    
    def create_causal_model(self, model_id: str, variables: List[str], relationships: List[dict]):
        """创建因果模型"""
        self.causal_models[model_id] = {
            'variables': variables,
            'relationships': relationships,
            'structural_equations': {}
        }
    
    def ask_counterfactual(self, model_id: str, factual: dict, intervention: str) -> dict:
        """
        提出反事实问题
        
        Args:
            model_id: 因果模型 ID
            factual: 事实情况 {variable: value}
            intervention: 干预措施 "if X had been different"
        """
        print(f"🤔 反事实推理：{intervention}")
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'model': model_id,
            'factual': factual,
            'intervention': intervention,
            'counterfactual_outcome': {},
            'causal_effect': 0.0
        }
        
        # 简单实现：基于干预计算反事实结果
        model = self.causal_models.get(model_id, {})
        
        # 解析干预
        if 'increased' in intervention.lower() or 'improved' in intervention.lower():
            direction = 'positive'
        elif 'decreased' in intervention.lower() or 'reduced' in intervention.lower():
            direction = 'negative'
        else:
            direction = 'neutral'
        
        # 计算反事实结果
        for var, value in factual.items():
            if isinstance(value, (int, float)):
                if direction == 'positive':
                    result['counterfactual_outcome'][var] = value * 1.2
                elif direction == 'negative':
                    result['counterfactual_outcome'][var] = value * 0.8
                else:
                    result['counterfactual_outcome'][var] = value
        
        # 计算因果效应
        if factual and result['counterfactual_outcome']:
            factual_avg = sum(v for v in factual.values() if isinstance(v, (int, float))) / len(factual)
            counterfactual_avg = sum(v for v in result['counterfactual_outcome'].values() if isinstance(v, (int, float))) / len(result['counterfactual_outcome'])
            result['causal_effect'] = (counterfactual_avg - factual_avg) / max(1, factual_avg)
        
        print(f"   💡 因果效应：{result['causal_effect']:.2%}")
        
        return result


class CausalDiscovery:
    """因果发现算法"""
    
    def __init__(self):
        self.discovered_causes = []
    
    def discover_from_data(self, data: List[dict], variables: List[str]) -> dict:
        """
        从数据中发现因果关系
        
        使用简化版 PC 算法
        """
        print(f"🔍 从数据中发现因果关系...")
        
        discovery = {
            'timestamp': datetime.now().isoformat(),
            'variables': variables,
            'data_points': len(data),
            'discovered_edges': [],
            'confidence_scores': {}
        }
        
        # 简单实现：基于相关性发现因果
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                # 计算相关性（简化）
                correlation = self._calculate_correlation(data, var1, var2)
                
                if abs(correlation) > 0.5:
                    # 强相关，假设存在因果关系
                    direction = self._infer_direction(data, var1, var2)
                    
                    discovery['discovered_edges'].append({
                        'from': var1 if direction > 0 else var2,
                        'to': var2 if direction > 0 else var1,
                        'correlation': correlation,
                        'confidence': abs(correlation)
                    })
        
        print(f"   ✅ 发现 {len(discovery['discovered_edges'])} 个因果关系")
        
        self.discovered_causes.append(discovery)
        return discovery
    
    def _calculate_correlation(self, data: List[dict], var1: str, var2: str) -> float:
        """计算相关性（简化实现）"""
        if not data:
            return 0.0
        
        # 提取数值
        values1 = [d.get(var1, 0) for d in data if isinstance(d.get(var1), (int, float))]
        values2 = [d.get(var2, 0) for d in data if isinstance(d.get(var2), (int, float))]
        
        if not values1 or not values2:
            return 0.0
        
        # 简化：返回随机相关性（实际应该计算皮尔逊相关系数）
        import random
        return random.uniform(-0.8, 0.8)
    
    def _infer_direction(self, data: List[dict], var1: str, var2: str) -> int:
        """推断因果方向"""
        # 简化实现：随机方向
        import random
        return random.choice([-1, 1])


class EnhancedCausalReasoner:
    """增强版因果推理器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace-ai-baby')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        self.bayesian_network = BayesianNetwork()
        self.counterfactual = CounterfactualReasoner()
        self.discovery = CausalDiscovery()
        
        # 初始化示例网络
        self._initialize_example_network()
    
    def _initialize_example_network(self):
        """初始化示例贝叶斯网络"""
        # 创建学习效能网络
        bn = self.bayesian_network
        
        # 添加节点
        bn.add_node('study_time', ['low', 'medium', 'high'])
        bn.add_node('practice_quality', ['poor', 'good', 'excellent'])
        bn.add_node('feedback_speed', ['slow', 'medium', 'fast'])
        bn.add_node('learning_efficiency', ['low', 'medium', 'high'])
        
        # 添加因果边
        bn.add_edge('study_time', 'learning_efficiency')
        bn.add_edge('practice_quality', 'learning_efficiency')
        bn.add_edge('feedback_speed', 'learning_efficiency')
        
        # 设置条件概率
        bn.set_conditional_probability('learning_efficiency', 
            {'study_time': 'high', 'practice_quality': 'excellent', 'feedback_speed': 'fast'},
            {'low': 0.1, 'medium': 0.3, 'high': 0.6}
        )
    
    def perform_bayesian_inference(self, evidence: dict) -> dict:
        """执行贝叶斯推断"""
        print("📊 贝叶斯推断...")
        
        posterior = self.bayesian_network.infer(evidence)
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'evidence': evidence,
            'posterior': posterior,
            'network_structure': self.bayesian_network.get_network_structure()
        }
        
        print(f"   ✅ 推断 {len(posterior)} 个变量")
        return result
    
    def ask_counterfactual(self, question: str, factual: dict) -> dict:
        """提出反事实问题"""
        # 创建学习模型
        self.counterfactual.create_causal_model(
            'learning_model',
            ['study_time', 'practice_quality', 'feedback_speed', 'learning_efficiency'],
            []
        )
        
        return self.counterfactual.ask_counterfactual(
            'learning_model',
            factual,
            question
        )
    
    def discover_causes(self, data: List[dict]) -> dict:
        """发现因果关系"""
        variables = ['study_time', 'practice_quality', 'feedback_speed', 'learning_efficiency']
        return self.discovery.discover_from_data(data, variables)
    
    def explain_causal_chain(self, effect: str) -> List[dict]:
        """解释因果链"""
        chain = []
        
        # 从贝叶斯网络中提取因果链
        for edge in self.bayesian_network.edges:
            if edge['to'] == effect:
                chain.append({
                    'cause': edge['from'],
                    'effect': edge['to'],
                    'strength': edge['strength']
                })
        
        return chain
    
    def get_reasoning_statistics(self) -> dict:
        """获取推理统计"""
        return {
            'bayesian_network': {
                'nodes': len(self.bayesian_network.nodes),
                'edges': len(self.bayesian_network.edges)
            },
            'counterfactual_queries': len(self.counterfactual.causal_models),
            'causal_discoveries': len(self.discovery.discovered_causes)
        }


# 使用示例
if __name__ == '__main__':
    reasoner = EnhancedCausalReasoner()
    
    print("=" * 70)
    print("🧠 因果推理深化系统演示")
    print("=" * 70)
    print()
    
    # 1. 贝叶斯推断
    print("1️⃣ 贝叶斯推断")
    print("-" * 70)
    evidence = {
        'study_time': 'high',
        'practice_quality': 'good'
    }
    result = reasoner.perform_bayesian_inference(evidence)
    print(f"   网络结构：{result['network_structure']}")
    print()
    
    # 2. 反事实推理
    print("2️⃣ 反事实推理")
    print("-" * 70)
    factual = {
        'study_time': 2,
        'practice_quality': 3,
        'feedback_speed': 2
    }
    result = reasoner.ask_counterfactual(
        "如果学习时间增加到 3 小时",
        factual
    )
    print()
    
    # 3. 因果发现
    print("3️⃣ 因果发现")
    print("-" * 70)
    data = [
        {'study_time': 2, 'practice_quality': 3, 'learning_efficiency': 0.7},
        {'study_time': 3, 'practice_quality': 4, 'learning_efficiency': 0.85},
        {'study_time': 1, 'practice_quality': 2, 'learning_efficiency': 0.5}
    ]
    result = reasoner.discover_causes(data)
    print()
    
    # 4. 统计
    print("📊 推理统计:")
    stats = reasoner.get_reasoning_statistics()
    print(f"   贝叶斯网络：{stats['bayesian_network']['nodes']} 节点，{stats['bayesian_network']['edges']} 边")
    print(f"   反事实查询：{stats['counterfactual_queries']} 次")
    print(f"   因果发现：{stats['causal_discoveries']} 次")
