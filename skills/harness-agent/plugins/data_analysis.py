# -*- coding: utf-8 -*-
"""
数据分析领域插件
Data Analysis Domain Plugin

适用于：数据分析、BI 报表、用户行为分析、业务洞察等
"""

from typing import List, Dict


class DataAnalysisPlugin:
    """数据分析领域插件"""
    
    name = 'data-analysis'
    description = '数据分析 - 数据探索/统计分析/可视化/业务洞察'
    version = '1.0.0'
    
    def get_decomposition_template(self) -> str:
        """任务分解模板"""
        return """
请按以下步骤分解数据分析任务：

1. **业务问题定义**
   - 核心问题是什么？（为什么销售额下滑？）
   - 决策场景是什么？（是否要增加营销预算？）
   - 期望输出是什么？（报告/仪表板/建议）
   - 成功标准是什么？（可执行的洞察）

2. **数据需求梳理**
   - 需要哪些数据源？（数据库/API/日志）
   - 时间范围？（最近 30 天/季度/年度）
   - 粒度要求？（日/周/月，用户/商品/渠道）
   - 数据质量评估？（完整性/准确性/一致性）

3. **数据收集与清洗**
   - SQL 查询或 API 调用
   - 缺失值处理
   - 异常值检测与处理
   - 数据格式标准化

4. **探索性数据分析 (EDA)**
   - 描述性统计（均值/中位数/标准差）
   - 分布分析（直方图/箱线图）
   - 相关性分析（热力图/散点图）
   - 趋势分析（时间序列）

5. **深度分析与建模**
   - 假设检验（A/B 测试结果分析）
   - 回归分析（影响因素分析）
   - 聚类分析（用户分群）
   - 预测模型（销量预测/流失预测）

6. **可视化与报告**
   - 关键指标仪表板
   - 趋势图表
   - 对比分析图
   - 结论与建议

7. **洞察提炼与行动建议**
   - 关键发现总结
   - 根因分析
   - 可执行建议
   - 后续追踪计划
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """验收标准"""
        return [
            "问题定义清晰：业务问题明确，决策场景清楚",
            "数据完整准确：关键数据无缺失，准确性>95%",
            "方法科学合适：统计方法适合数据类型和问题",
            "结论可靠：有统计显著性支持，效应量合理",
            "可视化清晰：图表易读，信息传达准确",
            "洞察可执行：有明确的行动建议，而非泛泛而谈",
            "可复现：提供完整代码和数据字典",
            "故事线清晰：从问题到结论逻辑连贯"
        ]
    
    def get_executor_tools(self) -> List[str]:
        """执行者可用的工具"""
        return [
            "SQL 客户端（DBeaver/DataGrip/pgAdmin）",
            "Python 分析库（pandas/numpy/scipy）",
            "可视化工具（Matplotlib/Seaborn/Plotly）",
            "BI 平台（Tableau/PowerBI/Looker）",
            "Jupyter Notebook/Lab",
            "统计软件（R/SPSS/SAS）",
            "大数据工具（Spark/Hive/Presto）",
            "A/B 测试平台（Optimizely/Google Optimize）"
        ]
    
    def get_best_practices(self) -> List[str]:
        """最佳实践"""
        return [
            "先问 Why，再问 What：理解业务背景比分析技术更重要",
            "数据质量优先：Garbage In, Garbage Out",
            "可视化少即是多：一张图只传达一个核心信息",
            "用数据讲故事：从问题→分析→洞察→建议的逻辑链",
            "避免因果谬误：相关不等于因果",
            "考虑基率：不要忽略基础概率",
            "敏感性分析：检验结论的稳健性",
            "同行评审：让其他人检查你的分析"
        ]
    
    def get_check_method(self, criterion: str):
        """获取特定标准的检查方法"""
        check_methods = {
            '数据完整准确': self._check_data_quality,
            '方法科学合适': self._check_methodology,
            '结论可靠': self._check_conclusion_validity,
            '可视化清晰': self._check_visualization,
        }
        return check_methods.get(criterion, self._default_check)
    
    async def _check_data_quality(self, results: Dict) -> Dict:
        """检查数据质量"""
        completeness = results.get('data_completeness', 100)  # 完整性%
        accuracy = results.get('data_accuracy', 100)  # 准确性%
        
        score = (completeness * 0.5 + accuracy * 0.5)
        passed = completeness >= 95 and accuracy >= 95
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'完整性{completeness}%, 准确性{accuracy}%',
            'suggestion': '补充缺失数据，校验数据源准确性' if not passed else ''
        }
    
    async def _check_methodology(self, results: Dict) -> Dict:
        """检查方法论"""
        methods_used = results.get('statistical_methods', [])
        appropriate = results.get('methods_appropriate', True)
        
        required_checks = [
            '描述性统计',
            '显著性检验' if 'hypothesis' in results.get('analysis_type', '') else None,
            '效应量报告' if 'comparison' in results.get('analysis_type', '') else None
        ]
        required_checks = [c for c in required_checks if c]
        
        score = 0
        for check in required_checks:
            if any(check.lower() in method.lower() for method in methods_used):
                score += 33
        if appropriate:
            score += 34
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'使用了{len(methods_used)}种统计方法',
            'suggestion': '补充必要的统计检验和效应量报告' if not passed else ''
        }
    
    async def _check_conclusion_validity(self, results: Dict) -> Dict:
        """检查结论有效性"""
        has_statistical_significance = results.get('has_statistical_significance', False)
        p_value = results.get('p_value', 1.0)
        effect_size = results.get('effect_size', 0)
        
        score = 0
        if has_statistical_significance and p_value < 0.05:
            score += 50
        if abs(effect_size) > 0.3:  # 中等效应
            score += 50
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'P 值={p_value:.3f}, 效应量={effect_size:.2f}',
            'suggestion': '确保统计显著性和实际意义' if not passed else ''
        }
    
    async def _check_visualization(self, results: Dict) -> Dict:
        """检查可视化质量"""
        chart_count = results.get('chart_count', 0)
        has_labels = results.get('charts_have_labels', True)
        color_accessible = results.get('color_accessible', True)
        
        score = 0
        if chart_count > 0 and chart_count <= 10:  # 避免过多
            score += 40
        if has_labels:
            score += 30
        if color_accessible:
            score += 30
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'{chart_count}张图表，标签：{"有" if has_labels else "无"}, 色盲友好：{"是" if color_accessible else "否"}',
            'suggestion': '简化图表数量，确保标签清晰，使用色盲友好配色' if not passed else ''
        }
    
    async def _default_check(self, results: Dict) -> Dict:
        """默认检查方法"""
        return {
            'passed': True,
            'score': 80,
            'reason': '符合要求',
            'suggestion': ''
        }
    
    def get_analysis_framework(self, analysis_type: str) -> Dict:
        """获取特定分析框架"""
        frameworks = {
            'cohort_analysis': {
                'name': '同期群分析',
                'purpose': '追踪不同时期用户的行为差异',
                'metrics': ['留存率', 'LTV', '转化率'],
                'tools': ['SQL', 'Python pandas', 'Mixpanel'],
                'output': '同期群热力图'
            },
            'funnel_analysis': {
                'name': '漏斗分析',
                'purpose': '识别转化流程中的流失点',
                'metrics': ['各步骤转化率', '平均转化时间', '流失率'],
                'tools': ['Google Analytics', '神策数据', 'SQL'],
                'output': '漏斗转化图'
            },
            'ab_testing': {
                'name': 'A/B 测试',
                'purpose': '验证假设，优化产品',
                'metrics': ['核心指标提升', '统计显著性', '置信区间'],
                'tools': ['Optimizely', 'Google Optimize', '自建平台'],
                'output': 'A/B 测试报告'
            },
            'rfm_analysis': {
                'name': 'RFM 分析',
                'purpose': '用户价值分层',
                'metrics': ['最近购买时间', '购买频率', '消费金额'],
                'tools': ['SQL', 'Python', 'Excel'],
                'output': '用户分层矩阵'
            }
        }
        
        return frameworks.get(analysis_type, {})


def load_plugin():
    """加载插件实例"""
    return DataAnalysisPlugin()


if __name__ == '__main__':
    plugin = DataAnalysisPlugin()
    
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
    
    print("\n📊 分析框架示例:")
    framework = plugin.get_analysis_framework('funnel_analysis')
    print(f"  名称：{framework.get('name', 'N/A')}")
    print(f"  用途：{framework.get('purpose', 'N/A')}")
    print(f"  指标：{', '.join(framework.get('metrics', []))}")
