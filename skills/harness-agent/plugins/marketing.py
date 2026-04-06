# -*- coding: utf-8 -*-
"""
Marketing Plugin - 营销策划插件

简洁版设计 / Simple design
适用于：营销活动、社交媒体、内容营销、品牌推广
"""

from typing import List, Dict


class MarketingPlugin:
    """营销策划领域插件"""
    
    name = 'marketing'
    description = 'Marketing - Campaigns, Social Media, Content, Branding'
    version = '1.0.0'
    
    def get_task_template(self) -> str:
        """任务分解模板"""
        return """
## 营销策划任务分解

1. **市场调研** - 目标用户、竞品分析、市场定位
2. **目标设定** - SMART 原则 (具体/可衡量/可实现/相关/时限)
3. **策略制定** - 渠道选择、内容规划、预算分配
4. **内容创作** - 文案、设计、视频制作
5. **执行投放** - 排期、监控、优化调整
6. **效果评估** - ROI 分析、数据复盘、经验总结
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """验收标准"""
        return [
            "✅ 目标清晰可衡量 (SMART)",
            "✅ 渠道选择合理匹配目标用户",
            "✅ 内容质量高且一致",
            "✅ 预算分配高效",
            "✅ 数据追踪完整",
            "✅ ROI 达到预期 (>3:1)"
        ]
    
    def get_tools(self) -> List[Dict]:
        """可用工具"""
        return [
            {
                "name": "plan_campaign",
                "desc": "策划营销活动",
                "params": ["campaign_name", "goals", "budget", "timeline"],
                "safe": False
            },
            {
                "name": "create_content",
                "desc": "创作营销内容",
                "params": ["content_type", "platform", "message"],
                "safe": False
            },
            {
                "name": "schedule_posts",
                "desc": "排期发布内容",
                "params": ["posts", "schedule", "platforms"],
                "safe": False
            },
            {
                "name": "analyze_performance",
                "desc": "分析营销效果",
                "params": ["campaign_id", "metrics", "date_range"],
                "safe": True  # 只读分析
            },
            {
                "name": "manage_ads",
                "desc": "管理广告投放",
                "params": ["platform", "budget", "target_audience"],
                "safe": False
            },
            {
                "name": "track_roi",
                "desc": "追踪投资回报率",
                "params": ["campaign_id", "cost", "revenue"],
                "safe": True
            }
        ]
    
    def get_channel_recommendations(self, target_audience: str) -> Dict:
        """渠道推荐"""
        channels = {
            'young_gen_z': {
                'primary': ['抖音', 'B 站', '小红书'],
                'content_types': ['短视频', '直播', '图文笔记'],
                'best_posting_time': '19:00-22:00',
                'avg_cpm': '¥20-50'
            },
            'professionals': {
                'primary': ['LinkedIn', '知乎', '微信公众号'],
                'content_types': ['专业文章', '行业报告', '线上讲座'],
                'best_posting_time': '工作日 8:00-9:00, 20:00-21:00',
                'avg_cpm': '¥50-100'
            },
            'mass_market': {
                'primary': ['微信朋友圈', '微博', '快手'],
                'content_types': ['图文', '短视频', 'H5 互动'],
                'best_posting_time': '12:00-13:00, 20:00-22:00',
                'avg_cpm': '¥15-30'
            }
        }
        return channels.get(target_audience, channels['mass_market'])
    
    def get_campaign_templates(self, campaign_type: str) -> Dict:
        """活动模板"""
        templates = {
            'product_launch': {
                'name': '新品发布会',
                'phases': [
                    '预热期 (T-7): 悬念营销，KOL 种草',
                    '发布期 (T+0): 直播发布，限时优惠',
                    '延续期 (T+7): 用户晒单，口碑传播'
                ],
                'kpis': ['曝光量', '预约数', '首日销量'],
                'budget_split': {'ads': '50%', 'kol': '30%', 'content': '20%'}
            },
            'festival_promotion': {
                'name': '节日促销',
                'phases': [
                    '预热：优惠券发放，购物车提醒',
                    '爆发：限时折扣，满减活动',
                    '返场：余热促销，好评返现'
                ],
                'kpis': ['GMV', '转化率', '客单价'],
                'budget_split': {'ads': '60%', 'discount': '30%', 'design': '10%'}
            },
            'brand_awareness': {
                'name': '品牌宣传',
                'phases': [
                    '故事包装：品牌故事，价值观传递',
                    '内容传播：软文，视频，话题营销',
                    '口碑建设：用户评价，媒体背书'
                ],
                'kpis': ['品牌提及度', '搜索指数', '粉丝增长'],
                'budget_split': {'content': '50%', 'pr': '30%', 'ads': '20%'}
            }
        }
        return templates.get(campaign_type, {})
    
    def get_best_practices(self) -> List[str]:
        """最佳实践"""
        return [
            "🎯 明确目标受众，精准营销",
            "📊 数据驱动决策，A/B 测试一切",
            "💬 与用户互动，建立社区",
            "🎨 保持品牌一致性",
            "⏰ 把握发布时间窗口",
            "📈 持续优化，关注 ROI"
        ]


def load_plugin():
    """加载插件"""
    return MarketingPlugin()


if __name__ == '__main__':
    plugin = MarketingPlugin()
    
    print("=" * 60)
    print(f"插件：{plugin.name}")
    print(f"描述：{plugin.description}")
    print("=" * 60)
    
    print("\n🛠️ 可用工具:")
    for tool in plugin.get_tools():
        safe_icon = "✅" if tool['safe'] else "⚠️"
        print(f"  {safe_icon} {tool['name']} - {tool['desc']}")
    
    print("\n📱 渠道推荐:")
    for audience in ['young_gen_z', 'professionals']:
        recs = plugin.get_channel_recommendations(audience)
        print(f"\n  {audience}:")
        print(f"    主要渠道：{', '.join(recs['primary'])}")
        print(f"    最佳时间：{recs['best_posting_time']}")
    
    print("\n🎉 活动模板:")
    for template_type in ['product_launch', 'festival_promotion']:
        template = plugin.get_campaign_templates(template_type)
        if template:
            print(f"\n  {template.get('name')}:")
            print(f"    KPIs: {', '.join(template.get('kpis', []))}")
    
    print("\n💡 最佳实践:")
    for practice in plugin.get_best_practices():
        print(f"  {practice}")
