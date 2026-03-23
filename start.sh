#!/bin/bash
# ai-baby 快速启动脚本
# 用于初始化、检查和启动自进化系统

set -e

WORKSPACE="/Users/dhr/.openclaw/workspace-ai-baby"
cd "$WORKSPACE"

echo "========================================"
echo "🍼 ai-baby 自进化系统 v5.1"
echo "========================================"
echo ""

# 检查数据库
echo "📊 检查数据库状态..."
python3 skills/memory-search/search_sqlite.py --stats 2>&1 | head -5

# 检查 RAG 日志
RAG_LOG=$(python3 -c "
from pathlib import Path
import yaml
config_path = Path.home() / '.openclaw' / 'workspace-ai-baby-config' / 'config.yaml'
if config_path.exists():
    config = yaml.safe_load(open(config_path))
    print(config.get('rag', {}).get('log_path', ''))
" 2>/dev/null)

if [ -n "$RAG_LOG" ] && [ ! -f "$RAG_LOG" ]; then
    echo "   ⚠️  RAG 日志不存在，创建中..."
    mkdir -p "$(dirname "$RAG_LOG")"
    touch "$RAG_LOG"
fi

echo "   ✅ 数据库检查完成"
echo ""

# 显示当前状态
echo "📈 系统状态:"
echo ""

# 记忆统计
echo "   记忆流:"
python3 skills/memory-search/search_sqlite.py --stats 2>/dev/null | grep -E "总数 | 按类型" | sed 's/^/      /'
echo ""

# RAG 统计
RAG_LOG=$(python3 -c "
from pathlib import Path
import yaml
config_path = Path.home() / '.openclaw' / 'workspace-ai-baby-config' / 'config.yaml'
if config_path.exists():
    config = yaml.safe_load(open(config_path))
    print(config.get('rag', {}).get('log_path', ''))
" 2>/dev/null)

if [ -n "$RAG_LOG" ] && [ -f "$RAG_LOG" ]; then
    RAG_COUNT=$(wc -l < "$RAG_LOG")
    echo "   RAG 评估:"
    echo "      总记录数：$RAG_COUNT"
    if [ "$RAG_COUNT" -ge 10 ]; then
        echo "      ✅ 可以进行自动调优"
    else
        echo "      ⏳ 需要积累更多数据 (当前：$RAG_COUNT/10)"
    fi
else
    echo "   RAG 评估：未激活"
fi
echo ""

# 自进化系统状态
echo "   自进化系统:"
if command -v python3 &> /dev/null; then
    cd skills/self-evolution-5.0
    python3 main.py status 2>&1 | grep -E "记忆 | 进化 | 知识库" | sed 's/^/      /' || echo "      ⚠️  需要初始化"
    cd ../..
fi
echo ""

echo "========================================"
echo "🚀 快速命令"
echo "========================================"
echo ""
echo "   # RAG 评估报告"
echo "   python3 skills/rag/evaluate.py --report --days 7"
echo ""
echo "   # 记忆搜索"
echo "   python3 skills/memory-search/search_sqlite.py \"查询\" --semantic"
echo ""
echo "   # 自进化功能"
echo "   cd skills/self-evolution-5.0 && python3 main.py fractal --limit 10"
echo ""
echo "   # 自动调优（需要 10+ 条 RAG 数据）"
echo "   python3 skills/rag/auto_tune.py --report"
echo ""
echo "========================================"
echo "✨ 准备就绪"
echo "========================================"
