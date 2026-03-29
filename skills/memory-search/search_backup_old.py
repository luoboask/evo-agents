#!/usr/bin/env python3
"""
Memory search - search through memory files.
"""

import argparse
import os
import re
from pathlib import Path
from path_utils import resolve_workspace, resolve_data_dir


def search_memory(query, max_results=5, case_sensitive=False):
    """Search through memory files."""
    workspace = Path(__file__).parent.parent.parent
    memory_dir = workspace / "memory"
    
    results = []
    files_to_search = []
    
    # Collect files
    if memory_dir.exists():
        files_to_search.extend(sorted(memory_dir.glob("*.md"), reverse=True))
    
    memory_file = workspace / "MEMORY.md"
    if memory_file.exists():
        files_to_search.append(memory_file)
    
    # Search
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(query, flags)
    
    for file_path in files_to_search:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = []
                for i, line in enumerate(content.split('\n'), 1):
                    if pattern.search(line):
                        matches.append((i, line.strip()))
                
                if matches:
                    results.append({
                        'file': file_path.name,
                        'path': str(file_path),
                        'matches': matches[:3]  # Max 3 matches per file
                    })
                    
                if len(results) >= max_results:
                    break
        except Exception as e:
            continue
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Search memory files')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--max-results', '-n', type=int, default=5, help='Max results')
    parser.add_argument('--case-sensitive', '-s', action='store_true', help='Case sensitive')
    
    args = parser.parse_args()
    
    results = search_memory(args.query, args.max_results, args.case_sensitive)
    
    if not results:
        print("No results found in memory.")
        return
    
    print(f"\n🔍 Memory search: {args.query}\n")
    
    for r in results:
        print(f"📄 {r['file']}:")
        for line_num, line_text in r['matches']:
            print(f"   Line {line_num}: {line_text[:100]}{'...' if len(line_text) > 100 else ''}")
        print()


if __name__ == '__main__':
    main()
