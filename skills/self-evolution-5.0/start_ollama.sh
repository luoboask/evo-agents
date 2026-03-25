#!/bin/bash
# Ollama 自动启动脚本

echo "🚀 启动 Ollama 服务..."

# 检查是否已经在运行
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama 已经在运行"
    ollama list
else
    echo "⚠️  Ollama 未运行，启动中..."
    # 后台启动 Ollama
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    
    # 等待启动完成
    echo "⏳ 等待 Ollama 启动..."
    for i in {1..10}; do
        if curl -s http://localhost:11434/api/tags > /dev/null; then
            echo "✅ Ollama 启动成功！"
            ollama list
            exit 0
        fi
        sleep 1
    done
    
    echo "❌ Ollama 启动失败，请检查日志：/tmp/ollama.log"
    exit 1
fi
