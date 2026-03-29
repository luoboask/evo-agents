#!/bin/bash
# 记忆系统维护脚本 - Memory Maintenance Script
# 添加到 crontab: 0 3 * * 0 /path/to/maintenance.sh

set -e

WORKSPACE="${1:-.}"
cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     记忆系统维护                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "工作目录：$WORKSPACE"
echo "时间：$(date)"
echo ""

# 1. 压缩旧缓存（压缩 30 天前的记录）
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. 压缩旧缓存"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 skills/memory-search/compress.py . --compress 30
echo ""

# 2. 清理旧记忆（清理 90 天前，重要性<3 的记录）
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. 清理旧记忆"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 skills/memory-search/cleanup.py . --cleanup 90 3.0
echo ""

# 3. 清理空文件
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. 清理空文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 skills/memory-search/cleanup.py . --empty
echo ""

# 4. 显示统计
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. 系统统计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 skills/memory-search/compress.py . --stats
echo ""
python3 skills/memory-search/cleanup.py . --stats
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║     ✅ 维护完成！                                       ║"
echo "╚════════════════════════════════════════════════════════╝"
