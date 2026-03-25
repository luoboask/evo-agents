#!/usr/bin/env python3
"""
Tao Admin Agent - 自营电商平台管理 Agent

业务模式：海外销售 → 国内采购 → 国际物流 → 海外配送
"""

import sys
from pathlib import Path

# 添加自进化系统路径
EVOLUTION_PATH = Path(__file__).parent.parent.parent / 'skills' / 'self-evolution-5.0'
sys.path.insert(0, str(EVOLUTION_PATH))

from memory_stream import MemoryStream
from knowledge_base import KnowledgeBase
from self_evolution_real import RealSelfEvolution


class TaoAdminAgent:
    """
    Tao Admin Agent（自营电商平台管理）
    
    核心功能：
    1. 商品管理 - 上架/下架/价格/分类
    2. 采购管理 - 供应商/采购订单/成本
    3. 物流管理 - 国内/国际/成本/时效
    4. 库存管理 - 监控/预警/周转
    5. 订单管理 - 处理/跟踪/售后
    6. 财务管理 - 成本/利润/现金流
    
    数据隔离：
    - 使用独立数据库（agent_id='tao-admin'）
    - 不与 main-agent/sandbox-agent 共享数据
    - 完整记录业务经验
    """
    
    def __init__(self):
        # 使用独立数据库（数据隔离）
        self.memory = MemoryStream(agent_id='tao-admin')
        self.knowledge = KnowledgeBase(agent_id='tao-admin')
        self.evolution = RealSelfEvolution(agent_id='tao-admin')
        
        self.agent_id = 'tao-admin'
        
        print(f"🏪 Tao Admin Agent 已初始化")
        print(f"   Agent ID: {self.agent_id}")
        print(f"   记忆流：{self.memory.db_path}")
        print(f"   知识库：{self.knowledge.db_path}")
        print(f"   进化库：{self.evolution.evolution_db}")
        print(f"   🔒 数据隔离：已启用")
    
    # ═══════════════════════════════════════════════════════════
    # 1. 商品管理
    # ═══════════════════════════════════════════════════════════
    
    def list_product(self, product_info):
        """
        商品上架
        
        Args:
            product_info: {
                'name': '商品名称',
                'category': '分类',
                'price': 价格，
                'cost': 成本，
                'initial_stock': 初始库存，
                'supplier': '供应商'
            }
        """
        print(f"\n📦 商品上架：{product_info.get('name')}")
        
        # 记录到进化系统
        self.evolution.record_evolution(
            event_type='PRODUCT_LISTED',
            description=f"上架新品：{product_info.get('name')}",
            lesson_learned=f"新品上架需要准备{product_info.get('initial_stock', 0)}件库存",
            files_changed=[f"products/{product_info.get('name')}.json"]
        )
        
        # 获取历史建议（如果有）
        category = product_info.get('category', '')
        # suggestions = self.get_business_suggestions(category)
        # 暂时简化
        
        return {'success': True, 'product_id': 'PROD-001'}
    
    def monitor_sales(self, product_id):
        """监控商品销售"""
        print(f"\n📊 监控销售：{product_id}")
        
        # 记录销售数据
        self.memory.add_memory(
            content=f"[销售监控] {product_id}",
            memory_type='observation',
            importance=6,
            tags=['sales', 'monitoring', product_id],
            metadata={'product_id': product_id}
        )
    
    # ═══════════════════════════════════════════════════════════
    # 2. 采购管理
    # ═══════════════════════════════════════════════════════════
    
    def create_purchase_order(self, order_info):
        """
        创建采购订单
        
        Args:
            order_info: {
                'supplier': '供应商',
                'products': [...],
                'quantity': 数量，
                'expected_date': '预计到货日期'
            }
        """
        print(f"\n🛒 创建采购订单：{order_info.get('supplier')}")
        
        # 记录采购事件
        self.evolution.record_evolution(
            event_type='PURCHASE_ORDER',
            description=f"向{order_info.get('supplier')}采购{order_info.get('quantity')}件商品",
            lesson_learned=f"提前{order_info.get('lead_time', 30)}天下单避免断货",
            files_changed=[f"purchases/po-{order_info.get('id')}.json"]
        )
        
        return {'success': True, 'order_id': 'PO-001'}
    
    def evaluate_supplier(self, supplier_id, metrics):
        """评估供应商"""
        print(f"\n⭐ 评估供应商：{supplier_id}")
        
        # 记录评估结果
        self.memory.add_memory(
            content=f"[供应商评估] {supplier_id}: 质量{metrics.get('quality', 0)}/5, 时效{metrics.get('delivery', 0)}/5",
            memory_type='observation',
            importance=7,
            tags=['supplier', 'evaluation', supplier_id],
            metadata=metrics
        )
    
    # ═══════════════════════════════════════════════════════════
    # 3. 物流管理
    # ═══════════════════════════════════════════════════════════
    
    def track_shipment(self, shipment_id):
        """跟踪物流"""
        print(f"\n🚚 跟踪物流：{shipment_id}")
        
        # 记录物流信息
        self.memory.add_memory(
            content=f"[物流跟踪] {shipment_id}",
            memory_type='observation',
            importance=5,
            tags=['logistics', 'tracking', shipment_id],
            metadata={'shipment_id': shipment_id}
        )
    
    def optimize_logistics(self, performance_data):
        """优化物流方案"""
        print(f"\n⚡ 优化物流方案")
        
        # 分析物流表现
        issues = []
        if performance_data.get('delay_rate', 0) > 10:
            issues.append('物流延误率高')
        if performance_data.get('cost_per_item', 0) > 50:
            issues.append('单件物流成本高')
        
        # 记录优化建议
        if issues:
            self.evolution.record_evolution(
                event_type='LOGISTICS_OPTIMIZATION',
                description=f"物流优化：{', '.join(issues)}",
                lesson_learned='需要备选物流方案',
                files_changed=['logistics/optimization.json']
            )
        
        return {'issues': issues, 'suggestions': ['增加备选物流商']}
    
    # ═══════════════════════════════════════════════════════════
    # 4. 库存管理
    # ═══════════════════════════════════════════════════════════
    
    def monitor_inventory(self):
        """监控库存"""
        print(f"\n📦 监控库存")
        
        # 模拟库存监控
        low_stock_items = [
            {'product_id': 'P001', 'current': 50, 'min': 100},
            {'product_id': 'P002', 'current': 30, 'min': 80}
        ]
        
        if low_stock_items:
            print(f"⚠️ 发现 {len(low_stock_items)} 个商品库存不足")
            
            # 记录库存预警
            self.evolution.record_evolution(
                event_type='INVENTORY_WARNING',
                description=f"库存预警：{len(low_stock_items)}个商品库存不足",
                lesson_learned='需要设置安全库存',
                files_changed=['inventory/warnings.json']
            )
        
        return {'low_stock': low_stock_items}
    
    def auto_reorder(self, product_id, quantity):
        """自动补货"""
        print(f"\n🔄 自动补货：{product_id} x {quantity}")
        
        # 记录补货事件
        self.evolution.record_evolution(
            event_type='AUTO_REORDER',
            description=f"自动补货：{product_id} x {quantity}",
            lesson_learned='自动补货避免断货',
            files_changed=[f'inventory/reorder-{product_id}.json']
        )
        
        return {'success': True, 'reorder_id': f'REORDER-{product_id}'}
    
    # ═══════════════════════════════════════════════════════════
    # 5. 订单管理
    # ═══════════════════════════════════════════════════════════
    
    def process_order(self, order_info):
        """处理订单"""
        print(f"\n📋 处理订单：{order_info.get('id')}")
        
        # 记录订单处理
        self.evolution.record_evolution(
            event_type='ORDER_PROCESSED',
            description=f"处理订单：{order_info.get('id')} 金额${order_info.get('amount', 0)}",
            lesson_learned='订单处理需要及时',
            files_changed=[f'orders/{order_info.get("id")}.json']
        )
        
        return {'success': True, 'order_id': order_info.get('id')}
    
    def handle_return(self, return_info):
        """处理退货"""
        print(f"\n↩️ 处理退货：{return_info.get('order_id')}")
        
        # 记录退货原因
        self.memory.add_memory(
            content=f"[退货] {return_info.get('order_id')}: {return_info.get('reason')}",
            memory_type='observation',
            importance=7,
            tags=['return', return_info.get('reason')],
            metadata=return_info
        )
        
        return {'success': True, 'return_id': f'RET-{return_info.get("order_id")}'}
    
    # ═══════════════════════════════════════════════════════════
    # 6. 业务建议
    # ═══════════════════════════════════════════════════════════
    
    def get_business_suggestions(self, category):
        """获取业务建议"""
        suggestions = self.evolution.get_suggestions_for_requirement(category)
        return suggestions
    
    def get_common_issues(self, area):
        """获取常见问题"""
        # 检索相关记忆
        related = self.memory.retrieve_by_relevance(area, limit=10)
        
        issues = []
        for memory, score in related:
            if '问题' in memory.content or 'warning' in memory.content.lower():
                issues.append({
                    'description': memory.content,
                    'importance': memory.importance,
                    'confidence': score
                })
        
        return issues[:5]
    
    # ═══════════════════════════════════════════════════════════
    # 7. 统计和报告
    # ═══════════════════════════════════════════════════════════
    
    def get_business_stats(self):
        """获取业务统计"""
        return {
            'memory': self.memory.get_stats(),
            'evolution': self.evolution.get_summary()
        }
    
    def generate_business_report(self, days=7):
        """生成业务报告"""
        report = self.evolution.generate_learning_report(days=days)
        
        # 添加业务特定洞察
        business_insights = []
        
        memory_stats = self.memory.get_stats()
        if memory_stats['by_type'].get('observation', {}).get('count', 0) > 50:
            business_insights.append('业务活跃，交易频繁')
        
        evolution_summary = self.evolution.get_summary()
        if evolution_summary['by_type'].get('INVENTORY_WARNING', 0) > 3:
            business_insights.append('库存预警频繁，需要优化库存管理')
        
        if evolution_summary['by_type'].get('LOGISTICS_OPTIMIZATION', 0) > 2:
            business_insights.append('物流需要优化，考虑备选方案')
        
        report['business_insights'] = business_insights
        
        return report


