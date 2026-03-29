#!/usr/bin/env python3
"""
Semantic memory search using Ollama embeddings.
Uses nomic-embed-text for local embedding generation.
"""

import argparse
import json
import numpy as np
import os
import pickle
from datetime import datetime
from pathlib import Path
import sys

# 添加 libs 到路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "libs"))
from path_utils import resolve_workspace, resolve_data_dir


OLLAMA_HOST = "http://127.0.0.1:11434"


def get_embedding(text, model="nomic-embed-text"):
    """Get embedding from Ollama."""
    import urllib.request
    import urllib.error
    
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
        print(f"Error getting embedding: {e}", file=os.sys.stderr)
        return []


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def load_memory_files():
    """Load all memory files."""
    workspace = Path(__file__).parent.parent.parent
    memory_dir = workspace / "memory"
    
    documents = []
    
    # Load daily memory files
    if memory_dir.exists():
        for file_path in sorted(memory_dir.glob("*.md"), reverse=True):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Split into chunks by section
                    sections = content.split('\n## ')
                    for i, section in enumerate(sections):
                        if section.strip():
                            documents.append({
                                'source': file_path.name,
                                'section': i,
                                'content': section.strip()[:1000],  # Limit length
                                'full_path': str(file_path)
                            })
            except Exception as e:
                continue
    
    # Load MEMORY.md
    memory_file = workspace / "MEMORY.md"
    if memory_file.exists():
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append({
                    'source': 'MEMORY.md',
                    'section': 0,
                    'content': content[:2000],
                    'full_path': str(memory_file)
                })
        except Exception as e:
            pass
    
    return documents


def build_index(documents, cache_file=None):
    """Build embedding index for documents."""
    if cache_file and os.path.exists(cache_file):
        print("Loading cached index...")
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    print(f"Building index for {len(documents)} documents...")
    indexed = []
    
    for i, doc in enumerate(documents):
        print(f"  Processing {i+1}/{len(documents)}: {doc['source']}...")
        embedding = get_embedding(doc['content'])
        if embedding:
            doc['embedding'] = embedding
            indexed.append(doc)
    
    if cache_file:
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'wb') as f:
            pickle.dump(indexed, f)
        print(f"Index cached to {cache_file}")
    
    return indexed


def semantic_search(query, index, top_k=5):
    """Search using semantic similarity."""
    query_embedding = get_embedding(query)
    
    if not query_embedding:
        return []
    
    results = []
    for doc in index:
        if 'embedding' in doc:
            similarity = cosine_similarity(query_embedding, doc['embedding'])
            results.append({
                **doc,
                'similarity': similarity
            })
    
    # Sort by similarity
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]


def main():
    parser = argparse.ArgumentParser(description='Semantic memory search with Ollama')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--top-k', '-k', type=int, default=5, help='Number of results')
    parser.add_argument('--rebuild', action='store_true', help='Rebuild index')
    parser.add_argument('--no-cache', action='store_true', help='Do not use cache')
    
    args = parser.parse_args()
    
    cache_file = Path(__file__).parent.parent.parent / "memory" / ".semantic_cache.pkl"
    
    # Load documents
    documents = load_memory_files()
    if not documents:
        print("No memory files found.")
        return
    
    # Build or load index
    if args.rebuild or args.no_cache:
        if args.no_cache and os.path.exists(cache_file):
            os.remove(cache_file)
        index = build_index(documents, cache_file if not args.no_cache else None)
    else:
        index = build_index(documents, cache_file)
    
    if not index:
        print("Failed to build index.")
        return
    
    # Search
    print(f"\n🔍 Semantic search: '{args.query}'\n")
    results = semantic_search(args.query, index, args.top_k)
    
    if not results:
        print("No results found.")
        return
    
    for i, r in enumerate(results, 1):
        similarity = r['similarity'] * 100
        print(f"{i}. [{similarity:.1f}%] {r['source']}")
        content = r['content'][:300]
        if len(r['content']) > 300:
            content += "..."
        print(f"   {content}")
        print()


if __name__ == '__main__':
    main()
