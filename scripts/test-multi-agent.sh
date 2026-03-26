#!/bin/bash
# test-multi-agent.sh - test-agents 多 Agent 完整测试脚本

set -e

WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     test-agents 多 Agent 完整测试                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 测试计数
TOTAL=0
PASSED=0
FAILED=0

# 测试函数
test_case() {
    TOTAL=$((TOTAL + 1))
    local name="$1"
    local cmd="$2"
    
    echo "🧪 测试 $TOTAL: $name"
    if eval "$cmd" > /tmp/test_$TOTAL.log 2>&1; then
        echo "   ✅ 通过"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo "   ❌ 失败"
        echo "   日志：/tmp/test_$TOTAL.log"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 测试阶段 1: 环境检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_case "根目录文件存在" "test -f AGENTS.md"
test_case "SOUL.md 存在" "test -f SOUL.md"
test_case "MEMORY.md 存在" "test -f MEMORY.md"
test_case "agents/analyst-agent 存在" "test -d agents/analyst-agent"
test_case "agents/developer-agent 存在" "test -d agents/developer-agent"
test_case "agents/tester-agent 存在" "test -d agents/tester-agent"
test_case "analyst-agent/memory 存在" "test -d agents/analyst-agent/memory"
test_case "analyst-agent/data 存在" "test -d agents/analyst-agent/data"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 测试阶段 2: 记录事件测试"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

TEST_EVENT="多 Agent 测试-$(date +%Y%m%d%H%M%S)"

test_case "记录事件到 analyst-agent" \
    "python3 scripts/session_recorder.py -t event -c '[$TEST_EVENT] 分析师分析需求' --agent analyst-agent"

test_case "记录事件到 developer-agent" \
    "python3 scripts/session_recorder.py -t event -c '[$TEST_EVENT] 开发者实现方案' --agent developer-agent"

test_case "记录事件到 tester-agent" \
    "python3 scripts/session_recorder.py -t event -c '[$TEST_EVENT] 测试员测试验证' --agent tester-agent"

test_case "记录决策到 test-agents" \
    "python3 scripts/session_recorder.py -t decision -c '[$TEST_EVENT] 采用多 Agent 架构' --agent test-agents"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 测试阶段 3: 数据隔离验证"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_case "analyst-agent 有今日记录" \
    "test -f agents/analyst-agent/memory/$(date +%Y-%m-%d).md"

test_case "developer-agent 有今日记录" \
    "test -f agents/developer-agent/memory/$(date +%Y-%m-%d).md"

test_case "tester-agent 有今日记录" \
    "test -f agents/tester-agent/memory/$(date +%Y-%m-%d).md"

test_case "test-agents 有今日记录" \
    "test -f memory/$(date +%Y-%m-%d).md"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 测试阶段 4: 搜索功能测试"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_case "搜索 analyst-agent 记忆" \
    "python3 scripts/unified_search.py '$TEST_EVENT' --agent analyst-agent --limit 1"

test_case "搜索 developer-agent 记忆" \
    "python3 scripts/unified_search.py '$TEST_EVENT' --agent developer-agent --limit 1"

test_case "搜索 tester-agent 记忆" \
    "python3 scripts/unified_search.py '$TEST_EVENT' --agent tester-agent --limit 1"

test_case "搜索 test-agents 记忆" \
    "python3 scripts/unified_search.py '$TEST_EVENT' --agent test-agents --limit 1"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 测试阶段 5: 统计功能测试"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

test_case "analyst-agent 统计" \
    "python3 scripts/memory_stats.py --agent analyst-agent"

test_case "developer-agent 统计" \
    "python3 scripts/memory_stats.py --agent developer-agent"

test_case "tester-agent 统计" \
    "python3 scripts/memory_stats.py --agent tester-agent"

test_case "test-agents 统计" \
    "python3 scripts/memory_stats.py --agent test-agents"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 测试阶段 6: 数据隔离深度验证"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 写入特定内容
UNIQUE_ANALYST="ANALYST_UNIQUE_$(date +%s)"
UNIQUE_DEVELOPER="DEVELOPER_UNIQUE_$(date +%s)"

python3 scripts/session_recorder.py -t event -c "$UNIQUE_ANALYST" --agent analyst-agent > /dev/null
python3 scripts/session_recorder.py -t event -c "$UNIQUE_DEVELOPER" --agent developer-agent > /dev/null

echo "🔍 验证数据隔离..."

# 验证 analyst-agent 的内容只在 analyst-agent
if grep -q "$UNIQUE_ANALYST" agents/analyst-agent/memory/$(date +%Y-%m-%d).md 2>/dev/null; then
    echo "   ✅ analyst-agent 数据正确写入"
    PASSED=$((PASSED + 1))
    TOTAL=$((TOTAL + 1))
else
    echo "   ❌ analyst-agent 数据写入失败"
    FAILED=$((FAILED + 1))
    TOTAL=$((TOTAL + 1))
fi

# 验证 developer-agent 的内容不在 analyst-agent
if ! grep -q "$UNIQUE_DEVELOPER" agents/analyst-agent/memory/$(date +%Y-%m-%d).md 2>/dev/null; then
    echo "   ✅ 数据隔离正确（developer 内容不在 analyst）"
    PASSED=$((PASSED + 1))
    TOTAL=$((TOTAL + 1))
else
    echo "   ❌ 数据隔离失败（developer 内容泄露到 analyst）"
    FAILED=$((FAILED + 1))
    TOTAL=$((TOTAL + 1))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 测试结果汇总"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "总测试数：$TOTAL"
echo "✅ 通过：$PASSED"
echo "❌ 失败：$FAILED"
echo "成功率：$((PASSED * 100 / TOTAL))%"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 所有测试通过！多 Agent 架构运行正常！"
    exit 0
else
    echo "⚠️  有 $FAILED 个测试失败，请检查日志"
    exit 1
fi
