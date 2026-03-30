#!/usr/bin/env python3
"""
社会模拟系统 - 快速开始示例

用法:
    python3 skills/social-simulation/examples/quick_start.py
"""

import asyncio
import sys
from pathlib import Path

# 添加技能路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_simulation import (
    init_society,
    join_society,
    start_simulation,
    get_society_status,
    generate_narrative,
    observe
)


async def main():
    print("=" * 60)
    print("🏛️  社会模拟系统 - 快速开始")
    print("=" * 60)
    
    # 1. 初始化社会
    print("\n1️⃣  初始化社会...")
    init_society()
    
    # 2. 创建多个 Agent
    print("\n2️⃣  创建 Agent...")
    join_society("merchant", name="钱老板")
    join_society("scholar", name="知教授")
    join_society("artist", name="画先生")
    join_society("worker", name="工师傅")
    
    # 3. 查看初始状态
    print("\n3️⃣  初始状态:")
    status = get_society_status()
    print(f"   天数：{status['day']}")
    print(f"   时间：{status['hour']}:00")
    print(f"   人口：{status['agent_count']}")
    print(f"\n   Agent 列表:")
    for agent in status['agents']:
        print(f"   - {agent['name']} ({agent['role']})")
        print(f"     金币：{agent['resources']['gold']}, 声誉：{agent['resources']['reputation']}")
    
    # 4. 启动模拟（10 倍速，运行 24 小时）
    print("\n4️⃣  启动模拟（10 倍速，24 小时）...")
    print("   （按 Ctrl+C 可提前停止）")
    
    try:
        await start_simulation(speed=10, duration=24)
    except KeyboardInterrupt:
        print("\n   ⏹️  模拟已停止")
    
    # 5. 最终状态
    print("\n5️⃣  最终状态:")
    status = get_society_status()
    print(f"   天数：{status['day']}")
    print(f"   时间：{status['hour']}:00")
    print(f"   对话：{status['active_conversations']}")
    
    # 6. 观察特定 Agent
    print("\n6️⃣  观察特定 Agent:")
    report = observe("merchant_01")
    print(f"   {report['summary']}")
    
    # 7. 生成叙事报告
    print("\n7️⃣  叙事报告:")
    story = generate_narrative()
    print(story)
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
    print("\n💡 提示:")
    print("   - 修改 config/society.yaml 自定义社会配置")
    print("   - 在 agents/ 目录下创建更多 Agent")
    print("   - 使用 --speed 参数调整模拟速度")
    print("   - 使用 --duration 参数设置模拟时长")


if __name__ == "__main__":
    asyncio.run(main())
