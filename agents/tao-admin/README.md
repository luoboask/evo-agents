# Tao Admin Agent

> 自营电商平台管理 Agent - 海外销售 + 国内采购 + 国际物流

---

## 🎯 业务模式

```
海外销售 → 国内采购 → 国际物流 → 海外配送
   ↓          ↓          ↓          ↓
商品管理   采购管理   物流管理   订单管理
   ↓          ↓          ↓          ↓
库存管理 ← 供应链管理 ← 仓储管理 ← 配送管理
```

---

## 📊 核心功能

### 1. 商品管理
- 商品上架/下架
- 价格管理
- 商品分类
- 商品描述优化

### 2. 采购管理
- 供应商管理
- 采购订单
- 采购成本核算
- 供应商评估

### 3. 物流管理
- 国内物流（供应商→仓库）
- 国际物流（仓库→海外）
- 物流成本优化
- 物流时效监控

### 4. 库存管理
- 库存监控
- 库存预警
- 库存周转分析
- 滞销品处理

### 5. 订单管理
- 订单处理
- 订单跟踪
- 售后服务
- 客户反馈

### 6. 财务管理
- 成本核算
- 利润分析
- 现金流管理
- 财务报表

---

## 🚀 快速开始

### 创建 Agent（独立数据库）

```python
from memory_stream import MemoryStream
from knowledge_base import KnowledgeBase
from self_evolution_real import RealSelfEvolution

# tao-admin 使用独立数据库（数据隔离）
tao_memory = MemoryStream(agent_id='tao-admin')
tao_kb = KnowledgeBase(agent_id='tao-admin')
tao_evolution = RealSelfEvolution(agent_id='tao-admin')
```

### 记录业务事件

```python
# 记录商品上架
tao_evolution.record_evolution(
    event_type='PRODUCT_LISTED',
    description='上架新品：无线蓝牙耳机',
    lesson_learned='新品上架需要准备充足库存',
    files_changed=['products/wireless-earbuds.json']
)

# 记录采购订单
tao_evolution.record_evolution(
    event_type='PURCHASE_ORDER',
    description='向供应商 A 采购 1000 件商品',
    lesson_learned='提前 30 天下单避免断货',
    files_changed=['purchases/po-2026-001.json']
)

# 记录物流问题
tao_evolution.record_evolution(
    event_type='LOGISTICS_ISSUE',
    description='国际物流延误 5 天',
    lesson_learned='需要备选物流方案',
    files_changed=['logistics/shipment-001.json']
)
```

### 获取业务建议

```python
# 基于历史经验获取建议
suggestions = tao_evolution.get_suggestions_for_category('采购')

# 获取常见问题
common_issues = tao_evolution.get_common_issues_for_category('物流')
```

---

## 📊 数据隔离

**tao-admin 使用独立数据库：**

| 数据库 | 文件 | 用途 |
|--------|------|------|
| 记忆流 | `tao-admin_memory_stream.db` | tao 的业务记忆 |
| 知识库 | `tao-admin_knowledge_base.db` | tao 的业务知识 |
| 进化事件 | `tao-admin_evolution.db` | tao 的业务事件 |

**与其他 Agent 完全隔离：**
- ✅ main-agent 无法访问 tao 的数据
- ✅ sandbox-agent 无法访问 tao 的数据
- ✅ tao 的数据独立管理

---

## 🎯 使用场景

### 场景 1: 新品上架决策

```python
# 查询历史销售数据
history = tao_memory.retrieve_by_relevance('无线耳机 销售')

# 获取采购建议
suggestions = get_procurement_suggestions('无线耳机')

# 决策：上架 + 采购数量
decision = {
    'action': 'list_product',
    'product': '无线蓝牙耳机',
    'initial_stock': 500,
    'reorder_point': 100
}
```

### 场景 2: 库存预警

```python
# 监控库存水平
low_stock = monitor_inventory()

# 自动触发采购
if low_stock:
    create_purchase_order(low_stock)
    record_event('AUTO_REORDER', {...})
```

### 场景 3: 物流优化

```python
# 分析物流时效
logistics_performance = analyze_logistics()

# 选择最优物流方案
best_option = select_best_logistics(logistics_performance)

# 记录经验
record_event('LOGISTICS_OPTIMIZED', {
    'from': '物流商 A',
    'to': '物流商 B',
    'reason': '时效提升 30%'
})
```

---

## 📁 文件结构

```
agents/tao-admin/
├── README.md           # 本文档
├── agent.py            # Agent 主程序
├── modules/            # 业务模块
│   ├── product.py      # 商品管理
│   ├── purchase.py     # 采购管理
│   ├── logistics.py    # 物流管理
│   ├── inventory.py    # 库存管理
│   ├── order.py        # 订单管理
│   └── finance.py      # 财务管理
└── config.yaml         # 配置文件
```

---

## ✅ 总结

**tao-admin Agent 特点：**

| 特性 | 说明 |
|------|------|
| 🏪 电商平台 | 自营电商平台管理 |
| 🌍 跨境业务 | 国内采购 + 海外销售 |
| 📦 全链路 | 采购→物流→销售→配送 |
| 🔒 数据隔离 | 独立数据库，不共享 |
| 🧠 自进化 | 从业务中学习经验 |

**tao-admin 是 tao 电商平台的智能管理 Agent！** 🎉
