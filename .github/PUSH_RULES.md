# GitHub 推送规则

**版本：** v1.0  
**更新日期：** 2026-03-26

---

## 🚨 血泪教训

**问题：** 把特定 Agent 的 workspace 内容推送到通用 GitHub 仓库

**后果：** 
- GitHub 仓库包含了特定 Agent 配置
- 包含了特定项目内容（xhs-research, MediaCrawler 等）
- 需要多次清理才能彻底移除

---

## ✅ 正确流程

### 1️⃣ 先 Clone，再修改

```bash
# ❌ 错误：直接从 workspace 推送
cd ~/.openclaw/workspace-growth-agents
git push origin master

# ✅ 正确：先 clone 到干净目录
cd /tmp
git clone https://github.com/luoboask/evo-agents.git evo-agents-clean
cd evo-agents-clean
```

---

### 2️⃣ 检查特定内容

```bash
# 检查是否有特定 Agent 内容
ls -la agents/
ls -la skills/
ls -la | grep -E "pinterest|xhs|baoyu|MediaCrawler"

# 检查 .gitignore
cat .gitignore | grep -E "agents|skills|data"
```

---

### 3️⃣ 清理特定内容

```bash
# 删除特定 Agent 文件
rm -rf agents/pinterest-agent/
rm -rf agents/xhs-agent/

# 删除特定 skills
rm -rf skills/aura-*/
rm -rf skills/danger-xhs-browser/
rm -rf skills/japan-media-agent/

# 删除特定项目
rm -rf xhs-research/
rm -rf MediaCrawler/
rm -rf baoyu-skills/

# 删除根目录特定文件
rm -f AGENTS.md SOUL.md MEMORY.md USER.md
rm -f prompts/ souls/
```

---

### 4️⃣ 更新 .gitignore

```gitignore
# Agent-specific data
agents/
!agents/.gitkeep

# 特定 Agent 的 skills
skills/aura-*/
skills/danger-xhs-browser/
skills/japan-media-agent/
skills/pinterest-browser-publisher/
skills/star-mansion-master/
skills/tarot-master/

# 特定项目
MediaCrawler/
baoyu-skills/
xhs-research/
prompts/
souls/

# 运行时数据
memory/
data/*/
!data/.gitkeep
.openclaw/
```

---

### 5️⃣ 提交并推送

```bash
git add -A
git commit -m "chore: 清理特定 Agent 内容，保持通用库"
git push origin master
```

---

### 6️⃣ 验证 GitHub

```bash
# 检查 GitHub skills
curl -s https://api.github.com/repos/luoboask/evo-agents/contents/skills | grep '"name"'

# 检查 GitHub agents
curl -s https://api.github.com/repos/luoboask/evo-agents/contents/agents | grep '"name"'

# 应该只看到：
# skills: memory-search, rag, self-evolution, websearch
# agents: .gitkeep
```

---

## 📋 检查清单

推送前必须检查：

- [ ] 已 clone 到干净目录（不是 workspace）
- [ ] 已删除所有特定 Agent 配置
- [ ] 已删除所有特定项目
- [ ] .gitignore 已更新
- [ ] config/agents.yaml 已清理为模板
- [ ] data/ 只保留 .gitkeep
- [ ] agents/ 只保留 .gitkeep
- [ ] 已验证 GitHub 内容

---

## 🎯 通用库应该包含

### ✅ 应该包含

| 类别 | 内容 |
|------|------|
| **skills** | memory-search, rag, self-evolution, websearch |
| **scripts** | 所有通用脚本 |
| **libs** | memory_hub |
| **docs** | 架构文档 |
| **README** | README.md, README.zh-CN.md |
| **指南** | workspace-setup.md, FEATURE_ACTIVATION_GUIDE.md |
| **配置模板** | config/agents.yaml（示例配置） |
| **占位目录** | agents/.gitkeep, data/.gitkeep |

---

### ❌ 不应该包含

| 类别 | 内容 |
|------|------|
| **特定 Agent** | pinterest-agent/, xhs-agent/ 等 |
| **特定 skills** | aura-*/, danger-xhs-browser/ 等 |
| **特定项目** | xhs-research/, MediaCrawler/, baoyu-skills/ |
| **运行时数据** | memory/*.md, data/*/memory/ |
| **Agent 配置** | AGENTS.md, SOUL.md, MEMORY.md, USER.md |
| **个人配置** | prompts/, souls/, .openclaw/ |

---

## 🔄 同步到其他 workspace

推送后，同步改动到其他 Agent 的 workspace：

```bash
# 从 GitHub 拉取最新改动
cd ~/.openclaw/workspace-test-agents
git pull origin master

# 或者手动复制关键文件
cp /tmp/evo-agents-clean/scripts/*.sh ~/.openclaw/workspace-test-agents/scripts/
cp /tmp/evo-agents-clean/*.md ~/.openclaw/workspace-test-agents/
```

---

## 📝 提交信息规范

```bash
# 清理特定内容
git commit -m "chore: 清理特定 Agent 内容，保持通用库

## 删除
- pinterest-agent/ (特定 Agent)
- xhs-research/ (特定项目)
- MediaCrawler/ (特定项目)

## 更新
- .gitignore (排除特定内容)
- config/agents.yaml (清理为模板)"

# 添加新功能
git commit -m "feat: 添加交互式激活脚本

## 新增
- scripts/activate-features.sh
- FEATURE_ACTIVATION_GUIDE.md"
```

---

## 🔗 相关文档

- `CONTRIBUTING.md` - 贡献指南
- `CODE_OF_CONDUCT.md` - 行为准则
- `SECURITY.md` - 安全政策

---

**最后更新：** 2026-03-26  
**维护者：** evo-agents team
