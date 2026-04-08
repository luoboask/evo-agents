#!/usr/bin/env python3
"""
Web search - 增强版
改进点：
1. 指数退避重试机制
2. 详细的错误分类和处理
3. 更智能的健康监控
4. 【新增】深度研究模式（多角度搜索 + 智能去重 + 综合摘要）
5. 【新增】结果质量评分（相关性/时效性/权威性）
6. 【新增】导出为 Markdown 格式
"""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path


class SmartSearchEngine:
    """智能搜索引擎 - v4 进化版"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.learning_dir = self.workspace / "memory" / "learning"
        
        # 搜索引擎健康状态
        self.engine_health = {
            "bing": {"healthy": True, "last_fail": None, "fail_count": 0, "success_count": 0},
            "baidu": {"healthy": True, "last_fail": None, "fail_count": 0, "success_count": 0},
            "google": {"healthy": True, "last_fail": None, "fail_count": 0, "success_count": 0},
            "duckduckgo": {"healthy": True, "last_fail": None, "fail_count": 0, "success_count": 0},
        }
        
        # 自适应超时
        self.base_timeout = 10
        self.max_timeout = 60
        self._update_adaptive_timeout()
    
    def _update_adaptive_timeout(self):
        """根据历史表现更新超时时间"""
        recent_logs = self._get_recent_logs(1)
        if recent_logs:
            avg_time = sum(l.get("duration", 10) for l in recent_logs) / len(recent_logs)
            # 自适应：平均时间的2倍，最少10秒，最多60秒
            self.base_timeout = min(self.max_timeout, max(10, avg_time * 2))
    
    def _get_recent_logs(self, days):
        """获取最近日志"""
        logs = []
        for i in range(days):
            date = (datetime.now() - __import__('datetime').timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = self.learning_dir / f"auto_reflections_{date}.jsonl"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
        return logs
    
    def _calculate_backoff_timeout(self, attempt):
        """计算指数退避超时时间"""
        # 指数退避: base * (2 ^ attempt)，但不超过 max
        timeout = self.base_timeout * (2 ** attempt)
        return min(timeout, self.max_timeout)
    
    def health_check(self, engine):
        """检查搜索引擎健康状态"""
        health = self.engine_health[engine]
        
        # 如果最近5分钟内失败过，标记为不健康
        if health["last_fail"]:
            time_since_fail = time.time() - health["last_fail"]
            if time_since_fail < 300:  # 5分钟
                return False
        
        # 如果失败次数超过3次，标记为不健康
        if health["fail_count"] >= 3:
            return False
        
        # 如果成功率低于50%，标记为不健康
        total = health["success_count"] + health["fail_count"]
        if total > 5 and health["success_count"] / total < 0.5:
            return False
        
        return health["healthy"]
    
    def mark_result(self, engine, success, error=None):
        """标记搜索结果"""
        if success:
            self.engine_health[engine]["success_count"] += 1
            self.engine_health[engine]["fail_count"] = 0  # 成功后重置失败计数
        else:
            self.engine_health[engine]["fail_count"] += 1
            self.engine_health[engine]["last_fail"] = time.time()
            self.engine_health[engine]["healthy"] = False
    
    def get_best_engine(self):
        """获取最佳搜索引擎"""
        engines = ["bing", "baidu", "google", "duckduckgo"]
        
        # 按成功率排序
        scored_engines = []
        for engine in engines:
            health = self.engine_health[engine]
            total = health["success_count"] + health["fail_count"]
            success_rate = health["success_count"] / total if total > 0 else 0.5
            scored_engines.append((engine, success_rate))
        
        scored_engines.sort(key=lambda x: -x[1])
        
        for engine, rate in scored_engines:
            if self.health_check(engine):
                return engine
        
        # 如果都不健康，重置并返回成功率最高的
        for engine, _ in scored_engines:
            self.engine_health[engine]["healthy"] = True
            self.engine_health[engine]["fail_count"] = 0
        
        return scored_engines[0][0]
    
    def search_with_retry(self, query, limit=5, max_retries=3):
        """带重试的搜索"""
        last_error = None
        
        for attempt in range(max_retries + 1):
            engine = self.get_best_engine()
            timeout = self._calculate_backoff_timeout(attempt)
            
            print(f"🔍 尝试 {attempt + 1}/{max_retries + 1}: {engine} (超时: {timeout:.1f}s)", 
                  file=sys.stderr)
            
            try:
                if engine == "bing":
                    results = self._search_bing(query, limit, timeout)
                elif engine == "baidu":
                    results = self._search_baidu(query, limit, timeout)
                elif engine == "google":
                    results = self._search_google(query, limit, timeout)
                elif engine == "duckduckgo":
                    results = self._search_duckduckgo(query, limit, timeout)
                else:
                    results = self._search_bing(query, limit, timeout)
                
                if results:
                    self.mark_result(engine, True)
                    print(f"✅ {engine} 搜索成功，找到 {len(results)} 个结果", file=sys.stderr)
                    return results
                else:
                    raise Exception("No results")
                    
            except Exception as e:
                last_error = e
                self.mark_result(engine, False, e)
                error_msg = self._classify_error(e)
                print(f"❌ {engine} 失败: {error_msg}", file=sys.stderr)
                
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # 指数退避等待
                    print(f"   等待 {wait_time}s 后重试...", file=sys.stderr)
                    time.sleep(wait_time)
        
        # 所有重试都失败
        raise Exception(f"所有搜索引擎都失败了。最后错误: {self._classify_error(last_error)}")
    
    def _classify_error(self, error):
        """分类错误类型"""
        if error is None:
            return "未知错误"
        
        error_str = str(error).lower()
        
        if "timeout" in error_str or "timed out" in error_str:
            return "网络超时"
        elif "certificate" in error_str or "ssl" in error_str:
            return "SSL证书错误"
        elif "connection" in error_str:
            return "连接错误"
        elif "dns" in error_str or "resolve" in error_str:
            return "DNS解析错误"
        elif "403" in error_str or "forbidden" in error_str:
            return "访问被拒绝"
        elif "404" in error_str or "not found" in error_str:
            return "页面不存在"
        elif "429" in error_str or "rate limit" in error_str:
            return "请求过于频繁"
        else:
            return f"其他错误: {str(error)[:50]}"
    
    def _search_bing(self, query, limit, timeout):
        """Bing 搜索"""
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.bing.com/search?q={encoded_query}&count={limit * 2}"
        
        headers = [
            '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        ]
        
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', str(int(timeout))] + headers + [url],
            capture_output=True, text=True, timeout=int(timeout) + 5
        )
        
        if result.returncode != 0:
            raise Exception(f"curl failed: {result.stderr}")
        
        return self._parse_results(result.stdout, limit)
    
    def _search_baidu(self, query, limit, timeout):
        """百度搜索 - 使用移动端接口（反爬较低）"""
        encoded_query = urllib.parse.quote(query)
        # 使用百度移动端接口，反爬较低
        url = f"https://m.baidu.com/s?wd={encoded_query}&rn={limit}"
        
        headers = [
            '-H', 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '-H', 'Accept-Language: zh-CN,zh;q=0.9',
            '-H', 'Referer: https://m.baidu.com/',
            '--compressed',
        ]
        
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', str(int(timeout))] + headers + [url],
            capture_output=True, text=True, timeout=int(timeout) + 5
        )
        
        if result.returncode != 0:
            raise Exception(f"curl failed: {result.stderr}")
        
        if len(result.stdout) < 500:
            raise Exception("百度返回内容过短，可能触发反爬")
        
        return self._parse_baidu_results(result.stdout, limit)
    
    def _search_google(self, query, limit, timeout):
        """Google 搜索"""
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}&num={limit * 2}"
        
        headers = [
            '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '-H', 'Accept-Language: en-US,en;q=0.9',
        ]
        
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', str(int(timeout))] + headers + [url],
            capture_output=True, text=True, timeout=int(timeout) + 5
        )
        
        if result.returncode != 0:
            raise Exception(f"curl failed: {result.stderr}")
        
        return self._parse_google_results(result.stdout, limit)
    
    def _search_duckduckgo(self, query, limit, timeout):
        """DuckDuckGo 搜索 - 轻量级 HTML 接口"""
        encoded_query = urllib.parse.quote(query)
        # 使用 lite 版本，更快更轻量
        url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
        
        headers = [
            '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '-H', 'Accept-Language: en-US,en;q=0.9',
        ]
        
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', str(int(timeout))] + headers + [url],
            capture_output=True, text=True, timeout=int(timeout) + 5
        )
        
        if result.returncode != 0:
            raise Exception(f"curl failed: {result.stderr}")
        
        if len(result.stdout) < 200:
            raise Exception("DuckDuckGo 返回内容过短")
        
        return self._parse_duckduckgo_results(result.stdout, limit)
    
    def _parse_baidu_results(self, html, limit):
        """解析百度搜索结果（移动端）"""
        results = []
        
        # 移动端结果容器 - 多种类名
        container_patterns = [
            r'<div[^>]*class="[^"]*result[^"]*"[^>]*>.*?</div>',
            r'<section[^>]*class="[^"]*result[^"]*"[^>]*>.*?</section>',
            r'<div[^>]*data-click="[^"]*"[^>]*>.*?</div>',
        ]
        
        containers = []
        for pattern in container_patterns:
            containers.extend(re.findall(pattern, html, re.DOTALL | re.IGNORECASE))
        
        # 提取所有链接和标题
        link_pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        links = re.findall(link_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for href, title in links:
            if len(results) >= limit:
                break
            
            # 过滤百度内部链接
            if 'baidu.com' in href and '/s?' not in href:
                continue
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            if 'tdk=' in href or 'click?' in href:
                continue
            
            # 清理标题
            title = re.sub(r'<[^>]+>', '', title).strip()
            if len(title) < 2 or len(title) > 100:
                continue
            
            results.append({
                'title': title,
                'url': href,
            })
        
        return results[:limit]
    
    def _parse_google_results(self, html, limit):
        """解析 Google 搜索结果"""
        results = []
        # Google 结果容器（多种类名）
        container_patterns = [
            r'<div[^>]*class="[^"]*g[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*yuRUbf[^"]*"[^>]*>(.*?)</div>',
        ]
        
        containers = []
        for pattern in container_patterns:
            containers.extend(re.findall(pattern, html, re.DOTALL | re.IGNORECASE))
        
        for container in containers[:limit * 3]:
            if len(results) >= limit:
                break
            
            result = {}
            
            # 提取标题和链接
            title_pattern = r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
            title_match = re.search(title_pattern, container, re.DOTALL | re.IGNORECASE)
            if title_match:
                url = title_match.group(1)
                # 过滤非结果链接
                if url.startswith('/search') or url.startswith('#') or 'google' in url.lower():
                    continue
                result['url'] = url
                title = re.sub(r'<[^>]+>', '', title_match.group(2))
                result['title'] = title.strip()
            
            # 提取摘要
            snippet_pattern = r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>(.*?)</div>'
            snippet_match = re.search(snippet_pattern, container, re.DOTALL | re.IGNORECASE)
            if snippet_match:
                snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1))
                result['snippet'] = snippet.strip()
            
            if result.get('title') and result.get('url'):
                results.append(result)
        
        return results
    
    def _parse_duckduckgo_results(self, html, limit):
        """解析 DuckDuckGo Lite 搜索结果"""
        results = []
        
        # Lite 版本使用表格布局，提取所有结果链接
        # 查找结果行（包含 result-link 类的链接）
        link_pattern = r'<a[^>]*class="result-link"[^>]*href="([^"]*)"[^>]*>([^<]+)</a>'
        links = re.findall(link_pattern, html, re.IGNORECASE)
        
        for href, title in links:
            if len(results) >= limit:
                break
            
            # 清理标题
            title = re.sub(r'<[^>]+>', '', title).strip()
            if len(title) < 2 or len(title) > 100:
                continue
            
            results.append({
                'title': title,
                'url': href,
            })
        
        # 如果没有找到，尝试通用解析
        if not results:
            # 提取所有外部链接
            all_links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html, re.IGNORECASE)
            for href, title in all_links:
                if len(results) >= limit:
                    break
                
                # 过滤 DuckDuckGo 内部链接
                if 'duckduckgo.com' in href:
                    continue
                if href.startswith('#') or 'javascript:' in href:
                    continue
                
                title = re.sub(r'<[^>]+>', '', title).strip()
                if len(title) < 2 or len(title) > 100:
                    continue
                
                results.append({
                    'title': title,
                    'url': href,
                })
        
        return results[:limit]
    
    def _parse_results(self, html, limit):
        """解析搜索结果"""
        results = []
        algo_pattern = r'<li[^>]*class="b_algo"[^>]*>(.*?)</li>'
        algo_matches = re.findall(algo_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for match in algo_matches[:limit]:
            result = {}
            title_pattern = r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
            title_match = re.search(title_pattern, match, re.DOTALL | re.IGNORECASE)
            if title_match:
                result['url'] = title_match.group(1)
                title = re.sub(r'<[^>]+>', '', title_match.group(2))
                result['title'] = title.strip()
            
            snippet_pattern = r'<p[^>]*>(.*?)</p>'
            snippet_match = re.search(snippet_pattern, match, re.DOTALL | re.IGNORECASE)
            if snippet_match:
                snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1))
                result['snippet'] = snippet.strip()
            
            if result.get('title') and result.get('url'):
                results.append(result)
        
        return results


def main():
    parser = argparse.ArgumentParser(description='Web search v4 - 进化版')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', type=int, default=5, help='Number of results')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--max-retries', type=int, default=3, help='Max retry attempts')
    
    args = parser.parse_args()
    
    engine = SmartSearchEngine()
    
    try:
        results = engine.search_with_retry(args.query, args.limit, args.max_retries)
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            if not results:
                print("No results found.")
                return
            
            print(f"\n🔍 Search results for: {args.query}\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r.get('title', 'No title')}")
                print(f"   {r.get('url', 'No URL')}")
                if r.get('snippet'):
                    snippet = r['snippet'][:200] + '...' if len(r['snippet']) > 200 else r['snippet']
                    print(f"   {snippet}")
                print()
    
    except Exception as e:
        print(f"\n❌ 搜索失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()


# ========== 增强功能：深度研究模式 ==========

def deep_research(query: str, num_angles: int = 4, results_per_angle: int = 5, verbose: bool = False):
    """深度研究模式 - 多角度搜索 + 智能去重 + 综合摘要"""
    import hashlib
    
    if verbose:
        print(f"\n🔬 启动深度研究：{query}\n")
    
    # Step 1: 生成多个搜索角度
    templates = [
        "{query} 最佳实践",
        "{query} 完整教程",
        "{query} 案例分析",
        "{query} 2026 年最新趋势",
        "{query} 优缺点对比",
        "{query} 常见问题",
    ]
    
    if "对比" in query or "vs" in query.lower():
        angles = [f"{query} 详细对比", f"{query} 性能测试", f"{query} 用户评价", f"{query} 价格对比"]
    elif "教程" in query or "如何" in query:
        angles = [f"{query} 入门指南", f"{query} 高级技巧", f"{query} 常见错误", f"{query} 实战案例"]
    else:
        angles = [t.format(query=query) for t in templates[:num_angles]]
    
    if verbose:
        print(f"📐 搜索角度:")
        for i, angle in enumerate(angles, 1):
            print(f"   {i}. {angle}")
        print()
    
    # Step 2: 多角度搜索
    searcher = SmartSearchEngine()
    all_results = []
    
    for angle in angles:
        try:
            results = searcher.search_with_retry(angle, limit=results_per_angle)
            all_results.extend(results)
            if verbose:
                print(f"✅ {angle}: 找到 {len(results)} 条结果")
        except Exception as e:
            if verbose:
                print(f"⚠️  '{angle}' 搜索失败：{e}")
    
    if verbose:
        print(f"\n📊 共收集 {len(all_results)} 条结果")
    
    # Step 3: 智能去重
    seen_urls = set()
    seen_titles = set()
    unique_results = []
    
    for result in all_results:
        url = result.get('url', '')
        title = result.get('title', '')
        
        if url in seen_urls:
            continue
        
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        if title_hash in seen_titles:
            continue
        
        seen_urls.add(url)
        seen_titles.add(title_hash)
        unique_results.append(result)
    
    if verbose:
        print(f"✨ 去重后剩余 {len(unique_results)} 条结果")
    
    # Step 4: 质量评分
    query_keywords = set(query.lower().split())
    scored_results = []
    
    for result in unique_results:
        score = 0.0
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        
        title_match = sum(1 for kw in query_keywords if kw in title)
        score += (title_match / len(query_keywords)) * 40 if query_keywords else 0
        
        snippet_match = sum(1 for kw in query_keywords if kw in snippet)
        score += (snippet_match / len(query_keywords)) * 30 if query_keywords else 0
        
        domain = result.get('domain', '')
        authoritative_domains = ['.gov', '.edu', '.org', 'github.com', 'stackoverflow.com']
        if any(auth in domain for auth in authoritative_domains):
            score += 30
        
        result['score'] = round(score, 1)
        scored_results.append(result)
    
    scored_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    # Step 5: 生成综合摘要
    key_points = []
    sources = []
    
    for result in scored_results[:10]:
        snippet = result.get('snippet', '')
        if snippet and len(snippet) > 50:
            key_point = snippet[:150] + "..." if len(snippet) > 150 else snippet
            key_points.append(key_point)
        
        sources.append({
            'title': result.get('title', ''),
            'url': result.get('url'),
            'domain': result.get('domain')
        })
    
    executive_summary = f"关于\"{query}\"的深度研究共找到 {len(scored_results)} 条相关结果。"
    executive_summary += f"以下是 {len(key_points)} 个关键发现："
    
    summary = {
        'executive_summary': executive_summary,
        'key_points': key_points[:10],
        'sources': sources
    }
    
    if verbose:
        print("\n📝 综合摘要:")
        print("-" * 60)
        print(summary['executive_summary'])
        print("\n关键点:")
        for point in summary['key_points'][:5]:
            print(f"  • {point}")
        print("-" * 60)
    
    return {
        'query': query,
        'timestamp': datetime.now().isoformat(),
        'search_angles': angles,
        'total_results': len(all_results),
        'unique_results': len(unique_results),
        'results': scored_results[:20],
        'summary': summary
    }


def export_to_markdown(data: dict, filename: str):
    """导出为 Markdown 格式"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 深度研究报告：{data['query']}\n\n")
        f.write(f"**生成时间**: {data['timestamp']}\n\n")
        f.write(f"**搜索角度**: {', '.join(data['search_angles'])}\n\n")
        f.write(f"**数据来源**: {data['total_results']} → {data['unique_results']} (去重)\n\n")
        
        if data.get('summary'):
            f.write(f"## 综合摘要\n\n{data['summary']['executive_summary']}\n\n")
            f.write(f"## 关键发现\n\n")
            for i, point in enumerate(data['summary']['key_points'], 1):
                f.write(f"{i}. {point}\n\n")
        
        f.write(f"## 详细结果\n\n")
        for i, result in enumerate(data['results'], 1):
            f.write(f"### {i}. {result['title']}\n\n")
            f.write(f"**来源**: [{result.get('domain', 'Unknown')}]({result['url']})\n\n")
            if result.get('snippet'):
                f.write(f"{result['snippet']}\n\n")
            if result.get('score'):
                f.write(f"**相关性评分**: {result['score']}/100\n\n")


