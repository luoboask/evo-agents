#!/bin/bash
# 标准测试脚本 - 固定 30 项测试

set -e
WORKSPACE="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     evo-agents 标准测试（30 项固定）                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

TOTAL=0; PASS=0; FAIL=0
test_result() {
    TOTAL=$((TOTAL + 1))
    [ "$1" -eq 0 ] && PASS=$((PASS + 1)) && echo "✅ $2" || { FAIL=$((FAIL + 1)); echo "❌ $2"; }
}

echo "1. 安装验证 (7 项)"
test -d "$WORKSPACE" && test_result 0 "Workspace" || test_result 1 "Workspace"
test -d "$WORKSPACE/scripts/core" && test_result 0 "scripts/core" || test_result 1 "scripts/core"
test -d "$WORKSPACE/skills/memory-search" && test_result 0 "memory-search" || test_result 1 "memory-search"
test -d "$WORKSPACE/skills/rag" && test_result 0 "rag" || test_result 1 "rag"
test -d "$WORKSPACE/skills/self-evolution" && test_result 0 "self-evolution" || test_result 1 "self-evolution"
test -d "$WORKSPACE/skills/web-knowledge" && test_result 0 "web-knowledge" || test_result 1 "web-knowledge"
test -d "$WORKSPACE/libs/memory_hub" && test_result 0 "memory_hub" || test_result 1 "memory_hub"
echo ""

echo "2. 路径系统 (1 项)"
python3 -c "import sys; sys.path.insert(0, 'scripts/core'); from path_utils import resolve_workspace; assert 'workspace-' in str(resolve_workspace())" && test_result 0 "path_utils" || test_result 1 "path_utils"
echo ""

echo "3. 核心功能 (7 项)"
python3 scripts/core/session_recorder.py -t event -c "测试" 2>&1 >/dev/null && test_result 0 "会话记录" || test_result 1 "会话记录"
python3 scripts/core/memory_indexer.py --full 2>&1 >/dev/null && test_result 0 "记忆索引" || test_result 1 "记忆索引"
test -f data/index/memory_index.db && test_result 0 "索引数据库" || test_result 1 "索引数据库"
python3 scripts/core/unified_search.py "测试" 2>&1 | grep -q "搜索" && test_result 0 "记忆搜索" || test_result 1 "记忆搜索"
python3 scripts/core/bridge/bridge_sync.py --agent "$(basename "$WORKSPACE" | sed 's/workspace-//')" 2>&1 | grep -q "双向" && test_result 0 "双向同步" || test_result 1 "双向同步"
python3 scripts/core/health_check.py --agent "$(basename "$WORKSPACE" | sed 's/workspace-//')" 2>&1 | grep -q "检查" && test_result 0 "健康检查" || test_result 1 "健康检查"
python3 scripts/core/self-check.py 2>&1 | grep -q "检查" && test_result 0 "自检功能" || test_result 1 "自检功能"
echo ""

echo "4. 子 Agent (6 项)"
bash scripts/core/add-agent.sh std-test "Standard Test" 🤖 2>&1 | grep -q "创建" && test_result 0 "创建子 agent" || test_result 1 "创建子 agent"
test -d agents/std-test-agent && test_result 0 "子 agent 目录" || test_result 1 "子 agent 目录"
test -L agents/std-test-agent/skills && test_result 0 "skills 符号链接" || test_result 1 "skills 符号链接"
openclaw agents list 2>/dev/null | grep -q "std-test-agent" && test_result 0 "OpenClaw 注册" || test_result 1 "OpenClaw 注册"
cd agents/std-test-agent && python3 ../../scripts/core/session_recorder.py -t event -c "测试" --agent std-test-agent 2>&1 >/dev/null && test_result 0 "子 agent 运行" || test_result 1 "子 agent 运行"
cd ../..
test -d data/std-test-agent && test_result 0 "子 agent 数据" || test_result 1 "子 agent 数据"
echo ""

echo "5. 激活功能 (1 项)"
echo "6" | bash scripts/core/activate-features.sh 2>&1 | grep -q "激活" && test_result 0 "激活所有功能" || test_result 1 "激活所有功能"
echo ""

echo "6. 维护工具 (3 项)"
test -f scripts/core/reinstall.sh && test_result 0 "reinstall.sh" || test_result 1 "reinstall.sh"
test -f scripts/core/uninstall-agent.sh && test_result 0 "uninstall-agent.sh" || test_result 1 "uninstall-agent.sh"
test -f scripts/core/uninstall-workspace.sh && test_result 0 "uninstall-workspace.sh" || test_result 1 "uninstall-workspace.sh"
echo ""

echo "7. 文档 (2 项)"
test -f README.md && test_result 0 "README.md" || test_result 1 "README.md"
test -f docs/TEST_REGRESSION_CHECKLIST.md && test_result 0 "TEST_REGRESSION_CHECKLIST.md" || test_result 1 "TEST_REGRESSION_CHECKLIST.md"
echo ""

echo "8. 数据隔离 (3 项)"
test -d "data/$(basename "$WORKSPACE" | sed 's/workspace-//')" && test_result 0 "主 agent 数据" || test_result 1 "主 agent 数据"
test -d data/std-test-agent && test_result 0 "子 agent 数据" || test_result 1 "子 agent 数据"
HARDCODED=$(grep -rn "my-agent\|demo-agent" skills/ --include="*.py" --include="*.json" 2>/dev/null | grep -v ".git" | grep -v "#" | wc -l)
[ "$HARDCODED" -eq 0 ] && test_result 0 "无硬编码" || test_result 1 "无硬编码 ($HARDCODED)"
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║     测试结果汇总                                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "总计：$TOTAL 项（固定 30 项）"
echo "通过：$PASS 项 ✅"
echo "失败：$FAIL 项 ❌"
[ "$TOTAL" -gt 0 ] && echo "通过率：$((PASS * 100 / TOTAL))%"
echo ""
[ "$FAIL" -eq 0 ] && echo "🎉 所有测试通过！" || echo "⚠️  $FAIL 项失败"

# 清理测试 agent
openclaw agents delete std-test-agent --force 2>/dev/null || true

exit $FAIL
