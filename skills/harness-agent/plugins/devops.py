# -*- coding: utf-8 -*-
"""
DevOps Plugin - 运维部署插件

简洁版设计 / Simple design
适用于：CI/CD、部署、监控、基础设施管理
"""

from typing import List, Dict


class DevOpsPlugin:
    """运维部署领域插件"""
    
    name = 'devops'
    description = 'DevOps - CI/CD, Deployment, Monitoring, Infrastructure'
    version = '1.0.0'
    
    def get_task_template(self) -> str:
        """任务分解模板"""
        return """
## DevOps 任务分解

1. **环境准备** - 开发/测试/生产环境配置
2. **CI/CD 管道** - 自动化构建、测试、部署
3. **基础设施** - 服务器、网络、存储配置
4. **部署策略** - Blue-Green/Canary/Rolling 部署
5. **监控告警** - 日志、指标、告警规则
6. **安全加固** - 漏洞扫描、访问控制、备份
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """验收标准"""
        return [
            "✅ CI/CD 管道运行正常",
            "✅ 部署成功且可回滚",
            "✅ 监控覆盖关键指标",
            "✅ 告警规则合理 (<5 分钟响应)",
            "✅ 日志完整可查询",
            "✅ 安全扫描无高危漏洞"
        ]
    
    def get_tools(self) -> List[Dict]:
        """可用工具"""
        return [
            {
                "name": "setup_ci_cd",
                "desc": "配置 CI/CD 管道",
                "params": ["platform", "build_steps", "deploy_target"],
                "safe": False  # 会创建配置文件
            },
            {
                "name": "deploy_application",
                "desc": "部署应用",
                "params": ["environment", "strategy", "version"],
                "safe": False  # 破坏性操作
            },
            {
                "name": "setup_monitoring",
                "desc": "配置监控系统",
                "params": ["metrics", "alerts", "dashboard"],
                "safe": False
            },
            {
                "name": "check_health",
                "desc": "健康检查",
                "params": ["services", "endpoints"],
                "safe": True  # 只读检查
            },
            {
                "name": "manage_infrastructure",
                "desc": "管理基础设施 (IaC)",
                "params": ["provider", "resources", "action"],
                "safe": False
            },
            {
                "name": "backup_restore",
                "desc": "备份与恢复",
                "params": ["target", "action", "schedule"],
                "safe": False
            }
        ]
    
    def get_platform_recommendations(self, need: str) -> Dict:
        """平台推荐"""
        recommendations = {
            'ci_cd': {
                'github_actions': {
                    'best_for': 'GitHub 项目，免费额度充足',
                    'integrates_with': ['GitHub', 'AWS', 'Azure', 'GCP'],
                    'pricing': '免费 2000 分钟/月'
                },
                'gitlab_ci': {
                    'best_for': 'GitLab 项目，一体化方案',
                    'integrates_with': ['GitLab', 'Kubernetes'],
                    'pricing': '免费 400 分钟/月'
                },
                'jenkins': {
                    'best_for': '高度定制化需求',
                    'integrates_with': ['所有平台'],
                    'pricing': '开源免费'
                }
            },
            'monitoring': {
                'prometheus_grafana': {
                    'best_for': '云原生应用，指标监控',
                    'stack': ['Prometheus', 'Grafana', 'Alertmanager'],
                    'pricing': '开源免费'
                },
                'datadog': {
                    'best_for': '企业级全栈监控',
                    'stack': ['APM', 'Logs', 'Synthetics'],
                    'pricing': '$15/host/月起'
                },
                'new_relic': {
                    'best_for': '应用性能监控',
                    'stack': ['APM', 'Browser', 'Mobile'],
                    'pricing': '免费 100GB/月'
                }
            },
            'cloud': {
                'aws': {
                    'best_for': '全球业务，服务最全',
                    'key_services': ['EC2', 'S3', 'RDS', 'Lambda'],
                    'pricing': '按量付费'
                },
                'aliyun': {
                    'best_for': '中国大陆业务',
                    'key_services': ['ECS', 'OSS', 'RDS', 'FC'],
                    'pricing': '按量付费'
                }
            }
        }
        return recommendations.get(need, {})
    
    def get_best_practices(self) -> List[str]:
        """最佳实践"""
        return [
            "🔄 自动化一切可自动化的流程",
            "📊 监控先行，部署在后",
            "🔒 最小权限原则管理访问",
            "💾 定期测试备份恢复",
            "🚀 小步快跑，频繁部署",
            "📝 所有变更版本化管理 (IaC)"
        ]


def load_plugin():
    """加载插件"""
    return DevOpsPlugin()


if __name__ == '__main__':
    plugin = DevOpsPlugin()
    
    print("=" * 60)
    print(f"插件：{plugin.name}")
    print(f"描述：{plugin.description}")
    print("=" * 60)
    
    print("\n🛠️ 可用工具:")
    for tool in plugin.get_tools():
        safe_icon = "✅" if tool['safe'] else "⚠️"
        print(f"  {safe_icon} {tool['name']} - {tool['desc']}")
    
    print("\n☁️ 平台推荐:")
    for category in ['ci_cd', 'monitoring', 'cloud']:
        recs = plugin.get_platform_recommendations(category)
        print(f"\n  {category.upper()}:")
        for name, info in list(recs.items())[:2]:  # 只显示前 2 个
            print(f"    • {name}: {info.get('best_for')}")
    
    print("\n💡 最佳实践:")
    for practice in plugin.get_best_practices():
        print(f"  {practice}")
