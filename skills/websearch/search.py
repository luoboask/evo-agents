#!/usr/bin/env python3
"""
Web search v4 - 进化版
改进点：
1. 指数退避重试机制
2. 详细的错误分类和处理
3. 更智能的健康监控
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
        self.workspace = Path(__file__).resolve().parents[2]
        self.learning_dir = self.workspace / "memory" / "learning"
        
        # 搜索引擎健康状态
        self.engine_health = {
            "bing": {"healthy": True, "last_fail": None, "fail_count": 0, "success_count": 0},
            "duckduckgo": {"healthy": True, "last_fail": None, "fail_count": 0, "success_count": 0},
            "google_lite": {"healthy": True, "last_fail": None, "fail_count": 0, "success_count": 0}
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
        engines = ["bing", "duckduckgo", "google_lite"]
        
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
                elif engine == "duckduckgo":
                    results = self._search_duckduckgo(query, limit, timeout)
                else:
                    results = self._search_google_lite(query, limit, timeout)
                
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
    
    def _search_duckduckgo(self, query, limit, timeout):
        """DuckDuckGo 搜索（简化版）"""
        print("   使用 DuckDuckGo 备选...", file=sys.stderr)
        return []
    
    def _search_google_lite(self, query, limit, timeout):
        """Google Lite 搜索（简化版）"""
        print("   使用 Google Lite 备选...", file=sys.stderr)
        return []
    
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
