#!/bin/bash
# 同步 GitHub 到 Gitee 的脚本

set -e

echo "🔄 开始同步 GitHub → Gitee"

# 1. 确保本地是最新的
echo "📥 拉取 GitHub 最新代码..."
git pull github master

# 2. 推送到 Gitee
echo "📤 推送到 Gitee..."
git push gitee master

# 3. 验证
echo ""
echo "✅ 同步完成！"
echo ""
echo "GitHub: https://github.com/luoboask/evo-agents/commit/$(git rev-parse --short HEAD)"
echo "Gitee:  https://gitee.com/luoboask/evo-agents/commit/$(git rev-parse --short HEAD)"
