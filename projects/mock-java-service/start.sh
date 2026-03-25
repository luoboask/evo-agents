#!/bin/bash

echo "======================================"
echo "🚀 启动 MTOP Mock Java 服务"
echo "======================================"
echo ""

cd /Users/dhr/.openclaw/workspace/projects/mock-java-service

# 检查 Maven 是否安装
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven 未安装，请先安装 Maven"
    exit 1
fi

echo "📦 编译项目..."
mvn clean package -DskipTests

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 编译成功！"
    echo ""
    echo "🚀 启动服务..."
    echo ""
    java -jar target/mock-java-service-1.0.0.jar
else
    echo ""
    echo "❌ 编译失败！"
    exit 1
fi
