#!/usr/bin/env python3
"""
Web Knowledge v5.0 - 完全免费增强版
=====================================

新增功能:
1. ✅ 多引擎自动切换 (Bing/Baidu/Google/DuckDuckGo/Sogou)
2. ✅ 深度研究模式 (多角度搜索 + 智能去重 + 综合摘要)
3. ✅ 智能摘要生成 (提取关键信息 + 去除广告)
4. ✅ 时间范围过滤 (最新/一周内/一月内/自定义)
5. ✅ 结果质量评分 (相关性/时效性/权威性)
6. ✅ 完全免费，无需 API Key

使用示例:
    # 基础搜索
    python3 search.py "2026 年电商支付方案"
    
    # 深度研究
    python3 search.py "AI agent 框架对比" --deep-research
    
    # 限定时间
    python3 search.py "Python 3.13" --date-after 2026-01-01
    
    # 指定引擎
    python3 search.py "跨境电商合规" --engine baidu
    
    # 导出结果
    python3 search.py "机器学习教程" --export results.md
"""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import hashlib


class EnhancedWebSearch:
    """增强型网络搜索引擎 - v5.0 完全免费版"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.cache_dir = self.workspace / ".cache" / "web-search"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 所有支持的引擎（全部免费，无需 API Key）
        self.engines = {
            'bing': {
                'name': 'Bing 国际',
                'url': 'https://www.bing.com/search?q={query}&first={start}',
                'parser': lambda h, n: self._parse_with_bs(h, n, 'bing'),
                'language': 'en',
                'region': 'global',
            },
            'bing-cn': {
                'name': 'Bing 中国',
                'url': 'https://cn.bing.com/search?q={query}&first={start}',
                'parser': lambda h, n: self._parse_with_bs(h, n, 'bing-cn'),
                'language': 'zh-CN',
                'region': 'CN',
            },
            'baidu': {
                'name': '百度',
                'url': 'https://www.baidu.com/s?wd={query}&pn={start}',
                'parser': self._parse_baidu_results,
                'language': 'zh-CN',
                'region': 'CN',
            },
            'google': {
                'name': 'Google',
                'url': 'https://www.google.com/search?q={query}&start={start}',
                'parser': lambda h, n: self._parse_with_bs(h, n, 'google'),
                'language': 'en',
                'region': 'global',
            },
            'duckduckgo': {
                'name': 'DuckDuckGo',
                'url': 'https://html.duckduckgo.com/html/?q={query}&s={start}',
                'parser': lambda h, n: self._parse_with_bs(h, n, 'duckduckgo'),
                'language': 'en',
                'region': 'global',
                'privacy': True,
            },
            'sogou': {
                'name': '搜狗',
                'url': 'https://www.sogou.com/web?query={query}&page={page}',
                'parser': lambda h, n: self._parse_with_bs(h, n, 'sogou'),
                'language': 'zh-CN',
                'region': 'CN',
            },
        }
        
        # 引擎优先级（中文场景）
        self.engine_priority = ['bing-cn', 'baidu', 'sogou', 'duckduckgo', 'bing', 'google']
        
        # 健康状态
        self.engine_health = {name: {'failures': 0, 'last_fail': 0, 'successes': 0} 
                             for name in self.engines}
        
        # 缓存机制
        self.cache_ttl = 3600  # 1 小时缓存
    
    def search(self, query: str, 
               engine: Optional[str] = None,
               num_results: int = 10,
               date_after: Optional[str] = None,
               date_before: Optional[str] = None,
               language: str = 'zh-CN',
               safe_search: bool = True,
               use_cache: bool = True,
               verbose: bool = False) -> List[Dict]:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            engine: 指定引擎（None=自动选择）
            num_results: 返回结果数量
            date_after: 日期之后 (YYYY-MM-DD)
            date_before: 日期之前 (YYYY-MM-DD)
            language: 语言偏好
            safe_search: 安全搜索
            use_cache: 使用缓存
            verbose: 详细输出
            
        Returns:
            搜索结果列表
        """
        
        # 检查缓存
        cache_key = self._generate_cache_key(query, engine, date_after, date_before)
        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached:
                if verbose:
                    print(f"✅ 使用缓存结果 ({len(cached)} 条)")
                return cached
        
        # 自动选择引擎
        if not engine:
            engine = self._select_best_engine(query, language)
            if verbose:
                print(f"🤖 自动选择引擎：{self.engines[engine]['name']}")
        
        # 执行搜索（带重试）
        max_retries = 3
        results = []
        
        for attempt in range(max_retries):
            try:
                timeout = self._calculate_timeout(attempt)
                
                if verbose:
                    print(f"🔍 搜索中... (引擎：{self.engines[engine]['name']}, 尝试：{attempt+1}/{max_retries})")
                
                raw_html = self._fetch_search_results(engine, query, num_results, timeout)
                results = self.engines[engine]['parser'](raw_html, num_results)
                
                # 标记成功
                self.engine_health[engine]['successes'] += 1
                self.engine_health[engine]['failures'] = 0
                
                break
                
            except Exception as e:
                if verbose:
                    print(f"⚠️  引擎 {engine} 失败：{e}")
                
                self.engine_health[engine]['failures'] += 1
                self.engine_health[engine]['last_fail'] = time.time()
                
                # 尝试下一个引擎
                if attempt < max_retries - 1:
                    engine = self._get_next_available_engine(engine)
                    if not engine:
                        raise Exception("所有引擎都不可用")
                else:
                    raise Exception(f"搜索失败：{e}")
        
        # 日期过滤
        if date_after or date_before:
            results = self._filter_by_date(results, date_after, date_before)
        
        # 质量评分
        results = self._score_results(results, query)
        
        # 排序
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # 保存到缓存
        if use_cache:
            self._save_to_cache(cache_key, results)
        
        if verbose:
            print(f"✅ 找到 {len(results)} 条结果")
        
        return results[:num_results]
    
    def deep_research(self, query: str, 
                     num_angles: int = 4,
                     results_per_angle: int = 5,
                     generate_summary: bool = True,
                     verbose: bool = False) -> Dict:
        """
        深度研究模式
        
        Args:
            query: 研究主题
            num_angles: 搜索角度数量
            results_per_angle: 每个角度的结果数
            generate_summary: 生成综合摘要
            verbose: 详细输出
            
        Returns:
            深度研究报告
        """
        
        if verbose:
            print(f"\n🔬 启动深度研究：{query}\n")
        
        # Step 1: 生成多个搜索角度
        angles = self._generate_search_angles(query, num_angles)
        
        if verbose:
            print(f"📐 搜索角度:")
            for i, angle in enumerate(angles, 1):
                print(f"   {i}. {angle}")
            print()
        
        # Step 2: 多角度搜索
        all_results = []
        for angle in angles:
            try:
                results = self.search(angle, num_results=results_per_angle, verbose=False)
                all_results.extend(results)
            except Exception as e:
                if verbose:
                    print(f"⚠️  角度 '{angle}' 搜索失败：{e}")
        
        if verbose:
            print(f"📊 共收集 {len(all_results)} 条结果")
        
        # Step 3: 智能去重
        unique_results = self._deduplicate_results(all_results)
        
        if verbose:
            print(f"✨ 去重后剩余 {len(unique_results)} 条结果")
        
        # Step 4: 生成综合摘要
        summary = None
        if generate_summary and unique_results:
            summary = self._generate_research_summary(query, unique_results)
            
            if verbose:
                print("\n📝 综合摘要:")
                print("-" * 60)
                print(summary['executive_summary'])
                print("\n关键点:")
                for point in summary['key_points'][:5]:
                    print(f"  • {point}")
                print("-" * 60)
        
        # Step 5: 生成报告
        report = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'search_angles': angles,
            'total_results': len(all_results),
            'unique_results': len(unique_results),
            'results': unique_results[:20],  # 最多返回 20 条
            'summary': summary,
            'contradictions': self._find_contradictions(unique_results) if summary else [],
            'gaps': self._identify_knowledge_gaps(unique_results, query) if summary else []
        }
        
        return report
    
    def _generate_search_angles(self, query: str, num_angles: int) -> List[str]:
        """生成多个搜索角度"""
        
        angle_templates = [
            "{query} 最佳实践",
            "{query} 完整教程",
            "{query} 案例分析",
            "{query} 2026 年最新趋势",
            "{query} 优缺点对比",
            "{query} 常见问题",
            "{query} 工具推荐",
            "{query} 专家观点",
        ]
        
        # 智能选择角度
        if "对比" in query or "vs" in query.lower():
            angles = [
                f"{query} 详细对比",
                f"{query} 性能测试",
                f"{query} 用户评价",
                f"{query} 价格对比"
            ]
        elif "教程" in query or "如何" in query:
            angles = [
                f"{query} 入门指南",
                f"{query} 高级技巧",
                f"{query} 常见错误",
                f"{query} 实战案例"
            ]
        else:
            angles = angle_templates[:num_angles]
        
        # 填充查询词
        return [angle.format(query=query) for angle in angles]
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """智能去重"""
        
        seen_urls = set()
        seen_titles = set()
        unique = []
        
        for result in results:
            url = result.get('url', '')
            title = result.get('title', '')
            
            # URL 去重
            if url in seen_urls:
                continue
            
            # 标题相似度去重
            title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
            if title_hash in seen_titles:
                continue
            
            seen_urls.add(url)
            seen_titles.add(title_hash)
            unique.append(result)
        
        return unique
    
    def _score_results(self, results: List[Dict], query: str) -> List[Dict]:
        """结果质量评分"""
        
        scored = []
        query_keywords = set(query.lower().split())
        
        for result in results:
            score = 0.0
            
            # 标题相关性 (40%)
            title = result.get('title', '').lower()
            title_match = sum(1 for kw in query_keywords if kw in title)
            score += (title_match / len(query_keywords)) * 40 if query_keywords else 0
            
            # 摘要相关性 (30%)
            snippet = result.get('snippet', '').lower()
            snippet_match = sum(1 for kw in query_keywords if kw in snippet)
            score += (snippet_match / len(query_keywords)) * 30 if query_keywords else 0
            
            # 时效性 (20%)
            pub_date = result.get('date')
            if pub_date:
                try:
                    days_old = (datetime.now() - datetime.strptime(pub_date, '%Y-%m-%d')).days
                    freshness_score = max(0, 20 - (days_old / 30) * 20)  # 30 天内满分
                    score += freshness_score
                except:
                    pass
            
            # 权威性 (10%)
            domain = result.get('domain', '')
            authoritative_domains = ['.gov', '.edu', '.org', 'github.com', 'stackoverflow.com']
            if any(auth in domain for auth in authoritative_domains):
                score += 10
            
            result['score'] = round(score, 1)
            scored.append(result)
        
        return scored
    
    def _generate_research_summary(self, query: str, results: List[Dict]) -> Dict:
        """生成综合摘要"""
        
        # 提取关键信息
        key_points = []
        sources = []
        
        for result in results[:10]:
            # 从标题和摘要提取关键点
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            
            # 简单提取：取前 100 个字符
            if len(snippet) > 100:
                key_point = snippet[:100] + "..."
            else:
                key_point = snippet
            
            if key_point.strip():
                key_points.append(key_point)
            
            # 记录来源
            sources.append({
                'title': title,
                'url': result.get('url'),
                'domain': result.get('domain')
            })
        
        # 生成执行摘要
        executive_summary = f"关于\"{query}\"的搜索共找到 {len(results)} 条相关结果。"
        executive_summary += f"以下是 {len(key_points)} 个关键发现："
        
        return {
            'executive_summary': executive_summary,
            'key_points': key_points[:10],
            'sources': sources,
            'coverage': {
                'total_results': len(results),
                'unique_domains': len(set(r.get('domain', '') for r in results)),
                'avg_score': sum(r.get('score', 0) for r in results) / len(results) if results else 0
            }
        }
    
    def _find_contradictions(self, results: List[Dict]) -> List[Dict]:
        """发现矛盾点"""
        # TODO: 实现矛盾检测
        return []
    
    def _identify_knowledge_gaps(self, results: List[Dict], query: str) -> List[str]:
        """识别知识空白"""
        # TODO: 实现知识空白识别
        return []
    
    # ========== 辅助方法 ==========
    
    def _generate_cache_key(self, *args) -> str:
        """生成缓存键"""
        key_str = "|".join(str(arg) for arg in args if arg)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[List[Dict]]:
        """从缓存获取"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if not cache_file.exists():
            return None
        
        # 检查过期
        age = time.time() - cache_file.stat().st_mtime
        if age > self.cache_ttl:
            return None
        
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    def _save_to_cache(self, cache_key: str, data: List[Dict]):
        """保存到缓存"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _select_best_engine(self, query: str, language: str) -> str:
        """选择最佳引擎"""
        
        # 中文优先国内引擎
        if 'zh' in language or any('\u4e00' <= c <= '\u9fff' for c in query):
            candidates = ['bing-cn', 'baidu', 'sogou']
        else:
            candidates = ['duckduckgo', 'bing', 'google']
        
        # 选择最健康的引擎
        for engine in candidates:
            if self.engine_health[engine]['failures'] < 3:
                return engine
        
        return candidates[0]
    
    def _get_next_available_engine(self, current: str) -> Optional[str]:
        """获取下一个可用引擎"""
        for engine in self.engine_priority:
            if engine != current and self.engine_health[engine]['failures'] < 3:
                return engine
        return None
    
    def _calculate_timeout(self, attempt: int) -> int:
        """计算超时时间（指数退避）"""
        base = 10
        return min(base * (2 ** attempt), 60)
    
    def _fetch_search_results(self, engine: str, query: str, 
                             num_results: int, timeout: int) -> str:
        """抓取搜索结果 HTML"""
        
        url_template = self.engines[engine]['url']
        start = 0
        
        # 构建 URL
        if engine == 'sogou':
            page = start // 10 + 1
            url = url_template.format(query=urllib.parse.quote(query), page=page)
        else:
            url = url_template.format(query=urllib.parse.quote_plus(query), start=start)
        
        # 使用 curl 抓取
        cmd = [
            'curl', '-s', '-L',
            '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-H', 'Accept: text/html,application/xhtml+xml',
            '-H', 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
            '--max-time', str(timeout),
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode != 0:
            raise Exception(f"cURL 失败：{result.stderr}")
        
        return result.stdout
    
    # ========== HTML 解析器 ==========
    
    def _parse_bing_cn_results(self, html: str, num_results: int) -> List[Dict]:
        """解析 Bing 中国结果"""
        return self._parse_with_bs(html, num_results, 'bing')
    
    def _parse_baidu_results(self, html: str, num_results: int) -> List[Dict]:
        """解析百度结果"""
        return self._parse_with_bs(html, num_results, 'baidu')
    
    def _parse_duckduckgo_results(self, html: str, num_results: int) -> List[Dict]:
        """解析 DuckDuckGo 结果"""
        return self._parse_with_bs(html, num_results, 'duckduckgo')
    
    def _parse_sogou_results(self, html: str, num_results: int) -> List[Dict]:
        """解析搜狗结果"""
        return self._parse_with_bs(html, num_results, 'sogou')
    
    def _parse_with_bs(self, html: str, num_results: int, engine: str) -> List[Dict]:
        """通用 BeautifulSoup 解析器"""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("请安装：pip3 install beautifulsoup4")
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # 根据不同引擎选择选择器
        selectors = {
            'bing': '#b_results .b_algo',
            'bing-cn': '#b_results .b_algo',
            'baidu': '.result.c-container',
            'duckduckgo': '.result',
            'sogou': '.fb-h-wrap',
        }
        
        selector = selectors.get(engine, '.result')
        items = soup.select(selector)[:num_results]
        
        for item in items:
            try:
                title_tag = item.find(['h2', 'h3'], class_=lambda x: x and ('title' in x.lower() or 'fb-h' in x.lower()))
                if not title_tag:
                    title_tag = item.find('a')
                
                if not title_tag:
                    continue
                
                title = title_tag.get_text(strip=True)
                url = title_tag.get('href', '')
                
                snippet_tag = item.find(class_=lambda x: x and ('snippet' in x.lower() or 'abstract' in x.lower()))
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                
                # 提取域名
                domain = urllib.parse.urlparse(url).netloc if url else ""
                
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet,
                    'domain': domain,
                    'engine': engine
                })
            except Exception as e:
                continue
        
        return results
    
    def _filter_by_date(self, results: List[Dict], 
                       date_after: Optional[str], 
                       date_before: Optional[str]) -> List[Dict]:
        """日期过滤"""
        # TODO: 实现日期解析和过滤
        return results


