#!/usr/bin/env python3
"""
Web search v5 - 智能增强版（透明集成知识图谱）

改进点：
1. 指数退避重试机制
2. 详细的错误分类和处理
3. 更智能的健康监控
4. 【新增】透明集成知识图谱（用户无感知）
5. 【新增】自动实体识别和关系扩展
6. 【新增】加权排序（文本 + 实体 + 关系）
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
    """智能搜索引擎 - v5 增强版（透明 KG 集成）"""
    
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
        
        # 知识图谱（自动加载，用户无感知）
        self.knowledge_graph = self._load_knowledge_graph()
    
    def _load_knowledge_graph(self):
        """后台加载知识图谱（用户无感知）"""
        kg_file = self.workspace / "memory" / "knowledge_graph.json"
        if kg_file.exists():
            try:
                with open(kg_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def _extract_entities(self, query):
        """从查询中提取实体（后台执行）"""
        if not self.knowledge_graph:
            return []
        
        entities = self.knowledge_graph.get('entities', {})
        found = []
        
        for entity_id, entity_data in entities.items():
            entity_name = entity_data.get('name', '')
            if entity_name and entity_name in query:
                found.append({
                    'id': entity_id,
                    'name': entity_name,
                    'type': entity_data.get('type', 'unknown'),
                    'mentions': entity_data.get('mentions', 0)
                })
        
        return found
    
    def _find_related_entities(self, entity_ids, max_depth=2):
        """通过关系网络找到相关实体（后台执行）"""
        if not self.knowledge_graph:
            return set()
        
        relationships = self.knowledge_graph.get('relationships', [])
        related = set()
        
        # 建立索引
        rel_from = {}
        rel_to = {}
        for rel in relationships:
            from_e = rel.get('from', '')
            to_e = rel.get('to', '')
            weight = rel.get('weight', 1)
            
            if from_e not in rel_from:
                rel_from[from_e] = []
            rel_from[from_e].append((to_e, weight))
            
            if to_e not in rel_to:
                rel_to[to_e] = []
            rel_to[to_e].append((from_e, weight))
        
        # BFS
        queue = [(e, 0) for e in entity_ids]
        visited = set(entity_ids)
        
        while queue:
            current, depth = queue.pop(0)
            if depth >= max_depth:
                continue
            
            for target, weight in (rel_from.get(current, []) + rel_to.get(current, [])):
                if target not in visited:
                    visited.add(target)
                    related.add((target, weight, depth + 1))
                    queue.append((target, depth + 1))
        
        return related
    
    def _enhanced_memory_search(self, query, memories):
        """增强的记忆搜索（透明 KG 集成）"""
        # Step 1: 实体识别
        query_entities = self._extract_entities(query)
        
        # Step 2: 关系扩展
        related_entities = set()
        if query_entities:
            entity_ids = [e['id'] for e in query_entities]
            related_entities = self._find_related_entities(entity_ids)
        
        # Step 3: 加权搜索
        results = []
        query_lower = query.lower()
        
        for memory in memories:
            content = memory.get('content', '')
            
            # 基础文本匹配
            text_score = content.lower().count(query_lower)
            
            # 实体匹配加分
            entity_score = sum(e['mentions'] for e in query_entities if e['name'] in content)
            
            # 相关实体加分
            related_score = sum(
                weight * (1.0 / depth)
                for target, weight, depth in related_entities
                if target in content
            )
            
            total_score = text_score * 1.0 + entity_score * 0.5 + related_score * 0.3
            
            if total_score > 0:
                results.append({
                    'file': memory.get('file', 'unknown'),
                    'score': total_score,
                    'content': content[:500],
                    'date': memory.get('date', '')
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def _update_adaptive_timeout(self):
        """根据历史表现更新超时时间"""
        recent_logs = self._get_recent_logs(1)
        if recent_logs:
            avg_time = sum(l.get("duration", 10) for l in recent_logs) / len(recent_logs)
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
        timeout = self.base_timeout * (2 ** attempt)
        return min(timeout, self.max_timeout)
    
    def health_check(self, engine):
        """检查搜索引擎健康状态"""
        health = self.engine_health[engine]
        if health["last_fail"]:
            time_since_fail = time.time() - health["last_fail"]
            if time_since_fail < 300:
                return False
        if health["fail_count"] >= 3:
            return False
        total = health["success_count"] + health["fail_count"]
        if total > 5 and health["success_count"] / total < 0.5:
            return False
        return health["healthy"]
    
    def mark_result(self, engine, success, error=None):
        """标记搜索结果"""
        if success:
            self.engine_health[engine]["success_count"] += 1
            self.engine_health[engine]["fail_count"] = 0
        else:
            self.engine_health[engine]["fail_count"] += 1
            self.engine_health[engine]["last_fail"] = time.time()
            self.engine_health[engine]["healthy"] = False
    
    def get_best_engine(self):
        """获取最佳搜索引擎"""
        for engine in ["bing", "baidu", "google", "duckduckgo"]:
            if self.health_check(engine):
                return engine
        return "bing"
    
    def search_with_retry(self, query, limit=5, max_retries=3):
        """带重试的搜索"""
        engine = self.get_best_engine()
        attempt = 0
        
        while attempt < max_retries:
            timeout = self._calculate_backoff_timeout(attempt)
            try:
                results = self._search(engine, query, limit, timeout)
                self.mark_result(engine, True)
                return results
            except Exception as e:
                self.mark_result(engine, False, str(e))
                attempt += 1
                if attempt == max_retries:
                    raise
                time.sleep(min(2 ** attempt, 10))
        
        return []
    
    def _search(self, engine, query, limit, timeout):
        """执行搜索"""
        url_templates = {
            "bing": "https://www.bing.com/search?q={query}",
            "baidu": "https://www.baidu.com/s?wd={query}",
            "google": "https://www.google.com/search?q={query}",
            "duckduckgo": "https://html.duckduckgo.com/html/?q={query}",
        }
        
        url = url_templates.get(engine, "").format(query=urllib.parse.quote_plus(query))
        
        cmd = [
            "curl", "-s", "-L",
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "-H", "Accept: text/html,application/xhtml+xml",
            "--max-time", str(timeout),
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode != 0:
            raise Exception(f"cURL failed: {result.stderr}")
        
        return self._parse_results(result.stdout, limit, engine)
    
    def _parse_results(self, html, limit, engine):
        """解析搜索结果"""
        results = []
        
        patterns = {
            "bing": r'<li[^>]*class="b_algo"[^>]*>(.*?)</li>',
            "baidu": r'<div[^>]*class="result"[^>]*>(.*?)</div>',
        }
        
        pattern = patterns.get(engine, "")
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        
        for match in matches[:limit]:
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
                result['snippet'] = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip()
            
            if result:
                results.append(result)
        
        if not results:
            all_links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html, re.IGNORECASE)
            for href, title in all_links[:limit]:
                if 'duckduckgo.com' not in href and not href.startswith('#'):
                    results.append({
                        'url': href,
                        'title': re.sub(r'<[^>]+>', '', title).strip()
                    })
        
        return results[:limit]
    
    def search_memories(self, query, limit=5):
        """搜索记忆文件（透明 KG 增强）"""
        memory_dir = self.workspace / "memory"
        memories = []
        
        for md_file in memory_dir.glob("*.md"):
            if md_file.name.startswith("2026-"):
                content = md_file.read_text(encoding="utf-8")
                memories.append({
                    'file': md_file.name,
                    'content': content,
                    'date': md_file.stem
                })
        
        memory_md = self.workspace / "MEMORY.md"
        if memory_md.exists():
            memories.append({
                'file': 'MEMORY.md',
                'content': memory_md.read_text(encoding="utf-8"),
                'date': 'long-term'
            })
        
        # 使用增强的搜索（透明 KG 集成）
        results = self._enhanced_memory_search(query, memories)
        return results[:limit]


def main():
    parser = argparse.ArgumentParser(description="Web Search - Intelligent Enhanced Version")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    engine = SmartSearchEngine()
    
    try:
        if args.verbose:
            print(f"🔍 Searching for: {args.query}")
            if engine.knowledge_graph:
                print(f"📊 Knowledge Graph: Loaded ({len(engine.knowledge_graph.get('entities', []))} entities)")
            print()
        
        results = engine.search_with_retry(args.query, args.limit)
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 Search results for: {args.query}\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r.get('title', 'No title')}")
                print(f"   {r.get('url', 'No URL')}")
                if r.get('snippet'):
                    snippet = r['snippet'][:200] + '...' if len(r['snippet']) > 200 else r['snippet']
                    print(f"   {snippet}")
                print()
    
    except Exception as e:
        print(f"\n❌ Search failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
