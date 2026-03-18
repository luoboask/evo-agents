#!/usr/bin/env python3
"""
学习记录同步工具 - 将学习记录同步到知识库
"""

import json
from pathlib import Path
from knowledge_base import KnowledgeBase

class LearningSync:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.learning_dir = Path('/Users/dhr/.openclaw/workspace-ai-baby/memory/learning')
    
    def sync_all(self):
        """同步所有学习记录到知识库"""
        print("=" * 80)
        print("🔄 同步学习记录到知识库")
        print("=" * 80)
        
        # 读取所有学习文件
        learning_files = sorted(self.learning_dir.glob('scheduled_learning_*.jsonl'), reverse=True)
        
        total_synced = 0
        for file_path in learning_files:
            print(f"\n📄 处理文件：{file_path.name}")
            synced = 0
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            learning = json.loads(line)
                            # 检查是否已有 domain 字段（新格式）
                            if 'details' in learning and 'domain' in learning.get('details', {}):
                                self.kb.add_knowledge(learning)
                                synced += 1
                        except Exception as e:
                            pass
            
            print(f"   ✅ 同步 {synced} 条")
            total_synced += synced
        
        print("\n" + "=" * 80)
        print(f"✅ 总共同步 {total_synced} 条知识到知识库")
        
        # 显示统计
        stats = self.kb.get_statistics()
        print(f"\n📊 知识库统计:")
        print(f"   总知识数：{stats['total']}")
        if stats['by_domain']:
            print(f"   领域分布:")
            for item in stats['by_domain'][:5]:
                print(f"     - {item['domain']}: {item['count']} 条")
        
        return total_synced

if __name__ == '__main__':
    sync = LearningSync()
    sync.sync_all()
