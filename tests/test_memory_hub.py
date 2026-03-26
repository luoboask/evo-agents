#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Hub 单元测试
测试 libs/memory_hub 模块的所有功能
"""

import sys
import unittest
import sqlite3
from pathlib import Path
from datetime import datetime

# 添加 libs 目录到路径
LIBS_DIR = Path(__file__).parent.parent / 'libs'
sys.path.insert(0, str(LIBS_DIR))

from memory_hub import MemoryHub, Memory, MemoryType


class TestMemoryHubInit(unittest.TestCase):
    """测试用例：Memory Hub 初始化 (TC-MH-001)"""
    
    def setUp(self):
        self.test_agent = 'test-agent-unit'
        self.workspace_root = Path(__file__).parent.parent
    
    def tearDown(self):
        # 清理测试数据库
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        if db_path.exists():
            db_path.unlink()
        # 清理目录
        test_dir = self.workspace_root / 'data' / self.test_agent
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
    
    def test_memory_hub_creation(self):
        """TC-MH-001: Memory Hub 实例创建成功"""
        hub = MemoryHub(self.test_agent)
        self.assertIsNotNone(hub)
        self.assertEqual(hub.agent_name, self.test_agent)
    
    def test_directory_structure_created(self):
        """TC-MH-001: 目录结构自动创建"""
        hub = MemoryHub(self.test_agent)
        expected_path = self.workspace_root / 'data' / self.test_agent / 'memory'
        self.assertTrue(expected_path.exists())
        self.assertTrue(expected_path.is_dir())
    
    def test_stats_returns_dict(self):
        """TC-MH-001: stats() 返回包含 total 键的字典"""
        hub = MemoryHub(self.test_agent)
        stats = hub.stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('total', stats)


class TestMemoryCRUD(unittest.TestCase):
    """测试用例：记忆 CRUD 操作 (TC-MH-002)"""
    
    def setUp(self):
        self.test_agent = 'test-agent-crud'
        self.workspace_root = Path(__file__).parent.parent
        self.hub = MemoryHub(self.test_agent)
    
    def tearDown(self):
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        if db_path.exists():
            db_path.unlink()
        test_dir = self.workspace_root / 'data' / self.test_agent
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
    
    def test_add_memory(self):
        """TC-MH-002.1: 添加记忆成功"""
        memory_id = self.hub.add(
            content='测试内容',
            memory_type='observation',
            importance=5.0,
            tags=['测试', 'unit']
        )
        self.assertIsInstance(memory_id, int)
        self.assertGreater(memory_id, 0)
    
    def test_get_memory(self):
        """TC-MH-002.2: 获取记忆成功"""
        memory_id = self.hub.add(content='测试获取', memory_type='observation')
        memory = self.hub.get(memory_id)
        self.assertIsNotNone(memory)
        self.assertEqual(memory['content'], '测试获取')
    
    def test_search_memory(self):
        """TC-MH-002.3: 搜索记忆成功"""
        self.hub.add(content='测试搜索内容 1', memory_type='observation')
        self.hub.add(content='测试搜索内容 2', memory_type='reflection')
        self.hub.add(content='其他内容', memory_type='observation')
        
        results = self.hub.search(query='测试搜索', top_k=5)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 5)
    
    def test_search_with_type_filter(self):
        """TC-MH-002.4: 按类型过滤搜索"""
        self.hub.add(content='观察内容', memory_type='observation')
        self.hub.add(content='反思内容', memory_type='reflection')
        
        results = self.hub.search(query='内容', top_k=5, memory_type='observation')
        for result in results:
            self.assertEqual(result['memory_type'], 'observation')
    
    def test_update_memory(self):
        """TC-MH-002.5: 更新记忆成功"""
        memory_id = self.hub.add(content='原始内容', memory_type='observation')
        success = self.hub.update(memory_id, content='更新后的内容')
        self.assertTrue(success)
        
        updated = self.hub.get(memory_id)
        self.assertEqual(updated['content'], '更新后的内容')
    
    def test_delete_memory(self):
        """TC-MH-002.6: 删除记忆成功"""
        memory_id = self.hub.add(content='待删除内容', memory_type='observation')
        success = self.hub.delete(memory_id)
        self.assertTrue(success)
        
        deleted = self.hub.get(memory_id)
        self.assertIsNone(deleted)
    
    def test_stats_after_operations(self):
        """TC-MH-002.7: 统计信息正确更新"""
        initial_stats = self.hub.stats()
        initial_count = initial_stats.get('total', 0)
        
        self.hub.add(content='测试 1', memory_type='observation')
        self.hub.add(content='测试 2', memory_type='reflection')
        
        new_stats = self.hub.stats()
        self.assertEqual(new_stats['total'], initial_count + 2)


class TestMemorySearch(unittest.TestCase):
    """测试用例：记忆搜索功能 (TC-MS-001)"""
    
    def setUp(self):
        self.test_agent = 'test-agent-search'
        self.workspace_root = Path(__file__).parent.parent
        self.hub = MemoryHub(self.test_agent)
        
        # 添加测试数据
        test_data = [
            ('Python 编程笔记', 'observation', ['python', 'programming']),
            ('机器学习学习心得', 'reflection', ['ml', 'learning']),
            ('项目会议记录', 'event', ['meeting', 'project']),
            ('代码审查反馈', 'observation', ['code', 'review']),
        ]
        for content, mem_type, tags in test_data:
            self.hub.add(content=content, memory_type=mem_type, tags=tags)
    
    def tearDown(self):
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        if db_path.exists():
            db_path.unlink()
        test_dir = self.workspace_root / 'data' / self.test_agent
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
    
    def test_search_returns_list(self):
        """TC-MS-001.1: 搜索返回 List[Dict] 格式"""
        results = self.hub.search(query='Python', top_k=5)
        self.assertIsInstance(results, list)
        if len(results) > 0:
            self.assertIsInstance(results[0], dict)
    
    def test_search_result_fields(self):
        """TC-MS-001.2: 结果包含必要字段"""
        results = self.hub.search(query='Python', top_k=5)
        if len(results) > 0:
            required_fields = ['content', 'memory_type', 'created_at']
            for field in required_fields:
                self.assertIn(field, results[0])
    
    def test_search_respects_top_k(self):
        """TC-MS-001.3: 结果数量不超过 top_k"""
        results = self.hub.search(query='测试', top_k=3)
        self.assertLessEqual(len(results), 3)
    
    def test_search_relevance(self):
        """TC-MS-001.4: 搜索结果相关性"""
        results = self.hub.search(query='Python 编程', top_k=5)
        if len(results) > 0:
            # 至少有一个结果包含查询关键词
            found_match = any('Python' in r.get('content', '') for r in results)
            self.assertTrue(found_match, "搜索结果中未找到包含关键词的结果")


class TestDatabaseIntegrity(unittest.TestCase):
    """测试用例：数据库完整性 (TC-DB-001)"""
    
    def setUp(self):
        self.test_agent = 'test-agent-db'
        self.workspace_root = Path(__file__).parent.parent
        self.hub = MemoryHub(self.test_agent)
    
    def tearDown(self):
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        if db_path.exists():
            db_path.unlink()
        test_dir = self.workspace_root / 'data' / self.test_agent
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
    
    def test_database_file_created(self):
        """TC-DB-001.1: 数据库文件自动创建"""
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        self.assertTrue(db_path.exists())
    
    def test_memories_table_exists(self):
        """TC-DB-001.2: memories 表存在"""
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        self.assertIn('memories', tables)
    
    def test_table_schema(self):
        """TC-DB-001.3: 表结构符合设计"""
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(memories)")
        columns = {row[1]: row[2] for row in cur.fetchall()}
        conn.close()
        
        required_columns = ['id', 'content', 'memory_type', 'created_at', 'importance']
        for col in required_columns:
            self.assertIn(col, columns)
    
    def test_indexes_exist(self):
        """TC-DB-001.4: 索引存在"""
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cur.fetchall()]
        conn.close()
        
        # 至少应该有自动创建的索引
        self.assertGreater(len(indexes), 0)


class TestEdgeCases(unittest.TestCase):
    """测试用例：边界条件"""
    
    def setUp(self):
        self.test_agent = 'test-agent-edge'
        self.workspace_root = Path(__file__).parent.parent
        self.hub = MemoryHub(self.test_agent)
    
    def tearDown(self):
        db_path = self.workspace_root / 'data' / self.test_agent / 'memory' / 'memory_stream.db'
        if db_path.exists():
            db_path.unlink()
        test_dir = self.workspace_root / 'data' / self.test_agent
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
    
    def test_empty_database_search(self):
        """边界测试：空数据库搜索"""
        results = self.hub.search(query='不存在的词', top_k=5)
        self.assertEqual(len(results), 0)
    
    def test_empty_content(self):
        """边界测试：空内容添加"""
        memory_id = self.hub.add(content='', memory_type='observation')
        self.assertIsInstance(memory_id, int)
    
    def test_special_characters(self):
        """边界测试：特殊字符处理"""
        special_content = "测试特殊字符：!@#$%^&*()_+-=[]{}|;':\",./<>?"
        memory_id = self.hub.add(content=special_content, memory_type='observation')
        retrieved = self.hub.get(memory_id)
        self.assertEqual(retrieved['content'], special_content)
    
    def test_unicode_content(self):
        """边界测试：Unicode 内容"""
        unicode_content = "测试中文 🎉 emoji 🚀 日本語テスト"
        memory_id = self.hub.add(content=unicode_content, memory_type='observation')
        retrieved = self.hub.get(memory_id)
        self.assertEqual(retrieved['content'], unicode_content)
    
    def test_large_content(self):
        """边界测试：大内容处理"""
        large_content = "测试内容 " * 1000  # 约 4KB
        memory_id = self.hub.add(content=large_content, memory_type='observation')
        retrieved = self.hub.get(memory_id)
        self.assertEqual(len(retrieved['content']), len(large_content))
    
    def test_invalid_memory_id(self):
        """边界测试：无效记忆 ID"""
        result = self.hub.get(999999)
        self.assertIsNone(result)
    
    def test_delete_nonexistent(self):
        """边界测试：删除不存在的记忆"""
        success = self.hub.delete(999999)
        self.assertFalse(success)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
