# -*- coding: utf-8 -*-
"""
电商运营领域插件
E-commerce Operations Domain Plugin

适用于：电商网站开发、运营管理、营销活动策划等
"""

from typing import List, Dict


class EcommerceOperationsPlugin:
    """电商运营领域插件"""
    
    name = 'ecommerce-operations'
    description = '电商运营 - 网站开发/商品管理/订单处理/营销策划'
    version = '1.0.0'
    
    def get_decomposition_template(self) -> str:
        """任务分解模板"""
        return """
请按以下步骤分解电商运营任务：

1. **需求分析与目标设定**
   - 业务目标（GMV/转化率/用户增长）
   - 目标用户画像
   - 竞品分析
   - 核心指标定义（KPI）

2. **技术架构设计**（如涉及开发）
   - 技术栈选择（前端/后端/数据库）
   - 系统架构（单体/微服务）
   - 第三方集成（支付/物流/ERP）
   - 性能与安全要求

3. **商品与供应链管理**
   - 商品类目规划
   - SKU 管理策略
   - 库存管理方案
   - 供应商对接

4. **营销活动策划**
   - 活动主题与时间
   - 促销方式（满减/折扣/秒杀）
   - 渠道投放计划
   - 预算分配

5. **用户体验优化**
   - 购物流程设计
   - 页面转化优化
   - 客服体系搭建
   - 售后流程

6. **数据分析体系**
   - 数据埋点规划
   - 核心报表设计
   - A/B 测试方案
   - 用户行为分析
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """验收标准"""
        return [
            "业务目标明确：有清晰的 GMV/转化率等目标",
            "技术方案可行：架构设计合理，能支撑预期流量",
            "支付集成完整：支持主流支付方式（支付宝/微信/银联）",
            "订单流程闭环：下单→支付→发货→确认→评价全流程通畅",
            "数据安全合规：用户信息加密，符合 GDPR/网络安全法",
            "性能达标：页面加载<3 秒，支持并发访问",
            "移动端适配：响应式设计或独立 APP",
            "数据可追踪：关键行为有埋点，数据可分析"
        ]
    
    def get_executor_tools(self) -> List[str]:
        """执行者可用的工具"""
        return [
            "电商平台框架（Shopify/Magento/WooCommerce/有赞）",
            "支付网关（Stripe/支付宝 SDK/微信支付 SDK）",
            "ERP 系统（聚水潭/万里牛/管易云）",
            "物流 API（顺丰/圆通/菜鸟网络）",
            "数据分析工具（Google Analytics/神策数据/GrowingIO）",
            "营销自动化工具（HubSpot/Marketo）",
            "A/B 测试工具（Optimizely/VWO）",
            "客服系统（Zendesk/七鱼/智齿科技）"
        ]
    
    def get_best_practices(self) -> List[str]:
        """最佳实践"""
        return [
            "移动优先：70%+流量来自移动端",
            "简化结账：减少结账步骤，提供游客购买",
            "信任建设：展示安全认证、用户评价、退换货政策",
            "个性化推荐：基于浏览历史和购买记录推荐商品",
            "社交证明：展示销量、好评、KOL 推荐",
            "紧急性营造：限时优惠、库存紧张提示",
            "多渠道整合：线上 + 线下 + 社交媒体全渠道",
            "数据驱动决策：所有优化基于数据而非直觉"
        ]
    
    def get_check_method(self, criterion: str):
        """获取特定标准的检查方法"""
        check_methods = {
            '支付集成完整': self._check_payment_integration,
            '订单流程闭环': self._check_order_flow,
            '性能达标': self._check_performance,
            '移动端适配': self._check_mobile_responsive,
        }
        return check_methods.get(criterion, self._default_check)
    
    async def _check_payment_integration(self, results: Dict) -> Dict:
        """检查支付集成"""
        payment_methods = results.get('payment_methods', [])
        
        required_methods = ['支付宝', '微信支付']
        supported = [m for m in required_methods if m in payment_methods]
        
        score = len(supported) / len(required_methods) * 100
        
        return {
            'passed': score >= 100,
            'score': score,
            'reason': f'支持{len(supported)}/{len(required_methods)}种主流支付方式',
            'suggestion': f'建议添加{"、".join(set(required_methods) - set(supported))}' if score < 100 else ''
        }
    
    async def _check_order_flow(self, results: Dict) -> Dict:
        """检查订单流程"""
        flow_steps = results.get('order_flow_steps', [])
        required_steps = ['下单', '支付', '发货', '确认', '评价']
        
        completed = sum(1 for step in required_steps if step in flow_steps)
        score = (completed / len(required_steps)) * 100
        
        return {
            'passed': score >= 100,
            'score': score,
            'reason': f'订单流程完成{completed}/{len(required_steps)}个关键步骤',
            'suggestion': f'建议补充{"、".join(set(required_steps) - set(flow_steps))}' if score < 100 else ''
        }
    
    async def _check_performance(self, results: Dict) -> Dict:
        """检查性能指标"""
        page_load_time = results.get('page_load_time', 5)  # 秒
        concurrent_users = results.get('concurrent_users', 100)
        
        score = 0
        if page_load_time <= 3:
            score += 50
        elif page_load_time <= 5:
            score += 30
        
        if concurrent_users >= 1000:
            score += 50
        elif concurrent_users >= 500:
            score += 30
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'页面加载{page_load_time}秒，并发{concurrent_users}用户',
            'suggestion': '优化图片、启用 CDN、数据库索引' if not passed else ''
        }
    
    async def _check_mobile_responsive(self, results: Dict) -> Dict:
        """检查移动端适配"""
        is_responsive = results.get('mobile_responsive', False)
        has_app = results.get('has_mobile_app', False)
        
        score = 0
        if is_responsive:
            score += 60
        if has_app:
            score += 40
        
        passed = score >= 60
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'响应式设计：{"是" if is_responsive else "否"}, 独立 APP: {"有" if has_app else "无"}',
            'suggestion': '必须实现响应式设计，考虑开发小程序或 APP' if not passed else ''
        }
    
    async def _default_check(self, results: Dict) -> Dict:
        """默认检查方法"""
        return {
            'passed': True,
            'score': 80,
            'reason': '符合要求',
            'suggestion': ''
        }
    
    def get_platform_config(self, platform_type: str) -> Dict:
        """获取特定平台配置"""
        platforms = {
            'shopify': {
                'name': 'Shopify',
                'type': 'SaaS',
                'monthly_fee': '$29-$299',
                'transaction_fee': '0.5%-2%',
                'best_for': '中小卖家，快速建站',
                'integrations': ['PayPal', 'Stripe', 'Facebook Shop']
            },
            'magento': {
                'name': 'Magento (Adobe Commerce)',
                'type': '开源/企业版',
                'monthly_fee': '免费/¥15 万+/年',
                'transaction_fee': '无',
                'best_for': '中大型企业，高度定制',
                'integrations': ['PayPal', 'Braintree', 'ERP']
            },
            'youzan': {
                'name': '有赞',
                'type': 'SaaS',
                'monthly_fee': '¥6800/年起',
                'transaction_fee': '0.6%',
                'best_for': '微信生态，社交电商',
                'integrations': ['微信支付', '小程序', '公众号']
            }
        }
        
        return platforms.get(platform_type, {})


def load_plugin():
    """加载插件实例"""
    return EcommerceOperationsPlugin()


if __name__ == '__main__':
    plugin = EcommerceOperationsPlugin()
    
    print("=" * 60)
    print(f"插件：{plugin.name}")
    print(f"描述：{plugin.description}")
    print("=" * 60)
    
    print("\n📋 任务分解模板:")
    print(plugin.get_decomposition_template()[:500] + "...")
    
    print("\n✅ 验收标准:")
    for i, criterion in enumerate(plugin.get_acceptance_criteria(), 1):
        print(f"  {i}. {criterion}")
    
    print("\n🛠️ 可用工具 (前 5 个):")
    for tool in plugin.get_executor_tools()[:5]:
        print(f"  - {tool}")
    
    print("\n💡 最佳实践 (前 5 条):")
    for practice in plugin.get_best_practices()[:5]:
        print(f"  - {practice}")
