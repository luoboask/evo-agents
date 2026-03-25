#!/bin/bash

# Frontend Sandbox 启动脚本
# 快速启动前端沙箱服务器

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=${1:-8080}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " 🔌 Frontend Sandbox 启动中..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 目录：$SCRIPT_DIR"
echo "🔌 端口：http://localhost:$PORT"
echo ""

# 检查 Python 是否可用
if command -v python3 &> /dev/null; then
    echo "✅ 使用 Python3 HTTP 服务器"
    echo ""
    echo "🚀 启动命令：python3 -m http.server $PORT"
    echo ""
    echo "按 Ctrl+C 停止服务器"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cd "$SCRIPT_DIR"
    python3 -m http.server $PORT
    exit 0
fi

# 检查 Node.js 是否可用
if command -v node &> /dev/null; then
    if command -v http-server &> /dev/null; then
        echo "✅ 使用 Node.js http-server"
        echo ""
        echo "🚀 启动命令：http-server -p $PORT"
        echo ""
        echo "按 Ctrl+C 停止服务器"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cd "$SCRIPT_DIR"
        http-server -p $PORT
        exit 0
    else
        echo "⚠️  未找到 http-server，尝试安装..."
        npm install -g http-server 2>/dev/null
        if command -v http-server &> /dev/null; then
            echo "✅ 安装成功，重新启动..."
            cd "$SCRIPT_DIR"
            http-server -p $PORT
            exit 0
        fi
    fi
fi

# 都不可用
echo "❌ 错误：未找到可用的 HTTP 服务器"
echo ""
echo "请安装以下任一工具："
echo "  1. Python 3 (推荐): brew install python3"
echo "  2. Node.js + http-server: npm install -g http-server"
echo ""
exit 1
