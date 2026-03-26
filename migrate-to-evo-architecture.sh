#!/bin/bash
# migrate-to-evo-architecture.sh - 将 growth-agents 迁移到 evo-agents 架构
# 用法：./migrate-to-evo-architecture.sh

set -e

WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKSPACE"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  迁移 growth-agents 到 evo-agents 架构                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 1. 复制核心脚本
echo "📦 复制核心脚本..."

if [ -d "$HOME/.openclaw/workspace-test-agents/scripts" ]; then
    cp "$HOME/.openclaw/workspace-test-agents/scripts/setup-multi-agent.sh" scripts/
    cp "$HOME/.openclaw/workspace-test-agents/scripts/add-agent.sh" scripts/
    chmod +x scripts/setup-multi-agent.sh scripts/add-agent.sh
    echo "   ✅ setup-multi-agent.sh"
    echo "   ✅ add-agent.sh"
else
    echo "   ⚠️  未找到 evo-agents 脚本，请手动复制"
fi

# 2. 复制文档模板
echo ""
echo "📄 复制文档模板..."

# 创建 workspace-setup.md 简版
cat > workspace-setup.md << 'EOF'
# growth-agents Workspace 安装指南

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🎯 概述

growth-agents 是一个基于 evo-agents 架构的 OpenClaw Workspace，专注于个人成长和自进化。

---

## 🚀 快速开始

### 使用已有安装

```bash
cd ~/.openclaw/workspace-growth-agents
```

### 新增子 Agent

```bash
# 批量创建
./scripts/setup-multi-agent.sh researcher writer organizer

# 新增单个
./scripts/add-agent.sh coach "成长教练" 🌱
```

---

## 🤖 多 Agent 管理

### setup-multi-agent.sh - 批量创建

```bash
./scripts/setup-multi-agent.sh <role1> [role2] [role3] ...
```

**示例：**
```bash
./scripts/setup-multi-agent.sh researcher writer organizer
```

### add-agent.sh - 新增单个

```bash
./scripts/add-agent.sh <role> [description] [emoji]
```

**示例：**
```bash
./scripts/add-agent.sh coach "成长教练" 🌱
```

---

## 📁 目录结构

```
growth-agents/
├── 📄 根目录文件
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── MEMORY.md
│   └── USER.md
│
├── 🔧 scripts/
│   ├── setup-multi-agent.sh
│   ├── add-agent.sh
│   └── ...
│
├── 🤖 agents/ (可选)
│   └── <sub-agent>/
│
└── ...
```

---

## 🔗 参考

- evo-agents: https://github.com/luoboask/evo-agents
- OpenClaw: https://github.com/openclaw/openclaw
EOF

echo "   ✅ workspace-setup.md"

# 3. 更新 README
echo ""
echo "📝 更新 README..."

# 在 README 中添加多 Agent 脚本说明
if grep -q "setup-multi-agent" README.md; then
    echo "   ⏭️  README.md 已包含多 Agent 脚本"
else
    cat >> README.md << 'EOF'

---

## 🤖 多 Agent 管理

### setup-multi-agent.sh - 批量创建

```bash
./scripts/setup-multi-agent.sh researcher writer organizer
```

### add-agent.sh - 新增单个

```bash
./scripts/add-agent.sh coach "成长教练" 🌱
```

详见 `workspace-setup.md` 完整文档。
EOF
    echo "   ✅ README.md 已更新"
fi

# 4. 清理不必要的文件
echo ""
echo "🧹 清理不必要的文件..."

# 移动测试脚本到 scripts/
if [ -f "test_all.py" ] && [ ! -f "scripts/test_all.py" ]; then
    mv test_all.py scripts/
    echo "   ✅ 移动 test_all.py 到 scripts/"
fi

if [ -f "init_system.py" ] && [ ! -f "scripts/init_system.py" ]; then
    mv init_system.py scripts/
    echo "   ✅ 移动 init_system.py 到 scripts/"
fi

# 5. 创建 agents/ 目录
echo ""
echo "📁 创建 agents/ 目录..."

if [ ! -d "agents" ]; then
    mkdir -p agents
    touch agents/.gitkeep
    echo "   ✅ 创建 agents/ 目录"
else
    echo "   ⏭️  agents/ 已存在"
fi

# 6. 更新 .gitignore
echo ""
echo "📝 更新 .gitignore..."

if ! grep -q "agents/" .gitignore 2>/dev/null; then
    cat >> .gitignore << 'EOF'

# Agent-specific data
agents/*/memory/
agents/*/data/
EOF
    echo "   ✅ .gitignore 已更新"
else
    echo "   ⏭️  .gitignore 已包含 agents/"
fi

# 7. 输出结果
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     ✅ 迁移完成！                                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 变更总结:"
echo "   ✅ 复制核心脚本（setup-multi-agent.sh, add-agent.sh）"
echo "   ✅ 创建 workspace-setup.md"
echo "   ✅ 更新 README.md"
echo "   ✅ 清理根目录（移动脚本到 scripts/）"
echo "   ✅ 创建 agents/ 目录"
echo "   ✅ 更新 .gitignore"
echo ""
echo "🎯 下一步:"
echo "   1. 测试脚本：./scripts/setup-multi-agent.sh test"
echo "   2. 提交变更：git add -A && git commit -m 'refactor: 迁移到 evo-agents 架构'"
echo "   3. 推送：git push origin master"
echo ""
