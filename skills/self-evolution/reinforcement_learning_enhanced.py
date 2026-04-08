#!/usr/bin/env python3
"""
强化学习优化系统 - Enhanced Reinforcement Learning
实现：深度 Q 网络、经验回放、目标网络
"""

import json
import math
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import deque


class ExperienceReplay:
    """经验回放缓冲区"""
    
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state: str, action: str, reward: float, next_state: str, done: bool):
        """添加经验"""
        self.buffer.append({
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state,
            'done': done,
            'timestamp': datetime.now().isoformat()
        })
    
    def sample(self, batch_size: int) -> List[dict]:
        """随机采样"""
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))
    
    def __len__(self) -> int:
        return len(self.buffer)
    
    def get_statistics(self) -> dict:
        """统计信息"""
        if not self.buffer:
            return {'size': 0, 'avg_reward': 0}
        
        rewards = [exp['reward'] for exp in self.buffer]
        return {
            'size': len(self.buffer),
            'avg_reward': sum(rewards) / len(rewards),
            'max_reward': max(rewards),
            'min_reward': min(rewards)
        }


class DeepQNetwork:
    """简化版深度 Q 网络（使用函数近似）"""
    
    def __init__(self, state_dim: int, action_dim: int):
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # 简化：使用字典存储 Q 值
        self.q_values = {}
        
        # 学习参数
        self.learning_rate = 0.01
        self.discount_factor = 0.99
        self.epsilon = 1.0  # 探索率
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
    
    def get_q_value(self, state: str, action: str) -> float:
        """获取 Q 值"""
        key = f"{state}_{action}"
        return self.q_values.get(key, 0.0)
    
    def update_q_value(self, state: str, action: str, target: float):
        """更新 Q 值"""
        key = f"{state}_{action}"
        current = self.q_values.get(key, 0.0)
        self.q_values[key] = current + self.learning_rate * (target - current)
    
    def get_best_action(self, state: str, actions: List[str]) -> str:
        """选择最优动作（ε-greedy）"""
        if random.random() < self.epsilon:
            return random.choice(actions)
        
        best_action = None
        best_value = float('-inf')
        
        for action in actions:
            value = self.get_q_value(state, action)
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action or random.choice(actions)
    
    def decay_epsilon(self):
        """衰减探索率"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def train_batch(self, batch: List[dict], actions: List[str]):
        """训练一个批次"""
        for exp in batch:
            state = exp['state']
            action = exp['action']
            reward = exp['reward']
            next_state = exp['next_state']
            done = exp['done']
            
            # 计算目标 Q 值
            if done:
                target = reward
            else:
                # 最大下一状态 Q 值
                max_next_q = max(
                    self.get_q_value(next_state, a) for a in actions
                )
                target = reward + self.discount_factor * max_next_q
            
            # 更新 Q 值
            self.update_q_value(state, action, target)
        
        # 衰减探索率
        self.decay_epsilon()
    
    def get_network_statistics(self) -> dict:
        """网络统计"""
        return {
            'q_values_count': len(self.q_values),
            'epsilon': self.epsilon,
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor
        }


class TargetNetwork:
    """目标网络（稳定训练）"""
    
    def __init__(self, main_network: DeepQNetwork, update_frequency: int = 10):
        self.main_network = main_network
        self.update_frequency = update_frequency
        self.training_steps = 0
        self.target_q_values = {}
    
    def update(self):
        """从主网络更新目标网络"""
        self.target_q_values = self.main_network.q_values.copy()
        self.training_steps = 0
    
    def should_update(self) -> bool:
        """是否应该更新"""
        self.training_steps += 1
        return self.training_steps >= self.update_frequency
    
    def get_target_q_value(self, state: str, action: str) -> float:
        """获取目标 Q 值"""
        key = f"{state}_{action}"
        return self.target_q_values.get(key, 0.0)


class EnhancedReinforcementLearner:
    """增强版强化学习器"""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace) if workspace else Path('/Users/dhr/.openclaw/workspace')
        self.learning_dir = self.workspace / 'memory' / 'learning'
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        self.experience_replay = ExperienceReplay(capacity=10000)
        self.q_network = DeepQNetwork(state_dim=100, action_dim=10)
        self.target_network = TargetNetwork(self.q_network, update_frequency=10)
        
        # 学习统计
        self.training_history = []
        self.total_episodes = 0
        
        self._load_model()
    
    def _load_model(self):
        """加载模型"""
        model_file = self.learning_dir / 'rl_model.json'
        if model_file.exists():
            with open(model_file, 'r') as f:
                model_data = json.load(f)
                self.q_network.q_values = model_data.get('q_values', {})
                self.q_network.epsilon = model_data.get('epsilon', 0.1)
    
    def _save_model(self):
        """保存模型"""
        model_file = self.learning_dir / 'rl_model.json'
        with open(model_file, 'w') as f:
            json.dump({
                'q_values': self.q_network.q_values,
                'epsilon': self.q_network.epsilon,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    
    def interact(self, state: str, actions: List[str]) -> str:
        """与环境交互"""
        return self.q_network.get_best_action(state, actions)
    
    def learn(self, state: str, action: str, reward: float, next_state: str, done: bool):
        """学习"""
        # 存储经验
        self.experience_replay.push(state, action, reward, next_state, done)
        
        # 采样批次
        batch_size = 32
        batch = self.experience_replay.sample(batch_size)
        
        # 训练
        actions = list(set([exp['action'] for exp in batch]))
        if not actions:
            actions = ['default_action']
        
        self.q_network.train_batch(batch, actions)
        
        # 更新目标网络
        if self.target_network.should_update():
            self.target_network.update()
        
        # 记录历史
        self.training_history.append({
            'timestamp': datetime.now().isoformat(),
            'state': state,
            'action': action,
            'reward': reward,
            'epsilon': self.q_network.epsilon
        })
    
    def train_episode(self, episode_data: dict) -> dict:
        """训练一个回合"""
        self.total_episodes += 1
        
        episode_result = {
            'episode': self.total_episodes,
            'timestamp': datetime.now().isoformat(),
            'steps': 0,
            'total_reward': 0,
            'final_epsilon': self.q_network.epsilon
        }
        
        # 模拟回合
        state = episode_data.get('initial_state', 'initial')
        actions = episode_data.get('actions', ['action1', 'action2', 'action3'])
        
        for step in range(10):  # 最多 10 步
            # 选择动作
            action = self.interact(state, actions)
            
            # 模拟环境响应（简化）
            next_state = f"state_{step + 1}"
            reward = random.uniform(-1, 1)
            done = (step == 9)
            
            # 学习
            self.learn(state, action, reward, next_state, done)
            
            episode_result['steps'] += 1
            episode_result['total_reward'] += reward
            
            if done:
                break
            
            state = next_state
        
        # 保存模型
        self._save_model()
        
        return episode_result
    
    def get_learning_statistics(self) -> dict:
        """获取学习统计"""
        if not self.training_history:
            return {
                'total_episodes': 0,
                'total_steps': 0,
                'avg_reward': 0,
                'current_epsilon': self.q_network.epsilon
            }
        
        recent_rewards = [h['reward'] for h in self.training_history[-100:]]
        
        return {
            'total_episodes': self.total_episodes,
            'total_steps': len(self.training_history),
            'avg_reward': sum(recent_rewards) / max(1, len(recent_rewards)),
            'current_epsilon': self.q_network.epsilon,
            'experience_replay': self.experience_replay.get_statistics(),
            'q_network': self.q_network.get_network_statistics()
        }
    
    def evaluate_policy(self, test_states: List[str], actions: List[str]) -> dict:
        """评估策略"""
        results = []
        
        for state in test_states:
            action = self.interact(state, actions)
            q_value = self.q_network.get_q_value(state, action)
            results.append({
                'state': state,
                'action': action,
                'q_value': q_value
            })
        
        return {
            'test_states': len(test_states),
            'avg_q_value': sum(r['q_value'] for r in results) / max(1, len(results)),
            'policy_results': results
        }


# 使用示例
if __name__ == '__main__':
    learner = EnhancedReinforcementLearner()
    
    print("=" * 70)
    print("🧠 强化学习优化系统演示")
    print("=" * 70)
    print()
    
    # 1. 训练回合
    print("1️⃣ 训练回合")
    print("-" * 70)
    for i in range(5):
        episode_data = {
            'initial_state': f'episode_{i}',
            'actions': ['optimize', 'learn', 'reflect', 'create', 'collaborate']
        }
        result = learner.train_episode(episode_data)
        print(f"   回合 {result['episode']}: "
              f"步数={result['steps']}, "
              f"总奖励={result['total_reward']:.2f}, "
              f"ε={result['final_epsilon']:.3f}")
    print()
    
    # 2. 学习统计
    print("2️⃣ 学习统计")
    print("-" * 70)
    stats = learner.get_learning_statistics()
    print(f"   总回合数：{stats['total_episodes']}")
    print(f"   总步数：{stats['total_steps']}")
    print(f"   平均奖励：{stats['avg_reward']:.3f}")
    print(f"   当前ε：{stats['current_epsilon']:.3f}")
    print(f"   经验回放：{stats['experience_replay']['size']} 条")
    print()
    
    # 3. 策略评估
    print("3️⃣ 策略评估")
    print("-" * 70)
    test_states = ['learning_scenario', 'optimization_scenario', 'creative_scenario']
    actions = ['analyze', 'plan', 'execute', 'verify', 'improve']
    evaluation = learner.evaluate_policy(test_states, actions)
    print(f"   测试状态：{evaluation['test_states']} 个")
    print(f"   平均 Q 值：{evaluation['avg_q_value']:.3f}")
    for result in evaluation['policy_results']:
        print(f"     {result['state']}: {result['action']} (Q={result['q_value']:.3f})")
    print()
    
    # 4. 模型保存
    print("✅ 模型已保存到：memory/learning/rl_model.json")
