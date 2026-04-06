#!/usr/bin/env python3
"""
网页内容爬取器 - 任意网络知识提取
功能：
1. 单网页爬取 - 提取正文、标题、发布时间等
2. 智能解析 - 识别文章/文档/产品页
3. 内容清洗 - 去除广告、导航、无关元素
4. 多格式输出 - Markdown/JSON/纯文本
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse


class WebCrawler:
    """智能网页爬虫"""
    
    def __init__(self):
        self.workspace = Path("/Users/dhr/.openclaw/workspace")
        self.cache_dir = self.workspace / "memory" / "web_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 超时配置
        self.fetch_timeout = 30
        self.parse_timeout = 10
        
        # User-Agent 池
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        ]
    
    def fetch_page(self, url):
        """获取网页内容"""
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "https://" + url
        
        headers = [
            '-H', f'User-Agent: {self.user_agents[0]}',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '-H', 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
            '-L',  # 跟随重定向
            '--max-time', str(self.fetch_timeout),
            '--connect-timeout', '10',
        ]
        
        # 添加 Referer（模拟从搜索引擎点击）
        if parsed.netloc:
            headers.extend(['-H', f'Referer: https://www.google.com/search?q={parsed.netloc}'])
        
        result = subprocess.run(
            ['curl', '-s'] + headers + [url],
            capture_output=True, text=True, timeout=self.fetch_timeout + 5
        )
        
        if result.returncode != 0:
            raise Exception(f"curl failed: {result.stderr[:200]}")
        
        if not result.stdout or len(result.stdout) < 100:
            raise Exception("页面内容为空或过短")
        
        return result.stdout
    
    def detect_page_type(self, html):
        """检测页面类型"""
        html_lower = html.lower()
        
        # 文章/博客特征
        article_patterns = [
            r'<article', r'class="[^"]*article[^"]*"', r'id="[^"]*article[^"]*"',
            r'<meta[^>]*property="og:type"[^>]*content="article"',
            r'<time[^>]*datetime', r'class="[^"]*post-date[^"]*"',
            r'class="[^"]*author[^"]*"', r'by\s+[\w\s]+',
        ]
        
        # 文档特征
        doc_patterns = [
            r'class="[^"]*doc[^"]*"', r'id="[^"]*documentation[^"]*"',
            r'<code>', r'<pre>', r'class="[^"]*api[^"]*"',
        ]
        
        # 产品页特征
        product_patterns = [
            r'class="[^"]*product[^"]*"', r'"price"', r'"buy"',
            r'<meta[^>]*property="og:type"[^>]*content="product"',
        ]
        
        # 首页/列表页特征
        list_patterns = [
            r'class="[^"]*index[^"]*"', r'class="[^"]*home[^"]*"',
            r'class="[^"]*list[^"]*"', r'<nav[^>]*class="[^"]*pagination',
        ]
        
        article_score = sum(1 for p in article_patterns if re.search(p, html_lower))
        doc_score = sum(1 for p in doc_patterns if re.search(p, html_lower))
        product_score = sum(1 for p in product_patterns if re.search(p, html_lower))
        list_score = sum(1 for p in list_patterns if re.search(p, html_lower))
        
        scores = {
            "article": article_score,
            "document": doc_score,
            "product": product_score,
            "list": list_score,
        }
        
        max_type = max(scores, key=scores.get)
        if scores[max_type] >= 2:
            return max_type, scores
        return "general", scores
    
    def extract_metadata(self, html, url):
        """提取元数据"""
        metadata = {
            "url": url,
            "title": "",
            "author": "",
            "publish_date": "",
            "site_name": "",
            "description": "",
            "language": "zh",
        }
        
        # 标题
        title_patterns = [
            r'<title[^>]*>([^<]+)</title>',
            r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"',
            r'<meta[^>]*name="title"[^>]*content="([^"]*)"',
            r'<h1[^>]*>([^<]+)</h1>',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                metadata["title"] = self._clean_text(match.group(1))
                break
        
        # 作者
        author_patterns = [
            r'<meta[^>]*name="author"[^>]*content="([^"]*)"',
            r'<meta[^>]*property="article:author"[^>]*content="([^"]*)"',
            r'class="[^"]*author[^"]*"[^>]*>([^<]+)</',
            r'by\s+([\w\s]+)\s*(?:on|in|\|)',
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                metadata["author"] = self._clean_text(match.group(1))
                break
        
        # 发布日期
        date_patterns = [
            r'<meta[^>]*property="article:published_time"[^>]*content="([^"]*)"',
            r'<meta[^>]*name="date"[^>]*content="([^"]*)"',
            r'<time[^>]*datetime="([^"]*)"',
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                metadata["publish_date"] = match.group(1)
                break
        
        # 站点名称
        site_patterns = [
            r'<meta[^>]*property="og:site_name"[^>]*content="([^"]*)"',
            r'<meta[^>]*name="site"[^>]*content="([^"]*)"',
        ]
        
        for pattern in site_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                metadata["site_name"] = self._clean_text(match.group(1))
                break
        
        # 描述
        desc_patterns = [
            r'<meta[^>]*name="description"[^>]*content="([^"]*)"',
            r'<meta[^>]*property="og:description"[^>]*content="([^"]*)"',
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                metadata["description"] = self._clean_text(match.group(1))
                break
        
        # 语言检测
        lang_match = re.search(r'<html[^>]*lang="([^"]+)"', html, re.IGNORECASE)
        if lang_match:
            metadata["language"] = lang_match.group(1)[:2]
        
        return metadata
    
    def extract_content(self, html, page_type="general"):
        """提取正文内容"""
        content = []
        
        # 移除不需要的元素
        html = self._remove_unwanted_elements(html)
        
        if page_type == "article":
            # 文章类型：优先提取 article 标签
            article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
            if article_match:
                html = article_match.group(1)
        
        # 提取段落
        paragraph_pattern = r'<p[^>]*>(.*?)</p>'
        paragraphs = re.findall(paragraph_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for p in paragraphs:
            text = self._clean_text(p)
            # 过滤太短的段落（可能是广告或导航）
            if len(text) > 30:
                content.append(text)
        
        # 如果没有段落，尝试提取其他文本
        if not content:
            # 提取所有文本内容
            text_pattern = r'>([^<]+)<'
            texts = re.findall(text_pattern, html)
            for text in texts:
                text = self._clean_text(text)
                if len(text) > 50:
                    content.append(text)
        
        return content
    
    def _remove_unwanted_elements(self, html):
        """移除不需要的元素"""
        # 移除 script 标签
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除 style 标签
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除 noscript 标签
        html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除注释
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # 移除常见广告类名
        ad_patterns = [
            r'<[^>]*class="[^"]*(?:ad|ads|advertisement|banner|promo)[^"]*"[^>]*>.*?</[^>]*>',
            r'<[^>]*id="[^"]*(?:ad|ads|advertisement|banner|promo)[^"]*"[^>]*>.*?</[^>]*>',
        ]
        
        for pattern in ad_patterns:
            html = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除导航
        html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除页脚
        html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        return html
    
    def _clean_text(self, text):
        """清理文本"""
        # 移除 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 解码 HTML 实体
        html_entities = {
            '&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&amp;': '&',
            '&quot;': '"', '&#39;': "'", '&mdash;': '—', '&ndash;': '–',
        }
        for entity, char in html_entities.items():
            text = text.replace(entity, char)
        
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # 移除不可见字符
        text = ''.join(c for c in text if ord(c) >= 32 or c in '\n\r\t')
        
        return text
    
    def crawl(self, url, output_format="markdown"):
        """爬取单个网页"""
        start_time = time.time()
        
        try:
            # 获取页面
            html = self.fetch_page(url)
            
            # 检测页面类型
            page_type, type_scores = self.detect_page_type(html)
            
            # 提取元数据
            metadata = self.extract_metadata(html, url)
            
            # 提取内容
            content = self.extract_content(html, page_type)
            
            # 构建结果
            result = {
                "success": True,
                "url": url,
                "page_type": page_type,
                "type_scores": type_scores,
                "metadata": metadata,
                "content": content,
                "content_length": sum(len(c) for c in content),
                "duration": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
            }
            
            # 格式化输出
            if output_format == "json":
                return json.dumps(result, ensure_ascii=False, indent=2)
            elif output_format == "text":
                output = [f"URL: {url}", f"标题：{metadata['title']}", ""]
                output.extend(content)
                return "\n".join(output)
            else:  # markdown
                output = [
                    f"# {metadata['title'] or '无标题'}",
                    "",
                    f"**URL:** {url}",
                ]
                if metadata.get('author'):
                    output.append(f"**作者:** {metadata['author']}")
                if metadata.get('publish_date'):
                    output.append(f"**日期:** {metadata['publish_date']}")
                if metadata.get('site_name'):
                    output.append(f"**站点:** {metadata['site_name']}")
                output.append("")
                output.append("---")
                output.append("")
                output.extend(content)
                return "\n".join(output)
        
        except Exception as e:
            result = {
                "success": False,
                "url": url,
                "error": str(e),
                "duration": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
            }
            
            if output_format == "json":
                return json.dumps(result, ensure_ascii=False, indent=2)
            else:
                return f"❌ 爬取失败：{url}\n错误：{e}"
    
    def crawl_batch(self, urls, output_format="markdown", max_workers=3):
        """批量爬取"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self._crawl_raw, url): url
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    # 根据输出格式处理
                    if output_format == "json":
                        results.append(result)  # 保持 dict 格式
                    else:
                        results.append(self._format_result(result, output_format))
                except Exception as e:
                    if output_format == "json":
                        results.append({"success": False, "url": url, "error": str(e)})
                    else:
                        results.append(f"❌ {url}: {e}")
        
        return results
    
    def _crawl_raw(self, url):
        """爬取单个网页（返回原始 dict）"""
        start_time = time.time()
        
        try:
            html = self.fetch_page(url)
            page_type, type_scores = self.detect_page_type(html)
            metadata = self.extract_metadata(html, url)
            content = self.extract_content(html, page_type)
            
            return {
                "success": True,
                "url": url,
                "page_type": page_type,
                "type_scores": type_scores,
                "metadata": metadata,
                "content": content,
                "content_length": sum(len(c) for c in content),
                "duration": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "duration": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
            }
    
    def _format_result(self, result, output_format):
        """格式化结果为指定格式"""
        if output_format == "json":
            return json.dumps(result, ensure_ascii=False, indent=2)
        elif output_format == "text":
            output = [f"URL: {result['url']}", f"标题：{result['metadata'].get('title', 'N/A')}", ""]
            if result['success']:
                output.extend(result['content'])
            else:
                output.append(f"错误：{result.get('error', 'Unknown')}")
            return "\n".join(output)
        else:  # markdown
            if not result['success']:
                return f"❌ 爬取失败：{result['url']}\n错误：{result.get('error', 'Unknown')}"
            metadata = result['metadata']
            output = [
                f"# {metadata.get('title', '无标题')}",
                "",
                f"**URL:** {result['url']}",
            ]
            if metadata.get('author'):
                output.append(f"**作者:** {metadata['author']}")
            if metadata.get('publish_date'):
                output.append(f"**日期:** {metadata['publish_date']}")
            if metadata.get('site_name'):
                output.append(f"**站点:** {metadata['site_name']}")
            output.append("")
            output.append("---")
            output.append("")
            output.extend(result['content'])
            return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='网页内容爬取器')
    parser.add_argument('url', nargs='?', help='要爬取的 URL')
    parser.add_argument('--urls', type=str, help='URL 列表文件路径（每行一个 URL）')
    parser.add_argument('--output', '-o', choices=['markdown', 'json', 'text'], default='markdown',
                        help='输出格式')
    parser.add_argument('--workers', type=int, default=3, help='并发工作线程数')
    parser.add_argument('--timeout', type=int, default=30, help='单个页面超时时间（秒）')
    
    args = parser.parse_args()
    
    crawler = WebCrawler()
    crawler.fetch_timeout = args.timeout
    
    urls = []
    if args.url:
        urls.append(args.url)
    if args.urls:
        with open(args.urls, 'r') as f:
            urls.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
    
    if not urls:
        print("❌ 请提供 URL 或使用 --urls 指定文件")
        sys.exit(1)
    
    print(f"🕷️  开始爬取 {len(urls)} 个页面...", file=sys.stderr)
    
    if len(urls) == 1:
        result = crawler.crawl(urls[0], args.output)
        print(result)
    else:
        results = crawler.crawl_batch(urls, args.output, args.workers)
        
        if args.output == "json":
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for i, result in enumerate(results, 1):
                if i > 1:
                    print("\n" + "="*80 + "\n")
                print(result)
    
    print(f"\n✅ 爬取完成", file=sys.stderr)


if __name__ == '__main__':
    main()
