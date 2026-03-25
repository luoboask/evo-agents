#!/bin/bash

# ============================================================================
# 导购×营销联调自动化工作流 - 完整流程
# ============================================================================
# 功能：执行完整的 7 步联调流程
# 输出：logs/full-flow.log
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$CASE_DIR/logs/full-flow.log"

# 清空日志
> "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "╔════════════════════════════════════════════════════════════╗" | tee -a "$LOG_FILE"
echo "║  🚀 导购×营销联调自动化工作流                              ║" | tee -a "$LOG_FILE"
echo "╚════════════════════════════════════════════════════════════╝" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📅 开始时间：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "📁 案例目录：$CASE_DIR" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

START_TIME=$(date +%s)

# Step 1: 环境准备
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo " 🔔 Step 1/7: 环境准备" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/step1-env.sh"
if [ $? -eq 0 ]; then
    echo "✅ Step 1 完成" | tee -a "$LOG_FILE"
else
    echo "❌ Step 1 失败" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Step 2: 数据构造
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo " 🔔 Step 2/7: 数据构造" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/step2-data.sh"
if [ $? -eq 0 ]; then
    echo "✅ Step 2 完成" | tee -a "$LOG_FILE"
else
    echo "❌ Step 2 失败" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Step 3: 场景验证
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo " 🔔 Step 3/7: 场景验证" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/step3-verify.sh"
if [ $? -eq 0 ]; then
    echo "✅ Step 3 完成" | tee -a "$LOG_FILE"
else
    echo "❌ Step 3 失败" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Step 4: 问题排查
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo " 🔔 Step 4/7: 问题排查" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/step4-debug.sh"
if [ $? -eq 0 ]; then
    echo "✅ Step 4 完成" | tee -a "$LOG_FILE"
else
    echo "❌ Step 4 失败" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Step 5: 自动修复
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo " 🔔 Step 5/7: 自动修复" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/step5-fix.sh"
if [ $? -eq 0 ]; then
    echo "✅ Step 5 完成" | tee -a "$LOG_FILE"
else
    echo "❌ Step 5 失败" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Step 6: 回归验证
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo " 🔔 Step 6/7: 回归验证" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/step6-regression.sh"
if [ $? -eq 0 ]; then
    echo "✅ Step 6 完成" | tee -a "$LOG_FILE"
else
    echo "❌ Step 6 失败" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# Step 7: 报告生成
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo " 🔔 Step 7/7: 报告生成" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
bash "$SCRIPT_DIR/step7-report.sh"
if [ $? -eq 0 ]; then
    echo "✅ Step 7 完成" | tee -a "$LOG_FILE"
else
    echo "❌ Step 7 失败" | tee -a "$LOG_FILE"
    exit 1
fi
echo "" | tee -a "$LOG_FILE"

# 计算总时间
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# 最终总结
echo "╔════════════════════════════════════════════════════════════╗" | tee -a "$LOG_FILE"
echo "║  🎉 联调完成！                                             ║" | tee -a "$LOG_FILE"
echo "╚════════════════════════════════════════════════════════════╝" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📊 执行统计:" | tee -a "$LOG_FILE"
echo "  总步数：7 步" | tee -a "$LOG_FILE"
echo "  状态：全部通过 ✅" | tee -a "$LOG_FILE"
echo "  耗时：${DURATION}秒" | tee -a "$LOG_FILE"
echo "  日志：$LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📄 报告位置:" | tee -a "$LOG_FILE"
echo "  $CASE_DIR/step7-report/final-report.md" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 发送最终通知
echo "📢 通知：联调流程全部完成！" | tee -a "$LOG_FILE"
echo "📢 通知：7 个步骤全部通过 ✅" | tee -a "$LOG_FILE"
echo "📢 通知：报告已生成 - step7-report/final-report.md" | tee -a "$LOG_FILE"