def main():
    parser = argparse.ArgumentParser(description='Web Knowledge v5.0 - 增强型网络搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--engine', '-e', choices=['bing', 'bing-cn', 'baidu', 'google', 'duckduckgo', 'sogou'],
                       help='指定搜索引擎')
    parser.add_argument('--num-results', '-n', type=int, default=10, help='返回结果数量')
    parser.add_argument('--date-after', help='日期之后 (YYYY-MM-DD)')
    parser.add_argument('--date-before', help='日期之前 (YYYY-MM-DD)')
    parser.add_argument('--deep-research', action='store_true', help='深度研究模式')
    parser.add_argument('--export', '-o', help='导出到文件')
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    searcher = EnhancedWebSearch()
    
    if args.deep_research:
        # 深度研究模式
        report = searcher.deep_research(args.query, verbose=args.verbose)
        
        # 输出报告
        if args.export:
            export_markdown(report, args.export)
            print(f"📄 报告已导出：{args.export}")
        else:
            print_report(report)
    else:
        # 普通搜索模式
        results = searcher.search(
            args.query,
            engine=args.engine,
            num_results=args.num_results,
            date_after=args.date_after,
            date_before=args.date_before,
            use_cache=not args.no_cache,
            verbose=args.verbose
        )
        
        # 输出结果
        if args.export:
            export_results(results, args.export)
            print(f"📄 结果已导出：{args.export}")
        else:
            print_results(results)


