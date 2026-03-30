"""
social-simulation - 多 Agent 社会模拟系统

让 Agent 自主对话、协作、发展剧情
"""

from .social_simulation import (
    init_society,
    join_society,
    start_simulation,
    stop_simulation,
    get_society_status,
    observe,
    generate_narrative,
    interact_with,
    SocialSimulation
)

__version__ = "1.0.0"
__all__ = [
    "init_society",
    "join_society",
    "start_simulation",
    "stop_simulation",
    "get_society_status",
    "observe",
    "generate_narrative",
    "interact_with",
    "SocialSimulation"
]
