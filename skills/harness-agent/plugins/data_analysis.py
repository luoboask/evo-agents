# -*- coding: utf-8 -*-
"""
Data Analysis Plugin - 数据分析插件

简洁版设计 / Simple design
适用于：业务数据分析、BI 报表、用户行为分析、数据可视化
"""

from typing import List, Dict


class DataAnalysisPlugin:
    """数据分析领域插件"""
    
    name = 'data_analysis'
    description = 'Data analysis - BI/Statistics/Visualization/Insights'
    version = '1.0.0'
    
    def get_task_template(self) -> str:
        """任务分解模板"""
        return """
## 数据分析任务分解

1. **问题定义** - 业务问题、分析目标、成功标准
2. **数据收集** - 数据源识别、数据采集、数据质量评估
3. **数据清洗** - 缺失值处理、异常值检测、格式标准化
4. **探索性分析** - 描述统计、分布分析、相关性分析
5. **深度分析** - 假设检验、回归分析、聚类分析
6. **可视化呈现** - 图表选择、仪表板设计、报告撰写
7. **洞察提炼** - 关键发现、行动建议、后续追踪
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """验收标准"""
        return [
            "✅ 数据完整性 >95%",
            "✅ 分析方法合适 (统计检验通过)",
            "✅ 结论有数据支持 (非主观臆断)",
            "✅ 可视化清晰易懂",
            "✅ 洞察可执行 (具体建议)",
            "✅ 报告逻辑连贯"
        ]
    
    def get_tools(self) -> List[Dict]:
        """可用工具"""
        return [
            {
                "name": "query_data",
                "desc": "查询数据 (SQL/API)",
                "params": ["source", "query", "date_range"],
                "safe": True  # 只读查询
            },
            {
                "name": "clean_data",
                "desc": "数据清洗 (去重/填充/格式化)",
                "params": ["dataset", "operations"],
                "safe": False  # 会修改数据
            },
            {
                "name": "analyze_statistics",
                "desc": "统计分析 (描述统计/假设检验)",
                "params": ["dataset", "metrics", "test_type"],
                "safe": True
            },
            {
                "name": "create_visualization",
                "desc": "创建可视化 (图表/仪表板)",
                "params": ["data", "chart_type", "dimensions"],
                "safe": False  # 创建文件
            },
            {
                "name": "generate_report",
                "desc": "生成分析报告",
                "params": ["findings", "recommendations", "format"],
                "safe": False  # 创建文件
            },
            {
                "name": "ab_test_analysis",
                "desc": "A/B 测试分析",
                "params": ["control_group", "test_group", "metric"],
                "safe": True
            }
        ]
    
    def get_analysis_frameworks(self, analysis_type: str) -> Dict:
        """分析框架推荐"""
        frameworks = {
            'cohort': {
                'name': '同期群分析 (Cohort Analysis)',
                'purpose': '追踪不同时期用户的行为差异',
                'metrics': ['留存率', 'LTV', '转化率'],
                'tools': ['SQL', 'Python pandas', 'Mixpanel'],
                'output': '同期群热力图'
            },
            'funnel': {
                'name': '漏斗分析 (Funnel Analysis)',
                'purpose': '识别转化流程中的流失点',
                'metrics': ['各步骤转化率', '平均转化时间'],
                'tools': ['Google Analytics', '神策数据', 'SQL'],
                'output': '漏斗转化图'
            },
            'rfm': {
                'name': 'RFM 分析 (用户价值分层)',
                'purpose': '根据消费行为划分用户价值',
                'metrics': ['最近购买时间', '购买频率', '消费金额'],
                'tools': ['SQL', 'Python', 'Excel'],
                'output': '用户分层矩阵'
            },
            'attribution': {
                'name': '归因分析 (Attribution Analysis)',
                'purpose': '确定各渠道对转化的贡献',
                'models': ['首次点击', '末次点击', '线性归因', '时间衰减'],
                'tools': ['Google Analytics', 'AppsFlyer'],
                'output': '渠道贡献度分析'
            }
        }
        return frameworks.get(analysis_type, {})
    
    def get_best_practices(self) -> List[str]:
        """最佳实践"""
        return [
            "🎯 先问 Why，再问 What - 理解业务背景",
            "📊 数据质量优先 - Garbage In, Garbage Out",
            "📈 可视化少即是多 - 一张图一个核心信息",
            "📝 用数据讲故事 - 问题→分析→洞察→建议",
            "⚠️ 避免因果谬误 - 相关不等于因果",
            "🔍 考虑基率 - 不要忽略基础概率"
        ]


def load_plugin():
    """加载插件"""
    return DataAnalysisPlugin()


if __name__ == '__main__':
    plugin = DataAnalysisPlugin()
    
    print("=" * 60)
    print(f"插件：{plugin.name}")
    print(f"描述：{plugin.description}")
    print("=" * 60)
    
    print("\n🛠️ 可用工具:")
    for tool in plugin.get_tools():
        safe_icon = "✅" if tool['safe'] else "⚠️"
        print(f"  {safe_icon} {tool['name']} - {tool['desc']}")
    
    print("\n📊 分析框架推荐:")
    for fw_type in ['cohort', 'funnel', 'rfm']:
        fw = plugin.get_analysis_frameworks(fw_type)
        print(f"\n  {fw.get('name')}:")
        print(f"    用途：{fw.get('purpose')}")
        print(f"    指标：{', '.join(fw.get('metrics', []))}")
    
    print("\n💡 最佳实践:")
    for practice in plugin.get_best_practices():
        print(f"  {practice}")