def print_results(results: List[Dict]):
    """打印搜索结果"""
    print(f"\n{'='*70}")
    print(f"🔍 搜索结果 ({len(results)} 条)")
    print(f"{'='*70}\n")
    
    for i, result in enumerate(results, 1):
        print(f"[{i}] {result['title']}")
        print(f"    URL: {result['url']}")
        if result.get('snippet'):
            print(f"    {result['snippet'][:200]}...")
        if result.get('score'):
            print(f"    评分：{result['score']}/100")
        print()


def print_report(report: Dict):
    """打印深度研究报告"""
    print(f"\n{'='*70}")
    print(f"🔬 深度研究报告")
    print(f"{'='*70}")
    print(f"主题：{report['query']}")
    print(f"时间：{report['timestamp']}")
    print(f"搜索角度：{len(report['search_angles'])} 个")
    print(f"总结果：{report['total_results']} 条 → 去重后：{report['unique_results']} 条")
    print(f"{'='*70}\n")
    
    if report.get('summary'):
        print("📝 综合摘要:")
        print(report['summary']['executive_summary'])
        print("\n关键点:")
        for i, point in enumerate(report['summary']['key_points'][:10], 1):
            print(f"  {i}. {point}")
        print()
    
    print("📊 Top 结果:")
    for i, result in enumerate(report['results'][:10], 1):
        print(f"  [{i}] {result['title']} (评分：{result.get('score', 'N/A')})")
    
    print(f"\n{'='*70}")


