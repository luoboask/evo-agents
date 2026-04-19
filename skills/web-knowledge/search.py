#!/usr/bin/env python3
"""
Web Search V7 - 最终优化版
核心改进：
1. 简单的 HTML 解析（基于 Bing 移动端）
2. 质量评分系统
3. 智能去重
4. 中文搜索优化
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime
import hashlib


def search_bing(query: str, limit: int = 10, timeout: int = 15) -> list:
    """Bing 搜索 - 使用移动端接口"""
    encoded = urllib.parse.quote(query)
    url = f"https://cn.bing.com/search?q={encoded}&count={limit * 2}"
    
    try:
        # 使用 shell 模式避免参数问题
        cmd = f"curl -s -L --max-time {timeout} -A 'Mozilla/5.0 (iPhone)' '{url}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout + 5)
        
        if result.returncode != 0 or len(result.stdout) < 100:
            return []
        
        return parse_bing(result.stdout, limit)
    except Exception as e:
        print(f"Bing 错误：{e}", file=sys.stderr)
        return []


def parse_bing(html: str, limit: int) -> list:
    """解析 Bing 结果 - 最终版"""
    results = []
    
    # 结构：<div class="b_algoheader"><a href="URL"><h2>TITLE</h2></a></div>
    pattern = r'<div class="b_algoheader"><a href="([^"]*)"[^>]*><h2 class="">([^<]*)</h2></a></div>'
    matches = re.findall(pattern, html)
    
    for url, title in matches:
        # 清理
        title = re.sub(r'\s+', ' ', title).strip()
        
        # 过滤无效
        if not title or not url or 'bing.com' in url or url.startswith('#'):
            continue
        
        # 质量评分
        score = 0.5
        if any(d in url for d in ['zhihu.com', 'github.com', 'medium.com', 'wikipedia.org']):
            score += 0.3
        
        results.append({
            'title': title[:200],
            'url': url,
            'snippet': '',
            'source': 'bing',
            'score': min(1.0, score)
        })
        
        if len(results) >= limit:
            break
    
    return results


def search_baidu(query: str, limit: int = 10, timeout: int = 20) -> list:
    """百度搜索"""
    encoded = urllib.parse.quote(query)
    url = f"https://m.baidu.com/s?wd={encoded}&rn={limit * 2}"
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', str(timeout),
             '-A', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
             '-H', 'Accept-Language: zh-CN,zh;q=0.9'],
            capture_output=True, text=True, timeout=timeout + 5
        )
        
        if result.returncode != 0 or len(result.stdout) < 500:
            return []
        
        return parse_baidu(result.stdout, limit)
    except:
        return []


def parse_baidu(html: str, limit: int) -> list:
    """解析百度结果"""
    results = []
    
    # 百度移动端结果
    pattern = r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*c-title[^"]*"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    
    for url, title in matches[:limit * 2]:
        if 'baidu.com' in url or url.startswith('#'):
            continue
        
        title = re.sub(r'\s+', ' ', title).strip()[:200]
        
        score = 0.5
        if any(d in url for d in ['zhihu.com', 'gov.cn', 'csdn.net']):
            score += 0.3
        
        results.append({
            'title': title,
            'url': url,
            'snippet': '',
            'source': 'baidu',
            'score': min(1.0, score)
        })
    
    return results[:limit]


def search(query: str, limit: int = 10) -> list:
    """智能搜索"""
    print(f"🎯 搜索：{query}", file=sys.stderr)
    
    all_results = []
    
    # 1. Bing 优先
    print("🔍 Bing 搜索中...", file=sys.stderr)
    bing_results = search_bing(query, limit * 2)
    if bing_results:
        print(f"✅ Bing 找到 {len(bing_results)} 个结果", file=sys.stderr)
        all_results.extend(bing_results)
    
    # 2. 百度补充
    if len(all_results) < limit:
        print("🔍 百度搜索中...", file=sys.stderr)
        baidu_results = search_baidu(query, limit * 2)
        if baidu_results:
            print(f"✅ 百度找到 {len(baidu_results)} 个结果", file=sys.stderr)
            all_results.extend(baidu_results)
    
    # 3. 去重
    seen = set()
    unique = []
    for r in all_results:
        key = hashlib.md5(r['url'].encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            unique.append(r)
    
    # 4. 按质量分排序
    unique.sort(key=lambda x: -x['score'])
    
    final = unique[:limit]
    print(f"✅ 最终返回 {len(final)} 个结果", file=sys.stderr)
    return final


def format_output(results: list, query: str, fmt: str = 'text') -> str:
    """格式化输出"""
    if fmt == 'json':
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    if fmt == 'markdown':
        output = f"# 搜索结果：{query}\n\n"
        output += f"_搜索时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n"
        for i, r in enumerate(results, 1):
            output += f"## {i}. {r['title']}\n\n"
            output += f"**来源**: {r['source']} | **质量分**: {r['score']:.2f}\n\n"
            output += f"**URL**: {r['url']}\n\n"
            if r['snippet']:
                output += f"**摘要**: {r['snippet']}\n\n"
            output += "---\n\n"
        return output
    
    # 文本格式
    output = f"\n🔍 搜索结果：{query}\n"
    output += f"共找到 {len(results)} 个结果\n\n"
    for i, r in enumerate(results, 1):
        output += f"{i}. {r['title']}\n"
        output += f"   URL: {r['url']}\n"
        output += f"   来源：{r['source']} | 质量分：{r['score']:.2f}\n"
        if r['snippet']:
            output += f"   摘要：{r['snippet'][:100]}...\n"
        output += "\n"
    return output


def main():
    parser = argparse.ArgumentParser(description="Web Search V7")
    parser.add_argument("query", nargs="?", help="搜索查询词")
    parser.add_argument("--limit", "-l", type=int, default=10, help="结果数量")
    parser.add_argument("--format", "-f", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--output", "-o", type=str, help="输出到文件")
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    try:
        results = search(args.query, args.limit)
        output = format_output(results, args.query, args.format)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ 已保存到：{args.output}", file=sys.stderr)
        else:
            print(output)
    
    except Exception as e:
        print(f"❌ 搜索失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
