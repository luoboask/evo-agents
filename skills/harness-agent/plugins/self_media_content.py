# -*- coding: utf-8 -*-
"""
自媒体内容创作领域插件
Self-Media Content Creation Domain Plugin

适用于：公众号文章、短视频脚本、小红书笔记、播客内容等创作任务
"""

from typing import List, Dict, Any


class SelfMediaContentPlugin:
    """自媒体内容创作领域插件"""
    
    name = 'self-media-content'
    description = '自媒体内容创作 - 公众号/短视频/小红书/播客等内容创作'
    version = '1.0.0'
    author = 'Harness Agent Team'
    
    # ========== 任务分解模板 ==========
    
    def get_decomposition_template(self) -> str:
        """返回任务分解模板"""
        return """
请按以下步骤分解自媒体内容创作任务：

1. **内容定位与受众分析**
   - 目标受众画像（年龄/兴趣/痛点）
   - 内容调性确定（专业/幽默/温暖/励志）
   - 平台特性适配（公众号/抖音/小红书/B 站）

2. **选题与角度策划**
   - 热点话题结合
   - 独特视角切入
   - 价值点提炼（知识/情感/娱乐）

3. **内容大纲设计**
   - 标题设计（3-5 个备选）
   - 开头钩子（前 3 秒/前 50 字抓住注意力）
   - 主体结构（总分总/故事线/清单体）
   - 结尾引导（互动/转化/关注）

4. **内容创作执行**
   - 初稿撰写
   - 配图/配视频规划
   - 金句/亮点打磨

5. **优化与发布准备**
   - SEO 关键词优化
   - 标签/话题选择
   - 发布时间规划
   - 互动预案准备

6. **数据追踪计划**
   - 核心指标定义（阅读/点赞/评论/转发）
   - A/B 测试方案
   - 复盘模板准备
"""
    
    # ========== 验收标准 ==========
    
    def get_acceptance_criteria(self) -> List[str]:
        """返回验收标准列表"""
        return [
            "内容定位清晰：明确目标受众和内容调性",
            "标题吸引力：至少 3 个备选标题，符合平台特性",
            "开头钩子强力：前 3 秒/前 50 字能抓住注意力",
            "内容价值明确：提供知识/情感/娱乐价值",
            "结构逻辑清晰：有清晰的起承转合",
            "结尾引导有效：包含互动/转化/关注引导",
            "SEO 优化到位：关键词自然融入，标签准确",
            "符合平台规范：无违规内容，符合社区准则",
            "原创性保证：无抄袭，查重率<10%"
        ]
    
    # ========== 执行者工具集 ==========
    
    def get_executor_tools(self) -> List[str]:
        """返回执行者可用的工具列表"""
        return [
            "内容灵感工具（今日热榜/新榜/灰豚数据）",
            "标题生成器（AI 辅助创作）",
            "排版工具（秀米/135 编辑器/Canva）",
            "配图工具（Unsplash/Pexels/稿定设计）",
            "视频剪辑工具（剪映/必剪/CapCut）",
            "数据分析工具（新榜/蝉妈妈/飞瓜数据）",
            "SEO 优化工具（5118/爱站网）",
            "查重工具（PaperPass/维普）"
        ]
    
    # ========== 最佳实践 ==========
    
    def get_best_practices(self) -> List[str]:
        """返回领域最佳实践列表"""
        return [
            "黄金 3 秒原则：开头必须在前 3 秒抓住注意力",
            "情绪价值优先：触发用户情感共鸣",
            "干货密度控制：每 500 字至少 1 个知识点/金句",
            "视觉化表达：多用图表/案例/对比",
            "互动设计：在关键节点设置互动点",
            "持续系列化：打造 IP 辨识度",
            "数据驱动迭代：根据数据反馈优化内容",
            "合规第一：严格遵守广告法和平台规则"
        ]
    
    # ========== 质检方法 ==========
    
    def get_check_method(self, criterion: str):
        """返回特定验收标准的检查方法"""
        check_methods = {
            '标题吸引力': self._check_title_quality,
            '开头钩子': self._check_hook_quality,
            '内容价值': self._check_content_value,
            'SEO 优化': self._check_seo_optimization,
            '原创性': self._check_originality,
        }
        return check_methods.get(criterion, self._default_check)
    
    async def _check_title_quality(self, results: Dict) -> Dict:
        """检查标题质量"""
        # 实际实现会调用 AI 评估或 A/B 测试数据
        titles_count = results.get('titles_count', 3)
        has_numbers = results.get('title_has_numbers', True)
        has_emotion = results.get('title_has_emotion', True)
        
        score = 0
        if titles_count >= 3:
            score += 30
        if has_numbers:
            score += 35
        if has_emotion:
            score += 35
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'提供了{titles_count}个标题，{"包含" if has_numbers else "缺少"}数字，{"包含" if has_emotion else "缺少"}情绪词',
            'suggestion': '' if passed else '建议提供更多标题备选，加入数字和情绪词'
        }
    
    async def _check_hook_quality(self, results: Dict) -> Dict:
        """检查开头钩子质量"""
        # 评估开头是否能在 3 秒内抓住注意力
        hook_type = results.get('hook_type', 'question')  # question/story/shocking/statistic
        hook_length = results.get('hook_length', 50)
        
        score = 80  # 默认良好
        if hook_length > 100:
            score -= 20  # 太长扣分
        if hook_type not in ['question', 'story', 'shocking', 'statistic']:
            score -= 30  # 钩子类型不明确
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': max(score, 0),
            'reason': f'钩子类型：{hook_type}, 长度：{hook_length}字',
            'suggestion': '开头控制在 50-100 字，使用疑问/故事/震惊/数据类钩子' if not passed else ''
        }
    
    async def _check_content_value(self, results: Dict) -> Dict:
        """检查内容价值"""
        # 评估内容是否提供足够的知识/情感/娱乐价值
        value_points = results.get('value_points', 5)  # 价值点数量
        has_examples = results.get('has_examples', True)
        has_actionable_tips = results.get('has_actionable_tips', True)
        
        score = min(100, value_points * 15)  # 每个价值点 15 分
        if not has_examples:
            score -= 20
        if not has_actionable_tips:
            score -= 20
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': max(score, 0),
            'reason': f'{value_points}个价值点，{"有" if has_examples else "缺少"}案例，{"有" if has_actionable_tips else "缺少"}可操作建议',
            'suggestion': '增加具体案例和可操作的建议' if not passed else ''
        }
    
    async def _check_seo_optimization(self, results: Dict) -> Dict:
        """检查 SEO 优化"""
        keywords_density = results.get('keywords_density', 2.5)  # 关键词密度%
        has_tags = results.get('has_tags', True)
        tags_count = results.get('tags_count', 5)
        
        score = 0
        if 1.0 <= keywords_density <= 3.0:
            score += 50
        elif keywords_density > 3.0:
            score += 20  # 堆砌关键词扣分
        if has_tags and tags_count >= 3:
            score += 50
        
        passed = score >= 70
        
        return {
            'passed': passed,
            'score': score,
            'reason': f'关键词密度{keywords_density}%, {tags_count}个标签',
            'suggestion': '调整关键词密度到 1-3%，添加 3-5 个相关标签' if not passed else ''
        }
    
    async def _check_originality(self, results: Dict) -> Dict:
        """检查原创性"""
        # 实际实现会调用查重 API
        similarity_rate = results.get('similarity_rate', 5)  # 相似度%
        
        score = 100 - (similarity_rate * 2)
        passed = similarity_rate < 10
        
        return {
            'passed': passed,
            'score': max(score, 0),
            'reason': f'查重相似度{similarity_rate}%',
            'suggestion': '改写高相似段落，增加原创观点' if not passed else ''
        }
    
    async def _default_check(self, results: Dict) -> Dict:
        """默认检查方法"""
        return {
            'passed': True,
            'score': 80,
            'reason': '符合要求',
            'suggestion': ''
        }
    
    # ========== 平台特定配置 ==========
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """获取特定平台的配置"""
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
        
        return platforms.get(platform, platforms['wechat'])


# ========== 插件导出 ==========

def load_plugin() -> SelfMediaContentPlugin:
    """加载插件实例"""
    return SelfMediaContentPlugin()


# ========== 使用示例 ==========

if __name__ == '__main__':
    import asyncio
    
    plugin = SelfMediaContentPlugin()
    
    print("=" * 60)
    print(f"插件：{plugin.name}")
    print(f"描述：{plugin.description}")
    print("=" * 60)
    
    print("\n📋 任务分解模板:")
    print(plugin.get_decomposition_template()[:500] + "...")
    
    print("\n✅ 验收标准:")
    for i, criterion in enumerate(plugin.get_acceptance_criteria(), 1):
        print(f"  {i}. {criterion}")
    
    print("\n🛠️ 可用工具:")
    for tool in plugin.get_executor_tools()[:5]:
        print(f"  - {tool}")
    
    print("\n💡 最佳实践:")
    for practice in plugin.get_best_practices()[:5]:
        print(f"  - {practice}")
    
    # 测试平台配置
    print("\n📱 平台配置示例（小红书）:")
    config = plugin.get_platform_config('xiaohongshu')
    for key, value in config.items():
        print(f"  {key}: {value}")
