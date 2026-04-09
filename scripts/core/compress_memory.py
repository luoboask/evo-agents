#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆压缩工具 - 帮助压缩超出限制的 MEMORY.md

用法:
    python3 scripts/compress_memory.py [--dry-run]
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.memory_hub.hub import MemoryHub, MEMORY_LIMIT


def analyze_memory(workspace_root: Path) -> dict:
    """分析 MEMORY.md 内容结构"""
    memory_file = workspace_root / 'MEMORY.md'
    if not memory_file.exists():
        return {'error': 'MEMORY.md not found'}
    
    content = memory_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 分析章节
    sections = []
    current_section = {'name': 'Header', 'start': 0, 'lines': 0, 'chars': 0}
    
    for i, line in enumerate(lines):
        if line.startswith('## '):
            if current_section['lines'] > 0:
                sections.append(current_section)
            current_section = {
                'name': line.replace('## ', '').strip(),
                'start': i,
                'lines': 1,
                'chars': len(line)
            }
        else:
            current_section['lines'] += 1
            current_section['chars'] += len(line) + 1  # +1 for newline
    
    if current_section['lines'] > 0:
        sections.append(current_section)
    
    return {
        'total_lines': len(lines),
        'total_chars': len(content),
        'sections': sections,
        'limit': MEMORY_LIMIT,
        'over_by': len(content) - MEMORY_LIMIT
    }


def suggest_compression(analysis: dict) -> list:
    """生成压缩建议"""
    suggestions = []
    
    if analysis['total_chars'] <= MEMORY_LIMIT:
        return ["✅ MEMORY.md 在限制范围内，无需压缩"]
    
    suggestions.append(f"⚠️  超出限制 {analysis['over_by']:,} 字符")
    suggestions.append("")
    
    # 分析各章节大小
    sections = analysis['sections']
    large_sections = [s for s in sections if s['chars'] > 300]
    
    if large_sections:
        suggestions.append("📌 建议压缩以下大章节:")
        for section in sorted(large_sections, key=lambda x: x['chars'], reverse=True)[:5]:
            pct = section['chars'] / analysis['total_chars'] * 100
            suggestions.append(f"   - {section['name']}: {section['chars']:,} chars ({pct:.1f}%)")
        suggestions.append("")
    
    suggestions.append("💡 压缩策略:")
    suggestions.append("   1. 移除冗余描述和重复信息")
    suggestions.append("   2. 合并相关的短条目")
    suggestions.append("   3. 删除过时的上下文")
    suggestions.append("   4. 使用更简洁的表达方式")
    suggestions.append("   5. 将详细信息移到 references/ 目录")
    
    return suggestions


def compress_memory(workspace_root: Path, dry_run: bool = True) -> str:
    """压缩 MEMORY.md"""
    memory_file = workspace_root / 'MEMORY.md'
    if not memory_file.exists():
        return "❌ MEMORY.md not found"
    
    content = memory_file.read_text(encoding='utf-8')
    
    # 简单的压缩策略示例
    compressed = content
    
    # 1. 移除多余空行（保留最多 2 个连续空行）
    import re
    compressed = re.sub(r'\n{3,}', '\n\n', compressed)
    
    # 2. 压缩代码块（如果有的话）
    # 这里可以添加更复杂的逻辑
    
    reduction = len(content) - len(compressed)
    reduction_pct = reduction / len(content) * 100 if content else 0
    
    result = f"""
📊 压缩结果:
   原始：{len(content):,} chars
   压缩后：{len(compressed):,} chars
   减少：{reduction:,} chars ({reduction_pct:.1f}%)
   仍超出：{max(0, len(compressed) - MEMORY_LIMIT):,} chars
"""
    
    if not dry_run and reduction > 0:
        # 备份
        backup = memory_file.parent / f'MEMORY.md.backup.{datetime.now().strftime("%Y%m%d%H%M%S")}'
        memory_file.rename(backup)
        
        # 写入压缩版本
        memory_file.write_text(compressed, encoding='utf-8')
        result += f"\n✅ 已保存到 {memory_file}"
        result += f"\n💾 备份在 {backup}"
    
    return result


def main():
    parser = argparse.ArgumentParser(description='压缩 MEMORY.md 到限制范围内')
    parser.add_argument('--dry-run', action='store_true', help='仅显示结果，不实际修改')
    parser.add_argument('--workspace', type=str, help='Workspace 路径', default=None)
    args = parser.parse_args()
    
    # 确定 workspace 路径
    if args.workspace:
        workspace_root = Path(args.workspace)
    else:
        workspace_root = Path.home() / '.openclaw' / 'workspace'
    
    print("=" * 60)
    print("MEMORY.md 压缩工具")
    print("=" * 60)
    
    # 分析
    print("\n📊 分析 MEMORY.md...")
    analysis = analyze_memory(workspace_root)
    
    if 'error' in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    print(f"   总字符数：{analysis['total_chars']:,}")
    print(f"   限制：{analysis['limit']:,}")
    print(f"   超出：{analysis['over_by']:,} chars")
    print(f"   章节数：{len(analysis['sections'])}")
    
    # 建议
    print("\n💡 压缩建议:")
    suggestions = suggest_compression(analysis)
    for suggestion in suggestions:
        print(suggestion)
    
    # 压缩
    print("\n🔄 执行压缩...")
    result = compress_memory(workspace_root, dry_run=args.dry_run)
    print(result)
    
    # 最终状态
    print("\n📊 最终状态:")
    hub = MemoryHub(agent_name='main', workspace_root=workspace_root)
    usage = hub.get_memory_usage()
    print(f"   当前：{usage['current']:,} chars")
    print(f"   限制：{usage['limit']:,} chars")
    print(f"   使用率：{usage['percentage']}%")
    
    if args.dry_run:
        print("\n⚠️  这是预览模式，使用 --workspace 参数执行实际压缩")


if __name__ == '__main__':
    main()
