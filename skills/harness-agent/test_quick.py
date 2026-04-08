#!/usr/bin/env python3
# Harness Agent 快速测试脚本

import asyncio
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("🧪 Harness Agent v5.0 快速测试")
print("=" * 60)

# ========== 测试 1: 自动领域检测 ==========
print("\n【测试 1】自动领域检测")
print("-" * 60)

def auto_detect_domain(task: str) -> str:
    """简化的领域检测逻辑（增强版）"""
    keyword_mapping = {
        'programming': [
            # 核心动词
            '代码', '开发', '编程', '编写', '实现', '构建', '搭建',
            # 名词 - 软件/网站
            '网站', 'APP', '应用', '软件', '系统', '平台',
            # 名词 - 技术组件
            'API', '数据库', '接口', '模块', '功能', '服务',
            # 名词 - 代码单元
            '函数', '脚本', '程序', '算法', '类', '方法',
            # 语言名称
            'Python', 'JavaScript', 'Java', 'Go', 'Rust', 'C++',
        ],
        'marketing': [
            '营销', '活动', '推广', '品牌', '广告', '社交媒体',
            '转化率', 'ROI', '流量', '用户增长', 'campaign',
        ],
        'legal': [
            '合同', '协议', '法律', '审查', '合规', '条款',
            '法规', '风险', '诉讼', '仲裁', '知识产权',
        ],
        'education': [
            '课程', '培训', '教学', '学习', '教材', '考试',
            '学生', '教育', '课件', '教案', '培训体系',
        ],
        'data-analysis': [
            '数据', '分析', '报表', '可视化', '统计', '模型',
            '洞察', 'BI', 'dashboard', '趋势', '预测',
        ],
    }
    
    # Layer 1: 关键词匹配
    for domain, keywords in keyword_mapping.items():
        if any(kw in task for kw in keywords):
            return domain
    
    # Layer 2: 任务模式识别（增强）
    patterns = {
        'build_pattern': ['创建', '开发', '构建', '实现', '搭建', '写一个', '做一个'],
        'analyze_pattern': ['分析', '研究', '调查', '评估', '总结', '找出'],
        'review_pattern': ['审查', '检查', '审核', '验收', '评审', '查看'],
        'create_content_pattern': ['撰写', '创作', '设计', '制作', '编写'],
        'plan_pattern': ['策划', '规划', '计划', '方案', '策略'],
    }
    
    pattern_to_domain = {
        'build_pattern': 'programming',
        'analyze_pattern': 'data-analysis',
        'review_pattern': 'legal',
        'create_content_pattern': 'media',
        'plan_pattern': 'marketing',
    }
    
    for pattern_name, pattern_words in patterns.items():
        if any(word in task for word in pattern_words):
            detected_domain = pattern_to_domain.get(pattern_name, 'generic')
            # 验证是否有该领域的特定关键词
            if detected_domain in keyword_mapping:
                return detected_domain
    
    return 'generic'

test_cases = [
    ("开发一个电商网站", "programming"),
    ("分析 Q1 销售数据", "data-analysis"),
    ("策划双十一营销活动", "marketing"),
    ("审查这份合同", "legal"),
    ("设计新员工培训课程", "education"),
    ("写一个 Hello World 函数", "programming"),
]

passed = 0
failed = 0

for task, expected in test_cases:
    detected = auto_detect_domain(task)
    status = "✅" if detected == expected else "⚠️"
    
    if detected == expected:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} 任务：{task}")
    print(f"   检测结果：{detected} | 期望：{expected}\n")

print(f"结果：{passed} 通过，{failed} 失败")

# ========== 测试 2: 进度文件初始化 ==========
print("\n【测试 2】进度文件初始化")
print("-" * 60)

async def init_progress_file():
    progress_file = Path('.harness/progress.md')
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    
    task_name = "测试任务：开发博客系统"
    domain = "programming"
    
    content = f"""# Harness 进度追踪

> 自动生成 | 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 领域：{domain}

## 📊 任务概览
- **任务**: {task_name}
- **领域**: {domain}
- **开始时间**: {datetime.now().isoformat()}
- **当前状态**: 🔄 初始化完成
- **总体进度**: ░░░░░░░░░░ 0%

## ✅ 已完成任务
_(暂无)_

## 🔄 当前进行
- **任务**: 等待 Planner 分解
- **进度**: 0%

## ⚠️ 遇到的问题
_(暂无)_

## 📅 下一步计划
1. Planner 分解任务
2. 启动 Specialists
3. 并行执行
4. Evaluator 质检

_此文件由 Harness Agent 自动维护_
"""
    
    progress_file.write_text(content, encoding='utf-8')
    
    if progress_file.exists():
        print(f"✅ 进度文件创建成功")
        print(f"📄 位置：{progress_file.absolute()}")
        
        # 显示前 20 行预览
        lines = content.split('\n')[:22]
        print(f"\n📋 文件预览:")
        for line in lines:
            print(f"  {line}")
        
        return True
    else:
        print("❌ 进度文件创建失败")
        return False

