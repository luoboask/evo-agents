#!/usr/bin/env python3
"""
social_simulation.py - 社会模拟系统核心

多 Agent 社会模拟，支持角色创建、自主对话、关系网络、资源经济
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import yaml

# 导入自进化系统（可选）
try:
    from skills.self_evolution.main import evolve as record_evolution
    HAS_SELF_EVOLUTION = True
except ImportError:
    HAS_SELF_EVOLUTION = False


class SocialSimulation:
    """社会模拟器"""
    
    # 角色模板
    ROLE_TEMPLATES = {
        "merchant": {
            "traits": ["精明的", "社交的", "务实的"],
            "goals": ["积累财富", "建立商业网络", "发现商机"],
            "speech_style": "直接、谈利益、喜欢讨价还价"
        },
        "scholar": {
            "traits": ["好奇的", "理性的", "孤僻的"],
            "goals": ["追求真理", "发表研究", "教学传承"],
            "speech_style": "严谨、引用数据、喜欢解释"
        },
        "artist": {
            "traits": ["感性的", "创意的", "情绪化的"],
            "goals": ["创作杰作", "获得认可", "表达自我"],
            "speech_style": "诗意、隐喻、情绪丰富"
        },
        "worker": {
            "traits": ["勤劳的", "实际的", "团结的"],
            "goals": ["稳定收入", "提升技能", "照顾家庭"],
            "speech_style": "朴实、直接、关心生活"
        }
    }
    
    def __init__(self, workspace_dir: str = None):
        self.workspace = Path(workspace_dir) if workspace_dir else Path(__file__).parent.parent.parent
        self.config = self._load_config()
        self.state = self._init_state()
        self.agents = {}
        self.running = False
        
        # 数据目录
        self.data_dir = self.workspace / "data" / "social"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🏛️  社会模拟系统已加载")
        print(f"   工作目录：{self.workspace}")
    
    def _load_config(self) -> dict:
        """加载社会配置"""
        config_file = self.workspace / "config" / "society.yaml"
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {}
    
    def _init_state(self) -> dict:
        """初始化社会状态"""
        return {
            "current_day": 1,
            "current_hour": 8,
            "active_conversations": [],
            "events": [],
            "created_at": datetime.now().isoformat()
        }
    
    def init_society(self, config_path: str = None):
        """初始化社会模拟环境"""
        if config_path:
            with open(config_path) as f:
                self.config = yaml.safe_load(f)
        
        print(f"✅ 社会模拟环境初始化完成")
        print(f"   社会名称：{self.config.get('society', {}).get('name', '未命名')}")
        print(f"   环境：{self.config.get('environment', {}).get('name', '未命名')}")
    
    def join_society(self, role: str, name: str = None, config: dict = None):
        """加入社会，扮演特定角色"""
        if role not in self.ROLE_TEMPLATES:
            raise ValueError(f"未知角色：{role}，可选：{list(self.ROLE_TEMPLATES.keys())}")
        
        # 生成 Agent ID
        agent_id = f"{role}_{len(self.agents) + 1:02d}"
        
        # 使用模板
        template = self.ROLE_TEMPLATES[role]
        agent_config = {
            "id": agent_id,
            "role": role,
            "name": name or f"{role.capitalize()}_{len(self.agents) + 1}",
            "display_name": self._generate_display_name(role),
            "traits": template["traits"],
            "goals": template["goals"],
            "speech_style": template["speech_style"],
            "state": {
                "location": "market_square",
                "status": "idle",
                "resources": self._get_initial_resources(role)
            }
        }
        
        # 覆盖配置
        if config:
            agent_config.update(config)
        
        self.agents[agent_id] = agent_config
        
        print(f"✅ {agent_config['display_name']} 加入社会")
        print(f"   角色：{role}")
        print(f"   性格：{', '.join(template['traits'])}")
        print(f"   目标：{', '.join(template['goals'])}")
        
        # 记录进化事件
        if HAS_SELF_EVOLUTION:
            record_evolution(
                type="SOCIAL_JOIN",
                content=f"加入社会，扮演{role}角色",
                metadata={"agent_id": agent_id, "role": role}
            )
        
        return agent_id
    
    def _generate_display_name(self, role: str) -> str:
        """生成角色显示名称"""
        names = {
            "merchant": "钱老板",
            "scholar": "知教授",
            "artist": "画先生",
            "worker": "工师傅"
        }
        return names.get(role, f"{role.capitalize()}")
    
    def _get_initial_resources(self, role: str) -> dict:
        """获取初始资源"""
        economy = self.config.get("economy", {})
        initial = economy.get("initial_distribution", {})
        
        base_gold = initial.get(role, 500)
        
        return {
            "gold": base_gold,
            "reputation": 50,
            "inventory": []
        }
    
    async def start_simulation(self, speed: int = 1, duration: int = None):
        """启动社会模拟"""
        if not self.agents:
            print("⚠️  请先加入社会（join_society）")
            return
        
        print(f"\n🚀 启动社会模拟")
        print(f"   速度：{speed}x")
        print(f"   时长：{duration or '持续'} 小时")
        print(f"   Agent 数量：{len(self.agents)}")
        
        self.running = True
        
        try:
            hours_run = 0
            while self.running:
                # 运行一个周期
                await self._run_cycle()
                
                hours_run += 1
                if duration and hours_run >= duration:
                    break
                
                # 速度控制
                await asyncio.sleep(1.0 / speed)
        
        except KeyboardInterrupt:
            print("\n⏹️  模拟已停止")
        finally:
            self.running = False
            self._save_state()
    
    async def _run_cycle(self):
        """运行一个社会周期（1 小时）"""
        # 时间推进
        self.state["current_hour"] += 1
        if self.state["current_hour"] >= 24:
            self.state["current_hour"] = 0
            self.state["current_day"] += 1
            self._nightly_cycle()
        
        # Agent 决定行动
        actions = await self._decide_actions()
        
        # 处理对话
        await self._process_dialogues(actions)
        
        # 记录事件
        self._record_actions(actions)
        
        # 保存状态
        self._save_state()
    
    async def _decide_actions(self) -> List[dict]:
        """每个 Agent 决定行动"""
        actions = []
        hour = self.state["current_hour"]
        
        for agent_id, agent in self.agents.items():
            # 根据时间和角色决定行动
            action = self._generate_action(agent, hour)
            actions.append(action)
        
        return actions
    
    def _generate_action(self, agent: dict, hour: int) -> dict:
        """生成 Agent 行动"""
        role = agent["role"]
        
        # 简单的工作/休息逻辑
        if 9 <= hour < 12 or 14 <= hour < 18:
            action_type = "work"
        elif 18 <= hour < 22:
            action_type = "social"
        else:
            action_type = "rest"
        
        return {
            "agent_id": agent["id"],
            "type": action_type,
            "hour": hour,
            "details": {}
        }
    
    async def _process_dialogues(self, actions: List[dict]):
        """处理对话"""
        social_actions = [a for a in actions if a["type"] == "social"]
        
        # 简单实现：随机匹配对话
        if len(social_actions) >= 2:
            for i in range(0, len(social_actions) - 1, 2):
                agent1 = social_actions[i]["agent_id"]
                agent2 = social_actions[i + 1]["agent_id"]
                
                # 生成对话
                dialogue = await self._generate_dialogue(agent1, agent2)
                
                self.state["active_conversations"].append({
                    "participants": [agent1, agent2],
                    "content": dialogue,
                    "timestamp": f"Day {self.state['current_day']} Hour {self.state['current_hour']}"
                })
                
                print(f"   💬 {agent1} ↔ {agent2}")
    
    async def _generate_dialogue(self, agent1_id: str, agent2_id: str) -> List[str]:
        """生成对话内容"""
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        
        # 简单实现：基于角色的模板对话
        dialogues = {
            "merchant": ["最近生意不错，有个买卖想跟你聊聊", "听说你研究出了新东西？"],
            "scholar": ["我最近有个有趣的发现", "从理论上来说，这个问题很有意思"],
            "artist": ["我有了新的创作灵感", "这件作品表达了什么情感？"],
            "worker": ["今天工作挺顺利的", "有什么需要帮忙的吗？"]
        }
        
        return [
            f"{agent1['display_name']}: {dialogues[agent1['role']][0]}",
            f"{agent2['display_name']}: {dialogues[agent2['role']][0]}"
        ]
    
    def _record_actions(self, actions: List[dict]):
        """记录行动"""
        for action in actions:
            event = {
                "day": self.state["current_day"],
                "hour": self.state["current_hour"],
                "agent": action["agent_id"],
                "type": action["type"],
                "details": action.get("details", {})
            }
            self.state["events"].append(event)
    
    def _nightly_cycle(self):
        """每日循环"""
        print(f"\n🌙 第{self.state['current_day']-1}天结束")
        
        # 保存日志
        log_path = self.data_dir / f"day_{self.state['current_day']-1:03d}.json"
        with open(log_path, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
        
        # 清空当日数据
        self.state["events"] = []
        self.state["active_conversations"] = []
    
    def _save_state(self):
        """保存社会状态"""
        with open(self.data_dir / "society_state.json", "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def stop_simulation(self):
        """停止社会模拟"""
        self.running = False
        print("⏹️  社会模拟已停止")
    
    def get_society_status(self) -> dict:
        """获取社会状态"""
        return {
            "day": self.state["current_day"],
            "hour": self.state["current_hour"],
            "agent_count": len(self.agents),
            "agents": [
                {
                    "id": agent["id"],
                    "name": agent["display_name"],
                    "role": agent["role"],
                    "status": agent["state"]["status"],
                    "resources": agent["state"]["resources"]
                }
                for agent in self.agents.values()
            ],
            "active_conversations": len(self.state["active_conversations"]),
            "events_today": len([e for e in self.state["events"] 
                                if e["day"] == self.state["current_day"]])
        }
    
    def observe(self, agent_id: str = None) -> dict:
        """上帝视角观察"""
        if agent_id:
            # 观察特定 Agent
            agent = self.agents.get(agent_id)
            if not agent:
                return {"error": f"Agent {agent_id} 不存在"}
            
            return {
                "agent_id": agent_id,
                "name": agent["display_name"],
                "role": agent["role"],
                "state": agent["state"],
                "summary": f"{agent['display_name']} 正在{agent['state']['status']}"
            }
        else:
            # 观察整体
            status = self.get_society_status()
            return {
                "summary": f"第{status['day']}天 {status['hour']}:00，{status['agent_count']}个 Agent，{status['active_conversations']}个对话",
                "status": status
            }
    
    def generate_narrative(self, day: int = None) -> str:
        """生成叙事报告"""
        if day is None:
            day = self.state["current_day"] - 1
        
        # 读取当日日志
        log_path = self.data_dir / f"day_{day:03d}.json"
        if not log_path.exists():
            return f"第{day}天的日志不存在"
        
        with open(log_path) as f:
            log_data = json.load(f)
        
        # 生成简单叙事
        narrative = f"""
