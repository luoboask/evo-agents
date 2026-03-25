#!/bin/bash

# ============================================================================
# Step 1: 环境准备
# ============================================================================
# 功能：启动 Java Mock 服务和前端开发服务器
# 输出：logs/step1-env.log
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$CASE_DIR/logs/step1-env.log"

echo "========================================" | tee -a "$LOG_FILE"
echo "📍 Step 1: 环境准备" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 创建日志目录
mkdir -p "$CASE_DIR/logs"

# 1.1 检查 Java 服务
echo "🔍 检查 Java Mock 服务..." | tee -a "$LOG_FILE"
if curl -s "http://localhost:8090/mtop/comet/async.api?api=mtop.alibaba.jp.guide.page.get" > /dev/null 2>&1; then
    echo "✅ Java Mock 服务已运行 (http://localhost:8090)" | tee -a "$LOG_FILE"
else
    echo "⚠️  Java Mock 服务未运行，正在启动..." | tee -a "$LOG_FILE"
    cd /Users/dhr/.openclaw/workspace/projects/mock-java-service
    nohup java -jar target/mock-java-service-1.0.0.jar > "$CASE_DIR/logs/java-service.log" 2>&1 &
    sleep 5
    if curl -s "http://localhost:8090/mtop/comet/async.api?api=mtop.alibaba.jp.guide.page.get" > /dev/null 2>&1; then
        echo "✅ Java Mock 服务启动成功" | tee -a "$LOG_FILE"
    else
        echo "❌ Java Mock 服务启动失败" | tee -a "$LOG_FILE"
        exit 1
    fi
fi

# 1.2 检查前端服务
echo "" | tee -a "$LOG_FILE"
echo "🔍 检查前端开发服务器..." | tee -a "$LOG_FILE"
if curl -s "http://localhost:3000/category" > /dev/null 2>&1; then
    echo "✅ 前端开发服务器已运行 (http://localhost:3000)" | tee -a "$LOG_FILE"
else
    echo "⚠️  前端开发服务器未运行" | tee -a "$LOG_FILE"
    echo "ℹ️  请手动启动：cd /Users/dhr/.openclaw/workspace/projects/jp-new-homepage-category-page && npm start" | tee -a "$LOG_FILE"
fi

# 1.3 验证服务连通性
echo "" | tee -a "$LOG_FILE"
echo "🔍 验证服务连通性..." | tee -a "$LOG_FILE"
RESPONSE=$(curl -s "http://localhost:8090/mtop/comet/async.api?api=mtop.alibaba.jp.guide.page.get")
if echo "$RESPONSE" | grep -q "SUCCESS"; then
    echo "✅ Java 服务响应正常" | tee -a "$LOG_FILE"
else
    echo "❌ Java 服务响应异常" | tee -a "$LOG_FILE"
    exit 1
fi

# 1.4 记录环境信息
echo "" | tee -a "$LOG_FILE"
echo "📊 环境信息:" | tee -a "$LOG_FILE"
echo "  Java 服务：http://localhost:8090" | tee -a "$LOG_FILE"
echo "  前端服务：http://localhost:3000" | tee -a "$LOG_FILE"
echo "  日志目录：$CASE_DIR/logs" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "✅ Step 1: 环境准备 完成" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 发送完成通知
echo "📢 通知：Step 1 已完成 - 环境准备就绪" | tee -a "$LOG_FILE"
