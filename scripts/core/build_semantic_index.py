#!/usr/bin/env python3
"""
构建/更新语义搜索索引

功能:
- 读取所有记忆文件
- 使用 Ollama 生成向量嵌入
- 保存索引到 pickle 文件
- 增量更新（只处理新文件）

用法:
    python3 scripts/core/build_semantic_index.py
    python3 scripts/core/build_semantic_index.py --force  # 强制重建
"""

import argparse
import json
import pickle
import sys
from datetime import datetime
from pathlib import Path

workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root / 'libs'))

from path_utils import resolve_workspace

WORKSPACE = resolve_workspace()
MEMORY_DIR = WORKSPACE / "memory"
INDEX_FILE = MEMORY_DIR / "semantic_index.pkl"
STATE_FILE = MEMORY_DIR / ".semantic_index_state.json"

OLLAMA_HOST = "http://127.0.0.1:11434"


def get_embedding(text, model="nomic-embed-text"):
    """从 Ollama 获取向量嵌入"""
    import urllib.request
    
    data = json.dumps({
        "model": model,
        "prompt": text
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/embeddings",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('embedding', [])
    except Exception as e:
        print(f"⚠️  Embedding 失败：{e}", file=sys.stderr)
        return []


def load_state():
    """加载索引状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'last_build': None, 'files': {}}


def save_state(state):
    """保存索引状态"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def load_memory_files(incremental=False):
    """加载记忆文件"""
    state = load_state() if incremental else None
    documents = []
    
    if MEMORY_DIR.exists():
        for file in sorted(MEMORY_DIR.glob("*.md")):
            if file.name.startswith("2026-"):
                # 增量模式：只处理新文件
                if incremental and state:
                    file_mtime = file.stat().st_mtime
                    if file.name in state.get('files', {}):
                        if state['files'][file.name] >= file_mtime:
                            continue
                
                content = file.read_text(encoding='utf-8')
                paragraphs = content.split('\n\n')
                for i, para in enumerate(paragraphs):
                    if para.strip() and len(para) > 10:
                        documents.append({
                            'source': file.name,
                            'paragraph': i,
                            'content': para.strip()[:500],
                            'full_path': str(file),
                            'mtime': file.stat().st_mtime
                        })
    
    # 加载 MEMORY.md
    memory_md = WORKSPACE / "MEMORY.md"
    if memory_md.exists():
        content = memory_md.read_text(encoding='utf-8')
        documents.append({
            'source': 'MEMORY.md',
            'paragraph': 0,
            'content': content[:2000],
            'full_path': str(memory_md),
            'mtime': memory_md.stat().st_mtime
        })
    
    return documents


def build_index(force=False):
    """构建语义索引"""
    print("🔨 构建语义搜索索引...")
    print("")
    
    # 检查 Ollama
    try:
        import urllib.request
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as response:
            print("✅ Ollama 服务正常")
    except Exception as e:
        print(f"❌ Ollama 服务不可用：{e}")
        print("   请先启动 Ollama: ollama serve")
        return False
    
    # 增量模式
    incremental = not force and INDEX_FILE.exists()
    if incremental:
        print("📥 加载现有索引...")
        print(f"   索引文件：{INDEX_FILE}")
        print("")
    
    # 加载记忆文件
    print("📄 加载记忆文件...")
    documents = load_memory_files(incremental=incremental)
    print(f"   找到 {len(documents)} 个段落")
    
    if not documents:
        print("   ⚠️  没有新内容，跳过")
        return False
    
    # 加载现有索引（增量模式）
    index = []
    if incremental and INDEX_FILE.exists():
        with open(INDEX_FILE, 'rb') as f:
            index = pickle.load(f)
        print(f"   现有索引：{len(index)} 条")
    
    # 生成嵌入
    print("🔢 生成向量嵌入...")
    new_count = 0
    for i, doc in enumerate(documents):
        embedding = get_embedding(doc['content'])
        if embedding:
            index.append({
                'embedding': embedding,
                'source': doc['source'],
                'paragraph': doc['paragraph'],
                'content': doc['content'],
                'full_path': doc['full_path']
            })
            new_count += 1
        
        if (i + 1) % 20 == 0:
            print(f"   处理 {i+1}/{len(documents)}...")
    
    # 保存索引
    print(f"\n💾 保存索引...")
    with open(INDEX_FILE, 'wb') as f:
        pickle.dump(index, f)
    
    # 更新状态
    state = load_state()
    for doc in documents:
        state['files'][doc['source']] = doc['mtime']
    state['last_build'] = datetime.now().isoformat()
    save_state(state)
    
    print(f"   ✅ 索引已保存 ({len(index)} 条，新增 {new_count} 条)")
    print(f"   大小：{INDEX_FILE.stat().st_size / 1024:.1f} KB")
    print("")
    print("✅ 完成")
    print("")
    print("使用语义搜索:")
    print("   python3 skills/memory-search/semantic_search.py \"关键词\"")
    
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="构建语义搜索索引")
    parser.add_argument("--force", action="store_true", help="强制重建索引")
    args = parser.parse_args()
    
    build_index(force=args.force)
