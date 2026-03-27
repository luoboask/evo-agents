# GitHub 推送规范

本文档说明如何将 Agent 代码推送到 GitHub 通用模板仓库。

## 🎯 目的

- ✅ 保持 GitHub 仓库为**通用模板**
- ✅ 保护**个人隐私和数据安全**
- ✅ 方便他人 fork 和使用
- ✅ **改造现有 Agent 时不丢失数据**

---

## 📁 目录结构对比

### GitHub 仓库（通用模板）

```
evo-agents/
├── skills/              # 通用技能
│   ├── memory-search
│   ├── rag
│   ├── self-evolution
│   └── web-knowledge
├── scripts/             # 工具脚本
├── docs/                # 文档
├── libs/                # 共享库
├── public/              # 公共模板（空）
├── agents/              # Agent 配置（空）
├── config/              # 配置模板（空）
├── data/                # 数据目录（空）
├── README.md
├── workspace-setup.md
└── .gitignore
```

### 本地 Agent（个人实例）

```
~/.openclaw/workspace-xxx/
├── skills/              # 技能（可能包含特定技能）
├── USER.md              # ⭐ 用户信息（个人）
├── SOUL.md              # ⭐ Agent 人格（个人）
├── IDENTITY.md          # ⭐ 身份标识（个人）
├── MEMORY.md            # ⭐ 长期记忆（个人）
├── memory/              # ⭐ 日常记忆（运行时）
├── public/              # ⭐ 知识库（运行时）
├── agents/              # ⭐ 已注册 Agent（运行时）
└── ...
```

---

## ✅ 应该提交的文件

| 类型 | 示例 | 说明 |
|------|------|------|
| **通用技能** | `skills/memory-search/` | 所有人可用的技能 |
| **工具脚本** | `scripts/*.py` | 通用工具 |
| **文档** | `README.md`, `docs/` | 项目文档 |
| **共享库** | `libs/memory_hub/` | 通用库 |
| **配置模板** | `config/.gitkeep` | 空模板 |
| **安装脚本** | `install.sh` | 一键安装 |

---

## ❌ 不应该提交的文件

| 类型 | 示例 | 原因 |
|------|------|------|
| **个人配置** | `USER.md`, `SOUL.md` | 每个 Agent 自己定义 |
| **运行时数据** | `memory/*.md` | 日常对话记录 |
| **知识库** | `public/*.json` | 用户生成的知识 |
| **Agent 配置** | `agents/*/` | 本地注册信息 |
| **特定技能** | `skills/xxx-agent/` | 特定场景专用 |
| **特定项目** | `MediaCrawler/` | 特定项目代码 |

---

## 🚨 改造现有 Agent 的注意事项

### ⚠️ 重要警告

**如果您是在改造现有 Agent（不是全新安装），必须遵守以下规则：**

### 1. 不要删除个人配置文件

```bash
# ❌ 错误 - 会丢失 Agent 人格和数据
rm USER.md SOUL.md IDENTITY.md MEMORY.md

# ✅ 正确 - 保留个人配置，只清理代码结构
# 保留这些文件（它们在 .gitignore 中，不会被提交）
```

### 2. 不要删除运行时数据

```bash
# ❌ 错误 - 会丢失所有记忆和知识
rm -rf memory/ public/ data/

# ✅ 正确 - 数据保留在本地，只清理 Git 追踪
# 确保 .gitignore 包含：
# memory/
# public/
# data/
```

### 3. 只清理特定技能和项目

```bash
# ✅ 正确 - 只删除特定技能，保留通用技能
cd skills/
rm -rf aura-content-strategist  # 特定技能
rm -rf danger-xhs-browser       # 特定技能
# 保留：memory-search, rag, self-evolution, web-knowledge
```

---

## 📋 推送检查清单

### 新安装 Agent

- [ ] 删除 `USER.md`, `SOUL.md` 等（模板文件，用户自己创建）
- [ ] 清空 `memory/`, `public/`, `data/`
- [ ] 清空 `agents/`, `config/`
- [ ] 保留通用技能
- [ ] 更新 `.gitignore`
- [ ] 推送

### 改造现有 Agent

- [ ] **保留** `USER.md`, `SOUL.md`, `IDENTITY.md`（本地使用）
- [ ] **保留** `memory/`, `public/`, `data/`（本地数据）
- [ ] **保留** `agents/`（已注册 Agent）
- [ ] 删除特定技能（只保留通用技能）
- [ ] 删除特定项目
- [ ] 更新 `.gitignore`（排除个人文件）
- [ ] 检查 `git status`（确认没有个人文件被暂存）
- [ ] 推送

---

## 🔧 操作流程

### 方法 A：手动操作

```bash
# 1. 备份（改造现有 Agent 时必须）
cp -r ~/.openclaw/workspace-xxx /tmp/workspace-backup

# 2. 清理特定技能
cd skills/
rm -rf 特定技能目录

# 3. 清理特定项目
cd ..
rm -rf MediaCrawler baoyu-skills

# 4. 更新 .gitignore
# 确保排除个人文件

# 5. 检查 Git 状态
git status
# 确认 USER.md, memory/, public/ 不在暂存区

# 6. 提交并推送
git add -A
git commit -m "refactor: 清理为通用模板"
git push origin master
```

### 方法 B：使用脚本

```bash
# 使用安全迁移脚本
bash docs/scripts/safe-migrate.sh ~/.openclaw/workspace-xxx
```

---

## 📊 验证推送结果

### 检查 GitHub

```bash
# 检查 skills 目录
curl -s "https://api.github.com/repos/luoboask/evo-agents/contents/skills" | \
  python3 -c "import sys,json; data=json.load(sys.stdin); \
  [print(f'✅ {item[\"name\"]}') for item in data if item['type']=='dir']"

# 应该只看到：
# ✅ memory-search
# ✅ rag
# ✅ self-evolution
# ✅ web-knowledge
```

### 检查本地

```bash
# 检查个人文件是否保留
ls -la USER.md SOUL.md MEMORY.md
# 应该存在（本地使用，不提交）

# 检查 Git 状态
git status
# USER.md, SOUL.md 等应该在 "Untracked files" 中
```

---

## 💡 常见问题

### Q: 我不小心删除了 USER.md，怎么办？

A: 如果是本地删除，从备份恢复。如果是 Git 删除，从历史恢复：
```bash
git checkout <commit-hash>^ -- USER.md SOUL.md
```

### Q: 我的 memory 数据被提交了，怎么办？

A: 立即从 Git 历史中删除：
```bash
git rm --cached memory/*.md
git commit -m "fix: 删除误提交的记忆文件"
git push
# 本地文件会保留
```

### Q: 如何确认没有个人数据被提交？

A: 推送前检查：
```bash
git status
# 查看暂存区文件
git diff --cached --name-only
# 确认没有 USER.md, memory/, public/ 等
```

---

## 📞 需要帮助？

遇到问题？

1. 查看 `docs/MIGRATION.md` - 详细迁移指南
2. 查看 `.gitignore` - 确认排除规则
3. 运行 `git status` - 检查文件状态
4. 提问！- 在 GitHub Issues 中询问

---

**记住：GitHub 是通用模板，个人数据保留在本地！**