【第{day}天 社会观察报告】

时间：{log_data.get('current_hour', '未知')} 时

今日事件：
"""
        events = log_data.get("events", [])
        if events:
            for event in events[:10]:  # 最多显示 10 个
                narrative += f"- {event['hour']}:00 {event['agent']} {event['type']}\n"
        else:
            narrative += "- 无明显事件\n"
        
        conversations = log_data.get("active_conversations", [])
        if conversations:
            narrative += "\n对话记录：\n"
            for conv in conversations[:5]:  # 最多显示 5 个
                narrative += f"- {conv['participants'][0]} ↔ {conv['participants'][1]}\n"
        
        narrative += "\n明日预测：\n"
        narrative += f"- 社会将继续演化，预计产生更多互动\n"
        
        return narrative


# ═══════════════════════════════════════════════════════════
# 全局实例（单例模式）
# ═══════════════════════════════════════════════════════════

_simulation_instance = None


def _get_simulation() -> SocialSimulation:
    """获取社会模拟实例"""
    global _simulation_instance
    if _simulation_instance is None:
        _simulation_instance = SocialSimulation()
    return _simulation_instance


# ═══════════════════════════════════════════════════════════
# 公开 API（技能接口）
# ═══════════════════════════════════════════════════════════

def init_society(config_path: str = None):
    """初始化社会模拟环境"""
    sim = _get_simulation()
    sim.init_society(config_path)


def join_society(role: str, name: str = None, config: dict = None):
    """加入社会，扮演特定角色"""
    sim = _get_simulation()
    return sim.join_society(role, name, config)


async def start_simulation(speed: int = 1, duration: int = None):
    """启动社会模拟"""
    sim = _get_simulation()
    await sim.start_simulation(speed, duration)


def stop_simulation():
    """停止社会模拟"""
    sim = _get_simulation()
    sim.stop_simulation()


def get_society_status() -> dict:
    """获取社会状态"""
    sim = _get_simulation()
    return sim.get_society_status()


def observe(agent_id: str = None) -> dict:
    """上帝视角观察"""
    sim = _get_simulation()
    return sim.observe(agent_id)


def generate_narrative(day: int = None) -> str:
    """生成叙事报告"""
    sim = _get_simulation()
    return sim.generate_narrative(day)


async def interact_with(agent_id: str, message: str = None, action: str = None):
    """与特定 Agent 互动"""
    # 简化实现
    print(f"🤝 与 {agent_id} 互动")
    if message:
        print(f"   消息：{message}")
    if action:
        print(f"   行动：{action}")


# ═══════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio
    
    async def main():
        # 初始化社会
        init_society()
        
        # 加入社会
        join_society("merchant", name="钱老板")
        join_society("scholar", name="知教授")
        
        # 启动模拟（10 倍速，运行 24 小时）
        await start_simulation(speed=10, duration=24)
        
        # 查看状态
        status = get_society_status()
        print(f"\n📊 社会状态：{status}")
        
        # 生成叙事
        story = generate_narrative()
        print(f"\n📖 叙事报告:\n{story}")
    
    asyncio.run(main())
