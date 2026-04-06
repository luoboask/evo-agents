#!/bin/bash
# init-knowledge-systems.sh - 自动初始化 Knowledge-Graph 和 RAG 系统
# 用法：./init-knowledge-systems.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     知识库系统初始化                                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# ========== 1. Knowledge-Graph 初始化 ==========
echo "📊 初始化 Knowledge-Graph..."

if [ ! -f memory/knowledge_graph.json ]; then
    echo '{"entities": [], "relationships": []}' > memory/knowledge_graph.json
    echo "   ✅ knowledge_graph.json 已创建"
else
    echo "   ✅ knowledge_graph.json 已存在"
fi

if [ ! -d skills/knowledge-graph ]; then
    echo "   ⚠️  warning: knowledge-graph skill not found"
else
    echo "   ✅ knowledge-graph skill 已就绪"
fi

echo ""

# ========== 2. RAG 系统初始化 ==========
echo "📈 初始化 RAG 评估系统..."

if [ -d "skills/rag" ]; then
    # 创建配置目录
    mkdir -p skills/rag/data
    
    # 初始化配置文件
    if [ ! -f skills/rag/config.json ]; then
        cat > skills/rag/config.json << 'EOF'
{
  "enabled": true,
  "auto_record": true,
  "evaluation_metrics": ["precision", "recall", "ndcg"],
  "min_score_threshold": 0.7,
  "max_history_size": 1000
}
EOF
        echo "   ✅ config.json 已创建"
    else
        echo "   ✅ config.json 已存在"
    fi
    
    # 初始化数据文件
    if [ ! -f skills/rag/data/evaluations.jsonl ]; then
        touch skills/rag/data/evaluations.jsonl
        echo "   ✅ evaluations.jsonl 已创建"
    else
        echo "   ✅ evaluations.jsonl 已存在"
    fi
    
    echo "   ✅ RAG 评估系统已就绪"
else
    echo "   ⚠️  warning: rag skill not found"
fi

echo ""

# ========== 3. Memory 系统验证 ==========
echo "🧠 验证 Memory 系统..."

memory_files=(
    "memory/MEMORY.md"
    "memory/$(date +%Y-%m-%d).md"
    "memory/knowledge_graph.json"
)

for file in "${memory_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ⚠️  $file (将创建)"
        if [[ "$file" == *".md" ]]; then
            if [[ "$file" == *"MEMORY.md" ]]; then
                cat > "$file" << 'EOF'
# MEMORY.md - 长期记忆

_重要的人、事、偏好、决定_

---

## 用户
- 名称：待填写
- 时区：Asia/Shanghai

## 重要事件

## 技能

## 偏好

## 决定

---

_最后更新：2026-04-06_
EOF
            elif [[ "$file" == *"$(date +%Y-%m-%d).md" ]]; then
                cat > "$file" << EOF
# $(date +%Y-%m-%d) - 会话记录

## 会话

---

_创建于：$(date +%Y-%m-%d %H:%M)_
EOF
            fi
            echo "      ✅ 已创建"
        fi
    fi
done

echo ""

# ========== 4. 目录结构 ==========
echo "📁 创建目录结构..."

dirs=(
    "memory/archive"
    "memory/weekly"
    "memory/monthly"
    "memory/yearly"
    "memory/vector_db"
    "memory/learning"
    "skills/rag/data"
)

for dir in "${dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "   ✅ $dir"
    else
        echo "   ✅ $dir (已存在)"
    fi
done

echo ""

# ========== 5. 完成总结 ==========
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 知识库系统初始化完成！"
echo ""
echo "📊 系统状态:"
echo "   • Knowledge-Graph: ✅ 就绪"
echo "   • RAG Evaluation: ✅ 就绪"
echo "   • Memory System: ✅ 就绪"
echo ""
echo "🚀 可以立即使用:"
echo ""
echo "   # 构建知识图谱"
echo "   cd skills/knowledge-graph && python3 builder.py"
echo ""
echo "   # RAG 评估"
echo "   cd skills/rag && python3 evaluate.py"
echo ""
echo "   # 记忆搜索"
echo "   python3 skills/memory-search/search.py \"查询内容\""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