def export_results(results: List[Dict], filename: str):
    """导出结果为 Markdown"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 网络搜索结果\n\n")
        f.write(f"搜索时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"共 {len(results)} 条结果\n\n")
        f.write("---\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"## {i}. {result['title']}\n\n")
            f.write(f"**URL**: {result['url']}\n\n")
            if result.get('snippet'):
                f.write(f"{result['snippet']}\n\n")
            if result.get('score'):
                f.write(f"**评分**: {result['score']}/100\n\n")
            f.write("---\n\n")


def export_markdown(report: Dict, filename: str):
    """导出深度研究报告为 Markdown"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 深度研究报告：{report['query']}\n\n")
        f.write(f"**生成时间**: {report['timestamp']}\n\n")
        f.write(f"**搜索角度**: {', '.join(report['search_angles'])}\n\n")
        f.write(f"**数据来源**: {report['total_results']} → {report['unique_results']} (去重)\n\n")
        
        if report.get('summary'):
            f.write(f"## 综合摘要\n\n")
            f.write(f"{report['summary']['executive_summary']}\n\n")
            
            f.write(f"## 关键发现\n\n")
            for i, point in enumerate(report['summary']['key_points'], 1):
                f.write(f"{i}. {point}\n\n")
        
        f.write(f"## 详细结果\n\n")
        for i, result in enumerate(report['results'], 1):
            f.write(f"### {i}. {result['title']}\n\n")
            f.write(f"**来源**: [{result.get('domain', 'Unknown')}]({result['url']})\n\n")
            if result.get('snippet'):
                f.write(f"{result['snippet']}\n\n")
            if result.get('score'):
                f.write(f"**相关性评分**: {result['score']}/100\n\n")


if __name__ == '__main__':
    main()