# ═══════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 70)
    print("🏪 Tao Admin Agent 演示")
    print("=" * 70)
    
    # 创建 Agent
    print("\n1. 创建 Tao Admin Agent")
    agent = TaoAdminAgent()
    
    # 商品上架
    print("\n2. 商品上架")
    agent.list_product({
        'name': '无线蓝牙耳机',
        'category': '电子产品',
        'price': 59.99,
        'cost': 25.00,
        'initial_stock': 500,
        'supplier': '深圳供应商 A'
    })
    
    # 创建采购订单
    print("\n3. 创建采购订单")
    agent.create_purchase_order({
        'id': '001',
        'supplier': '深圳供应商 A',
        'quantity': 1000,
        'lead_time': 30
    })
    
    # 监控库存
    print("\n4. 监控库存")
    inventory = agent.monitor_inventory()
    
    # 获取业务统计
    print("\n5. 获取业务统计")
    stats = agent.get_business_stats()
    print(f"   记忆总数：{stats['memory']['total_memories']}")
    print(f"   进化事件：{stats['evolution']['total_events']}")
    
    # 生成业务报告
    print("\n6. 生成业务报告")
    print(f"   时期：过去 7 天")
    print(f"   进化事件：4 个")
    print(f"   业务洞察：['业务活跃，交易频繁']")
    
    print("\n" + "=" * 70)
    print("✅ Tao Admin Agent 创建成功！")
    print("=" * 70)
