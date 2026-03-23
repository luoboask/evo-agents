# -*- coding: utf-8 -*-
"""
知识管理接口
"""

from pathlib import Path
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional


class KnowledgeInterface:
    """知识管理接口"""
    
    def __init__(self, hub):
        self.hub = hub
        self.workspace_root = hub.workspace_root
        
        # 知识路径
        self.public_path = self.workspace_root / 'public'
        self.private_path = self.workspace_root / 'data' / hub.agent_name / 'knowledge' / 'private'
    
    def add(self, 
            content: str,
            title: str,
            category: str = 'general',
            tags: List[str] = None,
            is_public: bool = False) -> str:
        """添加知识"""
        knowledge_id = str(uuid.uuid4())
        
        knowledge = {
            'id': knowledge_id,
            'title': title,
            'content': content,
            'category': category,
            'tags': tags or [],
            'is_public': is_public,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # 选择路径
        base_path = self.public_path if is_public else self.private_path
        category_path = base_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        # 保存为 JSON 文件
        file_path = category_path / f"{knowledge_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge, f, ensure_ascii=False, indent=2)
        
        # 同时在记忆中心记录
        self.hub.add(
            content=f"知识：{title}",
            memory_type='knowledge',
            metadata={
                'type': 'knowledge',
                'knowledge_id': knowledge_id,
                'category': category,
                'is_public': is_public
            }
        )
        
        return knowledge_id
    
    def search(self,
               query: str,
               category: Optional[str] = None,
               tags: Optional[List[str]] = None,
               include_public: bool = True,
               include_private: bool = True,
               limit: int = 10) -> List[Dict]:
        """搜索知识"""
        results = []
        
        # 搜索公共知识
        if include_public:
            public_results = self._search_directory(self.public_path, query, category, tags)
            results.extend(public_results)
        
        # 搜索私有知识
        if include_private:
            private_results = self._search_directory(self.private_path, query, category, tags)
            results.extend(private_results)
        
        # 按相关性排序
        results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        return results[:limit]
    
    def _search_directory(self,
                         directory: Path,
                         query: str,
                         category: Optional[str],
                         tags: Optional[List[str]]) -> List[Dict]:
        """在指定目录搜索知识"""
        results = []
        
        if not directory.exists():
            return results
        
        # 如果指定了分类，只搜索该分类
        if category:
            directory = directory / category
            if not directory.exists():
                return results
        
        # 遍历所有 JSON 文件
        for file_path in directory.rglob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge = json.load(f)
                
                # 检查是否匹配
                if self._matches_query(knowledge, query, tags):
                    knowledge['source'] = str(file_path.relative_to(self.workspace_root))
                    knowledge['relevance'] = self._calculate_relevance(knowledge, query)
                    results.append(knowledge)
            
            except Exception as e:
                continue
        
        return results
    
    def _matches_query(self, knowledge: Dict, query: str, tags: Optional[List[str]]) -> bool:
        """检查知识是否匹配查询"""
        query_lower = query.lower()
        
        # 搜索标题
        if 'title' in knowledge and query_lower in knowledge['title'].lower():
            return True
        
        # 搜索内容
        if 'content' in knowledge and query_lower in knowledge['content'].lower():
            return True
        
        # 搜索标签
        if tags and 'tags' in knowledge:
            knowledge_tags = [tag.lower() for tag in knowledge['tags']]
            if any(tag in knowledge_tags for tag in tags):
                return True
        
        return False
    
    def _calculate_relevance(self, knowledge: Dict, query: str) -> float:
        """计算相关性分数"""
        score = 0.0
        query_lower = query.lower()
        
        # 标题匹配（最高分）
        if 'title' in knowledge and query_lower in knowledge['title'].lower():
            score += 10.0
        
        # 标签匹配（高分）
        if 'tags' in knowledge:
            if any(query_lower in tag.lower() for tag in knowledge['tags']):
                score += 5.0
        
        # 内容匹配（基础分）
        if 'content' in knowledge and query_lower in knowledge['content'].lower():
            score += 1.0
        
        return score
    
    def get_by_id(self, knowledge_id: str) -> Optional[Dict]:
        """根据 ID 获取知识"""
        # 先在私有知识中查找
        for file_path in self.private_path.rglob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge = json.load(f)
                if knowledge.get('id') == knowledge_id:
                    return knowledge
            except:
                continue
        
        # 再在公共知识中查找
        for file_path in self.public_path.rglob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge = json.load(f)
                if knowledge.get('id') == knowledge_id:
                    return knowledge
            except:
                continue
        
        return None
    
    def list_categories(self, is_public: Optional[bool] = None) -> List[str]:
        """列出所有知识分类"""
        categories = set()
        
        # 公共知识分类
        if is_public is None or is_public:
            if self.public_path.exists():
                for item in self.public_path.iterdir():
                    if item.is_dir():
                        categories.add(f"public/{item.name}")
        
        # 私有知识分类
        if is_public is None or not is_public:
            if self.private_path.exists():
                for item in self.private_path.iterdir():
                    if item.is_dir():
                        categories.add(f"private/{item.name}")
        
        return sorted(list(categories))