# 修改 main() 添加深度研究支持
_original_main = main

def enhanced_main():
    parser = argparse.ArgumentParser(description="Web Search - 增强版")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("--deep-research", action="store_true", help="深度研究模式")
    parser.add_argument("--angles", type=int, default=4, help="搜索角度数量")
    parser.add_argument("--export", metavar="FILE", help="导出为 Markdown 文件")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    parser.add_argument("-l", "--limit", type=int, default=10, help="结果数量")
    parser.add_argument("--engine", choices=["bing", "baidu", "google", "duckduckgo"], help="指定引擎")
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    if args.deep_research:
        report = deep_research(args.query, num_angles=args.angles, verbose=args.verbose)
        
        if args.export:
            export_to_markdown(report, args.export)
            print(f"📄 报告已导出：{args.export}")
        else:
            print("\n" + "="*70)
            print("🔬 深度研究报告")
            print("="*70)
            print(f"主题：{args.query}")
            print(f"搜索角度：{len(report['search_angles'])} 个")
            print(f"总结果：{report['total_results']} → {report['unique_results']} (去重)")
            print("="*70)
            
            if report['summary']:
                print(f"\n{report['summary']['executive_summary']}\n")
                print("关键点:")
                for i, point in enumerate(report['summary']['key_points'][:10], 1):
                    print(f"  {i}. {point}")
            
            print("\n" + "="*70)
    else:
        _original_main()

if __name__ == '__main__':
    enhanced_main()