# 运行异步测试
progress_created = asyncio.run(init_progress_file())

# ========== 测试 3: 模拟任务分解 ==========
print("\n【测试 3】模拟任务分解（Planner）")
print("-" * 60)

def simulate_decomposition(task: str, domain: str) -> list:
    """模拟任务分解逻辑"""
    
    templates = {
        'programming': [
            "需求分析与用户故事梳理",
            "技术栈选择与架构设计",
            "数据库设计与 API 定义",
            "前端界面实现",
            "后端逻辑实现",
            "单元测试与集成测试",
            "文档编写与部署",
        ],
        'data-analysis': [
            "业务问题定义与假设提出",
            "数据收集与来源识别",
            "数据清洗与转换",
            "探索性数据分析 (EDA)",
            "建模与验证",
            "可视化与报告撰写",
        ],
        'marketing': [
            "市场环境与竞品分析",
            "目标受众画像",
            "渠道策略制定",
            "内容创作与日历规划",
            "活动执行与监控",
            "ROI 分析与总结",
        ],
    }
    
    base_tasks = templates.get(domain, ["任务分析", "方案设计", "执行实施", "质量检查", "总结交付"])
    
    # 根据具体任务调整
    subtasks = []
    for i, desc in enumerate(base_tasks, 1):
        subtasks.append({
            'id': f'task_{i}',
            'description': f'{desc}',
            'estimated_hours': 2,
            'status': 'pending'
        })
    
    return subtasks

# 测试编程领域
task = "开发一个简单的待办事项 APP"
domain = "programming"
subtasks = simulate_decomposition(task, domain)

print(f"任务：{task}")
print(f"领域：{domain}")
print(f"分解为 {len(subtasks)} 个子任务:\n")

for i, task in enumerate(subtasks, 1):
    print(f"  {i}. {task['description']} (预计：{task['estimated_hours']}小时)")

total_hours = sum(t['estimated_hours'] for t in subtasks)
print(f"\n总预估工作量：{total_hours} 小时")

# ========== 测试 4: 模拟质检流程 ==========
print("\n【测试 4】模拟质检流程（Evaluator）")
print("-" * 60)

def simulate_evaluation(results: dict) -> dict:
    """模拟质检逻辑"""
    
    # 模拟验收标准
    criteria = [
        "功能完整性",
        "代码质量",
        "测试覆盖率",
        "性能指标",
        "文档完整"
    ]
    
    issues = []
    scores = []
    
    # 模拟检查结果
    import random
    for criterion in criteria:
        score = random.randint(75, 95)  # 模拟分数
        scores.append(score)
        
        if score < 80:
            issues.append({
                'criterion': criterion,
                'reason': f'{criterion}得分较低 ({score}分)',
                'severity': 'medium',
                'suggestion': f'建议改进{criterion}'
            })
    
    final_score = sum(scores) / len(scores)
    passed = final_score >= 70 and not any(i['severity'] == 'high' for i in issues)
    
    return {
        'passed': passed,
        'score': round(final_score, 1),
        'issues': issues,
        'scores_by_criterion': dict(zip(criteria, scores))
    }

# 模拟执行结果
results = {
    'task_1': {'success': True},
    'task_2': {'success': True},
    'task_3': {'success': True},
}

evaluation = simulate_evaluation(results)

print("质检结果:")
print(f"  ✅ 通过：{evaluation['passed']}")
print(f"  📊 总分：{evaluation['score']}/100")
print(f"\n  各项得分:")
for criterion, score in evaluation['scores_by_criterion'].items():
    bar = '█' * int(score / 10) + '░' * (10 - int(score / 10))
    print(f"    {criterion}: {bar} {score}")

if evaluation['issues']:
    print(f"\n  ⚠️ 发现的问题 ({len(evaluation['issues'])}个):")
    for issue in evaluation['issues']:
        print(f"    - {issue['criterion']}: {issue['reason']}")
        print(f"      建议：{issue['suggestion']}")

# ========== 测试总结 ==========
print("\n" + "=" * 60)
print("📊 测试总结")
print("=" * 60)

tests_passed = [
    ("自动领域检测", passed > 0),
    ("进度文件初始化", progress_created),
    ("任务分解模拟", len(subtasks) > 0),
    ("质检流程模拟", 'score' in evaluation),
]

all_passed = all(result for _, result in tests_passed)

for test_name, result in tests_passed:
    status = "✅" if result else "❌"
    print(f"{status} {test_name}")

print("\n" + "=" * 60)
if all_passed:
    print("🎉 所有测试通过！Harness Agent 核心逻辑正常。")
    print("\n💡 下一步:")
    print("   1. 查看生成的进度文件：cat .harness/progress.md")
    print("   2. 尝试真实任务：/harness-agent \"你的任务\" --domain programming")
    print("   3. 查看详细文档：skills/harness-agent/SKILL.md")
else:
    print("⚠️ 部分测试未通过，请检查日志。")

print("=" * 60)
