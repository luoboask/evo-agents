# Agent 迁移指南

本文档说明如何将现有 Agent 改造为符合 evo-agents 通用模板结构。

## 🚨 重要警告

**如果您是在改造现有 Agent（不是全新安装），请仔细阅读本节！**

### ❌ 不要删除的文件

改造现有 Agent 时，**必须保留**以下个人配置文件：

```
保留以下文件（每个 Agent 的个人配置）：
├── USER.md          # 用户信息
├── SOUL.md          # Agent 人格
├── IDENTITY.md      # 身份标识
├── MEMORY.md        # 长期记忆
├── HEARTBEAT.md     # 心跳检查配置
├── TOOLS.md         # 本地工具配置
└── AGENTS.md        # 工作区说明（可能有本地修改）
```

### ❌ 不要删除的数据

```
保留以下运行时数据：
├── memory/*.md      # 日常记忆文件
├── memory/*.db      # 记忆数据库
├── memory/*.pkl     # 语义索引
├── public/*/        # 知识库数据
├── data/            # Agent 数据
└── agents/*/        # 已注册的 Agent 配置
```

---

## 📋 改造检查清单

### 第一步：备份

```bash
# 备份整个 workspace
cp -r ~/.openclaw/workspace-growth-agents /tmp/workspace-backup-$(date +%Y%m%d)
echo "✅ 已备份到 /tmp/workspace-backup-$(date +%Y%m%d)"
```

### 第二步：清理特定技能

```bash
cd ~/.openclaw/workspace-growth-agents/skills

# 查看当前技能
ls -la

# 只保留通用技能（删除特定 Agent 的技能）
# 通用技能：
# - memory-search
# - rag
# - self-evolution
# - web-knowledge

# 示例：删除特定技能
rm -rf aura-content-strategist
rm -rf danger-xhs-browser
# ... 其他特定技能
```

### 第三步：清理特定项目

```bash
cd ~/.openclaw/workspace-growth-agents

# 删除特定项目（如果有）
rm -rf MediaCrawler
rm -rf baoyu-skills
rm -rf xhs-research
# ... 其他特定项目
```

### 第四步：更新 .gitignore

确保 `.gitignore` 包含以下排除规则：

```gitignore
# Agent 实例文件（个人配置，不提交）
USER.md
SOUL.md
IDENTITY.md
MEMORY.md
HEARTBEAT.md

# 运行时数据（不提交）
memory/*.md
memory/*.db
memory/*.pkl
public/*/
data/
agents/
```

### 第五步：验证

```bash
# 检查 Git 状态
git status

# 确保以下文件在 Git 中：
# ✅ skills/ (通用技能)
# ✅ docs/
# ✅ scripts/
# ✅ README.md 等文档

# 确保以下文件不在 Git 中（被 .gitignore 排除）：
# ❌ USER.md
# ❌ SOUL.md
# ❌ memory/*.md
# ❌ public/*.json
```

### 第六步：推送

```bash
# 提交变更
git add -A
git commit -m "refactor: 清理为通用 evo-agents 模板"

# 推送到 GitHub
git push origin master
```

---

## 🆚 对比：新安装 vs 改造

| 操作 | 新安装 | 改造现有 |
|------|--------|---------|
| 删除 USER.md 等 | ✅ 可以 | ❌ **禁止** |
| 删除 memory/ | ✅ 可以 | ❌ **禁止** |
| 删除 public/ | ✅ 可以 | ❌ **禁止** |
| 清理特定技能 | ✅ 必须 | ✅ 必须 |
| 更新 .gitignore | ✅ 必须 | ✅ 必须 |

---

## 💡 最佳实践

1. **先备份，再操作** - 永远不要直接删除
2. **使用 git status 检查** - 确认哪些文件会被删除
3. **保留个人配置** - USER.md, SOUL.md 等是 Agent 的灵魂
4. **保留记忆数据** - memory/ 包含所有历史对话
5. **保留知识库** - public/ 包含 RAG 知识

---

## 🔧 快速脚本

```bash
#!/bin/bash
# safe-migrate.sh - 安全迁移脚本

WORKSPACE="$1"

if [ -z "$WORKSPACE" ]; then
    echo "用法：$0 <workspace 目录>"
    exit 1
fi

echo "⚠️  警告：此脚本会清理特定技能，但保留个人配置"
echo "工作区：$WORKSPACE"
read -p "确认继续？(y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
fi

cd "$WORKSPACE/skills"

# 保留的通用技能
KEEP_SKILLS="memory-search rag self-evolution web-knowledge"

# 删除其他技能
for dir in */; do
    skill=$(basename "$dir")
    if [[ ! " $KEEP_SKILLS " =~ " $skill " ]]; then
        echo "🗑️  删除特定技能：$skill"
        rm -rf "$dir"
    fi
done

echo "✅ 清理完成"
echo "⚠️  请手动检查 .gitignore 和 git status"
```

---

## 📞 需要帮助？

如果不确定某个文件是否应该删除：

1. 查看 `.gitignore` - 如果在排除列表中，保留
2. 查看文件内容 - 如果是个人配置，保留
3. 查看 Git 历史 - 如果是通用模板，可以更新
4. 提问！- 在 GitHub Issues 中询问

---

**记住：改造的目的是规范化结构，不是删除数据！**
