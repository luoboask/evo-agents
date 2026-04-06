# -*- coding: utf-8 -*-
"""
内容创作领域插件
Content Creation Domain Plugin

适用于：文章写作、视频脚本、社交媒体内容、营销文案等
"""

from typing import List, Dict


class ContentCreationPlugin:
    """内容创作领域插件"""
    
    name = 'content-creation'
    description = '内容创作 - 文章/视频脚本/社交媒体/营销文案'
    version = '1.0.0'
    
    def get_decomposition_template(self) -> str:
        """任务分解模板"""
        return """
请按以下步骤分解内容创作任务：

1. **内容定位与目标**
   - 目标受众是谁？（年龄/职业/兴趣/痛点）
   - 内容目的是什么？（品牌曝光/获客/转化/教育）
   - 发布平台是什么？（公众号/抖音/小红书/B 站）
   - 成功指标是什么？（阅读量/点赞/转发/转化）

2. **选题与角度策划**
   - 热点话题结合
   - 独特视角切入
   - 差异化定位
   - 价值主张提炼

3. **内容结构设计**
   - 标题设计（3-5 个备选）
   - 开头钩子（前 3 秒/前 50 字抓住注意力）
   - 主体框架（总分总/故事线/清单体/对比式）
   - 结尾引导（互动/转化/关注/分享）

4. **内容创作执行**
   - 初稿撰写
   - 案例与数据支撑
   - 金句打磨
   - 配图/配视频规划

5. **优化与润色**
   - 逻辑连贯性检查
   - 语言流畅度优化
   - SEO 关键词融入
   - 情绪感染力增强

6. **审核与发布准备**
   - 事实核查
   - 合规性检查（广告法/平台规则）
   - 标签/话题选择
   - 发布时间规划
"""
    
    def get_acceptance_criteria(self) -> List[str]:
        """验收标准"""
        return [
            "目标明确：清楚目标受众和内容目的",
            "标题吸引人：至少 3 个备选，符合平台特性",
            "开头强力：前 3 秒/前 50 字能抓住注意力",
            "结构清晰：有清晰的逻辑框架",
            "内容有料：提供知识/情感/娱乐价值",
            "语言流畅：无语法错误，表达清晰",
            "有行动引导：包含明确的 CTA（Call to Action）",
            "符合平台规范：无违规内容，符合社区准则"
        ]
    
    def get_executor_tools(self) -> List[str]:
        """执行者可用的工具"""
        return [
            "内容灵感工具（今日热榜/新榜/灰豚数据）",
            "标题生成器（AI 辅助创作）",
            "排版工具（秀米/135 编辑器/Canva）",
            "配图工具（Unsplash/Pexels/稿定设计）",
            "视频剪辑工具（剪映/必剪/CapCut）",
            "Grammarly/秘塔写作猫（语法检查）",
            "SEO 工具（5118/爱站网）",
            "内容协作平台（语雀/Notion/飞书文档）"
        ]
    
    def get_best_practices(self) -> List[str]:
        """最佳实践"""
        return [
            "黄金 3 秒原则：开头必须在前 3 秒抓住注意力",
            "情绪价值优先：触发用户情感共鸣",
            "干货密度：每 500 字至少 1 个知识点/金句",
            "视觉化表达：多用图表/案例/对比",
            "互动设计：在关键节点设置互动点",
            "系列化运营：打造 IP 辨识度",
            "A/B 测试：测试不同标题和封面",
            "数据复盘：根据数据反馈优化内容"
        ]
    
    def get_check_method(self, criterion: str):
        """获取特定标准的检查方法"""
        check_methods = {
            '标题吸引人': self._check_title_quality,
            '开头强力': self._check_hook_quality,
            '内容有料': self._check_content_value,
            '有行动引导': self._check_cta,
        }
        return check_methods.get(criterion, self._default_check)
    
    async def _check_title_quality(self, results: Dict) -> Dict:
        """检查标题质量"""
        titles_count = results.get('titles_count', 1)
        has_numbers = results.get('title_has_numbers', False)
        has_emotion = results.get('title_has_emotion', False)
        has_keyword = results.get('title_has_keyword', False)
        
        score = 0
        if titles_count >= 3:
            score += 25
        if has_numbers:
            score += 25
        if has_emotion:
            score += 25
        if has_keyword:
            score += 25
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'{titles_count}个标题，数字：{"有" if has_numbers else "无"}, 情绪：{"有" if has_emotion else "无"}, 关键词：{"有" if has_keyword else "无"}',
            'suggestion': '准备 3-5 个标题备选，加入数字、情绪词和关键词' if not passed else ''
        }
    
    async def _check_hook_quality(self, results: Dict) -> Dict:
        """检查开头钩子质量"""
        hook_type = results.get('hook_type', '')
        hook_length = results.get('hook_length', 0)
        
        good_hooks = ['疑问', '故事', '震惊', '数据', '对比', '承诺']
        is_good_hook = any(h in hook_type for h in good_hooks)
        
        score = 0
        if is_good_hook:
            score += 60
        if 30 <= hook_length <= 100:  # 字数适中
            score += 40
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'钩子类型：{hook_type}, 长度：{hook_length}字',
            'suggestion': '使用疑问/故事/震惊/数据类钩子，控制在 30-100 字' if not passed else ''
        }
    
    async def _check_content_value(self, results: Dict) -> Dict:
        """检查内容价值"""
        value_points = results.get('value_points', 0)  # 价值点数量
        has_examples = results.get('has_examples', False)
        has_data = results.get('has_data_support', False)
        word_count = results.get('word_count', 0)
        
        # 计算干货密度
        density = (value_points / word_count * 500) if word_count > 0 else 0
        
        score = 0
        if density >= 1:  # 每 500 字至少 1 个价值点
            score += 40
        if has_examples:
            score += 30
        if has_data:
            score += 30
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'{value_points}个价值点，案例：{"有" if has_examples else "无"}, 数据：{"有" if has_data else "无"}, 干货密度：{density:.1f}/500 字',
            'suggestion': '增加具体案例和数据支撑，提高干货密度' if not passed else ''
        }
    
    async def _check_cta(self, results: Dict) -> Dict:
        """检查行动引导"""
        has_cta = results.get('has_cta', False)
        cta_type = results.get('cta_type', '')
        cta_position = results.get('cta_position', '')
        
        good_cta_types = ['关注', '点赞', '评论', '分享', '购买', '预约', '领取']
        is_good_cta = any(cta in cta_type for cta in good_cta_types)
        
        score = 0
        if has_cta:
            score += 50
        if is_good_cta:
            score += 30
        if cta_position in ['结尾', '文中多处']:
            score += 20
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'CTA: {"有" if has_cta else "无"}, 类型：{cta_type}, 位置：{cta_position}',
            'suggestion': '添加明确的行动引导（关注/点赞/评论/购买等）' if not passed else ''
        }
    
    async def _default_check(self, results: Dict) -> Dict:
        """默认检查方法"""
        return {
            'passed': True,
            'score': 80,
            'reason': '符合要求',
            'suggestion': ''
        }
    
    def get_platform_config(self, platform: str) -> Dict:
        """获取特定平台配置"""
        platforms = {
            'wechat': {
                'name': '微信公众号',
                'best_post_time': '20:00-22:00',
                'title_max_length': 64,
                'abstract_max_length': 120,
                'cover_image_size': '900x383px',
                'content_tips': [
                    '标题控制在 20-30 字最佳',
                    '摘要要补充标题未表达的信息',
                    '正文多用小标题分割',
                    '文末添加往期推荐'
                ]
            },
            'xiaohongshu': {
                'name': '小红书',
                'best_post_time': '19:00-21:00',
                'title_max_length': 20,
                'content_max_length': 1000,
                'image_count': '3-9 张',
                'tags_max': 10,
                'content_tips': [
                    '标题要吸睛，多用 emoji',
                    '首图最重要，决定点击率',
                    '正文多分段，每段不超过 3 行',
                    '标签要精准，覆盖不同维度'
                ]
            },
            'douyin': {
                'name': '抖音',
                'best_post_time': '18:00-20:00',
                'video_duration': '15-60 秒',
                'hook_first_seconds': 3,
                'caption_max_length': 55,
                'content_tips': [
                    '前 3 秒必须有钩子',
                    '节奏要快，5-10 秒一个爆点',
                    'BGM 要热门且匹配内容',
                    '文案引导互动（点赞/评论/转发）'
                ]
            },
            'bilibili': {
                'name': 'B 站',
                'best_post_time': '18:00-20:00',
                'video_duration': '3-10 分钟',
                'title_max_length': 80,
                'cover_image_size': '1146x712px',
                'content_tips': [
                    '标题可以长一些，包含关键词',
                    '封面要有冲击力和信息量',
                    '前 30 秒交代清楚视频价值',
                    '弹幕互动点设计'
                ]
            }
        }
        
        return platforms.get(platform, {})


def load_plugin():
    """加载插件实例"""
    return ContentCreationPlugin()


if __name__ == '__main__':
    plugin = ContentCreationPlugin()
    
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
    
    print("\n📱 平台配置示例（小红书）:")
    config = plugin.get_platform_config('xiaohongshu')
    for key, value in config.items():
        print(f"  {key}: {value}")
